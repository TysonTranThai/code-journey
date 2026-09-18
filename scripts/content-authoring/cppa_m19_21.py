#!/usr/bin/env python3
"""C++ Advanced — module 19 (architecture-production), 20 (observability-production), 21 (capstone-hpc-service).

Module 19 grades architecture mechanics (dependency inversion with DI seams,
event bus with deterministic dispatch, config precedence ladder).
Module 20 grades observability math (health, metrics correctness, structured
logging, graceful shutdown sequencing).
Module 21 is the open-ended capstone (brief + ship), graded on a real
engineering kernel: a rate-limiter token bucket + a bounded cache with
correct eviction accounting.
"""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 19: architecture-production ============================
M19 = "architecture-production"

L19A = "boundaries-and-inversion"
L19B = "events-and-config"
L19C = "cppa-checkpoint-arch"

write_module(
    M19,
    "Architecture & Production",
    "Dependency inversion with real seams, event-driven decoupling, and configuration precedence — the structure that keeps large C++ systems changeable.",
    "Kiến Trúc & Production",
    "Đảo ngược dependency với seam thật, tách rời bằng event, và thứ tự ưu tiên cấu hình — cấu trúc giữ cho hệ thống C++ lớn luôn thay đổi được.",
    [L19A, L19B, L19C],
    ["m19-arch-practice"],
)

write_lesson(
    M19, L19A,
    "Boundaries & Dependency Inversion",
    "High-level policy depends on interfaces; details plug in from below. The seam is what you can test, swap, and version.",
    12,
    r'''
## The dependency rule

Business logic must not include storage, transport, or vendor headers. It defines the interface it *needs*; an adapter below implements it:

```cpp
struct Clock {                      // the seam — owned by the logic layer
    virtual ~Clock() = default;
    virtual std::int64_t nowMs() const = 0;
};

struct RateLimiter {                // high-level policy, testable
    explicit RateLimiter(const Clock* clock) : clock_(clock) {}
    bool allow(std::int64_t nowMs); // deterministic under a fake clock
    const Clock* clock_;
};
```

Production binds a real clock at composition time; tests bind a fake. The seam is why the logic is deterministic, and determinism is why it is testable — flaky time-based tests are a missing seam, not bad luck.

## Interfaces at boundaries

An abstract interface is also an ABI boundary (module 16): the vtable layout is the contract. Keep them small, stable, and versioned — a wide interface that grows entry-by-entry is how vtables end up "frozen forever".

## What belongs where

- **Domain**: types + rules, no I/O includes.
- **Adapters**: DB/queue/fs implementations of domain interfaces.
- **Composition root**: the one place that wires concrete types.

When a new requirement touches three layers, ask which dependency pointed the wrong way.
''',
    "Ranh Giới & Đảo Ngược Dependency",
    "Chính sách cấp cao phụ thuộc interface; chi tiết cắm vào từ phía dưới. Seam là thứ bạn test được, hoán đổi được, và phiên bản hóa được.",
    r'''
## Quy tắc dependency

Business logic không được include storage, transport, hay vendor header. Nó định nghĩa interface mà nó *cần*; một adapter phía dưới cài đặt:

```cpp
struct Clock {                      // seam — thuộc sở hữu của tầng logic
    virtual ~Clock() = default;
    virtual std::int64_t nowMs() const = 0;
};

struct RateLimiter {                // chính sách cấp cao, test được
    explicit RateLimiter(const Clock* clock) : clock_(clock) {}
    bool allow(std::int64_t nowMs); // xác định dưới fake clock
    const Clock* clock_;
};
```

Production gắn clock thật lúc compose; test gắn fake. Seam là lý do logic xác định, và tính xác định là lý do nó test được — test theo thời gian hay flaky là thiếu seam, không phải xui xẻo.

## Interface ở biên giới

Interface trừu tượng cũng là biên giới ABI (module 16): layout vtable chính là hợp đồng. Giữ chúng nhỏ, ổn định, có phiên bản — interface rộng lớn dần từng mục là cách vtable bị "đóng băng vĩnh viễn".

## Cái gì nằm ở đâu

- **Domain**: kiểu + quy tắc, không include I/O.
- **Adapter**: cài đặt DB/queue/fs của interface domain.
- **Composition root**: duy nhất một nơi nối các kiểu cụ thể.

Khi một yêu cầu mới chạm ba tầng, hãy hỏi dependency nào đang chỉ sai hướng.
''',
)

