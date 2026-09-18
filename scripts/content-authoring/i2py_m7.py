#!/usr/bin/env python3
"""Module 7: testing-debugging — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint

MOD = "testing-debugging"

write_module(
    MOD,
    "Testing & Debugging",
    "Professional verification: a testing pyramid you can actually build, test doubles that isolate behavior, and a debugging method that beats guesswork.",
    "Kiểm thử & Gỡ lỗi",
    "Xác minh ở mức chuyên nghiệp: kim tự tháp kiểm thử xây được thật, test double cô lập hành vi, và phương pháp gỡ lỗi thắng trò đoán mò.",
    ["why-testing", "unit-testing-foundations", "test-doubles", "debugging-method", "devtools-observability", "repair-checkpoint"],
    ["assertions-practice", "design-tests-practice", "doubles-practice", "diagnose-practice", "regression-practice"],
)

write_lesson(
    MOD, "why-testing",
    "Why Tests Exist (and What They're For)",
    "Tests are executable specifications: they pin behavior so change is safe. Different test sizes answer different questions.",
    16,
    """A test is code that runs your code and complains when reality differs from expectation. That's the whole idea — the discipline is in *what* you complain about.

## What tests buy you

- **Confidence to change.** Untested code ossifies: nobody dares touch it. Tested code can be refactored fearlessly — the tests tell you if behavior changed.
- **Executable documentation.** "How does this function handle an empty cart?" — read its tests.
- **Debugging acceleration.** When something breaks, a failing test pinpoints *where* before you open a browser.

## The pyramid

```text
        /  E2E  \\        few — whole system, slow, brittle
       / Integr. \\       some — modules together, real-ish
      /   Unit    \\      many — one function, fast, precise
```

- **Unit tests** answer: *is this function correct for these inputs?* Milliseconds. Hundreds of them.
- **Integration tests** answer: *do these modules cooperate correctly?* (your function + real localStorage, your route + real DB).
- **E2E tests** answer: *can a user actually do the thing?* Seconds each; reserve them for critical paths.

## What makes a good unit test

- **One behavior per test.** The name says what behavior: `rejects negative quantities` — not `testCart4`.
- **Arrange–Act–Assert.** Set up inputs, do the one thing, check the one outcome.
- **Independent.** No test depends on another having run, or on execution order.
- **Fast.** If your suite takes minutes, you'll stop running it, and then it protects nothing.

## When tests lie

Tests can be wrong in two directions: passing while the code is broken (weak assertions — asserting only "doesn't throw"), or failing while the code is right (over-specified tests asserting implementation details). Both destroy trust. Assert *observable behavior*.

## Coverage is a smoke detector, not a goal

100% coverage proves lines executed, not that behavior is correct. Chasing the number produces useless tests. Use coverage to find *untested areas*, then decide what deserves real tests.""",
    "Vì sao test tồn tại (và test để làm gì)",
    "Test là đặc tả chạy được: ghim hành vi để việc thay đổi trở nên an toàn. Mỗi cấp độ test trả lời một câu hỏi khác nhau.",
    """Test là code chạy code của bạn và phàn nàn khi hiện thực khác kỳ vọng. Vậy thôi — cái khó là *phàn nàn về điều gì*.

## Test mua cho bạn điều gì

- **Tự tin để thay đổi.** Code không có test bị hóa đá: không ai dám đụng vào. Code có test có thể refactor vô tư — test sẽ báo nếu hành vi đổi.
- **Tài liệu chạy được.** "Hàm này xử lý giỏ hàng rỗng thế nào?" — đọc test của nó.
- **Gỡ lỗi nhanh hơn.** Khi có gì đó hỏng, test failing chỉ đúng *ở đâu* trước khi bạn mở trình duyệt.

## Kim tự tháp

```text
        /  E2E  \\        ít — cả hệ thống, chậm, dễ gãy
       / Integr. \\       vừa — nhiều module cùng chạy
      /   Unit    \\      nhiều — một hàm, nhanh, chính xác
```

