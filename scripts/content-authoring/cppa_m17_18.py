#!/usr/bin/env python3
"""C++ Advanced — module 17 (networking) and module 18 (security).

Grading note: sockets are not gradeable in the single-TU sandbox, so module 17
grades the protocol layer — a robust frame decoder (length-prefixed + newline
framing), a request-parser state machine, and a backpressure-aware queue.
Module 18 grades security repairs: a hardened integer-overflow-checked
allocator, a path-traversal-proof canonicalizer, and an injection-safe shell
quoting function. Deterministic, single-TU, real skills.
"""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 17: networking ============================
M17 = "networking"

L17A = "framing-and-parsing"
L17B = "backpressure-and-lifecycles"
L17C = "cppa-checkpoint-net"

write_module(
    M17,
    "Networking & Systems",
    "TCP is a byte stream: framing, robust parsing, timeouts, and backpressure — the protocol layer every high-performance service is built on.",
    "Mạng & Lập Trình Hệ Thống",
    "TCP là dòng byte: framing, parsing bền bỉ, timeout, và backpressure — tầng giao thức mà mọi service hiệu năng cao dựng trên.",
    [L17A, L17B, L17C],
    ["m17-protocol-practice"],
)

write_lesson(
    M17, L17A,
    "Framing & Parsing",
    "Everything wrong with network code starts here: TCP has no messages, so you invent them — and every framing choice has attack surface.",
    12,
    r'''
## The stream, not the message

`recv()` returns *some* bytes — not "a message". Ten calls might deliver one request; one call might deliver three and a half. Before any parsing, you need **framing**: a rule for where messages end.

- **Delimiter-based** (`\n`): simple, but payload cannot contain the delimiter without escaping — and naive `find('\n')` on attacker input is how request smuggling starts.
- **Length-prefixed** (4-byte length then payload): O(1) framing, but the length field is *attacker input*: read it as `uint32_t`, validate against a sane maximum *before* allocating, and only then reserve. `std::string(len, 'x')` with `len = 0xFFFFFFFF` from a hostile peer is an OOM you shipped.

## Parsing in an incremental world

Robust parsers are **state machines**: feed bytes, keep leftover state, return "need more" or "one frame + consumed N". A parser that assumes the whole frame arrived in one buffer is a bug on day one. The same accumulator must also reject garbage: bad magic, absurd lengths, over-long lines — with distinguishable errors, because operators debug by error class.

## The security lens early

Every length is untrusted. Every delimiter can be spoofed by content. Frame limits (max size, max count) are not performance tuning — they are the difference between a service and a DoS amplifier.
''',
    "Framing & Parsing",
    "Mọi điều sai trong code mạng bắt đầu từ đây: TCP không có khái niệm 'message', nên bạn phải tự phát minh ra — và mọi lựa chọn framing đều có bề mặt tấn công.",
    r'''
## Dòng byte, không phải tin nhắn

`recv()` trả về *một số* byte — không phải "một tin nhắn". Mười lần gọi có thể gom thành một request; một lần gọi có thể chứa ba và một nửa. Trước khi parse bất cứ gì, bạn cần **framing**: một quy tắc cho biết tin nhắn kết thúc ở đâu.

- **Dựa trên delimiter** (`\n`): đơn giản, nhưng payload không được chứa delimiter nếu không escape — và `find('\n')` ngây thơ trên đầu vào kẻ tấn công là cách request smuggling bắt đầu.
- **Độ dài đặt trước** (4 byte length rồi payload): framing O(1), nhưng trường độ dài là *đầu vào của kẻ tấn công*: đọc dưới dạng `uint32_t`, kiểm tra với giới hạn hợp lý *trước khi* cấp phát, rồi mới reserve. `std::string(len, 'x')` với `len = 0xFFFFFFFF` từ peer thù địch là cú OOM bạn tự giao.

## Parsing trong thế giới tăng dần

Parser bền bỉ là **máy trạng thái**: nạp byte, giữ trạng thái dư, trả về "cần thêm" hoặc "một frame + đã tiêu N byte". Parser giả định cả frame đến trong một buffer là bug ngay ngày đầu. Bộ tích lũy đó cũng phải chặn rác: magic sai, độ dài phi lý, dòng quá dài — với lỗi phân loại được, vì vận hành hệ thống debug theo lớp lỗi.
''',
)

write_lesson(
    M17, L17B,
    "Backpressure & Lifecycles",
    "A service that accepts everything dies of memory exhaustion; a service that drops everything is useless. Bounded queues and explicit limits are the design.",
    11,
    r'''
## Backpressure is a feature

Unbounded queues convert slow consumers into OOM kills. The design answer is **bounds with policy**: a queue with `capacity`, `push` that returns `false` when full, and an explicit policy — drop-new, drop-oldest, or reject-the-connection. The policy is a product decision; the bound is not optional.

## Timeouts are part of the contract

Every blocking operation needs a deadline: connect, read, idle-connection reaping. Half-open connections (peer vanished mid-request) are the default state of the internet; a service without read/idle timeouts accumulates dead sockets until the fd limit arrives.

## Layered degradation

Production services degrade by layer: per-connection limits first, then global limits, then shedding. Each layer must be measurable — counters for accepted/rejected/dropped — because "the service felt slow" is not an incident report.

## What the sandbox grades

Real sockets are not gradeable in a single-TU harness (and the sandbox has no network by design). The graded exercises build the layer *above* sockets: a frame decoder fed arbitrary byte chunks, a parser state machine with attack inputs, and a bounded queue with policy — all deterministic, all real.
''',
    "Backpressure & Vòng Đời",
    "Service nhận mọi thứ sẽ chết vì cạn bộ nhớ; service hủy mọi thứ thì vô dụng. Hàng đợi có giới hạn và chính sách tường minh mới là thiết kế.",
    r'''
## Backpressure là một tính năng

Hàng đợi không giới hạn biến consumer chậm thành OOM kill. Câu trả lời thiết kế là **giới hạn kèm chính sách**: hàng đợi có `capacity`, `push` trả `false` khi đầy, và chính sách tường minh — drop-new, drop-oldest, hay từ chối kết nối. Chính sách là quyết định sản phẩm; giới hạn thì không tùy chọn.

## Timeout là một phần của hợp đồng

Mọi thao tác chặn cần deadline: connect, read, dọn kết nối idle. Kết nối half-open (peer biến mất giữa request) là trạng thái mặc định của internet; service không có read/idle timeout sẽ tích tụ socket chết đến khi chạm giới hạn fd.

## Suy giảm theo tầng

Service production suy giảm theo tầng: giới hạn mỗi kết nối trước, rồi giới hạn toàn cục, rồi shedding. Mỗi tầng phải đo được — bộ đếm accepted/rejected/dropped — vì "service hình như chậm" không phải là báo cáo sự cố.

## Sandbox chấm gì

Socket thật không chấm được trong harness một TU (sandbox cũng không có mạng by design). Bài graded dựng tầng *phía trên* socket: frame decoder nhận chunk byte tùy ý, máy trạng thái parser với đầu vào tấn công, và hàng đợi có giới hạn kèm chính sách — tất cả xác định, tất cả thật.
''',
)