write_lesson(
    M19, L19B,
    "Events & Configuration",
    "Event buses decouple components in *time*; configuration ladders decide truth in *layers*. Both must be deterministic to be debuggable.",
    11,
    r'''
## Event-driven decoupling

A synchronous direct call couples the caller to the callee's lifetime, latency, and failure. An event bus breaks those: publishers emit facts (`"OrderPlaced{...}"`), subscribers react. The cost is dispatch ordering — a serious bus *documents and guarantees* its order (registration order for sync buses is the common deterministic choice), because "usually fine" ordering is a production incident generator.

## The configuration ladder

Real systems resolve config in layers with defined precedence — the common ladder:

```
defaults  <  file  <  environment  <  explicit flag
```

Each layer overrides the previous *only where it speaks*. Debugging misconfiguration means asking, per key: "which layer set this?" A config system that cannot answer that question is a rumour mill.

## Secrets never ride the ladder

Values from secret stores must never be logged, never land in error messages, and never become part of a string you format. Redaction is a *sink* responsibility (the logging layer), but the config layer's job is to mark secrets so the sink can.

## What the sandbox grades

The exercises grade the mechanics: a DI seam that makes time-based logic deterministic, an event bus with registration-order dispatch and unsubscribe, and a precedence ladder you can interrogate per key.
''',
    "Event & Cấu Hình",
    "Event bus tách rời các thành phần theo *thời gian*; thang cấu hình quyết định sự thật theo *tầng*. Cả hai phải xác định để debug được.",
    r'''
## Tách rời bằng event

Gọi trực tiếp đồng bộ buộc caller vào vòng đời, độ trễ, và thất bại của callee. Event bus phá các ràng buộc đó: publisher phát sự kiện (`"OrderPlaced{...}"`), subscriber phản ứng. Cái giá là thứ tự dispatch — một bus nghiêm túc *ghi nhận và đảm bảo* thứ tự của nó (thứ tự đăng ký là lựa chọn xác định phổ biến cho bus đồng bộ), vì thứ tự "thường ổn" là máy tạo sự cố production.

## Thang cấu hình

Hệ thống thật phân giải config theo tầng với thứ tự ưu tiên rõ — thang phổ biến:

```
defaults  <  file  <  environment  <  cờ tường minh
```

Mỗi tầng ghi đè tầng dưới *chỉ ở những key nó nói tới*. Debug cấu hình sai nghĩa là hỏi, theo từng key: "tầng nào đã đặt giá trị này?" Một hệ cấu hình không trả lời được câu đó chỉ là tin đồn.

## Secret không đi trên thang

Giá trị từ secret store không bao giờ được log, không bao giờ lọt vào thông báo lỗi, không bao giờ thành một chuỗi bạn format. Việc che giấu là trách nhiệm của *sink* (tầng log), nhưng tầng config phải đánh dấu secret để sink có thể che.

## Sandbox chấm gì

Bài tập chấm cơ chế: seam DI biến logic theo thời gian thành xác định, event bus dispatch theo thứ tự đăng ký và có unsubscribe, và thang ưu tiên có thể truy vấn theo từng key.
''',
)

