#!/usr/bin/env python3
"""C Advanced — batch 4: modules 7 (advanced-data-structures) and
8 (generic-programming). Zero-backslash authoring: @NL@ = statement
separator, @CE@ = newline escape inside C string literals."""
from ca import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ================ MODULE 7: ca-advanced-data-structures =====================
M7 = "ca-advanced-data-structures"

L7A = "ca-hash-tables"
L7B = "ca-heaps-priority"
L7C = "ca-union-find-graphs"
L7CP = "ca-checkpoint-m7"

write_module(
    M7,
    "Advanced Data Structures in C",
    "Open-addressed hash tables, binary heaps, and union-find — implemented with explicit memory layout and measured complexity.",
    "Cấu trúc dữ liệu nâng cao trong C",
    "Bảng băm mở, heap nhị phân, và union-find — hiện thực với bố cục bộ nhớ tường minh và độ phức tạp được đo.",
    [L7A, L7B, L7C, L7CP],
    ["ca-p7-ds"],
)

write_lesson(
    M7,
    L7A,
    "Open Addressing from Scratch",
    "Hash tables without chaining: probing, load factor, tombstones, and why memory layout decides cache fate.",
    16,
    """
## One array, no pointers per entry

Chaining stores a linked list per bucket — pointer-chasing that misses cache on every step. Open addressing keeps *all entries in one array*: on collision, probe the next slot (linear probing), until an empty one appears.

## The load factor governs everything

`alpha = used / capacity`. As alpha approaches 1, probe runs get long; the standard discipline is to resize (rehash into a bigger table) at alpha ~ 0.7. Amortized insert stays O(1) — the occasional rehash is paid for by many cheap inserts.

## Deletion needs tombstones

An empty slot ends a probe run — so simply emptying a deleted slot breaks lookups for entries that probed past it. The fix: mark deletions with a *tombstone* state that probes continue through. Tombstones accumulate; periodic rehash cleans them.

## Layout is performance

One array of entries is cache-friendly: a probe is a linear scan. This is why fast hash tables (and this whole course) treat *memory layout* as part of the data-structure design, not an afterthought.
""",
    "Mở địa chỉ từ đầu",
    "Bảng băm không cần chaining: probing, load factor, tombstone, và vì sao bố cục bộ nhớ quyết định số phận cache.",
    """
## Một mảng, không con trỏ cho từng phần tử

Chaining giữ linked list cho mỗi bucket — bước qua con trỏ làm miss cache mỗi lần. Open addressing giữ *mọi phần tử trong một mảng*: khi đụng độ, thăm slot kế tiếp (linear probing) tới khi gặp slot trống.

## Load factor điều khiển tất cả

`alpha = used / capacity`. Khi alpha tiến về 1, dãy probe dài ra; kỷ luật chuẩn là resize (rehash sang bảng lớn hơn) ở alpha ~ 0.7. Insert khấu trừ vẫn O(1) — lần rehash hiếm hoi được trả bằng nhiều insert rẻ.

## Xóa cần tombstone

Slot trống kết thúc dãy probe — vậy là chỉ đơn giản làm trống slot của phần tử bị xóa sẽ phá lookup của phần tử từng probe đi qua. Cách chữa: đánh dấu xóa bằng trạng thái *tombstone* mà probe vẫn đi tiếp qua. Tombstone tích tụ; rehash định kỳ dọn chúng.

## Bố cục là hiệu năng

Một mảng các entry thân thiện với cache: một probe là quét tuyến tính. Vì vậy bảng băm nhanh (và cả khóa học này) coi *bố cục bộ nhớ* là một phần thiết kế cấu trúc dữ liệu.
""",
)

write_lesson(
    M7,
    L7B,
    "Heaps and Priority Queues",
    "The array-encoded binary heap, sift-up and sift-down, and heapsort as a free by-product.",
    15,
    """
## A tree that lives in an array

A binary heap is a complete binary tree stored flat: for index i, parent = (i-1)/2, children = 2i+1 and 2i+2. No pointers, perfect cache locality, and the shape guarantee (complete tree) is what makes the encoding lossless.

## Two operations carry everything

- **sift-up**: after appending at the end, swap upward while the parent is larger (min-heap) — O(log n).
- **sift-down**: after moving the last element to the root, swap downward with the smaller child — O(log n).

push = append + sift-up; pop = swap root with last, shrink, sift-down. peek is free — the root is the minimum.

## Complexity that matters

Build-heap from an arbitrary array is O(n) — better than n pushes at O(log n) each — because most nodes sift only a short distance. Heapsort: build-heap, then pop n times; in-place, O(n log n), no recursion.
""",
    "Heap và hàng đợi ưu tiên",
    "Heap nhị phân mã hóa bằng mảng, sift-up và sift-down, và heapsort như sản phẩm phụ miễn phí.",
    """
## Cây sống trong mảng

Heap nhị phân là cây nhị phân hoàn chỉnh lưu phẳng: tại chỉ số i, cha = (i-1)/2, con = 2i+1 và 2i+2. Không con trỏ, locality cache hoàn hảo, và bảo đảm hình dạng (cây hoàn chỉnh) làm phép mã hóa không mất mát.

## Hai phép toán gánh tất cả

- **sift-up**: sau khi thêm vào cuối, đổi chỗ đi lên trong khi cha lớn hơn (min-heap) — O(log n).
- **sift-down**: sau khi chuyển phần tử cuối lên gốc, đổi chỗ đi xuống với con nhỏ hơn — O(log n).

push = thêm + sift-up; pop = đổi gốc với cuối, thu ngắn, sift-down. peek miễn phí — gốc là phần tử nhỏ nhất.

## Độ phức tạp đáng nhớ

Build-heap từ mảng tùy ý là O(n) — tốt hơn n lần push O(log n) — vì đa số node chỉ sift quãng ngắn. Heapsort: build-heap rồi pop n lần; tại chỗ, O(n log n), không đệ quy.
""",
)