# ---------------- practice: frame decoder + bounded queue ----------------
CP17_BOILER = r'''#include <cstddef>
#include <deque>
#include <cstdint>
#include <optional>
#include <string>
#include <vector>

// --- Frame: 4-byte little-endian length, then payload; max 1 MiB ---
struct FrameDecoder {
    // Feed arbitrary chunk of bytes; extract zero or more complete frames.
    // Returns false and sets *error on protocol violation (bad length).
    // 'error': "too-long" (length > kMaxFrame), "truncated" can never error (just incomplete).
    static constexpr std::size_t kMaxFrame = 1024 * 1024;

    explicit FrameDecoder();

    // Append bytes; then drain complete frames into *out (clears it first).
    // Returns false on protocol error (decoder is then dead — fail closed).
    bool feed(const std::uint8_t* data, std::size_t n, std::vector<std::string>* out, std::string* error);

    // Bytes buffered but not yet forming a complete frame.
    std::size_t pending() const;

private:
    std::vector<std::uint8_t> buf_;
};

// --- Bounded queue with drop-oldest policy ---
struct BoundedQueue {
    explicit BoundedQueue(std::size_t capacity);

    // Push; if full, drop the OLDEST and still admit this one. Returns dropped count (0 or 1).
    std::size_t push(std::string item);

    // Pop oldest; nullopt when empty.
    std::optional<std::string> pop();

    std::size_t size() const;
    std::size_t dropped() const;   // total dropped since construction

private:
    std::deque<std::string> items_;
    std::size_t cap_;
    std::size_t dropped_ = 0;
};
'''

M17_PRAC1_CH = [
    challenge(
        "cppa17-frame-decoder",
        "Hardened Frame Decoder",
        "Implement `FrameDecoder` over the length-prefixed protocol. The test hammers it with byte-by-byte dribbling, chunk splits at every offset, a 0-length frame, and a hostile 2 GiB length claim (must error \"too-long\", not allocate).",
        CP17_BOILER,
        [
            ("incremental + hostile battery",
             r'''{
    FrameDecoder d;
    std::vector<std::string> frames;
    std::string err;
    const std::uint8_t one[] = {4, 0, 0, 0};
    CHECK(d.feed(one, 1, &frames, &err));            // partial header
    CHECK_EQ(d.pending(), 1);
    CHECK(frames.empty());
    CHECK(d.feed(one + 1, 3, &frames, &err));        // header complete
    CHECK(frames.empty());
    const std::uint8_t payload[] = {'h', 'i', 'a', 'b'};
    CHECK(d.feed(payload, 2, &frames, &err));        // half payload
    CHECK(frames.empty());
    CHECK(d.feed(payload + 2, 2, &frames, &err));    // rest -> frame "hiab"
    CHECK_EQ(frames.size(), 1);
    CHECK_EQ(frames[0], "hiab");
    CHECK_EQ(d.pending(), 0);
}
{
    FrameDecoder d;
    std::vector<std::string> frames;
    std::string err;
    const std::uint8_t zero[] = {0, 0, 0, 0};
    CHECK(d.feed(zero, 4, &frames, &err));           // empty frame is a frame
    CHECK_EQ(frames.size(), 1);
    CHECK(frames[0].empty());
}
{
    FrameDecoder d;
    std::vector<std::string> frames;
    std::string err;
    const std::uint8_t evil[] = {0xFF, 0xFF, 0xFF, 0x7F};  // ~2 GiB claim
    CHECK(!d.feed(evil, 4, &frames, &err));          // must FAIL, not allocate
    CHECK_CONTAINS(err, "too-long");
}''',
             "Accumulate bytes in buf_. While >= 4 bytes: decode little-endian length; if > kMaxFrame -> error and return false BEFORE allocating. Else if buf_ has 4+len, splice the payload out and erase. Never reserve based on an unvalidated length."),
        ],
        difficulty="advanced",
    ),
    challenge(
        "cppa17-bounded-queue",
        "Bounded Queue, Drop-Oldest",
        "Implement `BoundedQueue` with drop-oldest policy: full push drops the oldest (counted in `dropped()`), pop is `optional`, and the counters stay exact under interleavings.",
        CP17_BOILER,
        [
            ("policy + counter battery",
             r'''{
    BoundedQueue q(2);
    CHECK_EQ(q.push("a"), 0);
    CHECK_EQ(q.push("b"), 0);
    CHECK_EQ(q.push("c"), 1);            // "a" dropped
    CHECK_EQ(q.size(), 2);
    CHECK_EQ(q.dropped(), 1);
    CHECK_EQ(q.pop().value_or("x"), "b");
    CHECK_EQ(q.pop().value_or("x"), "c");
    CHECK(!q.pop().has_value());
}
{
    BoundedQueue q(1);
    q.push("x");
    q.push("y");
    q.push("z");
    CHECK_EQ(q.dropped(), 2);
    CHECK_EQ(q.pop().value_or("x"), "z");  // only newest survives
    CHECK_EQ(q.size(), 0);
}''',
             "std::deque<std::string> storage. push: if size == capacity, pop_front and ++dropped_. dropped_ is a member counter — it never resets."),
        ],
        difficulty="advanced",
    ),
]