# ---------------- practice: seam + bus + ladder ----------------
CP19_BOILER = r'''#include <algorithm>
#include <cstdint>
#include <map>
#include <functional>
#include <optional>
#include <string>
#include <vector>

// --- deterministic time seam ---
struct Clock {
    virtual ~Clock() = default;
    virtual std::int64_t nowMs() const = 0;
};
struct FixedClock : Clock {                 // test double
    explicit FixedClock(std::int64_t t) : t_(t) {}
    std::int64_t nowMs() const override { return t_; }
    void advance(std::int64_t ms) { t_ += ms; }
private:
    std::int64_t t_;
};

// --- token bucket over the seam ---
struct TokenBucket {
    TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec);
    // true and consumes one token if allowed; false otherwise.
    bool tryConsume();
    std::int64_t tokens() const;

private:
    const Clock* clock_;
    std::int64_t capacity_;
    std::int64_t refillPerSec_;   // tokens per second
    double tokens_ = 0.0;
    std::int64_t lastMs_ = 0;
};

// --- sync event bus, registration-order dispatch ---
struct EventBus {
    using Handler = std::function<void(const std::string&)>;

    int subscribe(Handler h);          // returns a subscription id
    bool unsubscribe(int id);          // true if it existed
    void emit(const std::string& event) const;   // calls handlers in subscription order

private:
    std::vector<std::pair<int, Handler>> handlers_;
    int nextId_ = 1;
};

// --- configuration ladder: defaults < file < env < flag ---
enum class Layer { Default, File, Env, Flag };

struct ConfigLadder {
    void set(Layer l, const std::string& key, const std::string& value);
    std::optional<std::string> get(const std::string& key) const;   // highest layer wins
    std::optional<Layer> source(const std::string& key) const;      // which layer set it

private:
    std::map<std::string, std::pair<Layer, std::string>> entries_;
};
'''

