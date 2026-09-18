#!/usr/bin/env python3
"""C — Intermediate — Module 16: cint-capstone.

Capstone: MiniKV — a persistent key-value store that integrates the course:
owned key copies (M3/M6), a documented byte-level format with magic +
checksum (M12), error contracts (M13), and deterministic tests. Probed
capability: file I/O against /tmp is gradeable in the sandbox. House
conventions: ISO C only, self-contained tests, Ws are behavioral
near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-capstone"

write_module(
    M,
    "Capstone: MiniKV",
    "Build a persistent key-value store end to end — ownership, binary "
    "format, error contract, and tests — everything in this course, in one "
    "library.",
    "Capstone: MiniKV",
    "Xây một key-value store bền vững từ đầu đến cuối — ownership, định dạng "
    "nhị phân, hợp đồng lỗi, và test — mọi thứ trong khóa học, gọn trong một "
    "thư viện.",
    lessons=["capstone-arch", "capstone-format", "capstone-testing", "cint-checkpoint-m16"],
    practices=["cint-p16-core", "cint-p16-persist"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "capstone-arch",
    "The Shape of a Small Library",
    "MiniKV's architecture: a fixed-capacity table with owned key copies, "
    "an error contract on every call, and no hidden I/O. Libraries are "
    "designed, not accumulated.",
    16,
    r"""
## One library, every lesson

The capstone is a **key-value store**: `put`, `get`, `del`, iterate —
persisted to a file, loaded back. It is small on purpose. Every decision
in it is one you have already studied; the capstone forces them into
**one coherent design**.

### The API, and what each line commits you to

```c
#define KV_CAP      16
#define KV_KEYMAX   32

typedef enum {
    KV_OK = 0,       /* success                                   */
    KV_EARGS,        /* NULL handle/buffer — caller's bug         */
    KV_ENOMEM,       /* table full — a state outcome, not a bug   */
    KV_ENOENT,       /* key not present — normal, reportable      */
    KV_EFORMAT,      /* file: bad magic/version                   */
    KV_ETRUNC,       /* file: shorter than its own layout         */
    KV_EBADSUM,      /* file: checksum mismatch — corrupted       */
} KVError;

typedef struct { char key[KV_KEYMAX]; long value; int live; } KVSlot;
typedef struct { KVSlot slots[KV_CAP]; size_t count; } KVStore;

KVError kv_put(KVStore *s, const char *key, long value);
KVError kv_get(const KVStore *s, const char *key, long *out);
KVError kv_del(KVStore *s, const char *key);
```

Read that header like a contract, because it is one:

- **Errors are values, not side channels.** `KV_OK` is the only success.
  Distinguishing *caller bug* (`KV_EARGS`) from *state* (`KV_ENOMEM`,
  `KV_ENOENT`) is the M13 discipline: three different answers to three
  different questions the caller must ask.
- **`kv_get` takes `const KVStore *`.** Reading must not mutate — the
  type system enforces the promise so reviewers do not have to.
- **Keys are copied.** `kv_put` copies the caller's bytes into
  `slot.key`; the caller may free or reuse their buffer immediately.
  This is the ownership rule from M3, expressed in the type signature.

### Why fixed capacity (for now)

`KV_CAP 16` with first-free-slot placement is not laziness — it is a
**scoping decision**. Growth, resizing, and heap-backed tables are the
next course's problem. A fixed table lets the capstone spend its
complexity budget on persistence and error design, where the threads
converge. Real designs state what they *defer*; that is this lesson's
meta-lesson.

### Single-threaded, on purpose

Concurrency is deliberately **absent**. M15 showed that threads make
every invariant probabilistic; a graded capstone test that races is a
flaky test, and flaky tests teach the wrong lesson. The honest statement
belongs in the header comment: *not thread-safe; serialize access
externally*. Adding an `mtx_t` around each call is exactly the M15
exercise — architecture prose here, machinery there.
""",
    "Kiểu dáng của một thư viện nhỏ",
    "Kiến trúc MiniKV: bảng dung lượng cố định với bản sao key thuộc sở hữu "
    "store, hợp đồng lỗi trên mỗi lời gọi, và không I/O ẩn. Thư viện được "
    "thiết kế, không phải tích lũy.",
    r"""
## Một thư viện, mọi bài học

Capstone là một **key-value store**: `put`, `get`, `del`, duyệt — lưu ra
file và nạp lại. Nó nhỏ một cách cố ý: mọi quyết định đều là thứ bạn đã
học; capstone ép chúng thành **một thiết kế nhất quán**.

### API, và mỗi dòng cam kết điều gì

```c
typedef enum {
    KV_OK = 0,       /* thành công                          */
    KV_EARGS,        /* NULL/tham số sai — lỗi người gọi    */
    KV_ENOMEM,       /* bảng đầy — trạng thái, không phải bug */
    KV_ENOENT,       /* không có key — bình thường           */
    KV_EFORMAT,      /* file: magic/version sai              */
    KV_ETRUNC,       /* file: ngắn hơn bố cục tự khai        */
    KV_EBADSUM,      /* file: checksum lệch — hỏng dữ liệu   */
} KVError;
```

- **Lỗi là giá trị, không phải kênh phụ.** Phân biệt *lỗi người gọi*
  (`KV_EARGS`) với *trạng thái* (`KV_ENOMEM`, `KV_ENOENT`) là kỷ luật
  của M13.
- **`kv_get` nhận `const KVStore *`.** Đọc không được mutation — hệ
  thống kiểu giữ lời hứa thay cho người review.
- **Key được sao chép.** `kv_put` copy bytes của người gọi vào
  `slot.key`; đây là quy tắc ownership của M3.

### Vì sao dung lượng cố định

`KV_CAP 16` không phải lười — đó là **quyết định phạm vi**. Resize là
vấn đề của khóa sau; bảng cố định giữ ngân sách phức tạp cho
persistence và thiết kế lỗi.

### Đơn luồng, cố ý

Concurrency vắng mặt có chủ đích. M15 đã cho thấy thread biến mọi bất
biến thành xác suất; test capstone có race là test flaky. Lời khai
trung thực nằm ở comment header: *không thread-safe; đồng bộ bên
ngoài*.
""",
)

write_lesson(
    M, "capstone-format",
    "A File Format That Survives Reality",
    "MiniKV's on-disk layout: magic, version, count, fixed-width records, "
    "checksum — written byte by byte, not struct-dumped. Formats outlive "
    "code.",
    18,
    r"""
## The format is the contract that outlives you

Code gets recompiled; files do not. The on-disk layout must be defined
byte by byte, independent of struct padding, endianness habits, or
compiler whims.

### MiniKV's layout (fixed, documented)

```
offset  size  field
0       4     magic  = 'C','J','K','V'
4       1     version = 1
5       4     count  (u32 LE) — number of LIVE records (informational)
9       656   all KV_CAP = 16 slots, 41 bytes each:
                key:   32 bytes, NUL-padded
                value: 8 bytes, i64 little-endian
                live:  1 byte (1 = live, 0 = free or tombstone)
last    4     checksum (u32 LE): byte-sum of bytes 9..664
```

Total size = `9 + 41*16 + 4 = 669`, always. Writing every slot (not
just live ones) makes the file a **snapshot of the table** — a deleted
key round-trips as the tombstone it is, and the loader never has to
guess where records end. Every field is written with explicit byte
stores — `fputc`, shifts, `& 0xFF` — never `fwrite(&struct)`. M12's
lesson applied: the struct layout belongs to the compiler; the format
belongs to you.

### Tombstones are part of the state

A deleted key is not *nothing* — in this format it is a slot with
`live = 0`. Why keep it? Because save/load must round-trip the
**logical state**: "key k was absent" is information. Compaction
(dropping dead slots on save) is a legitimate alternative design; what
is *not* legitimate is being vague about which one you chose. This
course's format states it plainly: snapshot, all 16 slots.

### Checksum: cheap, honest, non-cryptographic

The checksum is a **byte sum mod 2^32** over the record region. It
detects accidental corruption — a truncated write, a flipped bit — and
nothing else. It is *not* a hash, not a signature, and defends against
nothing adversarial. Saying exactly what a mechanism does not do is
part of specifying what it does; an over-claimed checksum is a bug
waiting for an auditor to find.

