#!/usr/bin/env python3
"""C++ Advanced — module 10 (memory-allocators) and module 11 (performance)."""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 10: memory-allocators ============================
M10 = "memory-allocators"

L10A = "allocation-costs"
L10B = "pmr-and-arenas"
L10C = "data-oriented-layout"
L10D = "cppa-checkpoint-allocators"

write_module(
    M10,
    "Memory Architecture & Allocators",
    "Where allocations really cost, how pmr arenas reshape ownership, and why data layout beats micro-optimization.",
    "Kiến trúc Bộ nhớ & Allocator",
    "Phép cấp phát thực sự tốn ở đâu, arena pmr định hình ownership thế nào, và tại sao bố trí dữ liệu đánh bại tối ưu vi mô.",
    [L10A, L10B, L10C, L10D],
    ["m10-pool-practice", "m10-pmr-practice"],
)

write_lesson(
    M10, L10A,
    "The Real Cost of new",
    "Allocation is not one cost: it is lookup, fragmentation, cache misses, and deallocation — measured, not guessed.",
    11,
    r'''
## What a heap allocation actually does

`new T[n]` asks the allocator for n*sizeof(T) bytes. Depending on the allocator that means: a size-class lookup, possibly a lock, possibly an OS syscall (mmap/sbrk), and metadata bookkeeping. The *CPU cost* is real but the *hidden* cost is bigger: a fresh allocation is a cache-cold object, and vectors that reallocate move or copy every element.

## The four costs, in order of pain

1. **Latency** — tens of ns hot, hundreds cold, microseconds if the OS gets involved.
2. **Fragmentation** — many small allocations with random lifetimes fragment the heap; footprint grows even when live bytes don't.
3. **Cache misses** — pointer-chasing into scattered nodes can cost 100+ cycles per hop.
4. **Deallocation** — free also costs, and per-object free of millions of elements is measurable.

## The beginner-advanced shift

Beginners ask "is new slow?" — unanswerable. Advanced engineers ask: *how many allocations per operation, what sizes, what lifetimes?* Then they count. `malloc_count`-style counters (like the one in this module's practice) make allocation behavior a testable property.

## Lifetime structure beats cleverness

If 10,000 objects live and die together, one arena allocation + one free replaces 20,000 ops. If a hot loop allocates per iteration, hoisting the buffer out of the loop is usually the whole fix. Object pools pay off when object lifetimes interleave unpredictably but sizes are uniform.
''',
    "Chi Phí Thực Sự của new",
    "Cấp phát không phải một chi phí: là tra tìm, phân mảnh, cache miss, và giải phóng — đo đếm, không phỏng đoán.",
    r'''
## Một phép cấp phát heap thực sự làm gì

`new T[n]` xin bộ cấp phát n*sizeof(T) byte. Tùy bộ cấp phát: tra tìm size-class, có thể khóa, có thể gọi hệ điều hành (mmap/sbrk), và ghi sổ metadata. *Chi phí CPU* là có thật nhưng *chi phí ẩn* lớn hơn: đối tượng mới cấp phát là đối tượng lạnh cache, và vector reallocate thì di chuyển hoặc sao chép mọi phần tử.

## Bốn loại chi phí, theo mức đau

1. **Độ trễ** — chục ns khi nóng, trăm ns khi lạnh, microsecond nếu OS nhúng tay.
2. **Phân mảnh** — nhiều cấp phát nhỏ với thời điểm sống ngẫu nhiên làm phân mảnh heap; dung lượng tăng dù byte sống không tăng.
3. **Cache miss** — đuổi con trỏ qua các node rải rác có thể tốn 100+ chu kỳ mỗi bước.
4. **Giải phóng** — free cũng tốn, và free từng đối tượng với hàng triệu phần tử là đo được.

## Bước nhảy từ beginner sang advanced

Người mới hỏi "new có chậm không?" — không trả lời được. Kỹ sư advanced hỏi: *mỗi thao tác cấp phát bao nhiêu lần, kích thước nào, thời điểm sống ra sao?* Rồi họ đếm. Bộ đếm kiểu `malloc_count` (như trong bài tập module này) biến hành vi cấp phát thành thuộc tính kiểm thử được.

## Cấu trúc thời điểm sống đánh bài sự khéo léo

Nếu 10.000 đối tượng sống và chết cùng nhau: một lần cấp phát arena + một lần free thay cho 20.000 thao tác. Nếu vòng lặp nóng cấp phát mỗi vòng, kéo buffer ra ngoài vòng lặp thường là cả bài tối ưu. Object pool có lợi khi thời điểm sống đan xen khó đoán nhưng kích thước đồng nhất.
''',
    difficulty="advanced",
)

write_lesson(
    M10, L10B,
    "std::pmr, Arenas, and Monotonic Buffers",
    "Polymorphic allocators make allocation strategy a runtime choice; monotonic_buffer_resource is the workhorse arena.",
    12,
    r'''
## The pmr idea

`std::pmr::memory_resource` is an interface with `do_allocate/do_deallocate`. Containers take an allocator argument: `std::pmr::vector<int> v{&resource};` Now *who owns memory and how it is carved* is a runtime, composable decision — no template recompilation per strategy.

## monotonic_buffer_resource: the arena

Grows forward, deallocate is a no-op, everything is freed when the resource dies:

```cpp
char buf[64 * 1024];
std::pmr::monotonic_buffer_resource arena(buf, sizeof(buf));
std::pmr::vector<std::pmr::string> rows{&arena};
rows.emplace_back("alpha");   // string + vector both allocate from the arena
```

Perfect for request-shaped work: parse, compute, drop. O(1) amortized bump allocation, zero per-object frees, perfect locality for small data.

## upstream and fallback chains

`pmr::new_delete_resource()` is the default upstream. `synchronized_pool_resource` pools small blocks. Nesting a pool over a monotonic buffer over the heap gives you: fast small-object reuse, arena reset, and OS fallback — in one declarative chain.

## When NOT to pmr

Single long-lived objects gain nothing. Objects whose lifetime outlives the arena are a use-after-free waiting to happen — the resource must outlive or be reset in lockstep with everything allocated from it.
''',
    "std::pmr, Arena, và Monotonic Buffer",
    "Allocator đa hình biến chiến lược cấp phát thành lựa chọn runtime; monotonic_buffer_resource là arena chủ lực.",
    r'''
## Ý tưởng pmr

`std::pmr::memory_resource` là một interface với `do_allocate/do_deallocate`. Container nhận allocator: `std::pmr::vector<int> v{&resource};` Giờ *ai sở hữu bộ nhớ và cách carve* là quyết định runtime, có thể kết hợp — không cần biên dịch lại template theo từng chiến lược.

## monotonic_buffer_resource: arena

Tăng dần về phía trước, deallocate là no-op, mọi thứ được giải phóng khi resource chết:

```cpp
char buf[64 * 1024];
std::pmr::monotonic_buffer_resource arena(buf, sizeof(buf));
std::pmr::vector<std::pmr::string> rows{&arena};
rows.emplace_back("alpha");   // string + vector đều cấp phát từ arena
```

Hoàn hảo cho công việc dạng request: parse, tính toán, vứt. Cấp phát bump O(1) khấu trừ, không free từng đối tượng, locality hoàn hảo với dữ liệu nhỏ.

## Chuỗi upstream và fallback

`pmr::new_delete_resource()` là upstream mặc định. `synchronized_pool_resource` gộp khối nhỏ. Lồng pool trên monotonic buffer trên heap cho bạn: tái sử dụng đối tượng nhỏ nhanh, reset arena, và fallback về OS — trong một chuỗi khai báo.

## Khi KHÔNG nên pmr

Đối tượng đơn sống lâu không được lợi gì. Đối tượng sống lâu hơn arena là use-after-free chờ xảy ra — resource phải sống lâu hơn hoặc được reset đồng bộ với mọi thứ đã cấp phát từ nó.
''',
    difficulty="advanced",
)