- **Unit test** trả lời: *hàm này đúng với những input này không?* Mili giây. Hàng trăm cái.
- **Integration test** trả lời: *các module có phối hợp đúng không?* (hàm của bạn + localStorage thật, route của bạn + DB thật).
- **E2E test** trả lời: *người dùng có làm được việc thật không?* Mỗi cái tốn vài giây; chỉ dành cho luồng quan trọng.

## Một unit test tốt trông thế nào

- **Một hành vi mỗi test.** Tên nói rõ hành vi: `rejects negative quantities` — không phải `testCart4`.
- **Arrange–Act–Assert.** Dựng input, làm đúng một việc, kiểm tra đúng một kết quả.
- **Độc lập.** Không test nào phụ thuộc test khác đã chạy, hay vào thứ tự chạy.
- **Nhanh.** Nếu bộ test mất vài phút, bạn sẽ ngừng chạy nó, và nó không còn bảo vệ gì nữa.

## Khi test nói dối

Test có thể sai theo hai hướng: pass trong khi code hỏng (assertion yếu — chỉ assert "không ném lỗi"), hoặc fail trong khi code đúng (test quá gắt, assert chi tiết hiện thực). Cả hai phá hủy niềm tin. Hãy assert *hành vi quan sát được*.

## Coverage là chuột báo khói, không phải mục tiêu

100% coverage chứng minh các dòng đã chạy, không chứng minh hành vi đúng. Đuổi theo con số sinh ra test vô dụng. Hãy dùng coverage để tìm *vùng chưa được test*, rồi quyết định vùng nào xứng đáng có test thật.""",
)

write_lesson(
    MOD, "unit-testing-foundations",
    "Assertions and Test Structure",
    "The mechanics beneath every test framework: comparisons that fail loudly, before/after hooks, and organizing suites that scale.",
    18,
    """Every test framework — Jest, Vitest, Mocha — is sugar over the same core: run code, compare, report. Build the core once and you'll understand all of them.

## Assertions: fail loudly, precisely

```js
function assertEqual(actual, expected, msg) {
  if (!Object.is(actual, expected)) {
    throw new Error(`${msg ?? "assert failed"}: expected ${fmt(expected)}, got ${fmt(actual)}`);
  }
}
```

Design rules learned the hard way:

- The **message names the expectation**, not the mechanism. "Cart total excludes negative quantities" beats "0 !== -5".
- **Deep equality** for objects: `Object.is` compares references; you need a structural compare (or `JSON.stringify` as a crude shortcut — order-sensitive, undefined-hostile).
- **`assertThrows(fn, ErrorType)`** must verify the *type* (and ideally the message) — "it threw something" is too weak.

## Structuring suites

```js
describe("formatPrice", () => {
  it("formats whole dollars without cents", () => { /* ... */ });
  it("always shows two decimals for fractional prices", () => { /* ... */ });
});
```

`describe` groups one *subject*; `it` states one *behavior*. Nested describes encode context: `describe("with an empty cart")`. If a test name needs "and", split it.

## Hooks

- `beforeEach` — fresh state per test (the default choice; independence!)
- `afterEach` — cleanup (restore stubbed globals, clear storage)
- `beforeAll` — expensive shared setup (start a server); use sparingly because it *couples* tests

The classic bug source: tests sharing mutable state (a module-level array one test appends to). Fresh state per test costs milliseconds and buys reliability.

## Edge cases first

For any function, before the happy path, enumerate: **empty input** (array, string, object), **boundaries** (0, -1, max), **wrong types** (null, undefined, non-numbers), and **duplicates**. Most production bugs live there — write the test that would have caught yours last time.""",
    "Assertion và cấu trúc test",
    "Cơ chế bên dưới mọi framework test: so sánh fail to và chính xác, hook before/after, và tổ chức suite có khả năng mở rộng.",
    """Mọi framework test — Jest, Vitest, Mocha — chỉ là lớp đường trên cùng một lõi: chạy code, so sánh, báo cáo. Tự dựng lõi một lần là hiểu hết tất cả.

## Assertion: fail to, fail chính xác

