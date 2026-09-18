#!/usr/bin/env python3
"""C++ Advanced — module 7 (coroutines)."""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

M7 = "coroutines"

L7A = "coroutine-machinery"
L7B = "generator-build"
L7C = "generator-lifetimes"
L7D = "cppa-checkpoint-coroutines"

write_module(
    M7,
    "Coroutines from First Principles",
    "co_await, co_yield, promise_type, and the handles that drive them — build a generator with your own hands so async C++ never looks like magic again.",
    "Coroutine Từ Nguyên Bản",
    "co_await, co_yield, promise_type và các handle điều khiển chúng — tự tay dựng một generator để async C++ không còn giống ma thuật.",
    [L7A, L7B, L7C, L7D],
    ["m7-generator-practice", "m7-lifetime-practice"],
)

write_lesson(
    M7, L7A,
    "The Coroutine Machinery",
    "Three keywords, one promise, one handle. What the compiler actually generates when it sees co_yield.",
    12,
    r'''
A **coroutine** is any function containing `co_await`, `co_yield`, or `co_return`. Calling one does not run its body — it builds a **frame** (heap storage holding parameters, locals, and state) and hands you an object the promise constructs.

## The three players

1. **The coroutine body** — your code with suspension points,
2. **`promise_type`** — the customization point: controls what calling the coroutine produces, what `co_yield`/`co_return` store, and what happens at the start/end of the frame,
3. **`std::coroutine_handle<P>`** — the steering wheel: `resume()` continues the body until the next suspension; `done()` reports completion; the handle is what your **return object** wraps so callers can drive the coroutine.

## What co_yield compiles into

`co_yield expr;` is exactly:

```cpp
promise.yield_value(expr);      // store the value
co_await promise.yield_value(expr);  // suspend here; resume continues AFTER this line
```

On resume, execution continues at the statement after the `co_yield`. That resumption point is why generators are lazy: nothing after the current suspension runs until someone asks.

## The required promise members

For a plain generator: `get_return_object()` (builds what the call returns), `initial_suspend()` (usually `std::suspend_always` — laziness), `final_suspend()` (must be **noexcept** and usually `std::suspend_always` so the frame survives until you destroy it), `return_void()` or `return_value(v)` (co_return handling), and `unhandled_exception()` (store or rethrow).

That is the whole contract. Next lesson: the ~40-line generator that implements it.
''',
    "Cơ chế Coroutine",
    "Ba từ khóa, một promise, một handle. Compiler sinh ra gì thật sự khi thấy co_yield.",
    r'''
**Coroutine** là bất kỳ hàm nào chứa `co_await`, `co_yield`, hoặc `co_return`. Gọi nó không chạy thân hàm — nó dựng một **frame** (bộ nhớ heap giữ tham số, biến cục bộ và trạng thái) rồi trao cho bạn đối tượng mà promise tạo ra.

## Ba nhân vật

1. **Thân coroutine** — code của bạn với các điểm treo,
2. **`promise_type`** — điểm tùy biến: quyết định lời gọi coroutine tạo ra gì, `co_yield`/`co_return` lưu gì, và điều gì xảy ra đầu/cuối frame,
3. **`std::coroutine_handle<P>`** — bánh lái: `resume()` chạy tiếp thân hàm đến điểm treo kế tiếp; `done()` báo hoàn tất; return object của bạn bọc handle để caller lái coroutine.

## co_yield biên dịch thành gì

`co_yield expr;` chính xác là:

```cpp
promise.yield_value(expr);           // lưu giá trị
co_await promise.yield_value(expr);  // treo tại đây; resume tiếp tục SAU dòng này
```

Khi resume, thực thi tiếp tục ở câu lệnh sau `co_yield`. Chính điểm phục hồi đó làm generator lười biếng: không gì sau điểm treo hiện tại chạy cho tới khi có người hỏi.

## Các thành viên bắt buộc của promise

Với một generator thô: `get_return_object()` (dựng thứ mà lời gọi trả về), `initial_suspend()` (thường `std::suspend_always` — tính lười), `final_suspend()` (bắt buộc **noexcept**, thường `std::suspend_always` để frame sống cho tới khi bạn hủy), `return_void()` hoặc `return_value(v)` (xử lý co_return), và `unhandled_exception()` (lưu hoặc ném lại).

Đó là toàn bộ hợp đồng. Bài kế tiếp: generator ~40 dòng cài đặt nó.
''',
    difficulty="advanced",
)

