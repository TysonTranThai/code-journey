#!/usr/bin/env python3
"""Module 13: advanced-testing — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "advanced-testing"

# ── lesson 1 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "test-strategy",
    "Testing Strategy: The Pyramid and the Budget",
    "Unit, integration, and system tests trade speed for realism — allocate deliberately, and keep the suite deterministic.",
    28,
    """
## The pyramid, honestly

- **Unit tests** — one function/class, dependencies faked. Thousands; each
  runs in milliseconds. They pin behavior *within* the code.
- **Integration tests** — several real pieces together (a repository against a
  real database, a handler with its real validation). Hundreds. They pin the
  *seams* — the places unit tests structurally cannot see.
- **System/end-to-end tests** — the whole service from the outside. Dozens.
  Slow and brittle; reserve them for the critical journeys (signup, checkout,
  login).

Inverted pyramids (mostly E2E) are slow, flaky, and diagnose backwards. Ice-cream
cones (mostly manual) aren't testing at all.

## Fakes, stubs, mocks — and the trade each makes

- **Stub**: hard-coded answers for calls ("the clock says noon").
- **Fake**: a working lightweight implementation (in-memory repository).
- **Mock**: records interactions and asserts on them.

Preference order for *stateful* dependencies: **fake first** — it tests
behavior, survives refactors, and reads like the domain. Mocks shine for
*interaction* contracts that have no meaningful state (did the email service
get called at all?). Over-mocked suites verify the implementation, not the
behavior — and fail on every refactor.

## Flaky tests are bugs in the test

A test that passes on retry is lying about something: time, randomness, network
ordering, shared state. The standard suspects and their cures:

- **time** — inject a clock; never `datetime.now()` deep inside logic under test,
- **randomness** — seed it explicitly (`random.Random(42)`),
- **shared fixtures** — each test constructs its own world (factory functions),
- **order dependence** — if test B only passes after test A, B is broken.

`pytest-randomly` and `-p no:cacheprovider`-style hygiene make order
dependence visible. A suite you cannot trust at face value is worse than no
suite: it teaches the team to ignore red.

## Fixtures architecture

Fixtures scale by *composition*, not inheritance: small fixtures (clock, empty
repository) compose into bigger ones (populated world), and `conftest.py` shares
them by directory scope. Factory functions (`make_order(customer=..., total=...)`
with sensible defaults) beat monolithic fixtures: each test states only the
facts it cares about.

## Coverage: a smoke detector, not a goal

90% coverage with weak assertions measures typing effort. Cover the *branches
that carry risk*: error paths, boundaries (empty, one, many), and every bug you
have ever shipped (regression tests). Mutation testing — flipping an operator
and checking some test fails — measures whether your assertions can actually
detect change.
""",
    "Chiến lược kiểm thử: Kim tự tháp và ngân sách",
    "Unit, integration và system test đánh đổi tốc độ lấy tính thực tế — phân bổ có chủ đích, và giữ bộ test xác định được.",
    """
## Kim tự tháp, nói thẳng

- **Unit test** — một hàm/lớp, dependency bị làm giả. Hàng nghìn; mỗi cái chạy
  trong mili giây. Chúng ghim hành vi *bên trong* code.
- **Integration test** — nhiều mảnh thật ghép với nhau (repository với database
  thật, handler với validation thật). Hàng trăm. Chúng ghim các *điểm nối* —
  nơi unit test vốn không thể nhìn thấy.
- **System/end-to-end test** — toàn bộ dịch vụ nhìn từ bên ngoài. Hàng chục.
  Chậm và dễ gãy; dành cho các hành trình quan trọng (đăng ký, thanh toán,
  đăng nhập).

Kim tự tháp ngược (chủ yếu E2E) thì chậm, dễ rung, và chẩn đoán ngược từ trên
xuống. Kem-ly (chủ yếu thủ công) không phải là kiểm thử.

## Fake, stub, mock — và cái giá của từng loại

- **Stub**: câu trả lời cứng cho các lời gọi ("đồng hồ说 12 giờ").
- **Fake**: một bản cài nhẹ hoạt động được (repository trong bộ nhớ).
- **Mock**: ghi lại các tương tác và khẳng định trên chúng.

Thứ tự ưu tiên cho dependency *có trạng thái*: **fake trước** — nó test hành
vi, sống sót qua refactor, và đọc như chính domain. Mock tỏa sáng với hợp đồng
*tương tác* không có trạng thái đáng kể (dịch vụ email có được gọi không?).
Suite bị quá nhiều mock xác minh bản cài đặt chứ không phải hành vi — và fail
trong mọi lần refactor.

## Test flaky là bug nằm trong bài test

Bài test pass khi chạy lại đang nói dối về điều gì đó: thời gian, tính ngẫu
nhiên, thứ tự mạng, trạng thái chia sẻ. Các nghi phạm kinh điển và thuốc của
chúng:

- **thời gian** — tiêm một đồng hồ; không bao giờ `datetime.now()` sâu trong
  logic được test,
- **tính ngẫu nhiên** — seed tường minh (`random.Random(42)`),
- **fixture chia sẻ** — mỗi bài test tự dựng thế giới của mình (hàm factory),
- **phụ thuộc thứ tự** — nếu test B chỉ pass sau test A, B đã hỏng.

`pytest-randomly` và các thói quen tương tự khiến sự phụ thuộc thứ tự hiện
hình. Một suite bạn không thể tin ở lần chạy đầu còn tệ hơn không có suite:
nó dạy cả đội phớt lờ màu đỏ.

## Kiến trúc fixture

Fixture mở rộng bằng *kết hợp*, không phải kế thừa: các fixture nhỏ (đồng hồ,
repository rỗng) kết hợp thành fixture lớn (thế giới có dữ liệu), và
`conftest.py` chia sẻ chúng theo phạm vi thư mục. Hàm factory
(`make_order(customer=..., total=...)` với default hợp lý) đánh bại fixture
khổng lồ: mỗi test chỉ nêu những sự thật nó quan tâm.