```c
static unsigned long kv_sum(const unsigned char *p, size_t n) {
    unsigned long s = 0;
    for (size_t i = 0; i < n; i++) s = (s + p[i]) & 0xFFFFFFFFUL;
    return s;
}
```

### Loading is validation

`kv_load` never trusts the file: check magic, check version, read
exactly 656 record bytes and 4 checksum bytes (any short read →
`KV_ETRUNC`), verify the checksum **before** touching the table
(mismatch → `KV_EBADSUM`). Each failure maps to a distinct `KVError` —
the M13 taxonomy, applied to bytes. A loader that returns "success"
with a half-populated table is lying, and M13 taught you what lies
cost. One more contract detail: `kv_load` **resets** the destination
store first — load is "become the state in this file", not "merge".
""",
    "Định dạng file sống sót qua thực tế",
    "Bố cục trên đĩa của MiniKV: magic, version, count, record fixed-width, "
    "checksum — ghi từng byte, không phải dump struct. Định dạng sống lâu "
    "hơn code.",
    r"""
## Định dạng là hợp đồng sống lâu hơn bạn

Code được biên dịch lại; file thì không. Bố cục trên đĩa phải định nghĩa
từng byte, độc lập với padding struct và thói quen endianness.

### Bố cục của MiniKV (cố định, có tài liệu)

```
offset  size  field
0       4     magic  = 'C','J','K','V'
4       1     version = 1
5       4     count  (u32 LE) — số record LIVE (thông tin)
9       656   cả KV_CAP = 16 slot, mỗi slot 41 bytes:
                key:   32 bytes, đệm NUL
                value: 8 bytes, i64 little-endian
                live:  1 byte (1 = live, 0 = trống hoặc tombstone)
last    4     checksum (u32 LE): tổng byte của vùng 9..664
```

Tổng kích thước = `9 + 41*16 + 4 = 669`, luôn luôn. Ghi cả 16 slot biến
file thành **ảnh chụp của bảng** — key đã xóa round-trip đúng như
tombstone của nó. Mọi trường được ghi bằng byte tường minh — không bao
giờ `fwrite(&struct)`.

### Tombstone là một phần của trạng thái

Key đã xóa không phải *không có gì* — trong định dạng này nó là slot
với `live = 0`. Save/load phải round-trip **trạng thái logic**.
Compaction là một thiết kế thay thế hợp lệ; điều *không* hợp lệ là
không nói rõ mình chọn cái nào.

### Checksum: rẻ, trung thực, không phải mật mã

Checksum là **tổng byte mod 2^32** trên vùng record. Nó phát hiện hỏng
ngẫu nhiên và không phòng thủ gì trước kẻ thù có chủ đích. Nói rõ một
cơ chế *không* làm gì cũng là một phần của đặc tả.

### Load là validation

`kv_load` không bao giờ tin file: kiểm tra magic, version, đọc đúng 656
byte record và 4 byte checksum (đọc thiếu → `KV_ETRUNC`), xác minh
checksum **trước khi** đụng vào bảng (lệch → `KV_EBADSUM`). Mỗi thất
bại ánh xạ tới một `KVError` riêng. Một chi tiết hợp đồng nữa:
`kv_load` **reset** store đích trước — load là "trở thành trạng thái
trong file", không phải "hòa vào trạng thái hiện có".
""",
)

write_lesson(
    M, "capstone-testing",
    "Testing a Library Like an Enemy",
    "Round-trips, corruption injection, boundary fills, and ownership "
    "probes — the test suite that would have caught every W in this course.",
    17,
    r"""
## Test the contract, not the implementation

Every challenge in this course had a **wrong version that almost
worked**. Your test suite exists to make almost-working fail. The
capstone's suite targets the four places libraries actually break:

### 1. Round-trip: the state, not the buffer

```
put k1..k3 → del k2 → save → load into fresh store →
expect: k1, k3 present; k2 absent; count == 2
```

This catches the classic persistence lie: saving the raw struct array
and calling it "state".

### 2. Corruption injection: break one byte, expect one answer

Flip the **last** byte (checksum region) → `KV_EBADSUM`. Truncate the
file by one byte → `KV_ETRUNC`. Overwrite the magic → `KV_EFORMAT`.
Each malformed input gets its **own** verdict — a loader that says
"corrupt" for everything is as useless as one that says "fine".

### 3. Boundaries: capacity is a real state

Fill all 16 slots. The 17th `put` must return `KV_ENOMEM` — and the 16
stored entries must be **untouched**. Overflow that silently drops, or
worse corrupts, is the bug this catches.

### 4. Ownership probes: the caller's memory is theirs

```c
char key[8] = "temp";
kv_put(&s, key, 1);
memset(key, 'x', 4);                       /* clobber the caller's buffer */
CHECK_EQ(kv_get(&s, "temp", &v), KV_OK);   /* store kept its copy */
```

A store that borrowed the pointer instead of copying the bytes fails
this probe — deterministically, because you clobbered the buffer on
purpose. This is the test that made M3's borrow-vs-copy W honest.

### The meta-test: would your suite fail?

For each test, ask the only question that matters: *what wrong
implementation does this test kill?* If you cannot name it, the test is
decoration. Every hidden test in this course could answer that
question; now the answer is yours to write.
""",
    "Test một thư viện như kẻ thù",
    "Round-trip, tiêm nhiễm hỏng dữ liệu, lấp đầy biên, và thăm dò "
    "ownership — bộ test mà nếu có từ đầu đã bắt mọi W trong khóa này.",
    r"""
## Test hợp đồng, không phải bản cài đặt

Mỗi challenge trong khóa này từng có một **bản sai mà gần đúng**. Bộ
test tồn tại để làm *gần đúng* thất bại. Suite của capstone nhắm vào
bốn chỗ thư viện thật hay gãy:

### 1. Round-trip: trạng thái, không phải buffer

```
put k1..k3 → del k2 → save → load vào store mới →
kỳ vọng: k1, k3 có; k2 vắng; count == 2
```

Điều này bắt lời nói dối kinh điển: dump mảng struct rồi gọi nó là
"trạng thái".

### 2. Tiêm nhiễm: hỏng một byte, kỳ vọng một câu trả lời

Lật byte **cuối** (vùng checksum) → `KV_EBADSUM`. Cắt bớt một byte →
`KV_ETRUNC`. Ghi đè magic → `KV_EFORMAT`. Mỗi đầu vào lỗi có **một**
phán quyết riêng.

### 3. Biên: dung lượng là trạng thái thật

Lấp đủ 16 slot. `put` thứ 17 phải trả `KV_ENOMEM` — và 16 entry đã lưu
phải **nguyên vẹn**.

### 4. Thăm dò ownership: bộ nhớ người gọi là của họ

```c
char key[8] = "temp";
kv_put(&s, key, 1);
memset(key, 'x', 4);                       /* phá buffer của người gọi */
CHECK_EQ(kv_get(&s, "temp", &v), KV_OK);   /* store giữ bản sao */
```

Store mượn con trỏ thay vì copy bytes sẽ trượt probe này — tất định.

### Meta-test: suite của bạn có biết thất bại không?

Với mỗi test, hỏi câu duy nhất quan trọng: *bản cài đặt sai nào test
này giết?* Nếu không gọi tên được, test đó chỉ là trang trí.
""",
)

# ---------------------------------------------------------------- practices

KV_CORE_BOILERPLATE = (
    C_PRELUDE
    + """#include <stddef.h>
