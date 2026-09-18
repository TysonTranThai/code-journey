#!/usr/bin/env python3
"""C — Intermediate — Module 8: cint-hash.

Hash tables from scratch: open-addressing with linear probing (int keys),
then separate chaining with generic void* values and a destroy callback —
the ownership seam where generic containers get dangerous. House
conventions: ISO C only, self-contained tests, Ws are behavioral
near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-hash"

write_module(
    M,
    "Hash Tables",
    "Average O(1) you build yourself: load factor, probing, chaining, and "
    "the ownership seam of generic values.",
    "Bảng băm",
    "O(1) trung bình bạn tự dựng: load factor, probing, chaining, và "
    "đườngOwnership của giá trị generic.",
    lessons=["hash-basics", "collisions", "generic-values", "cint-checkpoint-m8"],
    practices=["cint-p8-open", "cint-p8-chain"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "hash-basics",
    "The Array Behind the Magic",
    "Hash function, buckets, load factor, and why resizing is not optional.",
    16,
    r"""
## Trade a range for a slot

An array gives O(1) by *index*. A hash table gives O(1) *on average* by
*key*: a hash function maps the key to a bucket index:

```c
size_t idx = hash(key) % nbuckets;
```

Two properties divide good hash functions from bad: **determinism**
(same key → same bucket, always) and **uniformity** (keys spread evenly;
clusters become linear scans). For integers, multiplicative hashing is
the honest floor:

```c
/* Knuth multiplicative: fine for teaching, not for adversarial keys */
size_t h = (size_t)key * 2654435761u;
```

For strings, FNV-1a is the standard simple choice — multiply-then-xor
over every byte, so "ab" and "ba" differ.

## Load factor is the whole performance story

`load = n_entries / n_buckets`. With separate chaining, expected chain
length *is* the load factor — lookups are O(1 + load). Past ~1.0,
chains grow and the "constant" quietly becomes linear. The fix is
**resizing**: when load crosses a threshold (commonly 0.75), allocate a
bigger bucket array and *rehash every entry* — their indices change,
because the modulus changed. Resize is O(n) but amortized O(1) per
insertion, exactly like a growing dynamic array.

With open addressing, load must stay *lower* (0.5–0.7): probing clusters
degrade quadratically-ish as the table fills, and at 1.0 the table is
full — an insert can fail even though keys differ.
""",
"Mảng đứng sau phép màu",
    "Hàm băm, bucket, load factor, và vì sao resize không phải tùy chọn.",
    r"""
## Mảng đứng sau phép màu

Mảng cho O(1) theo *chỉ số*. Hash table cho O(1) *trung bình* theo *key*:
hàm băm maps key sang chỉ số bucket:

```c
size_t idx = hash(key) % nbuckets;
```

Hai tính chất chia hàm băm tốt/xấu: **định quán** (key giống → bucket
giống, luôn vậy) và **đều** (keys rải đều; cụm thành linear scan). Với
số nguyên, multiplicative hashing là sàn trung thực:

```c
/* Knuth multiplicative: đủ để dạy, không chống key đối kháng */
size_t h = (size_t)key * 2654435761u;
```

Với chuỗi, FNV-1a là lựa chọn đơn giản chuẩn — nhân rồi xor từng byte,
nên "ab" và "ba" khác nhau.

## Load factor là toàn bộ câu chuyện hiệu năng

`load = số phần tử / số bucket`. Với separate chaining, chiều dài chuỗi
kỳ vọng *chính là* load factor — lookup là O(1 + load). Quá ~1.0, chuỗi
dài dần và "hằng số" lặng lẽ thành tuyến tính. Cách chữa là **resize**:
khi load vượt ngưỡng (thường 0.75), cấp phát mảng bucket lớn hơn và
*rehash mọi phần tử* — chỉ số của chúng đổi, vì modulus đổi. Resize là
O(n) nhưng amortized O(1) mỗi lần chèn, đúng như dynamic array.

Với open addressing, load phải *thấp hơn* (0.5–0.7): cụm probing xấu đi
nhanh khi bảng đầy, và ở 1.0 bảng kín — insert có thể thất bại dù các
key khác nhau.
"""
)

write_lesson(
    M, "collisions",
    "Collisions: Chaining vs Probing",
    "Two keys, one bucket. The two classical answers and their tradeoffs.",
    16,
    r"""
## Separate chaining: a list per bucket

```c
typedef struct HNode {
    long          key;
    int           value;
    struct HNode *next;
} HNode;
HNode **buckets;      /* nbuckets slots, each NULL or a chain head */
```

Insert pushes at the chain head — O(1) always. Lookup walks one chain.
Delete unlinks (the `HNode **link` walk you already know). Chaining
tolerates load > 1 and never fails to insert; the costs are a pointer
per node, malloc traffic, and cache misses walking chains.