## Coverage: một đầu báo khói, không phải mục tiêu

90% coverage với assertion yếu chỉ đo công sức gõ phím. Hãy phủ các *nhánh mang
rủi ro*: đường lỗi, biên (rỗng, một, nhiều), và mọi bug từng ship (bài test
hồi quy). Mutation testing — lật một toán tử và kiểm tra có test nào fail không
— đo xem assertion của bạn thực sự phát hiện thay đổi được hay không.
""",
)

# ── lesson 2 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "property-and-contracts",
    "Property-Based Testing and Contracts",
    "Test the invariants instead of examples: generate hundreds of inputs, shrink the failures, and let the types carry part of the proof.",
    30,
    """
## Example tests pin; property tests generalize

An example test says: `sort([3,1,2]) == [1,2,3]`. A property says: *for every
list*, sorting yields the same multiset, in non-decreasing order. Properties
are where the real bugs live, because humans write examples for the cases they
imagined and bugs live in the cases they didn't.

Classic properties worth knowing by heart:

- **Round-trip**: `decode(encode(x)) == x` (serialize/deserialize, escape/unescape).
- **Invariant preservation**: the result is sorted / balanced / within range.
- **Oracle**: compare against a slow, obviously-correct implementation.
- **Idempotence**: `f(f(x)) == f(x)` (normalizers, deduplication).
- **Metamorphic relations**: the same query in a different order returns the
  same set; adding an item grows the count by exactly one.

## How a property-based framework works

Hypothesis-style flow, in four verbs:

1. **Generate** — draw inputs from a strategy (ints, strings, lists of your
   own strategies, and strategies you compose).
2. **Shrink** — on failure, automatically reduce to the *minimal* failing input
   (the empty list, the one bad string). The shrunk example is the bug report.
3. **Replay** — failures are cached and re-run before new cases, so a fixed
   bug stays fixed.
4. **Derandomize** — a seed pinpoints a run; CI replays it exactly.

Property tests complement, not replace, the pyramid: they're a unit-level
technique with much deeper search.

## Contracts at the boundaries

Design-by-contract makes properties *executable*: preconditions (what must be
true on entry), postconditions (what the caller gets), invariants (what never
changes). In Python, `assert` documents and enforces cheaply (enable with
`-O` off in tests, on in hot production paths only if measured). The trick
that pays: **reuse the contract as the property** — the postcondition you wrote
once becomes the property-based test's oracle.

## Types are tests that run for free

Type hints eliminate an entire class of property failures (wrong shapes,
wrong None-ness) before any input is drawn. `mypy --strict` in CI plus
property tests for behavior is the modern default: types for structure,
properties for logic, examples for regressions.
""",
    "Property-based testing và hợp đồng",
    "Kiểm tra bất biến thay vì ví dụ: sinh hàng trăm đầu vào, thu nhỏ các thất bại, và để kiểu dữ liệu mang một phần bằng chứng.",
    """
## Test ví dụ ghim; property test khái quát hóa

Test ví dụ nói: `sort([3,1,2]) == [1,2,3]`. Một property nói: *với mọi list*,
sắp xếp trả cùng một multiset, theo thứ tự không giảm. Property là nơi bug
thật sự sống, vì con người viết ví dụ cho các trường hợp họ tưởng tượng được
và bug sống ở những trường hợp họ không.

Các property kinh điển đáng thuộc lòng:

- **Khứ hồi**: `decode(encode(x)) == x` (serialize/deserialize, escape/unescape).
- **Bảo toàn bất biến**: kết quả đã sắp / cân bằng / trong khoảng.
- **Oracle**: so với một bản cài chậm nhưng hiển nhiên đúng.
- **Idempotence**: `f(f(x)) == f(x)` (bộ chuẩn hóa, khử trùng lặp).
- **Quan hệ metamorphic**: cùng truy vấn theo thứ tự khác trả cùng tập; thêm
  một phần tử thì tổng tăng đúng một.

## Framework property-based hoạt động thế nào

Dòng chảy kiểu Hypothesis, bốn động từ:

1. **Sinh** — rút đầu vào từ một strategy (int, chuỗi, list của chính strategy
   của bạn, và các strategy bạn kết hợp).
2. **Thu nhỏ** — khi thất bại, tự động giảm về đầu vào thất bại *tối tiểu*
   (list rỗng, chuỗi xấu duy nhất). Ví dụ đã thu nhỏ chính là báo cáo bug.
3. **Phát lại** — các thất bại được cache và chạy lại trước các ca mới, để
   bug đã sửa không tái xuất.
4. **Khử ngẫu nhiên** — một seed xác định một lượt chạy; CI phát lại chính xác.

Property test bổ sung chứ không thay thế kim tự tháp: đây là kỹ thuật cấp unit
với tầm tìm kiếm sâu hơn nhiều.

## Hợp đồng tại các ranh giới

Design-by-contract biến property thành thứ *thực thi được*: tiền điều kiện (điều
gì phải đúng khi vào), hậu điều kiện (caller nhận được gì), bất biến (điều gì
không bao giờ đổi). Trong Python, `assert` tài liệu hóa và thực thi rẻ (bật
trong test, chỉ bật trong đường nóng của production nếu đã đo). Mánh đáng tiền:
**tái sử dụng hợp đồng làm property** — hậu điều kiện bạn viết một lần trở
thành oracle của bài property test.

## Kiểu dữ liệu là bài test chạy miễn phí