#define KV_CAP 16
#define KV_KEYMAX 32
typedef enum {
    KV_OK = 0, KV_EARGS, KV_ENOMEM, KV_ENOENT,
    KV_EFORMAT, KV_ETRUNC, KV_EBADSUM
} KVError;
typedef struct { char key[KV_KEYMAX]; long value; int live; } KVSlot;
typedef struct { KVSlot slots[KV_CAP]; size_t count; } KVStore;
void kv_init(KVStore *s);
KVError kv_put(KVStore *s, const char *key, long value);
KVError kv_get(const KVStore *s, const char *key, long *out);
KVError kv_del(KVStore *s, const char *key);
size_t kv_count(const KVStore *s);
void kv_iter(const KVStore *s, void (*fn)(const char *key, long value, void *ctx), void *ctx);
/* ---- capture state for iteration tests (defined here) ---- */
static char kv_cap_keys[16][KV_KEYMAX];
static long kv_cap_vals[16];
static int kv_cap_n;
static void kv_capture(const char *key, long value, void *ctx) {
    (void)ctx;
    if (kv_cap_n < 16) {
        snprintf(kv_cap_keys[kv_cap_n], KV_KEYMAX, "%s", key);
        kv_cap_vals[kv_cap_n] = value;
        kv_cap_n++;
    }
}
static void kv_capture_reset(void) { kv_cap_n = 0; }
"""
)

write_practice(
    M, "cint-p16-core",
    "The Table Core",
    "put/get/del with owned keys, replace semantics, capacity as a state, "
    "and iteration you can reason about.",
    "Lõi bảng",
    "put/get/del với key thuộc sở hữu store, ngữ nghĩa replace, dung lượng "
    "là trạng thái, và thứ tự duyệt có thể lý luận được.",
    after_lesson="capstone-arch",
    minutes=30,
    difficulty="advanced",
    challenges=[
        challenge(
            "cint-p16-kvcore",
            "Put, Get, Del, Replace",
            "Implement the core table ops. Keys are copied into the store; "
            "putting an existing key replaces its value (no duplicates); del "
            "makes the slot reusable; a full table returns KV_ENOMEM and "
            "changes nothing.",
            KV_CORE_BOILERPLATE,
            [
                (
                    "core contract",
                    """
KVStore s; kv_init(&s);
long v;
CHECK_EQ(kv_get(&s, "a", &v), KV_ENOENT);          /* empty: absent */
CHECK_EQ(kv_put(&s, "a", 1), KV_OK);
CHECK_EQ(kv_put(&s, "b", 2), KV_OK);
CHECK_EQ(kv_get(&s, "a", &v), KV_OK); CHECK_EQ(v, 1);
CHECK_EQ(kv_put(&s, "a", 10), KV_OK);              /* replace */
CHECK_EQ(kv_get(&s, "a", &v), KV_OK); CHECK_EQ(v, 10);
CHECK_EQ(kv_count(&s), 2);                         /* no duplicate */
CHECK_EQ(kv_del(&s, "a"), KV_OK);
CHECK_EQ(kv_get(&s, "a", &v), KV_ENOENT);
CHECK_EQ(kv_count(&s), 1);
CHECK_EQ(kv_put(&s, "a", 11), KV_OK);              /* slot reused */
CHECK_EQ(kv_get(&s, "a", &v), KV_OK); CHECK_EQ(v, 11);
CHECK_EQ(kv_del(&s, "ghost"), KV_ENOENT);          /* deleting nothing */
CHECK_EQ(kv_put(NULL, "x", 1), KV_EARGS);
CHECK_EQ(kv_get(&s, NULL, &v), KV_EARGS);
""",
                    "Does replace insert or update? Does del free a slot for reuse?",
                ),
                (
                    "capacity is a state",
                    """
KVStore s; kv_init(&s);
char key[KV_KEYMAX];
for (int i = 0; i < 16; i++) {
    snprintf(key, sizeof key, "k%02d", i);
    CHECK_EQ(kv_put(&s, key, i), KV_OK);
}
CHECK_EQ(kv_count(&s), 16);
CHECK_EQ(kv_put(&s, "overflow", 99), KV_ENOMEM);   /* full: state, not args */
CHECK_EQ(kv_count(&s), 16);                        /* nothing changed */
long v;
CHECK_EQ(kv_get(&s, "k00", &v), KV_OK); CHECK_EQ(v, 0);   /* untouched */
CHECK_EQ(kv_put(&s, "k00", 100), KV_OK);           /* replace still fine */
CHECK_EQ(kv_get(&s, "k00", &v), KV_OK); CHECK_EQ(v, 100);
CHECK_EQ(kv_del(&s, "k07"), KV_OK);
CHECK_EQ(kv_put(&s, "overflow", 99), KV_OK);       /* freed slot reused */
""",
                    "ENOMEM must leave the table exactly as it was.",
                ),
            ],
            "advanced",
        ),
        challenge(
            "cint-p16-iter",
            "Deterministic Iteration",
            "Implement kv_count and kv_iter: visit live slots in slot order, "
            "skipping tombstones and empty slots. A deleted key must never "
            "be observed again, and count must agree with iteration on "
            "every state.",
            KV_CORE_BOILERPLATE,
            [
                (
                    "live slots in order",
                    """
KVStore s; kv_init(&s);
CHECK_EQ(kv_put(&s, "alpha", 1), KV_OK);
CHECK_EQ(kv_put(&s, "beta", 2), KV_OK);
CHECK_EQ(kv_put(&s, "gamma", 3), KV_OK);
CHECK_EQ(kv_del(&s, "beta"), KV_OK);
kv_capture_reset();
kv_iter(&s, kv_capture, NULL);
CHECK_EQ(kv_cap_n, 2);                             /* tombstone invisible */
CHECK_STR_EQ(kv_cap_keys[0], "alpha");             /* slot order */
CHECK_STR_EQ(kv_cap_keys[1], "gamma");
CHECK_EQ(kv_cap_vals[1], 3);
""",
                    "Tombstoned slots must be skipped, not reported.",
                ),
                (
                    "count agrees with iteration",
                    """
KVStore s; kv_init(&s);
for (int i = 0; i < 5; i++) {
    char k[8]; snprintf(k, sizeof k, "k%d", i);
    CHECK_EQ(kv_put(&s, k, i), KV_OK);
}
CHECK_EQ(kv_del(&s, "k2"), KV_OK);
CHECK_EQ(kv_del(&s, "k0"), KV_OK);
CHECK_EQ(kv_count(&s), 3);
kv_capture_reset();
kv_iter(&s, kv_capture, NULL);
CHECK_EQ(kv_cap_n, 3);
CHECK_EQ(kv_put(&s, "k9", 9), KV_OK);
CHECK_EQ(kv_count(&s), 4);
kv_capture_reset();
kv_iter(&s, kv_capture, NULL);
CHECK_EQ(kv_cap_n, 4);
""",
                    "kv_count and kv_iter must agree on every state.",
                ),
            ],
            "advanced",
        ),
        challenge(
            "cint-p16-own",
            "The Store Owns Its Keys",
            "Prove the ownership rule: kv_put must copy the caller's bytes. "
            "The store's observable behavior must not change when the "
            "caller's buffer is modified or reused after the put.",
            KV_CORE_BOILERPLATE,
            [
                (
                    "caller may clobber",
                    """
KVStore s; kv_init(&s);
long v;
char key[16];
snprintf(key, sizeof key, "temp");
CHECK_EQ(kv_put(&s, key, 42), KV_OK);
memset(key, 'x', 4);                               /* clobber the buffer */
CHECK_EQ(kv_get(&s, "temp", &v), KV_OK);           /* store kept its copy */
CHECK_EQ(v, 42);
snprintf(key, sizeof key, "other");
CHECK_EQ(kv_put(&s, key, 7), KV_OK);               /* reuse the buffer */
CHECK_EQ(kv_get(&s, "temp", &v), KV_OK);           /* first key intact */
CHECK_EQ(v, 42);
CHECK_EQ(kv_get(&s, "other", &v), KV_OK); CHECK_EQ(v, 7);
""",
                    "After put, the caller's buffer is theirs to reuse.",
                ),
                (
                    "distinct keys stay distinct",
                    """