```js
function assertEqual(actual, expected, msg) {
  if (!Object.is(actual, expected)) {
    throw new Error(`${msg ?? "assert failed"}: expected ${fmt(expected)}, got ${fmt(actual)}`);
  }
}
```

Những quy tắc đúc kết từ đau khổ:

- **Message nêu kỳ vọng**, không nêu cơ chế. "Tổng giỏ hàng loại bỏ số lượng âm" hơn "0 !== -5".
- **Deep equality** cho object: `Object.is` so tham chiếu; bạn cần so sánh cấu trúc (hoặc `JSON.stringify` như thủ thuật thô — nhạy thứ tự, ghét undefined).
- **`assertThrows(fn, ErrorType)`** phải kiểm tra cả *kiểu lỗi* (và lý tưởng là message) — "nó ném ra cái gì đó" là quá yếu.

## Tổ chức suite

```js
describe("formatPrice", () => {
  it("formats whole dollars without cents", () => { /* ... */ });
  it("always shows two decimals for fractional prices", () => { /* ... */ });
});
```

`describe` gom một *đối tượng*; `it` nêu một *hành vi*. describe lồng nhau mã hóa ngữ cảnh: `describe("with an empty cart")`. Tên test có chữ "and" là phải tách.

## Hook

- `beforeEach` — trạng thái mới cho mỗi test (lựa chọn mặc định; độc lập!)
- `afterEach` — dọn dẹp (khôi phục stub, xóa storage)
- `beforeAll` — setup đắt dùng chung (khởi động server); dùng ít vì nó *ghim* các test vào nhau

Nguồn bug kinh điển: các test dùng chung trạng thái mutable (một mảng module-level mà test này append). Trạng thái mới mỗi test tốn mili giây nhưng mua được độ tin cậy.

## Edge case trước

Với bất kỳ hàm nào, trước cả happy path, hãy liệt kê: **input rỗng** (mảng, chuỗi, object), **biên** (0, -1, max), **sai kiểu** (null, undefined, số không phải số), và **trùng lặp**. Phần lớn bug production sống ở đó — hãy viết cái test mà lần trước lẽ ra đã bắt được bug của bạn.""",
)

write_lesson(
    MOD, "test-doubles",
    "Test Doubles: Mocks, Stubs, Spies, Fakes",
    "Isolate the code under test from its collaborators — without letting the doubles themselves become lies.",
    20,
    """A unit test must fail because *your code* is wrong — not because the network was down, the clock drifted, or the database was empty. Test doubles replace collaborators with controllable stand-ins.

## The taxonomy (precisely)

- **Stub** — returns canned answers. `stubFetch` that always resolves `{"ok": true}`. You don't assert on it; your code calls it and you assert on the *result*.
- **Spy** — wraps a real (or fake) function and records calls: arguments, count, order. You assert on *how your code used it*.
- **Mock** — a stub with expectations pre-loaded: "this must be called once with X, or the test fails." Powerful; overuse couples tests to implementation.
- **Fake** — a real lightweight implementation: an in-memory Map instead of a database, a queue that actually queues.

## The dependency seam

You can only substitute what your code can *reach from outside*. This is why hardcoded dependencies are a testing smell:

```js
// untestable as a unit — fetch is welded in
export async function loadUser(id) {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

// testable — the collaborator arrives by parameter
export function makeUserLoader(fetchLike) {
  return async (id) => {
    const res = await fetchLike(`/api/users/${id}`);
    return res.json();
  };
}
```

Constructor injection, function parameters, or module-level indirection — any seam works. The pattern is the point, not the mechanism.

## The classic spy, by hand

```js
function makeSpy(impl) {
  const calls = [];
  const spy = (...args) => {
    calls.push(args);
    return impl?.(...args);
  };
  spy.calls = calls;
  return spy;
}
```

Then: `spy.calls.length === 2`, `spy.calls[0][0] === "/api/users/42"`. This is literally what `vi.fn()` / `jest.fn()` are.

## What NOT to double