M19_PRAC1_CH = [
    challenge(
        "cppa19-token-bucket",
        "Token Bucket on a Fake Clock",
        "Implement `TokenBucket` (refill proportional to elapsed ms, capped at capacity, floor at consumption time) so the whole battery is deterministic under `FixedClock`.",
        CP19_BOILER,
        [
            ("deterministic refill battery",
             r'''{
    FixedClock clk(0);
    TokenBucket b(&clk, 3, 1);       // cap 3, +1/sec
    clk.advance(1000);               // construction at t=0 -> now t=1s, bucket full
    CHECK(b.tryConsume());
    CHECK(b.tryConsume());
    CHECK(b.tryConsume());
    CHECK(!b.tryConsume());          // empty
    clk.advance(500);
    CHECK(!b.tryConsume());          // half a second: no whole token yet
    clk.advance(500);
    CHECK(b.tryConsume());           // one token refilled
    CHECK(!b.tryConsume());
}
{
    FixedClock clk(0);
    TokenBucket b(&clk, 2, 10);      // fast refill
    clk.advance(200);                // 2 tokens worth
    CHECK(b.tryConsume());
    CHECK(b.tryConsume());
    CHECK(!b.tryConsume());
}''',
             "On construction: tokens_ = capacity_, lastMs_ = now. tryConsume: tokens_ = min(capacity_, tokens_ + elapsedMs/1000.0 * refillPerSec_); if tokens_ >= 1, --tokens_ and true. Store tokens_ as double; test uses whole-second windows so results are exact."),
        ],
        difficulty="advanced",
    ),
    challenge(
        "cppa19-event-bus",
        "Deterministic Event Bus",
        "Implement `EventBus`: subscription ids, registration-order dispatch, unsubscribe mid-flight (an unsubscribed handler must not fire for the current event).",
        CP19_BOILER,
        [
            ("ordering + unsubscribe battery",
             r'''{
    EventBus bus;
    std::vector<std::string> log;
    int a = bus.subscribe([&](const std::string& e) { log.push_back("a:" + e); });
    int b = bus.subscribe([&](const std::string& e) { log.push_back("b:" + e); });
    bus.emit("go");
    CHECK_EQ(log.size(), 2);
    CHECK_EQ(log[0], "a:go");
    CHECK_EQ(log[1], "b:go");
    CHECK(bus.unsubscribe(b));
    CHECK(!bus.unsubscribe(b));      // double unsubscribe fails
    log.clear();
    bus.emit("again");
    CHECK_EQ(log.size(), 1);
    CHECK_EQ(log[0], "a:again");
}
{
    EventBus bus;
    std::vector<std::string> log;
    int cId = 0;
    bus.subscribe([&](const std::string& e) { log.push_back("a:" + e); if (e == "cut") bus.unsubscribe(cId); });
    bus.subscribe([&](const std::string& e) { log.push_back("b:" + e); });
    cId = bus.subscribe([&](const std::string& e) { log.push_back("c:" + e); });
    bus.emit("cut");
    CHECK_EQ(log.size(), 2);                       // c was cut mid-flight
    CHECK_EQ(log[0], "a:cut"); CHECK_EQ(log[1], "b:cut");
}''',
             "handlers_ is a vector of (id, handler) pairs; emit iterates a COPY or index-guarded loop and skips ids removed during dispatch. unsubscribe erases by id and returns whether it was present."),
        ],
        difficulty="advanced",
    ),
    challenge(
        "cppa19-config-ladder",
        "Configuration Ladder",
        "Implement `ConfigLadder` with Default < File < Env < Flag precedence and per-key provenance queries.",
        CP19_BOILER,
        [
            ("precedence + provenance battery",
             r'''{
    ConfigLadder c;
    c.set(Layer::Default, "port", "8080");
    c.set(Layer::File, "port", "9090");
    CHECK_EQ(c.get("port").value_or("?"), "9090");
    CHECK(c.source("port").value_or(Layer::Default) == Layer::File);
    c.set(Layer::Env, "port", "7070");
    CHECK_EQ(c.get("port").value_or("?"), "7070");
    c.set(Layer::Flag, "port", "6060");
    CHECK_EQ(c.get("port").value_or("?"), "6060");
    CHECK(c.source("port").value_or(Layer::Default) == Layer::Flag);
    CHECK(!c.get("missing").has_value());
    CHECK(!c.source("missing").has_value());
    c.set(Layer::File, "other", "x");           // lower layer speaks later
    CHECK_EQ(c.get("port").value_or("?"), "6060");   // Flag still wins
    CHECK_EQ(c.get("other").value_or("?"), "x");
    c.set(Layer::Env, "port", "5555");              // lower layer speaks last for an existing key
    CHECK_EQ(c.get("port").value_or("?"), "6060");   // Flag still wins
    CHECK(c.source("port").value_or(Layer::Default) == Layer::Flag);
    c.set(Layer::Flag, "port", "6161");             // equal layer re-set overwrites
    CHECK_EQ(c.get("port").value_or("?"), "6161");
}''',
             "One map key -> (layer, value). set: overwrite only if the new layer >= stored layer (or key absent). get/source read the map."),
        ],
        difficulty="advanced",
    ),
]

M19_PRAC1_VI = {
    "cppa19-token-bucket": vi_challenge(
        "Token Bucket Trên Fake Clock",
        "Cài `TokenBucket` (refill tỉ lệ theo ms trôi qua, chặn tại capacity, lấy sàn lúc tiêu) để cả bộ test xác định dưới `FixedClock`.",
        [("deterministic refill battery",
          "Khởi tạo: tokens_ = capacity_, lastMs_ = now. tryConsume: tokens_ = min(capacity_, tokens_ + elapsedMs/1000.0 * refillPerSec_); nếu tokens_ >= 1, --tokens_ và true. Giữ tokens_ kiểu double; test dùng cửa sổ tròn giây nên kết quả chính xác.")],
    ),
    "cppa19-event-bus": vi_challenge(
        "Event Bus Xác Định",
        "Cài `EventBus`: id đăng ký, dispatch theo thứ tự đăng ký, unsubscribe giữa chừng (handler đã hủy không được bắn với event hiện tại).",
        [("ordering + unsubscribe battery",
          "handlers_ là vector cặp (id, handler); emit duyệt bản SAO CHÉP hoặc vòng có guard theo index và bỏ qua id bị xóa trong lúc dispatch. unsubscribe xóa theo id và trả về có tồn tại hay không.")],
    ),
    "cppa19-config-ladder": vi_challenge(
        "Thang Cấu Hình",
        "Cài `ConfigLadder` với thứ tự Default < File < Env < Flag và truy vấn nguồn theo từng key.",
        [("precedence + provenance battery",
          "Một map key -> (layer, value). set: chỉ ghi đè khi tầng mới >= tầng đã lưu (hoặc key chưa có). get/source đọc map.")],
    ),
}