KVStore s; kv_init(&s);
long v;
CHECK_EQ(kv_put(&s, "prefix-a", 1), KV_OK);
CHECK_EQ(kv_put(&s, "prefix-b", 2), KV_OK);
CHECK_EQ(kv_get(&s, "prefix-a", &v), KV_OK); CHECK_EQ(v, 1);
CHECK_EQ(kv_get(&s, "prefix-b", &v), KV_OK); CHECK_EQ(v, 2);
CHECK_EQ(kv_del(&s, "prefix-a"), KV_OK);
CHECK_EQ(kv_get(&s, "prefix-b", &v), KV_OK);       /* sibling untouched */
CHECK_EQ(v, 2);
CHECK_EQ(kv_get(&s, "prefix-a", &v), KV_ENOENT);
""",
                    "Distinct keys must never share storage.",
                ),
            ],
            "advanced",
        ),
    ],
    vi_challenges={
        "cint-p16-kvcore": vi_challenge(
            "Put, Get, Del, Replace",
            "Cài các thao tác lõi. Key được sao chép vào store; put key đã có "
            "thì thay giá trị (không nhân đôi); del làm slot tái sử dụng "
            "được; bảng đầy trả KV_ENOMEM và không đổi gì.",
            [
                ("hợp đồng lõi", "Replace là chèn hay cập nhật? Del có nhả slot không?"),
                ("dung lượng là trạng thái", "ENOMEM phải để nguyên bảng y như trước."),
            ],
        ),
        "cint-p16-iter": vi_challenge(
            "Duyệt tất định",
            "Cài kv_count và kv_iter: duyệt các slot live theo thứ tự slot, "
            "bỏ qua tombstone và slot trống. Key đã xóa không bao giờ được "
            "quan sát lại, và count phải khớp với duyệt trong mọi trạng thái.",
            [
                ("slot live theo thứ tự", "Slot tombstone phải bị bỏ qua, không được báo."),
                ("count khớp với duyệt", "kv_count và kv_iter phải khớp trong mọi trạng thái."),
            ],
        ),
        "cint-p16-own": vi_challenge(
            "Store sở hữu key của nó",
            "Chứng minh quy tắc ownership: kv_put phải sao chép bytes của "
            "người gọi. Hành vi quan sát được của store không đổi khi "
            "buffer của người gọi bị sửa hoặc tái sử dụng sau put.",
            [
                ("người gọi được quyền phá buffer", "Sau put, buffer của caller là của họ."),
                ("các key khác nhau phải tách biệt", "Hai key khác nhau không bao giờ dùng chung bộ nhớ."),
            ],
        ),
    },
    solutions=[
        (
            "cint-p16-kvcore",
            r"""
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
}
static size_t kv_find(const KVStore *s, const char *key) {
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0)
            return i;
    return KV_CAP;
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    size_t at = kv_find(s, key);
    if (at < KV_CAP) { s->slots[at].value = value; return KV_OK; }
    for (size_t i = 0; i < KV_CAP; i++) {
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);        /* own the bytes */
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value;
            s->slots[i].live = 1;
            s->count++;
            return KV_OK;
        }
    }
    return KV_ENOMEM;                                     /* state unchanged */
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    size_t at = kv_find(s, key);
    if (at == KV_CAP) return KV_ENOENT;
    *out = s->slots[at].value;
    return KV_OK;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    size_t at = kv_find(s, key);
    if (at == KV_CAP) return KV_ENOENT;
    s->slots[at].live = 0;
    s->count--;
    return KV_OK;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    size_t n = 0;
    for (size_t i = 0; i < KV_CAP; i++) if (s->slots[i].live) n++;
    return n;
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(s->slots[i].key, s->slots[i].value, ctx);
}
""",
            r"""
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
}
static size_t kv_find(const KVStore *s, const char *key) {
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0)
            return i;
    return KV_CAP;
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    if (kv_find(s, key) < KV_CAP) return KV_OK;   /* wrong: replace is a no-op —
                                                     the old value silently wins */
    for (size_t i = 0; i < KV_CAP; i++) {
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value;
            s->slots[i].live = 1;
            s->count++;
            return KV_OK;
        }
    }
    return KV_ENOMEM;
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    size_t at = kv_find(s, key);
    if (at == KV_CAP) return KV_ENOENT;
    *out = s->slots[at].value;
    return KV_OK;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    size_t at = kv_find(s, key);
    if (at == KV_CAP) return KV_ENOENT;
    s->slots[at].live = 0;
    s->count--;
    return KV_OK;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    size_t n = 0;
    for (size_t i = 0; i < KV_CAP; i++) if (s->slots[i].live) n++;
    return n;
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(s->slots[i].key, s->slots[i].value, ctx);
}
""",
        ),
        (
            "cint-p16-iter",
            r"""
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            s->slots[i].value = value; return KV_OK;
        }
    for (size_t i = 0; i < KV_CAP; i++)
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value; s->slots[i].live = 1; s->count++;
            return KV_OK;
        }
    return KV_ENOMEM;
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            *out = s->slots[i].value; return KV_OK;
        }
    return KV_ENOENT;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            s->slots[i].live = 0; s->count--; return KV_OK;
        }
    return KV_ENOENT;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    size_t n = 0;
    for (size_t i = 0; i < KV_CAP; i++) if (s->slots[i].live) n++;
    return n;
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(s->slots[i].key, s->slots[i].value, ctx);
}
""",
            r"""
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            s->slots[i].value = value; return KV_OK;
        }
    for (size_t i = 0; i < KV_CAP; i++)
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value; s->slots[i].live = 1; s->count++;
            return KV_OK;
        }
    return KV_ENOMEM;
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            *out = s->slots[i].value; return KV_OK;
        }
    return KV_ENOENT;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            s->slots[i].live = 0; return KV_OK;   /* wrong: count not decremented —
                                                     count and iteration drift apart */
        }
    return KV_ENOENT;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    return s->count;   /* wrong: stale counter after deletes */
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(s->slots[i].key, s->slots[i].value, ctx);
}
""",
        ),
        (
            "cint-p16-own",
            r"""
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            s->slots[i].value = value; return KV_OK;
        }
    for (size_t i = 0; i < KV_CAP; i++) {
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);        /* own the bytes */
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value; s->slots[i].live = 1; s->count++;
            return KV_OK;
        }
    }
    return KV_ENOMEM;
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            *out = s->slots[i].value; return KV_OK;
        }
    return KV_ENOENT;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0) {
            s->slots[i].live = 0; s->count--; return KV_OK;
        }
    return KV_ENOENT;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    size_t n = 0;
    for (size_t i = 0; i < KV_CAP; i++) if (s->slots[i].live) n++;
    return n;
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(s->slots[i].key, s->slots[i].value, ctx);
}
""",
            r"""
/* wrong: ONE shared key buffer. Every put overwrites it; lookups match
   against it instead of each slot's own copy — the "borrow, don't copy"
   disease in its most compact form. */
static char kv_shared_key[KV_KEYMAX];
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
    kv_shared_key[0] = '\0';
}
static int kv_match_shared(const char *key) {
    return strncmp(kv_shared_key, key, KV_KEYMAX) == 0;
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    if (kv_match_shared(key)) {                 /* "replace" hits every slot */
        for (size_t i = 0; i < KV_CAP; i++)
            if (s->slots[i].live) s->slots[i].value = value;
        return KV_OK;
    }
    for (size_t i = 0; i < KV_CAP; i++) {
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value; s->slots[i].live = 1; s->count++;
            strncpy(kv_shared_key, key, KV_KEYMAX - 1);   /* the aliasing defect */
            return KV_OK;
        }
    }
    return KV_ENOMEM;
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    if (kv_match_shared(key))
        for (size_t i = 0; i < KV_CAP; i++)
            if (s->slots[i].live) { *out = s->slots[i].value; return KV_OK; }
    return KV_ENOENT;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    if (kv_match_shared(key))
        for (size_t i = 0; i < KV_CAP; i++)
            if (s->slots[i].live) { s->slots[i].live = 0; s->count--; return KV_OK; }
    return KV_ENOENT;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    size_t n = 0;
    for (size_t i = 0; i < KV_CAP; i++) if (s->slots[i].live) n++;
    return n;
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(kv_shared_key, s->slots[i].value, ctx);
}
""",
        ),
    ],
)

# ------------------------------------------------------------ persistence

# Practice boilerplate: the core is PROVIDED (reference implementation,
# defined here) — the graded work is save/load only. No collision with the
# learner's save/load, which is all their solution defines.
KV_IO_BOILERPLATE = (
    KV_CORE_BOILERPLATE
    + """KVError kv_save(const KVStore *s, const char *path);
