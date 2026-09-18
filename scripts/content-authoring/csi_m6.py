#!/usr/bin/env python3
"""C# — Intermediate — Module 6: csi-collections.

Collections & complexity: Dictionary/HashSet/Queue/Stack/LinkedList tradeoffs,
Big-O of operations, choosing structures, IReadOnly surfaces.
Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-collections"

write_module(
    M,
    "Collections & Complexity",
    "Choosing structures by their operation costs, from Dictionary to Queue — with the Big-O to defend the choice.",
    "Bộ sưu tập & Độ phức tạp",
    "Chọn cấu trúc theo chi phí thao tác, từ Dictionary tới Queue — với Big-O để bảo vệ lựa chọn.",
    ["collection-costs", "choosing-structures", "csi-checkpoint-m6"],
    ["csi-p6-collections"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "collection-costs",
    "The Cost Table: Every Operation Has a Price",
    "Big-O for the core collections, why hashing is O(1) *average*, and the memory/behavior tradeoffs.",
    16,
    r"""
## The table worth memorizing (then deriving)

| Structure | Contains/Add | Remove | Notes |
|---|---|---|---|
| `List<T>` | O(n) / O(1)* | O(n) | *amortized; index access O(1) |
| `Dictionary<K,V>` | O(1) avg | O(1) avg | worst O(n) under collisions; no order |
| `HashSet<T>` | O(1) avg | O(1) avg | unique items; set algebra |
| `SortedDictionary<K,V>` | O(log n) | O(log n) | ordered iteration; tree |
| `Queue<T>` / `Stack<T>` | O(1) | O(1) | FIFO / LIFO only |
| `LinkedList<T>` | O(1) at a node | O(1) at a node | find is O(n); no index |

"Average" hides the hash story: buckets + a good `GetHashCode` + `Equals`
consistency. A type whose hash varies with mutable state poisons any
dictionary it sits in — that is why dictionary KEYS are effectively immutable
by convention.

## Amortized growth

`List<T>` doubles capacity when full: occasional O(n) copies, amortized
O(1) appends. Pre-size hot paths — `new List<int>(capacity)` — when you
know the size; the same logic justifies `Dictionary` capacity hints.

## Set algebra exists

```csharp
var a = new HashSet<int> { 1, 2, 3 };
var b = new HashSet<int> { 3, 4 };
a.UnionWith(b);          // a becomes {1,2,3,4}
a.IntersectWith(b); a.ExceptWith(b); a.SymmetricExceptWith(b);
```

Distinct-by-key dedup (`HashSet` on projected keys) is the classic use.

## Check your understanding

- Why is Dictionary "no order"? (Bucket layout; insertion order is an implementation detail.)
- When is LinkedList right? (Splice/insert mid-sequence with a node in hand; rare.)
""",
    "Bảng giá: Mọi thao tác đều có giá",
    "Big-O cho các bộ sưu tập cốt lõi, vì sao hash là O(1) *trung bình*, và các đánh đổi bộ nhớ/hành vi.",
    r"""
## Bảng đáng nhớ (rồi tự suy ra)

| Cấu trúc | Contains/Add | Remove | Ghi chú |
|---|---|---|---|
| `List<T>` | O(n) / O(1)* | O(n) | *khuyếch đại; truy chỉ số O(1) |
| `Dictionary<K,V>` | O(1) trung bình | O(1) tb | xấu nhất O(n) khi đụng độ; không thứ tự |
| `HashSet<T>` | O(1) tb | O(1) tb | phần tử duy nhất; đại số tập hợp |
| `SortedDictionary<K,V>` | O(log n) | O(log n) | duyệt có thứ tự; cây |
| `Queue<T>` / `Stack<T>` | O(1) | O(1) | FIFO / LIFO duy nhất |
| `LinkedList<T>` | O(1) tại node | O(1) tại node | tìm là O(n); không chỉ số |

"Trung bình" che giấu chuyện hash: bucket + `GetHashCode` tốt + `Equals`
nhất quán. Một kiểu có hash thay đổi theo trạng thái biến đổi sẽ đầu độc
mọi dictionary chứa nó — vì vậy KEY của dictionary theo quy ước là bất biến.