write_lesson(
    M10, L10C,
    "Data-Oriented Design",
    "Organize data for how it is accessed, not how it is modeled: structure-of-arrays, hot/cold splitting, and allocation-free hot paths.",
    12,
    r'''
## The cache is the machine

A modern core executes 4+ instructions/cycle but a main-memory miss costs ~100 cycles. The layout of your data decides how often that happens. Two programs with identical big-O can differ 10x purely by layout.

## AoS vs SoA

Array-of-structs: `struct P { float x, y, z; bool active; };  std::vector<P> ps;` — updating only x drags every cache line through y, z, active. Struct-of-arrays: `struct Ps { std::vector<float> x, y, z; std::vector<char> active; };` — the x-update loop streams only x. If your hot loop touches a subset of fields, SoA wins. If it always touches whole records, AoS is fine.

## Hot/cold splitting

Fields accessed on every iteration belong together; fields touched once per thousand iterations belong elsewhere. Splitting `active` flags out of 64-byte records turns a scans-everything loop into a scan of a bitmap.

## The hot path contract

Advanced codebases make the hot path *allocation-free and branch-stable*: preallocated buffers, indices instead of pointers, reserved vectors. The graded exercises here make this measurable: allocation counters and cache-detectable stride patterns — no microbenchmarks needed.
''',
    "Data-Oriented Design",
    "Tổ chức dữ liệu theo cách nó được truy cập, không phải theo cách nó được mô hình hóa: structure-of-arrays, tách nóng/lạnh, và đường nóng không cấp phát.",
    r'''
## Cache mới là cái máy

Một core hiện đại thực thi 4+ lệnh/chu kỳ nhưng một lần miss tới bộ nhớ chính tốn ~100 chu kỳ. Bố trí dữ liệu quyết định tần suất điều đó xảy ra. Hai chương trình cùng big-O có thể khác nhau 10 lần thuần vì bố trí.

## AoS vs SoA

Array-of-structs: `struct P { float x, y, z; bool active; };  std::vector<P> ps;` — chỉ cập nhật x vẫn kéo cả cache line qua y, z, active. Struct-of-arrays: `struct Ps { std::vector<float> x, y, z; std::vector<char> active; };` — vòng lặp cập nhật x chỉ đọc duy nhất x. Nếu vòng nóng chỉ đụng một tập trường con, SoA thắng. Nếu luôn đụng cả bản ghi, AoS ổn.

## Tách nóng/lạnh

Trường dùng mỗi vòng lặp nên nằm cạnh nhau; trường dùng mỗi nghìn vòng nên nằm chỗ khác. Tách cờ `active` khỏi bản ghi 64-byte biến việc quét-tất-cả thành quét bitmap.

## Hợp đồng đường nóng

Codebase advanced biến đường nóng thành *không cấp phát và nhánh ổn định*: buffer cấp phát sẵn, chỉ số thay vì con trỏ, vector đã reserve. Các bài tập ở đây làm điều này đo được: bộ đếm cấp phát và mẫu stride nhận ra được qua cache — không cần microbenchmark.
''',
    difficulty="advanced",
)

# ---- module 10 checkpoint mdx ----
CP10_MD = r'''
Checkpoint on memory architecture: pool reuse counted by an allocation tracker, and an arena that must carve and reset cleanly.
'''

CP10_BOILER = r'''#include <cstddef>
#include <cstdint>
#include <vector>

// Deterministic allocation tracker the tests drive.
// (No real heap calls: the challenge models allocation behavior.)
class AllocTracker {
public:
    static int& allocs()   { static int n = 0; return n; }
    static int& frees()    { static int n = 0; return n; }
    static int& live()     { static int n = 0; return n; }
    static void noteAlloc(){ ++allocs(); ++live(); }
    static void noteFree() { ++frees(); --live(); }
    static void reset()    { allocs() = frees() = live() = 0; }
};

// A fixed-size pool of 'blocks' blocks of 'blockSize' bytes.
// acquire() returns a byte pointer or nullptr when exhausted;
// release(p) returns the block to the pool (p must be from this pool).
class BytePool {
public:
    BytePool(std::size_t blocks, std::size_t blockSize);
    ~BytePool();
    std::uint8_t* acquire();          // AllocTracker::noteAlloc() on success
    void release(std::uint8_t* p);    // AllocTracker::noteFree() on success
    std::size_t available() const;
private:
    std::size_t blocks_, blockSize_;
    std::uint8_t* storage_ = nullptr;   // your bookkeeping here
    std::vector<std::uint8_t*> freeList_;
};
'''

# ---- module 11: performance ----
M11 = "performance"

L11A = "cppa-measure-first"
L11B = "hot-path-optimization"
L11C = "compiler-and-layout"
L11D = "cppa-checkpoint-perf"

write_module(
    M11,
    "Performance Engineering",
    "Measure first, optimize with evidence: allocation counts, stride costs, and algorithmic wins verified by deterministic graders.",
    "Kỹ thuật Hiệu năng",
    "Đo trước, tối ưu bằng bằng chứng: số lần cấp phát, chi phí stride, và thắng lợi thuật toán được grader tất định xác minh.",
    [L11A, L11B, L11C, L11D],
    ["m11-alloc-practice", "m11-alg-practice"],
)