KVError kv_load(KVStore *s, const char *path);
/* ---- provided reference core (not graded here) ---- */
static size_t kv_find_ref(const KVStore *s, const char *key) {
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0)
            return i;
    return KV_CAP;
}
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    size_t at = kv_find_ref(s, key);
    if (at < KV_CAP) { s->slots[at].value = value; return KV_OK; }
    for (size_t i = 0; i < KV_CAP; i++) {
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value;
            s->slots[i].live = 1;
            s->count++;
            return KV_OK;
        }
    }
    return KV_ENOMEM;
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    size_t at = kv_find_ref(s, key);
    if (at == KV_CAP) return KV_ENOENT;
    *out = s->slots[at].value;
    return KV_OK;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    size_t at = kv_find_ref(s, key);
    if (at == KV_CAP) return KV_ENOENT;
    s->slots[at].live = 0;
    s->count--;
    return KV_OK;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    size_t n = 0;
    for (size_t i = 0; i < KV_CAP; i++) if (s->slots[i].live) n++;
    return n;
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(s->slots[i].key, s->slots[i].value, ctx);
}
"""
)

# Checkpoint boilerplate: core + save/load are DECLARED only — the learner's
# solution implements everything, so no definitions may precede it.
KV_CP_BOILERPLATE = (
    KV_CORE_BOILERPLATE
    + """KVError kv_save(const KVStore *s, const char *path);
KVError kv_load(KVStore *s, const char *path);
"""
)

write_practice(
    M, "cint-p16-persist",
    "Persistence & the Hostile File",
    "The byte-exact format: save a snapshot, load it back, and survive a "
    "file that lies — wrong magic, truncated, corrupted checksum.",
    "Persistence & tệp thù địch",
    "Định dạng đúng từng byte: lưu ảnh chụp, nạp lại, và sống sót trước "
    "một file nói dối — magic sai, bị cắt cụt, checksum hỏng.",
    after_lesson="capstone-format",
    minutes=34,
    difficulty="advanced",
    challenges=[
        challenge(
            "cint-p16-save",
            "Byte-Exact Save",
            "Implement kv_save: write the documented layout with explicit "
            "byte stores — magic, version, count (LE), all 16 slots (key "
            "NUL-padded, value i64 LE, live byte), then the checksum. The "
            "file must be exactly 669 bytes for KV_CAP 16.",
            KV_IO_BOILERPLATE,
            [
                (
                    "layout bytes",
                    """
KVStore s; kv_init(&s);
CHECK_EQ(kv_put(&s, "alpha", 1), KV_OK);
CHECK_EQ(kv_put(&s, "beta", 2), KV_OK);
CHECK_EQ(kv_save(&s, "/tmp/cj-kv-save-a.bin"), KV_OK);
FILE *f = fopen("/tmp/cj-kv-save-a.bin", "rb");
CHECK_NOT_NULL(f);
unsigned char hdr[9];
CHECK_EQ(fread(hdr, 1, 9, f), 9u);
CHECK_EQ(hdr[0], 'C'); CHECK_EQ(hdr[1], 'J'); CHECK_EQ(hdr[2], 'K'); CHECK_EQ(hdr[3], 'V');
CHECK_EQ(hdr[4], 1);                                  /* version */
CHECK_EQ(hdr[5], 2); CHECK_EQ(hdr[6], 0); CHECK_EQ(hdr[7], 0); CHECK_EQ(hdr[8], 0);
fseek(f, 0, SEEK_END);
long sz = ftell(f);
CHECK_EQ(sz, 669);                                    /* 9 + 41*16 + 4 */
/* alpha's record: key at 9, value at 41 (9+32), live at 49 */
unsigned char rec[41];
fseek(f, 9, SEEK_SET);
CHECK_EQ(fread(rec, 1, 41, f), 41u);
CHECK_STR_EQ((const char *)rec, "alpha");
long v = 0;
for (int i = 7; i >= 0; i--) v = (v << 8) | rec[32 + i];
CHECK_EQ(v, 1);
CHECK_EQ(rec[40], 1);                                 /* live */
fclose(f);
""",
                    "Every field is explicit bytes — shifts and 0xFF masks, never fwrite(&struct).",
                ),
                (
                    "snapshot includes tombstones",
                    """
KVStore s; kv_init(&s);
CHECK_EQ(kv_put(&s, "gone", 5), KV_OK);
CHECK_EQ(kv_put(&s, "stays", 6), KV_OK);
CHECK_EQ(kv_del(&s, "gone"), KV_OK);
CHECK_EQ(kv_save(&s, "/tmp/cj-kv-save-b.bin"), KV_OK);
FILE *f = fopen("/tmp/cj-kv-save-b.bin", "rb");
CHECK_NOT_NULL(f);
fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
CHECK_EQ(sz, 669);
/* gone was put first: its slot is slot 0 (dead), stays is slot 1 (live) */
unsigned char rec[41];
CHECK_EQ(fread(rec, 1, 41, f), 41u);
CHECK_EQ(rec[40], 0);                                 /* tombstone persisted */
fseek(f, 41 + 9, SEEK_SET);
CHECK_EQ(fread(rec, 1, 41, f), 41u);
CHECK_EQ(rec[40], 1);
fclose(f);
""",
                    "Deleted keys round-trip as tombstones — snapshot of the table.",
                ),
            ],
            "advanced",
        ),
        challenge(
            "cint-p16-load",
            "The Hostile File",
            "Implement kv_load with full validation: magic, version, exact "
            "length (short read → KV_ETRUNC), checksum before touching the "
            "table (mismatch → KV_EBADSUM). Load must RESET the destination "
            "store first.",
            KV_IO_BOILERPLATE,
            [
                (
                    "round-trip state",
                    """
KVStore a; kv_init(&a);
CHECK_EQ(kv_put(&a, "x", 10), KV_OK);
CHECK_EQ(kv_put(&a, "y", 20), KV_OK);
CHECK_EQ(kv_del(&a, "x"), KV_OK);
CHECK_EQ(kv_save(&a, "/tmp/cj-kv-rt.bin"), KV_OK);
KVStore b; kv_init(&b);
CHECK_EQ(kv_put(&b, "preexisting", 99), KV_OK);   /* must be wiped */
CHECK_EQ(kv_load(&b, "/tmp/cj-kv-rt.bin"), KV_OK);
long v;
CHECK_EQ(kv_get(&b, "x", &v), KV_ENOENT);         /* tombstone restored */
CHECK_EQ(kv_get(&b, "y", &v), KV_OK); CHECK_EQ(v, 20);
CHECK_EQ(kv_get(&b, "preexisting", &v), KV_ENOENT);  /* reset, not merge */
CHECK_EQ(kv_count(&b), 1);
""",
                    "Load is 'become the state in this file', not 'merge'.",
                ),
                (
                    "each corruption has its own verdict",
                    """
/* build a known-good file */
KVStore a; kv_init(&a);
CHECK_EQ(kv_put(&a, "k", 1), KV_OK);
CHECK_EQ(kv_save(&a, "/tmp/cj-kv-evil.bin"), KV_OK);
long v;
/* flip the LAST byte (checksum region) → EBADSUM */
{
    FILE *f = fopen("/tmp/cj-kv-evil.bin", "r+b");
    CHECK_NOT_NULL(f);
    fseek(f, -1, SEEK_END);
    int c = fgetc(f);
    fseek(f, -1, SEEK_END);      /* fgetc advanced to EOF: write REPLACES */
    fputc(c ^ 0xFF, f);
    fclose(f);
    KVStore b; kv_init(&b);
    CHECK_EQ(kv_load(&b, "/tmp/cj-kv-evil.bin"), KV_EBADSUM);
    CHECK_EQ(kv_count(&b), 0);                     /* table untouched */
}
/* truncate by one byte → ETRUNC */
{
    FILE *f = fopen("/tmp/cj-kv-evil.bin", "rb");
    CHECK_NOT_NULL(f);
    static unsigned char buf[700];
    size_t n = fread(buf, 1, sizeof buf, f);
    fclose(f);
    f = fopen("/tmp/cj-kv-evil2.bin", "wb");
    CHECK_NOT_NULL(f);
    fwrite(buf, 1, n - 1, f);
    fclose(f);
    KVStore b; kv_init(&b);
    CHECK_EQ(kv_load(&b, "/tmp/cj-kv-evil2.bin"), KV_ETRUNC);
}
/* overwrite the magic → EFORMAT */
{
    FILE *f = fopen("/tmp/cj-kv-evil.bin", "r+b");
    CHECK_NOT_NULL(f);
    fseek(f, 0, SEEK_SET);
    fputc('X', f);
    fclose(f);
    KVStore b; kv_init(&b);
    CHECK_EQ(kv_load(&b, "/tmp/cj-kv-evil.bin"), KV_EFORMAT);
}
CHECK_EQ(kv_load(NULL, "/tmp/cj-kv-evil.bin"), KV_EARGS);
CHECK_EQ(kv_load(&a, NULL), KV_EARGS);
""",
                    "A loader that says 'corrupt' for everything is as useless as one that says 'fine'.",
                ),
            ],
            "advanced",
        ),
    ],
    vi_challenges={
        "cint-p16-save": vi_challenge(
            "Lưu đúng từng byte",
            "Cài kv_save: ghi bố cục theo tài liệu bằng byte tường minh — "
            "magic, version, count (LE), cả 16 slot, rồi checksum. File phải "
            "đúng 669 byte khi KV_CAP 16.",
            [
                ("byte bố cục", "Mỗi trường là byte tường minh — shift và mask 0xFF."),
                ("ảnh chụp có tombstone", "Key đã xóa round-trip như tombstone."),
            ],
        ),
        "cint-p16-load": vi_challenge(
            "Tệp thù địch",
            "Cài kv_load với validation đầy đủ: magic, version, độ dài chính "
            "xác (đọc thiếu → KV_ETRUNC), checksum trước khi đụng bảng "
            "(lệch → KV_EBADSUM). Load phải RESET store đích trước.",
            [
                ("round-trip trạng thái", "Load là 'trở thành trạng thái trong file', không phải 'hòa vào'."),
                ("mỗi hỏng một phán quyết", "Magic sai, cắt cụt, checksum lệch — ba câu trả lời khác nhau."),
            ],
        ),
    },
    solutions=[
        (
            "cint-p16-save",
            r"""