write_lesson(
    M7, L7B,
    "Building Generator<T> — the Full Walkthrough",
    "The complete ~40-line generator: promise, handle wrapper, and the co_yield body. You will write it twice: once reading, once graded.",
    13,
    r'''
Here is the complete generator, annotated. Every graded exercise in this module is a variation of it.

```cpp
#include <coroutine>
#include <exception>
#include <utility>

template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};

        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }   // lazy start
        std::suspend_always final_suspend() noexcept { return {}; }     // keep frame; caller destroys
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }  // store + pause
        void return_void() {}
        void unhandled_exception() { std::terminate(); }   // course-scope simplification
    };

    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }             // RAII owns the frame

    // Advance and report: true if a fresh value is available.
    bool next() {
        h_.resume();
        return !h_.done();
    }
    T value() const { return h_.promise().current_; }

private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}
```

## Reading the flow

`counter(1, 3)` returns immediately: the frame exists, suspended at `initial_suspend`. `next()` resumes the body until the first `co_yield i` stores `1` and pauses. `value()` reads what the promise stored. `next()` again → resume after the yield → loop → yield `2`… When the loop ends, the body falls off; `final_suspend` pauses once more; `done()` becomes true. The destructor destroys the frame — because `final_suspend` kept it suspended, destroying is safe (no double-resume of a finished frame).

## The three classic bugs (each is a graded trap)

1. **Resuming a done coroutine** — UB. Guard: check `done()` before `resume()`.
2. **`final_suspend` returning `suspend_never`** — the frame self-destroys; your destructor then destroys it again: double-destroy UB. Keep `suspend_always`.
3. **Yielding a reference to a local** — the value dies with the frame resumption; store by value (`current_ = std::move(v)`), or guarantee the referenced thing outlives the generator.

## C++23 aside

`std::generator<T>` (C++23) is exactly this class, battle-hardened and range-compatible. GCC 14.2 ships an early version; the course teaches the hand-rolled form because the machinery *is* the lesson — and because the hand-rolled form compiles identically on both course toolchains.
''',
    "Dựng Generator<T> — Giải Thích Đầy Đủ",
    "Generator hoàn chỉnh ~40 dòng: promise, wrapper handle và thân co_yield. Bạn sẽ viết nó hai lần: một lần đọc, một lần được chấm.",
    r'''
Đây là generator hoàn chỉnh, có chú thích. Mọi bài tập chấm điểm trong module này đều là biến thể của nó.

```cpp
#include <coroutine>
#include <exception>
#include <utility>

template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};

        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }   // khởi động lười
        std::suspend_always final_suspend() noexcept { return {}; }     // giữ frame; caller hủy
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }  // lưu + treo
        void return_void() {}
        void unhandled_exception() { std::terminate(); }   // đơn giản hóa trong phạm vi khóa học
    };

    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }             // RAII sở hữu frame

    // Tiến và báo: true nếu có giá trị mới.
    bool next() {
        h_.resume();
        return !h_.done();
    }
    T value() const { return h_.promise().current_; }

private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}
```

## Đọc luồng chạy

`counter(1, 3)` trả về ngay lập tức: frame tồn tại, treo tại `initial_suspend`. `next()` phục hồi thân hàm cho tới `co_yield i` đầu tiên lưu `1` rồi treo. `value()` đọc những gì promise lưu. `next()` lần nữa → phục hồi sau yield → vòng lặp → yield `2`… Khi vòng lặp kết thúc, thân hàm kết thúc; `final_suspend` treo thêm lần nữa; `done()` thành true. Destructor hủy frame — vì `final_suspend` giữ nó treo, việc hủy là an toàn (không resume-hai-lần lên frame đã xong).

## Ba lỗi kinh điển (mỗi lỗi là một cái bẫy được chấm)

1. **Resume coroutine đã done** — UB. Phòng: kiểm tra `done()` trước `resume()`.
2. **`final_suspend` trả `suspend_never`** — frame tự hủy; destructor của bạn rồi lại hủy nó lần nữa: double-destroy UB. Giữ `suspend_always`.
3. **Yield tham chiếu tới biến cục bộ** — giá trị chết cùng lần phục hồi frame; lưu bằng giá trị (`current_ = std::move(v)`), hoặc bảo đảm thứ được tham chiếu sống lâu hơn generator.

## Ghi chú C++23

`std::generator<T>` (C++23) chính là lớp này, đã được tôi luyện và tương thích range. GCC 14.2 có bản sơ khai; khóa học dạy bản viết tay vì bản thân cơ chế *mới* là bài học — và vì bản viết tay biên dịch giống hệt trên cả hai toolchain của khóa học.
''',
    difficulty="advanced",
)