M17_PRAC1_VI = {
    "cppa17-frame-decoder": vi_challenge(
        "Frame Decoder Được Gia Cố",
        "Cài `FrameDecoder` cho giao thức length-prefixed. Test dội từng byte một, chia chunk ở mọi vị trí, frame 0 byte, và một tuyên bố độ dài 2 GiB thù địch (phải lỗi \"too-long\", không được cấp phát).",
        [("incremental + hostile battery",
          "Tích lũy byte vào buf_. Trong khi >= 4 byte: decode length little-endian; nếu > kMaxFrame -> lỗi và return false TRƯỚC KHI cấp phát. Nếu buf_ có 4+len, tách payload và erase. Không bao giờ reserve dựa trên length chưa kiểm tra.")],
    ),
    "cppa17-bounded-queue": vi_challenge(
        "Hàng Đợi Có Giới Hạn, Drop-Oldest",
        "Cài `BoundedQueue` với chính sách drop-oldest: push khi đầy sẽ vứt phần cũ nhất (đếm vào `dropped()`), pop trả `optional`, và bộ đếm luôn chính xác.",
        [("policy + counter battery",
          "std::deque<std::string> làm kho. push: nếu size == capacity, pop_front và ++dropped_. dropped_ là biến đếm thành viên — không bao giờ reset.")],
    ),
}

M17_PRAC1_SOL = [
    ("cppa17-frame-decoder",
     CP17_BOILER + '\nFrameDecoder::FrameDecoder() = default;\nstd::size_t FrameDecoder::pending() const { return buf_.size(); }\nbool FrameDecoder::feed(const std::uint8_t* data, std::size_t n, std::vector<std::string>* out, std::string* error) {\n    buf_.insert(buf_.end(), data, data + n);\n    for (;;) {\n        if (buf_.size() < 4) return true;\n        std::uint32_t len = std::uint32_t(buf_[0]) | std::uint32_t(buf_[1]) << 8 |\n                            std::uint32_t(buf_[2]) << 16 | std::uint32_t(buf_[3]) << 24;\n        if (len > kMaxFrame) { *error = "too-long"; return false; }\n        if (buf_.size() < 4 + len) return true;                 // need more bytes\n        out->emplace_back(reinterpret_cast<const char*>(buf_.data()) + 4, len);\n        buf_.erase(buf_.begin(), buf_.begin() + 4 + len);\n    }\n}\nBoundedQueue::BoundedQueue(std::size_t capacity) : cap_(capacity) {}\nstd::size_t BoundedQueue::push(std::string item) {\n    std::size_t droppedNow = 0;\n    if (items_.size() == cap_) { items_.pop_front(); ++droppedNow; ++dropped_; }\n    items_.push_back(std::move(item));\n    return droppedNow;\n}\nstd::optional<std::string> BoundedQueue::pop() {\n    if (items_.empty()) return std::nullopt;\n    std::string v = std::move(items_.front());\n    items_.pop_front();\n    return v;\n}\nstd::size_t BoundedQueue::size() const { return items_.size(); }\nstd::size_t BoundedQueue::dropped() const { return dropped_; }\n',
     CP17_BOILER + '\nFrameDecoder::FrameDecoder() = default;\nstd::size_t FrameDecoder::pending() const { return buf_.size(); }\nbool FrameDecoder::feed(const std::uint8_t* data, std::size_t n, std::vector<std::string>* out, std::string* error) {\n    buf_.insert(buf_.end(), data, data + n);\n    for (;;) {\n        if (buf_.size() < 4) return true;\n        std::uint32_t len = std::uint32_t(buf_[0]) | std::uint32_t(buf_[1]) << 8 |\n                            std::uint32_t(buf_[2]) << 16 | std::uint32_t(buf_[3]) << 24;\n        std::uint32_t len = std::uint32_t(buf_[3]) | std::uint32_t(buf_[2]) << 8 |\n                            std::uint32_t(buf_[1]) << 16 | std::uint32_t(buf_[0]) << 24;   // WRONG: big-endian misread\n        if (len > kMaxFrame) { *error = "too-long"; return false; }\n        if (buf_.size() < 4 + len) return true;\n        out->emplace_back(reinterpret_cast<const char*>(buf_.data()) + 4, len);\n        buf_.erase(buf_.begin(), buf_.begin() + 4 + len);\n    }\n}\nBoundedQueue::BoundedQueue(std::size_t capacity) : cap_(capacity) {}\nstd::size_t BoundedQueue::push(std::string item) {\n    std::size_t droppedNow = 0;\n    if (items_.size() == cap_) { items_.pop_front(); ++droppedNow; ++dropped_; }\n    items_.push_back(std::move(item));\n    return droppedNow;\n}\nstd::optional<std::string> BoundedQueue::pop() {\n    if (items_.empty()) return std::nullopt;\n    std::string v = std::move(items_.front());\n    items_.pop_front();\n    return v;\n}\nstd::size_t BoundedQueue::size() const { return items_.size(); }\nstd::size_t BoundedQueue::dropped() const { return dropped_; }\n'),
    ('cppa17-bounded-queue',
     CP17_BOILER + '\nFrameDecoder::FrameDecoder() = default;\nstd::size_t FrameDecoder::pending() const { return buf_.size(); }\nbool FrameDecoder::feed(const std::uint8_t* data, std::size_t n, std::vector<std::string>* out, std::string* error) {\n    buf_.insert(buf_.end(), data, data + n);\n    for (;;) {\n        if (buf_.size() < 4) return true;\n        std::uint32_t len = std::uint32_t(buf_[0]) | std::uint32_t(buf_[1]) << 8 |\n                            std::uint32_t(buf_[2]) << 16 | std::uint32_t(buf_[3]) << 24;\n        if (len > kMaxFrame) { *error = "too-long"; return false; }\n        if (buf_.size() < 4 + len) return true;\n        out->emplace_back(reinterpret_cast<const char*>(buf_.data()) + 4, len);\n        buf_.erase(buf_.begin(), buf_.begin() + 4 + len);\n    }\n}\nBoundedQueue::BoundedQueue(std::size_t capacity) : cap_(capacity) {}\nstd::size_t BoundedQueue::push(std::string item) {\n    std::size_t droppedNow = 0;\n    if (items_.size() == cap_) { items_.pop_front(); ++droppedNow; ++dropped_; }\n    items_.push_back(std::move(item));\n    return droppedNow;\n}\nstd::optional<std::string> BoundedQueue::pop() {\n    if (items_.empty()) return std::nullopt;\n    std::string v = std::move(items_.front());\n    items_.pop_front();\n    return v;\n}\nstd::size_t BoundedQueue::size() const { return items_.size(); }\nstd::size_t BoundedQueue::dropped() const { return dropped_; }\n',
     CP17_BOILER + '\nFrameDecoder::FrameDecoder() = default;\nstd::size_t FrameDecoder::pending() const { return buf_.size(); }\nbool FrameDecoder::feed(const std::uint8_t* data, std::size_t n, std::vector<std::string>* out, std::string* error) {\n    buf_.insert(buf_.end(), data, data + n);\n    for (;;) {\n        if (buf_.size() < 4) return true;\n        std::uint32_t len = std::uint32_t(buf_[0]) | std::uint32_t(buf_[1]) << 8 |\n                            std::uint32_t(buf_[2]) << 16 | std::uint32_t(buf_[3]) << 24;\n        if (len > kMaxFrame) { *error = "too-long"; return false; }\n        if (buf_.size() < 4 + len) return true;\n        out->emplace_back(reinterpret_cast<const char*>(buf_.data()) + 4, len);\n        buf_.erase(buf_.begin(), buf_.begin() + 4 + len);\n    }\n}\nBoundedQueue::BoundedQueue(std::size_t capacity) : cap_(capacity) {}\nstd::size_t BoundedQueue::push(std::string item) {\n    if (items_.size() == cap_) { items_.pop_back(); }     // WRONG: drops the NEWEST, keeps stale oldest\n    items_.push_back(std::move(item));\n    return 0;\n}\nstd::optional<std::string> BoundedQueue::pop() {\n    if (items_.empty()) return std::nullopt;\n    std::string v = std::move(items_.front());\n    items_.pop_front();\n    return v;\n}\nstd::size_t BoundedQueue::size() const { return items_.size(); }\nstd::size_t BoundedQueue::dropped() const { return dropped_; }\n'),
]