write_lesson(
    M11, L11A,
    "Measure First, Optimize Second",
    "Guesswork optimizes the wrong 3%. Counting allocations, operations, and data movement turns performance into evidence.",
    11,
    r'''
## The method

1. Establish a baseline with a *metric*, not a feeling.
2. Form one hypothesis ("the per-call allocation dominates").
3. Change one thing.
4. Re-measure the same metric.
5. Keep or revert — with numbers.

Wall-clock microbenchmarks are noisy and machine-dependent; this course grades the *countable* proxies professionals extract from profilers: allocation counts, bytes moved, comparisons, branch divergence detectable via deterministic patterns.

## Where C++ programs actually lose time

In rough order of frequency: unnecessary copies (strings, vectors), unnecessary allocations (per-iteration buffers), wrong data layout (pointer chasing), wrong algorithm (O(n log n) vs O(n)), and only *then* micro-stuff like branch order.

## Amdahl's law keeps you honest

If the sort is 90% of runtime, a 2x faster string format changes little. Profile-guided intuition: find the hot 10%, then optimize only inside it.
''',
    "Đo Trước, Tối Ưu Sau",
    "Phỏng đoán tối ưu sai 3% quan trọng nhất. Đếm cấp phát, thao tác, và dữ liệu di chuyển biến hiệu năng thành bằng chứng.",
    r'''
## Phương pháp

1. Thiết lập baseline bằng *chỉ số*, không phải cảm giác.
2. Đặt một giả thuyết ("cấp phát mỗi lần gọi là chiếm ưu thế").
3. Thay đổi đúng một thứ.
4. Đo lại cùng một chỉ số.
5. Giữ hoặc hoàn tác — kèm con số.

Microbenchmark đo thời gian thực nhiễu và phụ thuộc máy; khóa học này chấm các *proxy đếm được* mà kỹ sư trích từ profiler: số lần cấp phát, byte di chuyển, số phép so sánh, phân kỳ nhánh nhận ra được qua mẫu tất định.

## Chương trình C++ thực sự mất thời gian ở đâu

Theo tần suất: bản sao không cần thiết (string, vector), cấp phát không cần thiết (buffer mỗi vòng), bố trí dữ liệu sai (đuổi con trỏ), thuật toán sai (O(n log n) thay vì O(n)), rồi mới tới chuyện vi mô như thứ tự nhánh.

## Định luật Amdahl giữ bạn trung thực

Nếu sort chiếm 90% runtime, làm string format nhanh gấp 2 thay đổi rất ít. Trực giác kiểu profiler: tìm 10% nóng, rồi chỉ tối ưu bên trong đó.
''',
    difficulty="advanced",
)

write_lesson(
    M11, L11B,
    "The Hot Path: Allocation-Free and Copy-Free",
    "Reserve, reuse, move, and stringify once — the four habits that remove most runtime cost before touching the compiler flags.",
    11,
    r'''
## Reserve before you grow

`std::vector` doubling causes log(n) reallocations, each moving every element. `reserve(n)` up front makes the hot loop allocation-free. Allocation counters (like this module's) catch offenders instantly.

## Reuse buffers across iterations

A buffer allocated inside a loop is a per-iteration tax. Hoist it to the caller, pass by reference, clear with `clear()` (keeps capacity).

## Move, don't copy

`std::move` for last-use values, `emplace_back` in-place construction, and returning by value (RVO makes it free). A wrong `push_back(x)` where `push_back(std::move(x))` was meant costs a full deep copy per element.

## Copy strings once

Repeated concatenation in a loop is quadratic. Build with `reserve` + `append`, or accumulate into a single buffer. The graded exercises here count both allocations and byte-copies, so the quadratic version fails by arithmetic, not by opinion.
''',
    "Đường Nóng: Không Cấp Phát và Không Sao Chép",
    "Reserve, tái sử dụng, move, và string hóa một lần — bốn thói quen xóa phần lớn chi phí runtime trước cả khi đụng vào cờ trình biên dịch.",
    r'''
## Reserve trước khi lớn lên

`std::vector` nhân đôi gây log(n) lần reallocate, mỗi lần di chuyển mọi phần tử. `reserve(n)` từ đầu biến vòng nóng thành không cấp phát. Bộ đếm cấp phát (như của module này) bắt thủ phạm ngay lập tức.

## Tái sử dụng buffer giữa các vòng

Buffer cấp phát bên trong vòng lặp là thuế mỗi vòng. Kéo nó ra caller, truyền bằng tham chiếu, xóa bằng `clear()` (giữ capacity).

## Move, đừng copy

`std::move` cho giá trị lần-dùng-cuối, `emplace_back` để dựng tại chỗ, và trả về bằng giá trị (RVO làm nó miễn phí). Một `push_back(x)` sai chỗ cần `push_back(std::move(x))` tốn một bản sao sâu cho mỗi phần tử.

## Copy string một lần

Nối chuỗi lặp lại trong vòng lặp là cấp số nhân. Dựng bằng `reserve` + `append`, hoặc cộng dồn vào một buffer. Các bài tập chấm điểm ở đây đếm cả cấp phát lẫn byte-copy, nên bản cấp số nhân trượt bởi toán học, không phải ý kiến.
''',
    difficulty="advanced",
)