KVError kv_save(const KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "wb");
    if (!f) return KV_EARGS;
    unsigned long sum = 0;
    static const unsigned char magic[4] = {'C', 'J', 'K', 'V'};
    fwrite(magic, 1, 4, f);
    fputc(1, f);                                          /* version */
    unsigned long cnt = (unsigned long)s->count;
    for (int i = 0; i < 4; i++) fputc((int)((cnt >> (8 * i)) & 0xFF), f);
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41] = {0};
        strncpy((char *)rec, s->slots[i].key, KV_KEYMAX - 1);
        long v = s->slots[i].value;
        for (int b = 0; b < 8; b++) rec[32 + b] = (unsigned char)((v >> (8 * b)) & 0xFF);
        rec[40] = s->slots[i].live ? 1 : 0;
        fwrite(rec, 1, 41, f);
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    for (int i = 0; i < 4; i++) fputc((int)((sum >> (8 * i)) & 0xFF), f);
    fclose(f);
    return KV_OK;
}
KVError kv_load(KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "rb");
    if (!f) return KV_EARGS;
    unsigned char magic[4];
    if (fread(magic, 1, 4, f) != 4 || memcmp(magic, "CJKV", 4) != 0) { fclose(f); return KV_EFORMAT; }
    if (fgetc(f) != 1) { fclose(f); return KV_EFORMAT; }
    for (int i = 0; i < 4; i++) fgetc(f);                /* count: informational */
    KVStore fresh;
    memset(&fresh, 0, sizeof fresh);
    unsigned long sum = 0;
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41];
        if (fread(rec, 1, 41, f) != 41) { fclose(f); return KV_ETRUNC; }
        memcpy(fresh.slots[i].key, rec, KV_KEYMAX);
        fresh.slots[i].key[KV_KEYMAX - 1] = '\0';
        long v = 0;
        for (int b = 7; b >= 0; b--) v = (v << 8) | rec[32 + b];
        fresh.slots[i].value = v;
        fresh.slots[i].live = rec[40] ? 1 : 0;
        if (fresh.slots[i].live) fresh.count++;
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    unsigned long stored = 0;
    for (int b = 0; b < 4; b++) {
        int c = fgetc(f);
        if (c == EOF) { fclose(f); return KV_ETRUNC; }
        stored |= (unsigned long)c << (8 * b);          /* little-endian, as saved */
    }
    fclose(f);
    if (stored != sum) return KV_EBADSUM;
    *s = fresh;
    return KV_OK;
}
""",
            r"""
KVError kv_save(const KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "wb");
    if (!f) return KV_EARGS;
    unsigned long sum = 0;
    static const unsigned char magic[4] = {'C', 'J', 'K', 'V'};
    fwrite(magic, 1, 4, f);
    fputc(1, f);
    unsigned long cnt = (unsigned long)s->count;
    for (int i = 0; i < 4; i++) fputc((int)((cnt >> (8 * i)) & 0xFF), f);
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41] = {0};
        strncpy((char *)rec, s->slots[i].key, KV_KEYMAX - 1);
        long v = s->slots[i].value;
        for (int b = 0; b < 8; b++) rec[32 + b] = (unsigned char)((v >> (8 * b)) & 0xFF);
        rec[40] = s->slots[i].live ? 1 : 0;
        if (rec[40]) {                                    /* wrong: only live slots written —
                                                             the file is shorter than the
                                                             format, and slot positions
                                                             stop being meaningful */
            fwrite(rec, 1, 41, f);
            for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
        }
    }
    for (int i = 0; i < 4; i++) fputc((int)((sum >> (8 * i)) & 0xFF), f);
    fclose(f);
    return KV_OK;
}
KVError kv_load(KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "rb");
    if (!f) return KV_EARGS;
    unsigned char magic[4];
    if (fread(magic, 1, 4, f) != 4 || memcmp(magic, "CJKV", 4) != 0) { fclose(f); return KV_EFORMAT; }
    if (fgetc(f) != 1) { fclose(f); return KV_EFORMAT; }
    for (int i = 0; i < 4; i++) fgetc(f);                /* count: informational */
    KVStore fresh;
    memset(&fresh, 0, sizeof fresh);
    unsigned long sum = 0;
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41];
        if (fread(rec, 1, 41, f) != 41) { fclose(f); return KV_ETRUNC; }
        memcpy(fresh.slots[i].key, rec, KV_KEYMAX);
        fresh.slots[i].key[KV_KEYMAX - 1] = '\0';
        long v = 0;
        for (int b = 7; b >= 0; b--) v = (v << 8) | rec[32 + b];
        fresh.slots[i].value = v;
        fresh.slots[i].live = rec[40] ? 1 : 0;
        if (fresh.slots[i].live) fresh.count++;
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    unsigned long stored = 0;
    for (int b = 0; b < 4; b++) {
        int c = fgetc(f);
        if (c == EOF) { fclose(f); return KV_ETRUNC; }
        stored |= (unsigned long)c << (8 * b);          /* little-endian, as saved */
    }
    fclose(f);
    if (stored != sum) return KV_EBADSUM;
    *s = fresh;
    return KV_OK;
}
""",
        ),
        (
            "cint-p16-load",
            r"""
KVError kv_save(const KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "wb");
    if (!f) return KV_EARGS;
    unsigned long sum = 0;
    static const unsigned char magic[4] = {'C', 'J', 'K', 'V'};
    fwrite(magic, 1, 4, f);
    fputc(1, f);
    unsigned long cnt = (unsigned long)s->count;
    for (int i = 0; i < 4; i++) fputc((int)((cnt >> (8 * i)) & 0xFF), f);
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41] = {0};
        strncpy((char *)rec, s->slots[i].key, KV_KEYMAX - 1);
        long v = s->slots[i].value;
        for (int b = 0; b < 8; b++) rec[32 + b] = (unsigned char)((v >> (8 * b)) & 0xFF);
        rec[40] = s->slots[i].live ? 1 : 0;
        fwrite(rec, 1, 41, f);
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    for (int i = 0; i < 4; i++) fputc((int)((sum >> (8 * i)) & 0xFF), f);
    fclose(f);
    return KV_OK;
}
KVError kv_load(KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "rb");
    if (!f) return KV_EARGS;
    unsigned char magic[4];
    if (fread(magic, 1, 4, f) != 4 || memcmp(magic, "CJKV", 4) != 0) { fclose(f); return KV_EFORMAT; }
    if (fgetc(f) != 1) { fclose(f); return KV_EFORMAT; }
    for (int i = 0; i < 4; i++) fgetc(f);                /* count: informational */
    KVStore fresh;
    memset(&fresh, 0, sizeof fresh);
    unsigned long sum = 0;
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41];
        if (fread(rec, 1, 41, f) != 41) { fclose(f); return KV_ETRUNC; }
        memcpy(fresh.slots[i].key, rec, KV_KEYMAX);
        fresh.slots[i].key[KV_KEYMAX - 1] = '\0';
        long v = 0;
        for (int b = 7; b >= 0; b--) v = (v << 8) | rec[32 + b];
        fresh.slots[i].value = v;
        fresh.slots[i].live = rec[40] ? 1 : 0;
        if (fresh.slots[i].live) fresh.count++;
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    unsigned long stored = 0;
    for (int b = 0; b < 4; b++) {
        int c = fgetc(f);
        if (c == EOF) { fclose(f); return KV_ETRUNC; }
        stored |= (unsigned long)c << (8 * b);          /* little-endian, as saved */
    }
    fclose(f);
    if (stored != sum) return KV_EBADSUM;
    *s = fresh;
    return KV_OK;
}
""",
            r"""