## Open addressing: everything lives in the array

No nodes. On collision, *probe* — try the next slot (linear probing),
the slot at h+1², h+2² (quadratic), or the "double hash" stride. Lookup
follows the same probe sequence until an empty slot proves absence.
The subtlety is **deletion**: removing an entry leaves a hole that
would cut probe sequences — so deletions mark the slot *tombstone*
(occupied-for-probing, empty-for-insert), and tombstones need periodic
cleanup or the table slowly fills with ghosts.

| | chaining | open addressing |
|---|---|---|
| delete | easy | tombstones |
| load limit | >1 fine | 0.5–0.7 |
| memory | pointer/node | dense, cache-friendly |
| worst case | one long chain | full-table scan |

Rule of thumb: open addressing when memory locality matters (big
in-memory tables), chaining when deletion is frequent or load is
unpredictable.
""",
"Va chạm: Chaining vs Probing",
    "Hai key, một bucket. Hai câu trả lời kinh điển và đánh đổi của chúng.",
    r"""
## Separate chaining: một list mỗi bucket

```c
typedef struct HNode {
    long          key;
    int           value;
    struct HNode *next;
} HNode;
HNode **buckets;      /* nbuckets slot, mỗi slot NULL hoặc đầu chuỗi */
```

Chèn đẩy vào đầu chuỗi — luôn O(1). Lookup đi một chuỗi. Delete unlinks
(bạn đã biết phép đi `HNode **link`). Chaining chịu load > 1 và không
bao giờ hết chỗ chèn; giá phải trả là một con trỏ mỗi node, malloc
thường xuyên, và cache miss khi đi chuỗi.

## Open addressing: tất cả nằm trong mảng

Không node. Khi va chạm, *probe* — thử slot kế (linear), slot h+1², h+2²
(quadratic), hoặc bước "double hash". Lookup đi cùng chuỗi probe đến khi
slot rỗng chứng minh absence. Điều tinh tế là **xóa**: gỡ một phần tử để
lại lỗ thủng cắt đứt chuỗi probe — nên xóa đánh dấu slot thành
*tombstone* (chiếm chỗ khi probe, rỗng khi chèn), và tombstone cần dọn
định kỳ hoặc bảng đầy dần các con ma.

| | chaining | open addressing |
|---|---|---|
| xóa | dễ | tombstone |
| giới hạn load | >1 vẫn ổn | 0.5–0.7 |
| bộ nhớ | con trỏ/node | dày, cache-friendly |
| xấu nhất | một chuỗi dài | quét cả bảng |

Kinh nghiệm: open addressing khi locality bộ nhớ quan trọng (bảng lớn
trong RAM), chaining khi xóa nhiều hoặc load khó đoán.
"""
)

write_lesson(
    M, "generic-values",
    "Generic Values & the Ownership Seam",
    "void* makes a container generic — and makes 'who frees this?' a "
    "design decision you must publish.",
    17,
    r"""
## void* is a promise, not a type

```c
typedef struct HNode {
    const char   *key;      /* borrowed: caller keeps it alive */
    void         *value;    /* OWNERSHIP: decided by the table's policy */
    struct HNode *next;
} HNode;
```

The table cannot know what `value` points at. That is the point — and
the danger. Every generic container must publish an **ownership policy**,
and the clean way to make it explicit is a callback:

```c
typedef void (*FreeFn)(void *value);
/* destroy_frees: if true, hmap_destroy calls free_value on every value
   still stored; if false, values are left for their owner. */
void hmap_destroy(HMap *m, int destroy_frees, FreeFn free_value);
```

Now the contract is checkable at the call site: a table of malloc'd
buffers passes `1, free`; a table of borrowed strings passes `0, NULL`.
The bug class this kills: double frees when two containers both "clean
up" the same values, and leaks when none does.

## Keys are almost always borrowed

