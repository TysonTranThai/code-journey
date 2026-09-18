#!/usr/bin/env python3
"""Module 12: testing-and-code-quality — lessons + practices."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge

MOD = "testing-and-code-quality"

# ── Lessons ──────────────────────────────────────────────────────────────────
L1 = """
**assert** states what must be true — Python checks it for you:

```python
total = 245
assert total > 0, "total must be positive"
```

If the condition holds, nothing happens. If not, an `AssertionError` with your
message crashes the program AT THE LIE, not three steps later.

That idea scales into automated tests. You already used asserts as a learner;
writing them yourself flips the perspective:

```python
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

test_add()          # silent = passing; loud = a bug with an address
```

A test suite is a list of functions like this that anyone can re-run. Silent
output is the sound of confidence.
"""

L1_VI = """
**assert** phát biểu điều gì phải đúng — Python kiểm tra giúp bạn:

```python
total = 245
assert total > 0, "total must be positive"
```

Nếu điều kiện đúng, không có gì xảy ra. Nếu không, một `AssertionError` với
thông điệp của bạn làm sập chương trình NGAY TẠI NƠI NÓI DỐI, không phải ba bước
sau đó.

Ý tưởng đó mở rộng thành kiểm thử tự động. Bạn đã dùng assert với tư cách người
học; tự viết chúng sẽ lật ngược góc nhìn:

```python
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

test_add()          # im lặng = đang đạt; ồn ào = một bug có địa chỉ
```

Một bộ kiểm thử là danh sách các hàm như thế mà bất kỳ ai cũng có thể chạy lại.
Đầu ra im lặng chính là âm thanh của sự tự tin.
"""

L2 = """
Two habits separate throwaway tests from trustworthy ones.

## Test the edges, not just the happy path

```python
def test_grade():
    assert letter_grade(90) == "A"    # the boundary
    assert letter_grade(89.9) == "B"  # just below it — bugs live here
    assert letter_grade(150) == "A"   # nonsense input, defined behavior
```

Bugs cluster at boundaries: zero, empty, one-past-the-end, the day the discount
starts. Happy-path-only tests are passports that wave everything through.

## A failing test must fail for the RIGHT reason

Before celebrating a test that fails, read the error. Is it failing because the
code is wrong, or because the test itself is wrong? A test suite nobody trusts
is worse than no suite — it prints false alarms until people stop listening.
"""

L2_VI = """
Hai thói quen phân biệt kiểm thử vứt đi với kiểm thử đáng tin.

## Kiểm tra biên, không chỉ đường vui

```python
def test_grade():
    assert letter_grade(90) == "A"    # biên
    assert letter_grade(89.9) == "B"  # ngay dưới nó — bug cư ngụ đây
    assert letter_grade(150) == "A"   # đầu vào vô lý, hành vi được định nghĩa
```

Bug tụ tập ở biên: không, rỗng, vượt-một-đơn-vị, ngày giảm giá bắt đầu. Kiểm
thử chỉ có đường vui là hộ chiếu giơ tay cho mọi thứ đi qua.

## Một bài kiểm thử thất bại phải thất bại vì ĐÚNG lý do

Trước khi ăn mừng một bài kiểm thử đang lỗi, hãy đọc lỗi đó. Nó lỗi vì mã sai,
hay vì chính bài kiểm thử sai? Một bộ kiểm thử mà không ai tin còn tệ hơn không
có — nó báo động giả đến khi mọi người ngừng lắng nghe.
"""

L3 = """
Readable code is debuggable code. The rules are few and earned:

- **Names carry the design.** `retry_count` beats `n`; `is_valid_order(order)`
  beats `if o[2] == 1 and len(o) > 5`.
- **Small functions.** One screen, one job. If you need "and" to describe what a
  function does, it is two functions.
- **No magic numbers.** `if score >= 90:` — what is 90? `GRADE_A_CUTOFF = 90`
  documents itself.
- **Comments explain WHY, not what.** `# skip header row` teaches; `# add 1`
  repeats.