write_lesson(
    M7, L7C,
    "Coroutine Lifetimes and Hazards",
    "Frames are heap allocations. Parameters are copied or moved in. Lambdas with by-reference captures are the classic trap.",
    11,
    r'''
## The frame owns more than you think

The frame stores: the coroutine's **parameters** (copied or moved at call time — by-value parameters are moved into the frame; references stored as references still point outside and can dangle), all locals live across suspensions, and the promise. Frame allocation is normally a heap `operator new` — unless the compiler proves the lifetime is scoped and elides it (HALO). Treat every coroutine call as an allocation unless measured otherwise.

## The by-reference lambda trap

```cpp
auto makeGen() {
    int state = 0;
    return [&state]() -> Generator<int> {   // WRONG: state dies with makeGen
        while (state < 3) co_yield state++;
    }();
}
```

The lambda captured `state` **by reference**; the generator outlives it. First resume reads a dead variable. Fix: capture by value (`[state]`) or pass `state` as a by-value coroutine parameter (parameters live inside the frame — the safe home).

## Predictable lifetime rules

1. Coroutine parameters are safe **inside the frame** if passed by value/move.
2. Anything referenced (parameters by &, captures by &) must provably outlive the generator — same discipline as views.
3. The generator object owns the handle; moving the generator moves ownership; the moved-from one must not be resumed or destroyed twice (`std::exchange` in the move, as in the lesson's code).
4. Destroy or let RAII destroy **before** the referenced environment dies.

The graded exercise: repair exactly the dangling-capture generator, then predict which of several snippets dangle.
''',
    "Vòng Đời Coroutine và Các Nguy Cơ",
    "Frame là một phép cấp phát heap. Tham số được copy hoặc move vào. Lambda bắt tham chiếu là cái bẫy kinh điển.",
    r'''
## Frame sở hữu nhiều hơn bạn nghĩ

Frame lưu: **tham số** của coroutine (được copy/move lúc gọi — tham số truyền giá trị được move vào frame; tham chiếu được lưu dưới dạng tham chiếu vẫn trỏ ra ngoài và có thể dangling), mọi biến cục bộ sống qua các điểm treo, và promise. Cấp phát frame bình thường là một `operator new` trên heap — trừ khi compiler chứng minh được vòng đời nằm trong phạm vi và loại bỏ nó (HALO). Hãy coi mỗi lời gọi coroutine là một phép cấp phát, trừ khi đã đo.

## Bẫy lambda bắt tham chiếu

```cpp
auto makeGen() {
    int state = 0;
    return [&state]() -> Generator<int> {   // SAI: state chết cùng makeGen
        while (state < 3) co_yield state++;
    }();
}
```

Lambda bắt `state` **bằng tham chiếu**; generator sống lâu hơn nó. Lần resume đầu đọc một biến đã chết. Cách sửa: bắt bằng giá trị (`[state]`) hoặc truyền `state` làm tham số coroutine truyền giá trị (tham số sống *trong frame* — ngôi nhà an toàn).

## Quy tắc vòng đời dễ đoán

1. Tham số coroutine an toàn **trong frame** nếu truyền bằng giá trị/move.
2. Bất cứ thứ gì được tham chiếu (tham số bằng &, capture bằng &) phải chứng minh được sống lâu hơn generator — cùng kỷ luật với view.
3. Đối tượng generator sở hữu handle; di chuyển generator là di chuyển quyền sở hữu; bản bị move không được resume hay hủy hai lần (`std::exchange` trong move, như code trong bài học).
4. Hủy (hoặc để RAII hủy) **trước khi** môi trường được tham chiếu chết.

Bài tập chấm điểm: sửa chính xác generator bị dangling-capture, rồi dự đoán đoạn nào trong các đoạn cho sẵn bị dangling.
''',
    difficulty="advanced",
)

