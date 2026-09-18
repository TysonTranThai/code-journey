#!/usr/bin/env python3
"""Python Intermediate — module 7 (testing-discipline)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

M7 = "testing-discipline"
L7A = "unittest-first"
L7B = "subtest-parametrize"
L7C = "mocking-boundaries"
L7D = "checkpoint-repair"

write_module(
    M7,
    "Testing Discipline",
    "Test like an engineer: runnable suites, parametrized cases, and mocks at boundaries.",
    "Kỷ luật Kiểm thử",
    "Kiểm thử như một kỹ sư: bộ test chạy được, ca kiểm thử tham số hóa, và mock tại ranh giới.",
    [L7A, L7B, L7C, L7D],
    ["m7-unittest-practice", "m7-subtest-practice", "m7-mock-practice"],
)

write_lesson(
    M7, L7A,
    " unittest: Your First Real Suite",
    "TestCase classes, self.assertEqual, setUp, and running tests programmatically.",
    15,
    """
Assertions in a script stop at the first failure. A **test suite** runs every
case, reports all failures, and becomes your safety net for refactoring.
`unittest` ships with Python:

```python
import unittest

class TestInvoice(unittest.TestCase):
    def setUp(self):                       # fresh fixture per test
        self.invoice = Invoice(["tea", "cup"])

    def test_total_sums_items(self):
        self.assertEqual(self.invoice.total(), 7)

    def test_empty_invoice_is_zero(self):
        self.assertEqual(Invoice([]).total(), 0)

if __name__ == "__main__":
    unittest.main()
```

What you gain over bare asserts:

- **Independent tests**: `setUp` runs fresh before each method — no shared mutable state, no order dependence.
- **Rich failure output**: expected vs actual, per test.
- **A runner**: `python -m unittest` discovers and runs everything; the platform's sandbox runs your tests the same way.

Test naming is communication: `test_total_sums_items` says what behavior is
expected. When a test fails months from now, the name is the first hint.
""",
    "unittest: Bộ test thật đầu tiên",
    "Lớp TestCase, self.assertEqual, setUp, và chạy test bằng lập trình.",
    """
Assertion trong một script dừng ở lỗi đầu tiên. Một **bộ test** chạy mọi ca,
báo tất cả thất bại, và trở thành lưới an toàn khi refactor. `unittest` có
sẵn trong Python:

```python
import unittest

class TestInvoice(unittest.TestCase):
    def setUp(self):                       # fixture mới cho mỗi test
        self.invoice = Invoice(["tea", "cup"])

    def test_total_sums_items(self):
        self.assertEqual(self.invoice.total(), 7)

    def test_empty_invoice_is_zero(self):
        self.assertEqual(Invoice([]).total(), 0)

if __name__ == "__main__":
    unittest.main()
```

Những gì bạn có hơn assert trần:

- **Test độc lập**: `setUp` chạy mới trước mỗi method — không trạng thái dùng chung, không phụ thuộc thứ tự.
- **Kết quả thất bại giàu thông tin**: kỳ vọng vs thực tế, cho từng test.
- **Một runner**: `python -m unittest` dò và chạy tất cả; sandbox của nền tảng chạy test của bạn theo cùng cách.

Tên test là thông điệp: `test_total_sums_items` nói rõ hành vi kỳ vọng. Khi
một test thất bại nhiều tháng sau, cái tên là manh mối đầu tiên.
""",
)

write_lesson(
    M7, L7B,
    "Parametrizing with subTest",
    "One test, many cases — and failing all of them, not just the first.",
    12,
    """
Testing a function against twenty inputs by copy-pasting twenty methods is
noise. `subTest` runs a loop of cases **inside one test method** — and keeps
going after a failure so you see every broken case at once:

```python
import unittest

class TestParse(unittest.TestCase):
    def test_parse_counts(self):
        cases = [
            ("42", 42),        # plain
            ("  7 ", 7),       # whitespace
            ("0", 0),          # zero
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(parse_count(text), expected)
```

Without `subTest`, the first bad case hides the rest. With it, one run shows
`text='  7 '` failed AND `text='0'` failed — the full picture in a single
run. This is unittest's native answer to pytest's `parametrize` (pytest is
the ecosystem favorite; its shape transfers directly).