Don't stub the function under test's own pure logic — only collaborators with side effects (network, clock, storage, randomness). Over-mocked tests pass while production burns: they verify your *assumptions*, not your code. When a test needs five mocks to run, the code is asking for a redesign (fewer collaborators, more seam, smaller unit).""",
    "Test double: Mock, Stub, Spy, Fake",
    "Cô lập code đang test khỏi các cộng sự của nó — mà không để chính double trở thành lời nói dối.",
    """Unit test phải fail vì *code của bạn* sai — chứ không phải vì mạng chập chờn, đồng hồ trôi, hay database trống. Test double thay thế các cộng sự bằng bản đứng thay điều khiển được.

## Phân loại (chính xác)

- **Stub** — trả về câu trả lời đóng hộp. `stubFetch` luôn resolve `{"ok": true}`. Bạn không assert trên nó; code của bạn gọi nó và bạn assert trên *kết quả*.
- **Spy** — bọc một hàm thật (hoặc giả) và ghi lại các lần gọi: tham số, số lần, thứ tự. Bạn assert trên *cách code của bạn dùng nó*.
- **Mock** — stub kèm kỳ vọng nạp sẵn: "phải được gọi một lần với X, không thì test fail." Mạnh; lạm dụng sẽ ghim test vào hiện thực.
- **Fake** — một hiện thực nhẹ nhưng thật: Map trong bộ nhớ thay cho database, queue xếp hàng thật.

## Đường nối (seam) cho dependency

Chỉ thay thế được thứ mà code của bạn *chạm tới từ bên ngoài*. Đây là lý do dependency hardcode là mùi hiểm độc khi test:

```js
// không test được như unit — fetch bị hàn cứng
export async function loadUser(id) {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

// test được — cộng sự đi vào bằng tham số
export function makeUserLoader(fetchLike) {
  return async (id) => {
    const res = await fetchLike(`/api/users/${id}`);
    return res.json();
  };
}
```

Constructor injection, tham số hàm, hay gián tiếp qua module — seam nào cũng được. Mô hình mới là điểm mấu chốt, không phải cơ chế.

## Cây spy kinh điển, làm tay

```js
function makeSpy(impl) {
  const calls = [];
  const spy = (...args) => {
    calls.push(args);
    return impl?.(...args);
  };
  spy.calls = calls;
  return spy;
}
```

Rồi: `spy.calls.length === 2`, `spy.calls[0][0] === "/api/users/42"`. Đây chính xác là thứ mà `vi.fn()` / `jest.fn()` làm.

## Điều KHÔNG nên double

Đừng stub logic thuần của chính hàm đang test — chỉ double cộng sự có side effect (mạng, đồng hồ, storage, random). Test mock dư thừa pass trong khi production cháy: chúng xác minh *giả định* của bạn, không phải code của bạn. Khi một test cần năm mock mới chạy được, code đang kêu xin tái cấu trúc (ít cộng sự hơn, nhiều seam hơn, unit nhỏ hơn).""",
)

write_lesson(
    MOD, "debugging-method",
    "A Debugging Method That Works",
    "Reproduce, isolate, understand, fix, prove — replacing superstitious guesswork with a loop that always terminates.",
    22,
    """Debugging is not a talent; it's a search procedure. The difference between a struggling junior and a calm senior is that the senior's loop *halves the search space every step*.

## The five-step loop

1. **Reproduce reliably.** A bug you can't reproduce on demand is a bug you can't fix. Find the minimal input: which exact data, which exact sequence? (An automated reproduction — a failing test — is gold: it becomes your regression test later.)
2. **Isolate.** Binary search the pipeline. Does the data arrive wrong from the API, or get corrupted in processing, or render wrong? Log/inspect at the midpoint. Wrong upstream? The bug is upstream; throw away the downstream half. Repeat. Even a 10-step pipeline falls in ~4 steps.
3. **Understand.** Found the line — now explain *why* it produces the wrong output. "The filter keeps items where `qty` is truthy, and 0 is falsy" is understanding. "I removed the filter and it worked" is superstition; it'll bite you next week.
4. **Fix the cause, not the symptom.** Guarding against the corrupted value downstream hides the bug; fixing the producer of the corrupted value removes it. Symptom patches accumulate into systems nobody can reason about.
5. **Prove it.** Write the failing test FIRST (it fails before the fix), then fix, then watch it pass, then keep it forever as a regression test. A fix without a test is a rumor.