Values may be owned; keys should be *borrowed* — the caller's string
lives in the caller's storage, the table only compares addresses of
characters. If the table must own keys (the caller's buffer dies), it
must `strdup` them — and then it owns two things, and the policy
multiplies. Borrowed keys keep one rule: the key outlives the entry.

## The iteration contract

Any table that can be walked (`hmap_foreach`) must publish what
mutations during iteration do. The safe rule: you may *replace* the
current entry's value; you may not insert or remove while iterating.
Enforce it or document the undefined behavior — silent corruption is
the alternative.
""",
"Giá trị generic & đường ownership",
    "void* làm container generic — và biến 'ai free cái này?' thành quyết "
    "định thiết kế bạn phải công bố.",
    r"""
## void* là lời hứa, không phải kiểu

```c
typedef struct HNode {
    const char   *key;      /* mượn: caller giữ nó sống */
    void         *value;    /* OWNERSHIP: do policy của bảng quyết định */
    struct HNode *next;
} HNode;
```

Bảng không thể biết `value` trỏ vào gì. Đó là mục đích — và là nguy hiểm.
Mỗi generic container phải công bố **ownership policy**, và cách sạch để
làm nó tường minh là callback:

```c
typedef void (*FreeFn)(void *value);
/* destroy_frees: nếu true, hmap_destroy gọi free_value trên mọi value
   còn lưu; nếu false, value để lại cho chủ sở hữu. */
void hmap_destroy(HMap *m, int destroy_frees, FreeFn free_value);
```

Giờ hợp đồng kiểm được tại chỗ gọi: bảng của buffer malloc'd truyền
`1, free`; bảng của chuỗi mượn truyền `0, NULL`. Họ bug điều này giết
chết: double free khi hai container cùng "dọn" chung value, và leak khi
không ai dọn.

## Key gần như luôn mượn

Value có thể sở hữu; key nên *mượn* — chuỗi của caller nằm trong kho của
caller, bảng chỉ so sánh ký tự. Nếu bảng phải sở hữu key (buffer của
caller chết), nó phải `strdup` — và giờ nó sở hữu hai thứ, policy nhân
đôi. Key mượn giữ một quy tắc: key sống lâu hơn entry.

## Hợp đồng duyệt

Mọi bảng đi được (`hmap_foreach`) phải công bố việc biến đổi trong lúc
duệt làm gì. Quy tắc an toàn: được *thay* value của entry hiện tại;
không được chèn/xóa khi đang duyệt. Thực thi hoặc ghi rõ hành vi
undefined — thay vào đó là hỏng âm thầm.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p8-open",
    "Open Addressing Gym",
    "Linear-probing table with tombstones — the classic implementation, done right.",
    "Phòng gym open addressing",
    "Bảng linear-probing với tombstone — cài đặt kinh điển, làm đúng.",
    after_lesson="collisions",
    minutes=28,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p8-linear",
            "Linear Probe + Tombstone",
            """Implement an open-addressing table, long keys, int values.
The boilerplate declares:

```c
#define OTAB_CAP 16
/* status: 0 empty, 1 occupied, 2 tombstone */
typedef struct { long key; int value; int status; } OSlot;
typedef struct { OSlot slots[OTAB_CAP]; size_t count; } OTab;
void otab_init(OTab *t);                       /* all empty */
/* returns bucket index probed... no: 0 ok, 1 already-present
   (value updated), -1 table full (no empty AND no tombstone slot) */
int otab_put(OTab *t, long key, int value);
int otab_get(const OTab *t, long key, int *out);  /* 0 found, -1 absent */
/* marks a tombstone; 1 removed, 0 absent */
int otab_del(OTab *t, long key);
size_t otab_size(const OTab *t);               /* live entries only */
```

Hash: `(size_t)key % OTAB_CAP`, linear probing. Deleted slots become
tombstones — they are skipped by get, reused by put.""",
            C_PRELUDE + "\n#include <stddef.h>\n#define OTAB_CAP 16\ntypedef struct { long key; int value; int status; } OSlot;\ntypedef struct { OSlot slots[OTAB_CAP]; size_t count; } OTab;\nvoid otab_init(OTab *t);\nint otab_put(OTab *t, long key, int value);\nint otab_get(const OTab *t, long key, int *out);\nint otab_del(OTab *t, long key);\nsize_t otab_size(const OTab *t);\n",
            [
                (
                    "put/get/update",
                    r"""
OTab t;
otab_init(&t);
int v;
CHECK_EQ(otab_size(&t), 0);
CHECK_EQ(otab_get(&t, 42, &v), -1);          /* absent */
CHECK_EQ(otab_put(&t, 42, 1), 0);
CHECK_EQ(otab_put(&t, 42 + 16, 7), 0);       /* same bucket: probe */
CHECK_EQ(otab_get(&t, 42, &v), 0); CHECK_EQ(v, 1);
CHECK_EQ(otab_get(&t, 42 + 16, &v), 0); CHECK_EQ(v, 7);
CHECK_EQ(otab_put(&t, 42, 99), 1);           /* update, not duplicate */
CHECK_EQ(otab_size(&t), 2);
CHECK_EQ(otab_get(&t, 42, &v), 0); CHECK_EQ(v, 99);
""",
                    "put walks: occupied && same key -> update; empty -> insert; tombstone -> remember first, keep probing for the key.",
                ),
                (
                    "delete leaves a probe path",
                    r"""
OTab t;
otab_init(&t);
/* collide deliberately: keys k, k+16, k+32 share a bucket */
CHECK_EQ(otab_put(&t, 5, 10), 0);
CHECK_EQ(otab_put(&t, 21, 20), 0);
CHECK_EQ(otab_put(&t, 37, 30), 0);
CHECK_EQ(otab_del(&t, 21), 1);               /* middle of the chain */
CHECK_EQ(otab_del(&t, 21), 0);
CHECK_EQ(otab_size(&t), 2);
int v;
CHECK_EQ(otab_get(&t, 37, &v), 0);           /* probe THROUGH tombstone */
CHECK_EQ(v, 30);
CHECK_EQ(otab_get(&t, 5, &v), 0); CHECK_EQ(v, 10);
CHECK_EQ(otab_put(&t, 21, 55), 0);           /* tombstone reused */
CHECK_EQ(otab_get(&t, 21, &v), 0); CHECK_EQ(v, 55);
""",
                    "The classic bug: delete sets the slot empty and 37 becomes unreachable. Tombstone keeps get working; put may reuse it.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p8-linear": vi_challenge(
            "Linear probe + tombstone",
            "Cài OTab: put/get/del với probing tuyến tính; xóa để tombstone; put cập nhật key có sẵn -> 1.",
            [("xóa giữ đường probe", "tombstone: get nhảy qua, put tái sử dụng; get phải đi xuyên qua.")],
        ),
    },
    solutions=[
        (
            "cint-p8-linear",
            r"""
#include <string.h>
#include <stddef.h>
void otab_init(OTab *t) {
    if (!t) return;
    memset(t, 0, sizeof *t);
}
static size_t bucket(long key) { return (size_t)key % OTAB_CAP; }
int otab_put(OTab *t, long key, int value) {
    if (!t) return -1;
    size_t i = bucket(key);
    size_t tomb = (size_t)-1;
    for (size_t probe = 0; probe < OTAB_CAP; probe++) {
        OSlot *s = &t->slots[i];
        if (s->status == 1 && s->key == key) {
            s->value = value;
            return 1;                     /* updated */
        }
        if (s->status == 0) {
            /* insert at first tombstone if seen, else here */
            size_t at = (tomb != (size_t)-1) ? tomb : i;
            t->slots[at].key = key;
            t->slots[at].value = value;
            t->slots[at].status = 1;
            t->count++;
            return 0;
        }
        if (s->status == 2 && tomb == (size_t)-1) tomb = i;
        i = (i + 1) % OTAB_CAP;
    }
    if (tomb != (size_t)-1) {             /* full of tombstones/occupied: reuse tombstone */
        t->slots[tomb].key = key;
        t->slots[tomb].value = value;
        t->slots[tomb].status = 1;
        t->count++;
        return 0;
    }
    return -1;                            /* truly full */
}
int otab_get(const OTab *t, long key, int *out) {
    if (!t || !out) return -1;
    size_t i = bucket(key);
    for (size_t probe = 0; probe < OTAB_CAP; probe++) {
        const OSlot *s = &t->slots[i];
        if (s->status == 0) return -1;    /* empty terminates the probe */
        if (s->status == 1 && s->key == key) {
            *out = s->value;
            return 0;
        }
        i = (i + 1) % OTAB_CAP;           /* tombstones and other keys: keep probing */
    }
    return -1;
}
int otab_del(OTab *t, long key) {
    if (!t) return 0;
    size_t i = bucket(key);
    for (size_t probe = 0; probe < OTAB_CAP; probe++) {
        OSlot *s = &t->slots[i];
        if (s->status == 0) return 0;
        if (s->status == 1 && s->key == key) {
            s->status = 2;                /* tombstone */
            t->count--;
            return 1;
        }
        i = (i + 1) % OTAB_CAP;
    }
    return 0;
}
size_t otab_size(const OTab *t) { return t ? t->count : 0; }""",
            r"""
#include <string.h>
#include <stddef.h>
void otab_init(OTab *t) {
    if (!t) return;
    memset(t, 0, sizeof *t);
}
static size_t bucket(long key) { return (size_t)key % OTAB_CAP; }
int otab_put(OTab *t, long key, int value) {
    if (!t) return -1;
    size_t i = bucket(key);
    for (size_t probe = 0; probe < OTAB_CAP; probe++) {
        OSlot *s = &t->slots[i];
        if (s->status == 1 && s->key == key) {
            s->value = value;
            return 1;
        }
        if (s->status != 1) {             /* wrong: inserts onto a TOMBSTONE
                                             without checking whether the key
                                             already lives further along the probe
                                             chain -> duplicate keys */
            s->key = key;
            s->value = value;
            s->status = 1;
            t->count++;
            return 0;
        }
        i = (i + 1) % OTAB_CAP;
    }
    return -1;
}
int otab_get(const OTab *t, long key, int *out) {
    if (!t || !out) return -1;
    size_t i = bucket(key);
    for (size_t probe = 0; probe < OTAB_CAP; probe++) {
        const OSlot *s = &t->slots[i];
        if (s->status == 0 || s->status == 2) return -1;  /* wrong: tombstone
                                             stops the probe -> entries after a
                                             deletion become unreachable */
        if (s->status == 1 && s->key == key) {
            *out = s->value;
            return 0;
        }
        i = (i + 1) % OTAB_CAP;
    }
    return -1;
}
int otab_del(OTab *t, long key) {
    if (!t) return 0;
    size_t i = bucket(key);
    for (size_t probe = 0; probe < OTAB_CAP; probe++) {
        OSlot *s = &t->slots[i];
        if (s->status == 0) return 0;
        if (s->status == 1 && s->key == key) {
            memset(s, 0, sizeof *s);      /* wrong: empty hole cuts the probe chain */
            t->count--;
            return 1;
        }
        i = (i + 1) % OTAB_CAP;
    }
    return 0;
}
size_t otab_size(const OTab *t) { return t ? t->count : 0; }""",
        ),
    ],
)

write_practice(
    M, "cint-p8-chain",
    "Chaining & Generic Values Gym",
    "Separate-chaining map with generic void* values and a published ownership policy.",
    "Phòng gym chaining & giá trị generic",
    "Map separate-chaining với giá trị void* generic và ownership policy được công bố.",
    after_lesson="generic-values",
    minutes=28,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p8-hmap",
            "The Chaining Map",
            """Implement a string-keyed map with chaining. The boilerplate declares:

```c
#define HMAP_BUCKETS 8
typedef struct HNode {
    const char   *key;      /* borrowed */
    int           value;
    struct HNode *next;
} HNode;
typedef struct { HNode *buckets[HMAP_BUCKETS]; size_t count; } HMap;
void hmap_init(HMap *m);
/* 0 inserted, 1 updated, -1 bad args. key is borrowed. */
int hmap_put(HMap *m, const char *key, int value);
int hmap_get(const HMap *m, const char *key, int *out); /* 0 found, -1 absent */
int hmap_del(HMap *m, const char *key);                 /* 1 removed, 0 absent */
size_t hmap_size(const HMap *m);
/* longest chain length (collision health metric) */
size_t hmap_max_chain(const HMap *m);
void hmap_destroy(HMap *m);
```

Hash: FNV-1a over the key's bytes, mod buckets.""",
            C_PRELUDE + "\n#include <stddef.h>\n#define HMAP_BUCKETS 8\ntypedef struct HNode {\n    const char   *key;\n    int           value;\n    struct HNode *next;\n} HNode;\ntypedef struct { HNode *buckets[HMAP_BUCKETS]; size_t count; } HMap;\nvoid hmap_init(HMap *m);\nint hmap_put(HMap *m, const char *key, int value);\nint hmap_get(const HMap *m, const char *key, int *out);\nint hmap_del(HMap *m, const char *key);\nsize_t hmap_size(const HMap *m);\nsize_t hmap_max_chain(const HMap *m);\nvoid hmap_destroy(HMap *m);\n",
            [
                (
                    "map lifecycle",
                    r"""
HMap m;
hmap_init(&m);
int v;
CHECK_EQ(hmap_size(&m), 0);
CHECK_EQ(hmap_get(&m, "a", &v), -1);
CHECK_EQ(hmap_put(&m, "alpha", 1), 0);
CHECK_EQ(hmap_put(&m, "bravo", 2), 0);
CHECK_EQ(hmap_put(&m, "alpha", 11), 1);      /* update */
CHECK_EQ(hmap_size(&m), 2);
CHECK_EQ(hmap_get(&m, "alpha", &v), 0); CHECK_EQ(v, 11);
CHECK_EQ(hmap_get(&m, "bravo", &v), 0); CHECK_EQ(v, 2);
CHECK_EQ(hmap_del(&m, "alpha"), 1);
CHECK_EQ(hmap_del(&m, "alpha"), 0);
CHECK_EQ(hmap_get(&m, "alpha", &v), -1);
CHECK_EQ(hmap_get(&m, "bravo", &v), 0);      /* other keys intact */
CHECK_EQ(hmap_put(NULL, "x", 1), -1);
CHECK_EQ(hmap_put(&m, NULL, 1), -1);
hmap_destroy(&m);
""",
                    "FNV-1a: h = 2166136261u; per byte: h ^= byte, h *= 16777619u. Put walks its chain for the key before pushing.",
                ),
                (
                    "collisions are visible",
                    r"""
HMap m;
hmap_init(&m);
/* keys must LIVE for the whole test: the map borrows them, so one
   reused stack buffer would alias every entry (the lifetime rule). */
char keys[12][8];
for (int i = 0; i < 12; i++) {
    snprintf(keys[i], sizeof keys[i], "k%d", i);
    CHECK_EQ(hmap_put(&m, keys[i], i), 0);
}
CHECK_EQ(hmap_size(&m), 12);
CHECK(hmap_max_chain(&m) >= 2);              /* pigeonhole: 12 into 8 */
CHECK(hmap_max_chain(&m) <= 12);
/* every key still findable */
for (int i = 0; i < 12; i++) {
    int v;
    CHECK_EQ(hmap_get(&m, keys[i], &v), 0);
    CHECK_EQ(v, i);
}
hmap_destroy(&m);
""",
                    "12 keys into 8 buckets: pigeonhole forces a chain of 2+. max_chain just walks and counts. Keys live in a 2D array — the map borrows them.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p8-hmap": vi_challenge(
            "Bản đồ chaining",
            "Cài HMap: put/get/del/size/max_chain/destroy; key mượn; FNV-1a mod 8.",
            [("vòng đời map", "put đi chuỗi tìm key trước khi đẩy đầu; del unlinks.")],
        ),
    },
    solutions=[
        (
            "cint-p8-hmap",
            r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
static size_t fnv1a(const char *s) {
    size_t h = 2166136261u;
    for (const unsigned char *p = (const unsigned char *)s; *p; p++) {
        h ^= *p;
        h *= 16777619u;
    }
    return h;
}
void hmap_init(HMap *m) {
    if (!m) return;
    memset(m, 0, sizeof *m);
}
int hmap_put(HMap *m, const char *key, int value) {
    if (!m || !key) return -1;
    size_t b = fnv1a(key) % HMAP_BUCKETS;
    for (HNode *n = m->buckets[b]; n; n = n->next)
        if (strcmp(n->key, key) == 0) {
            n->value = value;
            return 1;
        }
    HNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->key = key;
    n->value = value;
    n->next = m->buckets[b];
    m->buckets[b] = n;
    m->count++;
    return 0;
}
int hmap_get(const HMap *m, const char *key, int *out) {
    if (!m || !key || !out) return -1;
    size_t b = fnv1a(key) % HMAP_BUCKETS;
    for (const HNode *n = m->buckets[b]; n; n = n->next)
        if (strcmp(n->key, key) == 0) {
            *out = n->value;
            return 0;
        }
    return -1;
}
int hmap_del(HMap *m, const char *key) {
    if (!m || !key) return 0;
    size_t b = fnv1a(key) % HMAP_BUCKETS;
    HNode **link = &m->buckets[b];
    while (*link) {
        HNode *n = *link;
        if (strcmp(n->key, key) == 0) {
            *link = n->next;
            free(n);
            m->count--;
            return 1;
        }
        link = &n->next;
    }
    return 0;
}
size_t hmap_size(const HMap *m) { return m ? m->count : 0; }
size_t hmap_max_chain(const HMap *m) {
    if (!m) return 0;
    size_t mx = 0;
    for (size_t b = 0; b < HMAP_BUCKETS; b++) {
        size_t len = 0;
        for (const HNode *n = m->buckets[b]; n; n = n->next) len++;
        if (len > mx) mx = len;
    }
    return mx;
}
void hmap_destroy(HMap *m) {
    if (!m) return;
    for (size_t b = 0; b < HMAP_BUCKETS; b++)
        while (m->buckets[b]) {
            HNode *n = m->buckets[b];
            m->buckets[b] = n->next;
            free(n);
        }
    m->count = 0;
}""",
            r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
static size_t fnv1a(const char *s) {
    size_t h = 2166136261u;
    for (const unsigned char *p = (const unsigned char *)s; *p; p++) {
        h ^= *p;
        h *= 16777619u;
    }
    return h;
}
void hmap_init(HMap *m) {
    if (!m) return;
    memset(m, 0, sizeof *m);
}
int hmap_put(HMap *m, const char *key, int value) {
    if (!m || !key) return -1;
    size_t b = fnv1a(key) % HMAP_BUCKETS;
    HNode *n = malloc(sizeof *n);       /* wrong: allocates BEFORE checking
                                             for an existing key -> duplicates */
    if (!n) return -1;
    n->key = key;
    n->value = value;
    n->next = m->buckets[b];
    m->buckets[b] = n;
    m->count++;
    return 0;
}
int hmap_get(const HMap *m, const char *key, int *out) {
    if (!m || !key || !out) return -1;
    size_t b = fnv1a(key) % HMAP_BUCKETS;
    for (const HNode *n = m->buckets[b]; n; n = n->next)
        if (n->key == key) {            /* wrong: pointer identity, not strcmp —
                                             equal contents in different buffers miss */
            *out = n->value;
            return 0;
        }
    return -1;
}
int hmap_del(HMap *m, const char *key) {
    if (!m || !key) return 0;
    size_t b = fnv1a(key) % HMAP_BUCKETS;
    for (HNode *n = m->buckets[b]; n; n = n->next) {
        if (strcmp(n->key, key) == 0) {
            free(n);                    /* wrong: previous node still points here */
            m->count--;
            return 1;
        }
    }
    return 0;
}
size_t hmap_size(const HMap *m) { return m ? m->count : 0; }
size_t hmap_max_chain(const HMap *m) {
    if (!m) return 0;
    size_t mx = 0;
    for (size_t b = 0; b < HMAP_BUCKETS; b++) {
        size_t len = 0;
        for (const HNode *n = m->buckets[b]; n; n = n->next) len++;
        if (len > mx) mx = len;
    }
    return mx;
}
void hmap_destroy(HMap *m) {
    if (!m) return;
    for (size_t b = 0; b < HMAP_BUCKETS; b++) {
        HNode *n = m->buckets[b];
        while (n) {
            free(n);                    /* wrong: reads n->next after free */
            n = n->next;
        }
        m->buckets[b] = NULL;
    }
    m->count = 0;
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m8-task",
    "Word Frequency Counter",
    """Combine the module: count word frequencies from an array of tokens.
The boilerplate declares:

```c
#define WF_BUCKETS 16
typedef struct WFNode {
    const char   *word;     /* the table strdups it: it OWNS its keys */
    size_t        count;
    struct WFNode *next;
} WFNode;
typedef struct { WFNode *buckets[WF_BUCKETS]; size_t distinct; } WF;
void wf_init(WF *w);
int wf_count(WF *w, const char *word);   /* 0 ok, -1 bad args/oom */
/* returns 1 and fills count+word_out (the table's OWNED copy, valid
   until wf_destroy) if present; 0 if absent */
int wf_lookup(const WF *w, const char *word, size_t *count, const char **word_out);
size_t wf_distinct(const WF *w);
void wf_destroy(WF *w);                  /* frees every node AND every strdup'd key */
```

The table must own its keys (strdup on first sight) — that is the
ownership seam: values are plain counts, but keys are owned.""",
    C_PRELUDE + "\n#include <stddef.h>\n#define WF_BUCKETS 16\ntypedef struct WFNode {\n    const char   *word;\n    size_t        count;\n    struct WFNode *next;\n} WFNode;\ntypedef struct { WFNode *buckets[WF_BUCKETS]; size_t distinct; } WF;\nvoid wf_init(WF *w);\nint wf_count(WF *w, const char *word);\nint wf_lookup(const WF *w, const char *word, size_t *count, const char **word_out);\nsize_t wf_distinct(const WF *w);\nvoid wf_destroy(WF *w);\n",
    [
        (
            "count, lookup, destroy owned keys",
            r"""
WF w;
wf_init(&w);
const char *tokens[] = {"go", "rust", "go", "c", "go", "rust"};
for (int i = 0; i < 6; i++) CHECK_EQ(wf_count(&w, tokens[i]), 0);
CHECK_EQ(wf_distinct(&w), 3);
size_t n;
const char *owned;
CHECK_EQ(wf_lookup(&w, "go", &n, &owned), 1);
CHECK_EQ(n, 3);
CHECK(!strcmp(owned, "go"));
CHECK(owned != tokens[0]);                 /* the table's own copy */
CHECK_EQ(wf_lookup(&w, "perl", &n, &owned), 0);
CHECK_EQ(wf_lookup(&w, NULL, &n, &owned), -1);
CHECK_EQ(wf_count(&w, NULL), -1);
wf_destroy(&w);
CHECK_EQ(wf_distinct(&w), 0);
""",
            "wf_count: walk chain for strcmp match -> count++; else strdup + push. destroy: free node then key — free key BEFORE dropping the node pointer.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Bộ đếm tần suất từ",
        "Cài WF: bảng đếm từ sở hữu key (strdup); lookup trả bản sao của bảng; destroy free node + key.",
        [("đếm, lookup, destroy key sở hữu", "strcmp match -> count++; else strdup + đẩy đầu.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m8",
    "Checkpoint: The Ownership Seam",
    "Prove you can build a hash table that OWNS its keys and frees every byte exactly once.",
    26,
    r"""
## The task

Implement `WF` (see the challenge): a word-frequency table that strdups
its keys, counts occurrences, hands out lookups into its own storage,
and destroys everything it owns. This is the module's whole lesson in
one structure: hashing, chaining, *and* the ownership seam — the table
owns its keys, the tests verify the copies are distinct, and destroy
frees every node and every key exactly once.

Passing this proves you can ship a generic container whose ownership
policy is explicit and whose cleanup is provable — the bar every real
library must clear.

Next module: the preprocessor — macros as a language over the language.
""",
    "Kiểm tra: Đường ownership",
    "Chứng minh bạn dựng hash table SỞ HỮU key của mình và free từng byte đúng một lần.",
    r"""
## Bài toán

Cài `WF` (xem challenge): bảng tần suất từ strdup key, đếm lần xuất
hiện, trả lookup vào kho của chính nó, và hủy mọi thứ nó sở hữu. Đây là
toàn bộ bài học của module trong một cấu trúc: hashing, chaining,
*và* đường ownership — bảng sở hữu key, test kiểm chứng bản sao khác
bản gốc, destroy free mọi node và mọi key đúng một lần.

Vượt qua chứng minh bạn đóng gói được generic container với ownership
policy tường minh và cleanup chứng minh được — chuẩn mà mọi thư viện
thật phải vượt.

Module sau: preprocessor — macro như ngôn ngữ trên ngôn ngữ.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
static size_t fnv1a(const char *s) {
    size_t h = 2166136261u;
    for (const unsigned char *p = (const unsigned char *)s; *p; p++) {
        h ^= *p;
        h *= 16777619u;
    }
    return h;
}
void wf_init(WF *w) {
    if (!w) return;
    memset(w, 0, sizeof *w);
}
int wf_count(WF *w, const char *word) {
    if (!w || !word || !*word) return -1;
    size_t b = fnv1a(word) % WF_BUCKETS;
    for (WFNode *n = w->buckets[b]; n; n = n->next)
        if (strcmp(n->word, word) == 0) {
            n->count++;
            return 0;
        }
    WFNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->word = malloc(strlen(word) + 1);
    if (!n->word) {
        free(n);
        return -1;
    }
    strcpy((char *)n->word, word);
    n->count = 1;
    n->next = w->buckets[b];
    w->buckets[b] = n;
    w->distinct++;
    return 0;
}
int wf_lookup(const WF *w, const char *word, size_t *count, const char **word_out) {
    if (!w || !word || !count || !word_out) return -1;
    size_t b = fnv1a(word) % WF_BUCKETS;
    for (const WFNode *n = w->buckets[b]; n; n = n->next)
        if (strcmp(n->word, word) == 0) {
            *count = n->count;
            *word_out = n->word;
            return 1;
        }
    return 0;
}
size_t wf_distinct(const WF *w) { return w ? w->distinct : 0; }
void wf_destroy(WF *w) {
    if (!w) return;
    for (size_t b = 0; b < WF_BUCKETS; b++)
        while (w->buckets[b]) {
            WFNode *n = w->buckets[b];
            w->buckets[b] = n->next;
            free((char *)n->word);      /* key first — the node still names it */
            free(n);
        }
    w->distinct = 0;
}""",
    wrong=r"""
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
static size_t fnv1a(const char *s) {
    size_t h = 2166136261u;
    for (const unsigned char *p = (const unsigned char *)s; *p; p++) {
        h ^= *p;
        h *= 16777619u;
    }
    return h;
}
void wf_init(WF *w) {
    if (!w) return;
    memset(w, 0, sizeof *w);
}
int wf_count(WF *w, const char *word) {
    if (!w || !word) return -1;         /* wrong: empty word accepted */
    size_t b = fnv1a(word) % WF_BUCKETS;
    for (WFNode *n = w->buckets[b]; n; n = n->next)
        if (strcmp(n->word, word) == 0) {
            n->count++;
            return 0;
        }
    WFNode *n = malloc(sizeof *n);
    if (!n) return -1;
    n->word = word;                     /* wrong: stores the CALLER's pointer —
                                             the table does not own its key */
    n->count = 1;
    n->next = w->buckets[b];
    w->buckets[b] = n;
    w->distinct++;
    return 0;
}
int wf_lookup(const WF *w, const char *word, size_t *count, const char **word_out) {
    if (!w || !word || !count || !word_out) return -1;
    size_t b = fnv1a(word) % WF_BUCKETS;
    for (const WFNode *n = w->buckets[b]; n; n = n->next)
        if (strcmp(n->word, word) == 0) {
            *count = n->count;
            *word_out = n->word;
            return 1;
        }
    return 0;
}
size_t wf_distinct(const WF *w) { return w ? w->distinct : 0; }
void wf_destroy(WF *w) {
    if (!w) return;
    for (size_t b = 0; b < WF_BUCKETS; b++)
        while (w->buckets[b]) {
            WFNode *n = w->buckets[b];
            w->buckets[b] = n->next;
            free(n);                    /* wrong: key never freed (or double-freed
                                             if the caller frees it) */
        }
    w->distinct = 0;
}""",
)

print("module 8 complete")