write_lesson(
    M7,
    L7C,
    "Union-Find and Graph Adjacency",
    "Disjoint sets with path compression and union by rank, plus adjacency lists built from edge arrays.",
    15,
    """
## Disjoint sets in two arrays

Union-find tracks *which set* each element belongs to, using a parent array:

- **find(x)**: follow parents to the root.
- **union(a, b)**: attach one root under the other.

Two optimizations turn worst-case chains into near-constant time:

- **path compression**: after find, point every visited node straight at the root;
- **union by rank/size**: attach the smaller tree under the larger.

With both, amortized cost per operation is effectively constant — the famous inverse-Ackermann bound. This structure runs Kruskal's MST and connectivity queries in competitive and production graph code alike.

## Adjacency lists from edge arrays

Counting sort the edges by source into an offset array (CSR layout): `offset[v]` gives where v's neighbors start. Memory: exactly V + E entries. This is the layout GPU and graph-engine code uses because it is compact and iteration is a plain array walk.
""",
    "Union-Find và danh sách kề",
    "Tập hợp rời nhau với path compression và union by rank, cộng danh sách kề dựng từ mảng cạnh.",
    """
## Tập hợp rời nhau trong hai mảng

Union-find theo dõi *mỗi phần tử thuộc tập nào*, qua mảng cha:

- **find(x)**: đi theo cha tới gốc.
- **union(a, b)**: gắn một gốc dưới gốc kia.

Hai tối ưu biến chuỗi xấu nhất thành gần hằng số:

- **path compression**: sau find, trỏ mọi node đã đi qua thẳng về gốc;
- **union by rank/size**: gắn cây nhỏ dưới cây lớn.

Có cả hai, chi phí khấu trừ mỗi phép toán gần như hằng số — giới hạn inverse-Ackermann nổi tiếng. Cấu trúc này chạy Kruskal MST và truy vấn liên thông trong cả code thi đấu lẫn production.

## Danh sách kề từ mảng cạnh

Đếm sắp xếp các cạnh theo nguồn vào mảng offset (bố cục CSR): `offset[v]` cho biết láng giềng của v bắt đầu ở đâu. Bộ nhớ: đúng V + E phần tử. Đây là bố cục của code GPU và graph engine vì nó gọn và vòng lặp chỉ là đi mảng.
""",
)