## Tools that matter

- **Breakpoints > console.log.** The debugger pauses *state in context*: every variable in scope, the call stack that led here. Log statements show you a photo; the debugger gives you the whole album, backward.
- **Conditional breakpoints** for loops that iterate 10,000 times: break only when `i === 937`.
- **Watch expressions** track a value across steps.
- **Network tab**: what actually left the browser, headers included. Half of "frontend bugs" are requests the code never made, or responses it misread.
- **`git bisect`** (module 6!): when "it used to work," history finds the culprit commit in log-time.

## Reading stack traces like a pro

Read the *top* frame first — that's where the error was thrown. Then walk down to the first frame that is *your code* (skip library internals). The error message tells you what; the frame tells you where; the surrounding code tells you why. `undefined is not a function` means a name resolved to undefined — check for typos, missing imports, or an object that isn't the shape you assumed.

## When you're stuck

Explain the bug out loud, line by line, to anyone (or a rubber duck) — articulating the *expected* vs *actual* flow frequently reveals the gap mid-sentence. And if 30 minutes of binary search hasn't narrowed anything: you're searching the wrong pipeline. Stop, re-map the data flow, pick a new midpoint.""",
    "Phương pháp gỡ lỗi thực sự hiệu quả",
    "Tái hiện, cô lập, hiểu, sửa, chứng minh — thay trò đoán bói bằng một vòng lặp luôn kết thúc.",
    """Gỡ lỗi không phải tài năng; đó là một thủ tục tìm kiếm. Khác biệt giữa junior loay hoay và senior bình tĩnh là vòng lặp của senior *chia đôi không gian tìm kiếm mỗi bước*.

## Vòng lặp năm bước

1. **Tái hiện được tin cậy.** Bug không tái hiện theo yêu cầu là bug không sửa được. Tìm input tối thiểu: dữ liệu chính xác nào, chuỗi thao tác chính xác nào? (Một bản tái hiện tự động — một test failing — là vàng: sau này nó trở thành regression test.)
2. **Cô lập.** Tìm kiếm nhị phân trên pipeline. Dữ liệu về sai từ API, bị hỏng trong lúc xử lý, hay render sai? Log/xem tại điểm giữa. Sai từ thượng nguồn? Bug nằm thượng nguồn; vứt bỏ nửa hạ nguồn. Lặp lại. Pipeline 10 bước cũng sụp trong ~4 bước.
3. **Hiểu.** Tìm ra dòng lỗi — giờ giải thích *tại sao* nó tạo output sai. "Bộ lọc giữ item có `qty` truthy, mà 0 là falsy" là hiểu. "Tôi bỏ filter đi và nó chạy" là mê tín; tuần sau nó cắn bạn.
4. **Sửa nguyên nhân, không sửa triệu chứng.** Chặn giá trị hỏng ở hạ nguồn chỉ là giấu bug; sửa nơi sinh ra giá trị hỏng mới xóa được nó. Các bản vá triệu chứng chất đống thành hệ thống không ai lý giải nổi.
5. **Chứng minh.** Viết test failing TRƯỚC (nó fail trước khi sửa), rồi sửa, rồi nhìn nó pass, rồi giữ nó mãi làm regression test. Bản sửa không có test chỉ là tin đồn.

## Công cụ đáng giá

- **Breakpoint > console.log.** Debugger dừng *trạng thái trong ngữ cảnh*: mọi biến trong scope, cả call stack dẫn đến đây. Câu log là một tấm ảnh; debugger cho cả cuốn album, kể cả những tấm phía sau.
- **Conditional breakpoint** cho vòng lặp chạy 10,000 lần: chỉ dừng khi `i === 937`.
- **Watch expression** theo dõi một giá trị qua từng bước.
- **Tab Network**: thứ thực sự rời khỏi trình duyệt, kèm headers. Một nửa "bug frontend" là request code không bao giờ gửi, hoặc response nó đọc sai.
- **`git bisect`** (module 6!): khi "trước đây nó chạy mà", lịch sử tìm ra commit thủ phạm theo thời gian log.