# ---- module 7 practices ----
GEN_BOILER = r'''#include <coroutine>
#include <cstddef>
#include <exception>
#include <utility>

// TODO: implement the Generator<T> class from the lesson:
//   promise_type with current_, get_return_object, initial/final suspend_always,
//   yield_value storing by move, return_void, unhandled_exception -> std::terminate;
//   move-only wrapper owning the handle; next() resume+done check; value() read.
template <class T>
class Generator;

// TODO: implement with co_yield: from, from+1, ..., to (inclusive; empty if from > to).
Generator<int> counter(int from, int to);
'''

CH_GEN_COUNTER = challenge(
    "cppa7-generator-counter",
    "Build Generator<int> from Scratch",
    "Implement the full `Generator<T>` from the lesson (promise, handle wrapper, RAII) and the `counter(from, to)` coroutine with `co_yield`. The graded checks resume it exactly and expect exact values.",
    GEN_BOILER,
    [
        ("counter yields an inclusive range",
         r'''Generator<int> g = counter(1, 4);
std::string got;
while (g.next()) got += std::to_string(g.value()) + ",";
CHECK_EQ(got, std::string("1,2,3,4,"));''',
         "for (int i = from; i <= to; ++i) co_yield i; — with from > to the loop never runs and every next() returns false."),
        ("empty range is truly empty",
         r'''Generator<int> e = counter(5, 4);
CHECK_EQ(e.next(), false);''',
         "The body runs once (resume), the for-condition fails immediately, final_suspend pauses, done() is true — no value ever stored."),
        ("two generators do not interfere",
         r'''Generator<int> a = counter(1, 2);
Generator<int> b = counter(10, 11);
CHECK_EQ(a.value() + b.value(), 0);  // values only valid after first next()
CHECK_EQ(a.next(), true);
CHECK_EQ(a.value(), 1);
CHECK_EQ(b.next(), true);
CHECK_EQ(b.value(), 10);''',
         "Each coroutine has its own frame and promise — frames are independent by construction."),
    ],
    difficulty="advanced",
)

VI_GEN_COUNTER = vi_challenge(
    "Dựng Generator<int> từ đầu",
    "Cài đầy đủ `Generator<T>` theo bài học (promise, wrapper handle, RAII) và coroutine `counter(from, to)` bằng `co_yield`. Các bài kiểm tra resume chính xác từng bước và đòi giá trị chính xác.",
    [
        ("counter yield dải bao hai đầu", "for (int i = from; i <= to; ++i) co_yield i; — với from > to vòng lặp không chạy và mọi next() trả false."),
        ("dải rỗng là rỗng thật", "Thân hàm chạy một lần (resume), điều kiện for sai ngay, final_suspend treo, done() true — không giá trị nào được lưu."),
        ("hai generator không nhiễu nhau", "Mỗi coroutine có frame và promise riêng — các frame độc lập bởi cấu trúc."),
    ],
)

