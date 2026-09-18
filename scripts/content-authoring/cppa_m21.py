#!/usr/bin/env python3
"""C++ Advanced — module 21 (capstone-hpc-service).

Capstone: an integrated, deterministic admission + reporting core. The clock
seam (M19), per-key state ownership (M6/M11), and exact-string ops reporting
(M20) come together in one acceptance battery. No sockets, no threads — the
integration is the challenge.
"""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

M21 = "capstone-hpc-service"

L21A = "cppa-capstone-brief"
L21B = "cppa-capstone-design"
L21C = "cppa-checkpoint-capstone"

CP21_BOILER = r'''#include <cstdint>
#include <map>
#include <optional>
#include <string>
#include <tuple>
#include <vector>

// ---- FixedClock: the deterministic time seam (module 19) ----
struct FixedClock {
    std::int64_t nowMs_ = 0;
    std::int64_t nowMs() const { return nowMs_; }
    void advance(std::int64_t ms) { nowMs_ += ms; }
};

// ---- Domain ----
enum class ClassId : int { Regular = 0, Premium = 1 };

struct Admission {
    bool admitted = false;
    int tag = -1;
    int ordinal = -1;   // arrival order within the winning tag this window
};

class AdmissionsCore {
public:
    explicit AdmissionsCore(const FixedClock* clock);
    // tag limits: tag >= 0, limit >= 1; re-setting an existing tag fails.
    bool setTagLimit(int tag, int limit);
    Admission admit(ClassId cls, int tag);   // unknown tags are rejected
    std::int64_t admittedCount() const { return admitted_; }
    std::int64_t rejectedCount() const { return rejected_; }

private:
    const FixedClock* clock_;
    std::map<int, int> limits_;
    std::map<int, int> used_;
    std::map<int, int> nextOrd_;
    std::int64_t window_ = -1;
    std::int64_t admitted_ = 0;
    std::int64_t rejected_ = 0;
};

class OpsReport {
public:
    explicit OpsReport(const FixedClock* clock);
    void record(std::int64_t tMs, std::string code, std::string key);
    // exact lines "[ts] CODE key\n" sorted by ts; at equal ts REJECT before ADMIT; oldest first
    std::string snapshot() const;

private:
    const FixedClock* clock_;
    std::vector<std::tuple<std::int64_t, std::string, std::string>> rows_;
};
'''

R_CORE = """AdmissionsCore::AdmissionsCore(const FixedClock* clock) : clock_(clock) {}
bool AdmissionsCore::setTagLimit(int tag, int limit) {
    if (tag < 0 || limit < 1) return false;
    if (limits_.count(tag)) return false;
    limits_[tag] = limit;
    return true;
}
Admission AdmissionsCore::admit(ClassId, int tag) {
    Admission out;
    const std::int64_t now = clock_->nowMs();
    if (now != window_) { window_ = now; used_.clear(); nextOrd_.clear(); }
    auto lim = limits_.find(tag);
    if (lim == limits_.end()) { ++rejected_; return out; }
    const int used = used_[tag];
    if (used >= lim->second) { ++rejected_; return out; }
    used_[tag] = used + 1;
    out.admitted = true;
    out.tag = tag;
    out.ordinal = ++nextOrd_[tag];
    ++admitted_;
    return out;
}"""

W_CORE = R_CORE.replace(
    "    if (now != window_) { window_ = now; used_.clear(); nextOrd_.clear(); }",
    "    // WRONG: window_ only moves backwards — rollover never clears counters\n    if (now < window_) { window_ = now; used_.clear(); nextOrd_.clear(); }",
)
assert W_CORE != R_CORE, "W_core"

