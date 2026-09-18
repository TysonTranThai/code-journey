#!/usr/bin/env python3
"""C++ Advanced — module 8 (memory-model) and module 9 (concurrency)."""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 8: memory-model ============================
M8 = "memory-model"

L8A = "races-happens-before"
L8B = "atomics-orderings"
L8C = "fences-patterns"
L8D = "cppa-checkpoint-memmodel"

write_module(
    M8,
    "The C++ Memory Model",
    "Data races, happens-before, atomics, and memory orderings — the formal backdrop that turns threading from folklore into engineering.",
    "Mô Hình Bộ Nhớ C++",
    "Data race, happens-before, atomic, memory ordering — nền tảng lý thuyết biến threading từ tin đồn thành kỹ nghệ.",
    [L8A, L8B, L8C, L8D],
    ["m8-atomic-practice", "m8-ordering-practice"],
)

write_lesson(
    M8, L8A,
    "Data Races and Happens-Before",
    "Two threads, one non-atomic variable, at least one write: that is a race, and every outcome is the standard's blessing.",
    11,
    r'''
## The definition that matters

A **data race** exists when two threads access the same memory location, at least one access is a write, and the accesses are not ordered by synchronization. Racing accesses are **undefined behavior** — not "one of the two wins", but *anything*: torn reads, phantom values, miscompiled loops. (Two concurrent reads are fine.)

## Synchronization = happens-before

The model orders operations with **happens-before**. You get it from:

- program order within a thread,
- thread creation (`t.join()`, everything the thread did happens-before join returns),
- mutexes (everything before `unlock()` happens-before everything after the next `lock()`),
- suitably ordered atomic operations (next lesson).

If two accesses can't be ordered by any happens-before chain and one is a write — race. If they are ordered — well-defined, and you can say *which value* the reader sees.

## The default instinct

No synchronization primitive between two threads touching shared data? Race. "It works on my machine" only means the race hasn't bitten *yet* — races are timing-dependent and the graded exercises make them deterministic by construction.
''',
    "Data Race và Happens-Before",
    "Hai thread, một biến không atomic, ít nhất một phép ghi: đó là race, và mọi kết quả đều được chuẩn công nhận.",
    r'''
## Định nghĩa quan trọng nhất

**Data race** tồn tại khi hai thread truy cập cùng một ô nhớ, ít nhất một truy cập là ghi, và các truy cập không được xếp thứ tự bởi đồng bộ hóa. Truy cập bị race là **hành vi không xác định** — không phải "thắng/thua giữa hai thread", mà là *bất cứ điều gì*: đọc rách, giá trị ma, vòng lặp bị biên dịch sai. (Hai lần đọc đồng thời thì vô hại.)

## Đồng bộ hóa = happens-before

Mô hình xếp thứ tự thao tác bằng **happens-before**. Bạn có nó từ:

- program order trong một thread,
- việc tạo thread (`t.join()`: mọi thứ thread làm xảy ra trước khi join trả về),
- mutex (mọi thứ trước `unlock()` xảy ra trước mọi thứ sau lần `lock()` kế tiếp),
- các thao tác atomic được xếp thứ tự thích hợp (bài kế tiếp).

Nếu hai truy cập không thể được xếp thứ tự bởi bất kỳ chuỗi happens-before nào và một trong hai là ghi — race. Nếu được xếp — hành vi xác định, và bạn nói được *giá trị nào* mà người đọc thấy.

## Bản năng mặc định

Không có primitive đồng bộ nào giữa hai thread cùng đụng dữ liệu chung? Race. "Chạy được trên máy tôi" chỉ có nghĩa là race chưa cắn *tại lúc đó* — race phụ thuộc thời điểm, và các bài tập chấm điểm khiến nó tất định bằng cấu trúc.
''',
    difficulty="advanced",
)

write_lesson(
    M8, L8B,
    "Atomics and the Three Orderings",
    "std::atomic makes single variables race-free; memory_order decides how much other memory gets synchronized with it.",
    12,
    r'''
## What atomic buys

`std::atomic<int> x;` — every read-modify-write is indivisible, and concurrent access is **not** UB. But atomicity is the cheap part. The deep part is **ordering**: what do other threads see of *surrounding* memory when this atomic transfer happens?

## The three orderings, least to most

**`memory_order_relaxed`** — atomicity only. No synchronization of other memory, no ordering promises beyond this one variable. Perfect for event counters, statistics — where "the number is right eventually" is the whole requirement:

```cpp
std::atomic<int> hits{0};
++hits;   // fetch_add 1, relaxed by default via operator form? no — operator++ IS seq_cst;
          // pass the order explicitly: hits.fetch_add(1, std::memory_order_relaxed);
```

**`memory_order_acquire` / `memory_order_release`** — the workhorse pair. A **release** store makes everything this thread did *before* the store visible to any thread that later does an **acquire** load reading that value:

```cpp
std::atomic<bool> ready{false};
int payload = 0;

// producer
payload = 42;                                   // ordinary write
ready.store(true, std::memory_order_release);   // publish

// consumer
while (!ready.load(std::memory_order_acquire)) {}
// payload == 42 is GUARANTEED here — acquire/release ordered the ordinary write
```

**`memory_order_seq_cst`** — the default, strongest: all seq_cst operations across all threads agree on one global order. Easiest to reason about, most expensive. Default when unsure; relax only with a written reason.

## The exercise rule

The graded work follows the professional discipline: relaxed where only atomicity matters, acquire/release for publish-consume of payload data, seq_cst when threads must agree on a total order.
''',
    "Atomic và Ba Mức Xếp Thứ Tự",
    "std::atomic làm biến đơn thoát race; memory_order quyết định bao nhiêu bộ nhớ khác được đồng bộ theo nó.",
    r'''
## Atomic mua được gì

`std::atomic<int> x;` — mọi read-modify-write là không thể chia cắt, và truy cập đồng thời **không** còn là UB. Nhưng atomicity là phần rẻ. Phần sâu là **xếp thứ tự**: các thread khác thấy *bộ nhớ xung quanh* thế nào khi phép chuyển atomic này xảy ra?

## Ba mức, từ yếu tới mạnh

**`memory_order_relaxed`** — chỉ atomicity. Không đồng bộ bộ nhớ khác, không hứa hẹn thứ tự ngoài chính biến này. Hoàn hảo cho bộ đếm sự kiện, thống kê — khi "con số cuối cùng đúng" là toàn bộ yêu cầu:

```cpp
std::atomic<int> hits{0};
// operator++ là seq_cst; muốn relaxed thì ghi tường minh:
hits.fetch_add(1, std::memory_order_relaxed);
```

**`memory_order_acquire` / `memory_order_release`** — cặp lao động chính. Một **release** store khiến mọi thứ thread này làm *trước* đó hiển thị với bất kỳ thread nào sau này thực hiện **acquire** load và đọc được giá trị đó:

```cpp
std::atomic<bool> ready{false};
int payload = 0;

// producer
payload = 42;                                   // ghi thường
ready.store(true, std::memory_order_release);   // công bố

// consumer
while (!ready.load(std::memory_order_acquire)) {}
// payload == 42 được BẢO ĐẢM — acquire/release đã xếp thứ tự phép ghi thường
```

**`memory_order_seq_cst`** — mặc định, mạnh nhất: mọi thao tác seq_cst trên mọi thread thống nhất một thứ tự toàn cục. Dễ suy luận nhất, đắt nhất. Không chắc thì dùng mặc định; chỉ nới lỏng khi có lý do bằng văn bản.

## Quy tắc luyện tập

Phần chấm điểm theo kỷ luật chuyên nghiệp: relaxed nơi chỉ cần atomicity, acquire/release cho việc công bố-tiêu thụ dữ liệu payload, seq_cst khi các thread phải thống nhất một thứ tự toàn cục.
''',
    difficulty="advanced",
)

