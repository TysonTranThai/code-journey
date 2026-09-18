#!/usr/bin/env python3
"""Java — Intermediate — Module 8: java-testing-deep.

Testing as engineering: AAA discipline, seams and test doubles, edge-case
nets, and deterministic tests. JUnit is taught conceptually (annotations
and lifecycle) while graded challenges use the platform's CjTestBase
harness — honest about the difference. House conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-testing-deep"

# ── lesson 8.1 — AAA & naming ───────────────────────────────────────────────
L_AAA_EN = r"""
## AAA and tests that read like specs

Every good test has three blocks, visibly separated:

```java
// Arrange — build the world
var cart = new Cart();
cart.add(new Item("pen", 200));

// Act — one behavior
int total = cart.totalCents();

// Assert — one expectation
assertEquals(200, total);
```

Discipline that scales:
- **One behavior per test** — two asserts of the same behavior are fine;
  two behaviors are not
- **Name = scenario + expectation**: `total_includes_quantity_multiplier`,
  not `testTotal`
- **No logic in tests** (no loops, no ifs) — if you need logic, you're
  re-implementing the subject under test
- Tests are the first reader of your API: if arranging is painful, the
  API needs a builder or factory

A failing test message should tell you what broke without opening a
debugger — that's why `checkEq(actual, expected, "what")` takes a label.
"""

L_AAA_VI = r"""
## AAA và test đọc như đặc tả

Mọi test tốt có ba khối, tách bạch rõ ràng:

```java
// Arrange — dựng thế giới
var cart = new Cart();
cart.add(new Item("pen", 200));

// Act — một hành vi
int total = cart.totalCents();

// Assert — một kỳ vọng
assertEquals(200, total);
```

Kỷ luật mở rộng được:
- **Một hành vi mỗi test** — hai assert cùng hành vi thì được; hai hành
  vi thì không
- **Tên = kịch bản + kỳ vọng**: `total_includes_quantity_multiplier`,
  không phải `testTotal`
- **Không logic trong test** (không vòng lặp, không if) — nếu cần logic,
  bạn đang viết lại phần mềm đang được test
- Test là người đọc đầu tiên của API: nếu Arrange đau khổ, API cần thêm
  builder hoặc factory

Thông báo test thất bại phải cho biết cái gì vỡ mà không cần mở debugger
— vì vậy `checkEq(actual, expected, "what")` có nhãn.
"""

# ── lesson 8.2 — seams & test doubles ──────────────────────────────────────
L_DOUBLES_EN = r"""
## Seams and test doubles

A *seam* is a replaceable point in code — usually a constructor-injected
interface. Doubles plug into seams:

- **Stub** — returns canned data (`FakeGateway` from Module 2)
- **Fake** — a working lightweight implementation (in-memory repo)
- **Spy** — records calls for later verification
- **Mock** — pre-programmed expectations (use sparingly; mocks that know
  too much make refactoring painful)

```java
interface Clock { Instant now(); }

class SubscriptionService {
    private final Clock clock;
    SubscriptionService(Clock clock) { this.clock = clock; }
    boolean isExpired(Instant until) { return clock.now().isAfter(until); }
}

// test: freeze time instead of sleeping/_waiting
Clock frozen = () -> Instant.parse("2026-09-14T00:00:00Z");
```

The rule: if code calls `Instant.now()` or `Math.random()` deep inside,
it has no seam — extract the decision behind an interface. Deterministic
tests are the payoff.
"""

L_DOUBLES_VI = r"""
## Seam và test double

*Seam* là điểm có thể thay thế trong code — thường là interface được tiêm
qua constructor. Double cắm vào seam:

- **Stub** — trả dữ liệu đóng gói sẵn (`FakeGateway` từ Module 2)
- **Fake** — hiện thực nhẹ hoạt động thật (repo trong bộ nhớ)
- **Spy** — ghi lại các lần gọi để kiểm chứng sau
- **Mock** — kỳ vọng được lập trình sẵn (dùng tiết chế; mock biết quá
  nhiều khiến refactor đau đớn)