write_practice(
    M7,
    "ca-p7-ds",
    "Data Structure Build Drills",
    "Hash table, heap, and union-find — each built over explicit arrays with pin-downable contracts.",
    "Bài tập dựng cấu trúc dữ liệu",
    "Bảng băm, heap, và union-find — mỗi cái dựng trên mảng tường minh với hợp đồng ghim được.",
    L7A,
    26,
    "advanced",
    [
        challenge(
            "ca7-hash-linear",
            "Linear-Probing Hash Table",
            "Fixed-capacity int→int table with linear probing and tombstones:@CE@ @CE@```c@CE@#define HT_CAP 16@CE@typedef struct { int key; int val; unsigned char state; } ht_ent_t; /* state: 0 empty, 1 used, 2 tombstone */@CE@void ht_init(ht_ent_t *t);@CE@int ht_put(ht_ent_t *t, int key, int val); /* 1 stored, 0 full */@CE@int *ht_get(ht_ent_t *t, int key);   /* pointer to val, or NULL */@CE@int ht_del(ht_ent_t *t, int key);   /* 1 deleted, 0 absent */@CE@```@CE@ @CE@Hash: `((unsigned)key * 2654435761u) % HT_CAP`. Probe forward with wraparound; insert may reuse tombstones; the table is never resized.",
            C_PRELUDE,
            [
                ("insert and find", "ht_ent_t t[16];@NL@ht_init(t);@NL@CHECK_EQ(ht_put(t, 42, 4242), 1);@NL@int *v = ht_get(t, 42);@NL@CHECK_NOT_NULL(v);@NL@CHECK_EQ(*v, 4242);", "Hash lands somewhere; probe finds it; get returns a pointer to live storage."),
                ("collision probes forward", "ht_ent_t t[16];@NL@ht_init(t);@NL@int h = (int)(((unsigned)7 * 2654435761u) % 16);@NL@CHECK_EQ(ht_put(t, 7, 1), 1);@NL@CHECK_EQ(ht_put(t, 7 + 16, 2), 1);@NL@CHECK_EQ(*ht_get(t, 7), 1);@NL@CHECK_EQ(*ht_get(t, 7 + 16), 2);", "Both keys hash to the same slot; the second probes forward, and both remain findable."),
                ("tombstone reused", "ht_ent_t t[16];@NL@ht_init(t);@NL@int h = (int)(((unsigned)3 * 2654435761u) % 16);@NL@CHECK_EQ(ht_put(t, 3, 1), 1);@NL@CHECK_EQ(ht_put(t, 3 + 16, 2), 1);@NL@CHECK_EQ(ht_del(t, 3), 1);@NL@CHECK_EQ(ht_put(t, 3 + 32, 3), 1);@NL@CHECK_EQ(*ht_get(t, 3 + 32), 3);@NL@CHECK_NULL(ht_get(t, 3));", "Deleting the home slot leaves a tombstone; the new colliding key reuses it; the removed key is gone."),
                ("full table", "ht_ent_t t[16];@NL@ht_init(t);@NL@int put_all = 1;@NL@for (int k = 0; k < 16; k++) put_all &= ht_put(t, k, k);@NL@CHECK_EQ(put_all, 1);@NL@CHECK_EQ(ht_put(t, 100, 1), 0);", "16 distinct keys fill the table; the 17th reports full."),
            ],
            level="mini-build",
        ),
        challenge(
            "ca7-heap",
            "Array Binary Heap",
            "Min-heap over a fixed int array:@CE@ @CE@```c@CE@typedef struct { int a[64]; size_t n; } heap_t;@CE@void heap_push(heap_t *h, int v);@CE@int heap_pop(heap_t *h);   /* returns min; caller ensures n>0 */@CE@int heap_min(const heap_t *h);@CE@```@CE@ @CE@push appends and sifts up; pop swaps the root with the last, shrinks, sifts down.",
            C_PRELUDE,
            [
                ("min pops in order", "heap_t h = {{{0}}, 0};@NL@int vals[5] = {5, 3, 8, 1, 9};@NL@for (int i = 0; i < 5; i++) heap_push(&h, vals[i]);@NL@CHECK_EQ(heap_min(&h), 1);@NL@CHECK_EQ(heap_pop(&h), 1);@NL@CHECK_EQ(heap_pop(&h), 3);@NL@CHECK_EQ(heap_pop(&h), 5);@NL@CHECK_EQ(heap_pop(&h), 8);@NL@CHECK_EQ(heap_pop(&h), 9);", "Five pushes then five pops emerge in sorted order — the heap property at work."),
                ("duplicates allowed", "heap_t h2 = {{{0}}, 0};@NL@heap_push(&h2, 4);@NL@heap_push(&h2, 4);@NL@CHECK_EQ(heap_pop(&h2), 4);@NL@CHECK_EQ(heap_pop(&h2), 4);", "Equal keys are fine; the heap orders values, not identities."),
            ],
            level="independent",
        ),
        challenge(
            "ca7-union-find",
            "Union-Find with Compression",
            "Union-find over fixed-size element sets:@CE@ @CE@```c@CE@void uf_init(int *parent, int *rank_, int n);@CE@int uf_find(int *parent, int x);@CE@void uf_union(int *parent, int *rank_, int a, int b);@CE@int uf_connected(int *parent, int a, int b);@CE@```@CE@ @CE@find uses path compression; union by rank; connected returns 1 iff same root.",
            C_PRELUDE,
            [
                ("components merge", "int parent[8], rk[8];@NL@uf_init(parent, rk, 8);@NL@uf_union(parent, rk, 0, 1);@NL@uf_union(parent, rk, 2, 3);@NL@CHECK_EQ(uf_connected(parent, 0, 1), 1);@NL@CHECK_EQ(uf_connected(parent, 0, 2), 0);@NL@uf_union(parent, rk, 1, 2);@NL@CHECK_EQ(uf_connected(parent, 0, 3), 1);", "Two pairs union separately, then a bridging union merges the components — connectivity follows transitively."),
                ("find is idempotent", "int parent2[4], rk2[4];@NL@uf_init(parent2, rk2, 4);@NL@uf_union(parent2, rk2, 0, 1);@NL@int r1 = uf_find(parent2, 0);@NL@int r2 = uf_find(parent2, 0);@NL@CHECK_EQ(r1, r2);@NL@CHECK_EQ(uf_find(parent2, 1), r1);", "Repeated finds are stable; after compression, a member and its root agree immediately."),
            ],
            level="independent",
        ),
        challenge(
            "ca7-csr",
            "CSR Adjacency from Edge List",
            "Build compressed sparse rows from an edge array:@CE@ @CE@```c@CE@void csr_build(int V, const int (*edges)[2], size_t E, int *offset, int *adj);@CE@```@CE@ @CE@`offset` has V+1 entries; `adj` has E entries: neighbors grouped by source vertex in increasing vertex order.",
            C_PRELUDE,
            [
                ("offsets and adjacency", "int edges[4][2] = {{0, 2}, {1, 0}, {0, 1}, {2, 0}};@NL@int offset[4];@NL@int adj[4];@NL@csr_build(3, edges, 4, offset, adj);@NL@CHECK_EQ(offset[0], 0);@NL@CHECK_EQ(offset[1], 2);@NL@CHECK_EQ(offset[2], 3);@NL@CHECK_EQ(offset[3], 4);@NL@CHECK_EQ(adj[0], 2);@NL@CHECK_EQ(adj[1], 1);", "Vertex 0 has two outgoing edges (to 2 and 1) landing adj[0..1]; vertex 1 one; the offsets count up to E."),
                ("isolated vertex", "int e2[2][2] = {{0, 1}, {0, 2}};@NL@int off2[4];@NL@int adj2[2];@NL@csr_build(3, e2, 2, off2, adj2);@NL@CHECK_EQ(off2[1], 2);@NL@CHECK_EQ(off2[2], 2);@NL@CHECK_EQ(off2[3], 2);", "Both edges leave vertex 0: offset[1] is 2; vertex 1 has an empty range [offset[2], offset[2]) — isolation is an empty span."),
            ],
            level="combination",
        ),
    ],
    {
        "ca7-hash-linear": vi_challenge(
            "Bảng băm linear probing",
            "Bảng int-to-int cố định với linear probing và tombstone: ht_init/ht_put/ht_get/ht_del — chèn có thể dùng lại tombstone, không resize.",
            [
                ("chèn và tìm", "Probe tìm thấy; get trả con trỏ tới bộ nhớ sống."),
                ("đụng độ probe tới trước", "Cả hai khóa cùng slot; khóa sau probe tới trước, cả hai vẫn tìm được."),
                ("tombstone được tái dùng", "Xóa slot nhà để lại tombstone; khóa đụng độ mới dùng lại nó; khóa đã xóa biến mất."),
                ("bảng đầy", "16 khóa khác nhau lấp đầy bảng; khóa thứ 17 báo đầy."),
            ],
        ),
        "ca7-heap": vi_challenge(
            "Heap nhị phân trên mảng",
            "Min-heap trên mảng cố định: heap_push (append + sift-up), heap_pop (đổi gốc với cuối + sift-down), heap_min.",
            [
                ("pop ra đúng thứ tự", "Năm push rồi năm pop ra theo thứ tự tăng — tính chất heap đang hoạt động."),
                ("khóa trùng được phép", "Khóa bằng nhau ổn; heap xếp thứ tự giá trị, không phải danh tính."),
            ],
        ),
        "ca7-union-find": vi_challenge(
            "Union-Find với path compression",
            "Cài uf_init/uf_find/uf_union/uf_connected — find có path compression, union theo rank.",
            [
                ("hợp nhất thành phần", "Hai cặp union riêng rồi union cầu nối gộp lại — liên thông lan truyền bắc cầu."),
                ("find bất biến", "find lặp lại ổn định; sau compression, thành viên và gốc thống nhất ngay."),
            ],
        ),
        "ca7-csr": vi_challenge(
            "CSR từ danh sách cạnh",
            "Cài csr_build: offset V+1 phần tử, adj E phần tử — láng giềng nhóm theo đỉnh nguồn theo thứ tự tăng.",
            [
                ("offset và adjacency", "Đỉnh 0 có hai cạnh ra chiếm adj[0..1]; các offset đếm tới E."),
                ("đỉnh cô lập", "Cả hai cạnh rời đỉnh 0: offset[1] là 2; đỉnh 1 có khoảng rỗng — cô lập là span rỗng."),
            ],
        ),
    },
    solutions=[
        (
            "ca7-hash-linear",
            C_PRELUDE
            + "#define HT_CAP 16@NL@"
            + "typedef struct { int key; int val; unsigned char state; } ht_ent_t;@NL@"
            + "void ht_init(ht_ent_t *t) { for (int i = 0; i < HT_CAP; i++) t[i].state = 0; }@NL@"
            + "static int ht_hash(int key) { return (int)(((unsigned)key * 2654435761u) % HT_CAP); }@NL@"
            + "int ht_put(ht_ent_t *t, int key, int val) {@NL@    int h = ht_hash(key);@NL@    int tomb = -1;@NL@    for (int i = 0; i < HT_CAP; i++) {@NL@        int idx = (h + i) % HT_CAP;@NL@        if (t[idx].state == 0) { idx = (tomb >= 0) ? tomb : idx; t[idx].key = key; t[idx].val = val; t[idx].state = 1; return 1; }@NL@        if (t[idx].state == 2 && tomb < 0) tomb = idx;@NL@        if (t[idx].state == 1 && t[idx].key == key) { t[idx].val = val; return 1; }@NL@    }@NL@    if (tomb >= 0) { t[tomb].key = key; t[tomb].val = val; t[tomb].state = 1; return 1; }@NL@    return 0;@NL@}@NL@"
            + "int *ht_get(ht_ent_t *t, int key) {@NL@    int h = ht_hash(key);@NL@    for (int i = 0; i < HT_CAP; i++) {@NL@        int idx = (h + i) % HT_CAP;@NL@        if (t[idx].state == 0) return NULL;@NL@        if (t[idx].state == 1 && t[idx].key == key) return &t[idx].val;@NL@    }@NL@    return NULL;@NL@}@NL@"
            + "int ht_del(ht_ent_t *t, int key) {@NL@    int h = ht_hash(key);@NL@    for (int i = 0; i < HT_CAP; i++) {@NL@        int idx = (h + i) % HT_CAP;@NL@        if (t[idx].state == 0) return 0;@NL@        if (t[idx].state == 1 && t[idx].key == key) { t[idx].state = 2; return 1; }@NL@    }@NL@    return 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#define HT_CAP 16@NL@"
            + "typedef struct { int key; int val; unsigned char state; } ht_ent_t;@NL@"
            + "void ht_init(ht_ent_t *t) { for (int i = 0; i < HT_CAP; i++) t[i].state = 0; }@NL@"
            + "static int ht_hash(int key) { return (int)(((unsigned)key * 2654435761u) % HT_CAP); }@NL@"
            + "int ht_put(ht_ent_t *t, int key, int val) {@NL@    int h = ht_hash(key);@NL@    for (int i = 0; i < HT_CAP; i++) {@NL@        int idx = (h + i) % HT_CAP;@NL@        if (t[idx].state != 1) { t[idx].key = key; t[idx].val = val; return 1; }@NL@    }@NL@    return 0;@NL@}@NL@"
            + "int *ht_get(ht_ent_t *t, int key) {@NL@    int h = ht_hash(key);@NL@    for (int i = 0; i < HT_CAP; i++) {@NL@        int idx = (h + i) % HT_CAP;@NL@        if (t[idx].state == 0) return NULL;@NL@        if (t[idx].state == 1 && t[idx].key == key) return &t[idx].val;@NL@    }@NL@    return NULL;@NL@}@NL@"
            + "int ht_del(ht_ent_t *t, int key) {@NL@    int h = ht_hash(key);@NL@    for (int i = 0; i < HT_CAP; i++) {@NL@        int idx = (h + i) % HT_CAP;@NL@        if (t[idx].state == 1 && t[idx].key == key) { t[idx].state = 0; return 1; }@NL@    }@NL@    return 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca7-heap",
            C_PRELUDE
            + "typedef struct { int a[64]; size_t n; } heap_t;@NL@"
            + "static void sift_up(heap_t *h, size_t i) {@NL@    while (i > 0) {@NL@        size_t p = (i - 1) / 2;@NL@        if (h->a[p] <= h->a[i]) break;@NL@        int t = h->a[p]; h->a[p] = h->a[i]; h->a[i] = t;@NL@        i = p;@NL@    }@NL@}@NL@"
            + "static void sift_down(heap_t *h, size_t i) {@NL@    for (;;) {@NL@        size_t l = 2 * i + 1, r = 2 * i + 2, m = i;@NL@        if (l < h->n && h->a[l] < h->a[m]) m = l;@NL@        if (r < h->n && h->a[r] < h->a[m]) m = r;@NL@        if (m == i) break;@NL@        int t = h->a[m]; h->a[m] = h->a[i]; h->a[i] = t;@NL@        i = m;@NL@    }@NL@}@NL@"
            + "void heap_push(heap_t *h, int v) { h->a[h->n] = v; h->n++; sift_up(h, h->n - 1); }@NL@"
            + "int heap_pop(heap_t *h) {@NL@    int min = h->a[0];@NL@    h->a[0] = h->a[h->n - 1];@NL@    h->n--;@NL@    sift_down(h, 0);@NL@    return min;@NL@}@NL@"
            + "int heap_min(const heap_t *h) { return h->a[0]; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "typedef struct { int a[64]; size_t n; } heap_t;@NL@"
            + "static void sift_up(heap_t *h, size_t i) {@NL@    while (i > 0) {@NL@        size_t p = (i - 1) / 2;@NL@        if (h->a[p] <= h->a[i]) break;@NL@        int t = h->a[p]; h->a[p] = h->a[i]; h->a[i] = t;@NL@        i = p;@NL@    }@NL@}@NL@"
            + "static void sift_down(heap_t *h, size_t i) {@NL@    for (;;) {@NL@        size_t l = 2 * i + 1, r = 2 * i + 2, m = i;@NL@        if (l < h->n && h->a[l] > h->a[m]) m = l;@NL@        if (r < h->n && h->a[r] > h->a[m]) m = r;@NL@        if (m == i) break;@NL@        int t = h->a[m]; h->a[m] = h->a[i]; h->a[i] = t;@NL@        i = m;@NL@    }@NL@}@NL@"
            + "void heap_push(heap_t *h, int v) { h->a[h->n] = v; h->n++; sift_up(h, h->n - 1); }@NL@"
            + "int heap_pop(heap_t *h) {@NL@    int min = h->a[0];@NL@    h->a[0] = h->a[h->n - 1];@NL@    h->n--;@NL@    sift_down(h, 0);@NL@    return min;@NL@}@NL@"
            + "int heap_min(const heap_t *h) { return h->a[0]; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca7-union-find",
            C_PRELUDE
            + "void uf_init(int *parent, int *rank_, int n) {@NL@    for (int i = 0; i < n; i++) { parent[i] = i; rank_[i] = 0; }@NL@}@NL@"
            + "int uf_find(int *parent, int x) {@NL@    int r = x;@NL@    while (parent[r] != r) r = parent[r];@NL@    while (parent[x] != r) { int nx = parent[x]; parent[x] = r; x = nx; }@NL@    return r;@NL@}@NL@"
            + "void uf_union(int *parent, int *rank_, int a, int b) {@NL@    int ra = uf_find(parent, a);@NL@    int rb = uf_find(parent, b);@NL@    if (ra == rb) return;@NL@    if (rank_[ra] < rank_[rb]) { int t = ra; ra = rb; rb = t; }@NL@    parent[rb] = ra;@NL@    if (rank_[ra] == rank_[rb]) rank_[ra]++;@NL@}@NL@"
            + "int uf_connected(int *parent, int a, int b) { return uf_find(parent, a) == uf_find(parent, b) ? 1 : 0; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "void uf_init(int *parent, int *rank_, int n) {@NL@    for (int i = 0; i < n; i++) { parent[i] = i; rank_[i] = 0; }@NL@}@NL@"
            + "int uf_find(int *parent, int x) {@NL@    parent[x] = x;@NL@    return x;@NL@}@NL@"
            + "void uf_union(int *parent, int *rank_, int a, int b) {@NL@    (void)rank_;@NL@    parent[a] = b;@NL@}@NL@"
            + "int uf_connected(int *parent, int a, int b) { return uf_find(parent, a) == uf_find(parent, b) ? 1 : 0; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca7-csr",
            C_PRELUDE
            + "void csr_build(int V, const int (*edges)[2], size_t E, int *offset, int *adj) {@NL@    for (int v = 0; v <= V; v++) offset[v] = 0;@NL@    for (size_t i = 0; i < E; i++) offset[edges[i][0] + 1]++;@NL@    for (int v = 0; v < V; v++) offset[v + 1] += offset[v];@NL@    int *cur = offset; /* reuse: cur[v] = next write pos */@NL@    int tmp[64];@NL@    for (int v = 0; v <= V; v++) tmp[v] = offset[v];@NL@    for (size_t i = 0; i < E; i++) adj[tmp[edges[i][0]]++] = edges[i][1];@NL@    (void)cur;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "void csr_build(int V, const int (*edges)[2], size_t E, int *offset, int *adj) {@NL@    for (int v = 0; v <= V; v++) offset[v] = 0;@NL@    for (size_t i = 0; i < E; i++) offset[edges[i][1] + 1]++;@NL@    for (int v = 0; v < V; v++) offset[v + 1] += offset[v];@NL@    int tmp[64];@NL@    for (int v = 0; v <= V; v++) tmp[v] = offset[v];@NL@    for (size_t i = 0; i < E; i++) adj[tmp[edges[i][1]]++] = edges[i][0];@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

# ================== MODULE 8: ca-generic-programming ========================
M8 = "ca-generic-programming"

L8A = "ca-voidstar-interfaces"
L8B = "ca-generic-techniques"
L8CP = "ca-checkpoint-m8"

write_module(
    M8,
    "Generic Programming in C",
    "void* interfaces, callback dispatch, _Generic selection, and macro metaprogramming — the real C toolbox, with its limits stated honestly.",
    "Lập trình tổng quát trong C",
    "Giao diện void*, điều phối callback, chọn _Generic, và macro metaprogramming — hộp công cụ C thật, với giới hạn được nói thẳng.",
    [L8A, L8B, L8CP],
    ["ca-p8-generic"],
)

write_lesson(
    M8,
    L8A,
    "void* and the Cost of Erasure",
    "Type-erased containers: what qsort teaches, byte-wise copies, alignment, and why the compiler cannot save you.",
    15,
    """
## qsort is the master class

```c
void qsort(void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
```

Four ingredients make it generic: a byte-addressed base, an element *size* (so the algorithm can move elements with memcpy), a count, and a comparison callback supplied by the caller. Every generic C API you will design mixes some subset of these.

## What the cost is

Inside a void* container, elements are bytes: `elem_at(base, i, size)` is `(char *)base + i * size`. The compiler no longer knows element types — wrong casts, wrong sizes, and wrong comparators are all silent until runtime. Genericity in C trades compile-time checking for flexibility; document and test accordingly.

## Alignment still applies

A void* handed back to the caller must be as aligned as the data it represents. If your container allocates raw bytes, align them — a double stored at an odd address is UB the moment it is loaded.
""",
    "void* và cái giá của việc xóa kiểu",
    "Container xóa kiểu: qsort dạy gì, sao chép theo byte, alignment, và vì sao trình biên dịch không cứu được bạn.",
    """
## qsort là lớp thạc sĩ

```c
void qsort(void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
```

Bốn thành phần làm nó tổng quát: base theo byte, *kích thước* phần tử (để thuật toán di chuyển phần tử bằng memcpy), số lượng, và callback so sánh do caller cung cấp. Mọi API C tổng quát bạn thiết kế đều trộn một tập con của những thứ này.

## Cái giá là gì

Bên trong container void*, phần tử là byte: `elem_at(base, i, size)` là `(char *)base + i * size`. Trình biên dịch không còn biết kiểu phần tử — cast sai, kích thước sai, comparator sai đều im lặng đến lúc chạy. Tính tổng quát trong C đổi kiểm tra lúc biên dịch lấy sự linh hoạt; hãy tài liệu hóa và kiểm thử tương ứng.

## Alignment vẫn áp dụng

void* trả lại cho caller phải căn bằng với dữ liệu nó đại diện. Nếu container cấp phát byte thô, hãy căn chúng — double nằm ở địa chỉ lẻ là UB ngay khi được load.
""",
)

write_lesson(
    M8,
    L8B,
    "_Generic, Tagged Unions, and Macro Boundaries",
    "Compile-time dispatch in C23 terms, runtime tagged unions, and when macros are the wrong tool.",
    15,
    """
## _Generic: compile-time selection

```c
#define type_name(x) _Generic((x), int: "int", double: "double", char *: "char *", default: "other")
```

The expression's *type* (not value) picks an arm at compile time. This gives C its only real compile-time overload: type-safe wrappers over type-erased machinery — for example, dispatching to `hash_int` vs `hash_str` while callers never touch the wrong one.

## Tagged unions: runtime generics

```c
typedef struct { unsigned char tag; union { long i; double d; char *s; } as; } value_t;
```

The tag says which arm is live; readers switch on it. This is how interpreters, JSON libraries, and every dynamic value in C works. The union itself stores representations, not types — the discipline lives in the tag.

## Macros: know the boundary

Token pasting and stringizing build small DSLs (register tables, X-macro enum/string lists). But macros do not respect scope, cannot be taken as pointers, and double-evaluate arguments. The professional rule: macro for *boilerplate elimination*, functions (even tiny static ones) for logic.
""",
    "_Generic, tagged union, và ranh giới macro",
    "Điều phối lúc biên dịch theo nghĩa C23, tagged union lúc chạy, và khi nào macro là công cụ sai.",
    """
## _Generic: chọn lúc biên dịch

```c
#define type_name(x) _Generic((x), int: "int", double: "double", char *: "char *", default: "other")
```

*Kiểu* của biểu thức (không phải giá trị) chọn nhánh lúc biên dịch. Đây là overload thực sự duy nhất của C: wrapper an-toàn-kiểu bên trên máy móc xóa-kiểu — ví dụ điều phối hash_int vs hash_str mà caller không bao giờ đụng nhầm.

## Tagged union: tổng quát lúc chạy

```c
typedef struct { unsigned char tag; union { long i; double d; char *s; } as; } value_t;
```

Tag nói nhánh nào đang sống; người đọc switch theo nó. Interpreter, thư viện JSON, và mọi giá trị động trong C đều thế. Union chỉ lưu biểu diễn, không phải kiểu — kỷ luật nằm ở tag.

## Macro: biết ranh giới

Token pasting và stringizing dựng DSL nhỏ (bảng đăng ký, danh sách enum/chuỗi X-macro). Nhưng macro không tôn trọng phạm vi, không lấy được địa chỉ như hàm, và đánh giá đối số hai lần. Quy tắc chuyên nghiệp: macro để *xóa boilerplate*, hàm (kể cả hàm static tí hon) cho logic.
""",
)

write_practice(
    M8,
    "ca-p8-generic",
    "Generic Mechanism Drills",
    "Byte-addressed genericity, compile-time dispatch, tagged unions, and X-macro tables — mechanisms with observable contracts.",
    "Bài tập cơ chế tổng quát",
    "Tổng quát theo địa chỉ byte, điều phối lúc biên dịch, tagged union, và bảng X-macro — cơ chế với hợp đồng quan sát được.",
    L8A,
    24,
    "advanced",
    [
        challenge(
            "ca8-bytesort",
            "A qsort of Your Own",
            "Implement insertion sort over void* exactly like the library contract:@CE@ @CE@```c@CE@void isort(void *base, size_t n, size_t size, int (*cmp)(const void *, const void *));@CE@```@CE@ @CE@Elements move via a stack temp of up to 64 bytes and memcpy; stability is required (equal elements keep order).",
            C_PRELUDE,
            [
                ("sorts ints", "int a[5] = {5, 2, 4, 1, 3};@NL@isort(a, 5, sizeof(int), cmp_int);@NL@CHECK_EQ(a[0], 1);@NL@CHECK_EQ(a[4], 5);", "Byte-wise moves with size sizeof(int) and the comparator produce a correct sort."),
                ("stable on records", "rec_t r[3] = {{2, 20}, {1, 11}, {2, 22}};@NL@isort(r, 3, sizeof(rec_t), cmp_rec_key);@NL@CHECK_EQ(r[0].seq, 11);@NL@CHECK_EQ(r[1].seq, 20);@NL@CHECK_EQ(r[2].seq, 22);", "Equal keys keep original relative order — the definition of stability."),
            ],
            level="mini-build",
        ),
        challenge(
            "ca8-generic-dispatch",
            "_Generic Front Door",
            "Implement `const char *describe(value_t v)` over a tagged union `typedef struct { unsigned char tag; union { long i; double d; } as; } value_t;` with tags 1 = long, 2 = double: return 'long' or 'double' for the live arm. Then implement `long long to_int(long long x)` (identity) — and note in the test that a _Generic macro selects the *type* of its argument at compile time, which is how C keeps type-safety at such doors without overloads.",
            C_PRELUDE,
            [
                ("tag selects arm", "value_t a = {1, {.i = 42}};@NL@value_t b = {2, {.d = 2.5}};@NL@CHECK_STR_EQ(describe(a), \"long\");@NL@CHECK_STR_EQ(describe(b), \"double\");", "The tag is the runtime truth; describe reports the live arm."),
                ("identity plus _Generic proof", "CHECK_EQ(to_int(5), 5);@NL@CHECK_STR_EQ(_Generic(5, int: \"int\", default: \"other\"), \"int\");", "to_int is identity; the _Generic expression proves compile-time type selection by naming int's arm."),
            ],
            level="combination",
        ),
        challenge(
            "ca8-xmacro",
            "X-Macro Opcode Table",
            "Given the X-macro list already in your editor:@CE@ @CE@```c@CE@#define OP_LIST(X) X(OP_ADD) X(OP_SUB) X(OP_MUL)@CE@enum { @CE@#define OP_E(e) e,@CE@OP_LIST(OP_E)@CE@#undef OP_E@CE@OP_COUNT };@CE@```@CE@ @CE@implement `const char *op_name(unsigned op)` generating its strings from the *same* list (a second expansion with a stringizing X) — adding an opcode must extend both, or the table lies.",
            "#define OP_LIST(X) X(OP_ADD) X(OP_SUB) X(OP_MUL)@NL@" + C_PRELUDE,
            [
                ("names from one list", "CHECK_STR_EQ(op_name(OP_ADD), \"OP_ADD\");@NL@CHECK_STR_EQ(op_name(OP_SUB), \"OP_SUB\");@NL@CHECK_STR_EQ(op_name(OP_MUL), \"OP_MUL\");", "Stringizing X expands the same OP_LIST that built the enum — the two tables cannot drift."),
                ("bounds respected", "CHECK_NULL(op_name(999));", "Out-of-range opcodes return NULL rather than reading garbage."),
            ],
            level="combination",
        ),
    ],
    {
        "ca8-bytesort": vi_challenge(
            "qsort của riêng bạn",
            "Cài insertion sort trên void* đúng hợp đồng thư viện: isort(base, n, size, cmp) — di chuyển bằng memcpy, phải ổn định.",
            [
                ("sắp int", "Di chuyển theo byte với size sizeof(int) và comparator cho kết quả sắp đúng."),
                ("ổn định trên bản ghi", "Khóa bằng nhau giữ thứ tự tương đối ban đầu — định nghĩa của ổn định."),
            ],
        ),
        "ca8-generic-dispatch": vi_challenge(
            "Cửa trước _Generic",
            "Cài describe(value_t) trên tagged union (tag 1 = long, 2 = double) và to_int dùng _Generic để chứng minh chọn lúc biên dịch.",
            [
                ("tag chọn nhánh", "Tag là sự thật lúc chạy; describe báo nhánh đang sống."),
                ("_Generic chọn lúc biên dịch", "to_int(5) đi qua nhánh int (đồng nhất); nhánh double sẽ đi qua phép cắt."),
            ],
        ),
        "ca8-xmacro": vi_challenge(
            "Bảng opcode X-macro",
            "Có sẵn OP_LIST. Cài op_name(op) sinh chuỗi từ cùng danh sách (mở rộng thứ hai với X stringizing) — thêm opcode phải mở rộng cả hai.",
            [
                ("tên từ một danh sách", "Stringizing X mở rộng cùng OP_LIST đã dựng enum — hai bảng không thể lệch nhau."),
                ("tôn trọng biên", "Opcode ngoài phạm vi trả NULL thay vì đọc rác."),
            ],
        ),
    },
    solutions=[
        (
            "ca8-bytesort",
            "#include <string.h>@NL@" + C_PRELUDE
            + "int cmp_int(const void *a, const void *b) {@NL@    int x = *(const int *)a, y = *(const int *)b;@NL@    return (x > y) - (x < y);@NL@}@NL@"
            + "typedef struct { int key; int seq; } rec_t;@NL@"
            + "int cmp_rec_key(const void *a, const void *b) {@NL@    int x = ((const rec_t *)a)->key, y = ((const rec_t *)b)->key;@NL@    return (x > y) - (x < y);@NL@}@NL@"
            + "void isort(void *base, size_t n, size_t size, int (*cmp)(const void *, const void *)) {@NL@    unsigned char tmp[64];@NL@    unsigned char *b = base;@NL@    for (size_t i = 1; i < n; i++) {@NL@        memcpy(tmp, b + i * size, size);@NL@        size_t j = i;@NL@        while (j > 0 && cmp(b + (j - 1) * size, tmp) > 0) {@NL@            memcpy(b + j * size, b + (j - 1) * size, size);@NL@            j--;@NL@        }@NL@        memcpy(b + j * size, tmp, size);@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
            "#include <string.h>@NL@" + C_PRELUDE
            + "int cmp_int(const void *a, const void *b) {@NL@    int x = *(const int *)a, y = *(const int *)b;@NL@    return (x > y) - (x < y);@NL@}@NL@"
            + "typedef struct { int key; int seq; } rec_t;@NL@"
            + "int cmp_rec_key(const void *a, const void *b) {@NL@    int x = ((const rec_t *)a)->key, y = ((const rec_t *)b)->key;@NL@    return (x > y) - (x < y);@NL@}@NL@"
            + "void isort(void *base, size_t n, size_t size, int (*cmp)(const void *, const void *)) {@NL@    unsigned char tmp[64];@NL@    unsigned char *b = base;@NL@    for (size_t i = 1; i < n; i++) {@NL@        memcpy(tmp, b + i * size, size);@NL@        size_t j = i;@NL@        while (j > 0 && cmp(b + (j - 1) * size, tmp) >= 0) {@NL@            memcpy(b + j * size, b + (j - 1) * size, size);@NL@            j--;@NL@        }@NL@        memcpy(b + j * size, tmp, size);@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca8-generic-dispatch",
            C_PRELUDE
            + "typedef struct { unsigned char tag; union { long i; double d; } as; } value_t;@NL@"
            + "const char *describe(value_t v) {@NL@    switch (v.tag) {@NL@    case 1: return \"long\";@NL@    case 2: return \"double\";@NL@    default: return \"unknown\";@NL@    }@NL@}@NL@"
            + "long long to_int(long long x) { return x; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "typedef struct { unsigned char tag; union { long i; double d; } as; } value_t;@NL@"
            + "const char *describe(value_t v) {@NL@    return v.tag == 1 ? \"double\" : \"long\";@NL@}@NL@"
            + "long long to_int(long long x) { return x; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca8-xmacro",
            "#define OP_LIST(X) X(OP_ADD) X(OP_SUB) X(OP_MUL)@NL@" + C_PRELUDE
            + "enum {@NL@#define OP_E(e) e,@NL@OP_LIST(OP_E)@NL@#undef OP_E@NL@OP_COUNT };@NL@"
            + "const char *op_name(unsigned op) {@NL@    switch (op) {@NL@#define OP_N(e) case e: return #e;@NL@OP_LIST(OP_N)@NL@#undef OP_N@NL@    default: return NULL;@NL@    }@NL@}@NL@"
            + "int main(void) { return 0; }",
            "#define OP_LIST(X) X(OP_ADD) X(OP_SUB) X(OP_MUL)@NL@" + C_PRELUDE
            + "enum {@NL@#define OP_E(e) e,@NL@OP_LIST(OP_E)@NL@#undef OP_E@NL@OP_COUNT };@NL@"
            + "const char *op_name(unsigned op) {@NL@    if (op == OP_ADD) return \"OP_SUB\";@NL@    if (op == OP_SUB) return \"OP_MUL\";@NL@    if (op == OP_MUL) return \"OP_ADD\";@NL@    return NULL;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M8,
    L8CP,
    "Checkpoint: One Table, Many Types",
    "Consolidated generic-programming checkpoint.",
    12,
    """
Checkpoint for module 8: a byte-wise generic container holding tagged values, sorted through a comparator, reported through a tag-driven describe.
""",
    "Kiểm tra: Một bảng, nhiều kiểu",
    "Kiểm tra tổng hợp lập trình tổng quát.",
    """
Kiểm tra mô-đun 8: container tổng quát theo byte chứa giá trị có tag, được sắp qua comparator, và mô tả qua describe điều khiển bởi tag.
""",
)

write_checkpoint(
    M8,
    L8CP,
    "Checkpoint: Generic Byte Container",
    "One program: insert tagged values into a byte-addressed array, sort them by a comparator over their payload, and verify both the order and the type dispatch.",
    16,
    "See lesson.",
    "Kiểm tra: Container byte tổng quát",
    "Một chương trình: chèn giá trị có tag vào mảng địa-chỉ-byte, sắp bằng comparator trên payload, và xác minh cả thứ tự lẫn điều phối kiểu.",
    "Xem bài học.",
    challenge(
        "ca8-checkpoint-generic",
        "Checkpoint: Generic Tagged Sort",
        "Types already in your editor:@CE@ @CE@```c@CE@typedef struct { unsigned char tag; int key; } item_t; /* tag 1 = int-like, 2 = double-like */@CE@```@CE@ @CE@Implement:@CE@1. `void item_sort(item_t *a, size_t n)` — insertion sort over the array treating elements as raw bytes (memcpy moves, comparator on key), stable.@CE@2. `const char *item_describe(const item_t *v)` — returns \"int-like\" for tag 1, \"double-like\" for tag 2, NULL otherwise.@CE@3. `size_t item_count_tag(const item_t *a, size_t n, unsigned char tag)` — how many carry the tag.",
        C_PRELUDE,
        [
            ("stable sort by key", "item_t a[4] = {{2, 30}, {1, 20}, {2, 10}, {1, 40}};@NL@item_sort(a, 4);@NL@CHECK_EQ(a[0].key, 10);@NL@CHECK_EQ(a[1].key, 20);@NL@CHECK_EQ(a[2].tag, 2);@NL@CHECK_EQ(a[3].tag, 1);", "Keys order 10, 20, 30, 40; the two tag-2 items keep relative order with their tag-1 neighbors."),
            ("describe dispatch", "item_t v = {2, 0};@NL@CHECK_STR_EQ(item_describe(&v), \"double-like\");@NL@CHECK_NULL(item_describe(&(item_t){7, 0}));", "Tag 1 and 2 report their names; unknown tags return NULL."),
            ("tag counting", "item_t b[3] = {{1, 0}, {2, 0}, {1, 0}};@NL@CHECK_EQ((int)item_count_tag(b, 3, 1), 2);@NL@CHECK_EQ((int)item_count_tag(b, 3, 2), 1);@NL@CHECK_EQ((int)item_count_tag(b, 3, 9), 0);", "Counting per tag is a plain linear scan with an exact contract."),
        ],
        level="mini-build",
    ),
    {
        "ca8-checkpoint-generic": vi_challenge(
            "Kiểm tra: Sắp tổng quát có tag",
            "Có sẵn item_t {tag, key}. Cài item_sort (insertion sort theo byte, ổn định, so trên key), item_describe (theo tag), item_count_tag.",
            [
                ("sắp ổn định theo key", "Key xếp 10, 20, 30, 40; các phần tử tag 2 giữ thứ tự tương đối với láng giềng tag 1."),
                ("describe điều phối", "Tag 1 và 2 báo đúng tên; tag lạ trả NULL."),
                ("đếm theo tag", "Đếm theo tag là quét tuyến tính với hợp đồng chính xác."),
            ],
        )
    },
    solution=C_PRELUDE
    + "#include <string.h>@NL@"
    + "typedef struct { unsigned char tag; int key; } item_t;@NL@"
    + "void item_sort(item_t *a, size_t n) {@NL@    unsigned char tmp[sizeof(item_t)];@NL@    for (size_t i = 1; i < n; i++) {@NL@        memcpy(tmp, &a[i], sizeof(item_t));@NL@        size_t j = i;@NL@        while (j > 0 && a[j - 1].key > ((item_t *)tmp)->key) {@NL@            memcpy(&a[j], &a[j - 1], sizeof(item_t));@NL@            j--;@NL@        }@NL@        memcpy(&a[j], tmp, sizeof(item_t));@NL@    }@NL@}@NL@"
    + "const char *item_describe(const item_t *v) {@NL@    if (!v) return NULL;@NL@    if (v->tag == 1) return \"int-like\";@NL@    if (v->tag == 2) return \"double-like\";@NL@    return NULL;@NL@}@NL@"
    + "size_t item_count_tag(const item_t *a, size_t n, unsigned char tag) {@NL@    size_t c = 0;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (a[i].tag == tag) c++;@NL@    }@NL@    return c;@NL@}@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "#include <string.h>@NL@"
    + "typedef struct { unsigned char tag; int key; } item_t;@NL@"
    + "void item_sort(item_t *a, size_t n) {@NL@    unsigned char tmp[sizeof(item_t)];@NL@    for (size_t i = 1; i < n; i++) {@NL@        memcpy(tmp, &a[i], sizeof(item_t));@NL@        size_t j = i;@NL@        while (j > 0 && a[j - 1].key >= ((item_t *)tmp)->key) {@NL@            memcpy(&a[j], &a[j - 1], sizeof(item_t));@NL@            j--;@NL@        }@NL@        memcpy(&a[j], tmp, sizeof(item_t));@NL@    }@NL@}@NL@"
    + "const char *item_describe(const item_t *v) {@NL@    if (!v) return NULL;@NL@    if (v->tag == 1) return \"double-like\";@NL@    if (v->tag == 2) return \"int-like\";@NL@    return NULL;@NL@}@NL@"
    + "size_t item_count_tag(const item_t *a, size_t n, unsigned char tag) {@NL@    size_t c = 0;@NL@    for (size_t i = 0; i < n; i++) {@NL@        if (a[i].tag == tag) c++;@NL@    }@NL@    return c;@NL@}@NL@"
    + "int main(void) { return 0; }",
)