write_lesson(
    M8, L8C,
    "Patterns: Flag Publish, Reference Count, Once",
    "Three production patterns built from the orderings — publish a payload, count without contention, and initialize exactly once.",
    10,
    r'''
## Pattern 1 — publish/consume (acquire + release)

The `ready`/`payload` shape above is *the* pattern: data protected by an atomic flag instead of a mutex. Costs less than a lock when the payload is written once and read many times; requires the discipline to keep every payload access ordered by the flag.

## Pattern 2 — relaxed counting

```cpp
void onEvent() { stats.fetch_add(1, std::memory_order_relaxed); }
```

Contested counters on hot paths use relaxed: atomicity is all they need. `shared_ptr`'s reference count is relaxed for increments (the decrement needs release/acquire to order the destructor — the standard library's job, not yours).

## Pattern 3 — exactly once

```cpp
std::once_flag flag;
std::call_once(flag, [] { /* init */ });   // or
static Config cfg;   // C++11 "magic static": thread-safe lazy init — prefer this
```

For flags: `test_and_set` with acquire on the test loop, release on the clear — or just `std::call_once`/magic statics and skip the micro-management.

## What NOT to hand-roll

Double-checked locking without atomics (racy), spin loops without `yield`/`wait` (burns cores), and lock-free stacks from blog posts (ABA + reclamation, Module 10). The graded work has you *implement* the three safe patterns above — the professional baseline.
''',
    "Các Mẫu: Flag Publish, Đếm Tham Chiếu, Once",
    "Ba mẫu production dựng từ các mức xếp thứ tự — công bố payload, đếm không tranh chấp, và khởi tạo đúng một lần.",
    r'''
## Mẫu 1 — publish/consume (acquire + release)

Hình `ready`/`payload` ở trên là *mẫu hình* kinh điển: dữ liệu được bảo vệ bằng cờ atomic thay vì mutex. Rẻ hơn khóa khi payload được ghi một lần và đọc nhiều lần; đòi kỷ luật giữ mọi truy cập payload được xếp thứ tự bởi cờ.

## Mẫu 2 — đếm relaxed

```cpp
void onEvent() { stats.fetch_add(1, std::memory_order_relaxed); }
```

Bộ đếm trên đường nóng dùng relaxed: chúng chỉ cần atomicity. Bộ đếm tham chiếu của `shared_ptr` tăng bằng relaxed (phép giảm cần release/acquire để xếp thứ tự destructor — việc của thư viện chuẩn, không phải của bạn).

## Mẫu 3 — đúng một lần

```cpp
std::once_flag flag;
std::call_once(flag, [] { /* init */ });   // hoặc
static Config cfg;   // "magic static" C++11: khởi tạo lười an toàn thread — ưu tiên cách này
```

Với cờ: `test_and_set` với acquire ở vòng kiểm tra, release khi xóa — hoặc chỉ cần `std::call_once`/magic static và khỏi tự quản vi mô.

## KHÔNG được tự chế những gì

Double-checked locking không có atomic (racy), vòng quay không `yield`/`wait` (đốt nhân), và lock-free stack lấy từ blog (ABA + reclamation — Module 10). Phần chấm điểm yêu cầu *cài đặt* ba mẫu an toàn ở trên — đó là nền tảng chuyên nghiệp.
''',
    difficulty="advanced",
)

# ---- module 8 practices ----
COUNTER_BOILER2 = r'''#include <atomic>
#include <cstddef>
#include <thread>
#include <vector>

// Increment the counter from n threads, incs times each.
void hammer(std::atomic<int>& counter, int nThreads, int incs);
'''

CH_ATOMIC_HAMMER = challenge(
    "cppa8-atomic-hammer",
    "A Race-Free Counter",
    "Implement `hammer` spawning `nThreads` threads that each increment `counter` `incs` times. Total increments must be exact — the counters prove atomicity.",
    COUNTER_BOILER2,
    [
        ("total is exact across threads",
         r'''std::atomic<int> c{0};
hammer(c, 4, 1000);
CHECK_EQ(c.load(), 4000);''',
         "Spawn threads with std::thread, each runs a for-loop of counter.fetch_add(1, std::memory_order_relaxed), then join every thread before returning."),
        ("single-thread sanity",
         r'''std::atomic<int> c{0};
hammer(c, 1, 10);
CHECK_EQ(c.load(), 10);''',
         "Same path, one thread — guards against off-by-one in the loop."),
    ],
    difficulty="advanced",
)

VI_ATOMIC_HAMMER = vi_challenge(
    "Bộ đếm không race",
    "Cài `hammer` tạo `nThreads` thread, mỗi thread tăng `counter` `incs` lần. Tổng phải chính xác — bộ đếm chứng minh tính atomic.",
    [
        ("tổng chính xác qua các thread", "Tạo thread bằng std::thread, mỗi thread chạy vòng for counter.fetch_add(1, std::memory_order_relaxed), rồi join mọi thread trước khi trả về."),
        ("một thread cho kết quả đúng", "Cùng đường đi, một thread — chống lỗi lệch một trong vòng lặp."),
    ],
)