CH_GEN_FIB = challenge(
    "cppa7-generator-fib",
    "A Stateful Fibonacci Generator",
    "With your `Generator<T>` from the previous exercise, implement `fibonacci(n)` yielding the first n Fibonacci numbers (1, 1, 2, 3, 5, ...).",
    GEN_BOILER + "\n// TODO: yield the first n Fibonacci numbers (n >= 0).\nGenerator<long long> fibonacci(int n);\n",
    [
        ("first values are exact",
         r'''Generator<long long> f = fibonacci(7);
std::string got;
while (f.next()) got += std::to_string(f.value()) + ",";
CHECK_EQ(got, std::string("1,1,2,3,5,8,13,"));''',
         "long long a = 1, b = 1; for (int i = 0; i < n; ++i) { co_yield a; auto t = a + b; a = b; b = t; }"),
        ("n = 0 and n = 1",
         r'''Generator<long long> z = fibonacci(0);
CHECK_EQ(z.next(), false);
Generator<long long> o = fibonacci(1);
CHECK_EQ(o.next(), true);
CHECK_EQ(o.value(), 1);
CHECK_EQ(o.next(), false);''',
         "The loop bounds handle the degenerate cases naturally."),
    ],
    difficulty="advanced",
)

VI_GEN_FIB = vi_challenge(
    "Generator Fibonacci có trạng thái",
    "Với `Generator<T>` của bài trước, cài `fibonacci(n)` yield n số Fibonacci đầu tiên (1, 1, 2, 3, 5, ...).",
    [
        ("các giá trị đầu chính xác", "long long a = 1, b = 1; for (int i = 0; i < n; ++i) { co_yield a; auto t = a + b; a = b; b = t; }"),
        ("n = 0 và n = 1", "Biên vòng lặp tự xử các trường hợp suy biến."),
    ],
)

CH_GEN_CAPTURE_FIX = challenge(
    "cppa7-generator-capture-fix",
    "Repair the Dangling Capture",
    "This starter's generator captures a local **by reference** and dangles. Repair `makeCounter` so the state lives inside the coroutine frame (by-value parameter) — the graded check forces a resumption that would read dead memory in the original.",
    GEN_BOILER + r'''
// TODO: repair — the parameter must travel inside the frame.
Generator<int> makeCounter(int start);
''',
    [
        ("state survives the return",
         r'''Generator<int> g = makeCounter(10);
std::string got;
while (g.next()) got += std::to_string(g.value()) + ",";
CHECK_EQ(got, std::string("10,11,12,"));''',
         "Generator<int> makeCounter(int start) { for (int i = 0; i < 3; ++i) co_yield start + i; } — start lives in the frame; no captures at all."),
    ],
    difficulty="advanced",
)

VI_GEN_CAPTURE_FIX = vi_challenge(
    "Sửa capture bị dangling",
    "Generator trong code khởi đầu bắt một biến cục bộ **bằng tham chiếu** và bị dangling. Hãy sửa `makeCounter` để trạng thái nằm trong frame coroutine (tham số truyền giá trị) — bài kiểm tra ép một lần resume mà bản gốc sẽ đọc vào bộ nhớ chết.",
    [
        ("trạng thái sống qua lời return", "Generator<int> makeCounter(int start) { for (int i = 0; i < 3; ++i) co_yield start + i; } — start sống trong frame; không cần capture nào."),
    ],
)

M7_PRAC1 = dict(
    sid="m7-generator-practice",
    title="Hands on the Handle",
    description="Build Generator<T> from raw primitives, then use it for a range, a stateful sequence, and a repaired capture.",
    vi_title="Đặt tay lên handle",
    vi_description="Dựng Generator<T> từ các nguyên thủy thô, rồi dùng nó cho một dải, một dãy có trạng thái, và một bản sửa capture.",
    after_lesson=L7B,
    minutes=30,
    difficulty="advanced",
)

M7_PRAC1_CH = [CH_GEN_COUNTER, CH_GEN_FIB, CH_GEN_CAPTURE_FIX]
M7_PRAC1_VI = {"cppa7-generator-counter": VI_GEN_COUNTER,
               "cppa7-generator-fib": VI_GEN_FIB,
               "cppa7-generator-capture-fix": VI_GEN_CAPTURE_FIX}

