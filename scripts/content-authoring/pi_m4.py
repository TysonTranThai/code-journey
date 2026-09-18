#!/usr/bin/env python3
"""Python Intermediate — module 4 (structure-and-typing)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

M4 = "structure-and-typing"
L4A = "modules-packages"
L4B = "package-layout"
L4C = "typing-essentials"
L4D = "typing-protocols"
L4E = "checkpoint-typed-app"

write_module(
    M4,
    "Structure and Typing",
    "Grow from scripts to packages, and annotate public APIs with modern typing.",
    "Cấu trúc và Typing",
    "Phát triển từ script sang package, và chú thích API công khai bằng typing hiện đại.",
    [L4A, L4B, L4C, L4D, L4E],
    ["m4-pkg-practice", "m4-typing-practice", "m4-protocol-practice"],
)

write_lesson(
    M4, L4A,
    "Modules and Imports",
    "How import really resolves, the __main__ guard, and avoiding circular imports.",
    14,
    """
A **module** is any `.py` file; `import` finds it on `sys.path`, executes it
**once**, and caches it in `sys.modules`:

```python
# pricing.py
DISCOUNT = 0.1            # module-level constant: UPPER_CASE

def apply(price):
    return price * (1 - DISCOUNT)
```

```python
from pricing import apply     # import the function, not the module
import pricing                # import the module; use pricing.apply
```

Two rules keep imports sane:

- **`from x import y` for names you use constantly; plain `import x` when the module gives context** (`csv.reader` reads better than a bare `reader`).
- **Never do `from x import *`** — it pollutes the namespace and defeats searchability.

## The __main__ guard

Code that should run only when a file is executed directly — not when
imported — belongs under the guard:

```python
def main():
    print("report generated")

if __name__ == "__main__":    # true only for direct execution
    main()
```

This is what makes a file both a **reusable module and a runnable script**.
Importers get the functions; nobody accidentally triggers side effects.

## Circular imports: the smell and the fix

If `a.py` imports `b` while `b` imports `a`, one of them receives a
half-built module. The real fix is almost always **structure**: pull the
shared thing (a type, a constant, a helper) into a third module both can
import. Cycles are a design complaint, not a loading-order puzzle.
""",
    "Module và Import",
    "import thực sự phân giải thế nào, __main__ guard, và tránh circular import.",
    """
**Module** là bất kỳ tệp `.py` nào; `import` tìm nó trên `sys.path`, chạy nó
**một lần duy nhất**, và lưu cache vào `sys.modules`:

```python
# pricing.py
DISCOUNT = 0.1            # hằng mức module: UPPER_CASE

def apply(price):
    return price * (1 - DISCOUNT)
```

```python
from pricing import apply     # import hàm, không phải module
import pricing                # import module; dùng pricing.apply
```

Hai quy tắc giữ import trong lành:

- **`from x import y` cho tên dùng liên tục; `import x` thường khi module tạo ngữ cảnh** (`csv.reader` đọc rõ hơn `reader` trần trụi).
- **Không bao giờ `from x import *`** — nó làm ô nhiễm namespace và phá khả năng tìm kiếm.

## __main__ guard

Code chỉ nên chạy khi tệp được chạy trực tiếp — không phải khi bị import —
đặt dưới guard:

```python
def main():
    print("report generated")

if __name__ == "__main__":    # chỉ đúng khi chạy trực tiếp
    main()
```

Điều này khiến một tệp vừa là **module tái sử dụng** vừa là **script chạy
được**. Người import nhận các hàm; không ai vô tình kích hoạt hiệu ứng phụ.

## Circular import: mùi và cách sửa

Nếu `a.py` import `b` trong khi `b` import `a`, một bên sẽ nhận được module
dở dang. Cách sửa đúng gần như luôn là **cấu trúc**: kéo phần dùng chung (một
kiểu, một hằng, một helper) ra module thứ ba để cả hai import. Vòng lặp là
lời phê bình thiết kế, không phải câu đố thứ tự nạp.
""",
)

write_lesson(
    M4, L4B,
    "Packages and Project Layout",
    "__init__.py, src/ layout, and where code lives as a project grows.",
    13,
    """
A **package** is a directory of modules (historically one containing
`__init__.py`). Packages give you dotted names and a place for shared setup:

```python
# tasknoter/
#   pyproject.toml
#   src/
#     tasknoter/
#       __init__.py        # makes 'tasknoter' a package
#       storage.py
#       cli.py

from tasknoter.storage import load_tasks
```

The **src/ layout** (a package directory inside `src/`) is the packaging
community's recommendation: it makes it impossible to accidentally import
the local copy instead of the installed one, because tests run against the
installed package.

## Layering a growing application

Professional Python codebases tend to separate three concerns:

- **domain** — the data and rules (`Task`, `complete()`, validation). Knows nothing about IO.
- **storage** — saving/loading (files, sqlite). Talks to the domain.
- **interface** — CLI or web handlers. Talks to both, contains no business rules.

Arrows point one way: `interface → domain ← storage`. The moment your CLI
function contains SQL and validation in the same 100 lines, tests get hard
and changes get risky. Layering is what makes module 7's testing and the
capstone enjoyable instead of painful.

## Absolute vs relative imports

Inside a package prefer **absolute** imports (`from tasknoter.storage import
load`). Relative imports (`from .storage import load`) work too but are a
frequent source of confusion when files move. Pick absolute by default.
""",
    "Package và Bố cục Dự án",
    "__init__.py, bố cục src/, và code sống ở đâu khi dự án lớn lên.",
    """
**Package** là một thư mục các module (truyền thống phải có `__init__.py`).
Package cho bạn tên dạng chấm và chỗ đặt cấu hình chung:

```python
# tasknoter/
#   pyproject.toml
#   src/
#     tasknoter/
#       __init__.py        # biến 'tasknoter' thành package
#       storage.py
#       cli.py

from tasknoter.storage import load_tasks
```