## Tăng trưởng khuyếch đại

`List<T>` nhân đôi sức chứa khi đầy: thỉnh thoảng sao chép O(n), cộng cuối
khuyếch đại O(1). Định sẵn kích thước cho đường nóng —
`new List<int>(capacity)` — khi bạn biết kích thước; cùng logic biện minh
cho capacity hint của `Dictionary`.

## Đại số tập hợp có sẵn

```csharp
var a = new HashSet<int> { 1, 2, 3 };
var b = new HashSet<int> { 3, 4 };
a.UnionWith(b);          // a thành {1,2,3,4}
a.IntersectWith(b); a.ExceptWith(b); a.SymmetricExceptWith(b);
```

Khử trùng lặp theo khóa (`HashSet` trên khóa chiếu) là ứng dụng kinh điển.

## Kiểm tra hiểu biết

- Vì sao Dictionary "không thứ tự"? (Bố cục bucket; thứ tự chèn là chi tiết hiện thực.)
- LinkedList đúng lúc nào? (Chèn/nối giữa chuỗi khi cầm node trong tay; hiếm.)
""",
    r"""
## Bảng đáng nhớ (rồi tự suy ra)

| Cấu trúc | Contains/Add | Remove | Ghi chú |
|---|---|---|---|
| `List<T>` | O(n) / O(1)* | O(n) | *khuyếch đại; truy chỉ số O(1) |
| `Dictionary<K,V>` | O(1) trung bình | O(1) tb | xấu nhất O(n) khi đụng độ; không thứ tự |
| `HashSet<T>` | O(1) tb | O(1) tb | phần tử duy nhất; đại số tập hợp |
| `SortedDictionary<K,V>` | O(log n) | O(log n) | duyệt có thứ tự; cây |
| `Queue<T>` / `Stack<T>` | O(1) | O(1) | FIFO / LIFO duy nhất |
| `LinkedList<T>` | O(1) tại node | O(1) tại node | tìm là O(n); không chỉ số |

"Trung bình" che giấu chuyện hash: bucket + `GetHashCode` tốt + `Equals`
nhất quán. Một kiểu có hash thay đổi theo trạng thái biến đổi sẽ đầu độc
mọi dictionary chứa nó — vì vậy KEY của dictionary theo quy ước là bất biến.

## Tăng trưởng khuyếch đại

`List<T>` nhân đôi sức chứa khi đầy: thỉnh thoảng sao chép O(n), cộng cuối
khuyếch đại O(1). Định sẵn kích thước cho đường nóng —
`new List<int>(capacity)` — khi bạn biết kích thước; cùng logic biện minh
cho capacity hint của `Dictionary`.

## Đại số tập hợp có sẵn

```csharp
var a = new HashSet<int> { 1, 2, 3 };
var b = new HashSet<int> { 3, 4 };
a.UnionWith(b);          // a thành {1,2,3,4}
a.IntersectWith(b); a.ExceptWith(b); a.SymmetricExceptWith(b);
```

Khử trùng lặp theo khóa (`HashSet` trên khóa chiếu) là ứng dụng kinh điển.

## Kiểm tra hiểu biết