```java
interface Clock { Instant now(); }

class SubscriptionService {
    private final Clock clock;
    SubscriptionService(Clock clock) { this.clock = clock; }
    boolean isExpired(Instant until) { return clock.now().isAfter(until); }
}

// test: đóng băng thời gian thay vì ngủ/đợi
Clock frozen = () -> Instant.parse("2026-09-14T00:00:00Z");
```

Quy tắc: nếu code gọi `Instant.now()` hoặc `Math.random()` chìm sâu bên
trong, nó không có seam — tách quyết định đó sau một interface. Kết quả
là test xác định được.
"""

# ── lesson 8.3 — edge cases & determinism ──────────────────────────────────
L_EDGE_EN = r"""
## Edge-case nets and determinism

An intermediate test suite hunts *boundaries*:

- **empty / single / many** — the three sizes every collection behavior
  must satisfy
- **zero, min, max** — numeric edges (0, Integer.MIN_VALUE, MAX_VALUE)
- **first / last / middle** — position-sensitive logic
- **duplicate and absent keys** — map semantics
- **null vs empty vs blank** — three different "nothings"

```java
// boundary net for a discount function
checkEq(discount(0), 0, "zero price");
checkEq(discount(1), 1, "minimal price");
checkEq(discount(Integer.MAX_VALUE), ..., "max price");
```

Determinism rules:
- never assert on unordered collections' toString (order is incidental)
- sort or compare as sets when order doesn't matter
- fixed seeds for randomness; frozen clocks for time
- a test that *sometimes* fails is worse than one that always fails —
  fix or delete it today

Regression nets: when you fix a bug, add the test that would have caught
it — forever.
"""

L_EDGE_VI = r"""
## Lưới case biên và tính xác định

Suite test trình trung cấp săn *biên*:

- **rỗng / một / nhiều** — ba kích thước mọi hành vi collection phải thỏa
- **0, min, max** — biên số học (0, Integer.MIN_VALUE, MAX_VALUE)
- **đầu / cuối / giữa** — logic nhạy cảm vị trí
- **key trùng và key vắng** — ngữ nghĩa map
- **null vs rỗng vs blank** — ba kiểu "không có gì" khác nhau

```java
// lưới biên cho hàm giảm giá
checkEq(discount(0), 0, "giá 0");
checkEq(discount(1), 1, "giá nhỏ nhất");
checkEq(discount(Integer.MAX_VALUE), ..., "giá lớn nhất");
```

Quy tắc xác định:
- không bao giờ assert trên toString của collection không thứ tự (thứ tự
  là ngẫu nhiên)
- sort hoặc so như set khi thứ tự không quan trọng
- seed cố định cho random; đồng hồ đóng băng cho thời gian
- test *thi thoảng* fail còn tệ hơn test luôn fail — sửa hoặc xóa ngay
  hôm nay

Lưới hồi quy: khi sửa một bug, thêm test lẽ ra bắt được nó — vĩnh viễn.
"""

write_module(
    MOD,
    "Testing Like a Professional",
    "AAA discipline, seams and test doubles, boundary nets, and the determinism rules that keep suites trustworthy.",
    "Kiểm thử như dân chuyên nghiệp",
    "Kỷ luật AAA, seam và test double, lưới case biên, và các quy tắc xác định giữ cho bộ test đáng tin.",
    ["aaa-discipline", "seams-doubles", "edge-determinism", "javi-checkpoint-testing"],
    ["javi-p8-testing"],
)

write_lesson(MOD, "aaa-discipline", "AAA & Test Naming", "The three-block shape, one behavior per test, and names that read like specifications.", 12, L_AAA_EN, "AAA & đặt tên test", "Dáng ba khối, một hành vi mỗi test, và cái tên đọc như đặc tả.", L_AAA_VI)

write_lesson(MOD, "seams-doubles", "Seams & Test Doubles", "Stubs, fakes, spies, mocks — and extracting Clock-like seams so time and randomness stop leaking into tests.", 14, L_DOUBLES_EN, "Seam & test double", "Stub, fake, spy, mock — và tách seam kiểu Clock để thời gian và random thôi rò vào test.", L_DOUBLES_VI)

write_lesson(MOD, "edge-determinism", "Edge Cases & Determinism", "The boundary checklist, order-blind assertions, and the regression-net habit after every bug fix.", 13, L_EDGE_EN, "Case biên & tính xác định", "Checklist biên, assert mù thứ tự, và thói quen lưới hồi quy sau mỗi lần sửa bug.", L_EDGE_VI)

# ── practice set ────────────────────────────────────────────────────────────
P8_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement types and methods below.
}
"""