write_lesson(
    M11, L11C,
    "Compiler Flags, Layout, and the Machine",
    "What -O2 actually assumes, why layout beats micro-opts, and how the same source gets faster by data arrangement.",
    10,
    r'''
## What the optimizer may and may not do

At `-O2` the compiler assumes no undefined behavior: signed overflow won't happen, pointers won't alias `char` buffers illegally, in-bounds access is guaranteed. UB lets it delete your "safety" checks — which is why UB hunting (module 12) is a performance topic too. It may reorder, vectorize, and inline — but it cannot fix O(n²).

## Flags that matter, briefly

`-O2` default shipping; `-O3` marginal, sometimes worse; `-march=native` for your machine only; `-fsanitize=…` never in production; LTO links the optimizer across translation units (module 15 territory).

## Layout micro-wins that are actually macro

- SoA over AoS when loops touch field subsets (module 10).
- `std::vector` over `std::list` almost always — contiguous beats node-based even with extra copying.
- Smaller structs → more records per cache line → fewer misses.
- Sorting before scanning improves branch prediction *and* lets early-exit algorithms fire.

None of these require cleverness — only measuring and choosing.
''',
    "Cờ Trình Biên Dịch, Bố Trí, và Cái Máy",
    "-O2 thực sự giả định gì, tại sao bố trí đánh bại tối ưu vi mô, và cùng một mã nguồn nhanh hơn bằng cách sắp xếp dữ liệu.",
    r'''
## Optimizer được và không được làm gì

Ở `-O2` trình biên dịch giả định không có UB: signed overflow sẽ không xảy ra, con trỏ không alias trái phép với buffer `char`, truy cập trong biên. UB cho phép nó xóa các "kiểm tra an toàn" của bạn — vì vậy săn UB (module 12) cũng là chủ đề hiệu năng. Nó có thể sắp xếp lại, vector hóa, inline — nhưng không thể chữa O(n²).

## Các cờ quan trọng, ngắn gọn

`-O2` mặc định khi xuất bản; `-O3` dư sức, đôi khi tệ hơn; `-march=native` chỉ cho máy bạn; `-fsanitize=…` không bao giờ dùng nơi sản xuất; LTO nối optimizer qua các translation unit (mảng module 15).

## Các điểm cộng bố trí thực ra là vĩ mô

- SoA hơn AoS khi vòng lặp chỉ đụng tập trường con (module 10).
- `std::vector` gần như luôn hơn `std::list` — liền kề đánh bại node-based dù tốn thêm sao chép.
- Struct nhỏ hơn → nhiều bản ghi mỗi cache line → ít miss hơn.
- Sort trước khi quét giúp dự đoán nhánh *và* kích hoạt thuật toán thoát sớm.

Không cái nào cần sự khéo léo — chỉ cần đo và chọn.
''',
    difficulty="advanced",
)

# ============================ MODULE 11 checkpoint + practice content ============================
CP11_MD = r'''
Checkpoint on performance engineering: take a quadratic accumulator and make it linear-and-allocation-free, with every claim checkable.
'''

# ---------------- MODULE 10 practice: pool + pmr ----------------
M10_PRAC1_CH = [
    challenge(
        "cppa10-pool-acquire",
        "Pool Acquire and Exhaust",
        "Complete the fixed-size `BytePool` declared in the boilerplate. `acquire()` hands out block pointers and calls `AllocTracker::noteAlloc()` on success; it must return `nullptr` when the pool is exhausted. This challenge only tests acquire/exhaust behavior — release comes next.",
        CP10_BOILER,
        [
            ("acquire hands out distinct blocks",
             r'''AllocTracker::reset();
BytePool pool{3, 16};
std::uint8_t* a = pool.acquire();
std::uint8_t* b = pool.acquire();
CHECK(a != nullptr);
CHECK(b != nullptr);
CHECK(a != b);
CHECK_EQ(AllocTracker::live(), 2);''',
             "Keep a free-list (stack) of block pointers initialized with all blocks; acquire pops one, calls AllocTracker::noteAlloc(), and returns nullptr when empty."),
            ("exhausted pool returns nullptr",
             r'''AllocTracker::reset();
BytePool pool{2, 8};
CHECK(pool.acquire() != nullptr);
CHECK(pool.acquire() != nullptr);
CHECK_EQ(pool.acquire(), nullptr);
CHECK_EQ(AllocTracker::live(), 2);''',
             "The free-list is empty after two acquires — the third must not underflow the stack or increment the tracker."),
        ],
        difficulty="advanced",
    ),
]

M10_PRAC1_SOL = [
    ("cppa10-pool-acquire",
     CP10_BOILER + "\nBytePool::BytePool(std::size_t blocks, std::size_t blockSize) : blocks_(blocks), blockSize_(blockSize) {\n    storage_ = new std::uint8_t[blocks * blockSize];\n    for (std::size_t i = 0; i < blocks; ++i) freeList_.push_back(storage_ + i * blockSize);\n}\nBytePool::~BytePool() { delete[] storage_; }\nstd::uint8_t* BytePool::acquire() {\n    if (freeList_.empty()) return nullptr;\n    std::uint8_t* p = freeList_.back();\n    freeList_.pop_back();\n    AllocTracker::noteAlloc();\n    return p;\n}\nvoid BytePool::release(std::uint8_t* p) { AllocTracker::noteFree(); freeList_.push_back(p); }\nstd::size_t BytePool::available() const { return freeList_.size(); }\n",
     CP10_BOILER + "\nBytePool::BytePool(std::size_t blocks, std::size_t blockSize) : blocks_(blocks), blockSize_(blockSize) {\n    storage_ = new std::uint8_t[blocks * blockSize];\n    for (std::size_t i = 0; i < blocks; ++i) freeList_.push_back(storage_ + i * blockSize);\n}\nBytePool::~BytePool() { delete[] storage_; }\nstd::uint8_t* BytePool::acquire() {\n    std::uint8_t* p = freeList_.back();  // WRONG: no emptiness check\n    freeList_.pop_back();\n    AllocTracker::noteAlloc();\n    return p;\n}\nvoid BytePool::release(std::uint8_t* p) { AllocTracker::noteFree(); freeList_.push_back(p); }\nstd::size_t BytePool::available() const { return freeList_.size(); }\n"),
]

M10_PRAC1_VI = {
    "cppa10-pool-acquire": {
        "title": "Pool: Cấp phát và Cạn kho",
        "prompt": "Hoàn thiện `BytePool` kích thước cố định theo khai báo trong boilerplate. `acquire()` trả con trỏ khối và gọi `AllocTracker::noteAlloc()` khi thành công; phải trả `nullptr` khi pool cạn. Bài này chỉ kiểm acquire/exhaust — release ở bài sau.",
        "hints": [
            "Giữ một free-list (stack) các con trỏ khối, khởi tạo đủ mọi khối; acquire pop một khối, gọi AllocTracker::noteAlloc(), trả nullptr khi rỗng.",
            "Sau hai lần acquire, free-list rỗng — lần thứ ba không được làm underflow stack hay tăng tracker.",
        ],
    },
}