R_REP = """OpsReport::OpsReport(const FixedClock* clock) : clock_(clock) {}
void OpsReport::record(std::int64_t tMs, std::string code, std::string key) {
    rows_.emplace_back(tMs, std::move(code), std::move(key));
}
std::string OpsReport::snapshot() const {
    auto rows = rows_;
    auto sev = [](const std::string& code) {
        if (code == "REJECT") return 0;
        if (code == "ADMIT") return 1;
        return 2;
    };
    std::stable_sort(rows.begin(), rows.end(), [&](const auto& a, const auto& b) {
        if (std::get<0>(a) != std::get<0>(b)) return std::get<0>(a) < std::get<0>(b);
        return sev(std::get<1>(a)) < sev(std::get<1>(b));
    });
    std::string out;
    for (const auto& [ts, code, key] : rows)
        out += "[" + std::to_string(ts) + "] " + code + " " + key + "\\n";
    return out;
}"""

W_REP = R_REP.replace(
    """        if (std::get<0>(a) != std::get<0>(b)) return std::get<0>(a) < std::get<0>(b);
        return sev(std::get<1>(a)) < sev(std::get<1>(b));""",
    """        // WRONG: stable ascending by timestamp only — ties keep call order
        return std::get<0>(a) < std::get<0>(b);""",
)
assert W_REP != R_REP, "W_rep"

# ------------------------------------------------------------------ lessons
write_lesson(
    M21, L21A,
    "Capstone Brief — The Admission Service",
    "One spec, one acceptance battery: per-tag admission with windows and provenance, plus an exact ops report. You ship when the battery is green.",
    12,
    r'''
## The brief

You are the engineer of record for an admission service core. There is no
tutorial for this module — the acceptance battery **is** the specification.

**`AdmissionsCore`** — tag-scoped admission over a deterministic clock:

- `setTagLimit(tag, limit)` accepts only `tag >= 0`, `limit >= 1`, and only
  the **first** configuration of a tag (re-setting fails, returns `false`).
- `admit(cls, tag)` — unknown tags are rejected; a tag admits while its
  in-window usage is under its limit; the winner gets its arrival `ordinal`
  within the tag for the current window.
- A **window** is a single clock timestamp: the first `admit` at a new
  timestamp rolls per-tag counters and ordinals.
- Running totals: `admittedCount()`, `rejectedCount()`.

**`OpsReport`** — the audit trail, graded as an exact string:

- `record(tMs, code, key)` then `snapshot()` produces `"[ts] CODE key\n"`
  lines, oldest timestamp first; **at equal timestamps, `REJECT` sorts before
  `ADMIT`** (an audit reads failures first).
- Determinism contract: same calls, same clock, byte-identical snapshot.

Everything from this course converges here: the clock seam (M19), per-key
state with clear ownership (M6/M11), exact-string reporting (M20), and the
two-sided testing discipline (M15).
''',
    "Tóm Tắt Capstone — Dịch Vụ Admission",
    "Một đặc tả, một bộ test nghiệm thu: admission theo tag với cửa sổ và truy vết, kèm báo cáo vận hành chính xác từng byte. Ship khi bộ test xanh.",
    r'''
## Đặc tả

Bạn là kỹ sư chịu trách nhiệm cho lõi dịch vụ admission. Không có hướng dẫn
cho module này — bộ test nghiệm thu **chính là** đặc tả.

**`AdmissionsCore`** — admission theo tag trên clock xác định:

- `setTagLimit(tag, limit)`: chỉ nhận `tag >= 0`, `limit >= 1`, và chỉ cấu
  hình **lần đầu** cho một tag (set lại thất bại, trả `false`).
- `admit(cls, tag)` — tag lạ bị từ chối; tag còn hạn mức trong cửa sổ thì
  được nhận; người thắng nhận `ordinal` theo thứ tự đến trong tag ở cửa sổ hiện tại.
- Một **cửa sổ** là một mốc timestamp: `admit` đầu tiên ở timestamp mới đặt
  lại bộ đếm và ordinal theo tag.
- Tổng cộng: `admittedCount()`, `rejectedCount()`.

**`OpsReport`** — nhật ký kiểm toán, chấm bằng chuỗi chính xác:

- `record(tMs, code, key)` rồi `snapshot()` tạo dòng `"[ts] CODE key\n"`,
  timestamp cũ trước; **timestamp bằng nhau thì `REJECT` đứng trước `ADMIT`**
  (bản kiểm tra đọc lỗi trước).
- Hợp đồng xác định: cùng lệnh gọi, cùng clock, snapshot giống từng byte.

Mọi thứ trong khóa học hội tụ ở đây: clock seam (M19), trạng thái theo key
với quyền sở hữu rõ (M6/M11), báo cáo chuỗi chính xác (M20), và kỷ luật
test hai chiều (M15).
''',
    "advanced",
)