CH_P8_CLOCK = challenge(
    "javi-p8-frozen-clock",
    "Freeze Time Behind a Seam",
    r"""Design time-dependent logic testably inside `Solution`:
- `interface Clock { java.time.Instant now(); }`
- `static class Trial` with a constructor `(Clock clock)`; method
  `boolean isActive(java.time.Instant start, java.time.Instant end)`
  returning `!clock.now().isBefore(start) && clock.now().isBefore(end)`.
- `static Clock frozenAt(String iso)` — a Clock pinned to that instant.

The tests freeze time instead of sleeping — the entire point of the seam.""",
    P8_BOILER,
    [
        (
            "active within window",
            r"""
Solution.Clock c = Solution.frozenAt("2026-09-14T12:00:00Z");
Solution.Trial t = new Solution.Trial(c);
checkEq(t.isActive(
    java.time.Instant.parse("2026-09-14T00:00:00Z"),
    java.time.Instant.parse("2026-09-15T00:00:00Z")), true, "inside window");
""",
            "Frozen now (12:00) is after start and before end.",
        ),
        (
            "expired after end",
            r"""
Solution.Clock c = Solution.frozenAt("2026-09-16T12:00:00Z");
Solution.Trial t = new Solution.Trial(c);
checkEq(t.isActive(
    java.time.Instant.parse("2026-09-14T00:00:00Z"),
    java.time.Instant.parse("2026-09-15T00:00:00Z")), false, "after end");
""",
            "now past end → false.",
        ),
        (
            "not yet started",
            r"""
Solution.Clock c = Solution.frozenAt("2026-09-13T12:00:00Z");
Solution.Trial t = new Solution.Trial(c);
checkEq(t.isActive(
    java.time.Instant.parse("2026-09-14T00:00:00Z"),
    java.time.Instant.parse("2026-09-15T00:00:00Z")), false, "before start");
""",
            "now before start → false.",
        ),
        (
            "start instant itself is active",
            r"""
Solution.Clock c = Solution.frozenAt("2026-09-14T00:00:00Z");
Solution.Trial t = new Solution.Trial(c);
checkEq(t.isActive(
    java.time.Instant.parse("2026-09-14T00:00:00Z"),
    java.time.Instant.parse("2026-09-15T00:00:00Z")), true, "inclusive start");
""",
            "now == start must count as active — the boundary catches strict-comparison bugs.",
        ),
    ],
    level="guided",
)

CH_P8_NET = challenge(
    "javi-p8-boundary-net",
    "Build the Boundary Net",
    r"""`static int clamp(int v, int lo, int hi)` needs a real test net.
Implement clamp, then write the net via `static List<String> selfCheck()`
returning one line per property it satisfies, in this exact order:
- `"low"` — clamp(5, 10, 20) == 10
- `"high"` — clamp(25, 10, 20) == 20
- `"in-range"` — clamp(15, 10, 20) == 15
- `"identity-at-bounds"` — clamp(10, 10, 20) == 10 && clamp(20, 10, 20) == 20

The grader verifies both the implementation AND that the net exists —
tests are deliverables here.""",
    P8_BOILER,
    [
        (
            "clamp behavior",
            r"""
checkEq(Solution.clamp(5, 10, 20), 10, "below lo");
checkEq(Solution.clamp(25, 10, 20), 20, "above hi");
checkEq(Solution.clamp(15, 10, 20), 15, "in range");
""",
            "Math.max(lo, Math.min(v, hi)).",
        ),
        (
            "bounds are inclusive",
            r"""
checkEq(Solution.clamp(10, 10, 20), 10, "lo inclusive");
checkEq(Solution.clamp(20, 10, 20), 20, "hi inclusive");
""",
            "Both endpoints pass through unchanged.",
        ),
        (
            "selfCheck reports the net",
            r"""
List<String> net = Solution.selfCheck();
checkEq(net, List.of("low", "high", "in-range", "identity-at-bounds"), "net present");
""",
            "One label per boundary property, in order.",
        ),
    ],
    level="independent",
)