## Edge cases deserve explicit rows

Keep a mental checklist as you write the case list: empty, zero, one,
negative, huge, unicode, whitespace, wrong type. Each becomes one row. A case
list is also **executable documentation** of what your function accepts.
""",
    "Tham số hóa với subTest",
    "Một test, nhiều ca — và báo hết các ca lỗi, không chỉ ca đầu tiên.",
    """
Kiểm thử một hàm với hai mươi input bằng cách dán hai mươi method là nhiễu.
`subTest` chạy một vòng các ca **bên trong một test method** — và tiếp tục
sau một lần fail để bạn thấy mọi ca lỗi cùng lúc:

```python
import unittest

class TestParse(unittest.TestCase):
    def test_parse_counts(self):
        cases = [
            ("42", 42),        # thuần
            ("  7 ", 7),       # khoảng trắng
            ("0", 0),          # số không
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(parse_count(text), expected)
```

Không có `subTest`, ca lỗi đầu che giấu phần còn lại. Với `subTest`, một lần
chạy cho thấy `text='  7 '` lỗi VÀ `text='0'` lỗi — toàn cảnh trong một lần
chạy. Đây là câu trả lời thuần unittest cho `parametrize` của pytest (pytest
là lựa chọn yêu thích của hệ sinh thái; hình dạng của nó chuyển giao trực tiếp).

## Các ca biên xứng đáng có dòng riêng

Giữ một checklist trong đầu khi viết danh sách ca: rỗng, số không, một, âm,
to, unicode, khoảng trắng, sai kiểu. Mỗi mục thành một dòng. Danh sách ca
còn là **tài liệu chạy được** cho những gì hàm của bạn chấp nhận.
""",
)

write_lesson(
    M7, L7C,
    "Mocking Boundaries",
    "unittest.mock.patch — isolate the code under test from slow, flaky, or dangerous collaborators.",
    14,
    """
Your function calls the network, the clock, the filesystem. Tests that hit
real services are slow, flaky, and sometimes destructive. **Mock** the
boundary:

```python
from unittest.mock import patch

def fetch_price(url):
    import urllib.request
    with urllib.request.urlopen(url) as r:
        return int(r.read())

class TestPrice(unittest.TestCase):
    @patch("__main__.urllib.request.urlopen")
    def test_fetch_price_parses(self, fake_urlopen):
        fake_urlopen.return_value.__enter__.return_value.read.return_value = b"123"
        self.assertEqual(fetch_price("http://example.com"), 123)
```

`patch` swaps the real object for a `Mock` for the duration of the test and
restores it afterwards. The mock records **how it was called**, so you can
assert behavior, not just return values:

```python
fake_send.assert_called_once_with("hello")
```

## What to mock — and what never to mock

Mock **edges**: network, clock, random, filesystem, external services. Keep
**domain logic real** — mocking the code under test's own calculations makes
the test a tautology. Rule of thumb: if you're mocking it, it should be a
collaborator, not the subject.

## The danger sign

Tests full of mocks that mirror the implementation break on every refactor
and prove nothing. Prefer testing through the public API; mock only what you
cannot afford to touch for real.
""",
    "Mock tại Ranh giới",
    "unittest.mock.patch — tách code đang test khỏi những collaborator chậm, hay lỗi, hoặc nguy hiểm.",
    """
Hàm của bạn gọi mạng, đồng hồ, hệ thống tệp. Test chạm dịch vụ thật thì
chậm, hay trục trặc, và đôi khi phá hoại. Hãy **mock** ranh giới:

```python
from unittest.mock import patch

def fetch_price(url):
    import urllib.request
    with urllib.request.urlopen(url) as r:
        return int(r.read())

class TestPrice(unittest.TestCase):
    @patch("__main__.urllib.request.urlopen")
    def test_fetch_price_parses(self, fake_urlopen):
        fake_urlopen.return_value.__enter__.return_value.read.return_value = b"123"
        self.assertEqual(fetch_price("http://example.com"), 123)
```

`patch` hoán đổi đối tượng thật bằng một `Mock` trong thời gian test và khôi
phục sau đó. Mock **ghi lại cách nó được gọi**, nên bạn có thể assert hành
vi, không chỉ giá trị trả về:

```python
fake_send.assert_called_once_with("hello")
```

## Mock gì — và không bao giờ mock gì

Mock **các cạnh**: mạng, đồng hồ, random, hệ thống tệp, dịch vụ ngoài. Giữ
**logic miền là thật** — mock chính phép tính của code đang test khiến bài
test thành đồng nghĩa lặp lại. Nguyên tắc: nếu bạn đang mock nó, nó phải là
một collaborator, không phải đối tượng chính.

## Dấu hiệu nguy hiểm

Test đầy mock phản chiếu chính bản cài đặt sẽ vỡ trong mọi lần refactor và
không chứng minh điều gì. Ưu tiên test qua API công khai; chỉ mock những gì
bạn không dám chạm thật.
""",
)

# --- module 7 practice sets ---
write_practice(
    M7, "m7-unittest-practice",
    "unittest Drills",
    "Build real suites with setUp and meaningful assertions.",
    "Luyện unittest",
    "Dựng bộ test thật với setUp và assertion có ý nghĩa.",
    L7A, 30, "intermediate",
    [
        challenge(
            "pi7-ut-suite", "First Suite",
            "Implement a function slugify(text) that lowercases and joins words with '-' (split on whitespace). Then write a unittest.TestCase class named TestSlugify with TWO test methods covering a normal case and an edge case, and assign the class to the variable SUITE_TEST (the grader imports it and runs it).",
            "import unittest\n\ndef slugify(text):\n    pass\n\nclass TestSlugify(unittest.TestCase):\n    pass\n\nSUITE_TEST = None  # set to your TestCase class\n",
            [
                ("slugify behaves",
                 "assert slugify('Hello Big World') == 'hello-big-world'\nassert slugify('  spaced   out  ') == 'spaced-out'",
                 "text.split() handles runs of whitespace; '-'.join(words)."),
                ("suite is a TestCase subclass with 2+ tests",
                 "import unittest\nassert issubclass(SUITE_TEST, unittest.TestCase)\nloader = unittest.TestLoader()\nsuite = loader.loadTestsFromTestCase(SUITE_TEST)\nassert suite.countTestCases() >= 2",
                 "Two or more test methods starting with 'test_'."),
                ("tests actually pass",
                 "import unittest, io\nstream = io.StringIO()\nrunner = unittest.TextTestRunner(stream=stream, verbosity=0)\nresult = runner.run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\nassert result.wasSuccessful(), stream.getvalue()",
                 "Your own tests must pass — the runner reports failures."),
            ],
            level="guided",
        ),
        challenge(
            "pi7-ut-setup", "Fixture Discipline",
            "Implement class Cart with add(item, price) and total(). Then write TestCart whose setUp creates a fresh self.cart with one item ('tea', 3) and whose tests add more and assert totals. Assign the class to SUITE_TEST.",
            "import unittest\n\nclass Cart:\n    pass\n\nclass TestCart(unittest.TestCase):\n    pass\n\nSUITE_TEST = None\n",
            [
                ("cart works",
                 "c = Cart()\nc.add('tea', 3)\nassert c.total() == 3\nc.add('cup', 4)\nassert c.total() == 7",
                 "add accumulates prices; total sums them."),
                ("setUp runs per test",
                 "import unittest\nsrc = __import__('inspect').getsource(SUITE_TEST)\nassert 'def setUp' in src\nassert src.count('def test_') >= 2",
                 "setUp method plus at least two tests using self.cart."),
                ("suite passes",
                 "import unittest, io\nstream = io.StringIO()\nresult = unittest.TextTestRunner(stream=stream, verbosity=0).run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\nassert result.wasSuccessful(), stream.getvalue()",
                 "Independent, green tests — no shared state leaks."),
            ],
            level="independent",
        ),
    ],
    {
        "pi7-ut-suite": vi_challenge("Bộ test đầu tiên", "Viết hàm slugify(text) chuyển thành chữ thường và nối các từ bằng '-' (tách theo khoảng trắng). Sau đó viết lớp unittest.TestCase tên TestSlugify với HAI test method phủ một ca thường và một ca biên, và gán lớp đó vào biến SUITE_TEST (trình chấm import và chạy nó).", [("slugify hoạt động", "text.split() xử lý chuỗi khoảng trắng; '-'.join(words)."), ("Suite là lớp con TestCase có 2+ test", "Hai hoặc nhiều method bắt đầu bằng 'test_'."), ("Test thật sự pass", "Test của chính bạn phải pass — runner sẽ báo lỗi.")]),
        "pi7-ut-setup": vi_challenge("Kỷ luật Fixture", "Viết class Cart với add(item, price) và total(). Sau đó viết TestCart mà setUp tạo một self.cart mới với một mặt hàng ('tea', 3) và các test thêm nữa rồi assert tổng. Gán lớp vào SUITE_TEST.", [("Cart hoạt động", "add tích lũy giá; total cộng lại."), ("setUp chạy cho từng test", "Method setUp cộng với ít nhất hai test dùng self.cart."), ("Suite pass", "Test xanh, độc lập — không rò rỉ trạng thái dùng chung.")]),
    },
    solutions=[
        ("pi7-ut-suite", "import unittest\n\ndef slugify(text):\n    return '-'.join(text.lower().split())\n\nclass TestSlugify(unittest.TestCase):\n    def test_normal(self):\n        self.assertEqual(slugify('Hello Big World'), 'hello-big-world')\n\n    def test_extra_whitespace(self):\n        self.assertEqual(slugify('  spaced   out  '), 'spaced-out')\n\nSUITE_TEST = TestSlugify", "import unittest\n\ndef slugify(text):\n    return text.lower().replace(' ', '-')\n\nclass TestSlugify(unittest.TestCase):\n    def test_normal(self):\n        self.assertEqual(slugify('Hello Big World'), 'hello-big-world')\n\n    def test_extra_whitespace(self):\n        self.assertEqual(slugify('  spaced   out  '), 'spaced   -out')\n\nSUITE_TEST = TestSlugify"),
        ("pi7-ut-setup", "import unittest\n\nclass Cart:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, item, price):\n        self.prices.append(price)\n\n    def total(self):\n        return sum(self.prices)\n\nclass TestCart(unittest.TestCase):\n    def setUp(self):\n        self.cart = Cart()\n        self.cart.add('tea', 3)\n\n    def test_starts_with_tea(self):\n        self.assertEqual(self.cart.total(), 3)\n\n    def test_adding_items(self):\n        self.cart.add('cup', 4)\n        self.assertEqual(self.cart.total(), 7)\n\nSUITE_TEST = TestCart", "import unittest\n\nclass Cart:\n    cart = []\n\n    def add(self, item, price):\n        Cart.cart.append(price)\n\n    def total(self):\n        return sum(Cart.cart)\n\nclass TestCart(unittest.TestCase):\n    def setUp(self):\n        self.cart = Cart()\n        self.cart.add('tea', 3)\n\n    def test_starts_with_tea(self):\n        self.assertEqual(self.cart.total(), 3)\n\n    def test_adding_items(self):\n        self.cart.add('cup', 4)\n        self.assertEqual(self.cart.total(), 10)\n\nSUITE_TEST = TestCart"),
    ],
)

write_practice(
    M7, "m7-subtest-practice",
    "subTest Drills",
    "Parametrize a matrix of cases and report every failure.",
    "Luyện subTest",
    "Tham số hóa một ma trận ca và báo mọi lỗi.",
    L7B, 25, "intermediate",
    [
        challenge(
            "pi7-sub-matrix", "Case Matrix",
            "Implement is_leap(year) (divisible by 4, except centuries unless divisible by 400). Then write TestLeap using subTest over at least 6 year/expected pairs including 2000, 1900, 2024, 2023. Assign the class to SUITE_TEST.",
            "import unittest\n\ndef is_leap(year):\n    pass\n\nclass TestLeap(unittest.TestCase):\n    pass\n\nSUITE_TEST = None\n",
            [
                ("leap logic correct",
                 "assert is_leap(2000) is True\nassert is_leap(1900) is False\nassert is_leap(2024) is True\nassert is_leap(2023) is False",
                 "y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)."),
                ("subTest structure",
                 "import unittest, inspect\nsrc = inspect.getsource(SUITE_TEST)\nassert 'subTest' in src\nassert src.count('self.subTest') >= 1",
                 "The test body must use self.subTest in a loop."),
                ("at least 6 cases and all pass",
                 "import unittest, io\nsuite = unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST)\nresult = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)\nassert result.wasSuccessful(), 'leap tests failed'\nassert result.testsRun >= 1",
                 "Six+ cases including the four anchor years."),
            ],
            level="guided",
        ),
        challenge(
            "pi7-sub-edges", "Edge-Case Sweep",
            "Implement clamp(value, low, high) returning value bounded into [low, high]. Write TestClamp with subTest sweeping: below range, above range, at each boundary, and equal low==high. Assign to SUITE_TEST.",
            "import unittest\n\ndef clamp(value, low, high):\n    pass\n\nclass TestClamp(unittest.TestCase):\n    pass\n\nSUITE_TEST = None\n",
            [
                ("clamps correctly",
                 "assert clamp(-5, 0, 10) == 0\nassert clamp(15, 0, 10) == 10\nassert clamp(5, 0, 10) == 5\nassert clamp(0, 0, 10) == 0\nassert clamp(7, 7, 7) == 7",
                 "Boundaries are inclusive on both ends."),
                ("boundary sweep present",
                 "import inspect\nsrc = inspect.getsource(SUITE_TEST)\nassert src.count('subTest') >= 1 and src.count('test_') >= 1",
                 "One parametrized test covering all five behaviors."),
                ("suite passes",
                 "import unittest, io\nresult = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\nassert result.wasSuccessful(), 'clamp tests failed'",
                 "All swept cases green."),
            ],
            level="independent",
        ),
    ],
    {
        "pi7-sub-matrix": vi_challenge("Ma trận ca kiểm thử", "Viết is_leap(year) (chia hết cho 4, trừ năm tròn thế kỷ trừ khi chia hết cho 400). Sau đó viết TestLeap dùng subTest với ít nhất 6 cặp year/expected gồm cả 2000, 1900, 2024, 2023. Gán lớp vào SUITE_TEST.", [("Logic năm nhuận đúng", "y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)."), ("Cấu trúc subTest", "Thân test phải dùng self.subTest trong một vòng lặp."), ("Ít nhất 6 ca và tất cả pass", "Sáu+ ca gồm cả bốn năm mốc.")]),
        "pi7-sub-edges": vi_challenge("Quét ca biên", "Viết clamp(value, low, high) trả về value bị chặn trong [low, high]. Viết TestClamp với subTest quét: dưới dải, trên dải, tại từng biên, và low==high. Gán vào SUITE_TEST.", [("Chặn đúng", "Hai biên đều bao gồm."), ("Có quét biên", "Một test tham số hóa phủ cả năm hành vi."), ("Suite pass", "Mọi ca quét đều xanh.")]),
    },
    solutions=[
        ("pi7-sub-matrix", "import unittest\n\ndef is_leap(year):\n    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n\nclass TestLeap(unittest.TestCase):\n    def test_years(self):\n        cases = [(2000, True), (1900, False), (2024, True), (2023, False), (4, True), (100, False)]\n        for year, expected in cases:\n            with self.subTest(year=year):\n                self.assertEqual(is_leap(year), expected)\n\nSUITE_TEST = TestLeap", "import unittest\n\ndef is_leap(year):\n    return year % 4 == 0\n\nclass TestLeap(unittest.TestCase):\n    def test_years(self):\n        cases = [(2000, True), (1900, False), (2024, True), (2023, False), (4, True), (100, False)]\n        for year, expected in cases:\n            with self.subTest(year=year):\n                self.assertEqual(is_leap(year), expected)\n\nSUITE_TEST = TestLeap"),
        ("pi7-sub-edges", "import unittest\n\ndef clamp(value, low, high):\n    return max(low, min(high, value))\n\nclass TestClamp(unittest.TestCase):\n    def test_clamp(self):\n        cases = [(-5, 0, 10, 0), (15, 0, 10, 10), (5, 0, 10, 5), (0, 0, 10, 0), (7, 7, 7, 7)]\n        for value, low, high, expected in cases:\n            with self.subTest(value=value):\n                self.assertEqual(clamp(value, low, high), expected)\n\nSUITE_TEST = TestClamp", "import unittest\n\ndef clamp(value, low, high):\n    if value < low:\n        return low\n    if value > high:\n        return low\n    return value\n\nclass TestClamp(unittest.TestCase):\n    def test_clamp(self):\n        cases = [(-5, 0, 10, 0), (15, 0, 10, 10), (5, 0, 10, 5), (0, 0, 10, 0), (7, 7, 7, 7)]\n        for value, low, high, expected in cases:\n            with self.subTest(value=value):\n                self.assertEqual(clamp(value, low, high), expected)\n\nSUITE_TEST = TestClamp"),
    ],
)

write_practice(
    M7, "m7-mock-practice",
    "Mock Drills",
    "Patch collaborators and assert interactions.",
    "Luyện Mock",
    "Patch các collaborator và assert tương tác.",
    L7C, 30, "intermediate",
    [
        challenge(
            "pi7-mock-clock", "Freeze the Clock",
            "Implement greeting(name, now=None) returning 'Good morning, <name>!' for hours 5-11, 'Good afternoon' for 12-17, 'Good evening' otherwise. now is a datetime; default to datetime.now(). Then write TestGreeting that patches the clock (patch the module-level datetime or inject fixed datetimes via now=) to test all three bands. Assign to SUITE_TEST.",
            "import unittest\nfrom datetime import datetime\n\ndef greeting(name, now=None):\n    pass\n\nclass TestGreeting(unittest.TestCase):\n    pass\n\nSUITE_TEST = None\n",
            [
                ("bands work with injected times",
                 "from datetime import datetime\nassert greeting('An', datetime(2026, 1, 1, 8)) == 'Good morning, An!'\nassert greeting('An', datetime(2026, 1, 1, 14)) == 'Good afternoon, An!'\nassert greeting('An', datetime(2026, 1, 1, 22)) == 'Good evening, An!'",
                 "Branch on now.hour when now is provided."),
                ("default path uses real clock",
                 "g = greeting('An')\nassert g.startswith(('Good morning', 'Good afternoon', 'Good evening'))",
                 "now=None must fall back to datetime.now()."),
                ("all three bands tested",
                 "import inspect\nsrc = inspect.getsource(SUITE_TEST)\nassert src.count('Good') >= 3",
                 "Each band needs its own asserted case."),
            ],
            level="guided",
        ),
        challenge(
            "pi7-mock-api", "Fake the API",
            "Implement fetch_json(url, opener=None): opener defaults to a real-ish callable; the function calls opener(url) expecting an object with .read() returning bytes of JSON, and returns the parsed dict. Write TestFetch using unittest.mock to pass a fake opener returning b'{\"ok\": true}' and assert the parsed result AND that the fake was called exactly once with the URL. Assign to SUITE_TEST.",
            "import unittest\nimport json\n\ndef fetch_json(url, opener=None):\n    pass\n\nclass TestFetch(unittest.TestCase):\n    pass\n\nSUITE_TEST = None\n",
            [
                ("parses the fake payload",
                 "from unittest.mock import Mock\nfake = Mock()\nfake.read.return_value = b'{\"ok\": true}'\nassert fetch_json('http://x', opener=lambda u: fake) == {'ok': True}",
                 "read() bytes → json.loads → dict."),
                ("opener called once with the url",
                 "from unittest.mock import Mock\ncalls = []\ndef rec(u):\n    calls.append(u)\n    class R:\n        def read(self):\n            return b'{}'\n    return R()\nfetch_json('http://y', opener=rec)\nassert calls == ['http://y']",
                 "The transport receives exactly the URL passed."),
                ("test uses mocking and passes",
                 "import unittest, io, inspect\nsrc = inspect.getsource(SUITE_TEST)\nassert 'mock' in src.lower() or 'Mock' in src\nresult = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\nassert result.wasSuccessful(), 'fetch tests failed'",
                 "Your suite must use a Mock and stay green."),
            ],
            level="combination",
        ),
    ],
    {
        "pi7-mock-clock": vi_challenge("Đóng băng Đồng hồ", "Viết greeting(name, now=None) trả về 'Good morning, <name>!' cho giờ 5-11, 'Good afternoon' cho 12-17, 'Good evening' với các giờ khác. now là một datetime; mặc định là datetime.now(). Sau đó viết TestGreeting đóng băng đồng hồ (patch module-level datetime hoặc truyền datetime cố định qua now=) để test cả ba dải. Gán vào SUITE_TEST.", [("Ba dải hoạt động với giờ truyền vào", "Rẽ nhánh theo now.hour khi now được cung cấp."), ("Đường mặc định dùng đồng hồ thật", "now=None phải rơi về datetime.now()."), ("Cả ba dải đều được test", "Mỗi dải cần một ca được assert riêng.")]),
        "pi7-mock-api": vi_challenge("Giả lập API", "Viết fetch_json(url, opener=None): opener mặc định là callable thật; hàm gọi opener(url) kỳ vọng đối tượng có .read() trả bytes của JSON, và trả về dict đã parse. Viết TestFetch dùng unittest.mock truyền một fake opener trả b'{\"ok\": true}' và assert kết quả parse VÀ fake được gọi đúng một lần với URL. Gán vào SUITE_TEST.", [("Parse payload giả", "read() bytes → json.loads → dict."), ("Opener được gọi một lần với url", "Transport nhận đúng URL được truyền."), ("Test dùng mocking và pass", "Suite của bạn phải dùng Mock và giữ màu xanh.")]),
    },
    solutions=[
        ("pi7-mock-clock", "import unittest\nfrom datetime import datetime\n\ndef greeting(name, now=None):\n    hour = now.hour if now is not None else datetime.now().hour\n    if 5 <= hour <= 11:\n        part = 'Good morning'\n    elif 12 <= hour <= 17:\n        part = 'Good afternoon'\n    else:\n        part = 'Good evening'\n    return f'{part}, {name}!'\n\nclass TestGreeting(unittest.TestCase):\n    def test_morning(self):\n        self.assertEqual(greeting('An', datetime(2026, 1, 1, 8)), 'Good morning, An!')\n\n    def test_afternoon(self):\n        self.assertEqual(greeting('An', datetime(2026, 1, 1, 14)), 'Good afternoon, An!')\n\n    def test_evening(self):\n        self.assertEqual(greeting('An', datetime(2026, 1, 1, 22)), 'Good evening, An!')\n\nSUITE_TEST = TestGreeting", "import unittest\nfrom datetime import datetime\n\ndef greeting(name, now=None):\n    hour = now.hour if now else datetime.now().hour\n    if hour < 12:\n        part = 'Good morning'\n    elif hour < 18:\n        part = 'Good afternoon'\n    else:\n        part = 'Good evening'\n    return f'{part}, {name}!'\n\nclass TestGreeting(unittest.TestCase):\n    def test_morning(self):\n        self.assertEqual(greeting('An', datetime(2026, 1, 1, 8)), 'Good morning, An!')\n\n    def test_afternoon(self):\n        self.assertEqual(greeting('An', datetime(2026, 1, 1, 14)), 'Good afternoon, An!')\n\n    def test_evening(self):\n        self.assertEqual(greeting('An', datetime(2026, 1, 1, 22)), 'Good evening, An!')\n\nSUITE_TEST = TestGreeting"),
        ("pi7-mock-api", "import unittest\nimport json\n\ndef fetch_json(url, opener=None):\n    if opener is None:\n        import urllib.request\n        opener = urllib.request.urlopen\n    return json.loads(opener(url).read())\n\nclass TestFetch(unittest.TestCase):\n    def test_parses_and_calls_once(self):\n        from unittest.mock import Mock\n        fake = Mock()\n        fake.read.return_value = b'{\"ok\": true}'\n        opener = Mock(return_value=fake)\n        self.assertEqual(fetch_json('http://x', opener=opener), {'ok': True})\n        opener.assert_called_once_with('http://x')\n\nSUITE_TEST = TestFetch", "import unittest\nimport json\n\ndef fetch_json(url, opener=None):\n    if opener is None:\n        import urllib.request\n        opener = urllib.request.urlopen\n    return json.loads(opener(url).read())\n\nclass TestFetch(unittest.TestCase):\n    def test_parses_and_calls_once(self):\n        from unittest.mock import Mock\n        fake = Mock()\n        fake.read.return_value = b'{\"ok\": true}'\n        opener = Mock(return_value=fake)\n        self.assertEqual(fetch_json('http://x', opener=opener), {'ok': True})\n        opener.assert_called_once_with('http://wrong')\n\nSUITE_TEST = TestFetch"),
    ],
)

# --- module 7 checkpoint ---
write_checkpoint(
    M7, L7D,
    "Checkpoint: Test-First Repair",
    "Diagnose a broken module through its failing tests — then fix it.",
    20,
    """