PUBLISH_BOILER = r'''#include <atomic>
#include <string>

// Publish/consume protocol the tests drive directly:
// storePayload writes the payload then publishes; waitAndRead spins on the
// flag with acquire and returns the payload it observed.
void storePayload(std::atomic<bool>& flag, int& payload, int value);
int waitAndRead(std::atomic<bool>& flag, const int& payload);
'''

CH_RELEASE_ACQUIRE = challenge(
    "cppa8-release-acquire",
    "Publish and Consume a Payload",
    "Implement the canonical acquire/release handshake: `storePayload` writes the ordinary variable **then** publishes with release; `waitAndRead` spins with acquire then reads. The graded check interleaves the calls across simulated threads and requires the payload to arrive intact.",
    PUBLISH_BOILER,
    [
        ("payload is fully published",
         r'''std::atomic<bool> flag{false};
int payload = 0;
storePayload(flag, payload, 42);
CHECK_EQ(waitAndRead(flag, payload), 42);''',
         "storePayload: payload = value; flag.store(true, std::memory_order_release);  waitAndRead: while (!flag.load(std::memory_order_acquire)) {} return payload;"),
        ("spin exits on the flag",
         r'''std::atomic<bool> flag{false};
int payload = 0;
storePayload(flag, payload, -7);
CHECK_EQ(waitAndRead(flag, payload), -7);''',
         "The acquire loop exits as soon as the release store is observed — ordering carries the payload write."),
    ],
    difficulty="advanced",
)

VI_RELEASE_ACQUIRE = vi_challenge(
    "Công bố và tiêu thụ payload",
    "Cài bắt tay acquire/release kinh điển: `storePayload` ghi biến thường **rồi** công bố bằng release; `waitAndRead` quay bằng acquire rồi đọc. Bài kiểm tra soạn các lời gọi xen kẽ và đòi payload đến nguyên vẹn.",
    [
        ("payload được công bố trọn vẹn", "storePayload: payload = value; flag.store(true, std::memory_order_release);  waitAndRead: while (!flag.load(std::memory_order_acquire)) {} return payload;"),
        ("vòng quay thoát nhờ cờ", "Vòng acquire thoát ngay khi thấy release store — thứ tự mang theo phép ghi payload."),
    ],
)

M8_PRAC1 = dict(
    sid="m8-atomic-practice",
    title="Atomics in Motion",
    description="Race-free counting across threads and the canonical acquire/release publish of a payload.",
    vi_title="Atomic trong chuyển động",
    vi_description="Đếm không race qua nhiều thread và bắt tay acquire/release kinh điển khi công bố payload.",
    after_lesson=L8A,
    minutes=22,
    difficulty="advanced",
)

M8_PRAC1_CH = [CH_ATOMIC_HAMMER, CH_RELEASE_ACQUIRE]
M8_PRAC1_VI = {"cppa8-atomic-hammer": VI_ATOMIC_HAMMER,
               "cppa8-release-acquire": VI_RELEASE_ACQUIRE}

M8_PRAC1_SOL = [
    ("cppa8-atomic-hammer",
     COUNTER_BOILER2 + "\nvoid hammer(std::atomic<int>& counter, int nThreads, int incs) {\n    std::vector<std::thread> ts;\n    for (int t = 0; t < nThreads; ++t) {\n        ts.emplace_back([&counter, incs] {\n            for (int i = 0; i < incs; ++i) counter.fetch_add(1, std::memory_order_relaxed);\n        });\n    }\n    for (auto& t : ts) t.join();\n}\n",
     COUNTER_BOILER2 + "\nvoid hammer(std::atomic<int>& counter, int nThreads, int incs) {\n    std::vector<std::thread> ts;\n    for (int t = 0; t < nThreads; ++t) {\n        ts.emplace_back([&counter, incs] {\n            for (int i = 0; i < incs; ++i) counter.fetch_add(1, std::memory_order_relaxed);\n        });\n    }\n    // WRONG: no join — threads may still be running when the caller reads\n}\n"),
    ("cppa8-release-acquire",
     PUBLISH_BOILER + "\nvoid storePayload(std::atomic<bool>& flag, int& payload, int value) {\n    payload = value;\n    flag.store(true, std::memory_order_release);\n}\nint waitAndRead(std::atomic<bool>& flag, const int& payload) {\n    while (!flag.load(std::memory_order_acquire)) {}\n    return payload;\n}\n",
     PUBLISH_BOILER + "\nvoid storePayload(std::atomic<bool>& flag, int& payload, int value) {\n    flag.store(true, std::memory_order_release);  // WRONG: payload never written\n}\nint waitAndRead(std::atomic<bool>& flag, const int& payload) {\n    while (!flag.load(std::memory_order_acquire)) {}\n    return payload;\n}\n"),
]

write_practice(M8, **M8_PRAC1, challenges=M8_PRAC1_CH, vi_challenges=M8_PRAC1_VI, solutions=M8_PRAC1_SOL)

CH_RELAXED_VS_SEQ = challenge(
    "cppa8-ordering-choice",
    "Choose the Ordering",
    "Implement three functions over one `std::atomic<unsigned>`: `bumpRelaxed` (statistics: relaxed is enough), `publishAndSpin` (release store, acquire load on a bool+int pair), and `seqTotal` (fetch_add with seq_cst, return the previous value).",
    r'''#include <atomic>

// Statistics increment — only atomicity needed.
void bumpRelaxed(std::atomic<unsigned>& counter);

// Publish: set value first, then release the flag.
void publishAndSpin(std::atomic<bool>& flag, int& value, int v);

// Consume: acquire the flag, then read the value.
int consumeAfter(std::atomic<bool>& flag, const int& value);

// seq_cst fetch_add; return the value BEFORE the add.
unsigned seqTotal(std::atomic<unsigned>& counter);
''',
    [
        ("relaxed bump accumulates",
         r'''std::atomic<unsigned> c{0};
for (int i = 0; i < 5; ++i) bumpRelaxed(c);
CHECK_EQ(c.load(), 5u);''',
         "counter.fetch_add(1, std::memory_order_relaxed);"),
        ("publish/consume round-trips",
         r'''std::atomic<bool> f{false};
int v = 0;
publishAndSpin(f, v, 99);
CHECK_EQ(consumeAfter(f, v), 99);''',
         "publishAndSpin: value = v; flag.store(true, std::memory_order_release);  consumeAfter: while (!flag.load(std::memory_order_acquire)) {} return value;"),
        ("seq_cst returns the previous",
         r'''std::atomic<unsigned> s{10};
CHECK_EQ(seqTotal(s), 10u);
CHECK_EQ(seqTotal(s), 11u);
CHECK_EQ(s.load(), 12u);''',
         "return counter.fetch_add(1, std::memory_order_seq_cst); — fetch_add returns the OLD value."),
    ],
    difficulty="advanced",
)