**Bố cục src/** (thư mục package nằm trong `src/`) là khuyến nghị của cộng
đồng packaging: nó khiến việc vô tình import bản local thay vì bản đã cài trở
nên bất khả thi, vì test chạy trên package đã cài.

## Phân tầng ứng dụng lớn dần

Codebase Python chuyên nghiệp thường tách ba mối quan tâm:

- **domain** — dữ liệu và quy tắc (`Task`, `complete()`, kiểm tra hợp lệ). Không biết gì về IO.
- **storage** — lưu/nạp (tệp, sqlite). Nói chuyện với domain.
- **interface** — CLI hoặc web handler. Nói chuyện với cả hai, không chứa business rule.

Mũi tên đi một chiều: `interface → domain ← storage`. Khoảnh khắc hàm CLI của
bạn chứa cả SQL và validation trong cùng 100 dòng, test trở nên khó khăn và
thay đổi trở nên rủi ro. Phân tầng là thứ khiến module 7 (testing) và capstone
dễ thở thay vì đau đầu.

## Absolute vs relative import

Trong package, ưu tiên **absolute** (`from tasknoter.storage import load`).
Relative import (`from .storage import load`) cũng hoạt động nhưng thường gây
rối khi tệp được di chuyển. Mặc định chọn absolute.
""",
)

write_lesson(
    M4, L4C,
    "Typing Essentials",
    "Annotate containers, unions, and literals — and why types are documentation that runs.",
    15,
    """
Type annotations describe **what a function consumes and returns**. They are
checked by external tools (mypy, pyright — run on your own machine), but they
cost nothing at runtime and serve three audiences at once: callers, editors,
and future-you.

```python
def average(values: list[float]) -> float:
    return sum(values) / len(values)

def find_user(user_id: int) -> dict | None:      # modern union (3.10+)
    ...

def set_level(level: Literal["debug", "info", "error"]) -> None:
    ...
```

## The vocabulary you need daily

- **Containers**: `list[str]`, `dict[str, int]`, `tuple[int, ...]` (variadic), `set[str]`.
- **Unions**: `int | None` replaces `Optional[int]`; `str | bytes` means exactly one of them.
- **`Any`** means "checked-free zone" — contagious and to be avoided; **`object`** means "any value, but handle it carefully".
- **`TypedDict`** types a dict's keys for when a dataclass is overkill (e.g., mirroring a JSON payload):

```python
from typing import TypedDict

class ProductDict(TypedDict):
    sku: str
    price: float
```

## Narrowing

Type checkers understand control flow — check a type and it narrows:

```python
def total(value: int | list[int]) -> int:
    if isinstance(value, list):
        return sum(value)        # here value: list[int]
    return value                 # here value: int
```

## Why annotate at all?

At three thousand lines, "what does this take?" stops being guessable.
Annotations catch real bugs before runtime (passing a `str` where seconds
were expected), make signatures searchable, and let editors autocomplete
correctly. You verify them here by **behavior and by `get_type_hints`
inspection**; on your own machine, run `mypy` for the full static check.
""",
    "Nền tảng Typing",
    "Chú thích container, union, literal — và vì sao type là tài liệu biết chạy.",
    """
Type annotation mô tả **hàm nhận gì và trả về gì**. Công cụ ngoài (mypy,
pyright — chạy trên máy của bạn) kiểm tra chúng, nhưng chúng không tốn chi phí
runtime và phục vụ ba đối tượng cùng lúc: người gọi, editor, và bạn của tương lai.

```python
def average(values: list[float]) -> float:
    return sum(values) / len(values)

def find_user(user_id: int) -> dict | None:      # union hiện đại (3.10+)
    ...

def set_level(level: Literal["debug", "info", "error"]) -> None:
    ...
```

## Từ vựng cần dùng hằng ngày

- **Container**: `list[str]`, `dict[str, int]`, `tuple[int, ...]` (biến đổi), `set[str]`.
- **Union**: `int | None` thay cho `Optional[int]`; `str | bytes` nghĩa là đúng một trong hai.
- **`Any`** nghĩa là "vùng miễn kiểm tra" — lây lan và nên tránh; **`object`** nghĩa là "bất kỳ giá trị nào, nhưng phải xử lý cẩn thận".
- **`TypedDict`** gán kiểu cho các key của dict khi dataclass là quá mức cần (ví dụ: phản chiếu payload JSON):

```python
from typing import TypedDict

class ProductDict(TypedDict):
    sku: str
    price: float
```

## Narrowing (thu hẹp kiểu)

Trình kiểm tra kiểu hiểu luồng điều khiển — kiểm tra kiểu rồi kiểu được thu hẹp:

```python
def total(value: int | list[int]) -> int:
    if isinstance(value, list):
        return sum(value)        # tại đây value: list[int]
    return value                 # tại đây value: int
```

## Vì sao phải chú thích?

Đến ba nghìn dòng, "hàm này nhận gì?" không còn đoán được. Annotation bắt lỗi
thật trước runtime (truyền `str` nơi kỳ vọng giây), giúp chữ ký tìm kiếm được,
và cho editor autocomplete đúng. Bạn kiểm chứng chúng ở đây bằng **hành vi và
qua `get_type_hints`**; trên máy riêng, chạy `mypy` để kiểm tra tĩnh đầy đủ.
""",
)

write_lesson(
    M4, L4D,
    "Protocols: Typing Duck Typing",
    "Structural interfaces with typing.Protocol — behavior over identity.",
    13,
    """
Module 2 ended with duck typing: anything with a `start()` works as an
engine. **`typing.Protocol`** gives that idea a name and type-checkable
shape — an interface matched *structurally*, not by inheritance:

```python
from typing import Protocol

class Storage(Protocol):
    def save(self, key: str, value: str) -> None: ...
    def load(self, key: str) -> str | None: ...

class MemoryStorage:                 # no inheritance from Storage!
    def __init__(self):
        self._data: dict[str, str] = {}

    def save(self, key: str, value: str) -> None:
        self._data[key] = value

    def load(self, key: str) -> str | None:
        return self._data.get(key)

def backup(store: Storage) -> None:      # accepts anything Storage-shaped
    store.save("backup", "2026-09-13")
```

`MemoryStorage` never mentions `Storage`, yet any type checker accepts it
where a `Storage` is expected — because it has the right **shape**. This is
structural typing, and it's how big Python codebases keep components swappable
without inheritance forests.

## When to write a Protocol

Write one when a **consumer** needs to promise a capability: "I need anything
that can `save`/`load`." The protocol lives with the consumer, not the
implementations — that keeps dependencies pointing the right way (module 4's
layering again). Reserve ABCs/inheritance for when you also want shared
implementation, not just shape.

## Runtime checking

Protocols are static by default; `isinstance` needs `@runtime_checkable` —
and even then it only checks method *names*. Design with protocols for the
type checker and humans; don't lean on runtime checks.
""",
    "Protocol: Gán kiểu cho duck typing",
    "Interface cấu trúc với typing.Protocol — hành vi hơn bản sắc.",
    """
Module 2 kết thúc bằng duck typing: cái gì có `start()` cũng dùng được như
engine. **`typing.Protocol`** đặt tên cho ý tưởng đó và cho nó hình dạng kiểm
được bằng type checker — một interface khớp theo **cấu trúc**, không phải qua
kế thừa:

```python
from typing import Protocol

class Storage(Protocol):
    def save(self, key: str, value: str) -> None: ...
    def load(self, key: str) -> str | None: ...

class MemoryStorage:                 # không kế thừa Storage!
    def __init__(self):
        self._data: dict[str, str] = {}

    def save(self, key: str, value: str) -> None:
        self._data[key] = value

    def load(self, key: str) -> str | None:
        return self._data.get(key)

def backup(store: Storage) -> None:      # nhận bất cứ thứ gì có hình Storage
    store.save("backup", "2026-09-13")
```

`MemoryStorage` chưa từng nhắc đến `Storage`, nhưng mọi type checker vẫn chấp
nhận nó nơi cần một `Storage` — vì nó có đúng **hình dạng**. Đó là structural
typing, và đó là cách các codebase Python lớn giữ các thành phần hoán đổi được
mà không cần rừng kế thừa.

## Khi nào viết một Protocol

Hãy viết khi một **bên tiêu thụ** cần hứa một năng lực: "tôi cần bất cứ thứ gì
`save`/`load` được." Protocol sống cùng bên tiêu thụ, không phải cùng các bản
cài đặt — điều đó giữ các phụ thuộc chỉ đúng chiều (lại là phân tầng của
module này). Dành ABC/kế thừa cho lúc bạn cần cả bản cài đặt dùng chung,
không chỉ hình dạng.

## Kiểm tra runtime

Protocol mặc định là tĩnh; `isinstance` cần `@runtime_checkable` — và kể cả
vậy nó chỉ kiểm tra **tên** method. Hãy thiết kế với protocol cho type checker
và con người; đừng dựa vào kiểm tra runtime.
""",
)

# --- module 4 practice sets ---
write_practice(
    M4, "m4-pkg-practice",
    "Import Discipline",
    "Write importable code: no import-time side effects, clean entry points.",
    "Kỷ luật Import",
    "Viết code import được: không hiệu ứng phụ lúc import, entry point sạch.",
    L4A, 25, "intermediate",
    [
        challenge(
            "pi4-pkg-main-guard", "Script or Module?",
            "Implement run_report() returning the string 'report'. Then implement the module-level pattern: a variable RAN_DIRECTLY set by the __main__ guard. Because the sandbox imports your code as a module, RAN_DIRECTLY must be False here — and run_report() must not print.",
            "RAN_DIRECTLY = None\n\ndef run_report():\n    pass\n\n# add the __main__ guard below\n",
            [
                ("run_report returns, does not print",
                 "import io, contextlib\nbuf = io.StringIO()\nwith contextlib.redirect_stdout(buf):\n    result = run_report()\nassert result == 'report'\nassert buf.getvalue() == ''",
                 "Return the string; printing would fail this test."),
                ("guard did not fire on import",
                 "assert RAN_DIRECTLY is False",
                 "if __name__ == '__main__': RAN_DIRECTLY = True — as an imported module, __name__ is not '__main__'."),
            ],
            level="guided",
        ),
        challenge(
            "pi4-pkg-namespace", "No Star Pollution",
            "Implement count_vowels(text) in a way that only defines the function and the constant VOWELS at module level. The grader checks that importing your code does NOT define the common name 'temp' — i.e., don't leak work variables to module scope.",
            "VOWELS = 'aeiou'\n\ndef count_vowels(text):\n    pass\n",
            [
                ("counts vowels",
                 "assert count_vowels('Hello World') == 3",
                 "Sum 1 for each char in VOWELS."),
                ("no leaked work variables",
                 "assert 'temp' not in dir() and 'result' not in dir()",
                 "Keep loop variables inside the function — module scope holds only VOWELS and count_vowels."),
                ("constant is at module level",
                 "assert VOWELS == 'aeiou'",
                 "The constant stays importable."),
            ],
            level="independent",
        ),
    ],
    {
        "pi4-pkg-main-guard": vi_challenge("Script hay Module?", "Viết run_report() trả về chuỗi 'report'. Sau đó cài mẫu module-level: biến RAN_DIRECTLY được gán bởi __main__ guard. Vì sandbox import code của bạn như một module, RAN_DIRECTLY phải là False ở đây — và run_report() không được print.", [("run_report trả về, không print", "Trả về chuỗi; print sẽ làm test này fail."), ("Guard không kích hoạt khi import", "if __name__ == '__main__': RAN_DIRECTLY = True — với vai trò module được import, __name__ không phải '__main__'.")]),
        "pi4-pkg-namespace": vi_challenge("Không ô nhiễm namespace", "Viết count_vowels(text) sao cho ở mức module chỉ định nghĩa hàm và hằng VOWELS. Trình chấm kiểm tra rằng import code của bạn KHÔNG định nghĩa biến thường dùng 'temp' — tức là không rò rỉ biến làm việc ra module scope.", [("Đếm nguyên âm", "Cộng 1 cho mỗi ký tự nằm trong VOWELS."), ("Không rò rỉ biến làm việc", "Giữ biến vòng lặp bên trong hàm — module scope chỉ có VOWELS và count_vowels."), ("Hằng ở mức module", "Hằng vẫn import được.")]),
    },
    solutions=[
        ("pi4-pkg-main-guard", "RAN_DIRECTLY = False\n\ndef run_report():\n    return 'report'\n\nif __name__ == '__main__':\n    RAN_DIRECTLY = True", "RAN_DIRECTLY = True\n\ndef run_report():\n    print('report')\n    return 'report'"),
        ("pi4-pkg-namespace", "VOWELS = 'aeiou'\n\ndef count_vowels(text):\n    total = 0\n    for ch in text.lower():\n        if ch in VOWELS:\n            total += 1\n    return total", "VOWELS = 'aeiou'\n\ntemp = 0\n\ndef count_vowels(text):\n    global temp\n    temp = 0\n    for ch in text.lower():\n        if ch in VOWELS:\n            temp += 1\n    return temp"),
    ],
)

write_practice(
    M4, "m4-typing-practice",
    "Annotation Drills",
    "Annotate signatures — verified via get_type_hints and behavior.",
    "Luyện Annotation",
    "Chú thích chữ ký hàm — kiểm chứng qua get_type_hints và hành vi.",
    L4C, 30, "intermediate",
    [
        challenge(
            "pi4-type-avg", "Annotated Average",
            "Implement average(values: list[float]) -> float that raises ValueError on an empty list. The annotations must be exactly list[float] and float (verifyable via typing.get_type_hints).",
            "from typing import get_type_hints\n\ndef average(values: list[float]) -> float:\n    pass\n",
            [
                ("computes the mean",
                 "assert average([2.0, 4.0]) == 3.0",
                 "sum/len — the annotations don't change behavior."),
                ("empty input raises",
                 "try:\n    average([])\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed",
                 "Guard the empty case with ValueError."),
                ("annotations are real",
                 "import typing\nhints = typing.get_type_hints(average)\nassert hints['values'] == list[float]\nassert hints['return'] is float",
                 "Keep the annotations: get_type_hints must see list[float] and float."),
            ],
            level="guided",
        ),
        challenge(
            "pi4-type-find", "Union Return",
            "Implement find_user(users: dict[int, str], user_id: int) -> str | None returning the name or None when absent. Annotate it — get_type_hints must report the union type.",
            "from typing import get_type_hints\n\ndef find_user(users: dict[int, str], user_id: int) -> str | None:\n    pass\n",
            [
                ("finds existing",
                 "us = {1: 'An'}\nassert find_user(us, 1) == 'An'",
                 "dict.get does it."),
                ("missing returns None",
                 "us = {1: 'An'}\nassert find_user(us, 9) is None",
                 "Return None, never raise, for absence."),
                ("union annotation present",
                 "import typing\nhints = typing.get_type_hints(find_user)\nassert hints['return'] == (str | None)",
                 "The return annotation must be str | None."),
            ],
            level="independent",
        ),
        challenge(
            "pi4-type-td", "Typed Payload",
            "Define a TypedDict ProductDict with keys sku: str and price: float. Then implement total_price(items: list[ProductDict]) -> float summing prices. get_type_hints(ProductDict) must show both annotations.",
            "from typing import TypedDict\n\nclass ProductDict(TypedDict):\n    pass\n\ndef total_price(items):\n    pass\n",
            [
                ("totals prices",
                 "items = [{'sku': 't', 'price': 3.0}, {'sku': 'c', 'price': 4.5}]\nassert total_price(items) == 7.5",
                 "sum(item['price'] for item in items)."),
                ("typed keys verified",
                 "import typing\nhints = typing.get_type_hints(ProductDict)\nassert hints['sku'] is str and hints['price'] is float",
                 "Annotate sku: str and price: float in the TypedDict body."),
            ],
            level="combination",
        ),
    ],
    {
        "pi4-type-avg": vi_challenge("Average có chú thích", "Viết average(values: list[float]) -> float raise ValueError khi list rỗng. Annotation phải đúng là list[float] và float (kiểm được qua typing.get_type_hints).", [("Tính trung bình", "sum/len — annotation không đổi hành vi."), ("Input rỗng raise", "Chặn trường hợp rỗng bằng ValueError."), ("Annotation phải có thật", "Giữ nguyên annotation: get_type_hints phải thấy list[float] và float.")]),
        "pi4-type-find": vi_challenge("Kiểu trả về Union", "Viết find_user(users: dict[int, str], user_id: int) -> str | None trả về tên hoặc None khi không có. Phải chú thích — get_type_hints phải báo union type.", [("Tìm thấy", "dict.get làm được việc này."), ("Không có thì trả None", "Trả None, không raise, khi vắng mặt."), ("Annotation union hiện diện", "Annotation trả về phải là str | None.")]),
        "pi4-type-td": vi_challenge("Payload có kiểu", "Định nghĩa TypedDict ProductDict với key sku: str và price: float. Rồi viết total_price(items: list[ProductDict]) -> float cộng các price. get_type_hints(ProductDict) phải hiện cả hai annotation.", [("Cộng các price", "sum(item['price'] for item in items)."), ("Kiểm chứng key có kiểu", "Chú thích sku: str và price: float trong thân TypedDict.")]),
    },
    solutions=[
        ("pi4-type-avg", "from typing import get_type_hints\n\ndef average(values: list[float]) -> float:\n    if not values:\n        raise ValueError('empty')\n    return sum(values) / len(values)", "from typing import get_type_hints\n\ndef average(values: list[float]) -> float:\n    if not values:\n        return 0.0\n    return sum(values) / len(values)"),
        ("pi4-type-find", "from typing import get_type_hints\n\ndef find_user(users: dict[int, str], user_id: int) -> str | None:\n    return users.get(user_id)", "from typing import get_type_hints\n\ndef find_user(users: dict[int, str], user_id: int) -> str | None:\n    return users[user_id]"),
        ("pi4-type-td", "from typing import TypedDict\n\nclass ProductDict(TypedDict):\n    sku: str\n    price: float\n\ndef total_price(items):\n    return sum(item['price'] for item in items)", "from typing import TypedDict\n\nclass ProductDict(TypedDict):\n    sku: str\n    price: int\n\ndef total_price(items):\n    return sum(item['price'] for item in items)"),
    ],
)

write_practice(
    M4, "m4-protocol-practice",
    "Protocol Drills",
    "Define structural interfaces and accept anything shaped right.",
    "Luyện Protocol",
    "Định nghĩa interface cấu trúc và chấp nhận bất cứ thứ gì đúng hình.",
    L4D, 25, "intermediate",
    [
        challenge(
            "pi4-proto-sink", "Notifiable Protocol",
            "Define a @runtime_checkable Protocol named Notifiable with method send(message: str) -> None. Then implement class EmailSink with send appending to its own .sent list. backup(n) below must work with any Notifiable.",
            "from typing import Protocol, runtime_checkable\n\n@runtime_checkable\nclass Notifiable(Protocol):\n    pass\n\nclass EmailSink:\n    def __init__(self):\n        self.sent = []\n\ndef notify_all(sinks, message):\n    pass\n",
            [
                ("email sink records",
                 "s = EmailSink()\nnotify_all([s], 'hi')\nassert s.sent == ['hi']",
                 "notify_all calls send on each sink."),
                ("any object with send works",
                 "class Log:\n    def __init__(self):\n        self.lines = []\n    def send(self, m):\n        self.lines.append(m)\nl = Log()\nnotify_all([l], 'x')\nassert l.lines == ['x']",
                 "Duck typing: no inheritance required."),
            ],
            level="independent",
        ),
        challenge(
            "pi4-proto-storage", "Two Storages, One Interface",
            "Implement MemoryStorage (dict-backed) and class PrefixedStorage wrapping another storage and adding 'p:' to every key on save and load (delegation + composition). Both satisfy the Storage protocol from the lesson.",
            "class MemoryStorage:\n    pass\n\nclass PrefixedStorage:\n    def __init__(self, inner):\n        pass\n",
            [
                ("memory storage round-trips",
                 "m = MemoryStorage()\nm.save('k', 'v')\nassert m.load('k') == 'v'\nassert m.load('nope') is None",
                 "dict-backed save/load; missing key loads None."),
                ("prefixed storage delegates",
                 "m = MemoryStorage()\np = PrefixedStorage(m)\np.save('k', 'v')\nassert m.load('p:k') == 'v'\nassert p.load('k') == 'v'",
                 "Prefixed adds 'p:' on the way in and reads through with the prefix."),
            ],
            level="combination",
        ),
    ],
    {
        "pi4-proto-sink": vi_challenge("Protocol Notifiable", "Định nghĩa Protocol tên Notifiable với @runtime_checkable, có method send(message: str) -> None. Sau đó viết class EmailSink với send thêm vào list .sent của nó. notify_all(sinks, message) phải hoạt động với bất kỳ Notifiable nào.", [("EmailSink ghi nhận", "notify_all gọi send trên từng sink."), ("Bất kỳ object nào có send đều được", "Duck typing: không cần kế thừa.")]),
        "pi4-proto-storage": vi_challenge("Hai Storage, Một Interface", "Viết MemoryStorage (nền dict) và class PrefixedStorage bọc một storage khác, thêm 'p:' vào mọi key khi save và load (ủy quyền + composition). Cả hai thỏa mãn protocol Storage trong bài học.", [("MemoryStorage khép vòng", "save/load trên dict; key thiếu load trả None."), ("PrefixedStorage ủy quyền", "Prefixed thêm 'p:' khi ghi và đọc xuyên qua với tiền tố.")]),
    },
    solutions=[
        ("pi4-proto-sink", "from typing import Protocol, runtime_checkable\n\n@runtime_checkable\nclass Notifiable(Protocol):\n    def send(self, message: str) -> None: ...\n\nclass EmailSink:\n    def __init__(self):\n        self.sent = []\n\n    def send(self, message):\n        self.sent.append(message)\n\ndef notify_all(sinks, message):\n    for s in sinks:\n        s.send(message)", "from typing import Protocol, runtime_checkable\n\n@runtime_checkable\nclass Notifiable(Protocol):\n    def send(self, message: str) -> None: ...\n\nclass EmailSink:\n    def __init__(self):\n        self.sent = []\n\ndef notify_all(sinks, message):\n    for s in sinks:\n        s.sent.append(message)"),
        ("pi4-proto-storage", "class MemoryStorage:\n    def __init__(self):\n        self._data = {}\n\n    def save(self, key, value):\n        self._data[key] = value\n\n    def load(self, key):\n        return self._data.get(key)\n\nclass PrefixedStorage:\n    def __init__(self, inner):\n        self.inner = inner\n\n    def save(self, key, value):\n        self.inner.save('p:' + key, value)\n\n    def load(self, key):\n        return self.inner.load('p:' + key)", "class MemoryStorage:\n    def __init__(self):\n        self._data = {}\n\n    def save(self, key, value):\n        self._data[key] = value\n\n    def load(self, key):\n        return self._data[key]\n\nclass PrefixedStorage:\n    def __init__(self, inner):\n        self.inner = inner\n\n    def save(self, key, value):\n        self.inner.save('p:' + key, value)\n\n    def load(self, key):\n        return self.inner.load(key)"),
    ],
)

# --- module 4 checkpoint ---
write_checkpoint(
    M4, L4E,
    "Checkpoint: A Typed Application Slice",
    "Combine a Protocol boundary, an annotated service function, and a TypedDict payload.",
    20,
    """
Real applications are layers with typed seams. This checkpoint builds one
seam end-to-end: a payload type, a Protocol for storage, and a service
function that validates and delegates — all annotated.

**Working with AI:** try "generate three edge cases for this signature" and
write the tests yourself before accepting any generated implementation.
""",
    "Checkpoint: Một Lát Ứng dụng Có Kiểu",
    "Kết hợp ranh giới Protocol, hàm service có chú thích, và payload TypedDict.",
    """
Ứng dụng thật là các tầng với đường nối có kiểu. Checkpoint này dựng một
đường nối trọn vẹn: kiểu payload, Protocol cho storage, và hàm service
kiểm tra hợp lệ rồi ủy quyền — tất cả đều có chú thích.

**Làm việc cùng AI:** hãy thử "sinh ba trường hợp biên cho chữ ký này" và tự
viết test trước khi chấp nhận bất kỳ bản cài đặt nào do AI tạo.
""",
    challenge(
        "pi4-ckpt-typed-app", "Typed Note Service",
        "Define TypedDict NoteDict(id: int, text: str), a @runtime_checkable Protocol NoteStore with add(note_id: int, text: str) -> None and get(note_id: int) -> str | None, class MemoryNotes implementing both, and function save_note(store: NoteStore, note: NoteDict) -> bool that raises ValueError when note['text'] is empty/whitespace, otherwise stores and returns True.",
        "from typing import TypedDict, Protocol, runtime_checkable, get_type_hints\n\nclass NoteDict(TypedDict):\n    pass\n\n@runtime_checkable\nclass NoteStore(Protocol):\n    pass\n\nclass MemoryNotes:\n    pass\n\ndef save_note(store, note):\n    pass\n",
        [
            ("stores a valid note",
             "m = MemoryNotes()\nassert save_note(m, {'id': 1, 'text': 'buy milk'}) is True\nassert m.get(1) == 'buy milk'",
             "Validate, then delegate to store.add."),
            ("rejects blank text",
             "m = MemoryNotes()\ntry:\n    save_note(m, {'id': 2, 'text': '   '})\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed",
             "Whitespace-only text must raise ValueError before touching the store."),
            ("missing get returns None",
             "m = MemoryNotes()\nassert m.get(999) is None",
             "get returns None for unknown ids."),
            ("annotations verifiable",
             "import typing\nhints = typing.get_type_hints(NoteDict)\nassert hints['id'] is int and hints['text'] is str",
             "NoteDict fields must carry id: int and text: str."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Note Service có kiểu",
        "Định nghĩa TypedDict NoteDict(id: int, text: str), Protocol NoteStore với @runtime_checkable có add(note_id: int, text: str) -> None và get(note_id: int) -> str | None, class MemoryNotes cài cả hai, và hàm save_note(store: NoteStore, note: NoteDict) -> bool raise ValueError khi note['text'] rỗng/chỉ-whitespace, ngược lại lưu và trả True.",
        [
            ("Lưu note hợp lệ", "Kiểm tra hợp lệ, rồi ủy quyền cho store.add."),
            ("Từ chối text trắng", "Text chỉ-whitespace phải raise ValueError trước khi đụng vào store."),
            ("get thiếu trả None", "get trả None cho id lạ."),
            ("Annotation kiểm chứng được", "Các trường NoteDict phải có id: int và text: str."),
        ],
    ),
    solution="from typing import TypedDict, Protocol, runtime_checkable\n\nclass NoteDict(TypedDict):\n    id: int\n    text: str\n\n@runtime_checkable\nclass NoteStore(Protocol):\n    def add(self, note_id: int, text: str) -> None: ...\n    def get(self, note_id: int) -> str | None: ...\n\nclass MemoryNotes:\n    def __init__(self):\n        self._notes = {}\n\n    def add(self, note_id, text):\n        self._notes[note_id] = text\n\n    def get(self, note_id):\n        return self._notes.get(note_id)\n\ndef save_note(store, note):\n    if not note['text'].strip():\n        raise ValueError('text must not be empty')\n    store.add(note['id'], note['text'])\n    return True",
    wrong="from typing import TypedDict, Protocol, runtime_checkable\n\nclass NoteDict(TypedDict):\n    id: int\n    text: str\n\n@runtime_checkable\nclass NoteStore(Protocol):\n    def add(self, note_id: int, text: str) -> None: ...\n    def get(self, note_id: int) -> str | None: ...\n\nclass MemoryNotes:\n    def __init__(self):\n        self._notes = {}\n\n    def add(self, note_id, text):\n        self._notes[note_id] = text\n\n    def get(self, note_id):\n        return self._notes.get(note_id)\n\ndef save_note(store, note):\n    if not note['text'].strip():\n        return False\n    store.add(note['id'], note['text'])\n    return True",
)

print("module 4 done")