M10_PRAC1_CH2 = [
    challenge(
        "cppa10-pool-release",
        "Pool Release and Reuse",
        "Extend the pool: `release(p)` returns a previously-acquired block to the free list (calls `AllocTracker::noteFree()`), and `available()` reports how many blocks can still be handed out.",
        CP10_BOILER,
        [
            ("released blocks are reusable",
             r'''AllocTracker::reset();
BytePool pool{1, 16};
std::uint8_t* a = pool.acquire();
CHECK_EQ(pool.available(), 0u);
pool.release(a);
CHECK_EQ(pool.available(), 1u);
std::uint8_t* b = pool.acquire();
CHECK_EQ(b, a);
CHECK_EQ(AllocTracker::live(), 1);''',
             "release pushes the block back onto the free-list and notes a free; acquire pops it — the same pointer comes back for a 1-block pool."),
            ("available tracks the free-list",
             r'''AllocTracker::reset();
BytePool pool{4, 8};
std::uint8_t* p1 = pool.acquire();
std::uint8_t* p2 = pool.acquire();
CHECK_EQ(pool.available(), 2u);
pool.release(p1);
pool.release(p2);
CHECK_EQ(pool.available(), 4u);
CHECK_EQ(AllocTracker::live(), 0);''',
             "available() == free-list size at all times; two releases after two acquires restore 4 and live()==0."),
        ],
        difficulty="advanced",
    ),
]

M10_PRAC1_SOL2 = [
    ("cppa10-pool-release",
     CP10_BOILER + "\nBytePool::BytePool(std::size_t blocks, std::size_t blockSize) : blocks_(blocks), blockSize_(blockSize) {\n    storage_ = new std::uint8_t[blocks * blockSize];\n    for (std::size_t i = 0; i < blocks; ++i) freeList_.push_back(storage_ + i * blockSize);\n}\nBytePool::~BytePool() { delete[] storage_; }\nstd::uint8_t* BytePool::acquire() {\n    if (freeList_.empty()) return nullptr;\n    std::uint8_t* p = freeList_.back();\n    freeList_.pop_back();\n    AllocTracker::noteAlloc();\n    return p;\n}\nvoid BytePool::release(std::uint8_t* p) { AllocTracker::noteFree(); freeList_.push_back(p); }\nstd::size_t BytePool::available() const { return freeList_.size(); }\n",
     CP10_BOILER + "\nBytePool::BytePool(std::size_t blocks, std::size_t blockSize) : blocks_(blocks), blockSize_(blockSize) {\n    storage_ = new std::uint8_t[blocks * blockSize];\n    for (std::size_t i = 0; i < blocks; ++i) freeList_.push_back(storage_ + i * blockSize);\n}\nBytePool::~BytePool() { delete[] storage_; }\nstd::uint8_t* BytePool::acquire() {\n    if (freeList_.empty()) return nullptr;\n    std::uint8_t* p = freeList_.back();\n    freeList_.pop_back();\n    AllocTracker::noteAlloc();\n    return p;\n}\nvoid BytePool::release(std::uint8_t* p) { AllocTracker::noteFree(); }\nstd::size_t BytePool::available() const { return freeList_.size(); }\n"),
]

M10_PRAC1_VI2 = {
    "cppa10-pool-release": {
        "title": "Pool: Trả khối và Tái sử dụng",
        "prompt": "Mở rộng pool: `release(p)` trả một khối đã cấp phát về free list (gọi `AllocTracker::noteFree()`), và `available()` báo số khối còn có thể phát.",
        "hints": [
            "release đẩy khối trở lại free-list và ghi nhận một free; acquire pop ra — pool 1 khối sẽ trả lại đúng con trỏ cũ.",
            "available() luôn bằng kích thước free-list; hai lần release sau hai lần acquire khôi phục 4 và live()==0.",
        ],
    },
}

M10_PRAC2_CH = [
    challenge(
        "cppa10-pmr-arena",
        "Arena Carve and Reset",
        "Implement a tiny linear arena: `Arena(bytes)` owns a buffer; `carve(n)` returns a pointer into it (16-byte aligned) or `nullptr` if `n` does not fit; `reset()` makes the whole buffer reusable; `used()` reports allocated bytes.",
        r'''#include <cstddef>
#include <cstdint>

// A linear (monotonic) arena.
class Arena {
public:
    explicit Arena(std::size_t bytes);
    ~Arena();
    void* carve(std::size_t n);   // 16-byte aligned; nullptr if it doesn't fit
    void reset();                 // everything becomes reusable
    std::size_t used() const;
private:
    std::size_t bytes_;
    std::size_t offset_ = 0;
    std::uint8_t* buf_ = nullptr;
};
''',
        [
            ("carve hands out aligned, non-overlapping ranges",
             r'''Arena a{100};
void* p1 = a.carve(10);
void* p2 = a.carve(10);
CHECK(p1 != nullptr);
CHECK(p2 != nullptr);
CHECK(static_cast<std::uint8_t*>(p2) >= static_cast<std::uint8_t*>(p1) + 10);
CHECK_EQ(reinterpret_cast<std::uintptr_t>(p1) % 16, 0u);
CHECK_EQ(reinterpret_cast<std::uintptr_t>(p2) % 16, 0u);
CHECK(a.used() >= 20u);''',
             "Round the offset up to the next multiple of 16 (padding counts toward used()), return buf_ + offset, advance offset by n."),
            ("reset restores capacity",
             r'''Arena a{64};
CHECK(a.carve(48) != nullptr);
CHECK_EQ(a.carve(48), nullptr);   // doesn't fit
a.reset();
CHECK_EQ(a.used(), 0u);
CHECK(a.carve(48) != nullptr);''',
             "reset() sets offset_ back to 0 — carve succeeds again after reset. The alignment rule: round the offset up to a multiple of 16 BEFORE handing out the pointer."),
        ],
        difficulty="advanced",
    ),
]

M10_PRAC2_SOL = [
    ("cppa10-pmr-arena",
     r'''#include <cstddef>
#include <cstdint>

class Arena {
public:
    explicit Arena(std::size_t bytes);
    ~Arena();
    void* carve(std::size_t n);
    void reset();
    std::size_t used() const;
private:
    std::size_t bytes_;
    std::size_t offset_ = 0;
    std::uint8_t* buf_ = nullptr;
};

Arena::Arena(std::size_t bytes) : bytes_(bytes), buf_(new std::uint8_t[bytes]) {}
Arena::~Arena() { delete[] buf_; }
void* Arena::carve(std::size_t n) {
    std::size_t aligned = (offset_ + 15) / 16 * 16;
    if (aligned + n > bytes_) return nullptr;
    void* p = buf_ + aligned;
    offset_ = aligned + n;
    return p;
}
void Arena::reset() { offset_ = 0; }
std::size_t Arena::used() const { return offset_; }
''',
     r'''#include <cstddef>
#include <cstdint>

class Arena {
public:
    explicit Arena(std::size_t bytes);
    ~Arena();
    void* carve(std::size_t n);
    void reset();
    std::size_t used() const;
private:
    std::size_t bytes_;
    std::size_t offset_ = 0;
    std::uint8_t* buf_ = nullptr;
};

Arena::Arena(std::size_t bytes) : bytes_(bytes), buf_(new std::uint8_t[bytes]) {}
Arena::~Arena() { delete[] buf_; }
void* Arena::carve(std::size_t n) {
    void* p = buf_ + offset_;
    offset_ += n + 16;   // WRONG: no alignment AND overcounts every carve
    return p;
}
void Arena::reset() { offset_ = 0; }
std::size_t Arena::used() const { return offset_; }
'''),
]