VI_RELAXED_VS_SEQ = vi_challenge(
    "Chọn mức xếp thứ tự",
    "Cài ba hàm trên một `std::atomic<unsigned>`: `bumpRelaxed` (thống kê: relaxed là đủ), `publishAndSpin` (release store, acquire load trên cặp bool+int), và `seqTotal` (fetch_add với seq_cst, trả về giá trị TRƯỚC khi cộng).",
    [
        ("bump relaxed cộng dồn", "counter.fetch_add(1, std::memory_order_relaxed);"),
        ("publish/consume khép kín vòng", "publishAndSpin: value = v; flag.store(true, std::memory_order_release);  consumeAfter: while (!flag.load(std::memory_order_acquire)) {} return value;"),
        ("seq_cst trả giá trị cũ", "return counter.fetch_add(1, std::memory_order_seq_cst); — fetch_add trả về giá trị CŨ."),
    ],
)

M8_PRAC2 = dict(
    sid="m8-ordering-practice",
    title="Ordering Selection",
    description="Relaxed vs acquire/release vs seq_cst on real micro-protocols — the ordering muscle memory.",
    vi_title="Lựa chọn mức xếp thứ tự",
    vi_description="Relaxed so với acquire/release so với seq_cst trên các vi-protocol thật — phản xạ chọn mức.",
    after_lesson=L8B,
    minutes=18,
    difficulty="advanced",
)

M8_PRAC2_CH = [CH_RELAXED_VS_SEQ]
M8_PRAC2_VI = {"cppa8-ordering-choice": VI_RELAXED_VS_SEQ}

M8_PRAC2_SOL = [
    ("cppa8-ordering-choice",
     r'''#include <atomic>

void bumpRelaxed(std::atomic<unsigned>& counter) { counter.fetch_add(1, std::memory_order_relaxed); }
void publishAndSpin(std::atomic<bool>& flag, int& value, int v) {
    value = v;
    flag.store(true, std::memory_order_release);
}
int consumeAfter(std::atomic<bool>& flag, const int& value) {
    while (!flag.load(std::memory_order_acquire)) {}
    return value;
}
unsigned seqTotal(std::atomic<unsigned>& counter) { return counter.fetch_add(1, std::memory_order_seq_cst); }
''',
     r'''#include <atomic>

void bumpRelaxed(std::atomic<unsigned>& counter) { counter.fetch_add(1, std::memory_order_seq_cst); }  // works, but misses the point: not relaxed
void publishAndSpin(std::atomic<bool>& flag, int& value, int v) {
    flag.store(true, std::memory_order_seq_cst);  // WRONG: publishes before the write
    value = v;
}
int consumeAfter(std::atomic<bool>& flag, const int& value) {
    while (!flag.load(std::memory_order_acquire)) {}
    return value;
}
unsigned seqTotal(std::atomic<unsigned>& counter) { return counter.fetch_add(1, std::memory_order_seq_cst) + 1; }  // WRONG: returns post-value
'''),
]

write_practice(M8, **M8_PRAC2, challenges=M8_PRAC2_CH, vi_challenges=M8_PRAC2_VI, solutions=M8_PRAC2_SOL)

# ---- module 8 checkpoint ----
CP8_MD = r'''
The memory-model checkpoint: a thread-safe histogram cell — atomic counting plus a publish/consume reset, all orderings deliberate.
'''

CP8_BOILER = r'''#include <atomic>

// A histogram cell with a lock-free bump and a reset that publishes.
struct Cell {
    std::atomic<unsigned> count{0};
    std::atomic<bool> fresh{false};
    int stamp = 0;   // ordinary int, ordered via fresh

    void bump();                       // +1, relaxed
    unsigned total() const;            // current count
    void reset(int newStamp);          // zero the count, then publish the stamp
    int readStamped();                 // acquire; returns -1 until a reset published
};
'''