## Đọc stack trace như dân chuyên

Đọc frame *đỉnh* trước — nơi lỗi được ném. Rồi đi xuống đến frame đầu tiên là *code của bạn* (bỏ qua nội bộ thư viện). Message nói cho bạn *cái gì*; frame nói *ở đâu*; code xung quanh nói *tại sao*. `undefined is not a function` nghĩa là một tên resolve thành undefined — kiểm tra lỗi gõ, thiếu import, hoặc object không có hình dạng bạn tưởng.

## Khi bí

Giải thích bug thành tiếng, từng dòng, cho bất kỳ ai (hoặc con vịt cao su) — việc nói ra *luồng kỳ vọng* và *luồng thực tế* thường hé lộ khoảng trống ngay giữa câu. Và nếu 30 phút tìm kiếm nhị phân mà chẳng thu hẹp được gì: bạn đang tìm sai pipeline. Dừng lại, vẽ lại luồng dữ liệu, chọn điểm giữa mới.""",
)

write_lesson(
    MOD, "devtools-observability",
    "Observing Real Applications",
    "DevTools as an instrument panel: sources and breakpoints, the network waterfall, console discipline, and performance first-aid.",
    18,
    """Production bugs don't come with test names. You observe live systems with DevTools — here's the panel.

## Sources panel: the debugger in the wild

- Set breakpoints in the served code (Sources → your file → click a line number).
- **Event listener breakpoints**: break on every `click` or `submit` — instantly find which handler owns a behavior.
- **XHR/fetch breakpoints**: break when any request URL matches a pattern — catch the code that fires surprise requests.
- **Debug on exception** (pause on caught/uncaught): stop exactly where things go wrong instead of chasing it after.

## Network panel: truth about requests

Columns that matter: **status** (304 vs 200 vs 404 — is caching working, is the endpoint real), **size** (actual transfer vs decompressed), **time** (queueing? TTFB? download?), and the **waterfall order** (what blocked what). Click any request → Response/Preview tabs to see the payload your code actually received. The "Initiator" column names the exact line that fired the request — the fastest route from mystery request to owning code.

## Console discipline

`console.log` is fine; three upgrades:

- `console.table(rows)` — arrays of objects, aligned and scannable
- `console.error`/`warn` for actual anomalies — they carry stack traces and filter separately
- **Log points** (right-click a line in Sources → "Add logpoint"): logging without editing code, surviving reloads

And the console *is a REPL*: inspect any live object, run `document.querySelectorAll` experiments, call functions by hand. The console is not just for output you anticipated.

## Performance first-aid (deep dive = module 8)

- **Performance panel**: record an interaction, look for the red — long tasks blocking the main thread, forced synchronous layout (purple "Recalculate Style" storms), jank between frames.
- **Lighthouse**: quick audit scores for performance/accessibility; a *compass*, not a map — it suggests, you diagnose.

## When DevTools lies