M19_PRAC1_SOL = [
    ("cppa19-token-bucket",
     CP19_BOILER + 'TokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)\n    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}\nbool TokenBucket::tryConsume() {\n    const std::int64_t now = clock_->nowMs();\n    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);\n    lastMs_ = now;\n    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }\n    return false;\n}\nstd::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }\nint EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }\nbool EventBus::unsubscribe(int id) {\n    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)\n        if (it->first == id) { handlers_.erase(it); return true; }\n    return false;\n}\nvoid EventBus::emit(const std::string& event) const {\n    auto snapshot = handlers_;\n    for (auto& [id, h] : snapshot) {\n        auto it = std::find_if(handlers_.begin(), handlers_.end(),\n                               [id](const auto& p) { return p.first == id; });\n        if (it != handlers_.end()) h(event);\n    }\n}\nvoid ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {\n    auto it = entries_.find(key);\n    if (it == entries_.end() || int(l) >= int(it->second.first))\n        entries_[key] = {l, value};\n}\nstd::optional<std::string> ConfigLadder::get(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.second;\n}\nstd::optional<Layer> ConfigLadder::source(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.first;\n}',
     CP19_BOILER + 'TokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)\n    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}\nbool TokenBucket::tryConsume() {\n    const std::int64_t now = clock_->nowMs();\n    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);\n    // WRONG: lastMs_ never advances — refill computed from a stale epoch\n    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }\n    return false;\n}\nstd::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }\nint EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }\nbool EventBus::unsubscribe(int id) {\n    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)\n        if (it->first == id) { handlers_.erase(it); return true; }\n    return false;\n}\nvoid EventBus::emit(const std::string& event) const {\n    auto snapshot = handlers_;\n    for (auto& [id, h] : snapshot) {\n        auto it = std::find_if(handlers_.begin(), handlers_.end(),\n                               [id](const auto& p) { return p.first == id; });\n        if (it != handlers_.end()) h(event);\n    }\n}\nvoid ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {\n    auto it = entries_.find(key);\n    if (it == entries_.end() || int(l) >= int(it->second.first))\n        entries_[key] = {l, value};\n}\nstd::optional<std::string> ConfigLadder::get(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.second;\n}\nstd::optional<Layer> ConfigLadder::source(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.first;\n}'),
    ("cppa19-event-bus",
     CP19_BOILER + 'TokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)\n    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}\nbool TokenBucket::tryConsume() {\n    const std::int64_t now = clock_->nowMs();\n    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);\n    lastMs_ = now;\n    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }\n    return false;\n}\nstd::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }\nint EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }\nbool EventBus::unsubscribe(int id) {\n    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)\n        if (it->first == id) { handlers_.erase(it); return true; }\n    return false;\n}\nvoid EventBus::emit(const std::string& event) const {\n    auto snapshot = handlers_;\n    for (auto& [id, h] : snapshot) {\n        auto it = std::find_if(handlers_.begin(), handlers_.end(),\n                               [id](const auto& p) { return p.first == id; });\n        if (it != handlers_.end()) h(event);\n    }\n}\nvoid ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {\n    auto it = entries_.find(key);\n    if (it == entries_.end() || int(l) >= int(it->second.first))\n        entries_[key] = {l, value};\n}\nstd::optional<std::string> ConfigLadder::get(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.second;\n}\nstd::optional<Layer> ConfigLadder::source(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.first;\n}',
     CP19_BOILER + 'TokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)\n    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}\nbool TokenBucket::tryConsume() {\n    const std::int64_t now = clock_->nowMs();\n    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);\n    lastMs_ = now;\n    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }\n    return false;\n}\nstd::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }\nint EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }\nbool EventBus::unsubscribe(int id) {\n    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)\n        if (it->first == id) { handlers_.erase(it); return true; }\n    return false;\n}\nvoid EventBus::emit(const std::string& event) const {\n    // WRONG: snapshot without re-check — a handler cut mid-flight still fires\n    auto snapshot = handlers_;\n    for (auto& [id, h] : snapshot) h(event);\n}\nvoid ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {\n    auto it = entries_.find(key);\n    if (it == entries_.end() || int(l) >= int(it->second.first))\n        entries_[key] = {l, value};\n}\nstd::optional<std::string> ConfigLadder::get(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.second;\n}\nstd::optional<Layer> ConfigLadder::source(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.first;\n}'),
]