```python
def letter_grade(score):
    if score >= GRADE_A_CUTOFF:
        return "A"
    ...
```

These habits cost seconds while writing and save hours while debugging — the
compound interest of craftsmanship.
"""

L3_VI = """
Mã dễ đọc là mã dễ gỡ. Quy tắc ít nhưng đáng giá:

- **Tên biến mang thiết kế.** `retry_count` đánh bại `n`; `is_valid_order(order)`
  đánh bại `if o[2] == 1 and len(o) > 5`.
- **Hàm nhỏ.** Một màn hình, một việc. Nếu cần từ "và" để mô tả hàm làm gì, đó
  là hai hàm.
- **Không con số thần thánh.** `if score >= 90:` — 90 là gì? `GRADE_A_CUTOFF = 90`
  tự giải thích.
- **Chú thích giải thích VÌ SAO, không phải cái gì.** `# bỏ qua dòng tiêu đề`
  dạy điều; `# cộng 1` lặp lại vô ích.

```python
def letter_grade(score):
    if score >= GRADE_A_CUTOFF:
        return "A"
    ...
```

Những thói quen này tốn vài giây khi viết và tiết kiệm hàng giờ khi gỡ — lãi
kép của nghề.
"""

# ── Practices ────────────────────────────────────────────────────────────────
write_practice(
    MOD, "m12-assert-practice",
    "Assertions & Make-the-Tests-Pass",
    "Raise informative errors; satisfy boundary-hitting test suites.",
    "Assert & biến bài kiểm thử thành đạt",
    "Raise lỗi giàu thông tin; làm đạt các bộ kiểm thử đánh trúng biên.",
    "assertions", 30, "beginner",
    [
        challenge(
            "py-test-validate-age",
            "Assert with a Message",
            "Write validate_age(age): raise AssertionError('age must be an int') when age is not an int (booleans are NOT ints here), AssertionError('age out of range') when outside 0..150, and return the string ok otherwise.",
            "",
            [("asserts fire correctly", 'assert validate_age(30) == "ok"\ntry:\n    validate_age("30")\n    _ok = False\nexcept AssertionError as e:\n    _ok = True\n    assert "int" in str(e), f"message must mention int, got {e}"\nassert _ok, "str must raise AssertionError"\n\n_raised = False\ntry:\n    validate_age(True)\nexcept AssertionError:\n    _raised = True\nassert _raised, "bool must raise (bool is not an int here)"\n\ntry:\n    validate_age(200)\n    _ok2 = False\nexcept AssertionError as e:\n    _ok2 = True\n    assert "range" in str(e), f"message must mention range, got {e}"\nassert _ok2, "200 must raise AssertionError"',
              "isinstance(age, bool) check FIRST (bool is a subclass of int!), then isinstance(age, int), then 0 <= age <= 150.")],
            level="guided",
        ),
        challenge(
            "py-test-normalize-phone",
            "Make the Tests Pass: Phone",
            "Implement normalize_phone(raw) so the hidden test suite passes: keep only digits, but keep a leading + if present.",
            "",
            [("suite passes", 'cases = [("+84 901-234-567", "+84901234567"), ("(028) 38-22-77", "028382277"), ("123", "123")]\nfor raw, want in cases:\n    got = normalize_phone(raw)\n    assert got == want, f"normalize_phone({raw!r}) = {got!r}, want {want!r}"\nassert normalize_phone("no digits") == "", "no digits -> empty string"',
              "keep str digits; if the original starts with '+', prefix the result.")],
            level="guided",
        ),
        challenge(
            "py-test-grade-boundary",
            "Make the Tests Pass: Boundaries",
            "Implement letter_grade(score): A >= 90, B >= 80, C >= 70, D >= 60, else F. The suite attacks the boundaries.",
            "",
            [("boundaries hold", 'for score, want in [(90, "A"), (89.9, "B"), (80, "B"), (79.5, "C"), (70, "C"), (60, "D"), (59.99, "F"), (150, "A")]:\n    got = letter_grade(score)\n    assert got == want, f"letter_grade({score}) = {got!r}, want {want!r}"',
              "Descending elif chain with >= — 89.9 must fall through to B.")],
            level="guided",
        ),
    ],
    {
        "py-test-validate-age": vi_challenge("Assert kèm thông điệp", "Viết validate_age(age): raise AssertionError('age must be an int') khi age không phải int (boolean KHÔNG tính là int ở đây), AssertionError('age out of range') khi ngoài 0..150, và trả về chuỗi ok trong trường hợp khác.",
                                        [("assert phát đúng lúc", "isinstance(age, bool) kiểm tra TRƯỚC (bool là lớp con của int!), rồi isinstance(age, int), rồi 0 <= age <= 150.")]),
        "py-test-normalize-phone": vi_challenge("Biến bài kiểm thử thành đạt: Điện thoại", "Cài đặt normalize_phone(raw) để bộ kiểm thử ẩn đạt: chỉ giữ chữ số, nhưng giữ dấu + đầu nếu có.",
                                        [("bộ kiểm thử đạt", "giữ các ký tự chữ số; nếu chuỗi gốc bắt đầu bằng '+', thêm tiền tố vào kết quả.")]),
        "py-test-grade-boundary": vi_challenge("Biến bài kiểm thử thành đạt: Biên", "Cài đặt letter_grade(score): A >= 90, B >= 80, C >= 70, D >= 60, còn lại F. Bộ kiểm thử tấn công các biên.",
                                        [("biên được giữ vững", "Chuỗi elif giảm dần với >= — 89.9 phải rơi xuống B.")]),
    },
    solutions=[
        ("py-test-validate-age", 'def validate_age(age):\n    if isinstance(age, bool) or not isinstance(age, int):\n        raise AssertionError("age must be an int")\n    if not (0 <= age <= 150):\n        raise AssertionError("age out of range")\n    return "ok"',
         'def validate_age(age):\n    if not isinstance(age, int):\n        raise AssertionError("age must be an int")\n    if not (0 <= age <= 150):\n        raise AssertionError("age out of range")\n    return "ok"'),
        ("py-test-normalize-phone", 'def normalize_phone(raw):\n    digits = "".join(ch for ch in raw if ch.isdigit())\n    if raw.startswith("+"):\n        return "+" + digits\n    return digits',
         'def normalize_phone(raw):\n    digits = "".join(ch for ch in raw if ch.isdigit())\n    if "+" in raw:\n        return "+" + digits'),
        ("py-test-grade-boundary", 'def letter_grade(score):\n    if score >= 90:\n        return "A"\n    if score >= 80:\n        return "B"\n    if score >= 70:\n        return "C"\n    if score >= 60:\n        return "D"\n    return "F"',
         'def letter_grade(score):\n    if score > 90:\n        return "A"\n    if score >= 80:\n        return "B"\n    if score >= 70:\n        return "C"\n    if score >= 60:\n        return "D"\n    return "F"'),
    ],
)

write_practice(
    MOD, "m12-write-tests-practice",
    "Write Your Own Tests",
    "Become the test author — catch the broken implementation.",
    "Tự viết bài kiểm thử của bạn",
    "Trở thành tác giả kiểm thử — bắt được bản cài đặt hỏng.",
    "basic-automated-tests", 35, "beginner",
    [
        challenge(
            "py-test-write-tests",
            "Test the Palindrome",
            "Write test_palindrome(fn) that receives a palindrome checker and RETURNS a list of failure-message strings (empty list = your tests all passed). Your tests must cover: 'radar' -> True, 'Racecar' -> True (case-insensitive), 'hello' -> False, '' -> True. The grader runs your tests against a correct AND a subtly broken implementation — both must be caught appropriately.",
            "",
            [("your tests judge correctly", 'def _ok(s):\n    s = s.lower()\n    return s == s[::-1]\n\ndef _broken(s):\n    s = s.lower()\n    return s == s[::-1] and len(s) > 0\n\nassert test_palindrome(_ok) == [], f"correct impl must pass your tests, got {test_palindrome(_ok)}"\n_fails = test_palindrome(_broken)\nassert len(_fails) >= 1, "your tests must catch the broken impl (empty string)"\nassert all(isinstance(f, str) for f in _fails), "failures are message strings"',
              "call fn(...) inside try/except AssertionError, or assert and collect — return the list of what failed.")],
            level="mini-build",
        ),
        challenge(
            "py-test-report-runner",
            "Mini Build: Test Report Runner",
            'Write run_suite(cases) — cases is a list of (label, callable, expected). For each, call it with NO arguments, compare to expected, and RETURN a dict {"passed": n, "failed": m, "failures": [labels of failed cases in order]}.',
            "",
            [("report computed", 'cases = [\n    ("add ok", lambda: 2 + 2, 4),\n    ("bad math", lambda: 2 + 2, 5),\n    ("upper ok", lambda: "ok".upper(), "OK"),\n]\nr = run_suite(cases)\nassert r == {"passed": 2, "failed": 1, "failures": ["bad math"]}, f"got {r}"\nassert run_suite([]) == {"passed": 0, "failed": 0, "failures": []}, "empty suite"',
              "loop, call the callable, compare, accumulate — failures keep their order.")],
            level="mini-build",
        ),
    ],
    {
        "py-test-write-tests": vi_challenge("Kiểm thử palindrome", "Viết test_palindrome(fn) nhận một hàm kiểm tra palindrome và TRẢ VỀ danh sách các thông điệp thất bại (danh sách rỗng = tất cả bài kiểm thử của bạn đạt). Bài kiểm thử của bạn phải phủ: 'radar' -> True, 'Racecar' -> True (không phân biệt hoa thường), 'hello' -> False, '' -> True. Bộ chấm chạy bài kiểm thử của bạn với một bản cài đúng VÀ một bản hỏng tinh vi — cả hai phải được xử lý đúng.",
                                        [("bài kiểm thử của bạn phán đúng", "gọi fn(...) trong try/except AssertionError, hoặc assert và ghi nhận — trả về danh sách cái gì đã lỗi.")]),
        "py-test-report-runner": vi_challenge('Mini build: Bộ chạy báo cáo kiểm thử', 'Viết run_suite(cases) — cases là danh sách (nhãn, hàm_gọi, kỳ_vọng). Với mỗi mục, gọi hàm KHÔNG tham số, so với kỳ vọng, và TRẢ VỀ dict {"passed": n, "failed": m, "failures": [nhãn các mục lỗi theo thứ tự]}.',
                                        [("báo cáo được tính", "duyệt, gọi hàm, so sánh, tích lũy — failures giữ nguyên thứ tự.")]),
    },
    solutions=[
        ("py-test-write-tests", 'def test_palindrome(fn):\n    failures = []\n    cases = [("radar", True), ("Racecar", True), ("hello", False), ("", True)]\n    for text, want in cases:\n        try:\n            got = fn(text)\n            if got != want:\n                failures.append(f"palindrome({text!r}) = {got!r}, want {want!r}")\n        except Exception as e:\n            failures.append(f"palindrome({text!r}) raised {e!r}")\n    return failures',
         'def test_palindrome(fn):\n    failures = []\n    cases = [("radar", True), ("Racecar", True), ("hello", False)]\n    for text, want in cases:\n        got = fn(text)\n        if got != want:\n            failures.append(f"palindrome({text!r}) = {got!r}")\n    return failures'),
        ("py-test-report-runner", 'def run_suite(cases):\n    passed = 0\n    failures = []\n    for label, thunk, expected in cases:\n        if thunk() == expected:\n            passed += 1\n        else:\n            failures.append(label)\n    return {"passed": passed, "failed": len(failures), "failures": failures}',
         'def run_suite(cases):\n    passed = 0\n    failures = []\n    for label, thunk, expected in cases:\n        if thunk() != expected:\n            passed += 1\n            failures.append(label)\n    return {"passed": passed, "failed": len(failures), "failures": failures}'),
    ],
)

print("module 12 content written")