write_lesson(
    M21, L21B,
    "Design Worksheet — Before You Type",
    "Decide the invariants first: who owns the window, what reset means, and why the report is a total order — then implement once.",
    10,
    r'''
## Decisions to lock before implementing

1. **Window ownership.** Where does "current window" live? (Hint: a single
   timestamp comparison in `admit` — not a timer, not a thread.)
2. **Reset semantics.** A window rolls on the *first* admit at a new
   timestamp: clear usage **and** ordinals together, or nothing.
3. **Reject paths are ordered too.** Unknown tag and exhausted tag are both
   rejections — one counter, two reasons, same discipline.
4. **The report is a total order.** Timestamp asc, then code severity
   (REJECT < ADMIT), then stable insertion — which makes `snapshot()`
   deterministic even for equal-timestamp evidence.
5. **Provenance.** `Admission.ordinal` must survive the roll (restart at 1)
   — learners who store ordinals globally fail the acceptance battery.

Write your answers as comments above each method, then implement. The
acceptance battery below is the grader, in the practice and again — harder —
in the checkpoint.
''',
    "Bảng Thiết Kế — Trước Khi Gõ Code",
    "Chốt bất biến trước: ai sở hữu cửa sổ, reset nghĩa là gì, vì sao báo cáo là thứ tự toàn phần — rồi cài một lần.",
    r'''
## Các quyết định cần chốt trước khi cài

1. **Quyền sở hữu cửa sổ.** "Cửa sổ hiện tại" nằm ở đâu? (Gợi ý: một phép
   so sánh timestamp trong `admit` — không phải timer, không phải thread.)
2. **Ngữ nghĩa reset.** Cửa sổ lăn ở *lần admit đầu* tại timestamp mới: xóa
   hạn mức đã dùng **và** ordinal cùng lúc, hoặc không xóa gì cả.
3. **Đường từ chối cũng có thứ tự.** Tag lạ và tag hết hạn mức đều là từ
   chối — một bộ đếm, hai lý do, cùng kỷ luật.
4. **Báo cáo là thứ tự toàn phần.** Timestamp tăng, rồi độ nghiêm trọng mã
   (REJECT < ADMIT), rồi ổn định theo thứ tự ghi — để `snapshot()` xác định
   cả khi bằng timestamp.
5. **Truy vết.** `Admission.ordinal` phải qua được lần lăn cửa sổ (đặt lại
   từ 1) — ai lưu ordinal toàn cục sẽ trượt bộ test nghiệm thu.

Viết câu trả lời thành chú thích trên từng phương thức, rồi cài. Bộ test
nghiệm thu bên dưới là người chấm, trong bài luyện và lần nữa — khó hơn —
ở checkpoint.
''',
    "advanced",
)