M10_PRAC2_VI = {
    "cppa10-pmr-arena": {
        "title": "Arena: Carve và Reset",
        "prompt": "Cài một arena tuyến tính mini: `Arena(bytes)` sở hữu một buffer; `carve(n)` trả con trỏ vào trong đó (căn chỉnh 16 byte) hoặc `nullptr` nếu `n` không vừa; `reset()` biến cả buffer dùng lại được; `used()` báo số byte đã cấp phát.",
        "hints": [
            "Làm tròn offset lên bội của 16, trả buf_ + offset, rồi tăng offset thêm n.",
            "reset() đưa offset_ về 0 — carve thành công trở lại sau reset.",
        ],
    },
}

# ---------------- MODULE 11 practice: allocation counting + algorithmic win ----------------
M11_PRAC1_CH = [
    challenge(
        "cppa11-reserve-then-build",
        "Reserve Then Build",
        "Implement `squares` so it produces n values 1..n into the output vector using **at most one allocation**: reserve the exact capacity before writing. `push_back` in a loop after reserving is fine.",
        r'''#include <cstdlib>
#include <vector>

// Global allocation counter (each graded test is its own program).
inline int& gAllocs() { static int n = 0; return n; }
void* operator new(std::size_t sz) { ++gAllocs(); return std::malloc(sz); }
void* operator new[](std::size_t sz) { ++gAllocs(); return std::malloc(sz); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
inline int allocCount() { return gAllocs(); }

// Fill out with 1², 2², …, n² using at most ONE allocation.
void squares(std::vector<long long>& out, int n);
''',
        [
            ("values and single allocation",
             r'''std::vector<long long> v;
int before = allocCount();
squares(v, 5);
CHECK_EQ(allocCount() - before <= 1, true);
CHECK_EQ(v.size(), 5u);
CHECK_EQ(v[0], 1LL);
CHECK_EQ(v[4], 25LL);''',
             "out.reserve(n) before the loop — a growing vector reallocates O(log n) times."),
            ("large n stays at one allocation",
             r'''std::vector<long long> v;
int before = allocCount();
squares(v, 10000);
CHECK_EQ(allocCount() - before <= 1, true);
CHECK_EQ(v.back(), 100000000LL);''',
             "reserve(10000) then push_back n times — no reallocation path is ever taken."),
        ],
        difficulty="advanced",
    ),
]

M11_PRAC1_SOL = [
    ("cppa11-reserve-then-build",
     M11_PRAC1_CH[0]["boilerplate"] + r'''void squares(std::vector<long long>& out, int n) {
    out.reserve(n);
    for (int i = 1; i <= n; ++i) out.push_back(1LL * i * i);
}
''',
     M11_PRAC1_CH[0]["boilerplate"] + r'''void squares(std::vector<long long>& out, int n) {
    for (int i = 1; i <= n; ++i) out.push_back(1LL * i * i);  // WRONG: no reserve
}
'''),
]

M11_PRAC1_VI = {
    "cppa11-reserve-then-build": {
        "title": "Reserve Rồi Mới Dựng",
        "prompt": "Cài `squares` tạo n giá trị 1..n vào vector đầu ra với **tối đa một lần cấp phát**: reserve đúng dung lượng trước khi ghi. `push_back` trong vòng lặp sau khi reserve là được.",
        "hints": [
            "out.reserve(n) trước vòng lặp — vector tự lớn phải reallocate O(log n) lần.",
            "reserve(10000) rồi push_back n lần — không bao giờ đi vào nhánh reallocate.",
        ],
    },
}

M11_PRAC2_CH = [
    challenge(
        "cppa11-alg-win",
        "Algorithmic Win: Count Once",
        "`sumUnique` returns the sum of distinct values. The naive version sorts and scans, or worse, is O(n²). Implement it to run in **at most n long-long comparisons** by using an unordered_set — the grader counts comparisons via a tracked type.",
        r'''#include <cstdint>
#include <vector>

// Elements carry a comparison counter. A hash-based solution compares
// elements only on duplicate insertion (<= n total); a sort-based one
// needs O(n log n) comparisons and fails the bound.
#include <unordered_set>

struct Tracked {
    long long value;
    inline static int& comparisons() { static int n = 0; return n; }
    friend bool operator<(const Tracked& a, const Tracked& b) { ++comparisons(); return a.value < b.value; }
    friend bool operator==(const Tracked& a, const Tracked& b) { ++comparisons(); return a.value == b.value; }
};
template <>
struct std::hash<Tracked> {
    std::size_t operator()(const Tracked& t) const noexcept { return std::hash<long long>{}(t.value); }
};
inline int trackedComparisons() { return Tracked::comparisons(); }

// Sum of the distinct values in data.
long long sumUnique(const std::vector<Tracked>& data);
''',
        [
            ("correct sums",
             r'''CHECK_EQ(sumUnique({{1}, {2}, {3}, {2}, {1}}), 6LL);
CHECK_EQ(sumUnique({}), 0LL);
CHECK_EQ(sumUnique({{5}, {5}, {5}}), 5LL);
CHECK_EQ(sumUnique({{-1}, {-1}, {2}, {3}}), 4LL);''',
             "Insert everything into std::unordered_set<Tracked>, adding t.value when the insert is new."),
            ("no sorting-based comparisons",
             r'''int before = trackedComparisons();
sumUnique({{9}, {8}, {7}, {6}, {5}, {4}, {3}, {2}, {1}, {9}, {8}});
CHECK(trackedComparisons() - before <= 11);''',
             "unordered_set compares only when a duplicate lands in an occupied bucket — at most n comparisons; a sort-based approach needs O(n log n) and fails the bound."),
        ],
        difficulty="advanced",
    ),
]

