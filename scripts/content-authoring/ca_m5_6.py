#!/usr/bin/env python3
"""C Advanced — batch 3: modules 5 (memory-allocators) and 6 (memory-ownership).
Zero-backslash authoring: @NL@ = statement separator, @CE@ = newline escape
inside C string literals."""
from ca import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# =================== MODULE 5: ca-memory-allocators =========================
M5 = "ca-memory-allocators"

L5A = "ca-allocator-anatomy"
L5B = "ca-arena-pool-patterns"
L5CP = "ca-checkpoint-m5"

write_module(
    M5,
    "Memory Allocators from First Principles",
    "Build the allocators production systems actually use — arenas, pools, growth policies — and learn the tradeoffs each one makes.",
    "Bộ cấp phát bộ nhớ từ nguyên lý",
    "Dựng những bộ cấp phát mà hệ thống thật dùng — arena, pool, chính sách tăng trưởng — và hiểu tradeoff của từng loại.",
    [L5A, L5B, L5CP],
    ["ca-p5-allocators"],
)

write_lesson(
    M5,
    L5A,
    "What malloc Actually Does",
    "The anatomy of an allocator: metadata, bins, coalescing, and why the interface is so small.",
    16,
    """
## The interface is three functions; the job is enormous

`malloc`, `free`, `realloc` hide a subsystem that must satisfy conflicting goals at once:

- **throughput** — allocate fast (the common case should be a few instructions);
- **memory efficiency** — metadata and fragmentation must not eat the heap;
- **low fragmentation** — long-running programs mix sizes unpredictably;
- **thread safety** — modern allocators do this without a global lock.

Real allocators (glibc's, musl's, jemalloc) chunk memory into size classes, keep free lists per class, coalesce neighbors on free, and mmap very large requests directly.

## The tradeoff triangle

Fast + compact + general: pick two. Arena allocators choose fast + compact for *one lifetime batch* and give up general free. Pools choose fast for *one size* and give up flexibility. Understanding *why* each design gives something up is the engineering content of this module — code alone does not teach it.

## Alignment is part of the contract

Every allocation is aligned for any fundamental type (typically 16 bytes). Your own allocators must honor that, or every struct cast through the result is a latent crash.
""",
    "malloc thực sự làm gì",
    "Giải phẫu bộ cấp phát: metadata, bins, coalescing, và vì sao giao diện lại nhỏ đến vậy.",
    """
## Giao diện chỉ ba hàm; công việc khổng lồ

`malloc`, `free`, `realloc` che một hệ thống con phải đạt các mục tiêu mâu thuẫn cùng lúc:

- **thông lượng** — cấp phát nhanh (trường hợp thường chỉ vài lệnh);
- **hiệu quả bộ nhớ** — metadata và phân mảnh không được ăn hết heap;
- **phân mảnh thấp** — chương trình dài hạn trộn kích thước khó đoán;
- **an toàn luồng** — allocator hiện đại làm điều đó không cần khóa toàn cục.

Các allocator thật (glibc, musl, jemalloc) chia heap thành size class, giữ free list theo class, ghép láng giềng khi free, và mmap trực tiếp các yêu cầu rất lớn.

## Tam giác tradeoff

Nhanh + gọn + tổng quát: chọn hai. Arena chọn nhanh + gọn cho *một lô cùng vòng đời* và từ bỏ free riêng lẻ. Pool chọn nhanh cho *một kích thước* và từ bỏ sự linh hoạt. Hiểu *vì sao* mỗi thiết kế từ bỏ thứ gì đó mới là nội dung kỹ thuật của mô-đun này.

## Alignment là một phần hợp đồng

Mọi cấp phát được căn cho mọi kiểu cơ bản (thường 16 byte). Allocator tự viết phải tôn trọng điều đó, nếu không mọi struct cast qua kết quả là một crash tiềm ẩn.
""",
)

write_lesson(
    M5,
    L5B,
    "Arenas and Pools",
    "Region allocation and fixed-size pools — the two workhorse patterns behind compilers, game engines, and network servers.",
    15,
    """
## Arena (region) allocation

Allocate a big block; hand out consecutive slices; free them *all at once* by discarding the block. An arena is a bump pointer plus a capacity:

```c
void *arena_alloc(arena_t *a, size_t n) {
    if (a->used + n > a->cap) return NULL;
    void *p = a->mem + a->used;
    a->used += n;
    return p;
}
```

No per-object free, no fragmentation, near-zero overhead per allocation. The discipline: every object in the arena must share one lifetime. Compilers arena per-function IR; servers arena per-request.

## Pool allocation

Same block size everywhere: keep a free list of slots. get() pops a slot; put() pushes it back. O(1) with zero searching, and no size-class machinery at all.

## realloc growth policies

Growing a buffer by doubling gives amortized O(1) per element; growing by +1 gives O(n^2) total copies. The policy lives in *your* code — `realloc` just moves bytes when told.

```c
size_t newcap = cap ? cap * 2 : 1;
```
""",
    "Arena và Pool",
    "Cấp phát theo vùng và pool kích thước cố định — hai mẫu lực lượng chính sau trình biên dịch, game engine, và network server.",
    """
## Cấp phát arena (vùng)

Cấp phát một khối lớn; cắt phát liên tiếp; giải phóng *toàn bộ cùng lúc* bằng cách bỏ khối. Arena là một bump pointer cộng dung lượng:

```c
void *arena_alloc(arena_t *a, size_t n) {
    if (a->used + n > a->cap) return NULL;
    void *p = a->mem + a->used;
    a->used += n;
    return p;
}
```

Không free từng đối tượng, không phân mảnh, overhead gần bằng 0. Kỷ luật: mọi đối tượng trong arena phải chung một vòng đời. Trình biên dịch arena theo hàm; server arena theo request.

## Cấp phát pool

Cùng một kích thước khối ở mọi nơi: giữ free list các slot. get() lấy một slot; put() trả lại. O(1) không cần tìm kiếm, không cần máy móc size class.

## Chính sách tăng trưởng realloc

Tăng gấp đôi cho chi phí khấu trừ O(1) mỗi phần tử; tăng +1 cho tổng O(n^2) lần copy. Chính sách nằm trong *code của bạn* — realloc chỉ chuyển byte khi được bảo.
""",
)