Minified production code renames everything; use source maps (or reproduce locally). And remember *heisenbugs*: adding logging can change timing and hide race conditions. When a bug won't show itself under observation, look for ordering/timing assumptions — module 3 taught you why those exist.""",
    "Quan sát ứng dụng thật",
    "DevTools như bảng đồng hồ vận hành: sources và breakpoint, waterfall mạng, kỷ luật console, và sơ cứu hiệu năng.",
    """Bug production không mang theo tên test. Bạn quan sát hệ thống đang sống bằng DevTools — đây là bảng điều khiển.

## Panel Sources: debugger ngoài tự nhiên

- Đặt breakpoint trên code được serve (Sources → file của bạn → bấm số dòng).
- **Event listener breakpoint**: dừng ở mọi `click` hoặc `submit` — lập tức tìm ra handler nào sở hữu hành vi đó.
- **XHR/fetch breakpoint**: dừng khi URL request khớp mẫu — tóm được code phát request bất ngờ.
- **Debug on exception** (dừng ở caught/uncaught): đứng đúng chỗ mọi thứ sai thay vì đuổi theo sau đó.

## Panel Network: sự thật về request

Các cột quan trọng: **status** (304 so với 200 so với 404 — cache có chạy, endpoint có tồn tại), **size** (transfer thực so với đã giải nén), **time** (chờ đợi? TTFB? download?), và **thứ tự waterfall** (cái gì chặn cái gì). Bấm vào request → tab Response/Preview để thấy payload code của bạn thực sự nhận. Cột "Initiator" nêu tên dòng chính xác đã bắn request — con đường nhanh nhất từ request bí ẩn đến code sở hữu nó.

## Kỷ luật console

`console.log` vẫn ổn; ba nâng cấp:

- `console.table(rows)` — mảng object, thẳng hàng, quét nhanh được
- `console.error`/`warn` cho dị thường thật — chúng kèm stack trace và lọc riêng được
- **Log point** (chuột phải một dòng trong Sources → "Add logpoint"): log mà không sửa code, sống sót qua reload

Và console *là một REPL*: inspect mọi object đang sống, chạy thử `document.querySelectorAll`, gọi hàm thủ công. Console không chỉ để in những gì bạn lường trước.

## Sơ cứu hiệu năng (đào sâu = module 8)

- **Panel Performance**: ghi lại một tương tác, tìm chỗ đỏ — long task chặn main thread, forced synchronous layout (bão "Recalculate Style" màu tím), giật giữa các frame.
- **Lighthouse**: audit nhanh điểm số hiệu năng/khả năng tiếp cận; là *kim chỉ nam*, không phải bản đồ — nó gợi ý, bạn chẩn đoán.

## Khi DevTools nói dối

Code production đã minify đổi tên mọi thứ; dùng source map (hoặc tái hiện local). Và nhớ *heisenbug*: thêm log có thể đổi thời điểm chạy và giấu race condition. Khi một bug không chịu lộ diện dưới quan sát, hãy nghi ngờ các giả định về thứ tự/thời điểm — module 3 đã dạy bạn vì sao chúng tồn tại.""",
)