CH_P8_ORDERBLIND = challenge(
    "javi-p8-order-blind",
    "Order-Blind Assertions",
    r"""Implement `static Set<String> uniqueTags(String csv)` — split on
commas, trim each, drop empties, collect as a Set.

Then implement `static boolean sameContent(List<String> a, List<String> b)`
returning true when both lists contain the same elements with the same
multiplicities — regardless of order (sort copies, or count with a map).

The lesson: never assert on a HashSet's iteration order; assert on
content instead.""",
    P8_BOILER,
    [
        (
            "tags dedupe and trim",
            r"""
checkEq(Solution.uniqueTags(" a , b ,  ,a "), Set.of("a", "b"), "content only");
""",
            "Set equality is order-blind by nature.",
        ),
        (
            "sameContent ignores order",
            r"""
checkEq(Solution.sameContent(List.of("x", "y", "x"), List.of("x", "x", "y")), true, "same multiset");
checkEq(Solution.sameContent(List.of("x", "y"), List.of("x", "x")), false, "different counts");
""",
            "Compare sorted copies or frequency maps.",
        ),
        (
            "empty handling",
            r"""
checkEq(Solution.uniqueTags("  "), Set.of(), "empty set");
checkEq(Solution.sameContent(List.of(), List.of()), true, "both empty");
""",
            "Blank input → empty set; two empties are equal.",
        ),
    ],
    level="independent",
)

VI_CH_P8_CLOCK = vi_challenge(
    "Đóng băng thời gian sau seam",
    r"""Thiết kế logic phụ thuộc thời gian có thể test bên trong `Solution`:
- `interface Clock { java.time.Instant now(); }`
- `static class Trial` với constructor `(Clock clock)`; method
  `boolean isActive(java.time.Instant start, java.time.Instant end)`
  trả `!clock.now().isBefore(start) && clock.now().isBefore(end)`.
- `static Clock frozenAt(String iso)` — Clock đóng băng tại thời điểm đó.

Test đóng băng thời gian thay vì ngủ/đợi — đó là toàn bộ ý nghĩa của seam.""",
    [
        ("Hoạt động trong cửa sổ", "now đóng băng (12:00) sau start và trước end."),
        ("Hết hạn sau end", "now quá end → false."),
        ("Chưa bắt đầu", "now trước start → false."),
        ("Đúng thời điểm start vẫn hoạt động", "now == start phải tính là hoạt động — biên này bắt bug so sánh nghiêm ngặt."),
    ],
)

VI_CH_P8_NET = vi_challenge(
    "Dựng lưới case biên",
    r"""`static int clamp(int v, int lo, int hi)` cần một lưới test thật.
Cài clamp, rồi viết lưới qua `static List<String> selfCheck()` trả một
dòng cho mỗi tính chất nó thỏa, đúng thứ tự này:
- `"low"` — clamp(5, 10, 20) == 10
- `"high"` — clamp(25, 10, 20) == 20
- `"in-range"` — clamp(15, 10, 20) == 15
- `"identity-at-bounds"` — clamp(10, 10, 20) == 10 && clamp(20, 10, 20) == 20

Máy chấm kiểm cả hiện thực LẪN sự tồn tại của lưới — test ở đây là sản
phẩm giao hàng.""",
    [
        ("Hành vi clamp", "Math.max(lo, Math.min(v, hi))."),
        ("Hai biên thuộc khoảng", "Cả hai đầu đi qua không đổi."),
        ("selfCheck báo lưới", "Một nhãn mỗi tính chất biên, theo thứ tự."),
    ],
)