- Vì sao Dictionary "không thứ tự"? (Bố cục bucket; thứ tự chèn là chi tiết hiện thực.)
- LinkedList đúng lúc nào? (Chèn/nối giữa chuỗi khi cầm node trong tay; hiếm.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "choosing-structures",
    "Choosing Structures: The Frequency-Map Discipline",
    "Worked decisions: counting, eviction, ordering needs, and the readonly surfaces that protect invariants.",
    15,
    r"""
## Start from the access pattern, not the type

Ask in order: (1) keyed lookup? (2) uniqueness? (3) order matters? (4) FIFO/
LIFO? (5) index access? Each answer eliminates half the menu.

- Counting occurrences → `Dictionary<K,int>` (or `Dictionary<K, List<T>>`
  for grouping). This is the **frequency map**, the single most reused
  intermediate structure in application code.
- "Seen before?" → `HashSet<T>`.
- Process in arrival order → `Queue<T>`; undo → `Stack<T>`.
- "Top N by score" → sort once, or a heap-shaped approach; a full sort is
  fine below thousands of items — measure before contorting.

## Protect invariants with readonly surfaces

Methods that shouldn't mutate should accept (and return) readonly views:

```csharp
private readonly Dictionary<string, int> _scores = new();

public IReadOnlyDictionary<string, int> Scores => _scores;   // caller can't Add
public IReadOnlyList<string> Names => _names.AsReadOnly();
```

`IReadOnly*` is a VIEW, not a copy — the caller sees live data but cannot
mutate through that reference. Returning the raw `Dictionary` hands every
caller the keys to your invariants.

## The eviction shape (LRU thinking)

An LRU cache pairs a `Dictionary<K, LinkedListNode<(K,V)>>` with a
`LinkedList`: dictionary for O(1) lookup, list for recency order, node
handles connecting them. You will build a simplified version in the
checkpoint — the point is that *composition* of two structures buys what
neither provides alone.

## Check your understanding

- Why return `IReadOnlyDictionary` instead of a copy? (Zero-cost view; copies hide staleness.)
- Grouping 10k rows by category: what structure? (Dictionary<string, List<Row>>, one pass.)
""",
    "Chọn cấu trúc: Kỷ luật bảng tần suất",
    "Các quyết định được phân tích: đếm, đẩy-ra, nhu cầu thứ tự, và bề mặt readonly bảo vệ bất biến.",
    r"""
## Bắt đầu từ mẫu truy cập, không phải kiểu

Hỏi theo thứ tự: (1) tra theo khóa? (2) tính duy nhất? (3) thứ tự quan trọng?
(4) FIFO/LIFO? (5) truy chỉ số? Mỗi câu trả lời loại một nửa thực đơn.

- Đếm tần suất → `Dictionary<K,int>` (hoặc `Dictionary<K, List<T>>` để nhóm).
  Đây là **bảng tần suất**, cấu trúc trung gian được tái sử dụng nhiều nhất
  trong code ứng dụng.
- "Đã thấy chưa?" → `HashSet<T>`.
- Xử lý theo thứ tự đến → `Queue<T>`; undo → `Stack<T>`.
- "Top N theo điểm" → sắp một lần, hoặc hướng tiếp cận kiểu-heap; sort trọn
  vẹn ổn dưới hàng nghìn phần tử — đo trước khi uốn éo.

## Bảo vệ bất biến bằng bề mặt readonly

Phương thức không nên biến đổi thì nhận (và trả) view chỉ đọc:

```csharp
private readonly Dictionary<string, int> _scores = new();

public IReadOnlyDictionary<string, int> Scores => _scores;   // caller không Add được
public IReadOnlyList<string> Names => _names.AsReadOnly();
```

`IReadOnly*` là VIEW, không phải bản sao — caller thấy dữ liệu sống nhưng
không biến đổi được qua tham chiếu đó. Trả thẳng `Dictionary` trao cho mọi
caller chìa khóa của bất biến của bạn.

## Hình dạng đẩy-ra (tư duy LRU)

Cache LRU ghép `Dictionary<K, LinkedListNode<(K,V)>>` với `LinkedList`:
dictionary cho tra O(1), list cho thứ tự dùng-gần-đây, node handle nối chúng.
Checkpoint sẽ cho bạn dựng bản đơn giản — điểm mấu chốt là *kết hợp* hai cấu
trúc mua được thứ mà không cấu trúc nào cung cấp một mình.

## Kiểm tra hiểu biết

- Vì sao trả `IReadOnlyDictionary` thay vì bản sao? (View chi phí-zero; bản sao che trạng thái cũ.)
- Nhóm 10k dòng theo danh mục: cấu trúc nào? (Dictionary<string, List<Row>>, một lượt duyệt.)
""",
    r"""
## Bắt đầu từ mẫu truy cập, không phải kiểu

Hỏi theo thứ tự: (1) tra theo khóa? (2) tính duy nhất? (3) thứ tự quan trọng?
(4) FIFO/LIFO? (5) truy chỉ số? Mỗi câu trả lời loại một nửa thực đơn.

- Đếm tần suất → `Dictionary<K,int>` (hoặc `Dictionary<K, List<T>>` để nhóm).
  Đây là **bảng tần suất**, cấu trúc trung gian được tái sử dụng nhiều nhất
  trong code ứng dụng.
- "Đã thấy chưa?" → `HashSet<T>`.
- Xử lý theo thứ tự đến → `Queue<T>`; undo → `Stack<T>`.
- "Top N theo điểm" → sắp một lần, hoặc hướng tiếp cận kiểu-heap; sort trọn
  vẹn ổn dưới hàng nghìn phần tử — đo trước khi uốn éo.

## Bảo vệ bất biến bằng bề mặt readonly

Phương thức không nên biến đổi thì nhận (và trả) view chỉ đọc:

```csharp
private readonly Dictionary<string, int> _scores = new();

public IReadOnlyDictionary<string, int> Scores => _scores;   // caller không Add được
public IReadOnlyList<string> Names => _names.AsReadOnly();
```

`IReadOnly*` là VIEW, không phải bản sao — caller thấy dữ liệu sống nhưng
không biến đổi được qua tham chiếu đó. Trả thẳng `Dictionary` trao cho mọi
caller chìa khóa của bất biến của bạn.

## Hình dạng đẩy-ra (tư duy LRU)

Cache LRU ghép `Dictionary<K, LinkedListNode<(K,V)>>` với `LinkedList`:
dictionary cho tra O(1), list cho thứ tự dùng-gần-đây, node handle nối chúng.
Checkpoint sẽ cho bạn dựng bản đơn giản — điểm mấu chốt là *kết hợp* hai cấu
trúc mua được thứ mà không cấu trúc nào cung cấp một mình.

## Kiểm tra hiểu biết

- Vì sao trả `IReadOnlyDictionary` thay vì bản sao? (View chi phí-zero; bản sao che trạng thái cũ.)
- Nhóm 10k dòng theo danh mục: cấu trúc nào? (Dictionary<string, List<Row>>, một lượt duyệt.)
""",
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m6",
    "Checkpoint — The Collection Toolkit",
    "Frequency maps, dedup, queue processing, and an LRU-shaped eviction cache in one graded unit.",
    24,
    r"""
## The gate (mini-build)

Four tools in one graded unit:

1. `Frequency(string text)` → `IReadOnlyDictionary<string, int>` counting
   lowercase whitespace-separated words.
2. `FirstUnique(string text)` → the first word (lowercased) with count 1,
   or null.
3. `ProcessOrders(IEnumerable<string> commands)` — "push X" enqueues, "pop"
   dequeues; returns the join of popped values in order (empty string when
   nothing popped). FIFO, not LIFO.
4. `EvictCache` — a tiny cache with `Put(k, v)` and `Get(k)`: capacity 3;
   `Put` on a full cache evicts the least-recently-used-or-updated key;
   `Get` refreshes recency; `Get` miss returns -1.

Tool 4 is the composition lesson: Dictionary + recency tracking, graded
behaviorally.
""",
    "Checkpoint — Bộ công cụ Bộ sưu tập",
    "Bảng tần suất, khử trùng lặp, xử lý hàng đợi, và cache đẩy-ra hình dạng LRU trong một đơn vị chấm.",
    r"""
## Cổng kiểm tra (mini-build)

Bốn công cụ trong một đơn vị chấm:

1. `Frequency(string text)` → `IReadOnlyDictionary<string, int>` đếm từ cách
   nhau bởi khoảng trắng, chữ thường.
2. `FirstUnique(string text)` → từ đầu tiên (chữ thường) có số đếm 1, hoặc
   null.
3. `ProcessOrders(IEnumerable<string> commands)` — "push X" thêm vào hàng
   đợi, "pop" lấy ra; trả về join các giá trị đã lấy theo thứ tự (chuỗi rỗng
   khi không lấy gì). FIFO, không phải LIFO.
4. `EvictCache` — cache nhỏ với `Put(k, v)` và `Get(k)`: sức chứa 3; `Put`
   khi đầy sẽ đẩy khóa ít-dùng-gần-đây-hoặc-cập-nhật; `Get` làm mới độ gần
   đây; `Get` trượt trả -1.

Công cụ 4 là bài học composition: Dictionary + theo dõi độ gần đây, chấm theo
hành vi.
""",
    challenge(
        "csi-checkpoint-m6-task",
        "Checkpoint: Collections in Anger",
        """Implement the four tools described in the checkpoint:

```csharp
static IReadOnlyDictionary<string, int> Frequency(string text);
static string? FirstUnique(string text);
static string ProcessOrders(IEnumerable<string> commands);
public sealed class EvictCache
{
    public EvictCache(int capacity);
    public void Put(string key, int value);
    public int Get(string key);
}
```""",
        CS_PRELUDE,
        [
            (
                "frequency + first unique",
                r"""
var freq = Solution.Frequency("the cat the dog the bird");
Cj.Eq(freq["the"], 3, "the x3");
Cj.Eq(freq["cat"], 1, "cat x1");
Cj.Eq(freq["bird"], 1, "bird x1");
Cj.Eq(Solution.FirstUnique("the cat the dog the bird"), "cat", "first count-1 in order");
Cj.Eq(Solution.FirstUnique("a a b b"), null, "no unique word");
Cj.Eq(Solution.FirstUnique(""), null, "empty text -> null");
""",
                "Split on whitespace, lowercase, one Dictionary pass; FirstUnique re-walks in original order.",
            ),
            (
                "queue processing",
                r"""
Cj.Eq(Solution.ProcessOrders(new[] { "push a", "push b", "pop", "push c", "pop", "pop" }), "a,b,c", "FIFO order");
Cj.Eq(Solution.ProcessOrders(new[] { "pop", "pop" }), "", "pop empty queue is fine");
Cj.Eq(Solution.ProcessOrders(new[] { "push x" }), "", "no pops, empty result");
""",
                "Queue<string>.Enqueue/Dequeue — Dequeue returns the OLDEST.",
            ),
            (
                "eviction cache",
                r"""
var cache = new Solution.EvictCache(2);
cache.Put("a", 1); cache.Put("b", 2);
Cj.Eq(cache.Get("a"), 1, "hit a");
cache.Put("c", 3);                       // evicts b (a refreshed by Get)
Cj.Eq(cache.Get("b"), -1, "b evicted");
Cj.Eq(cache.Get("a"), 1, "a survives");
cache.Put("a", 10);                      // update refreshes recency too
cache.Put("d", 4);                       // evicts c
Cj.Eq(cache.Get("c"), -1, "c evicted");
Cj.Eq(cache.Get("a"), 10, "a updated value");
""",
                "Dictionary for values + a recency list updated on both Get-hit and Put; evict the tail.",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: Bộ sưu tập trong thực chiến",
        "Hiện thực bốn công cụ mô tả trong checkpoint: bảng tần suất, từ duy nhất đầu tiên, xử lý FIFO, và cache đẩy-ra với độ gần đây được làm mới bởi cả Get và Put.",
        [
            ("frequency + first unique", "Tách theo khoảng trắng, chữ thường, một lượt Dictionary; FirstUnique đi lại theo thứ tự gốc."),
            ("queue processing", "Queue<string>.Enqueue/Dequeue — Dequeue trả phần TỰ GIỮA LÂU NHẤT."),
            ("eviction cache", "Dictionary cho giá trị + danh sách độ gần đây cập nhật trên cả Get-trúng và Put; đẩy đuôi."),
        ],
    ),
    solution='public class Solution\n{\n    public static IReadOnlyDictionary<string, int> Frequency(string text)\n    {\n        var counts = new Dictionary<string, int>();\n        foreach (string raw in text.Split(\' \', System.StringSplitOptions.RemoveEmptyEntries))\n        {\n            string word = raw.ToLowerInvariant();\n            counts[word] = System.Collections.Generic.CollectionExtensions.GetValueOrDefault(counts, word) + 1;\n        }\n        return counts;\n    }\n\n    public static string? FirstUnique(string text)\n    {\n        var counts = new Dictionary<string, int>();\n        var order = new List<string>();\n        foreach (string raw in text.Split(\' \', System.StringSplitOptions.RemoveEmptyEntries))\n        {\n            string word = raw.ToLowerInvariant();\n            if (!counts.ContainsKey(word)) order.Add(word);\n            counts[word] = System.Collections.Generic.CollectionExtensions.GetValueOrDefault(counts, word) + 1;\n        }\n        foreach (string word in order)\n            if (counts[word] == 1) return word;\n        return null;\n    }\n\n    public static string ProcessOrders(IEnumerable<string> commands)\n    {\n        var queue = new Queue<string>();\n        var popped = new List<string>();\n        foreach (string command in commands)\n        {\n            if (command == "pop")\n            {\n                if (queue.Count > 0) popped.Add(queue.Dequeue());\n            }\n            else if (command.StartsWith("push "))\n            {\n                queue.Enqueue(command.Substring(5));\n            }\n        }\n        return string.Join(",", popped);\n    }\n\n    public sealed class EvictCache\n    {\n        private readonly int _capacity;\n        private readonly Dictionary<string, int> _values = new();\n        private readonly List<string> _recency = new();\n\n        public EvictCache(int capacity) => _capacity = capacity;\n\n        public void Put(string key, int value)\n        {\n            if (_values.ContainsKey(key)) _recency.Remove(key);\n            else if (_values.Count >= _capacity)\n            {\n                string oldest = _recency[0];\n                _recency.RemoveAt(0);\n                _values.Remove(oldest);\n            }\n            _values[key] = value;\n            _recency.Add(key);\n        }\n\n        public int Get(string key)\n        {\n            if (!_values.TryGetValue(key, out int v)) return -1;\n            _recency.Remove(key);\n            _recency.Add(key);\n            return v;\n        }\n    }\n}\n',
    wrong='public class Solution\n{\n    public static IReadOnlyDictionary<string, int> Frequency(string text)\n    {\n        var counts = new Dictionary<string, int>();\n        foreach (string raw in text.Split(\' \', System.StringSplitOptions.RemoveEmptyEntries))\n        {\n            string word = raw.ToLowerInvariant();\n            counts[word] = System.Collections.Generic.CollectionExtensions.GetValueOrDefault(counts, word) + 1;\n        }\n        return counts;\n    }\n\n    public static string? FirstUnique(string text)\n    {\n        var counts = new Dictionary<string, int>();\n        foreach (string raw in text.Split(\' \', System.StringSplitOptions.RemoveEmptyEntries))\n        {\n            string word = raw.ToLowerInvariant();\n            counts[word] = System.Collections.Generic.CollectionExtensions.GetValueOrDefault(counts, word) + 1;\n        }\n        // near-miss: dictionary order is insertion order here, but the walk\n        // returns the first word with count 1 WITHOUT preserving first-seen\n        // order when a later duplicate re-adds — the mixed-case test breaks\n        foreach (var pair in counts)\n            if (pair.Value == 1) return pair.Key;\n        return null;\n    }\n\n    public static string ProcessOrders(IEnumerable<string> commands)\n    {\n        var stack = new Stack<string>();\n        var popped = new List<string>();\n        foreach (string command in commands)\n        {\n            if (command == "pop")\n            {\n                if (stack.Count > 0) popped.Add(stack.Pop());\n            }\n            else if (command.StartsWith("push "))\n            {\n                stack.Push(command.Substring(5));\n            }\n        }\n        return string.Join(",", popped);\n    }\n\n    public sealed class EvictCache\n    {\n        private readonly int _capacity;\n        private readonly Dictionary<string, int> _values = new();\n\n        public EvictCache(int capacity) => _capacity = capacity;\n\n        public void Put(string key, int value)\n        {\n            if (_values.Count >= _capacity)\n            {\n                // near-miss: removes an ARBITRARY (first) key, not the least\n                // recently used — "a survives" fails after the refresh path\n                string victim = new List<string>(_values.Keys)[0];\n                _values.Remove(victim);\n            }\n            _values[key] = value;\n        }\n\n        public int Get(string key) =>\n            _values.TryGetValue(key, out int v) ? v : -1;\n    }\n}\n',
)
print("module 6 authored")
