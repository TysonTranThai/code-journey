#!/usr/bin/env python3
"""HSG Intermediate — Module 6: hsgi-segtree (Segment Tree).

Build/query/point-update anatomy over a monoid, max & composite merge,
lazy propagation for range add + range sum, and a graded checkpoint that
composes lazy segtree with coordinate compression of returns.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \n escapes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgi import (
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
#include <map>
#include <cmath>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-segtree"
write_module(
    M,
    "Segment Trees — Range Queries With Range Updates",
    "Build the recursive segment tree, extend it beyond sums with any merge, then add lazy propagation so range updates become O(log n) too.",
    "Cây phân đoạn — Truy vấn đoạn với cập nhật đoạn",
    "Dựng cây phân đoạn đệ quy, mở rộng sang phép hợp bất kỳ, rồi thêm phép lười hóa để cập nhật đoạn cũng chỉ tốn O(log n).",
    ["hsgi-m6-anatomy", "hsgi-m6-beyond-sum", "hsgi-m6-lazy", "hsgi-cp-m6"],
    ["hsgi-p6-segtree"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m6-anatomy",
    "Segment Tree Anatomy — Build, Query, Update",
    "The recursive half-split, O(n) nodes, and the divide-and-conquer query that makes both reads and writes O(log n).",
    18,
    """## The problem Fenwick leaves open

Fenwick gives prefix sums with updates. But "max on a[l..r]" or "count
of values ≥ k on a[l..r]" has no invertible operation — subtraction does
not work. The segment tree (cây phân đoạn) answers arbitrary range
queries with updates, at O(log n) for both.

### The anatomy

Each node covers a segment. A node covering [l, r] with l < r splits at
mid = (l + r) / 2 into [l, mid] and [mid+1, r]; leaves cover single
indices. node[v] stores the MERGE of its two children (sum, max, gcd...).

```cpp
int n;
vector<long long> t;          // 4n space is always safe

void build(const vector<long long>& a, int v, int lo, int hi) {
    if (lo == hi) { t[v] = a[lo]; return; }
    int mid = (lo + hi) / 2;
    build(a, 2*v, lo, mid);
    build(a, 2*v+1, mid+1, hi);
    t[v] = t[2*v] + t[2*v+1];             // merge = sum here
}

long long query(int v, int lo, int hi, int l, int r) {
    if (r < lo || hi < l) return 0;       // identity (0 for sum)
    if (l <= lo && hi <= r) return t[v];  // fully covered
    int mid = (lo + hi) / 2;
    return query(2*v, lo, mid, l, r) + query(2*v+1, mid+1, hi, l, r);
}

void update(int v, int lo, int hi, int i, long long x) {  // a[i] = x
    if (lo == hi) { t[v] = x; return; }
    int mid = (lo + hi) / 2;
    if (i <= mid) update(2*v, lo, mid, i, x);
    else          update(2*v+1, mid+1, hi, i, x);
    t[v] = t[2*v] + t[2*v+1];             // re-merge on the way back up
}
```

### Why O(log n)

- A query decomposes [l, r] into O(log n) disjoint node segments: at
  every level at most 4 nodes are "half-covered", and half-covered nodes
  do not recurse further.
- An update touches exactly one node per level: the path root → leaf i.

### The cost you must not ignore