Type hint loại bỏ cả một lớp thất bại property (sai hình dạng, sai tính
None-ness) trước khi bất kỳ đầu vào nào được rút ra. `mypy --strict` trong CI
cộng property test cho hành vi là mặc định hiện đại: kiểu cho cấu trúc,
property cho logic, ví dụ cho hồi quy.
""",
)

# ── lesson 3 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "testing-in-production-truths",
    "Concurrency, Performance, and the Honest Test Suite",
    "Testing async code, timing-sensitive behavior, and what the suite can never tell you.",
    28,
    """
## Testing async code

The rule: drive the event loop yourself. `asyncio.run(coro())` in a test is
fine; what's *not* fine is `time.sleep` — it freezes the loop and tests
nothing. Use `await asyncio.sleep(0)` to yield control deterministically, fake
clocks for timeouts, and assert on *task states* (`task.done()`,
`task.cancelled()`) rather than wall-clock guesses.

## Timing-sensitive tests

Never assert `elapsed < X` on a loaded machine — CI machines lie. The stable
alternatives:

- **Injected clocks** (every module in this course): pass `now` in, advance it
  by hand.
- **Call counting**: assert "at most N attempts" instead of "finished within Y
  ms".
- **Deterministic schedulers**: for queue/worker logic, step the scheduler
  explicitly (the `deliver()` sweep from the distributed module).

## Test doubles for I/O

A network dependency in a unit test is a flaky test with extra steps. Fake the
*port* (the interface you already defined in the architecture module): an
in-memory queue, a canned clock, a fake repository. Keep one thin integration
suite that exercises the real adapters, and let it be the only place network
flakiness can live.

## What the suite cannot tell you

- That your performance holds under *production* data volumes — load test
  separately.
- That your security holds against a motivated adversary — audit separately.
- That users want the feature — that's not a test suite's job.

Honest scope: the suite verifies behavior you specified, deterministically.
Everything else needs a different tool.

## The maintenance contract

Tests are code: naming, duplication, dead tests deleted, helpers factored. A
test suite is a *system under active maintenance* — budget for it, review it,
refactor it. The pyramid's shape is a policy: when the integration tier grows
fat, push logic down into unit-testable cores; when unit tests multiply on a
thin layer, the design is telling you the logic belongs elsewhere.
""",
    "Concurrency, hiệu năng, và bộ test trung thực",
    "Test code async, hành vi nhạy thời gian, và những điều bộ test không bao giờ nói được.",
    """
## Test code async

Quy tắc: tự lái event loop. `asyncio.run(coro())` trong test là ổn; điều *không*
ổn là `time.sleep` — nó đóng băng loop và không test được gì. Dùng
`await asyncio.sleep(0)` để nhường quyền điều khiển một cách xác định, fake
clock cho các timeout, và khẳng định trên *trạng thái task* (`task.done()`,
`task.cancelled()`) thay vì phỏng đoán theo đồng hồ.

## Test nhạy thời gian

Không bao giờ khẳng định `elapsed < X` trên máy đang tải — máy CI hay nói dối.
Những lựa chọn ổn định:

- **Đồng hồ được tiêm** (mọi module trong khóa học này): truyền `now` vào,
  tự tay đẩy nó lên.
- **Đếm số lần gọi**: khẳng định "tối đa N lần thử" thay vì "xong trong Y ms".
- **Bộ lập lịch xác định**: với logic queue/worker, điều khiển bộ lập lịch
  tường minh (lượt quét `deliver()` từ module distributed).

## Test double cho I/O

Một dependency mạng trong unit test là một bài test flaky với các bước thừa.
Fake *port* (giao diện bạn đã định nghĩa ở module kiến trúc): một queue trong
bộ nhớ, một đồng hồ đóng gói, một fake repository. Giữ một suite integration
mỏng chạy các adapter thật, và để nó là nơi duy nhất mạng được phép rung.

## Điều bộ test không nói được

- Hiệu năng có giữ vững với khối lượng dữ liệu *production* không — load test
  riêng.
- Bảo mật có giữ vững trước một đối thủ có động cơ không — audit riêng.
- Người dùng có muốn tính năng không — đó không phải việc của bộ test.

Phạm vi trung thực: bộ test xác minh hành vi bạn đã đặc tả, một cách xác định.
Mọi thứ khác cần công cụ khác.

## Hợp đồng bảo trì