The most honest test of testing skill: a broken implementation and a good
suite. Read the failures, understand the contract the tests describe, and
repair the code — without touching the tests.

**Working with AI:** paste the failing test output and ask for *hypotheses
ranked by likelihood*, not for the fix. Then verify each hypothesis yourself.
""",
    "Checkpoint: Sửa lỗi theo hướng test",
    "Chẩn đoán một module hỏng qua các test đang fail — rồi sửa nó.",
    """
Thử thách trung thực nhất về kỹ năng kiểm thử: một bản cài đặt hỏng và một
bộ test tốt. Đọc các lỗi, hiểu hợp đồng mà test mô tả, và sửa code — không
đụng vào test.

**Làm việc cùng AI:** dán kết quả test fail và nhờ mentor đưa *các giả thuyết
xếp theo khả năng*, không phải lời giải. Sau đó tự xác minh từng giả thuyết.
""",
    challenge(
        "pi7-ckpt-repair", "Repair the Stack",
        "The class Stack below has THREE bugs: pop on empty must raise IndexError (it returns None), peek must not remove the item (it does), and size must reflect the count (it miscounts). Fix the class so all behaviors hold. Do not rename anything.",
        "class Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        return self._items.pop() if self._items else None\n\n    def peek(self):\n        return self._items.pop()\n\n    def size(self):\n        return len(self._items) + 1\n",
        [
            ("pop empty raises IndexError",
             "s = Stack()\ntry:\n    s.pop()\n    failed = False\nexcept IndexError:\n    failed = True\nassert failed",
             "Guard the empty case: raise IndexError, never return None."),
            ("peek does not remove",
             "s = Stack()\ns.push('x')\nassert s.peek() == 'x'\nassert s.size() == 1",
             "peek reads the last item without popping."),
            ("size is accurate",
             "s = Stack()\ns.push(1); s.push(2); s.pop()\nassert s.size() == 1",
             "len(self._items) — no fudge factors."),
            ("full lifecycle",
             "s = Stack()\ns.push('a'); s.push('b')\nassert s.pop() == 'b' and s.peek() == 'a' and s.size() == 1",
             "LIFO order preserved end to end."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Sửa lại Stack",
        "Lớp Stack dưới đây có BA lỗi: pop trên stack rỗng phải raise IndexError (hiện trả về None), peek không được xóa phần tử (hiện có xóa), và size phải phản ánh đúng số phần tử (hiện đếm sai). Sửa lớp để mọi hành vi trên đều đúng. Không được đổi tên bất cứ thứ gì.",
        [
            ("pop khi rỗng raise IndexError", "Chặn ca rỗng: raise IndexError, không bao giờ trả None."),
            ("peek không xóa", "peek đọc phần tử cuối mà không pop."),
            ("size chính xác", "len(self._items) — không hệ số cộng trừ tùy tiện."),
            ("Toàn bộ vòng đời", "Trật tự LIFO được giữ từ đầu đến cuối."),
        ],
    ),
    solution="class Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        if not self._items:\n            raise IndexError('pop from empty stack')\n        return self._items.pop()\n\n    def peek(self):\n        if not self._items:\n            raise IndexError('peek from empty stack')\n        return self._items[-1]\n\n    def size(self):\n        return len(self._items)",
    wrong="class Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        if not self._items:\n            raise IndexError('pop from empty stack')\n        return self._items.pop()\n\n    def peek(self):\n        if not self._items:\n            raise IndexError('peek from empty stack')\n        return self._items.pop()\n\n    def size(self):\n        return len(self._items)",
)

print("module 7 done")