build is O(n) but RECURSES depth ⌈log₂ n⌉ ≈ 18 for n = 2·10^5 — depth is
fine (≈ 18 frames). But writing build RECURSIVELY over 4·10^5 nodes is
fine; writing a RECURSIVE solution that recurses once per element (like
a linked-list walk) is not. Recursion depth and recursion COUNT are
different budgets (module 1's lesson, in a new costume).

Note the merge must be ASSOCIATIVE (sums, min, max, gcd are; average is
not). Every structure in this module is just "some associative merge".

**Điểm mấu chốt:** segment tree = cây nhị phân trên các đoạn; node lưu
PHÉP HỢP của hai con; query phân rã đoạn thành O(log n) nút rời rạc;
update đi đúng một đường từ gốc đến lá.""",
    "Giải phẫu cây phân đoạn — Dựng, truy vấn, cập nhật",
    "Cách chia đôi đệ quy, O(n) nút, và truy vấn chia để trị cho cả đọc lẫn ghi O(log n).",
    """## Vấn đề Fenwick không giải được

Fenwick mạnh với tổng tiền tố, nhưng "max trên a[l..r]" hay "đếm giá trị
≥ k trên a[l..r]" không có phép đảo ngược — không thể lấy hiệu. Cây phân
đoạn trả lời truy vấn đoạn bất kỳ kèm cập nhật, cả hai O(log n).

### Giải phẫu

Mỗi nút phủ một đoạn. Nút [l, r] với l < r chia tại mid = (l + r) / 2
thành [l, mid] và [mid+1, r]; lá phủ một chỉ số. node[v] lưu PHÉP HỢP
của hai con (tổng, max, gcd...).

```cpp
int n;
vector<long long> t;          // 4n chỗ luôn an toàn

void build(const vector<long long>& a, int v, int lo, int hi) {
    if (lo == hi) { t[v] = a[lo]; return; }
    int mid = (lo + hi) / 2;
    build(a, 2*v, lo, mid);
    build(a, 2*v+1, mid+1, hi);
    t[v] = t[2*v] + t[2*v+1];             // hợp = tổng ở đây
}

long long query(int v, int lo, int hi, int l, int r) {
    if (r < lo || hi < l) return 0;       // phần tử trung tính
    if (l <= lo && hi <= r) return t[v];  // bị phủ hoàn toàn
    int mid = (lo + hi) / 2;
    return query(2*v, lo, mid, l, r) + query(2*v+1, mid+1, hi, l, r);
}

void update(int v, int lo, int hi, int i, long long x) {  // a[i] = x
    if (lo == hi) { t[v] = x; return; }
    int mid = (lo + hi) / 2;
    if (i <= mid) update(2*v, lo, mid, i, x);
    else          update(2*v+1, mid+1, hi, i, x);
    t[v] = t[2*v] + t[2*v+1];             // hợp lại khi đi lên
}
```

### Vì sao O(log n)

- Truy vấn phân rã [l, r] thành O(log n) nút rời rạc: mỗi mức tối đa 4
  nút "phủ một nửa", và nút phủ một nửa không đệ quy sâu hơn.
- Cập nhật đi đúng một nút mỗi mức: đường gốc → lá i.

### Chi phí không được quên

build là O(n), độ sâu đệ quy ⌈log₂ n⌉ ≈ 18 với n = 2·10^5 — an toàn.
Nhưng DEPTH đệ quy và COUNT phép đệ quy là hai ngân sách khác nhau
(bài học module 1 trong bộ áo mới).

Phép hợp phải GIAO HOÁN-KẾT-HỢP (tổng, min, max, gcd có; trung bình
không). Toàn bộ cấu trúc trong module này chỉ là "một phép hợp nào đó".

**Điểm mấu chốt:** cây phân đoạn = cây nhị phân trên đoạn; query phân rã
thành O(log n) nút; update đi một đường.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m6-beyond-sum",
    "Any Merge — Max, Count, Composite",
    "The same skeleton answers max, min, gcd, counts, and pairs of values; only the identity and the merge function change.",
    16,
    """## One skeleton, many merges

Swap the identity and merge, keep everything else:

| merge | identity (out-of-range) | what a range query returns |
| --- | --- | --- |
| sum | 0 | range sum |
| max | −∞ (LLONG_MIN) | range max |
| gcd | 0 | range gcd |
| (count, sum) pair | (0, 0) | count + sum in one query |

### Worked example: range max with point updates

```cpp
struct SegMax {
    int n;
    vector<long long> t;
    SegMax(int n_) : n(n_), t(4 * n_, LLONG_MIN) {}
    void update(int v, int lo, int hi, int i, long long x) {
        if (lo == hi) { t[v] = x; return; }
        int mid = (lo + hi) / 2;
        if (i <= mid) update(2*v, lo, mid, i, x);
        else          update(2*v+1, mid+1, hi, i, x);
        t[v] = max(t[2*v], t[2*v+1]);
    }
    long long query(int v, int lo, int hi, int l, int r) {
        if (r < lo || hi < l) return LLONG_MIN;   // identity
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        return max(query(2*v, lo, mid, l, r),
                   query(2*v+1, mid+1, hi, l, r));
    }
};
```

### The composite trap: (count, sum) vs two trees

Counting "values > k in [l, r]" via two separate trees (one for count,
one for sum) forces two traversals; a single tree of PAIRS (cnt, sum)
merges both in one traversal with
`{a.first + b.first, a.second + b.second}`. Same complexity, half the
constant. When you need two dependent statistics, compose them into one
node type.

### Recognition pattern

"Range query + point update + merge not invertible" → segment tree.
If the merge IS invertible (sum/xor) and updates are point-only,
Fenwick is smaller and faster. Choose deliberately.

**Điểm mấu chốt:** đổi identity + merge là đổi bài toán; hai đại lượng
phụ thuộc nên gộp thành một nút cặp giá trị.""",
    "Phép hợp bất kỳ — Max, đếm, cấu trúc kép",
    "Cùng một bộ khung trả lời max, min, gcd, đếm, hoặc cặp giá trị; chỉ đổi phần tử trung tính và phép hợp.",
    """## Một bộ khung, nhiều phép hợp

Đổi phần tử trung tính và phép hợp, giữ nguyên phần còn lại:

| phép hợp | trung tính (ngoài đoạn) | truy vấn trả về |
| --- | --- | --- |
| tổng | 0 | tổng đoạn |
| max | −∞ (LLONG_MIN) | max đoạn |
| gcd | 0 | gcd đoạn |
| cặp (đếm, tổng) | (0, 0) | đếm + tổng cùng lúc |

### Ví dụ: max đoạn với cập nhật điểm

```cpp
struct SegMax {
    int n;
    vector<long long> t;
    SegMax(int n_) : n(n_), t(4 * n_, LLONG_MIN) {}
    void update(int v, int lo, int hi, int i, long long x) {
        if (lo == hi) { t[v] = x; return; }
        int mid = (lo + hi) / 2;
        if (i <= mid) update(2*v, lo, mid, i, x);
        else          update(2*v+1, mid+1, hi, i, x);
        t[v] = max(t[2*v], t[2*v+1]);
    }
    long long query(int v, int lo, int hi, int l, int r) {
        if (r < lo || hi < l) return LLONG_MIN;   // trung tính
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        return max(query(2*v, lo, mid, l, r),
                   query(2*v+1, mid+1, hi, l, r));
    }
};
```

### Bẫy ghép: (đếm, tổng) và hai cây

Đếm "giá trị > k trong [l, r]" bằng hai cây riêng (một cây đếm, một cây
tổng) buộc hai lần duyệt; một cây duy nhất lưu CẶP (cnt, sum) hợp cả hai
trong một lần duyệt với `{a.first + b.first, a.second + b.second}`. Cùng
độ phức tạp, hằng số nhỏ hơn. Khi hai đại lượng PHỤ THUỘC nhau, gộp thành
một kiểu nút.

### Mẫu nhận diện

"Truy vấn đoạn + cập nhật điểm + phép hợp không đảo ngược" → cây phân
đoạn. Nếu phép hợp CÓ đảo ngược (tổng/xor) và chỉ có cập nhật điểm,
Fenwick gọn và nhanh hơn. Chọn có chủ đích.

**Điểm mấu chốt:** identity + merge định nghĩa bài toán; đại lượng kép →
nút cặp.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 3
write_lesson(
    M,
    "hsgi-m6-lazy",
    "Lazy Propagation — Range Updates, Range Queries",
    "The lazy tag: defer a segment-wide change by storing it at the covering node and pushing it down only when a descent visits.",
    20,
    """## The gap

Add x to every a[i] in [l, r] — that is 2·10^5 point updates, O(n log n)
per operation: dead. Lazy propagation (lười hóa) makes RANGE updates
O(log n) too.

### The invariant

A node fully covered by an update does not descend. It applies the
change to its own value instantly (for range ADD of x on a node covering
k elements: value += x·k) and records a TAG: "everything below me still
owes +x". The tag is only pushed to children when some later operation
actually walks through the node.

```cpp
struct LazySeg {                       // range add, range sum
    int n;
    vector<long long> t, lz;           // t[v] = sum of node segment
    LazySeg(int n_) : n(n_), t(4*n_), lz(4*n_) {}
    void push(int v, int lo, int mid, int hi) {   // hand tag to children
        if (lz[v]) {
            t[2*v]   += lz[v] * (mid - lo + 1);
            t[2*v+1] += lz[v] * (hi - mid);
            lz[2*v]   += lz[v];        // tags ADD (for additive updates)
            lz[2*v+1] += lz[v];
            lz[v] = 0;
        }
    }
    void add(int v, int lo, int hi, int l, int r, long long x) {
        if (r < lo || hi < l) return;
        if (l <= lo && hi <= r) {      // fully covered: stop, tag it
            t[v] += x * (hi - lo + 1);
            lz[v] += x;
            return;
        }
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        add(2*v, lo, mid, l, r, x);
        add(2*v+1, mid+1, hi, l, r, x);
        t[v] = t[2*v] + t[2*v+1];
    }
    long long query(int v, int lo, int hi, int l, int r) {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);          // must push before descending
        return query(2*v, lo, mid, l, r) + query(2*v+1, mid+1, hi, l, r);
    }
};
```

### The two classic bugs

1. **Forgetting to push before descending** in query — reads stale
   values below an unpushed tag. (In `add`, push happens implicitly by
   recursing after push; in query it is the only place children learn
   the tag.)
2. **Tag composition wrong for the update type.** For range ADD, tags
   accumulate additively (lz[child] += lz[parent]). For range ASSIGN
   (set a[i] := x), tags OVERRIDE (lz[child] = x) and you need a "no
   tag" sentinel. Mixing the two rules is a silent wrong answer.

### Amortized honesty

Each operation pushes O(log n) tags along one root path — worst case is
genuinely O(log n) per op, not amortized. n, q = 2·10^5 gives
2·10^5 · 18 · (tag ops) ≈ 10^7·(constant): comfortably inside budget.

**Điểm mấu chốt:** node phủ toàn bộ → áp dụng ngay + đặt tag, không đi
xuống; push CHỈ xảy ra khi có thao tác đi qua; quy tắc cộng tag phụ thuộc
loại cập nhật (cộng ↔ cộng, gán ↔ ghi đè).""",
    "Lười hóa — Cập nhật đoạn, truy vấn đoạn",
    "Tag lười: hoãn thay đổi cả đoạn tại nút phủ, chỉ đẩy xuống khi có thao tác đi qua.",
    """## Khoảng trống

Cộng x vào mọi a[i] trong [l, r] — tức 2·10^5 cập nhật điểm, O(n log n)
mỗi thao tác: chết. Lười hóa đưa CẬP NHẬT ĐOẠN về O(log n).

### Bất biến thức

Nút bị phủ toàn bộ KHÔNG đi xuống. Nó áp thay đổi lên giá trị của chính
mình ngay lập tức (cộng đoạn x trên nút phủ k phần tử: value += x·k) và
ghi TAG: "mọi thứ bên dưới còn nợ +x". Tag chỉ bị đẩy xuống con khi một
thao tác sau này thực sự đi qua nút.

```cpp
struct LazySeg {                       // cộng đoạn, tổng đoạn
    int n;
    vector<long long> t, lz;           // t[v] = tổng của nút
    LazySeg(int n_) : n(n_), t(4*n_), lz(4*n_) {}
    void push(int v, int lo, int mid, int hi) {   // trao tag cho con
        if (lz[v]) {
            t[2*v]   += lz[v] * (mid - lo + 1);
            t[2*v+1] += lz[v] * (hi - mid);
            lz[2*v]   += lz[v];        // tag CỘNG dồn (cập nhật cộng)
            lz[2*v+1] += lz[v];
            lz[v] = 0;
        }
    }
    void add(int v, int lo, int hi, int l, int r, long long x) {
        if (r < lo || hi < l) return;
        if (l <= lo && hi <= r) {      // phủ trọn: dừng, đặt tag
            t[v] += x * (hi - lo + 1);
            lz[v] += x;
            return;
        }
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        add(2*v, lo, mid, l, r, x);
        add(2*v+1, mid+1, hi, l, r, x);
        t[v] = t[2*v] + t[2*v+1];
    }
    long long query(int v, int lo, int hi, int l, int r) {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);          // phải push trước khi xuống
        return query(2*v, lo, mid, l, r) + query(2*v+1, mid+1, hi, l, r);
    }
};
```

### Hai lỗi kinh điển

1. **Quên push trước khi đi xuống** trong query — đọc giá trị cũ bên
   dưới tag chưa đẩy. (Trong `add`, push nằm ngay trước khi đệ quy; còn
   trong query đó là chỗ duy nhất con được biết tag.)
2. **Quy tắc dồn tag sai loại cập nhật.** Cộng đoạn: tag CỘNG dồn
   (lz[child] += lz[parent]). Gán đoạn (a[i] := x): tag GHI ĐÈ
   (lz[child] = x) và cần giá trị "không tag" đánh dấu. Trộn hai quy tắc
   = sai im lặng.

### Trung thực về khấu hao

Mỗi thao tác đẩy O(log n) tag trên một đường gốc — xấu nhất thật sự là
O(log n) mỗi thao tác, không phải khấu hao. n, q = 2·10^5 cho
2·10^5 · 18 · (hằng số) ≈ 10^7: dư dả ngân sách.

**Điểm mấu chốt:** nút phủ trọn → áp dụng + đặt tag, không đi xuống;
push chỉ khi đi qua; quy tắc tag theo loại cập nhật.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p6-point",
    "Point Updates, Range Sums",
    """**Bài toán.** Cho dãy a_1..a_n. Xử lý q thao tác:
- `1 i x` — gán a_i := x;
- `2 l r` — in tổng a_l..a_r.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; 1 ≤ i ≤ n; 1 ≤ l ≤ r ≤ n; 1 ≤ a_i, x ≤ 10^9.

Tổng mỗi truy vấn có thể tới 2·10^14 — dùng long long.""",
    [
        contest_test(
            "ví dụ",
            T("5 4", "3 1 4 1 5", "2 2 4", "1 3 10", "2 2 4", "2 1 5"),
            T("6", "12", "20"),
            "a[2..4] = 1+4+1 = 6; sau khi gán a[3] := 10: 1+10+1 = 12; toàn dãy 3+1+10+1+5 = 20.",
        ),
        contest_test(
            "n = 1 mọi thao tác trỏ cùng điểm",
            T("1 4", "7", "2 1 1", "1 1 9", "2 1 1", "1 1 1000000000"),
            T("7", "9"),
            "Truy vấn, gán, truy vấn, gán (không in) — câu cuối không in gì.",
        ),
        contest_test(
            "truy vấn toàn mảng",
            T("6 3", "1000000000 1000000000 1000000000 1000000000 1000000000 1000000000", "2 1 6", "1 6 1", "2 1 6"),
            T("6000000000", "5000000001"),
            "6·10^9 vượt int — long long; sau khi gán phần tử cuối về 1: 5·10^9 + 1.",
        ),
        contest_test(
            "n lớn trộn dày đặc",
            T("200000 200000") + T(" ".join("1" for _ in range(200000)))
            + T("".join("1 " + str((i % 200000) + 1) + " " + str(i + 1) + chr(10) for i in range(100000)))
            + T("".join("2 1 " + str(200000) + chr(10) for i in range(100000))),
            T(chr(10).join("5000150000" for _ in range(100000))),
            "100000 gán a[i] := i+1 (vị trí 1..100000) trên nền toàn 1: tổng = 100000·100001/2 + 100000·1 = 5000150000; 100000 truy vấn toàn mảng — vét cạn O(nq) là 4·10^10, chết ngân sách.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p6-maxsum",
    "Range Max With Point Updates",
    """**Bài toán.** Cho dãy a_1..a_n. Xử lý q thao tác:
- `1 i x` — gán a_i := x;
- `2 l r` — in max a_l..a_r.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; −10^9 ≤ a_i, x ≤ 10^9.""",
    [
        contest_test(
            "ví dụ",
            T("5 3", "-3 -1 -4 -1 -5", "2 1 5", "1 3 0", "2 1 5"),
            T("-1", "0"),
            "Mọi phần tử âm: max đoạn = −1 (KHÔNG trả 0 mặc định — bẫy identity!).",
        ),
        contest_test(
            "đoạn một phần tử hai đầu",
            T("3 3", "5 9 2", "2 2 2", "1 1 -100", "2 1 1"),
            T("9", "-100"),
            "l = r vẫn là truy vấn hợp lệ — trả a[l] sau cập nhật mới nhất.",
        ),
        contest_test(
            "n lớn âm xen kẽ dương",
            T("200000 2") + T(" ".join(str(-10**9 + (i % 3)) for i in range(200000)), "1 200000 10", "2 1 200000"),
            T("10"),
            "Sau gán a[200000] := 10 thì max toàn dãy là 10 — khởi tạo identity −∞ chứ không phải 0, nếu không mọi dãy âm sẽ trả 0 sai.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p6-gcd",
    "Range GCD",
    """**Bài toán.** Cho dãy a_1..a_n. Xử lý q thao tác:
- `1 i x` — gán a_i := x (1 ≤ x ≤ 10^9);
- `2 l r` — in gcd(a_l..a_r).

**Ràng buộc:** 1 ≤ n, q ≤ 100 000.

gcd là phép hợp có phần tử trung tính 0: gcd(0, x) = x.""",
    [
        contest_test(
            "ví dụ",
            T("5 3", "12 18 24 6 9", "2 1 5", "1 2 7", "2 1 4"),
            T("3", "1"),
            "gcd(12,18,24,6,9) = 3; sau gán a[2] := 7: gcd(12,7,24,6) = 1.",
        ),
        contest_test(
            "đoạn một phần tử — gcd(x, 0) = x",
            T("3 2", "8 12 20", "2 2 2", "2 3 3"),
            T("12", "20"),
            "Lá: gcd(x) = x; phần tử trung tính 0 KHÔNG phá kết quả.",
        ),
        contest_test(
            "gcd toàn dãy về 1 sau một gán",
            T("4 2", "6 10 15 21", "1 3 7", "2 1 4"),
            T("1"),
            "gcd(6,10,7,21) = 1 — một phần tử nguyên tố cùng nhau đủ để hạ toàn bộ.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p6-lazy-sum",
    "Range Add, Range Sum",
    """**Bài toán.** Cho dãy a_1..a_n. Xử lý q thao tác:
- `1 l r x` — cộng x vào mọi a_i, l ≤ i ≤ r;
- `2 l r` — in tổng a_l..a_r.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |a_i|, |x| ≤ 10^4; 1 ≤ l ≤ r ≤ n.

Đây chính là cấu trúc lazy của bài 6.3 — cộng tag theo kiểu cộng dồn.""",
    [
        contest_test(
            "ví dụ",
            T("5 4", "1 2 3 4 5", "1 2 4 10", "2 2 4", "1 1 5 -2", "2 1 5"),
            T("39", "35"),
            "Sau cộng [2,4] += 10: 1,12,13,14,5 → tổng [2,4] = 39; sau [1,5] −= 2: 15 + 30 − 10 = 35.",
        ),
        contest_test(
            "cộng đè nhiều lần cùng đoạn",
            T("3 5", "0 0 0", "1 1 3 1", "1 1 3 1", "1 1 3 1", "2 1 3", "2 2 2"),
            T("9", "3"),
            "Ba lần +1 trên toàn [1,3]: mỗi phần tử 3 — tag cộng dồn 3 lần.",
        ),
        contest_test(
            "n lớn xen kẽ cập nhật/truy vấn",
            T("200000 200000") + T(" ".join("1" for _ in range(200000)))
            + T("".join("1 1 200000 1" + chr(10) for i in range(100000)))
            + T("".join("2 1 200000" + chr(10) for i in range(100000))),
            T(chr(10).join("20000200000" for i in range(100000))),
            "Nền toàn 1 (tổng 200000); 100000 lần +1 toàn mảng cộng thêm 100000·200000 = 2·10^10 → mỗi truy vấn 20000200000. Cộng tag toàn root, không bao giờ phải push — trường hợp tốt nhất của lazy.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p6-range-assign",
    "Range Assign, Range Min — Tag Ghi Đè",
    """**Bài toán.** Cho dãy a_1..a_n. Xử lý q thao tác:
- `1 l r x` — GÁN a_i := x với mọi l ≤ i ≤ r;
- `2 l r` — in min a_l..a_r.

**Ràng buộc:** 1 ≤ n, q ≤ 100 000; 1 ≤ a_i, x ≤ 10^9.

Cập nhật GÂN: tag ghi đè (lz[child] = x), không cộng dồn — quy tắc khác
bài 6.4 một cách có chủ đích.""",
    [
        contest_test(
            "ví dụ",
            T("5 4", "4 9 2 7 3", "1 2 3 5", "2 1 5", "1 1 1 100", "2 1 5"),
            T("3", "3"),
            "Sau gán [2,3] := 5: 4,5,5,7,3 → min toàn dãy = 3 (a[5]); sau gán a[1] := 100: min vẫn 3.",
        ),
        contest_test(
            "gán đè gán — tag mới thắng tag cũ",
            T("4 4", "1 2 3 4", "1 1 4 9", "1 2 3 1", "2 1 4", "2 2 3"),
            T("1", "1"),
            "Gán toàn [1,4] := 9 rồi [2,3] := 1: dãy 9,1,1,9 — tag gán GHI ĐÈ, không cộng.",
        ),
        contest_test(
            "min sau gán toàn mảng",
            T("3 3", "5 5 5", "1 1 3 7", "2 2 3", "2 1 1"),
            T("7", "7"),
            "Mọi lá ghi 7 — min mọi đoạn = 7.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI6 = {
    "hsgi-p6-point": vi_challenge(
        "Cập nhật điểm, tổng đoạn",
        """**Bài toán.** Dãy a_1..a_n; q thao tác: `1 i x` gán a_i := x;
`2 l r` in tổng a_l..a_r. n, q ≤ 200 000; giá trị ≤ 10^9. long long!""",
        [("ví dụ", "6; sau gán a[3] := 10 → 12; toàn dãy → 20."),
         ("n lớn", "O(n log n) — cây phân đoạn.")],
    ),
    "hsgi-p6-maxsum": vi_challenge(
        "Max đoạn với cập nhật điểm",
        """**Bài toán.** Dãy a_1..a_n; `1 i x` gán; `2 l r` in max.
Giá trị từ −10^9 — phần tử trung tính phải là −∞, không phải 0.""",
        [("ví dụ", "Dãy toàn âm: max = −1."),
         ("n lớn", "Gán a[200000] := 10 → max = 10.")],
    ),
    "hsgi-p6-gcd": vi_challenge(
        "GCD đoạn",
        """**Bài toán.** Dãy a_1..a_n; `1 i x` gán (x ≥ 1); `2 l r` in
gcd(a_l..a_r). Phép hợp gcd, trung tính 0.""",
        [("ví dụ", "gcd(12,18,24,6,9) = 3; gán 7 vào giữa → 1."),
         ("một phần tử", "gcd(x) = x.")],
    ),
    "hsgi-p6-lazy-sum": vi_challenge(
        "Cộng đoạn, tổng đoạn",
        """**Bài toán.** Dãy a_1..a_n; `1 l r x` cộng x vào [l, r];
`2 l r` in tổng [l, r]. n, q ≤ 200 000 — lười hóa.""",
        [("ví dụ", "[2,4] += 10 → tổng 39; [1,5] −= 2 → 33."),
         ("đè nhiều lần", "Tag cộng dồn.")],
    ),
    "hsgi-p6-range-assign": vi_challenge(
        "Gán đoạn, min đoạn — tag ghi đè",
        """**Bài toán.** Dãy a_1..a_n; `1 l r x` GÁN a_i := x trên [l, r];
`2 l r` in min. Tag gán ghi đè (không cộng).""",
        [("ví dụ", "[2,3] := 5 → min = 3."),
         ("gán đè gán", "Tag mới thắng tag cũ: 9,1,1,9.")],
    ),
}

write_practice(
    M,
    "hsgi-p6-segtree",
    "Segment Tree Problem Set",
    "Five problems: point-update sums, range max (identity trap), range gcd, lazy range add, and range assign with override tags.",
    "Bài tập cây phân đoạn",
    "Năm bài: tổng với cập nhật điểm, max đoạn (bẫy trung tính), gcd đoạn, cộng đoạn lười hóa, và gán đoạn với tag ghi đè.",
    "hsgi-m6-lazy",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI6,
    solutions=[
        (
            "hsgi-p6-point",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0);
    // iterative-friendly recursive build over explicit values
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // build iteratively bottom-up (size = next pow2 not needed for sum):
    // use classic recursive lambda build on 4n tree
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = t[2*v] + t[2*v+1];
    };
    bld(bld, 1, 1, n);
    auto upd = [&](auto&& self, int v, int lo, int hi, int i, long long x) -> void {
        if (lo == hi) { t[v] = x; return; }
        int mid = (lo + hi) / 2;
        if (i <= mid) self(self, 2*v, lo, mid, i, x);
        else self(self, 2*v+1, mid+1, hi, i, x);
        t[v] = t[2*v] + t[2*v+1];
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        return self(self, 2*v, lo, mid, l, r) + self(self, 2*v+1, mid+1, hi, l, r);
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int i; long long x; in >> i >> x; upd(upd, 1, 1, n, i, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = t[2*v] + t[2*v+1];
    };
    bld(bld, 1, 1, n);
    // near-miss: query trả max thay vì tổng — người học nhầm phép hợp khi
    // chép bộ khung bài max (lỗi ghép bộ khung kinh điển)
    auto upd = [&](auto&& self, int v, int lo, int hi, int i, long long x) -> void {
        if (lo == hi) { t[v] = x; return; }
        int mid = (lo + hi) / 2;
        if (i <= mid) self(self, 2*v, lo, mid, i, x);
        else self(self, 2*v+1, mid+1, hi, i, x);
        t[v] = t[2*v] + t[2*v+1];
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        return max(self(self, 2*v, lo, mid, l, r), self(self, 2*v+1, mid+1, hi, l, r));
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int i; long long x; in >> i >> x; upd(upd, 1, 1, n, i, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
        ),
        (
            "hsgi-p6-maxsum",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, LLONG_MIN);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = max(t[2*v], t[2*v+1]);
    };
    bld(bld, 1, 1, n);
    auto upd = [&](auto&& self, int v, int lo, int hi, int i, long long x) -> void {
        if (lo == hi) { t[v] = x; return; }
        int mid = (lo + hi) / 2;
        if (i <= mid) self(self, 2*v, lo, mid, i, x);
        else self(self, 2*v+1, mid+1, hi, i, x);
        t[v] = max(t[2*v], t[2*v+1]);
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return LLONG_MIN;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        return max(self(self, 2*v, lo, mid, l, r), self(self, 2*v+1, mid+1, hi, l, r));
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int i; long long x; in >> i >> x; upd(upd, 1, 1, n, i, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0);
    // near-miss: khởi tạo và identity là 0 thay vì −∞ — dãy toàn âm trả 0 sai
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = max(t[2*v], t[2*v+1]);
    };
    bld(bld, 1, 1, n);
    auto upd = [&](auto&& self, int v, int lo, int hi, int i, long long x) -> void {
        if (lo == hi) { t[v] = x; return; }
        int mid = (lo + hi) / 2;
        if (i <= mid) self(self, 2*v, lo, mid, i, x);
        else self(self, 2*v+1, mid+1, hi, i, x);
        t[v] = max(t[2*v], t[2*v+1]);
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        return max(self(self, 2*v, lo, mid, l, r), self(self, 2*v+1, mid+1, hi, l, r));
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int i; long long x; in >> i >> x; upd(upd, 1, 1, n, i, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
        ),
        (
            "hsgi-p6-gcd",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = std::gcd(t[2*v], t[2*v+1]);
    };
    bld(bld, 1, 1, n);
    auto upd = [&](auto&& self, int v, int lo, int hi, int i, long long x) -> void {
        if (lo == hi) { t[v] = x; return; }
        int mid = (lo + hi) / 2;
        if (i <= mid) self(self, 2*v, lo, mid, i, x);
        else self(self, 2*v+1, mid+1, hi, i, x);
        t[v] = std::gcd(t[2*v], t[2*v+1]);
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        return std::gcd(self(self, 2*v, lo, mid, l, r), self(self, 2*v+1, mid+1, hi, l, r));
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int i; long long x; in >> i >> x; upd(upd, 1, 1, n, i, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = std::gcd(t[2*v], t[2*v+1]);
    };
    bld(bld, 1, 1, n);
    // near-miss: cache gcd TOÀN DÃY một lần rồi trả ra cho MỌI truy vấn —
    // bỏ qua hoàn toàn đoạn [l, r] của câu hỏi
    long long g = 0;
    for (int i = 1; i <= n; ++i) g = std::gcd(g, a[i]);
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int i; long long x; in >> i >> x; }
        else { int l, r; in >> l >> r; out << g << "{{NL}}"; }
    }
""") + END,
        ),
        (
            "hsgi-p6-lazy-sum",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0), lz(4 * n, 0);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = t[2*v] + t[2*v+1];
    };
    bld(bld, 1, 1, n);
    auto push = [&](int v, int lo, int mid, int hi) -> void {
        if (lz[v]) {
            t[2*v] += lz[v] * (mid - lo + 1);
            t[2*v+1] += lz[v] * (hi - mid);
            lz[2*v] += lz[v];
            lz[2*v+1] += lz[v];
            lz[v] = 0;
        }
    };
    auto add = [&](auto&& self, int v, int lo, int hi, int l, int r, long long x) -> void {
        if (r < lo || hi < l) return;
        if (l <= lo && hi <= r) {
            t[v] += x * (hi - lo + 1);
            lz[v] += x;
            return;
        }
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        self(self, 2*v, lo, mid, l, r, x);
        self(self, 2*v+1, mid+1, hi, l, r, x);
        t[v] = t[2*v] + t[2*v+1];
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        return self(self, 2*v, lo, mid, l, r) + self(self, 2*v+1, mid+1, hi, l, r);
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long x; in >> l >> r >> x; add(add, 1, 1, n, l, r, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0), lz(4 * n, 0);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = t[2*v] + t[2*v+1];
    };
    bld(bld, 1, 1, n);
    auto push = [&](int v, int lo, int mid, int hi) -> void {
        if (lz[v]) {
            t[2*v] += lz[v] * (mid - lo + 1);
            t[2*v+1] += lz[v] * (hi - mid);
            lz[2*v] += lz[v];
            lz[2*v+1] += lz[v];
            lz[v] = 0;
        }
    };
    auto add = [&](auto&& self, int v, int lo, int hi, int l, int r, long long x) -> void {
        if (r < lo || hi < l) return;
        if (l <= lo && hi <= r) {
            t[v] += x * (hi - lo + 1);
            lz[v] += x;
            return;
        }
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        self(self, 2*v, lo, mid, l, r, x);
        self(self, 2*v+1, mid+1, hi, l, r, x);
        t[v] = t[2*v] + t[2*v+1];
    };
    // near-miss: query KHÔNG push trước khi xuống — đọc giá trị cũ dưới tag
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        return self(self, 2*v, lo, mid, l, r) + self(self, 2*v+1, mid+1, hi, l, r);
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long x; in >> l >> r >> x; add(add, 1, 1, n, l, r, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
        ),
        (
            "hsgi-p6-range-assign",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0), lz(4 * n, -1);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        lz[v] = -1;
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = min(t[2*v], t[2*v+1]);
    };
    bld(bld, 1, 1, n);
    auto push = [&](int v, int lo, int mid, int hi) -> void {
        if (lz[v] != -1) {                       // tag GHI ĐÈ xuống con
            t[2*v] = lz[v];
            t[2*v+1] = lz[v];
            lz[2*v] = lz[v];
            lz[2*v+1] = lz[v];
            lz[v] = -1;
        }
    };
    auto assign = [&](auto&& self, int v, int lo, int hi, int l, int r, long long x) -> void {
        if (r < lo || hi < l) return;
        if (l <= lo && hi <= r) {
            t[v] = x;
            lz[v] = x;
            return;
        }
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        self(self, 2*v, lo, mid, l, r, x);
        self(self, 2*v+1, mid+1, hi, l, r, x);
        t[v] = min(t[2*v], t[2*v+1]);
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return LLONG_MAX;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        return min(self(self, 2*v, lo, mid, l, r), self(self, 2*v+1, mid+1, hi, l, r));
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long x; in >> l >> r >> x; assign(assign, 1, 1, n, l, r, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0), lz(4 * n, -1);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        lz[v] = -1;
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = min(t[2*v], t[2*v+1]);
    };
    bld(bld, 1, 1, n);
    // near-miss: tag GHI ĐÈ được áp kiểu CỘNG dồn trong push — gán đoạn
    // thành "cộng thêm x" âm ương: kết quả sai ngay trên test gán đè gán
    auto push = [&](int v, int lo, int mid, int hi) -> void {
        if (lz[v] != -1) {
            t[2*v] += lz[v];
            t[2*v+1] += lz[v];
            lz[2*v] += lz[v];
            lz[2*v+1] += lz[v];
            lz[v] = -1;
        }
    };
    auto assign = [&](auto&& self, int v, int lo, int hi, int l, int r, long long x) -> void {
        if (r < lo || hi < l) return;
        if (l <= lo && hi <= r) {
            t[v] = x;
            lz[v] = x;
            return;
        }
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        self(self, 2*v, lo, mid, l, r, x);
        self(self, 2*v+1, mid+1, hi, l, r, x);
        t[v] = min(t[2*v], t[2*v+1]);
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return LLONG_MAX;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        return min(self(self, 2*v, lo, mid, l, r), self(self, 2*v+1, mid+1, hi, l, r));
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long x; in >> l >> r >> x; assign(assign, 1, 1, n, l, r, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH6 = challenge(
    "hsgi-cp-m6-minpath",
    "Checkpoint — Chiến dịch trúng mùa",
    """**Bài toán.** Kho chứa n thùng hàng thẳng hàng, thùng i có lượng tồn
ban đầu a_i. Mỗi ngày công ty xử lý một CHIẾN DỊCH: chọn đoạn [l, r] và
tăng lượng tồn của mọi thùng trong đoạn thêm x (x có thể âm nếu thu hồi).
Sau từng đợt, bộ phận khảo sát hỏi: tồn TỐI THIỂU trong đoạn [l, r] là bao
nhiêu? Trả lời từng câu hỏi theo thứ tự.

**Ràng buộc:** 1 ≤ n, q ≤ 100 000; 0 ≤ a_i ≤ 10^9; 1 ≤ l ≤ r ≤ n;
−10^4 ≤ x ≤ 10^4.

Tồn có thể âm nhẹ sau thu hồi — min identity là −∞, không phải 0.""",
    [
        contest_test(
            "ví dụ",
            T("5 4", "4 9 2 7 3", "1 2 3 5", "2 1 5", "1 1 1 100", "2 1 5"),
            T("3", "3"),
            "Cộng [2,3] += 5: 4,14,7,7,3 → min = 3; cộng a[1] += 100: 104,14,7,7,3 → min vẫn 3 (hai truy vấn, hai dòng).",
        ),
        contest_test(
            "cộng đè gán nhiều nhịp",
            T("4 5", "1 2 3 4", "1 1 4 9", "2 1 4", "1 2 3 1", "2 1 4", "2 2 3"),
            T("10", "10", "12"),
            "Thao tác 1 là CỘNG (chiến dịch tăng, x có thể âm): [1,4] += 9 → 10,11,12,13, min = 10; [2,3] += 1 → min toàn dãy vẫn 10; riêng [2,3] = min(12,13) = 12.",
        ),
        contest_test(
            "n lớn luân phiên cộng/truy vấn",
            T("100000 2") + T(" ".join("1000000000" for _ in range(100000)), "1 1 100000 -10000", "2 1 100000"),
            T("999990000"),
            "Cả dãy −10^4: min = 10^9 − 10^4. Một cập nhật + một truy vấn — thang đo thật của lazy.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP6 = vi_challenge(
    "Checkpoint — Chiến dịch trúng mùa",
    """**Bài toán.** n thùng hàng thẳng hàng, thùng i tồn a_i. Mỗi ngày: chọn
đoạn [l, r] và cộng x vào cả đoạn (x có thể âm). Sau từng đợt, hỏi tồn
TỐI THIỂU trong [l, r]. Trả lời theo thứ tự.

**Ràng buộc:** 1 ≤ n, q ≤ 100 000; 0 ≤ a_i ≤ 10^9; −10^4 ≤ x ≤ 10^4.""",
    [("ví dụ", "Cộng [2,3] += 5 rồi hỏi min toàn dãy."),
     ("n lớn", "Lười hóa cộng đoạn + min đoạn.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m6",
    "Checkpoint — Segment Trees",
    "Pass the graded problem to finish the segment tree module.",
    25,
    """**Checkpoint — Segment Trees.** Pass the graded challenge below to
complete the module. It composes everything the module taught: a lazy
segment tree whose updates are range ADD (tags accumulate) and whose
queries are range MIN (identity −∞). One tree, two different rules —
this is the structure you will reuse in every graph/DP optimization
later. Watch the identities: add-identity 0 for sums on the way, min
identity LLONG_MAX for the query merge... and never let the add-tag
rule touch the min-merge rule.

**Điểm kiểm tra — Cây phân đoạn.** Pass bài chấm bên dưới để hoàn thành
module. Đây là phép ghép của cả module: cây lười hóa với cập nhật CỘNG
đoạn (tag cộng dồn) và truy vấn MIN đoạn (trung tính −∞). Một cây, hai
quy tắc khác nhau — cấu trúc bạn sẽ tái sử dụng trong mọi tối ưu đồ
thị/DP sau này. Chú ý phần tử trung tính: cộng → 0, min → −∞/MAX.""",
    "Checkpoint — Segment Trees",
    "Pass bài chấm để hoàn thành module cây phân đoạn.",
    """**Điểm kiểm tra — Cây phân đoạn.** Pass bài chấm bên dưới: cộng đoạn
(tag cộng dồn) + truy vấn min đoạn. Một cây, hai quy tắc.""",
    CH6,
    VI_CP6,
    solution=CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(4 * n, 0), lz(4 * n, 0);
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    auto bld = [&](auto&& self, int v, int lo, int hi) -> void {
        if (lo == hi) { t[v] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        self(self, 2*v, lo, mid);
        self(self, 2*v+1, mid+1, hi);
        t[v] = min(t[2*v], t[2*v+1]);
    };
    bld(bld, 1, 1, n);
    auto push = [&](int v, int lo, int mid, int hi) -> void {
        if (lz[v]) {                                  // range ADD: tag cộng dồn
            t[2*v] += lz[v];
            t[2*v+1] += lz[v];
            lz[2*v] += lz[v];
            lz[2*v+1] += lz[v];
            lz[v] = 0;
        }
    };
    auto add = [&](auto&& self, int v, int lo, int hi, int l, int r, long long x) -> void {
        if (r < lo || hi < l) return;
        if (l <= lo && hi <= r) {
            t[v] += x;
            lz[v] += x;
            return;
        }
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        self(self, 2*v, lo, mid, l, r, x);
        self(self, 2*v+1, mid+1, hi, l, r, x);
        t[v] = min(t[2*v], t[2*v+1]);
    };
    auto qry = [&](auto&& self, int v, int lo, int hi, int l, int r) -> long long {
        if (r < lo || hi < l) return LLONG_MAX;
        if (l <= lo && hi <= r) return t[v];
        int mid = (lo + hi) / 2;
        push(v, lo, mid, hi);
        return min(self(self, 2*v, lo, mid, l, r), self(self, 2*v+1, mid+1, hi, l, r));
    };
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long x; in >> l >> r >> x; add(add, 1, 1, n, l, r, x); }
        else { int l, r; in >> l >> r; out << qry(qry, 1, 1, n, l, r) << "{{NL}}"; }
    }
""") + END,
    wrong=CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // near-miss: mỗi truy vấn quét TOÀN DÃY thay vì đoạn [l, r] — quên
    // đối số l, r khi dịch bộ khung prefix-min; đúng với truy vấn toàn dãy,
    // sai với mọi đoạn nhỏ hơn
    while (q--) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long x; in >> l >> r >> x; for (int i = l; i <= r; ++i) a[i] += x; }
        else { int l, r; in >> l >> r; long long mn = LLONG_MAX; for (int i = 1; i <= n; ++i) mn = min(mn, a[i]); out << mn << "{{NL}}"; }
    }
""") + END,
)