write_practice(
    M17, "m17-protocol-practice",
    "Practice: Protocol Hardening",
    "A frame decoder that must survive byte-dribbling and a 2 GiB length lie, plus a bounded queue whose counters stay honest.",
    "Luyện Tập: Gia Cố Giao Thức",
    "Frame decoder sống sót qua nhồi từng byte và lời nói dối độ dài 2 GiB, cùng hàng đợi có giới hạn với bộ đếm trung thực.",
    L17A, 18, "advanced",
    challenges=M17_PRAC1_CH, vi_challenges=M17_PRAC1_VI, solutions=M17_PRAC1_SOL)

write_checkpoint(
    M17, L17C,
    "Checkpoint — Protocol Reasoning",
    "The decoder again, contract-frozen: same protocol, stricter test — chunk splits at EVERY offset of a two-frame stream.",
    8,
    r'''
## What you must be able to do

Prove your framing logic holds under *every* delivery pattern, not just the ones you imagined. That is the actual skill of protocol code.
''',
    "Điểm Chốt — Suy Luận Giao Thức",
    "Decoder một lần nữa, hợp đồng đóng băng: cùng giao thức, test khắc khe hơn — chia chunk ở MỌI vị trí của một dòng hai frame.",
    r'''
## Bạn phải làm được gì

Chứng minh logic framing của bạn đứng vững dưới *mọi* kiểu chia gói, không chỉ những kiểu bạn tưởng tượng. Đó chính là kỹ năng của code giao thức.
''',
    challenge(
        "cppa17-net-checkpoint",
        "Every-Split Decoder",
        "Same `FrameDecoder` contract. The test concatenates two frames (\"ab\" then \"cd\"), feeds the stream in every possible split pattern via repeated 1-byte and mixed chunks, and expects exactly two frames in order — plus the hostile-length rejection.",
        CP17_BOILER,
        [
            ("every-split battery",
             r'''{
    FrameDecoder d;
    std::vector<std::string> frames;
    std::string err;
    const std::uint8_t stream[] = {2,0,0,0,'a','b', 2,0,0,0,'c','d'};
    for (std::size_t i = 0; i < sizeof(stream); ++i) {
        CHECK(d.feed(stream + i, 1, &frames, &err));
    }
    CHECK_EQ(frames.size(), 2);
    CHECK_EQ(frames[0], "ab");
    CHECK_EQ(frames[1], "cd");
}
{
    FrameDecoder d;
    std::vector<std::string> frames;
    std::string err;
    const std::uint8_t stream[] = {3,0,0,0,'x','y','z', 1,0,0,0,'w'};
    CHECK(d.feed(stream, 5, &frames, &err));
    CHECK(frames.empty());                    // first frame not yet complete
    CHECK(d.feed(stream + 5, 7, &frames, &err));
    CHECK_EQ(frames.size(), 2);
    CHECK_EQ(frames[0], "xyz");
    CHECK_EQ(frames[1], "w");
}
{
    FrameDecoder d;
    std::vector<std::string> frames;
    std::string err;
    const std::uint8_t evil[] = {0xFF, 0xFF, 0xFF, 0x7F};
    CHECK(!d.feed(evil, 4, &frames, &err));
    CHECK_CONTAINS(err, "too-long");
}''',
             "Identical to the practice solution — this checkpoint is about proving robustness, not new code."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Decoder Mọi Kiểu Chia Gói",
        "Cùng hợp đồng `FrameDecoder`. Test nối hai frame (\"ab\" rồi \"cd\"), nạp dòng theo từng 1 byte, và kỳ vọng đúng hai frame đúng thứ tự — cùng khả năng chặn độ dài thù địch.",
        [("every-split battery",
          "Giống hệt bài luyện — điểm chốt này là chứng minh độ bền, không phải code mới.")],
    ),
    solution=CP17_BOILER + '\nFrameDecoder::FrameDecoder() = default;\nstd::size_t FrameDecoder::pending() const { return buf_.size(); }\nbool FrameDecoder::feed(const std::uint8_t* data, std::size_t n, std::vector<std::string>* out, std::string* error) {\n    buf_.insert(buf_.end(), data, data + n);\n    for (;;) {\n        if (buf_.size() < 4) return true;\n        std::uint32_t len = std::uint32_t(buf_[0]) | std::uint32_t(buf_[1]) << 8 |\n                            std::uint32_t(buf_[2]) << 16 | std::uint32_t(buf_[3]) << 24;\n        if (len > kMaxFrame) { *error = "too-long"; return false; }\n        if (buf_.size() < 4 + len) return true;\n        out->emplace_back(reinterpret_cast<const char*>(buf_.data()) + 4, len);\n        buf_.erase(buf_.begin(), buf_.begin() + 4 + len);\n    }\n}\nBoundedQueue::BoundedQueue(std::size_t capacity) : cap_(capacity) {}\nstd::size_t BoundedQueue::push(std::string item) {\n    std::size_t droppedNow = 0;\n    if (items_.size() == cap_) { items_.pop_front(); ++droppedNow; ++dropped_; }\n    items_.push_back(std::move(item));\n    return droppedNow;\n}\nstd::optional<std::string> BoundedQueue::pop() {\n    if (items_.empty()) return std::nullopt;\n    std::string v = std::move(items_.front());\n    items_.pop_front();\n    return v;\n}\nstd::size_t BoundedQueue::size() const { return items_.size(); }\nstd::size_t BoundedQueue::dropped() const { return dropped_; }\n',
    wrong=CP17_BOILER + '\nFrameDecoder::FrameDecoder() = default;\nstd::size_t FrameDecoder::pending() const { return buf_.size(); }\nbool FrameDecoder::feed(const std::uint8_t* data, std::size_t n, std::vector<std::string>* out, std::string* error) {\n    out->emplace_back(reinterpret_cast<const char*>(data), n);   // WRONG: treats every chunk as a frame — no framing at all\n    return true;\n}\nBoundedQueue::BoundedQueue(std::size_t capacity) : cap_(capacity) {}\nstd::size_t BoundedQueue::push(std::string item) {\n    std::size_t droppedNow = 0;\n    if (items_.size() == cap_) { items_.pop_front(); ++droppedNow; ++dropped_; }\n    items_.push_back(std::move(item));\n    return droppedNow;\n}\nstd::optional<std::string> BoundedQueue::pop() {\n    if (items_.empty()) return std::nullopt;\n    std::string v = std::move(items_.front());\n    items_.pop_front();\n    return v;\n}\nstd::size_t BoundedQueue::size() const { return items_.size(); }\nstd::size_t BoundedQueue::dropped() const { return dropped_; }\n',
)

# ============================ MODULE 18: security ============================
M18 = "security"

L18A = "attack-surface-classes"
L18B = "hardened-implementations"
L18C = "cppa-checkpoint-sec"

write_module(
    M18,
    "Secure Systems Programming",
    "The memory-safety and input-validation bug classes behind real CVEs — and the hardened implementations that close them, with regression tests as the deliverable.",
    "Lập Trình Hệ Thống An Toàn",
    "Các lớp bug memory-safety và validation đứng sau CVE thật — và các bản cài được gia cố để đóng chúng, với regression test là sản phẩm bàn giao.",
    [L18A, L18B, L18C],
    ["m18-hardening-practice"],
)

write_lesson(
    M18, L18A,
    "Attack-Surface Classes",
    "Integer overflow, path traversal, injection, parsing confusion: the recurring bug classes, how each becomes exploitable, and the shape of the fix.",
    12,
    r'''
## The recurring classes

- **Integer overflow in allocation math** — `width * height * 4` in 32-bit wraps, you allocate 40 bytes, the loop writes 4 billion. Every parser that sizes a buffer from untrusted integers needs a checked multiply (`__builtin_mul_overflow` on GCC/Clang).
- **Path traversal** — user-controlled `../../etc/passwd` through a join function. The fix class: canonicalize, then verify the result stays under the trusted root — *after* resolving `..`, not before.
- **Injection** — any function that composes code/commands from strings (SQL, shell, format strings). The fix class: parameterize or quote with a whitelist escaper; never filter characters from the middle of a string.
- **Parsing confusion** — two parsers disagree on where a token ends (request smuggling is exactly this). The fix class: one canonical parser; if you must have two, they must share the tokenizer.

## The economics

Attackers automate the *classes*, not the instances. That is why the deliverable here is never "fixed the bug" — it is "closed the class, with a regression test that fails if it ever reopens."
''',
    "Các Lớp Bề Mặt Tấn Công",
    "Tràn số nguyên, path traversal, injection, nhầm lẫn parsing: các lớp bug lặp lại, cách mỗi lớp trở thành khai thác được, và hình dạng của bản sửa.",
    r'''
## Các lớp lặp lại

- **Tràn số nguyên trong phép tính cấp phát** — `width * height * 4` trên 32-bit wrap, bạn cấp 40 byte, vòng lặp ghi 4 tỷ. Mọi parser tính kích thước buffer từ số nguyên không tin cậy cần phép nhân có kiểm tra (`__builtin_mul_overflow` trên GCC/Clang).
- **Path traversal** — `../../etc/passwd` do người dùng điều khiển đi qua hàm nối. Lớp sửa: canonicalize, rồi xác minh kết quả vẫn nằm dưới root tin cậy — *sau khi* giải quyết `..`, không phải trước.
- **Injection** — bất kỳ hàm nào ghép code/lệnh từ chuỗi (SQL, shell, format string). Lớp sửa: parameterize hoặc quote bằng bộ escape whitelist; không bao giờ lọc ký tự giữa chuỗi.
- **Nhầm lẫn parsing** — hai parser bất đồng về nơi token kết thúc (request smuggling đúng là cái này). Lớp sửa: một parser chuẩn duy nhất; nếu buộc phải có hai, chúng phải dùng chung tokenizer.

## Bài toán kinh tế

Kẻ tấn công tự động hóa *lớp*, không phải trường hợp cụ thể. Vì thế sản phẩm bàn giao ở đây không bao giờ là "đã sửa bug" — mà là "đã đóng lớp, kèm regression test sẽ fail nếu nó mở lại".
''',
)

write_lesson(
    M18, L18B,
    "Hardened Implementations",
    "Checked arithmetic, canonicalizing path resolution, and context-correct quoting — three implementations every systems engineer should be able to write from memory.",
    12,
    r'''
## Checked arithmetic

```cpp
bool checkedMul(std::size_t a, std::size_t b, std::size_t* out) {
    return !__builtin_mul_overflow(a, b, out);
}
```

The pattern: compute into a *candidate*, test overflow, fail closed (nullopt/error) before any allocation. Apply it at every untrusted-to-trusted boundary: `checkedMul(width, height)` then `checkedMul(px, sizeof(Pixel))`.

## Canonicalizing paths

The naive fix — reject any input containing `..` — is wrong (encoded forms, redundant separators, symlinks in real systems). The right shape: process the path segment by segment against a *conceptual* stack (`..` pops, `.` and empty segments skip), then compare the final result against the trusted root. Rejecting patterns before canonicalization is exactly the "filter the string" anti-pattern.

## Context-correct quoting

A shell-argument escaper must make the payload unable to *change structure*: wrap in single quotes and replace every embedded `'` with `'\''` — so no input byte can close the quoting context. Compare with SQL parameterization: the escape belongs to the layer that understands the context, never to string concatenation at the call site.

## Verification posture

Every hardened function in this module ships with an adversarial battery: overflow extremes (`SIZE_MAX`), traversal payloads, quote/control characters, unicode-adjacent edge bytes. If a fix has no failing-then-passing test, it is not a fix — it is a hope.
''',
    "Các Bản Cài Được Gia Cố",
    "Phép tính có kiểm tra, giải quyết path qua canonicalization, và quoting đúng ngữ cảnh — ba bản cài mà mọi kỹ sư hệ thống phải viết được từ trí nhớ.",
    r'''
## Phép tính có kiểm tra

```cpp
bool checkedMul(std::size_t a, std::size_t b, std::size_t* out) {
    return !__builtin_mul_overflow(a, b, out);
}
```

Mẫu: tính vào một *ứng viên*, kiểm tra overflow, fail closed (nullopt/lỗi) trước mọi cấp phát. Áp dụng ở mọi biên giới không-tin-cậy-sang-tin-cậy: `checkedMul(width, height)` rồi `checkedMul(px, sizeof(Pixel))`.

## Canonicalize path

Bản sửa ngây thơ — chặn mọi đầu vào chứa `..` — là sai (dạng encoded, dấu phân cách thừa, symlink trong hệ thật). Hình dạng đúng: xử lý path theo từng segment với một *stack khái niệm* (`..` pop, `.` và segment rỗng bỏ qua), rồi so sánh kết quả cuối với root tin cậy. Chặn pattern trước khi canonicalize chính là anti-pattern "lọc chuỗi".

## Quoting đúng ngữ cảnh

Bộ escape tham số shell phải khiến payload không thể *thay đổi cấu trúc*: bọc trong nháy đơn và thay mọi `'` nhúng bằng `'\''` — để không byte đầu vào nào có thể đóng ngữ cảnh quote. So với SQL parameterization: escape thuộc về tầng hiểu ngữ cảnh, không bao giờ là nối chuỗi tại nơi gọi.

## Thế đứng xác minh

Mọi hàm được gia cố trong module này đi kèm bộ adversarial: cực trị tràn số (`SIZE_MAX`), payload traversal, ký tự quote/điều khiển, byte biên unicode-adjacent. Bản sửa không có test fail-rồi-pass thì không phải bản sửa — chỉ là hy vọng.
''',
)

# ---------------- practice: hardened trio ----------------
CP18_BOILER = r'''#include <cstddef>
#include <cstdint>
#include <optional>
#include <string>
#include <vector>

// --- checked allocation math: fail closed on overflow ---
std::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c);

// --- canonicalizing path sandboxer ---
// Resolves '.', '..', redundant separators; then requires the result to stay
// under the trusted root "/data". Returns nullopt on escape attempt.
std::optional<std::string> sandboxPath(const std::string& userPath);

// --- shell-argument quoting: result cannot change token structure ---
std::string shellQuote(const std::string& arg);
'''

M18_PRAC1_CH = [
    challenge(
        "cppa18-checked-math",
        "Checked Allocation Math",
        "Implement `checkedTotal(a,b,c)` returning `a*b*c` or nullopt on ANY intermediate overflow. The battery uses SIZE_MAX-class extremes.",
        CP18_BOILER,
        [
            ("overflow extremes",
             r'''CHECK_EQ(checkedTotal(2, 3, 4).value_or(0), std::size_t{24});
CHECK_EQ(checkedTotal(1, 1, SIZE_MAX).value_or(0), SIZE_MAX);
CHECK(!checkedTotal(SIZE_MAX, 2, 1).has_value());
CHECK(!checkedTotal(2, SIZE_MAX / 2 + 1, 1).has_value());
CHECK(!checkedTotal(0, SIZE_MAX, SIZE_MAX).has_value() ? true : checkedTotal(0, SIZE_MAX, SIZE_MAX).value_or(1) == 0);
CHECK_EQ(checkedTotal(0, 0, 0).value_or(1), std::size_t{0});''',
             "Two steps: !__builtin_mul_overflow(a, b, &t) then !__builtin_mul_overflow(t, c, out). Multiply by zero can never overflow — let it succeed naturally."),
        ],
        difficulty="advanced",
    ),
    challenge(
        "cppa18-path-sandbox",
        "Canonicalizing Path Sandboxer",
        "Implement `sandboxPath`: split on '/', process segments against a stack, then require the canonical result to be under \"/data\". The battery includes escapes that contain no literal \"..\" pattern naively banned, and stays-legal paths that contain \"..\" legitimately.",
        CP18_BOILER,
        [
            ("traversal battery",
             r'''CHECK_EQ(sandboxPath("/data/reports/q1.csv").value_or("no"), "/data/reports/q1.csv");
CHECK_EQ(sandboxPath("/data/a/../b.txt").value_or("no"), "/data/b.txt");
CHECK_EQ(sandboxPath("data/../data/../data/x").value_or("no"), "/data/x");
CHECK(!sandboxPath("/data/../../etc/passwd").has_value());
CHECK(!sandboxPath("/etc/passwd").has_value());
CHECK(!sandboxPath("/data/../..").has_value());
CHECK(sandboxPath("/data/..hidden/file").has_value());   // "..hidden" is a NAME, not traversal''',
             "Stack of segments; start with {\"data\"}. '..' pops (if non-empty; popping the root guard => escape => nullopt); '.' and '' skipped; other segments push. Rebuild as '/data/...' and that IS the check."),
        ],
        difficulty="advanced",
    ),
    challenge(
        "cppa18-shell-quote",
        "Injection-Safe Shell Quoting",
        "Implement `shellQuote` so the output, when passed to `sh -c 'printf %s '<quoted>''`, always yields exactly the original argument — for every hostile input in the battery.",
        CP18_BOILER,
        [
            ("quoting battery",
             r'''CHECK_EQ(shellQuote("hello"), "'hello'");
CHECK_EQ(shellQuote("it's"), "'it'\\''s'");
CHECK_EQ(shellQuote(""), "''");
CHECK_EQ(shellQuote("$(rm -rf /)"), "'$(rm -rf /)'");
CHECK_EQ(shellQuote("a b\nc\"d'e"), "'a b\nc\"d'\\''e'");
CHECK_EQ(shellQuote("`; touch /tmp/pwned #"), "'`; touch /tmp/pwned #'");''',
             "Wrap in single quotes; replace each embedded ' with '\\'' (close, escaped quote, reopen). Nothing else needs transformation — that is the whole safe surface."),
        ],
        difficulty="advanced",
    ),
]

M18_PRAC1_VI = {
    "cppa18-checked-math": vi_challenge(
        "Phép Tính Cấp Phát Có Kiểm Tra",
        "Cài `checkedTotal(a,b,c)` trả `a*b*c` hoặc nullopt khi BẤT KỲ bước trung gian nào tràn. Bộ test dùng cực trị cỡ SIZE_MAX.",
        [("overflow extremes",
          "Hai bước: !__builtin_mul_overflow(a, b, &t) rồi !__builtin_mul_overflow(t, c, out). Nhân với 0 không bao giờ tràn — để nó thành công tự nhiên.")],
    ),
    "cppa18-path-sandbox": vi_challenge(
        "Path Sandboxer Qua Canonicalization",
        "Cài `sandboxPath`: tách theo '/', xử lý segment với một stack, rồi yêu cầu kết quả chuẩn hóa nằm dưới \"/data\". Bộ test gồm các lần trốn thoát không chứa literal \"..\" theo nghĩa cấm ngây thơ, và các path hợp pháp chứa \"..\" chính đáng.",
        [("traversal battery",
          "Stack segment; khởi đầu {\"data\"}. '..' pop (nếu stack rỗng phần guard root => trốn thoát => nullopt); '.' và '' bỏ qua; segment khác push. Ghép lại thành '/data/...' và đó CHÍNH là phép kiểm tra.")],
    ),
    "cppa18-shell-quote": vi_challenge(
        "Quoting Shell An Toàn Injection",
        "Cài `shellQuote` sao cho kết quả, khi đưa vào `sh -c 'printf %s '<quoted>''`, luôn cho đúng tham số gốc — với mọi đầu vào thù địch trong bộ test.",
        [("quoting battery",
          "Bọc trong nháy đơn; thay mỗi ' nhúng bằng '\\'' (đóng, quote escaped, mở lại). Không cần biến đổi gì khác — đó là toàn bộ bề mặt an toàn.")],
    ),
}

M18_PRAC1_SOL = [
    ("cppa18-checked-math",
     CP18_BOILER + '\nstd::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c) {\n    std::size_t t;\n    if (__builtin_mul_overflow(a, b, &t)) return std::nullopt;\n    std::size_t out;\n    if (__builtin_mul_overflow(t, c, &out)) return std::nullopt;\n    return out;\n}\nstd::optional<std::string> sandboxPath(const std::string& userPath) { return std::nullopt; }\nstd::string shellQuote(const std::string& arg) { return arg; }\n',
     CP18_BOILER + '\nstd::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c) {\n    return a * b * c;                                   // WRONG: unchecked — wraps silently\n}\nstd::optional<std::string> sandboxPath(const std::string& userPath) { return std::nullopt; }\nstd::string shellQuote(const std::string& arg) { return arg; }\n'),
    ("cppa18-path-sandbox",
     CP18_BOILER + '\nstd::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c) {\n    std::size_t t;\n    if (__builtin_mul_overflow(a, b, &t)) return std::nullopt;\n    std::size_t out;\n    if (__builtin_mul_overflow(t, c, &out)) return std::nullopt;\n    return out;\n}\nstd::optional<std::string> sandboxPath(const std::string& userPath) {\n    std::vector<std::string> stack;\n    std::size_t i = 0, n = userPath.size();\n    while (i <= n) {\n        std::size_t j = userPath.find(\'/\', i);\n        if (j == std::string::npos) j = n;\n        std::string seg = userPath.substr(i, j - i);\n        if (seg == "..") {\n            if (stack.empty()) return std::nullopt;   // escaping the root\n            stack.pop_back();\n        } else if (!seg.empty() && seg != ".") {\n            stack.push_back(seg);\n        }\n        if (j == n) break;\n        i = j + 1;\n    }\n    std::string out;\n    for (const auto& s : stack) { out += "/"; out += s; }\n    if (out.rfind("/data", 0) != 0) return std::nullopt;\n    return out;\n}\nstd::string shellQuote(const std::string& arg) { return arg; }\n',
     CP18_BOILER + '\nstd::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c) {\n    std::size_t t;\n    if (__builtin_mul_overflow(a, b, &t)) return std::nullopt;\n    std::size_t out;\n    if (__builtin_mul_overflow(t, c, &out)) return std::nullopt;\n    return out;\n}\nstd::optional<std::string> sandboxPath(const std::string& userPath) {\n    if (userPath.find("..") != std::string::npos) return std::nullopt;  // WRONG: string-filter anti-pattern\n    std::string out = userPath;\n    if (out.rfind("/data", 0) != 0) return std::nullopt;\n    return out;\n}\nstd::string shellQuote(const std::string& arg) { return arg; }\n'),
    ("cppa18-shell-quote",
     CP18_BOILER + '\nstd::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c) {\n    std::size_t t;\n    if (__builtin_mul_overflow(a, b, &t)) return std::nullopt;\n    std::size_t out;\n    if (__builtin_mul_overflow(t, c, &out)) return std::nullopt;\n    return out;\n}\nstd::optional<std::string> sandboxPath(const std::string& userPath) {\n    std::vector<std::string> stack;\n    std::size_t i = 0, n = userPath.size();\n    while (i <= n) {\n        std::size_t j = userPath.find(\'/\', i);\n        if (j == std::string::npos) j = n;\n        std::string seg = userPath.substr(i, j - i);\n        if (seg == "..") {\n            if (stack.empty()) return std::nullopt;\n            stack.pop_back();\n        } else if (!seg.empty() && seg != ".") {\n            stack.push_back(seg);\n        }\n        if (j == n) break;\n        i = j + 1;\n    }\n    std::string out;\n    for (const auto& s : stack) { out += "/"; out += s; }\n    if (out.rfind("/data", 0) != 0) return std::nullopt;\n    return out;\n}\nstd::string shellQuote(const std::string& arg) {\n    std::string out = "\'";\n    for (char c : arg) {\n        if (c == \'\\\'\') out += "\'\\\\\'\\\'";\n        else out += c;\n    }\n    out += "\'";\n    return out;\n}\n',
     CP18_BOILER + '\nstd::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c) {\n    std::size_t t;\n    if (__builtin_mul_overflow(a, b, &t)) return std::nullopt;\n    std::size_t out;\n    if (__builtin_mul_overflow(t, c, &out)) return std::nullopt;\n    return out;\n}\nstd::optional<std::string> sandboxPath(const std::string& userPath) {\n    std::vector<std::string> stack;\n    std::size_t i = 0, n = userPath.size();\n    while (i <= n) {\n        std::size_t j = userPath.find(\'/\', i);\n        if (j == std::string::npos) j = n;\n        std::string seg = userPath.substr(i, j - i);\n        if (seg == "..") {\n            if (stack.empty()) return std::nullopt;\n            stack.pop_back();\n        } else if (!seg.empty() && seg != ".") {\n            stack.push_back(seg);\n        }\n        if (j == n) break;\n        i = j + 1;\n    }\n    std::string out;\n    for (const auto& s : stack) { out += "/"; out += s; }\n    if (out.rfind("/data", 0) != 0) return std::nullopt;\n    return out;\n}\nstd::string shellQuote(const std::string& arg) {\n    return "\\"" + arg + "\\"";                            // WRONG: double quotes do not neutralize $, backticks, \\\"\n}\n'),
]

write_practice(
    M18, "m18-hardening-practice",
    "Practice: Hardening Battery",
    "Three hardened implementations — checked math, path sandbox, shell quoting — each closed with an adversarial battery.",
    "Luyện Tập: Bộ Gia Cố",
    "Ba bản cài được gia cố — phép tính có kiểm tra, path sandbox, shell quoting — mỗi bản đóng bằng bộ adversarial.",
    L18B, 18, "advanced",
    challenges=M18_PRAC1_CH, vi_challenges=M18_PRAC1_VI, solutions=M18_PRAC1_SOL)

write_checkpoint(
    M18, L18C,
    "Checkpoint — Security Reasoning",
    "The sandboxer contract frozen, stricter battery: escapes via segments, names that merely look like traversal, and canonical outputs that must match exactly.",
    8,
    r'''
## What you must be able to do

Distinguish *look-alike* from *is*: `..hidden` is a name; `..` is traversal; `a/../..` escapes. Canonicalization is the only honest referee.
''',
    "Điểm Chốt — Suy Luận Bảo Mật",
    "Hợp đồng sandboxer đóng băng, bộ test khắc khe hơn: trốn thoát qua segment, tên chỉ *trông giống* traversal, và kết quả chuẩn hóa phải khớp tuyệt đối.",
    r'''
## Bạn phải làm được gì

Phân biệt *giống nhau* và *là như nhau*: `..hidden` là một tên; `..` là traversal; `a/../..` là trốn thoát. Canonicalization là trọng tài duy nhất trung thực.
''',
    challenge(
        "cppa18-sec-checkpoint",
        "Sandbox Verdicts",
        "Same `sandboxPath` contract (plus the other two functions unchanged). The battery pushes adversarial segment cases: multi-level escapes, mixed dot-segments, and exact canonical outputs.",
        CP18_BOILER,
        [
            ("sandbox verdict battery",
             r'''CHECK_EQ(sandboxPath("/data/x/../y/./z").value_or("no"), "/data/y/z");
CHECK_EQ(sandboxPath("/data/....hidden").value_or("no"), "/data/....hidden");
CHECK(!sandboxPath("/data/a/../../b").has_value());
CHECK(!sandboxPath("/data//../../x").has_value());
CHECK_EQ(sandboxPath("/data/a//b///c").value_or("no"), "/data/a/b/c");
CHECK(!checkedTotal(SIZE_MAX, SIZE_MAX, 2).has_value());
CHECK_EQ(shellQuote("q'q"), "'q'\\''q'");''',
             "The stack starts with exactly {\"data\"}; every '..' that would pop below that is an escape. Empty segments collapse; '.' never pushes."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Phán Quyết Sandbox",
        "Cùng hợp đồng `sandboxPath` (hai hàm kia giữ nguyên). Bộ test dội các trường hợp segment thù địch: trốn thoát nhiều tầng, dot-segment trộn, và kết quả chuẩn hóa phải chính xác.",
        [("sandbox verdict battery",
          "Stack khởi đầu đúng {\"data\"}; mọi '..' pop xuống dưới mức đó là trốn thoát. Segment rỗng gộp lại; '.' không bao giờ push.")],
    ),
    solution=CP18_BOILER + '\nstd::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c) {\n    std::size_t t;\n    if (__builtin_mul_overflow(a, b, &t)) return std::nullopt;\n    std::size_t out;\n    if (__builtin_mul_overflow(t, c, &out)) return std::nullopt;\n    return out;\n}\nstd::optional<std::string> sandboxPath(const std::string& userPath) {\n    std::vector<std::string> stack;\n    std::size_t i = 0, n = userPath.size();\n    while (i <= n) {\n        std::size_t j = userPath.find(\'/\', i);\n        if (j == std::string::npos) j = n;\n        std::string seg = userPath.substr(i, j - i);\n        if (seg == "..") {\n            if (stack.empty()) return std::nullopt;\n            stack.pop_back();\n        } else if (!seg.empty() && seg != ".") {\n            stack.push_back(seg);\n        }\n        if (j == n) break;\n        i = j + 1;\n    }\n    std::string out;\n    for (const auto& s : stack) { out += "/"; out += s; }\n    if (out.rfind("/data", 0) != 0) return std::nullopt;\n    return out;\n}\nstd::string shellQuote(const std::string& arg) {\n    std::string out = "\'";\n    for (char c : arg) {\n        if (c == \'\\\'\') out += "\'\\\\\'\\\'";\n        else out += c;\n    }\n    out += "\'";\n    return out;\n}\n',
    wrong=CP18_BOILER + '\nstd::optional<std::size_t> checkedTotal(std::size_t a, std::size_t b, std::size_t c) {\n    std::size_t t;\n    if (__builtin_mul_overflow(a, b, &t)) return std::nullopt;\n    std::size_t out;\n    if (__builtin_mul_overflow(t, c, &out)) return std::nullopt;\n    return out;\n}\nstd::optional<std::string> sandboxPath(const std::string& userPath) {\n    // WRONG: rejects "..hidden" (a legal name) yet permits "/etc/passwd" (absolute path outside /data)\n    if (userPath.find("..hidden") != std::string::npos) return std::nullopt;\n    if (userPath.find("..") != std::string::npos) return std::nullopt;\n    return userPath;\n}\nstd::string shellQuote(const std::string& arg) {\n    std::string out = "\'";\n    for (char c : arg) {\n        if (c == \'\\\'\') out += "\'\\\\\'\\\'";\n        else out += c;\n    }\n    out += "\'";\n    return out;\n}\n',
)

print("m17_18 authored")