M19_PRAC2_CH = [
    challenge(
        "cppa19-config-ladder",
        "Configuration Ladder",
        "Implement `ConfigLadder` with Default < File < Env < Flag precedence and per-key provenance queries.",
        CP19_BOILER,
        [
            ("precedence + provenance battery",
             r'''{
    ConfigLadder c;
    c.set(Layer::Default, "port", "8080");
    c.set(Layer::File, "port", "9090");
    CHECK_EQ(c.get("port").value_or("?"), "9090");
    CHECK(c.source("port").value_or(Layer::Default) == Layer::File);
    c.set(Layer::Env, "port", "7070");
    CHECK_EQ(c.get("port").value_or("?"), "7070");
    c.set(Layer::Flag, "port", "6060");
    CHECK_EQ(c.get("port").value_or("?"), "6060");
    CHECK(c.source("port").value_or(Layer::Default) == Layer::Flag);
    CHECK(!c.get("missing").has_value());
    CHECK(!c.source("missing").has_value());
    c.set(Layer::File, "other", "x");
    CHECK_EQ(c.get("port").value_or("?"), "6060");
    CHECK_EQ(c.get("other").value_or("?"), "x");
    c.set(Layer::Env, "port", "5555");              // lower layer speaks last for an existing key
    CHECK_EQ(c.get("port").value_or("?"), "6060");   // Flag still wins
    CHECK(c.source("port").value_or(Layer::Default) == Layer::Flag);
    c.set(Layer::Flag, "port", "6161");             // equal layer re-set overwrites
    CHECK_EQ(c.get("port").value_or("?"), "6161");
}''',
             "One map key -> (layer, value). set: overwrite only if the new layer >= stored layer (or key absent). get/source read the map."),
        ],
        difficulty="advanced",
    ),
]

M19_PRAC2_VI = {
    "cppa19-config-ladder": vi_challenge(
        "Thang Cấu Hình",
        "Cài `ConfigLadder` với thứ tự Default < File < Env < Flag và truy vấn nguồn theo từng key.",
        [("precedence + provenance battery",
          "Một map key -> (layer, value). set: chỉ ghi đè khi tầng mới >= tầng đã lưu (hoặc key chưa có). get/source đọc map.")],
    ),
}