M11_PRAC2_SOL = [
    ("cppa11-alg-win",
     M11_PRAC2_CH[0]["boilerplate"] + r'''long long sumUnique(const std::vector<Tracked>& data) {
    std::unordered_set<Tracked> s;
    long long sum = 0;
    for (const Tracked& t : data) {
        if (s.insert(t).second) sum += t.value;
    }
    return sum;
}
''',
     M11_PRAC2_CH[0]["boilerplate"] + r'''long long sumUnique(const std::vector<Tracked>& data) {
    std::vector<Tracked> v = data;              // WRONG: sorts -> comparisons blow the bound
    std::sort(v.begin(), v.end());
    v.erase(std::unique(v.begin(), v.end()), v.end());
    long long sum = 0;
    for (const Tracked& t : v) sum += t.value;
    return sum;
}
'''),
]

M11_PRAC2_VI = {
    "cppa11-alg-win": {
        "title": "Thắng Thuật Toán: Đếm Một Lần",
        "prompt": "`sumUnique` trả tổng các giá trị phân biệt. Bản ngây thơ sort rồi quét, hoặc tệ hơn, là O(n²). Hãy cài để chạy với **tối đa n phép so sánh long-long** bằng unordered_set — grader đếm so sánh qua một kiểu được theo dõi.",
        "hints": [
            "Chèn tất cả vào std::unordered_set<long long>, rồi cộng dồn các phần tử của set.",
            "unordered_set dùng băm — phép so sánh phần tử giữ ở 0; cách dựa trên sort so sánh O(n log n) lần và trượt.",
        ],
    },
}