M7_PRAC1_SOL = [
    ("cppa7-generator-counter",
     r'''#include <coroutine>
#include <cstddef>
#include <exception>
#include <utility>

template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}
''',
     r'''#include <coroutine>
#include <cstddef>
#include <exception>
#include <utility>

template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_never initial_suspend() noexcept { return {}; }   // WRONG: eager start breaks laziness
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}
'''),
    ("cppa7-generator-fib",
     GEN_BOILER + r'''
template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}

Generator<long long> fibonacci(int n) {
    long long a = 1, b = 1;
    for (int i = 0; i < n; ++i) {
        co_yield a;
        auto t = a + b;
        a = b;
        b = t;
    }
}
''',
     GEN_BOILER + r'''
template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}

Generator<long long> fibonacci(int n) {
    long long a = 0, b = 1;   // WRONG: starts at 0 -> "0,1,1,2,..."
    for (int i = 0; i < n; ++i) {
        co_yield a;
        auto t = a + b;
        a = b;
        b = t;
    }
}
'''),
    ("cppa7-generator-capture-fix",
     GEN_BOILER + r'''
template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}

Generator<int> makeCounter(int start) {
    for (int i = 0; i < 3; ++i) co_yield start + i;
}
''',
     GEN_BOILER + r'''
template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}

Generator<int> makeCounter(int start) {
    int state = start;
    return [&state]() -> Generator<int> {   // WRONG: dangling by-ref capture
        for (int i = 0; i < 3; ++i) co_yield state + i;
    }();
}
'''),
]

write_practice(M7, **M7_PRAC1, challenges=M7_PRAC1_CH, vi_challenges=M7_PRAC1_VI, solutions=M7_PRAC1_SOL)

M7_PRAC2 = dict(
    sid="m7-lifetime-practice",
    title="Coroutine Lifetime Clinic",
    description="Move-only ownership, single-consumption discipline, and the frame-allocation mental model.",
    vi_title="Phòng khám vòng đời coroutine",
    vi_description="Quyền sở hữu move-only, kỷ luật tiêu thụ một lần, và mô hình tư duy cấp phát frame.",
    after_lesson=L7C,
    minutes=16,
    difficulty="advanced",
)

CH_GEN_TAKE = challenge(
    "cppa7-generator-take",
    "A Consuming take() Adapter",
    "With your `Generator<T>` intact, implement `take(Generator<int> src, int n)` — a **move-only** function returning a Generator that yields at most n values from src. This grades the ownership rule: the adapter must own src by move.",
    GEN_BOILER + "\n// TODO: yield at most n values of src (src is consumed by move).\nGenerator<int> take(Generator<int> src, int n);\n",
    [
        ("take limits the count",
         r'''Generator<int> t = take(counter(1, 100), 3);
std::string got;
while (t.next()) got += std::to_string(t.value()) + ",";
CHECK_EQ(got, std::string("1,2,3,"));''',
         "Inside the coroutine, loop i in [0, n): if (!src.next()) break; co_yield src.value(); — src is a coroutine parameter, so it lives inside the frame (the safe home from the lesson)."),
        ("take of more than available",
         r'''Generator<int> t = take(counter(1, 2), 10);
std::string got;
while (t.next()) got += std::to_string(t.value()) + ",";
CHECK_EQ(got, std::string("1,2,"));''',
         "The break on !src.next() handles exhaustion before n is reached."),
    ],
    difficulty="advanced",
)

VI_GEN_TAKE = vi_challenge(
    "Bộ chuyển take() tiêu thụ",
    "Giữ nguyên `Generator<T>`, cài `take(Generator<int> src, int n)` — hàm **move-only** trả về một Generator yield tối đa n giá trị từ src. Bài kiểm tra chấm quy tắc sở hữu: adapter phải sở hữu src bằng move.",
    [
        ("take giới hạn số lượng", "Trong coroutine, duyệt i trong [0, n): if (!src.next()) break; co_yield src.value(); — src là tham số coroutine nên sống trong frame (ngôi nhà an toàn trong bài học)."),
        ("take nhiều hơn số có sẵn", "Lệnh break khi !src.next() xử lý việc cạn nguồn trước khi đủ n."),
    ],
)

M7_PRAC2_CH = [CH_GEN_TAKE]
M7_PRAC2_VI = {"cppa7-generator-take": VI_GEN_TAKE}