M19_PRAC2_SOL = [
    ("cppa19-config-ladder",
     CP19_BOILER + 'TokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)\n    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}\nbool TokenBucket::tryConsume() {\n    const std::int64_t now = clock_->nowMs();\n    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);\n    lastMs_ = now;\n    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }\n    return false;\n}\nstd::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }\nint EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }\nbool EventBus::unsubscribe(int id) {\n    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)\n        if (it->first == id) { handlers_.erase(it); return true; }\n    return false;\n}\nvoid EventBus::emit(const std::string& event) const {\n    auto snapshot = handlers_;\n    for (auto& [id, h] : snapshot) {\n        auto it = std::find_if(handlers_.begin(), handlers_.end(),\n                               [id](const auto& p) { return p.first == id; });\n        if (it != handlers_.end()) h(event);\n    }\n}\nvoid ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {\n    auto it = entries_.find(key);\n    if (it == entries_.end() || int(l) >= int(it->second.first))\n        entries_[key] = {l, value};\n}\nstd::optional<std::string> ConfigLadder::get(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.second;\n}\nstd::optional<Layer> ConfigLadder::source(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.first;\n}',
     CP19_BOILER + 'TokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)\n    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}\nbool TokenBucket::tryConsume() {\n    const std::int64_t now = clock_->nowMs();\n    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);\n    lastMs_ = now;\n    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }\n    return false;\n}\nstd::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }\nint EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }\nbool EventBus::unsubscribe(int id) {\n    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)\n        if (it->first == id) { handlers_.erase(it); return true; }\n    return false;\n}\nvoid EventBus::emit(const std::string& event) const {\n    auto snapshot = handlers_;\n    for (auto& [id, h] : snapshot) {\n        auto it = std::find_if(handlers_.begin(), handlers_.end(),\n                               [id](const auto& p) { return p.first == id; });\n        if (it != handlers_.end()) h(event);\n    }\n}\nvoid ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {\n    auto it = entries_.find(key);\n    entries_[key] = {l, value};                       // WRONG: last-writer-wins, layers ignored\n}\nstd::optional<std::string> ConfigLadder::get(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.second;\n}\nstd::optional<Layer> ConfigLadder::source(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.first;\n}'),
]

# ConfigLadder private members (used by solutions above)
# ---------------- write module 19 ----------------
write_practice(
    M19, "m19-arch-practice",
    "Practice: Architecture Mechanics",
    "A token bucket made deterministic by a clock seam, a bus whose dispatch order is a guarantee, and a config ladder with provenance.",
    "Luyện Tập: Cơ Chế Kiến Trúc",
    "Token bucket trở nên xác định nhờ clock seam, bus có thứ tự dispatch là lời đảm bảo, và thang cấu hình có truy vết.",
    L19A, 20, "advanced",
    challenges=M19_PRAC1_CH[:2], vi_challenges={k: M19_PRAC1_VI[k] for k in ("cppa19-token-bucket", "cppa19-event-bus")}, solutions=M19_PRAC1_SOL)

write_practice(
    M19, "m19-config-practice",
    "Practice: Configuration Ladder",
    "Precedence and provenance for per-key configuration truth.",
    "Luyện Tập: Thang Cấu Hình",
    "Ưu tiên và truy vết cho sự thật cấu hình theo từng key.",
    L19B, 10, "advanced",
    challenges=M19_PRAC2_CH, vi_challenges=M19_PRAC2_VI, solutions=M19_PRAC2_SOL)