write_checkpoint(
    M8, L8D,
    "Checkpoint: Memory Model",
    "Prove deliberate ordering choices on a small concurrent structure.",
    17,
    CP8_MD,
    "Checkpoint: Mô hình bộ nhớ",
    "Chứng minh lựa chọn mức xếp thứ tự có chủ đích trên một cấu trúc đồng thời nhỏ.",
    r'''
Checkpoint mô hình bộ nhớ: một ô histogram thread-safe — đếm atomic cộng với reset kiểu publish/consume, mọi mức đều có chủ đích.
''',
    challenge(
        "cppa8-memmodel-checkpoint",
        "Ordering Gauntlet",
        "Implement the four `Cell` methods with the right orderings: relaxed bump, acquire read, release publish in reset.",
        CP8_BOILER,
        [
            ("bump/total round-trip",
             r'''Cell c;
for (int i = 0; i < 7; ++i) c.bump();
CHECK_EQ(c.total(), 7u);''',
             "void Cell::bump() { count.fetch_add(1, std::memory_order_relaxed); }  unsigned Cell::total() const { return count.load(std::memory_order_relaxed); }"),
            ("reset publishes the stamp",
             r'''Cell c;
CHECK_EQ(c.readStamped(), -1);
for (int i = 0; i < 3; ++i) c.bump();
c.reset(42);
CHECK_EQ(c.readStamped(), 42);
CHECK_EQ(c.total(), 0u);''',
             "reset: count.store(0, relaxed); stamp = newStamp; fresh.store(true, release);  readStamped: while (!fresh.load(acquire)) {} return stamp;"),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại mô hình bộ nhớ",
        "Cài bốn phương thức `Cell` với mức xếp thứ tự đúng: bump relaxed, đọc acquire, publish bằng release trong reset.",
        [
            ("bump/total khép kín", "void Cell::bump() { count.fetch_add(1, std::memory_order_relaxed); }  unsigned Cell::total() const { return count.load(std::memory_order_relaxed); }"),
            ("reset công bố stamp", "reset: count.store(0, relaxed); stamp = newStamp; fresh.store(true, release);  readStamped: while (!fresh.load(acquire)) {} return stamp;"),
        ],
    ),
    solution=CP8_BOILER + "\nvoid Cell::bump() { count.fetch_add(1, std::memory_order_relaxed); }\nunsigned Cell::total() const { return count.load(std::memory_order_relaxed); }\nvoid Cell::reset(int newStamp) {\n    count.store(0, std::memory_order_relaxed);\n    stamp = newStamp;\n    fresh.store(true, std::memory_order_release);\n}\nint Cell::readStamped() {\n    if (!fresh.load(std::memory_order_acquire)) return -1;\n    return stamp;\n}\n",
    wrong=CP8_BOILER + "\nvoid Cell::bump() { count.fetch_add(1, std::memory_order_relaxed); }\nunsigned Cell::total() const { return count.load(std::memory_order_relaxed); }\nvoid Cell::reset(int newStamp) {\n    stamp = newStamp;\n    fresh.store(true, std::memory_order_release);  // WRONG: count never zeroed\n}\nint Cell::readStamped() {\n    if (!fresh.load(std::memory_order_acquire)) return -1;\n    return stamp;\n}\n",
)

# ============================ MODULE 9: concurrency ============================
M9 = "concurrency"

L9A = "threads-jthread"
L9B = "mutex-cv-futures"
L9C = "thread-pool-design"
L9D = "cppa-checkpoint-concurrency"

write_module(
    M9,
    "Advanced Concurrency",
    "Threads, jthread, mutexes, condition variables, futures, and the design of a thread pool — build the plumbing every server owns.",
    "Concurrency Nâng Cao",
    "Thread, jthread, mutex, condition variable, future và thiết kế thread pool — dựng nền móng mà mọi server đều có.",
    [L9A, L9B, L9C, L9D],
    ["m9-threads-practice", "m9-sync-practice"],
)

write_lesson(
    M9, L9A,
    "std::thread, std::jthread, stop_token",
    "Ownership of a thread, automatic joining, and cooperative cancellation — the modern lifecycle.",
    10,
    r'''
## std::thread: you own it

A `std::thread` runs your callable immediately. Forgetting `join()` or `detach()` before destruction calls `std::terminate` — ownership is explicit and unforgiving. Scope threads tightly and join unconditionally.

## std::jthread: the RAII thread (C++20)

`std::jthread` **auto-joins** in its destructor and carries a `std::stop_token` for cooperative cancellation:

```cpp
std::jthread worker([](std::stop_token st) {
    while (!st.stop_requested()) {
        // do a unit of work
    }
});
// ... destructor requests stop AND joins — no terminate on scope exit
```

Cancellation is **cooperative**: the thread decides where checking `stop_requested()` is safe. Nothing preempts your code.

## The graded discipline

Every thread/jthread a function creates must be joined (or handed to an owner that will). The exercises verify by side effects: results written before join, no leaked running threads at scope exit.
''',
    "std::thread, std::jthread, stop_token",
    "Quyền sở hữu thread, tự động join, và hủy hợp tác — vòng đời hiện đại.",
    r'''
## std::thread: bạn sở hữu nó

`std::thread` chạy callable của bạn ngay lập tức. Quên `join()` hay `detach()` trước khi hủy sẽ gọi `std::terminate` — quyền sở hữu tường minh và không khoan nhượng. Giữ thread trong phạm vi hẹp và join vô điều kiện.

## std::jthread: thread RAII (C++20)

`std::jthread` **tự join** trong destructor và mang theo `std::stop_token` để hủy hợp tác:

```cpp
std::jthread worker([](std::stop_token st) {
    while (!st.stop_requested()) {
        // làm một đơn vị công việc
    }
});
// ... destructor yêu cầu stop VÀ join — không terminate khi ra khỏi phạm vi
```

Hủy là **hợp tác**: thread tự quyết định chỗ nào kiểm tra `stop_requested()` là an toàn. Không gì chiếm đoạt code của bạn.

## Kỷ luật được chấm

Mọi thread/jthread mà một hàm tạo ra phải được join (hoặc trao cho một owner sẽ làm việc đó). Các bài tập kiểm chứng bằng hiệu ứng phụ: kết quả được ghi trước join, không thread nào còn chạy khi ra khỏi phạm vi.
''',
    difficulty="advanced",
)

write_lesson(
    M9, L9B,
    "Mutexes, Condition Variables, Futures",
    "Protecting shared state, waking sleepers, and one-shot hand-offs — the three coordination tools.",
    11,
    r'''
## Mutex + RAII guards

`std::mutex` with `std::lock_guard` (scope-locked) or `std::unique_lock` (movable, conditional). The rule: guard construction owns the lock; never call the mutex directly when a guard exists. Shared-read-heavy data wants `std::shared_mutex` with `shared_lock` readers / `unique_lock` writers.

## Condition variables: wait for a state change

```cpp
std::mutex m;
std::condition_variable cv;
bool ready = false;

// waiter
std::unique_lock lk(m);
cv.wait(lk, [] { return ready; });   // releases m while waiting; re-acquires before returning

// notifier
{ std::lock_guard lk(m); ready = true; }
cv.notify_one();
```

The **predicate form** is not optional polish — it guards against lost wakeups and spurious wakeups. Every wait must be predicated; every state change must hold the mutex and notify.

## std::future / std::promise: one-shot hand-off

`std::promise` is the write end, `std::future` the read end of a single value transfer — including exceptions:

```cpp
std::promise<int> p;
std::future<int> f = p.get_future();
std::thread t([&p] { p.set_value(compute()); });
int result = f.get();   // blocks until set — or rethrows the worker's exception
t.join();
```

`std::async` wraps this; `std::packaged_task` wraps a callable. These are for *one-shot* results; a queue of tasks is the thread pool's job (next lesson).
''',
    "Mutex, Condition Variable, Future",
    "Bảo vệ trạng thái chia sẻ, đánh thức người ngủ, và bàn giao một lần — ba công cụ phối hợp.",
    r'''
## Mutex + RAII guard

`std::mutex` với `std::lock_guard` (khóa theo phạm vi) hoặc `std::unique_lock` (di chuyển được, có điều kiện). Quy tắc: construction của guard sở hữu khóa; không bao giờ gọi mutex trực tiếp khi guard còn tồn tại. Dữ liệu đọc-nhiều dùng `std::shared_mutex` với `shared_lock` cho người đọc / `unique_lock` cho người ghi.

## Condition variable: chờ thay đổi trạng thái

```cpp
std::mutex m;
std::condition_variable cv;
bool ready = false;

// người chờ
std::unique_lock lk(m);
cv.wait(lk, [] { return ready; });   // nhả m khi chờ; giữ lại trước khi trả về

// người báo
{ std::lock_guard lk(m); ready = true; }
cv.notify_one();
```

**Dạng vị từ** không phải trang trí — nó chống mất đánh thức và đánh thức giả. Mọi wait phải có vị từ; mọi thay đổi trạng thái phải giữ mutex và notify.

## std::future / std::promise: bàn giao một lần

`std::promise` là đầu ghi, `std::future` là đầu đọc của một lần chuyển giá trị — kể cả ngoại lệ:

```cpp
std::promise<int> p;
std::future<int> f = p.get_future();
std::thread t([&p] { p.set_value(compute()); });
int result = f.get();   // chặn cho tới khi set — hoặc ném lại ngoại lệ của worker
t.join();
```

`std::async` bọc cơ chế này; `std::packaged_task` bọc một callable. Chúng phục vụ *kết quả một lần*; hàng đợi công việc là việc của thread pool (bài kế tiếp).
''',
    difficulty="advanced",
)

write_lesson(
    M9, L9C,
    "Designing a Thread Pool",
    "The workhorse of every server: a task queue, N workers, and a clean shutdown. Design decisions before code.",
    12,
    r'''
## The anatomy

1. **Task queue** — `std::deque<std::function<void()>>` under a mutex, with a `condition_variable` to wake idle workers,
2. **Workers** — N threads looping: wait for a task, run it, repeat,
3. **Shutdown** — a `stopping` flag; workers drain or abandon the queue per policy, then exit.

```cpp
class ThreadPool {
public:
    explicit ThreadPool(std::size_t n);
    void submit(std::function<void()> f);   // enqueue + notify_one
    ~ThreadPool();                          // set stopping, notify_all, join all
};
```

## The design decisions that matter

- **Backpressure**: unbounded queues hide overload until memory dies. Production pools bound the queue or shed load.
- **Worker count**: ~hardware_concurrency for CPU-bound work; more for I/O-bound. Measure, never guess (Module 11).
- **Futures on submit**: production `submit` returns `std::future<T>` via `std::packaged_task` so callers get results *and* exceptions. The graded build does exactly this.
- **Exception safety**: a task that throws must not kill a worker — `packaged_task` captures the exception into the future; a bare loop must catch.

## The graded build

You will implement a small pool with future-returning submit and graceful shutdown, then verify: all tasks run, results are correct, exceptions surface through futures, and the destructor joins cleanly.
''',
    "Thiết Kế Thread Pool",
    "Lao động chính của mọi server: hàng đợi công việc, N worker, và tắt máy sạch sẽ. Quyết định thiết kế trước code.",
    r'''
## Giải phẫu

1. **Hàng đợi công việc** — `std::deque<std::function<void()>>` dưới một mutex, với `condition_variable` đánh thức worker rảnh,
2. **Worker** — N thread lặp: chờ công việc, chạy, lặp lại,
3. **Tắt máy** — cờ `stopping`; worker rút cạn hoặc bỏ hàng đợi tùy chính sách, rồi thoát.

```cpp
class ThreadPool {
public:
    explicit ThreadPool(std::size_t n);
    void submit(std::function<void()> f);   // enqueue + notify_one
    ~ThreadPool();                          // bật stopping, notify_all, join tất cả
};
```

## Những quyết định thiết kế quan trọng

- **Backpressure**: hàng đợi vô hạn che giấu quá tải cho tới khi bộ nhớ chết. Pool production giới hạn hàng đợi hoặc vứt bớt việc.
- **Số worker**: xấp xỉ hardware_concurrency cho việc nặng CPU; nhiều hơn cho việc nặng I/O. Đo, đừng đoán (Module 11).
- **submit trả future**: production `submit` trả `std::future<T>` qua `std::packaged_task` để caller nhận cả kết quả lẫn ngoại lệ. Bản được chấm làm đúng như vậy.
- **An toàn ngoại lệ**: task ném ngoại lệ không được giết worker — `packaged_task` bắt ngoại lệ vào future; vòng lặp trần phải bắt.

## Bản được chấm

Bạn sẽ cài một pool nhỏ với submit trả future và tắt máy êm, rồi kiểm chứng: mọi task chạy, kết quả đúng, ngoại lệ lộ ra qua future, và destructor join sạch sẽ.
''',
    difficulty="advanced",
)

# ---- module 9 practices ----
SUM_BOILER = r'''#include <atomic>
#include <numeric>
#include <thread>
#include <vector>

// Sum [0, n) using nThreads threads splitting the range evenly.
long long parallelSum(int n, int nThreads);
'''

CH_PARALLEL_SUM = challenge(
    "cppa9-parallel-sum",
    "Split, Spawn, Join",
    "Implement `parallelSum`: split [0, n) into nThreads contiguous chunks, sum each chunk on its own std::thread into a shared atomic, join everything, return the total.",
    SUM_BOILER,
    [
        ("even split sums exactly",
         r'''CHECK_EQ(parallelSum(1000, 4), 1000LL * 999 / 2);
CHECK_EQ(parallelSum(10, 3), 45);''',
         "Chunk [lo, hi) per thread: lo = i * n / nThreads, hi = (i+1) * n / nThreads — the rounding splits contiguously without gaps or overlap."),
        ("more threads than elements",
         r'''CHECK_EQ(parallelSum(2, 8), 1);''',
         "Empty chunks (lo == hi) must simply add 0 — never spawn on an empty range or guard the loop."),
    ],
    difficulty="advanced",
)

VI_PARALLEL_SUM = vi_challenge(
    "Chia, tạo, join",
    "Cài `parallelSum`: chia [0, n) thành nThreads đoạn liền kề, cộng từng đoạn trên std::thread riêng vào một atomic chia sẻ, join tất cả, trả tổng.",
    [
        ("chia đều cộng chính xác", "Đoạn [lo, hi) mỗi thread: lo = i * n / nThreads, hi = (i+1) * n / nThreads — phép làm tròn chia liền kề, không hụt không chồng."),
        ("nhiều thread hơn phần tử", "Đoạn rỗng (lo == hi) chỉ cần cộng 0 — đừng tạo thread trên đoạn rỗng hoặc bảo vệ vòng lặp."),
    ],
)

CH_CV_PRODUCER = challenge(
    "cppa9-cv-handoff",
    "Condition-Variable Handoff",
    "Implement a one-slot mailbox: `put` stores a value under the mutex and notifies; `take` waits (predicated) until a value is present, removes and returns it.",
    r'''#include <condition_variable>
#include <chrono>
#include <deque>
#include <mutex>
#include <optional>
#include <thread>

class Mailbox {
public:
    void put(int v);       // store + notify_one
    int take();            // wait until present, then remove & return
    bool empty() const;
private:
    mutable std::mutex m_;
    std::condition_variable cv_;
    std::deque<int> q_;
};
''',
    [
        ("take blocks until put",
         r'''Mailbox box;
std::thread t([&box] { std::this_thread::sleep_for(std::chrono::milliseconds(20)); box.put(7); });
CHECK_EQ(box.take(), 7);
t.join();''',
         "put: { std::lock_guard lk(m_); q_.push_back(v); } cv_.notify_one();  take: std::unique_lock lk(m_); cv_.wait(lk, [this]{ return !q_.empty(); }); int v = q_.front(); q_.pop_front(); return v;"),
        ("fifo across two puts",
         r'''Mailbox box;
box.put(1);
box.put(2);
CHECK_EQ(box.take(), 1);
CHECK_EQ(box.take(), 2);''',
         "A waiting take re-checks the predicate after every wakeup — two puts mean two successful takes in order."),
    ],
    difficulty="advanced",
)

VI_CV_PRODUCER = vi_challenge(
    "Bàn giao bằng condition variable",
    "Cài hộp thư một ô: `put` lưu giá trị dưới mutex và notify; `take` chờ (có vị từ) tới khi có giá trị, lấy ra và trả về.",
    [
        ("take chặn cho tới khi put", "put: { std::lock_guard lk(m_); q_.push_back(v); } cv_.notify_one();  take: std::unique_lock lk(m_); cv_.wait(lk, [this]{ return !q_.empty(); }); int v = q_.front(); q_.pop_front(); return v;"),
        ("fifo qua hai lần put", "take đang chờ kiểm tra lại vị từ sau mỗi lần đánh thức — hai put nghĩa là hai take thành công đúng thứ tự."),
    ],
)

CH_FUTURE_ROUNDTRIP = challenge(
    "cppa9-future-roundtrip",
    "Promise/Future Across Threads",
    "Implement `runWithResult(std::function<int()>)`: run the callable on a fresh std::thread, deliver its result through a promise/future, join the thread, and return the result.",
    r'''#include <functional>
#include <future>
#include <thread>

int runWithResult(std::function<int()> fn);
''',
    [
        ("result crosses the thread",
         r'''CHECK_EQ(runWithResult([] { return 6 * 7; }), 42);''',
         "std::promise<int> p; auto fut = p.get_future(); std::thread t([&p, &fn] { p.set_value(fn()); }); int r = fut.get(); t.join(); return r;"),
        ("futures compose sequentially",
         r'''int doubled = runWithResult([] { return 21; }) * 2;
CHECK_EQ(doubled, 42);''',
         "Each call is independent — the future.get() blocks only until that worker finishes."),
    ],
    difficulty="advanced",
)

VI_FUTURE_ROUNDTRIP = vi_challenge(
    "Promise/Future qua các thread",
    "Cài `runWithResult(std::function<int()>)`: chạy callable trên một std::thread mới, chuyển kết quả qua promise/future, join thread, và trả kết quả.",
    [
        ("kết quả băng qua thread", "std::promise<int> p; auto fut = p.get_future(); std::thread t([&p, &fn] { p.set_value(fn()); }); int r = fut.get(); t.join(); return r;"),
        ("future kết hợp tuần tự", "Mỗi lời gọi độc lập — future.get() chỉ chặn cho tới khi worker đó xong."),
    ],
)

M9_PRAC1 = dict(
    sid="m9-threads-practice",
    title="Threads That Behave",
    description="Deterministic splitting/joining and a cross-thread result — the thread lifecycle drilled.",
    vi_title="Thread biết điều",
    vi_description="Chia/join tất định và kết quả băng qua thread — luyện vòng đời thread.",
    after_lesson=L9A,
    minutes=20,
    difficulty="advanced",
)

M9_PRAC1_CH = [CH_PARALLEL_SUM, CH_FUTURE_ROUNDTRIP]
M9_PRAC1_VI = {"cppa9-parallel-sum": VI_PARALLEL_SUM,
               "cppa9-future-roundtrip": VI_FUTURE_ROUNDTRIP}

M9_PRAC1_SOL = [
    ("cppa9-parallel-sum",
     SUM_BOILER + "\nlong long parallelSum(int n, int nThreads) {\n    std::atomic<long long> total{0};\n    std::vector<std::thread> ts;\n    for (int i = 0; i < nThreads; ++i) {\n        int lo = (int)((long long)i * n / nThreads);\n        int hi = (int)((long long)(i + 1) * n / nThreads);\n        ts.emplace_back([lo, hi, &total] {\n            long long s = 0;\n            for (int x = lo; x < hi; ++x) s += x;\n            total.fetch_add(s, std::memory_order_relaxed);\n        });\n    }\n    for (auto& t : ts) t.join();\n    return total.load();\n}\n",
     SUM_BOILER + "\nlong long parallelSum(int n, int nThreads) {\n    std::atomic<long long> total{0};\n    std::vector<std::thread> ts;\n    for (int i = 0; i < nThreads; ++i) {\n        int lo = (int)((long long)i * n / nThreads);\n        int hi = (int)((long long)(i + 1) * n / nThreads);\n        ts.emplace_back([lo, hi, &total] {\n            long long s = 0;\n            for (int x = lo; x < hi; ++x) s += x;\n            total.fetch_add(s, std::memory_order_relaxed);\n        });\n    }\n    return total.load();  // WRONG: no join — reads before workers finish\n}\n"),
    ("cppa9-future-roundtrip",
     r'''#include <functional>
#include <future>
#include <thread>

int runWithResult(std::function<int()> fn) {
    std::promise<int> p;
    auto fut = p.get_future();
    std::thread t([&p, &fn] {
        p.set_value(fn());
    });
    int r = fut.get();
    t.join();
    return r;
}
''',
     r'''#include <functional>
#include <future>
#include <thread>

int runWithResult(std::function<int()> fn) {
    std::promise<int> p;
    auto fut = p.get_future();
    std::thread t([&p, &fn] {
        p.set_value(fn());
    });
    return fut.get();  // WRONG: thread never joined before return (and fut.get() races the join-less scope exit)
}
'''),
]

write_practice(M9, **M9_PRAC1, challenges=M9_PRAC1_CH, vi_challenges=M9_PRAC1_VI, solutions=M9_PRAC1_SOL)

M9_PRAC2 = dict(
    sid="m9-sync-practice",
    title="Coordination Primitives",
    description="The predicated condition-variable handoff and shared-state discipline.",
    vi_title="Primitive phối hợp",
    vi_description="Bàn giao condition-variable có vị từ và kỷ luật trạng thái chia sẻ.",
    after_lesson=L9B,
    minutes=18,
    difficulty="advanced",
)

M9_PRAC2_CH = [CH_CV_PRODUCER]
M9_PRAC2_VI = {"cppa9-cv-handoff": VI_CV_PRODUCER}

M9_PRAC2_SOL = [
    ("cppa9-cv-handoff",
     CH_CV_PRODUCER["boilerplate"] + r'''void Mailbox::put(int v) {
    {
        std::lock_guard<std::mutex> lk(m_);
        q_.push_back(v);
    }
    cv_.notify_one();
}
int Mailbox::take() {
    std::unique_lock<std::mutex> lk(m_);
    cv_.wait(lk, [this] { return !q_.empty(); });
    int v = q_.front();
    q_.pop_front();
    return v;
}
bool Mailbox::empty() const {
    std::lock_guard<std::mutex> lk(m_);
    return q_.empty();
}
''',
     r'''#include <condition_variable>
#include <mutex>
#include <optional>

void Mailbox::put(int v) {
    q_;                     // WRONG: value never enqueued
    cv_.notify_one();
}
int Mailbox::take() {
    std::unique_lock<std::mutex> lk(m_);
    cv_.wait(lk);           // WRONG: no predicate — lost/spurious wakeups
    int v = *slot_;
    slot_.reset();
    return v;
}
bool Mailbox::empty() const {
    std::lock_guard<std::mutex> lk(m_);
    return q_.empty();
}
'''),
]

write_practice(M9, **M9_PRAC2, challenges=M9_PRAC2_CH, vi_challenges=M9_PRAC2_VI, solutions=M9_PRAC2_SOL)

# ---- module 9 checkpoint ----
CP9_MD = r'''
The concurrency checkpoint: a two-slot pipeline stage — inbox + outbox mailboxes driven by a worker thread.
'''

CP9_BOILER = r'''#include <condition_variable>
#include <deque>
#include <mutex>
#include <optional>
#include <thread>

// A worker that moves values from inbox to outbox, transformed by +delta,
// until the inbox closes (sentinel -1 means close).
class Stage {
public:
    Stage(int delta);
    void put(int v);       // inbox push (sentinel -1 closes)
    int take();            // outbox pop (blocks)
    void run();            // the worker loop (called on its own thread by tests)
private:
    int delta_;
    std::deque<int> in_;                  // inbox queue
    std::deque<int> out_;                 // outbox queue
    std::mutex m_;                        // guards in_
    std::mutex om_;                       // guards out_
    std::condition_variable inCv_;        // signaled when in_ becomes non-empty
    std::condition_variable oCv_;         // signaled when out_ becomes non-empty
};
'''

write_checkpoint(
    M9, L9D,
    "Checkpoint: Concurrency",
    "Prove thread + mutex + condition-variable choreography on a transforming stage.",
    20,
    CP9_MD,
    "Checkpoint: Concurrency",
    "Chứng minh kỹ choreography thread + mutex + condition variable trên một stage biến đổi dữ liệu.",
    r'''
Checkpoint concurrency: một stage hai ô — inbox + outbox được worker thread dẫn dắt.
''',
    challenge(
        "cppa9-concurrency-checkpoint",
        "Pipeline Stage Gauntlet",
        "Implement `Stage`: `put` feeds the inbox (value -1 closes it), `run` moves inbox values (+delta) to the outbox until closed, `take` blocks for outbox values.",
        CP9_BOILER,
        [
            ("values transform and flow",
             r'''Stage s{100};
std::thread t([&s] { s.run(); });
s.put(1);
s.put(2);
s.put(-1);
CHECK_EQ(s.take(), 101);
CHECK_EQ(s.take(), 102);
t.join();''',
             "Two mailbox slots (each mutex+cv+optional): run loops taking from inbox (waiting predicated), breaking on -1, otherwise pushing value+delta to outbox and notifying."),
            ("late take blocks until value",
             r'''Stage s{5};
std::thread feeder([&s] {
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    s.put(3);
    s.put(-1);
});
std::thread worker([&s] { s.run(); });
CHECK_EQ(s.take(), 8);
feeder.join();
worker.join();''',
             "take waits on the outbox condition variable with a predicate — the timing skew must not matter."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại pipeline stage",
        "Cài `Stage`: `put` nạp inbox (giá trị -1 đóng), `run` chuyển giá trị inbox (+delta) sang outbox cho tới khi đóng, `take` chặn chờ giá trị outbox.",
        [
            ("giá trị biến đổi và chảy", "Hai ô mailbox (mỗi ô mutex+cv+optional): run lặp lấy từ inbox (chờ có vị từ), thoát khi gặp -1, nếu không đẩy giá trị+delta vào outbox và notify."),
            ("take muộn vẫn chặn chờ", "take chờ trên condition variable của outbox có vị từ — lệch thời điểm không được làm sai."),
        ],
    ),
    solution=CP9_BOILER + r'''
Stage::Stage(int delta) : delta_(delta) {}
void Stage::put(int v) {
    { std::lock_guard<std::mutex> lk(m_); in_.push_back(v); } inCv_.notify_one();
}
int Stage::take() {
    std::unique_lock<std::mutex> lk(om_);
    oCv_.wait(lk, [this] { return !out_.empty(); });
    int v = out_.front();
    out_.pop_front();
    return v;
}
void Stage::run() {
    while (true) {
        int v;
        { std::unique_lock<std::mutex> lk(m_); inCv_.wait(lk, [this]{ return !in_.empty(); }); v = in_.front(); in_.pop_front(); }
        if (v == -1) break;
        { std::lock_guard<std::mutex> lk(om_); out_.push_back(v + delta_); } oCv_.notify_one();
    }
}
''',
    wrong=CP9_BOILER + r'''
void Stage::put(int v) {
    if (v == -1) { return; }  // WRONG: bypasses the inbox entirely
    { std::lock_guard<std::mutex> lk(om_); out_.push_back(v); }  // WRONG: raw value straight to the outbox
    oCv_.notify_one();
}
int Stage::take() {
    std::unique_lock<std::mutex> lk(om_);
    oCv_.wait(lk, [this] { return !out_.empty(); });
    int v = out_.front();
    out_.pop_front();
    return v;
}
void Stage::run() {
    while (true) {
        int v;
        { std::unique_lock<std::mutex> lk(m_); inCv_.wait(lk, [this]{ return !in_.empty(); }); v = in_.front(); in_.pop_front(); }
        if (v == -1) break;
        { std::lock_guard<std::mutex> lk(om_); out_.push_back(v + delta_); } oCv_.notify_one();
    }
}
''',
)

print("modules 8-9 done")