M7_PRAC2_SOL = [
    ("cppa7-generator-take",
     GEN_BOILER + r'''
template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}

Generator<int> take(Generator<int> src, int n) {
    for (int i = 0; i < n; ++i) {
        if (!src.next()) break;
        co_yield src.value();
    }
}
''',
     GEN_BOILER + r'''
template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}

Generator<int> take(Generator<int> src, int n) {
    for (int i = 0; i < n; ++i) {
        src.next();                       // WRONG: ignores exhaustion -> resumes a done frame (UB)
        co_yield src.value();
    }
}
'''),
]

write_practice(M7, **M7_PRAC2, challenges=M7_PRAC2_CH, vi_challenges=M7_PRAC2_VI, solutions=M7_PRAC2_SOL)

# ---- module 7 checkpoint ----
CP7_MD = r'''
The coroutines checkpoint: a filtering adapter over your Generator, exact resumption semantics graded.
'''

CP7_BOILER = GEN_BOILER + "\n// TODO: yield only the even values of src, in order (src consumed by move).\nGenerator<int> evens(Generator<int> src);\n"

write_checkpoint(
    M7, L7D,
    "Checkpoint: Coroutines",
    "Prove the full machinery: build the Generator, then compose a filtering adapter over it.",
    18,
    CP7_MD,
    "Checkpoint: Coroutines",
    "Chứng minh trọn bộ cơ chế: dựng Generator, rồi kết hợp một adapter lọc phía trên.",
    r'''
Checkpoint coroutines: adapter lọc trên Generator của bạn, ngữ nghĩa resume chính xác được chấm điểm.
''',
    challenge(
        "cppa7-coroutines-checkpoint",
        "Coroutine Gauntlet",
        "Implement Generator<T> + counter (as in the lesson) and the `evens` filtering adapter (consumes src by move).",
        CP7_BOILER,
        [
            ("counter yields inclusively",
             r'''Generator<int> c = counter(0, 5);
std::string got;
while (c.next()) got += std::to_string(c.value()) + ",";
CHECK_EQ(got, std::string("0,1,2,3,4,5,"));''',
             "The lesson's generator verbatim; the counter body is a simple inclusive for-loop with co_yield."),
            ("evens filters through the frame",
             r'''Generator<int> e = evens(counter(1, 7));
std::string got;
while (e.next()) got += std::to_string(e.value()) + ",";
CHECK_EQ(got, std::string("2,4,6,"));''',
             "Generator<int> evens(Generator<int> src) { while (src.next()) if (src.value() % 2 == 0) co_yield src.value(); } — src lives in the frame; the while ends the coroutine when src exhausts."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Vượt chướng ngại coroutine",
        "Cài Generator<T> + counter (như bài học) và adapter lọc `evens` (tiêu thụ src bằng move).",
        [
            ("counter yield trọn dải", "Generator trong bài học nguyên văn; thân counter là vòng for bao hai đầu đơn giản với co_yield."),
            ("evens lọc qua frame", "Generator<int> evens(Generator<int> src) { while (src.next()) if (src.value() % 2 == 0) co_yield src.value(); } — src sống trong frame; while kết thúc coroutine khi src cạn."),
        ],
    ),
    solution=CP7_BOILER + r'''
template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}

Generator<int> evens(Generator<int> src) {
    while (src.next()) {
        if (src.value() % 2 == 0) co_yield src.value();
    }
}
''',
    wrong=CP7_BOILER + r'''
template <class T>
class Generator {
public:
    struct promise_type {
        T current_{};
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }   // WRONG: self-destroying frame
        std::suspend_always yield_value(T v) { current_ = std::move(v); return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    explicit Generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    Generator& operator=(Generator&&) = delete;
    ~Generator() { if (h_) h_.destroy(); }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().current_; }
private:
    std::coroutine_handle<promise_type> h_;
};

Generator<int> counter(int from, int to) {
    for (int i = from; i <= to; ++i) co_yield i;
}

Generator<int> evens(Generator<int> src) {
    while (src.next()) {
        if (src.value() % 2 == 0) co_yield src.value();
    }
}
''',
)

print("module 7 done")