write_checkpoint(
    M19, L19C,
    "Checkpoint — Architecture Reasoning",
    "The bus contract frozen, with the mid-flight unsubscribe case made explicit.",
    8,
    r'''
## What you must be able to do

Guarantee dispatch order and mid-flight unsubscribe semantics — the two details that decide whether an event bus is debuggable in production.
''',
    "Điểm Chốt — Suy Luận Kiến Trúc",
    "Hợp đồng bus đóng băng, với trường hợp unsubscribe giữa chừng được nêu tường minh.",
    r'''
## Bạn phải làm được gì

Đảm bảo thứ tự dispatch và ngữ nghĩa unsubscribe giữa chừng — hai chi tiết quyết định event bus có debug được trong production hay không.
''',
    challenge(
        "cppa19-arch-checkpoint",
        "Bus Semantics, Frozen",
        "Same `EventBus` contract (all other types available too). The battery interleaves subscribe/emit/unsubscribe and demands exact log contents.",
        CP19_BOILER,
        [
            ("interleaved + mid-flight battery",
             r'''{
    EventBus bus;
    std::vector<std::string> log;
    int aId = 0;
    int cId = 0;
    aId = bus.subscribe([&](const std::string& e) {
        log.push_back("a:" + e);
        if (e == "boom") { bus.unsubscribe(cId); bus.unsubscribe(aId); }
    });
    bus.subscribe([&](const std::string& e) { log.push_back("b:" + e); });
    cId = bus.subscribe([&](const std::string& e) { log.push_back("c:" + e); });
    bus.emit("ok");
    CHECK_EQ(log.size(), 3);
    CHECK_EQ(log[0], "a:ok"); CHECK_EQ(log[1], "b:ok"); CHECK_EQ(log[2], "c:ok");
    log.clear();
    bus.emit("boom");
    CHECK_EQ(log.size(), 2);                       // c was cut mid-flight
    CHECK_EQ(log[0], "a:boom"); CHECK_EQ(log[1], "b:boom");
    log.clear();
    bus.emit("again");
    CHECK_EQ(log.size(), 1);                       // a cut itself; only b remains
    CHECK_EQ(log[0], "b:again");
}''',
             "Snapshot then membership-check: emit iterates a copy but re-checks each id against the live list right before firing; ids are never reused."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Ngữ Nghĩa Bus, Đóng Băng",
        "Cùng hợp đồng `EventBus` (các kiểu khác cũng có sẵn). Bộ test xen kẽ subscribe/emit/unsubscribe và đòi nội dung log chính xác tuyệt đối.",
        [("interleaved battery",
          "Mẫu snapshot rồi kiểm tra thành viên từ bài luyện; id không bao giờ tái sử dụng.")],
    ),
    solution=CP19_BOILER + '\nTokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)\n    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}\nbool TokenBucket::tryConsume() {\n    const std::int64_t now = clock_->nowMs();\n    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);\n    lastMs_ = now;\n    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }\n    return false;\n}\nstd::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }\nint EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }\nbool EventBus::unsubscribe(int id) {\n    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)\n        if (it->first == id) { handlers_.erase(it); return true; }\n    return false;\n}\nvoid EventBus::emit(const std::string& event) const {\n    auto snapshot = handlers_;\n    for (auto& [id, h] : snapshot) {\n        auto it = std::find_if(handlers_.begin(), handlers_.end(),\n                               [id](const auto& p) { return p.first == id; });\n        if (it != handlers_.end()) h(event);\n    }\n}\nvoid ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {\n    auto it = entries_.find(key);\n    if (it == entries_.end() || int(l) >= int(it->second.first))\n        entries_[key] = {l, value};\n}\nstd::optional<std::string> ConfigLadder::get(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.second;\n}\nstd::optional<Layer> ConfigLadder::source(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.first;\n}\n',
    wrong=CP19_BOILER + 'TokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)\n    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}\nbool TokenBucket::tryConsume() {\n    const std::int64_t now = clock_->nowMs();\n    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);\n    lastMs_ = now;\n    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }\n    return false;\n}\nstd::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }\nint EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }\nbool EventBus::unsubscribe(int id) {\n    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)\n        if (it->first == id) { handlers_.erase(it); return true; }\n    return false;\n}\nvoid EventBus::emit(const std::string& event) const {\n    // WRONG: snapshot without re-check — a handler cut mid-flight still fires\n    auto snapshot = handlers_;\n    for (auto& [id, h] : snapshot) h(event);\n}\nvoid ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {\n    auto it = entries_.find(key);\n    if (it == entries_.end() || int(l) >= int(it->second.first))\n        entries_[key] = {l, value};\n}\nstd::optional<std::string> ConfigLadder::get(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.second;\n}\nstd::optional<Layer> ConfigLadder::source(const std::string& key) const {\n    auto it = entries_.find(key);\n    if (it == entries_.end()) return std::nullopt;\n    return it->second.first;\n}',
)

print("m19_20_21 part A (module 19) authored")