VI_CH_P8_ORDERBLIND = vi_challenge(
    "Assert mù thứ tự",
    r"""Cài `static Set<String> uniqueTags(String csv)` — tách theo dấu phẩy,
trim từng phần, bỏ phần rỗng, gom thành Set.

Rồi cài `static boolean sameContent(List<String> a, List<String> b)`
trả true khi hai list chứa cùng phần tử với cùng số lần xuất hiện — bất
kể thứ tự (sort bản sao, hoặc đếm bằng map).

Bài học: không bao giờ assert trên thứ tự duyệt của HashSet; assert trên
nội dung thay thế.""",
    [
        ("Tag khử trùng lặp và trim", "Phép bằng Set mù thứ tự sẵn."),
        ("sameContent bỏ qua thứ tự", "So bản sao đã sort hoặc map tần suất."),
        ("Xử lý rỗng", "Input blank → set rỗng; hai cái rỗng bằng nhau."),
    ],
)

write_practice(
    MOD,
    "javi-p8-testing",
    "Testing Lab",
    "Frozen-clock seams, boundary nets as deliverables, and order-blind assertions.",
    "Xưởng kiểm thử",
    "Seam đồng hồ đóng băng, lưới biên như sản phẩm, và assert mù thứ tự.",
    "edge-determinism",
    40,
    "intermediate",
    [CH_P8_CLOCK, CH_P8_NET, CH_P8_ORDERBLIND],
    {CH_P8_CLOCK["id"]: VI_CH_P8_CLOCK, CH_P8_NET["id"]: VI_CH_P8_NET, CH_P8_ORDERBLIND["id"]: VI_CH_P8_ORDERBLIND},
    solutions=[
        (
            CH_P8_CLOCK["id"],
            r"""
import java.time.*;

public class Solution {
    public interface Clock { Instant now(); }

    public static class Trial {
        private final Clock clock;
        public Trial(Clock clock) { this.clock = clock; }
        public boolean isActive(Instant start, Instant end) {
            Instant now = clock.now();
            return !now.isBefore(start) && now.isBefore(end);
        }
    }

    public static Clock frozenAt(String iso) {
        Instant pinned = Instant.parse(iso);
        return () -> pinned;
    }
}
""",
            r"""
import java.time.*;

public class Solution {
    public interface Clock { Instant now(); }

    public static class Trial {
        private final Clock clock;
        public Trial(Clock clock) { this.clock = clock; }
        // W: strict start comparison — a trial is reported inactive at
        // its exact start instant (now.isAfter(start) excludes equality).
        public boolean isActive(Instant start, Instant end) {
            Instant now = clock.now();
            return now.isAfter(start) && now.isBefore(end);
        }
    }

    public static Clock frozenAt(String iso) {
        Instant pinned = Instant.parse(iso);
        return () -> pinned;
    }
}
""",
        ),
        (
            CH_P8_NET["id"],
            r"""
import java.util.*;

public class Solution {
    public static int clamp(int v, int lo, int hi) {
        return Math.max(lo, Math.min(v, hi));
    }

    public static List<String> selfCheck() {
        List<String> net = new ArrayList<>();
        if (clamp(5, 10, 20) == 10) net.add("low");
        if (clamp(25, 10, 20) == 20) net.add("high");
        if (clamp(15, 10, 20) == 15) net.add("in-range");
        if (clamp(10, 10, 20) == 10 && clamp(20, 10, 20) == 20) net.add("identity-at-bounds");
        return net;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    // W: clamp floors at lo but never caps at hi — every above-hi test
    // in the net catches it (and selfCheck honestly omits "high").
    public static int clamp(int v, int lo, int hi) {
        return Math.max(lo, v);
    }

    public static List<String> selfCheck() {
        List<String> net = new ArrayList<>();
        if (clamp(5, 10, 20) == 10) net.add("low");
        if (clamp(25, 10, 20) == 20) net.add("high");
        if (clamp(15, 10, 20) == 15) net.add("in-range");
        if (clamp(10, 10, 20) == 10 && clamp(20, 10, 20) == 20) net.add("identity-at-bounds");
        return net;
    }
}
""",
        ),
        (
            CH_P8_ORDERBLIND["id"],
            r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static Set<String> uniqueTags(String csv) {
        return Arrays.stream(csv.split(","))
            .map(String::trim)
            .filter(s -> !s.isEmpty())
            .collect(Collectors.toSet());
    }

    public static boolean sameContent(List<String> a, List<String> b) {
        if (a == null || b == null) return a == b;
        List<String> sa = new ArrayList<>(a), sb = new ArrayList<>(b);
        Collections.sort(sa);
        Collections.sort(sb);
        return sa.equals(sb);
    }
}
""",
            r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static Set<String> uniqueTags(String csv) {
        return Arrays.stream(csv.split(","))
            .map(String::trim)
            .filter(s -> !s.isEmpty())
            .collect(Collectors.toSet());
    }

    // W: sameContent compares lists positionally — order-sensitive, so
    // ["x","y"] vs ["y","x"] wrongly reports false. The order-blind
    // contract is the whole point.
    public static boolean sameContent(List<String> a, List<String> b) {
        if (a == null || b == null) return a == b;
        return a.equals(b);
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — testing

You can now: structure AAA tests that read like specs, freeze time behind
seams, and ship boundary nets as deliverables. Prove it with a rate
limiter designed for testability.
"""

CP_MDX_VI = r"""
## Checkpoint — kiểm thử

Giờ bạn có thể: cấu trúc test AAA đọc như đặc tả, đóng băng thời gian sau
seam, và giao lưới biên như sản phẩm. Chứng minh bằng một bộ giới hạn tần
suất thiết kế để test được.
"""

CH_CP8 = challenge(
    "javi-checkpoint-m8-testing",
    "Testable Rate Limiter",
    r"""Design a rate limiter around a Clock seam in `Solution`:
- `interface Clock { long nowMillis(); }`
- `static class RateLimiter` with constructor `(Clock clock, int maxPerWindow)`
  and `boolean allow(String key)`:
  - counts calls per key within a 1000ms rolling window (from the clock)
  - returns true if under the limit, false otherwise
  - calls OLDER than 1000ms (strictly) no longer count
- `static Clock manualClock(long startMillis)` returns a mutable-ish
  clock advanced by calling `((Solution.AdvanceableClock) c).advance(ms)`
  — define `static interface AdvanceableClock extends Clock` with
  `void advance(long ms)`.

The tests drive time explicitly — no sleeps.""",
    r"""
import java.util.*;

public class Solution {
    // Provide Clock, AdvanceableClock, manualClock, RateLimiter here.
}
""",
    [
        (
            "under limit allows",
            r"""
Solution.Clock c = Solution.manualClock(0);
Solution.RateLimiter rl = new Solution.RateLimiter(c, 2);
checkEq(rl.allow("u"), true, "first");
checkEq(rl.allow("u"), true, "second");
""",
            "Two calls within the window pass.",
        ),
        (
            "third call blocked",
            r"""
Solution.Clock c = Solution.manualClock(0);
Solution.RateLimiter rl = new Solution.RateLimiter(c, 2);
rl.allow("u"); rl.allow("u");
checkEq(rl.allow("u"), false, "over limit");
""",
            "maxPerWindow is a hard cap.",
        ),
        (
            "window rolls with the clock",
            r"""
Solution.AdvanceableClock c = Solution.manualClock(0);
Solution.RateLimiter rl = new Solution.RateLimiter(c, 1);
rl.allow("u");
c.advance(1500);
checkEq(rl.allow("u"), true, "old call expired");
""",
            "After advancing 1500ms, the old call (>1000ms) drops out.",
        ),
        (
            "keys are independent",
            r"""
Solution.Clock c = Solution.manualClock(0);
Solution.RateLimiter rl = new Solution.RateLimiter(c, 1);
checkEq(rl.allow("a"), true, "key a");
checkEq(rl.allow("b"), true, "key b");
""",
            "Limit is per key.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP8 = vi_challenge(
    "Bộ giới hạn tần suất test được",
    r"""Thiết kế rate limiter quanh một seam Clock trong `Solution`:
- `interface Clock { long nowMillis(); }`
- `static class RateLimiter` với constructor `(Clock clock, int maxPerWindow)`
  và `boolean allow(String key)`:
  - đếm lượt gọi theo key trong cửa sổ trượt 1000ms (từ clock)
  - trả true nếu dưới hạn mức, false nếu ngược lại
  - các lượt gọi CŨ hơn 1000ms (nghiêm ngặt) không còn được đếm
- `static Clock manualClock(long startMillis)` trả một clock có thể tua
  bằng cách gọi `((Solution.AdvanceableClock) c).advance(ms)` — định nghĩa
  `static interface AdvanceableClock extends Clock` với
  `void advance(long ms)`.

Test điều khiển thời gian tường minh — không ngủ.""",
    [
        ("Dưới hạn mức được qua", "Hai lượt gọi trong cửa sổ đi qua."),
        ("Lượt thứ ba bị chặn", "maxPerWindow là trần cứng."),
        ("Cửa sổ trượt theo clock", "Sau khi tua 1500ms, lượt cũ (>1000ms) rơi ra."),
        ("Các key độc lập", "Hạn mức tính theo key."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-testing",
    "Checkpoint: Testing",
    "Graded checkpoint: a rolling-window rate limiter whose time is fully controlled by an advanceable clock seam.",
    15,
    CP_MDX,
    "Checkpoint: Kiểm thử",
    "Checkpoint chấm điểm: rate limiter cửa sổ trượt với thời gian hoàn toàn điều khiển bởi seam clock có thể tua.",
    CP_MDX_VI,
    CH_CP8,
    VI_CH_CP8,
    solution=r"""
import java.util.*;

public class Solution {
    public interface Clock { long nowMillis(); }
    public interface AdvanceableClock extends Clock { void advance(long ms); }

    public static AdvanceableClock manualClock(long startMillis) {
        return new AdvanceableClock() {
            private long now = startMillis;
            public long nowMillis() { return now; }
            public void advance(long ms) { now += ms; }
        };
    }

    public static class RateLimiter {
        private final Clock clock;
        private final int maxPerWindow;
        private final Map<String, List<Long>> calls = new HashMap<>();

        public RateLimiter(Clock clock, int maxPerWindow) {
            this.clock = clock;
            this.maxPerWindow = maxPerWindow;
        }

        public boolean allow(String key) {
            long now = clock.nowMillis();
            List<Long> stamps = calls.computeIfAbsent(key, k -> new ArrayList<>());
            stamps.removeIf(t -> now - t >= 1000);
            if (stamps.size() >= maxPerWindow) return false;
            stamps.add(now);
            return true;
        }
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public interface Clock { long nowMillis(); }
    public interface AdvanceableClock extends Clock { void advance(long ms); }

    public static AdvanceableClock manualClock(long startMillis) {
        return new AdvanceableClock() {
            private long now = startMillis;
            public long nowMillis() { return now; }
            public void advance(long ms) { now += ms; }
        };
    }

    public static class RateLimiter {
        private final Clock clock;
        private final int maxPerWindow;
        private final Map<String, List<Long>> calls = new HashMap<>();

        public RateLimiter(Clock clock, int maxPerWindow) {
            this.clock = clock;
            this.maxPerWindow = maxPerWindow;
        }

        // W: expiry never runs (removeIf guarded by an always-false
        // condition), so old calls block forever — the rolling window
        // is the entire feature.
        public boolean allow(String key) {
            long now = clock.nowMillis();
            List<Long> stamps = calls.computeIfAbsent(key, k -> new ArrayList<>());
            if (false) stamps.removeIf(t -> now - t >= 1000);
            if (stamps.size() >= maxPerWindow) return false;
            stamps.add(now);
            return true;
        }
    }
}
""",
)