write_checkpoint(
    MOD,
    "repair-checkpoint",
    "Checkpoint: Test & Repair",
    "Prove the debugging loop: diagnose failures from evidence, write the regression test, and fix the cause.",
    20,
    """This checkpoint compresses the repair workflow into runnable form: each challenge hands you evidence (a test failure, a stack trace pattern, a spy's call log) and grades whether your *diagnosis and fix* are correct — the same reasoning you'll do in a real editor with a real broken app.""",
    "Kiểm tra kiến thức: Test & Sửa lỗi",
    "Chứng minh vòng lặp gỡ lỗi: chẩn đoán từ bằng chứng, viết regression test, và sửa đúng nguyên nhân.",
    """Checkpoint này nén quy trình sửa lỗi thành dạng chạy được: mỗi thử thách đưa cho bạn bằng chứng (một lần test fail, một mẫu stack trace, nhật ký gọi của spy) và chấm xem *chẩn đoán và bản sửa* của bạn có đúng không — cùng lập luận bạn sẽ làm trong editor thật với một ứng dụng hỏng thật.""",
    {
        "id": "i2-repair-checkpoint",
        "title": "Repair Room",
        "prompt": "Write THREE functions. 1) `diagnose(testName)` — map failing test names to causes: names containing \"empty\" -> \"edge-case\", containing \"slow\" -> \"performance\", containing \"null\" or \"undefined\" -> \"type-error\", otherwise \"logic\". 2) `analyzeSpy(spy, expectedCount, expectedFirstArg)` — spy is { calls: [[arg...], ...] }; return true only when calls.length === expectedCount AND calls[0][0] === expectedFirstArg, else false (handle zero calls safely). 3) `fixAndProve(isFixed, testPasses)` — a fix counts only when BOTH the underlying behavior is fixed AND the regression test passes: return \"fixed\" when both true, \"untested\" when fixed but test fails, \"broken\" otherwise.",
        "difficulty": "intermediate",
        "level": "checkpoint",
        "boilerplate": "function diagnose(testName) {\n  // your code\n}\n\nfunction analyzeSpy(spy, expectedCount, expectedFirstArg) {\n  // your code\n}\n\nfunction fixAndProve(isFixed, testPasses) {\n  // your code\n}\n",
        "tests": [
            {
                "name": "diagnoses from test evidence",
                "code": "const fn = new Function(code + \"\\nreturn { diagnose, analyzeSpy, fixAndProve };\");\nconst { diagnose } = fn();\nif (diagnose(\"handles empty cart\") !== \"edge-case\") throw new Error(\"'empty' => edge-case.\");\nif (diagnose(\"responds slowly\") !== \"performance\") throw new Error(\"'slow' => performance.\");\nif (diagnose(\"crashes on null input\") !== \"type-error\") throw new Error(\"'null' => type-error.\");\nif (diagnose(\"adds items in order\") !== \"logic\") throw new Error(\"Everything else => logic.\");",
                "hint": "Check 'empty' first, then 'slow', then 'null'/'undefined', then default.",
            },
            {
                "name": "reads spy evidence correctly",
                "code": "const fn = new Function(code + \"\\nreturn { diagnose, analyzeSpy, fixAndProve };\");\nconst { analyzeSpy } = fn();\nif (!analyzeSpy({ calls: [[\"/api/users\"], [\"/api/posts\"]] }, 2, \"/api/users\")) throw new Error(\"Two calls, first is /api/users => true.\");\nif (analyzeSpy({ calls: [[\"/api/users\"]] }, 2, \"/api/users\")) throw new Error(\"Wrong count => false.\");\nif (analyzeSpy({ calls: [] }, 0, \"x\")) throw new Error(\"Zero calls can't match a first arg => false.\");\nif (analyzeSpy({ calls: [[\"a\"]] }, 1, \"a\") !== true) throw new Error(\"Exact match => true.\");",
                "hint": "Guard the empty-calls case before reading calls[0][0].",
            },
            {
                "name": "a fix only counts with proof",
                "code": "const fn = new Function(code + \"\\nreturn { diagnose, analyzeSpy, fixAndProve };\");\nconst { fixAndProve } = fn();\nif (fixAndProve(true, true) !== \"fixed\") throw new Error(\"Fixed + proven => fixed.\");\nif (fixAndProve(true, false) !== \"untested\") throw new Error(\"Fixed without a passing test => untested.\");\nif (fixAndProve(false, true) !== \"broken\") throw new Error(\"Test passes but behavior broken => broken.\");",
                "hint": "Three outcomes from two booleans — truth table it.",
            },
        ],
    },
    {
        "id": "i2-repair-checkpoint",
        "title": "Phòng sửa lỗi",
        "prompt": "Viết BA hàm. 1) `diagnose(testName)` — ánh xạ tên test fail sang nguyên nhân: tên chứa \"empty\" -> \"edge-case\", chứa \"slow\" -> \"performance\", chứa \"null\" hoặc \"undefined\" -> \"type-error\", còn lại \"logic\". 2) `analyzeSpy(spy, expectedCount, expectedFirstArg)` — spy là { calls: [[arg...], ...] }; trả về true chỉ khi calls.length === expectedCount VÀ calls[0][0] === expectedFirstArg, ngược lại false (xử lý an toàn khi không có lần gọi nào). 3) `fixAndProve(isFixed, testPasses)` — một bản sửa chỉ được tính khi CẢ hành vi đã được sửa VÀ regression test pass: trả về \"fixed\" khi cả hai true, \"untested\" khi đã sửa nhưng test fail, \"broken\" trong các trường hợp còn lại.",
        "tests": [
            {"name": "chẩn đoán từ bằng chứng test", "hint": "Kiểm tra 'empty' trước, rồi 'slow', rồi 'null'/'undefined', cuối cùng là mặc định."},
            {"name": "đọc đúng bằng chứng từ spy", "hint": "Chặn trường hợp calls rỗng trước khi đọc calls[0][0]."},
            {"name": "bản sửa chỉ được tính khi có chứng minh", "hint": "Ba kết quả từ hai boolean — lập bảng chân trị."},
        ],
    },
)

print("Module 7 lessons + checkpoint written.")