Test cũng là code: đặt tên, chống trùng lặp, xóa test chết, tách helper. Một
test suite là *một hệ thống được bảo trì tích cực* — dành ngân sách cho nó,
review nó, refactor nó. Hình dáng kim tự tháp là một chính sách: khi tầng
integration phình to, đẩy logic xuống phần lõi unit-test được; khi unit test
nhân lên trên một tầng mỏng, thiết kế đang nói với bạn rằng logic thuộc về
nơi khác.
""",
)

# ── practice 1: fakes & seams ────────────────────────────────────────────────
FAKECLOCK_REF = (
    "class FakeClock:\n"
    "    '''Deterministic clock. starts at `start`; advance() moves it forward.'''\n"
    "\n"
    "    def __init__(self, start=0.0):\n"
    "        self.now_value = float(start)\n"
    "\n"
    "    def now(self):\n"
    "        return self.now_value\n"
    "\n"
    "    def advance(self, seconds):\n"
    "        assert seconds >= 0\n"
    "        self.now_value += seconds\n"
    "\n"
    "\n"
    "class RateLimiter:\n"
    "    '''Allows `rate` events per window; driven by an injected clock.'''\n"
    "\n"
    "    def __init__(self, rate, window, clock):\n"
    "        self.rate = rate\n"
    "        self.window = window\n"
    "        self.clock = clock\n"
    "        self._events = []\n"
    "\n"
    "    def allow(self):\n"
    "        now = self.clock.now()\n"
    "        self._events = [t for t in self._events if now - t < self.window]\n"
    "        if len(self._events) < self.rate:\n"
    "            self._events.append(now)\n"
    "            return True\n"
    "        return False\n"
)
FAKECLOCK_WRONG = (
    "import time as _time\n"
    "\n"
    "\n"
    "class FakeClock:\n"
    "    def __init__(self, start=0.0):\n"
    "        self.now_value = float(start)\n"
    "\n"
    "    def now(self):\n"
    "        return self.now_value\n"
    "\n"
    "    def advance(self, seconds):\n"
    "        assert seconds >= 0\n"
    "        self.now_value += seconds\n"
    "\n"
    "\n"
    "class RateLimiter:\n"
    "    def __init__(self, rate, window, clock):\n"
    "        self.rate = rate\n"
    "        self.window = window\n"
    "        self.clock = clock\n"
    "        self._events = []\n"
    "\n"
    "    def allow(self):\n"
    "        # WRONG: reads the real clock — injected clock ignored, tests flaky\n"
    "        now = _time.time()\n"
    "        self._events = [t for t in self._events if now - t < self.window]\n"
    "        if len(self._events) < self.rate:\n"
    "            self._events.append(now)\n"
    "            return True\n"
    "        return False\n"
)

MOCKSPY_REF = (
    "class MailerSpy:\n"
    "    '''Interaction-test double for a mailer port: records, never sends.'''\n"
    "\n"
    "    def __init__(self):\n"
    "        self.sent = []\n"
    "        self.fail_next = False\n"
    "\n"
    "    def send(self, to, subject, body):\n"
    "        if self.fail_next:\n"
    "            self.fail_next = False\n"
    "            raise ConnectionError('smtp down')\n"
    "        self.sent.append({'to': to, 'subject': subject, 'body': body})\n"
    "        return True\n"
    "\n"
    "\n"
    "def send_welcome(mailer, user):\n"
    "    '''Domain logic under test: exactly one welcome email on success,\n"
    "    none on failure.'''\n"
    "    try:\n"
    "        mailer.send(user['email'], 'Welcome!', f\"Hi {user['name']}\")\n"
    "        return True\n"
    "    except ConnectionError:\n"
    "        return False\n"
)
MOCKSPY_WRONG = (
    "class MailerSpy:\n"
    "    def __init__(self):\n"
    "        self.sent = []\n"
    "        self.fail_next = False\n"
    "\n"
    "    def send(self, to, subject, body):\n"
    "        if self.fail_next:\n"
    "            self.fail_next = False\n"
    "            raise ConnectionError('smtp down')\n"
    "        self.sent.append({'to': to, 'subject': subject, 'body': body})\n"
    "        return True\n"
    "\n"
    "\n"
    "def send_welcome(mailer, user):\n"
    "    # WRONG: swallows the failure AND retries the send inside the same call\n"
    "    while True:\n"
    "        try:\n"
    "            mailer.send(user['email'], 'Welcome!', f\"Hi {user['name']}\")\n"
    "            return True\n"
    "        except ConnectionError:\n"
    "            continue\n"
)

write_practice(
    MOD, "pa-p13-fakes-practice",
    "Deterministic Doubles",
    "An injected clock makes time testable; a spy port makes interaction contracts testable.",
    "Test double xác định",
    "Một đồng hồ được tiêm khiến thời gian test được; một spy port khiến hợp đồng tương tác test được.",
    "test-strategy", 24, "advanced",
    [
        challenge(
            "pa-test-fake-clock",
            "Move time by hand",
            "Implement `FakeClock(start=0.0)` and a `RateLimiter(rate, window, clock)` that uses it:\n\n- FakeClock: `now()` returns the current value; `advance(seconds)` moves it forward (negative advance asserts)\n- RateLimiter: `allow()` permits at most `rate` events in any window of `window` seconds, using ONLY the injected clock (never `time.*`); events older than the window stop counting\n\nDeterminism under test: the suite must be able to replay any scenario exactly.",
            "class FakeClock:\n    def __init__(self, start=0.0):\n        ...\n\n    def now(self):\n        ...\n\n    def advance(self, seconds):\n        ...\n\n\nclass RateLimiter:\n    def __init__(self, rate, window, clock):\n        ...\n\n    def allow(self):\n        ...",
            [
                ("the window slides with the injected clock",
                 "clock = FakeClock()\nrl = RateLimiter(rate=2, window=10, clock=clock)\nassert rl.allow() and rl.allow()\nassert not rl.allow()\nclock.advance(10)      # exactly at the boundary: window is exclusive\nassert rl.allow()\nassert not rl.allow()\nclock.advance(9.9)\nassert rl.allow()      # the first event (t=0) is now outside the 10s window\nprint('ok')",
                 "Events strictly older than the window expire; boundary is exclusive."),
            ],
            level="guided",
        ),
        challenge(
            "pa-test-mailer-spy",
            "The interaction contract",
            "Implement `MailerSpy` and `send_welcome(mailer, user)`:\n\n- MailerSpy: `send(to, subject, body)` records the call and returns True; if `fail_next` is set, it raises `ConnectionError` once (and clears the flag) instead\n- `send_welcome`: sends `('Welcome!', 'Hi <name>')` to `user['email']`; returns True on success, False when the mailer raised `ConnectionError` — and on failure it must NOT retry inside the call\n\nThe spy makes the contract observable: exactly one send on success, exactly zero on failure.",
            "class MailerSpy:\n    def __init__(self):\n        ...\n\n    def send(self, to, subject, body):\n        ...\n\n\ndef send_welcome(mailer, user):\n    ...",
            [
                ("one send on success, zero on failure",
                 "spy = MailerSpy()\nassert send_welcome(spy, {'email': 'a@x.y', 'name': 'Lan'}) is True\nassert spy.sent == [{'to': 'a@x.y', 'subject': 'Welcome!', 'body': 'Hi Lan'}]\nspy.fail_next = True\nassert send_welcome(spy, {'email': 'b@x.y', 'name': 'Minh'}) is False\nassert len(spy.sent) == 1  # the failed attempt recorded nothing, and did not loop\nprint('ok')",
                 "Failure surfaces as a return value, not an infinite retry."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-test-fake-clock": vi_challenge(
            "Tự tay đẩy thời gian",
            "Cài `FakeClock(start=0.0)` và một `RateLimiter(rate, window, clock)` sử dụng nó:\n\n- FakeClock: `now()` trả giá trị hiện tại; `advance(seconds)` đẩy nó tới trước (advance âm thì assert)\n- RateLimiter: `allow()` cho phép tối đa `rate` sự kiện trong bất kỳ cửa sổ `window` giây nào, CHỈ dùng đồng hồ được tiêm (không bao giờ `time.*`); các sự kiện cũ hơn cửa sổ ngừng được tính\n\nTính xác định dưới phép kiểm: bộ test phải phát lại được mọi kịch bản một cách chính xác.",
            [("Cửa sổ trượt theo đồng hồ được tiêm", "Sự kiện cũ hơn cửa sổ hết hạn; biên là loại trừ."),
             ("Phát lại bất kỳ kịch bản nào một cách chính xác", "Suite phải tái tạo được từng kịch bản.")],
        ),
        "pa-test-mailer-spy": vi_challenge(
            "Hợp đồng tương tác",
            "Cài `MailerSpy` và `send_welcome(mailer, user)`:\n\n- MailerSpy: `send(to, subject, body)` ghi lại lời gọi và trả True; nếu `fail_next` được bật, nó raise `ConnectionError` đúng một lần (và tắt cờ) thay vì thế\n- `send_welcome`: gửi `('Welcome!', 'Hi <name>')` tới `user['email']`; trả True khi thành công, False khi mailer raise `ConnectionError` — và khi thất bại KHÔNG được retry ngay trong lần gọi đó\n\nSpy khiến hợp đồng quan sát được: đúng một lần gửi khi thành công, đúng không lần khi thất bại.",
            [("Một lần gửi khi thành công, không lần khi thất bại", "Thất bại hiện lên như một giá trị trả về, không phải vòng lặp vô hạn.")],
        ),
    },
    solutions=[("pa-test-fake-clock", FAKECLOCK_REF, FAKECLOCK_WRONG),
               ("pa-test-mailer-spy", MOCKSPY_REF, MOCKSPY_WRONG)],
)

# ── practice 2: property testing ─────────────────────────────────────────────
PROP_REF = (
    "def check_roundtrip_codec(encode, decode, samples):\n"
    "    '''Mini property engine: for each sample, decode(encode(x)) must equal x.\n"
    "    Returns (passed, first_failure) where first_failure is the failing sample\n"
    "    (shrunk to its minimal core: for lists, the first bad element) or None.'''\n"
    "    for x in samples:\n"
    "        try:\n"
    "            if decode(encode(x)) != x:\n"
    "                return False, x\n"
    "        except Exception:\n"
    "            return False, x\n"
    "    return True, None\n"
    "\n"
    "\n"
    "def shrink(samples, bad):\n"
    "    '''List shrinking: try removing elements while the property still fails;\n"
    "    return the minimal failing prefix-content list.'''\n"
    "    current = list(bad)\n"
    "    changed = True\n"
    "    while changed and len(current) > 1:\n"
    "        changed = False\n"
    "        for i in range(len(current)):\n"
    "            candidate = current[:i] + current[i + 1:]\n"
    "            ok, _ = check_roundtrip_codec(lambda v: v, lambda v: v, [candidate])\n"
    "            if ok is False:\n"
    "                current = candidate\n"
    "                changed = True\n"
    "                break\n"
    "    return current\n"
)
PROP_WRONG = (
    "def check_roundtrip_codec(encode, decode, samples):\n"
    "    # WRONG: compares encode(decode(x)) — the wrong direction of the round-trip\n"
    "    for x in samples:\n"
    "        try:\n"
    "            if encode(decode(x)) != x:\n"
    "                return False, x\n"
    "        except Exception:\n"
    "            return False, x\n"
    "    return True, None\n"
    "\n"
    "\n"
    "def shrink(samples, bad):\n"
    "    return list(bad)  # WRONG: no shrinking at all\n"
)

FLAKY_REF = (
    "def diagnose_flaky(test_record):\n"
    "    '''test_record: {'name', 'uses_time': bool, 'uses_random_unseeded': bool,\n"
    "    'shared_state': bool, 'order_dependent': bool}\n"
    "    Returns (verdict, causes): verdict 'flaky' if any cause, else 'sound';\n"
    "    causes is a list of human-readable strings in fixed order:\n"
    "    time, randomness, shared state, order dependence.'''\n"
    "    causes = []\n"
    "    if test_record['uses_time']:\n"
    "        causes.append('reads the wall clock: inject a clock')\n"
    "    if test_record['uses_random_unseeded']:\n"
    "        causes.append('unseeded randomness: seed it')\n"
    "    if test_record['shared_state']:\n"
    "        causes.append('shared state: give each test its own world')\n"
    "    if test_record['order_dependent']:\n"
    "        causes.append('order-dependent: construct prerequisites in the test')\n"
    "    return ('flaky' if causes else 'sound', causes)\n"
)
FLAKY_WRONG = (
    "def diagnose_flaky(test_record):\n"
    "    # WRONG: order dependence ignored — the classic hidden flake\n"
    "    causes = []\n"
    "    if test_record['uses_time']:\n"
    "        causes.append('reads the wall clock: inject a clock')\n"
    "    if test_record['uses_random_unseeded']:\n"
    "        causes.append('unseeded randomness: seed it')\n"
    "    if test_record['shared_state']:\n"
    "        causes.append('shared state: give each test its own world')\n"
    "    return ('flaky' if causes else 'sound', causes)\n"
)

write_practice(
    MOD, "pa-p13-property-practice",
    "Property & Diagnosis Drills",
    "Build the property engine's core — check and shrink — and mechanize flaky-test triage.",
    "Bài tập property và chẩn đoán",
    "Xây lõi của engine property — kiểm tra và thu nhỏ — và cơ khí hóa việc phân loại test flaky.",
    "property-and-contracts", 26, "advanced",
    [
        challenge(
            "pa-test-property-engine",
            "Check and shrink",
            "Implement two functions of a mini property engine:\n\n- `check_roundtrip_codec(encode, decode, samples)` — for each sample, `decode(encode(x))` must equal `x` (any exception counts as failure). Returns `(passed, first_failure)` — the failing sample or `None`.\n- `shrink(samples, bad)` — minimize a failing list: repeatedly try removing one element and keep the removal when the property (identity round-trip via `check_roundtrip_codec`) still fails; stop when no single removal keeps it failing or one element remains. Returns the minimal list.\n\nShrinking is what turns 'fails on this 50-element monster' into 'fails on `[\"\\x00\"]`' — the bug report the author can act on.",
            "# TODO: check_roundtrip_codec + shrink",
            [
                ("clean codec passes, broken codec fails",
                 "ok, fail = check_roundtrip_codec(lambda x: x.upper(), lambda x: x.lower(), ['ab', 'Cd'])\nassert ok is False and fail == 'ab'   # lower(upper('ab')) == 'AB' != 'ab'\nok, fail = check_roundtrip_codec(lambda x: x, lambda x: x, ['ab', 'Cd'])\nassert ok is True and fail is None\nprint('ok')",
                 "The property catches what an example test never imagined."),
                ("shrinking finds the minimal failing list",
                 "def bad_encode(items):\n    return [x for x in items if x != 7]  # drops 7s: round-trip fails on any list containing one\nbad = [1, 2, 7, 3]\nminimal = shrink(bad, bad)\nassert minimal == [7] or (7 in minimal and len(minimal) == 1), minimal\nprint('ok')",
                 "Remove elements while the property still fails; one 7 remains."),
            ],
            level="combination",
        ),
        challenge(
            "pa-test-flaky-triage",
            "Diagnose the flaky test",
            "Implement `diagnose_flaky(test_record)` — the record has booleans `uses_time`, `uses_random_unseeded`, `shared_state`, `order_dependent`:\n\n- returns `(verdict, causes)`: `'flaky'` when any cause fires, else `'sound'`\n- causes are human-readable fixes in fixed order: time → `'reads the wall clock: inject a clock'`; randomness → `'unseeded randomness: seed it'`; shared state → `'shared state: give each test its own world'`; order dependence → `'order-dependent: construct prerequisites in the test'`\n\nMechanized triage: the reviewer's first five minutes, as a function.",
            "# TODO: diagnose_flaky",
            [
                ("every cause reported, in order",
                 "rec = {'uses_time': True, 'uses_random_unseeded': True, 'shared_state': True, 'order_dependent': True}\nverdict, causes = diagnose_flaky(rec)\nassert verdict == 'flaky' and len(causes) == 4\nassert causes[0].startswith('reads the wall clock')\nassert causes[-1].startswith('order-dependent')\nprint('ok')",
                 "All four suspects checked, in the fixed order."),
            ],
            level="debugging",
        ),
    ],
    {
        "pa-test-property-engine": vi_challenge(
            "Kiểm tra và thu nhỏ",
            "Cài hai hàm của một engine property mini:\n\n- `check_roundtrip_codec(encode, decode, samples)` — với mỗi sample, `decode(encode(x))` phải bằng `x` (mọi exception tính là thất bại). Trả `(passed, first_failure)` — sample failing hoặc `None`.\n- `shrink(samples, bad)` — tối tiểu một list failing: liên tục thử bỏ một phần tử và giữ việc bỏ đó khi property (khứ hồi danh tính qua `check_roundtrip_codec`) vẫn fail; dừng khi không còn lần bỏ nào khiến nó fail hoặc chỉ còn một phần tử. Trả list tối tiểu.\n\nThu nhỏ là thứ biến 'fail với con quái vật 50 phần tử này' thành 'fail với `[\"\\x00\"]`' — báo cáo bug mà tác giả hành động được.",
            [("Codec sạch pass, codec hỏng fail", "Property bắt được thứ mà test ví dụ không bao giờ tưởng tượng tới."),
             ("Thu nhỏ tìm list failing tối tiểu", "Bỏ phần tử trong khi property vẫn fail; còn lại một 7.")],
        ),
        "pa-test-flaky-triage": vi_challenge(
            "Chẩn đoán test flaky",
            "Cài `diagnose_flaky(test_record)` — bản ghi có các boolean `uses_time`, `uses_random_unseeded`, `shared_state`, `order_dependent`:\n\n- trả `(verdict, causes)`: `'flaky'` khi có bất kỳ nguyên nhân nào, ngược lại `'sound'`\n- causes là các cách sửa đọc được theo thứ tự cố định: thời gian → `'reads the wall clock: inject a clock'`; ngẫu nhiên → `'unseeded randomness: seed it'`; trạng thái chia sẻ → `'shared state: give each test its own world'`; phụ thuộc thứ tự → `'order-dependent: construct prerequisites in the test'`\n\nPhân loại cơ khí hóa: năm phút đầu của reviewer, dưới dạng một hàm.",
            [("Mọi nguyên nhân được báo, đúng thứ tự", "Cả bốn nghi phạm được kiểm, theo thứ tự cố định.")],
        ),
    },
    solutions=[("pa-test-property-engine", PROP_REF, PROP_WRONG),
               ("pa-test-flaky-triage", FLAKY_REF, FLAKY_WRONG)],
)

# ── practice 3: testing project ──────────────────────────────────────────────
RUNNER_REF = (
    "def run_suite(tests, order=None):\n"
    "    '''tests: list of {'name', 'fn'}; fn() returns 'pass' or raises AssertionError.\n"
    "    order: optional explicit order of names to run (deterministic replay).\n"
    "    Returns {'passed': [names], 'failed': [names], 'errors': [names], 'skipped': [names]}\n"
    "    in execution order. AssertionError -> failed; anything else -> errors;\n"
    "    a name in `order` that doesn't exist is an error entry '<name>: no such test'.'''\n"
    "    by_name = {t['name']: t for t in tests}\n"
    "    if order is None:\n"
    "        sequence = list(tests)\n"
    "    else:\n"
    "        sequence = [by_name[n] for n in order if n in by_name]\n"
    "    result = {'passed': [], 'failed': [], 'errors': [], 'skipped': []}\n"
    "    if order is not None:\n"
    "        known = set(order)\n"
    "        for t in tests:\n"
    "            if t['name'] not in known:\n"
    "                result['skipped'].append(t['name'])\n"
    "        for n in order:\n"
    "            if n not in by_name:\n"
    "                result['errors'].append(f'{n}: no such test')\n"
    "    for t in sequence:\n"
    "        try:\n"
    "            outcome = t['fn']()\n"
    "            result['passed'].append(t['name'])\n"
    "        except AssertionError:\n"
    "            result['failed'].append(t['name'])\n"
    "        except Exception:\n"
    "            result['errors'].append(t['name'])\n"
    "    return result\n"
)
RUNNER_WRONG = (
    "def run_suite(tests, order=None):\n"
    "    by_name = {t['name']: t for t in tests}\n"
    "    if order is None:\n"
    "        sequence = list(tests)\n"
    "    else:\n"
    "        # WRONG: unknown names silently vanish — typos in the order list hide tests\n"
    "        sequence = [by_name[n] for n in order if n in by_name]\n"
    "    result = {'passed': [], 'failed': [], 'errors': [], 'skipped': []}\n"
    "    for t in sequence:\n"
    "        try:\n"
    "            t['fn']()\n"
    "            result['passed'].append(t['name'])\n"
    "        except Exception:\n"
    "            # WRONG: assertions and real errors conflated\n"
    "            result['failed'].append(t['name'])\n"
    "    return result\n"
)

write_practice(
    MOD, "pa-p13-testing-project",
    "Test Runner Mini-Project",
    "Build a tiny deterministic runner: explicit order, honest triage of failures vs errors, and unknown names reported.",
    "Dự án mini test runner",
    "Xây một runner nhỏ xác định: thứ tự tường minh, phân loại trung thực giữa fail và error, và tên lạ được báo cáo.",
    "testing-in-production-truths", 28, "advanced",
    [
        challenge(
            "pa-test-runner",
            "A runner that tells the truth",
            "Implement `run_suite(tests, order=None)` — tests are `{'name', 'fn'}` dicts whose `fn()` either returns normally or raises:\n\n- execution follows `order` (a list of names) when given, else input order\n- returns `{'passed': [...], 'failed': [...], 'errors': [...], 'skipped': [...]}`\n- `AssertionError` → `failed`; any other exception → `errors` (a failing assertion is a test result; a NameError is a broken test)\n- names in `order` that match no test → entries `'<name>: no such test'` in `errors`; tests not mentioned in a given order → `skipped`\n\nThe discriminating scenario: a suite where one test raises `NameError` must report it as an error, not a failure — that distinction is the whole point.",
            "# TODO: run_suite",
            [
                ("assertions are failures, other exceptions are errors",
                 "def boom_assert():\n    raise AssertionError('x != y')\ndef boom_name():\n    return undefined_variable  # noqa: F821\nsuite = [{'name': 'a', 'fn': lambda: None}, {'name': 'f', 'fn': boom_assert}, {'name': 'e', 'fn': boom_name}]\nr = run_suite(suite)\nassert r['passed'] == ['a'] and r['failed'] == ['f'] and r['errors'] == ['e']\nprint('ok')",
                 "The triage that keeps CI diagnostics honest."),
                ("explicit order replays exactly",
                 "suite = [{'name': 'x', 'fn': lambda: None}, {'name': 'y', 'fn': lambda: None}]\nr = run_suite(suite, order=['y', 'x'])\nassert r['passed'] == ['y', 'x']\nr2 = run_suite(suite, order=['y', 'zz'])\nassert r2['errors'] == ['zz: no such test'] and r2['skipped'] == ['x']\nprint('ok')",
                 "Deterministic replay; unknown names are loud, not silent."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-test-runner": vi_challenge(
            "Runner nói thật",
            "Cài `run_suite(tests, order=None)` — tests là các dict `{'name', 'fn'}` với `fn()` hoặc trả về bình thường hoặc raise:\n\n- thực thi theo `order` (list tên) khi có, ngược lại theo thứ tự input\n- trả `{'passed': [...], 'failed': [...], 'errors': [...], 'skipped': [...]}`\n- `AssertionError` → `failed`; exception khác → `errors` (assertion hỏng là một kết quả test; NameError là một test bị hỏng)\n- tên trong `order` không khớp test nào → các entry `'<name>: no such test'` trong `errors`; test không được nhắc trong order đã cho → `skipped`\n\nKịch bản phân biệt: một suite có test raise `NameError` phải được báo là error, không phải failure — sự phân biệt đó là toàn bộ ý nghĩa.",
            [("Assertion là failure, exception khác là error", "Phân loại giúp chẩn đoán CI trung thực."),
             ("Thứ tự tường minh phát lại chính xác", "Phát lại xác định; tên lạ ầm ĩ chứ không im lặng.")],
        ),
    },
    solutions=[("pa-test-runner", RUNNER_REF, RUNNER_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
write_checkpoint(
    MOD, "pa-checkpoint-testing",
    "Checkpoint: Advanced Testing",
    "Prove you can make an untrustworthy suite trustworthy: isolate the flaky causes, then pin the behavior deterministically.",
    25,
    """