KVError kv_save(const KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "wb");
    if (!f) return KV_EARGS;
    unsigned long sum = 0;
    static const unsigned char magic[4] = {'C', 'J', 'K', 'V'};
    fwrite(magic, 1, 4, f);
    fputc(1, f);
    unsigned long cnt = (unsigned long)s->count;
    for (int i = 0; i < 4; i++) fputc((int)((cnt >> (8 * i)) & 0xFF), f);
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41] = {0};
        strncpy((char *)rec, s->slots[i].key, KV_KEYMAX - 1);
        long v = s->slots[i].value;
        for (int b = 0; b < 8; b++) rec[32 + b] = (unsigned char)((v >> (8 * b)) & 0xFF);
        rec[40] = s->slots[i].live ? 1 : 0;
        fwrite(rec, 1, 41, f);
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    for (int i = 0; i < 4; i++) fputc((int)((sum >> (8 * i)) & 0xFF), f);
    fclose(f);
    return KV_OK;
}
KVError kv_load(KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "rb");
    if (!f) return KV_EARGS;
    unsigned char magic[4];
    if (fread(magic, 1, 4, f) != 4 || memcmp(magic, "CJKV", 4) != 0) { fclose(f); return KV_EFORMAT; }
    if (fgetc(f) != 1) { fclose(f); return KV_EFORMAT; }
    for (int i = 0; i < 4; i++) fgetc(f);                /* count: informational */
    KVStore fresh;
    memset(&fresh, 0, sizeof fresh);
    for (size_t i = 0; i < KV_CAP; i++) {           /* wrong: NO checksum check —
                                                       any byte-sum collision or
                                                       silent corruption loads as
                                                       if it were state */
        unsigned char rec[41];
        if (fread(rec, 1, 41, f) != 41) { fclose(f); return KV_ETRUNC; }
        memcpy(fresh.slots[i].key, rec, KV_KEYMAX);
        fresh.slots[i].key[KV_KEYMAX - 1] = '\0';
        long v = 0;
        for (int b = 7; b >= 0; b--) v = (v << 8) | rec[32 + b];
        fresh.slots[i].value = v;
        fresh.slots[i].live = rec[40] ? 1 : 0;
        if (fresh.slots[i].live) fresh.count++;
    }
    *s = fresh;
    return KV_OK;
}
""",
        ),
    ],
)

# ------------------------------------------------------------ checkpoint

write_checkpoint(
    M, "cint-checkpoint-m16",
    "Checkpoint: The Store That Survives",
    "Prove the integration: ownership, byte-exact persistence, error "
    "taxonomy, and round-trip state — all at once, under tests that try to "
    "make almost-right fail.",
    32,
    r"""
## The task

Implement the full MiniKV core + persistence (see the challenge). The
graded surface is integration: a store that owns its keys, a format
that is byte-exact, a loader that validates before trusting, and an
error taxonomy that distinguishes caller bugs from states from hostile
files.

Passing this proves you can ship a small library — the actual skill
this course exists to teach. Every W-shaped bug in this course is one
the hidden tests were designed to catch; your own implementation must
survive them without ever having seen them.
""",
    "Checkpoint: Cửa hàng sống sót",
    "Chứng minh sự tích hợp: ownership, persistence đúng từng byte, hệ "
    "phân loại lỗi, và round-trip trạng thái — tất cả cùng lúc, dưới các "
    "test cố làm *gần đúng* thất bại.",
    r"""
## Bài toán

Cài đầy đủ lõi MiniKV + persistence (xem challenge). Bề mặt chấm điểm
là tích hợp: store sở hữu key, định dạng đúng từng byte, loader
validation trước khi tin, và hệ phân loại lỗi phân biệt lỗi người gọi
khỏi trạng thái khỏi tệp thù địch.

Đỗ checkpoint này chứng minh bạn có thể ship một thư viện nhỏ — kỹ năng
thật mà khóa học tồn tại để dạy.
""",
    challenge(
        "cint-checkpoint-m16-task",
        "MiniKV, Integrated",
        "Implement kv_init/put/get/del/count/iter, kv_save, and kv_load per "
        "the documented format (669-byte snapshot, checksummed) and the "
        "error contract. Ownership, replace semantics, capacity, and "
        "validation are all graded.",
        KV_CP_BOILERPLATE,
        [
            (
                "core + ownership",
                """
KVStore s; kv_init(&s);
long v;
char key[16];
snprintf(key, sizeof key, "temp");
CHECK_EQ(kv_put(&s, key, 42), KV_OK);
memset(key, 'x', 4);
CHECK_EQ(kv_get(&s, "temp", &v), KV_OK); CHECK_EQ(v, 42);   /* owned */
CHECK_EQ(kv_put(&s, "temp", 43), KV_OK);                    /* replace */
CHECK_EQ(kv_get(&s, "temp", &v), KV_OK); CHECK_EQ(v, 43);
CHECK_EQ(kv_count(&s), 1);
char full[KV_KEYMAX];
for (int i = 0; i < 15; i++) {
    snprintf(full, sizeof full, "f%02d", i);
    CHECK_EQ(kv_put(&s, full, i), KV_OK);
}
CHECK_EQ(kv_put(&s, "overflow", 1), KV_ENOMEM);             /* state */
CHECK_EQ(kv_count(&s), 16);
""",
                    "Owned keys, replace, capacity as a state — one pass, no partial credit.",
                ),
            (
                "persistence + hostile files",
                """