write_practice(
    M5,
    "ca-p5-allocators",
    "Allocator Engineering Drills",
    "Build arenas, pools, and growth policies — each with capacity semantics a test can pin down.",
    "Bài tập kỹ thuật allocator",
    "Dựng arena, pool, và chính sách tăng trưởng — mỗi cái với ngữ nghĩa năng lực mà test có thể ghim chặt.",
    L5A,
    24,
    "advanced",
    [
        challenge(
            "ca5-arena",
            "Build a Bump Arena",
            "Implement a bump allocator over caller-provided memory:@CE@ @CE@```c@CE@typedef struct { unsigned char *mem; size_t cap; size_t used; } arena_t;@CE@void arena_init(arena_t *a, unsigned char *buf, size_t cap);@CE@void *arena_alloc(arena_t *a, size_t n);@CE@void arena_reset(arena_t *a);@CE@```@CE@ @CE@`arena_alloc` returns NULL when the request does not fit the remaining capacity; `arena_reset` rewinds `used` to 0.",
            C_PRELUDE,
            [
                ("sequential slices", "unsigned char buf[64];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@unsigned char *p1 = arena_alloc(&a, 16);@NL@unsigned char *p2 = arena_alloc(&a, 40);@NL@CHECK_EQ((int)(p1 - buf), 0);@NL@CHECK_EQ((int)(p2 - buf), 16);", "Slices hand out consecutively from the front of the buffer."),
                ("exhaustion is NULL", "unsigned char buf[64];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@arena_alloc(&a, 56);@NL@CHECK_NULL(arena_alloc(&a, 16));", "56 of 64 bytes used; 16 more do not fit — return NULL, never overrun."),
                ("reset rewinds", "unsigned char buf[64];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@arena_alloc(&a, 32);@NL@arena_reset(&a);@NL@CHECK_NOT_NULL(arena_alloc(&a, 64));", "After reset the full capacity is available again in one slice."),
            ],
            level="guided",
        ),
        challenge(
            "ca5-pool",
            "Build a Fixed-Size Pool",
            "Implement an opaque fixed-block pool:@CE@ @CE@```c@CE@typedef struct pool pool_t;@CE@pool_t *pool_create(size_t blocks, size_t block_size);@CE@void *pool_get(pool_t *p);@CE@void pool_put(pool_t *p, void *blk);@CE@```@CE@ @CE@`pool_get` returns a block or NULL when exhausted; `pool_put` returns a block to the free list; a just-returned block must be handed out again first (LIFO).",
            C_PRELUDE,
            [
                ("exhaustion", "pool_t *p = pool_create(2, 16);@NL@void *b1 = pool_get(p);@NL@void *b2 = pool_get(p);@NL@CHECK_NOT_NULL(b1);@NL@CHECK_NOT_NULL(b2);@NL@CHECK_NULL(pool_get(p));", "Two blocks exist; the third get must report exhaustion."),
                ("LIFO reuse", "pool_t *p = pool_create(2, 16);@NL@void *b1 = pool_get(p);@NL@pool_put(p, b1);@NL@void *b3 = pool_get(p);@NL@CHECK_EQ((int)(b3 == b1), 1);", "A returned block goes to the head of the free list and is handed out first."),
            ],
            level="independent",
        ),
        challenge(
            "ca5-vec-push",
            "Doubling Growth Policy",
            "Implement a growable vector with an explicit growth contract:@CE@ @CE@```c@CE@int vec_push(int **buf, size_t *len, size_t *cap, int v);@CE@```@CE@ @CE@Starts at capacity 1; when full, the capacity *doubles*; returns 0 on success, -1 if allocation fails (leave everything unchanged then).",
            C_PRELUDE,
            [
                ("five pushes, cap 8", "int *buf = NULL;@NL@size_t len = 0, cap = 0;@NL@for (int i = 1; i <= 5; i++) vec_push(&buf, &len, &cap, i);@NL@CHECK_EQ((long long)cap, 8);@NL@CHECK_EQ((long long)len, 5);@NL@CHECK_EQ(buf[0], 1);@NL@CHECK_EQ(buf[4], 5);", "1 doubles to 2, 4, 8; the fifth push triggers the 4-to-8 growth; values survive every move."),
                ("first push allocates", "int *b = NULL;@NL@size_t l = 0, c = 0;@NL@CHECK_EQ(vec_push(&b, &l, &c, 9), 0);@NL@CHECK_EQ((long long)c, 1);@NL@CHECK_EQ(b[0], 9);", "The NULL/zero start must allocate capacity 1, not 0."),
            ],
            level="independent",
        ),
        challenge(
            "ca5-align-up",
            "Alignment Helper",
            "Implement `unsigned char *align_up(unsigned char *p, size_t align)` returning the smallest address >= p that is a multiple of align (align is a power of two). This is the helper every arena needs before handing out typed slices.",
            C_PRELUDE,
            [
                ("rounds up", "unsigned char raw[64];@NL@unsigned char *p = align_up(raw + 3, 8);@NL@CHECK_EQ((int)(p - raw), 8);", "Offset 3 rounds to the next multiple of 8."),
                ("already aligned", "unsigned char raw2[64];@NL@unsigned char *q = align_up(raw2 + 16, 8);@NL@CHECK_EQ((int)(q - raw2), 16);", "A multiple stays put — no gratuitous bump."),
                ("align 1 identity", "unsigned char raw3[64];@NL@unsigned char *r = align_up(raw3 + 7, 1);@NL@CHECK_EQ((int)(r - raw3), 7);", "align 1 is the identity."),
            ],
            level="independent",
        ),
    ],
    {
        "ca5-arena": vi_challenge(
            "Dựng arena bump",
            "Cài arena trên bộ nhớ do caller cấp: arena_init/arena_alloc/arena_reset — hết chỗ trả NULL, reset đưa used về 0.",
            [
                ("cắt phát liên tiếp", "Các slice phát tuần tự từ đầu buffer."),
                ("hết chỗ là NULL", "Đã dùng 56/64 byte; 16 nữa không vừa — trả NULL, không bao giờ tràn."),
                ("reset quay về", "Sau reset toàn bộ dung lượng có lại trong một slice."),
            ],
        ),
        "ca5-pool": vi_challenge(
            "Dựng pool khối cố định",
            "Cài pool opaque: pool_create/pool_get/pool_put — hết thì NULL, put trả slot về đầu free list (LIFO).",
            [
                ("hết slot", "Hai khối tồn tại; lần get thứ ba phải báo hết."),
                ("tái dùng LIFO", "Khối vừa trả về đầu free list và được phát đầu tiên."),
            ],
        ),
        "ca5-vec-push": vi_challenge(
            "Chính sách tăng gấp đôi",
            "Cài vec_push: bắt đầu cap 1, đầy thì tăng gấp đôi, lỗi cấp phát trả -1 không đổi gì.",
            [
                ("năm push, cap 8", "1 tăng thành 2, 4, 8; push thứ năm kích hoạt tăng 4-to-8; giá trị sống sót qua mọi lần chuyển."),
                ("push đầu tiên", "Khởi điểm NULL/0 phải cấp cap 1, không phải 0."),
            ],
        ),
        "ca5-align-up": vi_challenge(
            "Hàm căn địa chỉ",
            "Cài align_up trả địa chỉ nhỏ nhất >= p chia hết cho align (align là lũy thừa 2).",
            [
                ("làm tròn lên", "Offset 3 làm tròn thành bội kế của 8."),
                ("đã căn giữ nguyên", "Bội số đứng yên — không nhảy thừa."),
                ("align 1 là đồng nhất", "align 1 trả nguyên p."),
            ],
        ),
    },
    solutions=[
        (
            "ca5-arena",
            C_PRELUDE
            + "typedef struct { unsigned char *mem; size_t cap; size_t used; } arena_t;@NL@"
            + "void arena_init(arena_t *a, unsigned char *buf, size_t cap) { a->mem = buf; a->cap = cap; a->used = 0; }@NL@"
            + "void *arena_alloc(arena_t *a, size_t n) {@NL@    if (n > a->cap - a->used) return NULL;@NL@    void *p = a->mem + a->used;@NL@    a->used += n;@NL@    return p;@NL@}@NL@"
            + "void arena_reset(arena_t *a) { a->used = 0; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "typedef struct { unsigned char *mem; size_t cap; size_t used; } arena_t;@NL@"
            + "void arena_init(arena_t *a, unsigned char *buf, size_t cap) { a->mem = buf; a->cap = cap; a->used = 0; }@NL@"
            + "void *arena_alloc(arena_t *a, size_t n) {@NL@    if (n > a->cap) return NULL;@NL@    void *p = a->mem + a->used;@NL@    a->used += n;@NL@    return p;@NL@}@NL@"
            + "void arena_reset(arena_t *a) { a->used = 0; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca5-pool",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "typedef struct pool { unsigned char *mem; void **free; size_t nblocks; size_t bsize; size_t nfree; } pool_t;@NL@"
            + "pool_t *pool_create(size_t blocks, size_t block_size) {@NL@    pool_t *p = malloc(sizeof *p);@NL@    if (!p) return NULL;@NL@    p->mem = malloc(blocks * block_size);@NL@    p->free = malloc(blocks * sizeof(void *));@NL@    if (!p->mem || !p->free) { free(p->mem); free(p->free); free(p); return NULL; }@NL@    p->nblocks = blocks;@NL@    p->bsize = block_size;@NL@    p->nfree = blocks;@NL@    for (size_t i = 0; i < blocks; i++) p->free[i] = p->mem + i * block_size;@NL@    return p;@NL@}@NL@"
            + "void *pool_get(pool_t *p) {@NL@    if (p->nfree == 0) return NULL;@NL@    return p->free[--p->nfree];@NL@}@NL@"
            + "void pool_put(pool_t *p, void *blk) {@NL@    if (blk) p->free[p->nfree++] = blk;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "typedef struct pool { unsigned char *mem; void **free; size_t nblocks; size_t bsize; size_t nfree; } pool_t;@NL@"
            + "pool_t *pool_create(size_t blocks, size_t block_size) {@NL@    pool_t *p = malloc(sizeof *p);@NL@    p->mem = malloc(blocks * block_size);@NL@    p->free = malloc(blocks * sizeof(void *));@NL@    p->nblocks = blocks;@NL@    p->bsize = block_size;@NL@    p->nfree = blocks;@NL@    for (size_t i = 0; i < blocks; i++) p->free[i] = p->mem + i * block_size;@NL@    return p;@NL@}@NL@"
            + "void *pool_get(pool_t *p) {@NL@    if (p->nfree == 0) return NULL;@NL@    return p->free[--p->nfree];@NL@}@NL@"
            + "void pool_put(pool_t *p, void *blk) { (void)p; (void)blk; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca5-vec-push",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "int vec_push(int **buf, size_t *len, size_t *cap, int v) {@NL@    if (*len == *cap) {@NL@        size_t nc = *cap ? *cap * 2 : 1;@NL@        int *nb = realloc(*buf, nc * sizeof(int));@NL@        if (!nb) return -1;@NL@        *buf = nb;@NL@        *cap = nc;@NL@    }@NL@    (*buf)[(*len)++] = v;@NL@    return 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "int vec_push(int **buf, size_t *len, size_t *cap, int v) {@NL@    if (*len == *cap) {@NL@        size_t nc = *cap + 1;@NL@        int *nb = realloc(*buf, nc * sizeof(int));@NL@        if (!nb) return -1;@NL@        *buf = nb;@NL@        *cap = nc;@NL@    }@NL@    (*buf)[(*len)++] = v;@NL@    return 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca5-align-up",
            C_PRELUDE
            + "#include <stdint.h>@NL@""unsigned char *align_up(unsigned char *p, size_t align) {@NL@    uintptr_t u = (uintptr_t)p;@NL@    uintptr_t m = align - 1;@NL@    return (unsigned char *)((u + m) & ~m);@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#include <stdint.h>@NL@""unsigned char *align_up(unsigned char *p, size_t align) {@NL@    uintptr_t u = (uintptr_t)p;@NL@    return (unsigned char *)(u + align);@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M5,
    L5CP,
    "Checkpoint: An Arena with Alignment",
    "Consolidated allocator checkpoint.",
    12,
    """
Checkpoint for module 5: extend the arena with aligned allocation and usage statistics — the shape real arenas ship.
""",
    "Kiểm tra: Arena có căn chỉnh",
    "Kiểm tra tổng hợp allocator.",
    """
Kiểm tra mô-đun 5: mở rộng arena với cấp phát có căn và thống kê dung lượng — hình dáng arena thật khi đóng gói.
""",
)

write_checkpoint(
    M5,
    L5CP,
    "Checkpoint: Arena with Alignment",
    "One allocator: bump slices that honor alignment requests, report used bytes, and reset cleanly.",
    16,
    "See lesson.",
    "Kiểm tra: Arena có căn chỉnh",
    "Một allocator: cắt phát tôn trọng yêu cầu căn, báo số byte đã dùng, và reset sạch sẽ.",
    "Xem bài học.",
    challenge(
        "ca5-checkpoint-aligned-arena",
        "Checkpoint: Aligned Arena",
        "Implement the arena with one addition — aligned allocation:@CE@ @CE@```c@CE@typedef struct { unsigned char *mem; size_t cap; size_t used; } arena_t;@CE@void arena_init(arena_t *a, unsigned char *buf, size_t cap);@CE@void *arena_alloc_aligned(arena_t *a, size_t n, size_t align);@CE@size_t arena_used(const arena_t *a);@CE@void arena_reset(arena_t *a);@CE@```@CE@ @CE@`arena_alloc_aligned` first aligns the current offset up to `align` (power of two), then places the slice; returns NULL if it cannot fit. `arena_used` reports current `used`.",
        C_PRELUDE,
        [
            ("alignment skips padding", "unsigned char buf[128];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@unsigned char *p1 = arena_alloc_aligned(&a, 3, 8);@NL@CHECK_EQ((int)(p1 - buf), 0);@NL@unsigned char *p2 = arena_alloc_aligned(&a, 1, 8);@NL@CHECK_EQ((int)(p2 - buf), 8);", "After a 3-byte slice the offset 3 aligns up to 8 — padding is consumed invisibly."),
            ("used counts padding", "unsigned char buf[128];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@arena_alloc_aligned(&a, 3, 8);@NL@arena_alloc_aligned(&a, 1, 8);@NL@CHECK_EQ((long long)arena_used(&a), 9);", "used is the next free offset: 1 byte at offset 8 means 9 total."),
            ("exhaustion respects align", "unsigned char buf[128];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@CHECK_NULL(arena_alloc_aligned(&a, 200, 8));", "A request larger than the whole buffer must fail even when the offset is aligned."),
            ("reset rewinds", "unsigned char buf[128];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@arena_alloc_aligned(&a, 40, 8);@NL@arena_reset(&a);@NL@CHECK_EQ((long long)arena_used(&a), 0);@NL@CHECK_NOT_NULL(arena_alloc_aligned(&a, 128, 16));", "After reset the entire buffer serves one maximally aligned slice."),
        ],
        level="mini-build",
    ),
    {
        "ca5-checkpoint-aligned-arena": vi_challenge(
            "Kiểm tra: Arena có căn chỉnh",
            "Cài arena_alloc_aligned (căn offset hiện tại lên bội align trước khi đặt slice), arena_used, arena_reset.",
            [
                ("căn nhảy qua đệm", "Sau slice 3 byte, offset 3 căn lên 8 — đệm được tiêu thụ vô hình."),
                ("used tính cả đệm", "used là offset trống kế tiếp: 1 byte tại offset 8 nghĩa là tổng 9."),
                ("hết chỗ tôn trọng căn", "Yêu cầu lớn hơn cả buffer phải thất bại."),
                ("reset quay về", "Sau reset cả buffer phục vụ một slice căn tối đa."),
            ],
        )
    },
    solution=C_PRELUDE
    + "typedef struct { unsigned char *mem; size_t cap; size_t used; } arena_t;@NL@"
    + "void arena_init(arena_t *a, unsigned char *buf, size_t cap) { a->mem = buf; a->cap = cap; a->used = 0; }@NL@"
    + "void *arena_alloc_aligned(arena_t *a, size_t n, size_t align) {@NL@    size_t aligned = (a->used + align - 1) & ~(align - 1);@NL@    if (aligned > a->cap || n > a->cap - aligned) return NULL;@NL@    void *p = a->mem + aligned;@NL@    a->used = aligned + n;@NL@    return p;@NL@}@NL@"
    + "size_t arena_used(const arena_t *a) { return a->used; }@NL@"
    + "void arena_reset(arena_t *a) { a->used = 0; }@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "typedef struct { unsigned char *mem; size_t cap; size_t used; } arena_t;@NL@"
    + "void arena_init(arena_t *a, unsigned char *buf, size_t cap) { a->mem = buf; a->cap = cap; a->used = 0; }@NL@"
    + "void *arena_alloc_aligned(arena_t *a, size_t n, size_t align) {@NL@    void *p = a->mem + a->used;@NL@    if (n > a->cap - a->used) return NULL;@NL@    a->used += n;@NL@    return p;@NL@}@NL@"
    + "size_t arena_used(const arena_t *a) { return a->used; }@NL@"
    + "void arena_reset(arena_t *a) { a->used = 0; }@NL@"
    + "int main(void) { return 0; }",
)

# =================== MODULE 6: ca-memory-ownership ==========================
M6 = "ca-memory-ownership"

L6A = "ca-ownership-contracts"
L6B = "ca-error-cleanup"
L6CP = "ca-checkpoint-m6"

write_module(
    M6,
    "Ownership and Error-Safe Cleanup",
    "C has no garbage collector — it has contracts. Ownership documentation, transfer vs borrow, and cleanup ladders that survive every error path.",
    "Quyền sở hữu và dọn dẹp an-toàn-lỗi",
    "C không có garbage collector — C có hợp đồng. Tài liệu hóa quyền sở hữu, chuyển giao vs mượn, và thang dọn dẹp sống sót qua mọi đường lỗi.",
    [L6A, L6B, L6CP],
    ["ca-p6-ownership"],
)

write_lesson(
    M6,
    L6A,
    "Ownership Contracts",
    "Who owns what: create/destroy pairs, transfer of ownership, borrows, and liveness counters as executable documentation.",
    15,
    """
## Every pointer has an owner

For every heap allocation the codebase must answer: which function or struct is responsible for freeing this, and when? Everything else holds a *borrow* — a pointer valid only within the owner's lifetime.

## The API shapes that encode ownership

- `handle_create` / `handle_destroy` — the module owns; callers hold a borrow between the two calls.
- `take(buf)` — the callee *takes ownership*: after the call, the caller must not free or use `buf`.
- `give()` — the callee returns ownership: the caller must eventually free it.
- `const T *view(const T *x)` — pure borrow: never freed by the receiver.

APIs that hide which shape they use are bugs in documentation form.

## Liveness counters make contracts executable

A module-level `objects_alive` counter — incremented in create, decremented in destroy — turns 'the caller leaked' from a code-review opinion into a testable fact. Production code does this in debug builds; this course does it in every ownership challenge.
""",
    "Hợp đồng quyền sở hữu",
    "Ai sở hữu cái gì: cặp create/destroy, chuyển giao quyền sở hữu, mượn, và bộ đếm sống làm tài liệu chạy được.",
    """
## Mọi con trỏ đều có chủ

Với mỗi cấp phát heap, codebase phải trả lời: hàm hoặc struct nào chịu trách nhiệm free thứ này, và khi nào? Mọi thứ khác chỉ *mượn* — con trỏ hợp lệ trong vòng đời của chủ.

## Các hình dạng API mã hóa quyền sở hữu

- `handle_create` / `handle_destroy` — mô-đun sở hữu; caller mượn giữa hai lần gọi.
- `take(buf)` — hàm được gọi *nhận quyền sở hữu*: sau lời gọi, caller không được free hay dùng `buf`.
- `give()` — hàm được gọi trao quyền sở hữu: caller cuối cùng phải free.
- `const T *view(const T *x)` — mượn thuần: người nhận không bao giờ free.

API che giấu hình dạng của nó là lỗi dưới dạng tài liệu.

## Bộ đếm sống biến hợp đồng thành thứ chạy được

Bộ đếm `objects_alive` cấp mô-đun — tăng trong create, giảm trong destroy — biến 'caller bị leak' từ ý kiến review thành sự kiện kiểm thử được. Code production làm điều này ở bản debug; khóa học làm điều đó trong mọi bài quyền sở hữu.
""",
)

write_lesson(
    M6,
    L6B,
    "Cleanup on Every Path",
    "The goto-cleanup ladder, single-exit discipline, and why error paths are where leaks are born.",
    14,
    """
## Errors happen in the middle

A function that acquires three resources can fail at three points. Every failure must release *exactly what was acquired so far* — no more, no less. Ad hoc frees duplicated in each branch is how leaks and double-frees are born.

## The ladder pattern

```c
int run(void) {
    int rc = -1;
    res_a *a = a_open();
    if (!a) goto fail;
    res_b *b = b_open(a);
    if (!b) goto fail_a;
    if (use(a, b) != 0) goto fail_b;
    rc = 0;
fail_b:
    b_close(b);
fail_a:
    a_close(a);
fail:
    return rc;
}
```

One exit ladder, unwinding in reverse acquisition order. `goto` is not taboo here — it is the pattern Linux itself uses, because it makes 'what happens on failure' readable in one place.

## Move-to-transfer hollows the source

Transferring a buffer between owners must *NULL out the source* — a hollowed owner is proof the transfer happened; a still-set source pointer is a double-free waiting for the second cleanup.
""",
    "Dọn dẹp trên mọi đường",
    "Thang goto-cleanup, kỷ luật một-lối-ra, và vì sao đường lỗi là nơi sinh ra leak.",
    """
## Lỗi xảy ra ở giữa

Hàm có ba tài nguyên có thể thất bại tại ba điểm. Mỗi thất bại phải giải phóng *đúng những gì đã cấp đến lúc đó* — không thiếu, không thừa. Free lặp lại tùy ý trong từng nhánh là nơi sinh ra leak và double-free.

## Mẫu thang

```c
int run(void) {
    int rc = -1;
    res_a *a = a_open();
    if (!a) goto fail;
    res_b *b = b_open(a);
    if (!b) goto fail_a;
    if (use(a, b) != 0) goto fail_b;
    rc = 0;
fail_b:
    b_close(b);
fail_a:
    a_close(a);
fail:
    return rc;
}
```

Một thang lối ra, trải ngược thứ tự cấp phát. `goto` không phải cấm kỵ ở đây — Linux dùng mẫu này, vì 'chuyện gì xảy ra khi lỗi' đọc được ở một chỗ.

## Chuyển giao làm rỗng nguồn

Chuyển buffer giữa hai chủ phải *gán NULL cho nguồn* — nguồn rỗng là bằng chứng chuyển giao đã xảy ra; nguồn vẫn giữ con trỏ là một double-free chờ lần dọn thứ hai.
""",
)

write_practice(
    M6,
    "ca-p6-ownership",
    "Ownership Contract Drills",
    "Create/destroy discipline, transfer semantics, cleanup ladders, and refcounting — each observable through liveness counters.",
    "Bài tập hợp đồng sở hữu",
    "Kỷ luật create/destroy, ngữ nghĩa chuyển giao, thang dọn dẹp, và refcount — mỗi cái quan sát được qua bộ đếm sống.",
    L6A,
    24,
    "advanced",
    [
        challenge(
            "ca6-gadget",
            "Create/Destroy with a Liveness Counter",
            "A file-scope `int gadgets_alive = 0;` is already in your editor. Implement `gadget_t *gadget_create(int id)` (heap-allocate, set id, increment the counter), `int gadget_id(const gadget_t *g)`, and `void gadget_destroy(gadget_t *g)` (decrement, free; NULL is a no-op). The counter is the contract, made executable.",
            C_PRELUDE + "int gadgets_alive = 0;@NL@",
            [
                ("lifecycle tracks", "CHECK_EQ(gadgets_alive, 0);@NL@gadget_t *g = gadget_create(42);@NL@CHECK_EQ(gadgets_alive, 1);@NL@CHECK_EQ(gadget_id(g), 42);@NL@gadget_destroy(g);@NL@CHECK_EQ(gadgets_alive, 0);", "Create increments, destroy decrements — the pair is balanced in one lifetime."),
                ("NULL destroy is safe", "gadget_destroy(NULL);@NL@CHECK_EQ(gadgets_alive, 0);", "Freeing nothing must not corrupt the count."),
            ],
            level="guided",
        ),
        challenge(
            "ca6-move-hollow",
            "Transfer Hollows the Source",
            "Implement the buffer move that transfers ownership:@CE@ @CE@```c@CE@typedef struct { int *buf; size_t len; size_t cap; } vec_t;@CE@void vec_move(vec_t *dst, vec_t *src);@CE@void vec_free(vec_t *v);@CE@```@CE@ @CE@`vec_move` gives dst the buffer and *hollows* src (buf = NULL, len = cap = 0). `vec_free` releases what an owner holds. A file-scope `int buffers_alive = 0;` increments in... nothing yet — see the rules: define it yourself inside vec allocations if you need it; the tests only check the hollowing and value preservation.",
            C_PRELUDE,
            [
                ("move preserves values", "int *b = malloc(3 * sizeof(int));@NL@for (int i = 0; i < 3; i++) b[i] = i + 1;@NL@vec_t src = {b, 3, 3};@NL@vec_t dst = {0, 0, 0};@NL@vec_move(&dst, &src);@NL@CHECK_EQ(dst.buf[0], 1);@NL@CHECK_EQ(dst.buf[2], 3);@NL@CHECK_EQ((long long)dst.len, 3);@NL@free(dst.buf);", "The buffer pointer transfers; the values ride along untouched."),
                ("source is hollowed", "int *b2 = malloc(2 * sizeof(int));@NL@b2[0] = 7;@NL@vec_t s2 = {b2, 2, 2};@NL@vec_t d2 = {0, 0, 0};@NL@vec_move(&d2, &s2);@NL@CHECK_NULL(s2.buf);@NL@CHECK_EQ((long long)s2.len, 0);@NL@free(d2.buf);", "After the move the source holds nothing — a second free of it is impossible by construction."),
            ],
            level="independent",
        ),
        challenge(
            "ca6-ladder",
            "The Cleanup Ladder",
            "File-scope counters `int a_alive = 0, b_alive = 0, c_alive = 0;` are already in your editor. Implement `int cleanup_ladder(int fail_at)` simulating a three-resource acquisition: allocate A (a_alive++), then B (b_alive++), then C (c_alive++); if fail_at is 1, 2, or 3, simulate failure *before* that resource's allocation, releasing everything acquired so far in reverse order and returning -1; success returns 0 with everything released too. Every path must leave all counters at 0.",
            C_PRELUDE + "int a_alive = 0, b_alive = 0, c_alive = 0;@NL@",
            [
                ("fail at 1", "CHECK_EQ(cleanup_ladder(1), -1);@NL@CHECK_EQ(a_alive, 0);@NL@CHECK_EQ(b_alive, 0);@NL@CHECK_EQ(c_alive, 0);", "Nothing beyond A was acquired; A itself is released on the way out."),
                ("fail at 2", "CHECK_EQ(cleanup_ladder(2), -1);@NL@CHECK_EQ(a_alive, 0);@NL@CHECK_EQ(b_alive, 0);", "A and B acquired, both released, reverse order."),
                ("fail at 3", "CHECK_EQ(cleanup_ladder(3), -1);@NL@CHECK_EQ(a_alive, 0);@NL@CHECK_EQ(b_alive, 0);@NL@CHECK_EQ(c_alive, 0);", "All three acquired, all released."),
                ("success releases too", "CHECK_EQ(cleanup_ladder(0), 0);@NL@CHECK_EQ(a_alive, 0);@NL@CHECK_EQ(c_alive, 0);", "The success path is also a cleanup path."),
            ],
            level="combination",
        ),
        challenge(
            "ca6-refcount",
            "Reference Counting by Hand",
            "A file-scope `int rcs_alive = 0;` is already in your editor. Implement `rc_t *rc_create(void)` (refs = 1, counter++), `void rc_hold(rc_t *r)` (refs++), `void rc_release(rc_t *r)` (refs--; when it reaches 0: counter--, free; NULL is a no-op), and `int rc_refs(const rc_t *r)`.",
            C_PRELUDE + "int rcs_alive = 0;@NL@",
            [
                ("ref arithmetic", "rc_t *r = rc_create();@NL@CHECK_EQ(rc_refs(r), 1);@NL@rc_hold(r);@NL@rc_hold(r);@NL@CHECK_EQ(rc_refs(r), 3);@NL@rc_release(r);@NL@CHECK_EQ(rc_refs(r), 2);@NL@rc_release(r);@NL@rc_release(r);@NL@CHECK_EQ(rcs_alive, 0);", "holds raise, releases lower, the last one frees — the counter proves it."),
                ("over-release guard", "rc_t *r2 = rc_create();@NL@rc_release(r2);@NL@rc_release(NULL);@NL@CHECK_EQ(rcs_alive, 0);", "Release on an already-freed object must not be possible through the API; NULL release is a no-op."),
            ],
            level="combination",
        ),
    ],
    {
        "ca6-gadget": vi_challenge(
            "Create/Destroy với bộ đếm sống",
            "Có sẵn `int gadgets_alive = 0;`. Cài gadget_create/gadget_id/gadget_destroy — bộ đếm là hợp đồng chạy được.",
            [
                ("vòng đời khớp", "Create tăng, destroy giảm — cặp này cân bằng trong một vòng đời."),
                ("destroy NULL an toàn", "Free cái không gì không được làm hỏng bộ đếm."),
            ],
        ),
        "ca6-move-hollow": vi_challenge(
            "Chuyển giao làm rỗng nguồn",
            "Cài vec_move (dst nhận buffer, src bị rỗng) và vec_free — sau chuyển giao nguồn không còn gì để free lần hai.",
            [
                ("chuyển giữ nguyên giá trị", "Con trỏ buffer chuyển giao; giá trị đi theo không đổi."),
                ("nguồn bị rỗng", "Sau move nguồn không giữ gì — free lần hai bất khả theo cấu trúc."),
            ],
        ),
        "ca6-ladder": vi_challenge(
            "Thang dọn dẹp",
            "Có sẵn bộ đếm a/b/c_alive. Cài cleanup_ladder(fail_at): mô phỏng lấy 3 tài nguyên, thất bại thì giải phóng ngược thứ tự, mọi đường để bộ đếm về 0.",
            [
                ("fail tại 1", "Chỉ A được cấp; A được giải phóng trên đường ra."),
                ("fail tại 2", "A và B được cấp, cả hai được giải phóng theo thứ tự ngược."),
                ("fail tại 3", "Cả ba được cấp, cả ba được giải phóng."),
                ("thành công cũng dọn", "Đường thành công cũng là đường dọn dẹp."),
            ],
        ),
        "ca6-refcount": vi_challenge(
            "Đếm tham chiếu thủ công",
            "Có sẵn `int rcs_alive = 0;`. Cài rc_create/rc_hold/rc_release/rc_refs — lần release cuối free, NULL là no-op.",
            [
                ("số học tham chiếu", "hold tăng, release giảm, lần cuối free — bộ đếm chứng minh điều đó."),
                ("chống release thừa", "Release trên đối tượng đã free không thể xảy ra qua API; release NULL là no-op."),
            ],
        ),
    },
    solutions=[
        (
            "ca6-gadget",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "int gadgets_alive = 0;@NL@"
            + "typedef struct { int id; } gadget_t;@NL@"
            + "gadget_t *gadget_create(int id) {@NL@    gadget_t *g = malloc(sizeof *g);@NL@    if (!g) return NULL;@NL@    g->id = id;@NL@    gadgets_alive++;@NL@    return g;@NL@}@NL@"
            + "int gadget_id(const gadget_t *g) { return g->id; }@NL@"
            + "void gadget_destroy(gadget_t *g) {@NL@    if (!g) return;@NL@    gadgets_alive--;@NL@    free(g);@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "int gadgets_alive = 0;@NL@"
            + "typedef struct { int id; } gadget_t;@NL@"
            + "gadget_t *gadget_create(int id) {@NL@    gadget_t *g = malloc(sizeof *g);@NL@    g->id = id;@NL@    gadgets_alive++;@NL@    return g;@NL@}@NL@"
            + "int gadget_id(const gadget_t *g) { return g->id; }@NL@"
            + "void gadget_destroy(gadget_t *g) { free(g); }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca6-move-hollow",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "typedef struct { int *buf; size_t len; size_t cap; } vec_t;@NL@"
            + "void vec_move(vec_t *dst, vec_t *src) {@NL@    dst->buf = src->buf;@NL@    dst->len = src->len;@NL@    dst->cap = src->cap;@NL@    src->buf = NULL;@NL@    src->len = 0;@NL@    src->cap = 0;@NL@}@NL@"
            + "void vec_free(vec_t *v) {@NL@    free(v->buf);@NL@    v->buf = NULL;@NL@    v->len = 0;@NL@    v->cap = 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "typedef struct { int *buf; size_t len; size_t cap; } vec_t;@NL@"
            + "void vec_move(vec_t *dst, vec_t *src) {@NL@    dst->buf = malloc(src->len * sizeof(int));@NL@    dst->len = src->len;@NL@    dst->cap = src->cap;@NL@    for (size_t i = 0; i < src->len; i++) dst->buf[i] = src->buf[i];@NL@}@NL@"
            + "void vec_free(vec_t *v) {@NL@    free(v->buf);@NL@    v->buf = NULL;@NL@    v->len = 0;@NL@    v->cap = 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca6-ladder",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "int a_alive = 0, b_alive = 0, c_alive = 0;@NL@"
            + "int cleanup_ladder(int fail_at) {@NL@    a_alive++;@NL@    if (fail_at == 1) { a_alive--; return -1; }@NL@    b_alive++;@NL@    if (fail_at == 2) { b_alive--; a_alive--; return -1; }@NL@    c_alive++;@NL@    if (fail_at == 3) { c_alive--; b_alive--; a_alive--; return -1; }@NL@    c_alive--; b_alive--; a_alive--;@NL@    return 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "int a_alive = 0, b_alive = 0, c_alive = 0;@NL@"
            + "int cleanup_ladder(int fail_at) {@NL@    a_alive++;@NL@    if (fail_at == 1) { a_alive--; return -1; }@NL@    b_alive++;@NL@    if (fail_at == 2) { b_alive--; return -1; }@NL@    c_alive++;@NL@    if (fail_at == 3) { c_alive--; b_alive--; a_alive--; return -1; }@NL@    c_alive--; b_alive--; a_alive--;@NL@    return 0;@NL@}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca6-refcount",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "int rcs_alive = 0;@NL@"
            + "typedef struct { int refs; } rc_t;@NL@"
            + "rc_t *rc_create(void) {@NL@    rc_t *r = malloc(sizeof *r);@NL@    if (!r) return NULL;@NL@    r->refs = 1;@NL@    rcs_alive++;@NL@    return r;@NL@}@NL@"
            + "void rc_hold(rc_t *r) { if (r) r->refs++; }@NL@"
            + "void rc_release(rc_t *r) {@NL@    if (!r) return;@NL@    if (--r->refs == 0) { rcs_alive--; free(r); }@NL@}@NL@"
            + "int rc_refs(const rc_t *r) { return r->refs; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "#include <stdlib.h>@NL@"
            + "int rcs_alive = 0;@NL@"
            + "typedef struct { int refs; } rc_t;@NL@"
            + "rc_t *rc_create(void) {@NL@    rc_t *r = malloc(sizeof *r);@NL@    r->refs = 1;@NL@    rcs_alive++;@NL@    return r;@NL@}@NL@"
            + "void rc_hold(rc_t *r) { if (r) r->refs += 2; }@NL@"
            + "void rc_release(rc_t *r) {@NL@    if (!r) return;@NL@    if (--r->refs <= 0) { rcs_alive--; free(r); }@NL@}@NL@"
            + "int rc_refs(const rc_t *r) { return r->refs; }@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_lesson(
    M6,
    L6CP,
    "Checkpoint: Move and Clean Up",
    "Consolidated ownership checkpoint.",
    12,
    """
Checkpoint for module 6: transfer a buffer with hollowing, push values through it, and survive a mid-stream failure with zero leaks — counters prove every claim.
""",
    "Kiểm tra: Chuyển giao và dọn dẹp",
    "Kiểm tra tổng hợp quyền sở hữu.",
    """
Kiểm tra mô-đun 6: chuyển giao buffer với rỗng hóa, push giá trị qua nó, và sống sót qua lỗi giữa đường với không leak — bộ đếm chứng minh mọi lời nói.
""",
)

write_checkpoint(
    M6,
    L6CP,
    "Checkpoint: Transfer and Survive Failure",
    "One program: a vector that transfers ownership by hollowing, a fill routine that can simulate failure at any step, and a liveness counter proving no path leaks.",
    16,
    "See lesson.",
    "Kiểm tra: Chuyển giao và sống sót qua lỗi",
    "Một chương trình: vector chuyển giao quyền sở hữu bằng rỗng hóa, hàm fill mô phỏng lỗi ở bất kỳ bước nào, và bộ đếm sống chứng minh không đường nào leak.",
    "Xem bài học.",
    challenge(
        "ca6-checkpoint-transfer",
        "Checkpoint: Transfer + Failure-Safe Fill",
        "A file-scope `int vecs_alive = 0;` is in your editor. Implement:@CE@ @CE@```c@CE@typedef struct { int *buf; size_t len; size_t cap; } vec_t;@CE@int vec_push(vec_t *v, int value);@CE@void vec_free(vec_t *v);@CE@void vec_move(vec_t *dst, vec_t *src);@CE@int vec_fill(vec_t *v, int n, int fail_at);@CE@```@CE@ @CE@`vec_push` doubles capacity (starting at 1) and counts as an allocation: while `v->buf` is non-NULL it counts one toward `vecs_alive` — simplest honest model: vec_push sets `vecs_alive = 1` the first time it allocates for this vec. `vec_free` releases and hollows. `vec_move` transfers and hollows the source (without changing the counter — ownership moved, the count did not). `vec_fill` pushes 1..n; if the push that would be number `fail_at` (1-based) cannot proceed because a simulated allocation failure occurs there, free everything and return -1; success returns 0. Simulate the failure deterministically: fail exactly when the next index equals fail_at, before allocating.",
        C_PRELUDE + "int vecs_alive = 0;@NL@",
        [
            ("fill then free", "vec_t v = {0, 0, 0};@NL@CHECK_EQ(vec_fill(&v, 3, 0), 0);@NL@CHECK_EQ(v.buf[0], 1);@NL@CHECK_EQ(v.buf[2], 3);@NL@CHECK_EQ(vecs_alive, 1);@NL@vec_free(&v);@NL@CHECK_EQ(vecs_alive, 0);@NL@CHECK_NULL(v.buf);", "Fill pushes 1..3; one live buffer while owned; free zeroes both the memory and the counter."),
            ("failure cleans up", "vec_t w = {0, 0, 0};@NL@CHECK_EQ(vec_fill(&w, 5, 3), -1);@NL@CHECK_EQ(vecs_alive, 0);@NL@CHECK_NULL(w.buf);", "Failing before the third push releases the first two reallocations — no leak survives."),
            ("move hollows source", "vec_t s = {0, 0, 0};@NL@vec_fill(&s, 2, 0);@NL@vec_t d = {0, 0, 0};@NL@vec_move(&d, &s);@NL@CHECK_NULL(s.buf);@NL@CHECK_EQ(d.buf[1], 2);@NL@CHECK_EQ(vecs_alive, 1);@NL@vec_free(&d);@NL@CHECK_EQ(vecs_alive, 0);", "The transfer hollows the source; the live count is unchanged by moving; freeing the new owner zeroes it."),
        ],
        level="mini-build",
    ),
    {
        "ca6-checkpoint-transfer": vi_challenge(
            "Kiểm tra: Chuyển giao + fill an toàn lỗi",
            "Có sẵn `int vecs_alive = 0;`. Cài vec_push (tăng gấp đôi), vec_free, vec_move (rỗng hóa nguồn), vec_fill (mô phỏng lỗi tại fail_at, dọn sạch rồi trả -1).",
            [
                ("fill rồi free", "Fill push 1..3; một buffer sống khi được sở hữu; free xóa cả bộ nhớ lẫn bộ đếm."),
                ("lỗi được dọn", "Thất bại trước push thứ ba giải phóng hai lần cấp lại trước đó — không leak sống sót."),
                ("move rỗng hóa nguồn", "Chuyển giao rỗng hóa nguồn; số sống không đổi khi chuyển; free chủ mới đưa về 0."),
            ],
        )
    },
    solution=C_PRELUDE
    + "#include <stdlib.h>@NL@"
    + "int vecs_alive = 0;@NL@"
    + "typedef struct { int *buf; size_t len; size_t cap; } vec_t;@NL@"
    + "int vec_push(vec_t *v, int value) {@NL@    if (v->len == v->cap) {@NL@        size_t nc = v->cap ? v->cap * 2 : 1;@NL@        int *nb = realloc(v->buf, nc * sizeof(int));@NL@        if (!nb) return -1;@NL@        v->buf = nb;@NL@        v->cap = nc;@NL@        vecs_alive = 1;@NL@    }@NL@    v->buf[v->len++] = value;@NL@    return 0;@NL@}@NL@"
    + "void vec_free(vec_t *v) {@NL@    free(v->buf);@NL@    v->buf = NULL;@NL@    v->len = 0;@NL@    v->cap = 0;@NL@    vecs_alive = 0;@NL@}@NL@"
    + "void vec_move(vec_t *dst, vec_t *src) {@NL@    dst->buf = src->buf;@NL@    dst->len = src->len;@NL@    dst->cap = src->cap;@NL@    src->buf = NULL;@NL@    src->len = 0;@NL@    src->cap = 0;@NL@}@NL@"
    + "int vec_fill(vec_t *v, int n, int fail_at) {@NL@    for (int i = 1; i <= n; i++) {@NL@        if (i == fail_at) { vec_free(v); return -1; }@NL@        if (vec_push(v, i) != 0) { vec_free(v); return -1; }@NL@    }@NL@    return 0;@NL@}@NL@"
    + "int main(void) { return 0; }",
    wrong=C_PRELUDE
    + "#include <stdlib.h>@NL@"
    + "int vecs_alive = 0;@NL@"
    + "typedef struct { int *buf; size_t len; size_t cap; } vec_t;@NL@"
    + "int vec_push(vec_t *v, int value) {@NL@    if (v->len == v->cap) {@NL@        size_t nc = v->cap ? v->cap * 2 : 1;@NL@        int *nb = realloc(v->buf, nc * sizeof(int));@NL@        if (!nb) return -1;@NL@        v->buf = nb;@NL@        v->cap = nc;@NL@        vecs_alive = 1;@NL@    }@NL@    v->buf[v->len++] = value;@NL@    return 0;@NL@}@NL@"
    + "void vec_free(vec_t *v) {@NL@    free(v->buf);@NL@    v->buf = NULL;@NL@    v->len = 0;@NL@    v->cap = 0;@NL@    vecs_alive = 0;@NL@}@NL@"
    + "void vec_move(vec_t *dst, vec_t *src) {@NL@    dst->buf = src->buf;@NL@    dst->len = src->len;@NL@    dst->cap = src->cap;@NL@}@NL@"
    + "int vec_fill(vec_t *v, int n, int fail_at) {@NL@    for (int i = 1; i <= n; i++) {@NL@        if (i == fail_at) { return -1; }@NL@        if (vec_push(v, i) != 0) { vec_free(v); return -1; }@NL@    }@NL@    return 0;@NL@}@NL@"
    + "int main(void) { return 0; }",
)