# ------------------------------------------------------------------ practice 1
CAP_CORE_TESTS = [
    ("limits battery",
     r'''{
    FixedClock clk;
    AdmissionsCore core(&clk);
    CHECK(core.setTagLimit(1, 2));
    CHECK(core.setTagLimit(2, 1));
    CHECK(!core.setTagLimit(1, 0));      // limit must be >= 1
    CHECK(!core.setTagLimit(1, -1));
    CHECK(!core.setTagLimit(-3, 1));     // tag must be >= 0
    CHECK(!core.setTagLimit(1, 5));      // first configuration wins
}''',
     "setTagLimit returns false for tag < 0, limit < 1, or a re-set of an existing tag; true only on first successful configuration."),
    ("admission + window rollover battery",
     r'''{
    FixedClock clk;
    AdmissionsCore core(&clk);
    CHECK(core.setTagLimit(1, 2));
    Admission a = core.admit(ClassId::Premium, 1);
    CHECK(a.admitted);
    CHECK(a.ordinal == 1);
    Admission b = core.admit(ClassId::Regular, 1);
    CHECK(b.admitted);
    CHECK(b.ordinal == 2);
    Admission c = core.admit(ClassId::Regular, 1);
    CHECK(!c.admitted);                  // limit reached
    Admission d = core.admit(ClassId::Regular, 9);
    CHECK(!d.admitted);                  // unknown tag
    CHECK(core.admittedCount() == 2);
    CHECK(core.rejectedCount() == 2);
    clk.advance(1000);
    Admission e = core.admit(ClassId::Premium, 1);   // window rolls here
    CHECK(e.admitted);
    CHECK(e.ordinal == 1);               // ordinals restart per window
}''',
     "admit rejects unknown tags and over-limit tags; the first admit at a new timestamp clears usage and ordinals (next ordinal is 1 again)."),
]

CAP_REP_TESTS = [
    ("ops report battery",
     r'''{
    FixedClock clk;
    OpsReport rep(&clk);
    rep.record(10, "ADMIT", "t1#1");
    rep.record(30, "ADMIT", "t2#1");
    rep.record(30, "REJECT", "t1#3");
    rep.record(20, "ADMIT", "t3#1");
    const std::string snap = rep.snapshot();
    CHECK_CONTAINS(snap, "[10] ADMIT t1#1");
    CHECK_CONTAINS(snap, "[20] ADMIT t3#1");
    CHECK_CONTAINS(snap, "[30] REJECT t1#3");
    CHECK_CONTAINS(snap, "[30] ADMIT t2#1");
    const size_t p10 = snap.find("[10]");
    const size_t p20 = snap.find("[20]");
    const size_t p30r = snap.find("[30] REJECT");
    const size_t p30a = snap.find("[30] ADMIT");
    CHECK(p10 < p20 && p20 < p30r);
    CHECK(p30r < p30a);                  // equal ts: REJECT before ADMIT
}''',
     "snapshot sorts by timestamp; ties are broken by code severity (REJECT before ADMIT), then stable insertion order. Lines are exactly \"[ts] CODE key\\n\"."),
    ("determinism battery",
     r'''{
    FixedClock clk;
    OpsReport rep(&clk);
    rep.record(5, "ADMIT", "x");
    rep.record(6, "REJECT", "y");
    const std::string first = rep.snapshot();
    const std::string second = rep.snapshot();
    CHECK_EQ(first, second);
    CHECK_CONTAINS(first, "[6] REJECT y");
}''',
     "snapshot() is pure: repeated calls return byte-identical strings."),
]

write_practice(
    M21, "cppa-capstone-core-practice",
    "Capstone Practice — Admission Core",
    "The tag-limit and window mechanics of the capstone, graded on a deterministic clock.",
    "Luyện Capstone — Lõi Admission",
    "Cơ chế hạn mức theo tag và cửa sổ của capstone, chấm trên clock xác định.",
    L21B, 20, "advanced",
    challenges=[
        challenge(
            "cppa21-capstone-core",
            "Admission Core",
            "Implement `AdmissionsCore` exactly to spec: first-config tag limits, per-window usage and ordinals, unknown-tag rejection, running totals.",
            CP21_BOILER,
            CAP_CORE_TESTS,
            difficulty="advanced",
        ),
    ],
    vi_challenges={
        "cppa21-capstone-core": vi_challenge(
            "Lõi Admission",
            "Cài `AdmissionsCore` đúng đặc tả: hạn mức tag cấu hình lần đầu, hạn mức dùng và ordinal theo cửa sổ, từ chối tag lạ, tổng cộng chạy.",
            [(name, hint) for name, _, hint in CAP_CORE_TESTS],
        ),
    },
    solutions=[
        ("cppa21-capstone-core", CP21_BOILER + "\n" + R_CORE + "\n", CP21_BOILER + "\n" + W_CORE + "\n"),
    ],
)