KVStore s; kv_init(&s);
CHECK_EQ(kv_put(&s, "alpha", 1), KV_OK);
CHECK_EQ(kv_del(&s, "alpha"), KV_OK);                       /* tombstone */
CHECK_EQ(kv_put(&s, "beta", 2), KV_OK);
CHECK_EQ(kv_save(&s, "/tmp/cj-kv-ck.bin"), KV_OK);
FILE *f = fopen("/tmp/cj-kv-ck.bin", "rb");
CHECK_NOT_NULL(f);
fseek(f, 0, SEEK_END);
long sz = ftell(f);
fclose(f);
CHECK_EQ(sz, 669);                                          /* full snapshot */
KVStore b; kv_init(&b);
CHECK_EQ(kv_load(&b, "/tmp/cj-kv-ck.bin"), KV_OK);
long v;
CHECK_EQ(kv_get(&b, "alpha", &v), KV_ENOENT);               /* dead stays dead */
CHECK_EQ(kv_get(&b, "beta", &v), KV_OK); CHECK_EQ(v, 2);
/* hostile: flip checksum byte */
f = fopen("/tmp/cj-kv-ck.bin", "r+b");
CHECK_NOT_NULL(f);
fseek(f, -1, SEEK_END);
int c = fgetc(f);
fseek(f, -1, SEEK_END);      /* fgetc advanced to EOF: write REPLACES */
fputc(c ^ 0x01, f);
fclose(f);
KVStore c2; kv_init(&c2);
CHECK_EQ(kv_load(&c2, "/tmp/cj-kv-ck.bin"), KV_EBADSUM);
CHECK_EQ(kv_count(&c2), 0);                                 /* untouched on failure */
""",
                    "Snapshot length, tombstone round-trip, checksum verdict, atomic failure.",
                ),
        ],
        "advanced",
    ),
    vi_challenge(
        "MiniKV, tích hợp",
        "Cài kv_init/put/get/del/count/iter, kv_save và kv_load theo định "
        "dạng đã tài liệu hóa (ảnh chụp 669 byte, có checksum) và hợp đồng "
        "lỗi. Ownership, ngữ nghĩa replace, dung lượng và validation đều "
        "được chấm.",
        [
            ("lõi + ownership", "Owned key, replace, dung lượng là trạng thái — một lượt, không có điểm từng phần."),
            ("persistence + tệp thù địch", "Độ dài ảnh chụp, round-trip tombstone, phán quyết checksum, thất bại nguyên tử."),
        ],
    ),
    solution=r"""
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
}
static size_t kv_find(const KVStore *s, const char *key) {
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && strncmp(s->slots[i].key, key, KV_KEYMAX) == 0)
            return i;
    return KV_CAP;
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    size_t at = kv_find(s, key);
    if (at < KV_CAP) { s->slots[at].value = value; return KV_OK; }
    for (size_t i = 0; i < KV_CAP; i++) {
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value;
            s->slots[i].live = 1;
            s->count++;
            return KV_OK;
        }
    }
    return KV_ENOMEM;
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    size_t at = kv_find(s, key);
    if (at == KV_CAP) return KV_ENOENT;
    *out = s->slots[at].value;
    return KV_OK;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    size_t at = kv_find(s, key);
    if (at == KV_CAP) return KV_ENOENT;
    s->slots[at].live = 0;
    s->count--;
    return KV_OK;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    size_t n = 0;
    for (size_t i = 0; i < KV_CAP; i++) if (s->slots[i].live) n++;
    return n;
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(s->slots[i].key, s->slots[i].value, ctx);
}
KVError kv_save(const KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "wb");
    if (!f) return KV_EARGS;
    unsigned long sum = 0;
    static const unsigned char magic[4] = {'C', 'J', 'K', 'V'};
    fwrite(magic, 1, 4, f);
    fputc(1, f);
    unsigned long cnt = (unsigned long)s->count;
    for (int i = 0; i < 4; i++) fputc((int)((cnt >> (8 * i)) & 0xFF), f);
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41] = {0};
        strncpy((char *)rec, s->slots[i].key, KV_KEYMAX - 1);
        long v = s->slots[i].value;
        for (int b = 0; b < 8; b++) rec[32 + b] = (unsigned char)((v >> (8 * b)) & 0xFF);
        rec[40] = s->slots[i].live ? 1 : 0;
        fwrite(rec, 1, 41, f);
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    for (int i = 0; i < 4; i++) fputc((int)((sum >> (8 * i)) & 0xFF), f);
    fclose(f);
    return KV_OK;
}
KVError kv_load(KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "rb");
    if (!f) return KV_EARGS;
    unsigned char magic[4];
    if (fread(magic, 1, 4, f) != 4 || memcmp(magic, "CJKV", 4) != 0) { fclose(f); return KV_EFORMAT; }
    if (fgetc(f) != 1) { fclose(f); return KV_EFORMAT; }
    for (int i = 0; i < 4; i++) fgetc(f);                /* count: informational */
    KVStore fresh;
    memset(&fresh, 0, sizeof fresh);
    unsigned long sum = 0;
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41];
        if (fread(rec, 1, 41, f) != 41) { fclose(f); return KV_ETRUNC; }
        memcpy(fresh.slots[i].key, rec, KV_KEYMAX);
        fresh.slots[i].key[KV_KEYMAX - 1] = '\0';
        long v = 0;
        for (int b = 7; b >= 0; b--) v = (v << 8) | rec[32 + b];
        fresh.slots[i].value = v;
        fresh.slots[i].live = rec[40] ? 1 : 0;
        if (fresh.slots[i].live) fresh.count++;
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    unsigned long stored = 0;
    for (int b = 0; b < 4; b++) {
        int c = fgetc(f);
        if (c == EOF) { fclose(f); return KV_ETRUNC; }
        stored |= (unsigned long)c << (8 * b);          /* little-endian, as saved */
    }
    fclose(f);
    if (stored != sum) return KV_EBADSUM;
    *s = fresh;
    return KV_OK;
}
""",
    wrong=r"""
/* wrong: kv_get searches ALL slots, including dead ones — after a
   delete+re-put cycle it can resurrect a stale value; and kv_load
   skips checksum verification entirely. */
void kv_init(KVStore *s) {
    if (!s) return;
    memset(s, 0, sizeof *s);
}
static int kv_key_eq(const char *a, const char *b) {
    return strncmp(a, b, KV_KEYMAX) == 0;
}
KVError kv_put(KVStore *s, const char *key, long value) {
    if (!s || !key) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && kv_key_eq(s->slots[i].key, key)) {
            s->slots[i].value = value; return KV_OK;
        }
    for (size_t i = 0; i < KV_CAP; i++)
        if (!s->slots[i].live) {
            memset(s->slots[i].key, 0, KV_KEYMAX);
            strncpy(s->slots[i].key, key, KV_KEYMAX - 1);
            s->slots[i].value = value; s->slots[i].live = 1; s->count++;
            return KV_OK;
        }
    return KV_ENOMEM;
}
KVError kv_get(const KVStore *s, const char *key, long *out) {
    if (!s || !key || !out) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (kv_key_eq(s->slots[i].key, key)) {   /* wrong: ignores .live */
            *out = s->slots[i].value; return KV_OK;
        }
    return KV_ENOENT;
}
KVError kv_del(KVStore *s, const char *key) {
    if (!s || !key) return KV_EARGS;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live && kv_key_eq(s->slots[i].key, key)) {
            s->slots[i].live = 0; s->count--; return KV_OK;
        }
    return KV_ENOENT;
}
size_t kv_count(const KVStore *s) {
    if (!s) return 0;
    size_t n = 0;
    for (size_t i = 0; i < KV_CAP; i++) if (s->slots[i].live) n++;
    return n;
}
void kv_iter(const KVStore *s, void (*fn)(const char *, long, void *), void *ctx) {
    if (!s || !fn) return;
    for (size_t i = 0; i < KV_CAP; i++)
        if (s->slots[i].live) fn(s->slots[i].key, s->slots[i].value, ctx);
}
KVError kv_save(const KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "wb");
    if (!f) return KV_EARGS;
    unsigned long sum = 0;
    static const unsigned char magic[4] = {'C', 'J', 'K', 'V'};
    fwrite(magic, 1, 4, f);
    fputc(1, f);
    unsigned long cnt = (unsigned long)s->count;
    for (int i = 0; i < 4; i++) fputc((int)((cnt >> (8 * i)) & 0xFF), f);
    for (size_t i = 0; i < KV_CAP; i++) {
        unsigned char rec[41] = {0};
        strncpy((char *)rec, s->slots[i].key, KV_KEYMAX - 1);
        long v = s->slots[i].value;
        for (int b = 0; b < 8; b++) rec[32 + b] = (unsigned char)((v >> (8 * b)) & 0xFF);
        rec[40] = s->slots[i].live ? 1 : 0;
        fwrite(rec, 1, 41, f);
        for (int b = 0; b < 41; b++) sum = (sum + rec[b]) & 0xFFFFFFFFUL;
    }
    for (int i = 0; i < 4; i++) fputc((int)((sum >> (8 * i)) & 0xFF), f);
    fclose(f);
    return KV_OK;
}
KVError kv_load(KVStore *s, const char *path) {
    if (!s || !path) return KV_EARGS;
    FILE *f = fopen(path, "rb");
    if (!f) return KV_EARGS;
    unsigned char magic[4];
    if (fread(magic, 1, 4, f) != 4 || memcmp(magic, "CJKV", 4) != 0) { fclose(f); return KV_EFORMAT; }
    if (fgetc(f) != 1) { fclose(f); return KV_EFORMAT; }
    for (int i = 0; i < 4; i++) fgetc(f);                /* count: informational */
    KVStore fresh;
    memset(&fresh, 0, sizeof fresh);
    for (size_t i = 0; i < KV_CAP; i++) {           /* wrong: no checksum */
        unsigned char rec[41];
        if (fread(rec, 1, 41, f) != 41) { fclose(f); return KV_ETRUNC; }
        memcpy(fresh.slots[i].key, rec, KV_KEYMAX);
        fresh.slots[i].key[KV_KEYMAX - 1] = '\0';
        long v = 0;
        for (int b = 7; b >= 0; b--) v = (v << 8) | rec[32 + b];
        fresh.slots[i].value = v;
        fresh.slots[i].live = rec[40] ? 1 : 0;
        if (fresh.slots[i].live) fresh.count++;
    }
    *s = fresh;
    return KV_OK;
}
""",
)

print("module 16 complete")