**The exam question:** CI is red, but rerunning the suite turns it green. What
do you do first — rerun again, or hunt the nondeterminism?

The checkpoint: a test-record audit plus a deterministic re-implementation.
First classify which tests are untrustworthy and why (the flaky causes), then
rewrite the risky ones around injected time, seeded randomness, and isolated
state — the exact moves from this module.
""",
    "Checkpoint: Kiểm thử nâng cao",
    "Chứng minh bạn biến được một bộ test không đáng tin thành đáng tin: cô lập nguyên nhân flaky, rồi ghim hành vi một cách xác định.",
    """
**Câu hỏi thi:** CI đỏ, nhưng chạy lại suite thì lại xanh. Bạn làm gì trước
tiên — chạy lại lần nữa, hay săn tính không xác định?

Checkpoint: một cuộc audit bản ghi test cộng một bản cài lại xác định. Trước
tiên phân loại test nào không đáng tin và vì sao (các nguyên nhân flaky), sau
đó viết lại những cái rủi ro quanh thời gian được tiêm, tính ngẫu nhiên có
seed, và trạng thái cô lập — đúng những nước đi của module này.
""",
    challenge(
        "pa-test-suite-audit",
        "Make the suite trustworthy",
        "Implement `audit_suite(records)` and `plan_fix(record)`:\n\n- `audit_suite(records)` returns `{'sound': [names], 'flaky': [names]}` — flaky when any of the four boolean causes is set (`uses_time`, `uses_random_unseeded`, `shared_state`, `order_dependent`); both lists keep input order\n- `plan_fix(record)` returns the ordered list of concrete fixes for a flaky record — the exact four strings from the diagnose drill — or `[]` for a sound one\n- the plan's fixes map 1:1 in order: time → inject a clock; randomness → seed it; shared state → isolate the world; order dependence → construct prerequisites\n\nThe invariant: after applying every fix in the plan, re-running `diagnose_flaky` on the record yields `'sound'`.",
        "# TODO: audit_suite + plan_fix",
        [
            ("classify, plan, and the plan actually cures",
             "recs = [\n    {'name': 't1', 'uses_time': False, 'uses_random_unseeded': False, 'shared_state': False, 'order_dependent': False},\n    {'name': 't2', 'uses_time': True, 'uses_random_unseeded': False, 'shared_state': False, 'order_dependent': True},\n]\na = audit_suite(recs)\nassert a['sound'] == ['t1'] and a['flaky'] == ['t2']\nplan = plan_fix(recs[1])\nassert len(plan) == 2 and 'inject a clock' in plan[0] and 'prerequisites' in plan[1]\nprint('ok')",
             "Sound tests are named; flaky ones get an ordered, actionable plan."),
        ],
        level="build",
    ),
    vi_challenge(
        "Biến bộ test đáng tin",
        "Cài `audit_suite(records)` và `plan_fix(record)`:\n\n- `audit_suite(records)` trả `{'sound': [tên], 'flaky': [tên]}` — flaky khi có bất kỳ nguyên nhân boolean nào (`uses_time`, `uses_random_unseeded`, `shared_state`, `order_dependent`); cả hai list giữ thứ tự input\n- `plan_fix(record)` trả list các cách sửa cụ thể theo thứ tự cho bản ghi flaky — đúng bốn chuỗi từ bài chẩn đoán — hoặc `[]` cho bản ghi sound\n- các cách sửa trong plan ánh xạ 1:1 theo thứ tự: thời gian → tiêm đồng hồ; ngẫu nhiên → seed; trạng thái chia sẻ → cô lập thế giới; phụ thuộc thứ tự → tự dựng điều kiện tiên quyết\n\nBất biến: sau khi áp mọi fix trong plan, chạy lại `diagnose_flaky` trên bản ghi cho `'sound'`.",
        [("Phân loại, lập kế hoạch, và kế hoạch thực sự chữa được", "Test sound được nêu tên; test flaky nhận một kế hoạch có thứ tự, hành động được.")],
    ),
    solution=(
        "def audit_suite(records):\n"
        "    sound, flaky = [], []\n"
        "    for r in records:\n"
        "        causes = any([r['uses_time'], r['uses_random_unseeded'], r['shared_state'], r['order_dependent']])\n"
        "        (flaky if causes else sound).append(r['name'])\n"
        "    return {'sound': sound, 'flaky': flaky}\n"
        "\n"
        "\n"
        "def plan_fix(record):\n"
        "    plan = []\n"
        "    if record['uses_time']:\n"
        "        plan.append('reads the wall clock: inject a clock')\n"
        "    if record['uses_random_unseeded']:\n"
        "        plan.append('unseeded randomness: seed it')\n"
        "    if record['shared_state']:\n"
        "        plan.append('shared state: give each test its own world')\n"
        "    if record['order_dependent']:\n"
        "        plan.append('order-dependent: construct prerequisites in the test')\n"
        "    return plan\n"
    ),
    wrong=(
        "def audit_suite(records):\n"
        "    # WRONG: order-dependent tests classified as sound — the hidden flake ships\n"
        "    sound, flaky = [], []\n"
        "    for r in records:\n"
        "        causes = any([r['uses_time'], r['uses_random_unseeded'], r['shared_state']])\n"
        "        (flaky if causes else sound).append(r['name'])\n"
        "    return {'sound': sound, 'flaky': flaky}\n"
        "\n"
        "\n"
        "def plan_fix(record):\n"
        "    return []  # WRONG: no plan, no cure\n"
    ),
)

print("module 13 complete")