write_practice(
    M21, "cppa-capstone-report-practice",
    "Capstone Practice — Ops Report",
    "The audit trail as an exact string: total order over timestamps and severities, deterministic by construction.",
    "Luyện Capstone — Báo cáo Vận hành",
    "Nhật ký kiểm toán dưới dạng chuỗi chính xác: thứ tự toàn phần theo timestamp và độ nghiêm trọng, xác định ngay từ thiết kế.",
    L21B, 15, "advanced",
    challenges=[
        challenge(
            "cppa21-capstone-report",
            "Ops Report",
            "Implement `OpsReport::snapshot()`: \"[ts] CODE key\" lines, timestamp ascending, equal-timestamp ties REJECT before ADMIT, byte-deterministic.",
            CP21_BOILER,
            CAP_REP_TESTS,
            difficulty="advanced",
        ),
    ],
    vi_challenges={
        "cppa21-capstone-report": vi_challenge(
            "Báo cáo Vận hành",
            "Cài `OpsReport::snapshot()`: dòng \"[ts] CODE key\", timestamp tăng dần, bằng timestamp thì REJECT trước ADMIT, xác định từng byte.",
            [(name, hint) for name, _, hint in CAP_REP_TESTS],
        ),
    },
    solutions=[
        ("cppa21-capstone-report", CP21_BOILER + "\n" + R_REP + "\n", CP21_BOILER + "\n" + W_REP + "\n"),
    ],
)

# ------------------------------------------------------------------ checkpoint
CAP_SHIP_TESTS = [
    ("ship-gate acceptance battery",
     r'''{
    FixedClock clk;
    AdmissionsCore core(&clk);
    OpsReport rep(&clk);
    CHECK(core.setTagLimit(1, 2));
    CHECK(core.setTagLimit(2, 1));

    Admission a = core.admit(ClassId::Premium, 1);
    Admission b = core.admit(ClassId::Regular, 1);
    Admission c = core.admit(ClassId::Regular, 1);
    Admission d = core.admit(ClassId::Premium, 2);
    Admission e = core.admit(ClassId::Regular, 9);

    rep.record(clk.nowMs(), a.admitted ? "ADMIT" : "REJECT", "p1#t1");
    rep.record(clk.nowMs(), b.admitted ? "ADMIT" : "REJECT", "r1#t1");
    rep.record(clk.nowMs(), c.admitted ? "ADMIT" : "REJECT", "r2#t1");
    rep.record(clk.nowMs(), d.admitted ? "ADMIT" : "REJECT", "p2#t2");
    rep.record(clk.nowMs(), e.admitted ? "ADMIT" : "REJECT", "r3#t9");

    CHECK(core.admittedCount() == 3);
    CHECK(core.rejectedCount() == 2);
    CHECK(a.admitted && a.ordinal == 1);
    CHECK(!c.admitted);
    CHECK(!e.admitted);

    const std::string snap = rep.snapshot();
    CHECK_CONTAINS(snap, "[0] ADMIT p1#t1");
    CHECK_CONTAINS(snap, "[0] REJECT r2#t1");
    CHECK_CONTAINS(snap, "[0] REJECT r3#t9");
    CHECK(snap.find("r2#t1") < snap.find("p2#t2"));   // equal ts: REJECT first
    CHECK(snap.find("r3#t9") < snap.find("p2#t2"));
}
{
    FixedClock clk;
    AdmissionsCore core(&clk);
    OpsReport rep(&clk);
    CHECK(core.setTagLimit(4, 1));
    core.admit(ClassId::Premium, 4);
    clk.advance(1500);
    Admission nxt = core.admit(ClassId::Regular, 4);
    rep.record(clk.nowMs(), nxt.admitted ? "ADMIT" : "REJECT", "r#t4");
    CHECK(nxt.admitted);
    CHECK(nxt.ordinal == 1);
    CHECK(core.rejectedCount() == 0);
    CHECK_CONTAINS(rep.snapshot(), "[1500] ADMIT r#t4");
}''',
     "Run the whole service on the FixedClock: window rollover restarts ordinals, unknown tags are rejections, and the report reads failures before successes at equal timestamps."),
]