# ---------------- MODULE 10 checkpoint ----------------
write_checkpoint(
    M10, L10D,
    "Checkpoint: Memory Architecture",
    "Prove pool semantics: acquire, exhaust, release, reuse — with allocation accounting that must balance.",
    17,
    CP10_MD,
    "Checkpoint: Kiến trúc Bộ nhớ",
    "Chứng minh ngữ nghĩa pool: acquire, cạn, release, tái sử dụng — với sổ sách cấp phát phải khớp.",
    r'''
Checkpoint kiến trúc bộ nhớ: pool tái sử dụng đếm qua bộ theo dõi cấp phát, và arena phải carve và reset sạch sẽ.
''',
    challenge(
        "cppa10-alloc-checkpoint",
        "Pool Lifecycle Gauntlet",
        "Implement the full `BytePool` lifecycle: acquire until exhausted (nullptr after), release back (noteFree), and reuse released blocks. The tracker's live count must always equal blocks-out minus blocks-returned.",
        CP10_BOILER,
        [
            ("acquire, exhaust, release, reuse",
             r'''AllocTracker::reset();
BytePool pool{2, 32};
std::uint8_t* a = pool.acquire();
std::uint8_t* b = pool.acquire();
CHECK_EQ(pool.acquire(), nullptr);
CHECK_EQ(AllocTracker::live(), 2);
pool.release(a);
CHECK_EQ(AllocTracker::live(), 1);
std::uint8_t* c = pool.acquire();
CHECK_EQ(c, a);
CHECK_EQ(AllocTracker::live(), 2);''',
             "Free-list of block pointers: acquire pops (nullptr when empty, noteAlloc), release pushes (noteFree) — live() stays consistent automatically."),
            ("release of both blocks restores everything",
             r'''AllocTracker::reset();
BytePool pool{3, 16};
std::uint8_t* a = pool.acquire();
std::uint8_t* b = pool.acquire();
std::uint8_t* c = pool.acquire();
pool.release(a);
pool.release(b);
pool.release(c);
CHECK_EQ(pool.available(), 3u);
CHECK_EQ(AllocTracker::live(), 0);
CHECK_EQ(AllocTracker::allocs(), 3);
CHECK_EQ(AllocTracker::frees(), 3);''',
             "Three acquires then three releases: available()==3, live()==0, allocs==frees==3."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại vòng đời pool",
        "Cài trọn vòng đời `BytePool`: acquire tới khi cạn (nullptr sau đó), release trả về (noteFree), và tái sử dụng khối đã trả. Số live của tracker luôn bằng số khối đã phát trừ số khối đã trả.",
        [
            ("acquire, cạn, release, tái sử dụng", "Free-list các con trỏ khối: acquire pop (nullptr khi rỗng, noteAlloc), release push (noteFree) — live() tự khớp."),
            ("release cả hai khối khôi phục mọi thứ", "Ba lần acquire rồi ba lần release: available()==3, live()==0, allocs==frees==3."),
        ],
    ),
    solution=CP10_BOILER + "\nBytePool::BytePool(std::size_t blocks, std::size_t blockSize) : blocks_(blocks), blockSize_(blockSize) {\n    storage_ = new std::uint8_t[blocks * blockSize];\n    for (std::size_t i = 0; i < blocks; ++i) freeList_.push_back(storage_ + i * blockSize);\n}\nBytePool::~BytePool() { delete[] storage_; }\nstd::uint8_t* BytePool::acquire() {\n    if (freeList_.empty()) return nullptr;\n    std::uint8_t* p = freeList_.back();\n    freeList_.pop_back();\n    AllocTracker::noteAlloc();\n    return p;\n}\nvoid BytePool::release(std::uint8_t* p) { AllocTracker::noteFree(); freeList_.push_back(p); }\nstd::size_t BytePool::available() const { return freeList_.size(); }\n",
    wrong=CP10_BOILER + "\nBytePool::BytePool(std::size_t blocks, std::size_t blockSize) : blocks_(blocks), blockSize_(blockSize) {\n    storage_ = new std::uint8_t[blocks * blockSize];\n    for (std::size_t i = 0; i < blocks; ++i) freeList_.push_back(storage_ + i * blockSize);\n}\nBytePool::~BytePool() { delete[] storage_; }\nstd::uint8_t* BytePool::acquire() {\n    if (freeList_.empty()) return nullptr;\n    std::uint8_t* p = freeList_.back();\n    freeList_.pop_back();\n    AllocTracker::noteAlloc();\n    return p;\n}\nvoid BytePool::release(std::uint8_t* p) { AllocTracker::noteFree(); }  // WRONG: block never returned to the free list\nstd::size_t BytePool::available() const { return freeList_.size(); }\n",
)

CP11_PERF_BOILER = r'''#include <cstdint>
#include <cstdlib>
#include <vector>

// Allocation counter (each graded test is its own program).
inline int& gAllocs() { static int n = 0; return n; }
void* operator new(std::size_t sz) { ++gAllocs(); return std::malloc(sz); }
void* operator new[](std::size_t sz) { ++gAllocs(); return std::malloc(sz); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
inline int allocCount() { return gAllocs(); }

// Comparison-counted element (see module 11 practice).
#include <unordered_set>

struct Tracked {
    long long value;
    inline static int& comparisons() { static int n = 0; return n; }
    friend bool operator<(const Tracked& a, const Tracked& b) { ++comparisons(); return a.value < b.value; }
    friend bool operator==(const Tracked& a, const Tracked& b) { ++comparisons(); return a.value == b.value; }
};
template <>
struct std::hash<Tracked> {
    std::size_t operator()(const Tracked& t) const noexcept { return std::hash<long long>{}(t.value); }
};
inline int trackedComparisons() { return Tracked::comparisons(); }

// (1) out gets 0..n-1 with at most one allocation.
void buildRange(std::vector<int>& out, int n);

// (2) number of distinct values; hash-based membership keeps comparisons <= n.
int countDistinct(const std::vector<Tracked>& data);
'''

write_checkpoint(
    M11, L11D,
    "Checkpoint: Performance",
    "Prove the evidence chain: reserve-first construction and hash-based uniqueness — both counted, not timed.",
    18,
    CP11_MD,
    "Checkpoint: Hiệu năng",
    "Chứng minh chuỗi bằng chứng: dựng kiểu reserve-trước và tính duy nhất bằng băm — đều được đếm, không đo thời gian.",
    r'''
Checkpoint hiệu năng: biến bộ cộng dồn cấp số nhân thành tuyến-tính-và-không-cấp-phát, mọi khẳng định đều kiểm chứng được.
''',
    challenge(
        "cppa11-perf-checkpoint",
        "Evidence Gauntlet",
        "Two graded properties: (1) `buildRange` produces n values with at most one allocation, (2) `countDistinct` uses hashing so tracked element comparisons stay at zero.",
        CP11_PERF_BOILER,
        [
            ("buildRange: one allocation, right values",
             r'''std::vector<int> v;
int before = allocCount();
buildRange(v, 8);
CHECK_EQ(allocCount() - before <= 1, true);
CHECK_EQ(v.size(), 8u);
CHECK_EQ(v.front(), 0);
CHECK_EQ(v.back(), 7);''',
             "out.reserve(n) then fill 0..n-1."),
            ("countDistinct: hash, don't compare",
             r'''int before = trackedComparisons();
CHECK_EQ(countDistinct({{1}, {2}, {2}, {3}, {3}, {3}}), 3);
CHECK(trackedComparisons() - before <= 6);
CHECK_EQ(countDistinct({}), 0);''',
             "std::unordered_set<Tracked> s; insert each element; return (int)s.size();"),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại bằng chứng hiệu năng",
        "Hai thuộc tính được chấm: (1) `buildRange` tạo n giá trị với tối đa một lần cấp phát, (2) `countDistinct` dùng băm nên phép so sánh phần tử được theo dõi giữ ở 0.",
        [
            ("buildRange: một lần cấp phát, giá trị đúng", "out.reserve(n) rồi ghi 0..n-1."),
            ("countDistinct: băm, đừng so sánh", "std::unordered_set<int> s(data.begin(), data.end()); return (int)s.size();"),
        ],
    ),
    solution=CP11_PERF_BOILER + r'''void buildRange(std::vector<int>& out, int n) {
    out.reserve(n);
    for (int i = 0; i < n; ++i) out.push_back(i);
}
int countDistinct(const std::vector<Tracked>& data) {
    std::unordered_set<Tracked> s;
    for (const Tracked& t : data) s.insert(t);
    return static_cast<int>(s.size());
}
''',
    wrong=CP11_PERF_BOILER + r'''void buildRange(std::vector<int>& out, int n) {
    for (int i = 0; i < n; ++i) out.push_back(i);   // WRONG: no reserve
}
int countDistinct(const std::vector<Tracked>& data) {
    std::vector<Tracked> v = data;                  // WRONG: sort-based -> comparisons blow the bound
    std::sort(v.begin(), v.end());
    v.erase(std::unique(v.begin(), v.end()), v.end());
    return static_cast<int>(v.size());
}
''',
)

write_practice(
    M10, "m10-pool-practice",
    "Practice: Pool Mechanics",
    "Build a fixed-size block pool: acquire, exhaust, release, reuse — with allocation accounting that must balance.",
    "Luyện tập: Cơ chế Pool",
    "Dựng pool khối kích thước cố định: acquire, cạn, release, tái sử dụng — với sổ sách cấp phát phải khớp.",
    L10A, 15, "advanced",
    challenges=M10_PRAC1_CH + M10_PRAC1_CH2,
    vi_challenges={**M10_PRAC1_VI, **M10_PRAC1_VI2},
    solutions=M10_PRAC1_SOL + M10_PRAC1_SOL2)

write_practice(
    M10, "m10-pmr-practice",
    "Practice: Arena and pmr",
    "Implement a linear arena with 16-byte alignment, carve, and reset — the shape every monotonic resource shares.",
    "Luyện tập: Arena và pmr",
    "Cài arena tuyến tính với căn chỉnh 16 byte, carve, và reset — hình dạng chung của mọi monotonic resource.",
    L10B, 15, "advanced",
    challenges=M10_PRAC2_CH, vi_challenges=M10_PRAC2_VI, solutions=M10_PRAC2_SOL)

write_practice(
    M11, "m11-alloc-practice",
    "Practice: Counting Allocations",
    "Make construction allocation-bounded: reserve-first building graded by an allocation counter.",
    "Luyện tập: Đếm Cấp phát",
    "Biến việc dựng dữ liệu thành có giới hạn cấp phát: dựng kiểu reserve-trước được chấm bằng bộ đếm cấp phát.",
    L11A, 14, "advanced",
    challenges=M11_PRAC1_CH, vi_challenges=M11_PRAC1_VI, solutions=M11_PRAC1_SOL)

write_practice(
    M11, "m11-alg-practice",
    "Practice: Algorithmic Wins",
    "Replace sort-and-scan with hashing when the grader counts comparisons — algorithmic wins proven by arithmetic.",
    "Luyện tập: Thắng Thuật Toán",
    "Thay sort-và-quét bằng băm khi grader đếm phép so sánh — thắng thuật toán được chứng minh bằng toán học.",
    L11B, 14, "advanced",
    challenges=M11_PRAC2_CH, vi_challenges=M11_PRAC2_VI, solutions=M11_PRAC2_SOL)

print("modules 10-11 done")