write_checkpoint(
    M21, L21C,
    "Checkpoint — Ship Gate",
    "The full acceptance battery over both capstone components: admission semantics and the exact audit trail, on one deterministic clock.",
    25,
    r'''
## The ship gate

This is the course's final graded challenge: `AdmissionsCore` and `OpsReport`
driven end-to-end on the `FixedClock`, with the acceptance battery as the
only authority. Everything is deterministic — if your design decisions from
the worksheet hold, the battery is green; if any invariant leaks (a global
ordinal, a stable tie order in the report, a window that never rolls), the
battery names it.

Shipping is not "it compiles". Shipping is: **reference passes, and every
documented wrong variant fails.**
''',
    "Điểm Chốt — Cổng Ship",
    "Bộ test nghiệm thu đầy đủ trên cả hai thành phần capstone: ngữ nghĩa admission và nhật ký kiểm tra chính xác, trên một clock xác định.",
    r'''
## Cổng ship

Đây là thử thách chấm điểm cuối của khóa học: `AdmissionsCore` và
`OpsReport` chạy trọn vẹn trên `FixedClock`, với bộ test nghiệm thu là thẩm
quyền duy nhất. Mọi thứ đều xác định — nếu các quyết định thiết kế trong
bảng giữ vững, bộ test xanh; nếu bất kỳ bất biến nào rò rỉ (ordinal toàn
cục, thứ tự hòa ổn định trong báo cáo, cửa sổ không bao giờ lăn), bộ test
sẽ chỉ tên.

Ship không phải là "biên dịch được". Ship là: **bản tham chiếu pass, và mọi
biến thể sai được ghi nhận đều fail.**
''',
    challenge(
        "cppa21-capstone-ship",
        "Ship Gate — Full Service Battery",
        "Wire `AdmissionsCore` + `OpsReport` end-to-end on the `FixedClock` and satisfy the acceptance battery.",
        CP21_BOILER,
        CAP_SHIP_TESTS,
        difficulty="advanced",
    ),
    vi_challenge(
        "Cổng Ship — Bộ Test Toàn Diện",
        "Nối `AdmissionsCore` + `OpsReport` trọn vẹn trên `FixedClock` và vượt bộ test nghiệm thu.",
        [(name, hint) for name, _, hint in CAP_SHIP_TESTS],
    ),
    solution=CP21_BOILER + "\n" + R_CORE + "\n" + R_REP + "\n",
    wrong=CP21_BOILER + "\n" + W_CORE + "\n" + R_REP + "\n",
)

write_module(
    M21,
    "Capstone — High-Performance Service",
    "Integrate the whole course in one deterministic service core: admission windows with provenance, an exact audit trail, and a ship gate that accepts nothing less.",
    "Capstone — Dịch Vụ Hiệu Năng Cao",
    "Hội tụ toàn bộ khóa học trong một lõi dịch vụ xác định: cửa sổ admission có truy vết, nhật ký kiểm toán chính xác, và cổng ship không chấp nhận thỏa hiệp.",
    [L21A, L21B, L21C],
    ["cppa-capstone-core-practice", "cppa-capstone-report-practice"],
)

print("module 21 (capstone-hpc-service) authored")
