#!/usr/bin/env python3
"""Module 3: advanced-typing — lessons + practices + checkpoint (graded code targets 3.11)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "advanced-typing"

write_module(
    MOD,
    "Advanced Typing & Static Design",
    "Types as engineering tools: generics and variance, overloads, Protocols, TypedDict, ParamSpec — design first, checker second.",
    "Typing nâng cao & thiết kế tĩnh",
    "Type như công cụ kỹ thuật: generic và variance, overload, Protocol, TypedDict, ParamSpec — thiết kế trước, checker sau.",
    ["typing-philosophy", "generics-variance", "protocols-overloads", "typeddict-paramspec"],
    ["pa-p3-generics-practice", "pa-p3-protocol-practice", "pa-p3-typed-project"],
)

L1_EN = """
## Runtime vs static: what types are and are not

Python's type hints are **not enforced at runtime**. `def f(x: int) -> str` runs
happily with `f("oops")`. Hints are consumed by *static checkers* (mypy, pyright)
and by *readers* — they are a design language layered over the code.

What this means at an advanced level:

- Types describe **intent and contracts**, not runtime behavior. A wrong
  annotation is a lie that ships silently unless a checker runs in CI.
- `typing.get_type_hints(obj)` / `obj.__annotations__` can read hints at runtime
  — that is how dataclasses, pydantic, and dependency-injection frameworks
  build behavior from annotations.
- The workflow professionals run: annotate the boundaries first (function
  signatures, API models), let inference handle the inside, run the checker in
  CI, and treat `Any` as a TODO, not a default.

Version note (prose only): Python 3.12 adds PEP 695 type-parameter syntax
(`def first[T](xs: list[T]) -> T`), and 3.13 adds `typing.TypeIs`. This course's
graded code targets 3.11 (`TypeVar`, `Generic`, `TypeGuard`), which runs
unchanged on 3.12+ sandboxes.
"""

L1_VI = L1_EN.replace(
    "## Runtime vs static: what types are and are not",
    "## Runtime vs tĩnh: type là gì và không phải là gì",
).replace(
    "Python's type hints are **not enforced at runtime**. `def f(x: int) -> str` runs\nhappily with `f(\"oops\")`. Hints are consumed by *static checkers* (mypy, pyright)\nand by *readers* — they are a design language layered over the code.",
    "Type hint của Python **không được thực thi lúc runtime**. `def f(x: int) -> str`\nvẫn chạy ngon với `f(\"oops\")`. Hint được *static checker* (mypy, pyright) và\n*người đọc* tiêu thụ — chúng là một ngôn ngữ thiết kế phủ lên trên code.",
).replace(
    "What this means at an advanced level:",
    "Ở mức nâng cao, điều này có nghĩa là:",
).replace(
    "- Types describe **intent and contracts**, not runtime behavior. A wrong\n  annotation is a lie that ships silently unless a checker runs in CI.\n- `typing.get_type_hints(obj)` / `obj.__annotations__` can read hints at runtime\n  — that is how dataclasses, pydantic, and dependency-injection frameworks\n  build behavior from annotations.\n- The workflow professionals run: annotate the boundaries first (function\n  signatures, API models), let inference handle the inside, run the checker in\n  CI, and treat `Any` as a TODO, not a default.",
    "- Type mô tả **ý định và hợp đồng**, không phải hành vi runtime. Annotation sai\n  là lời nói dối được ship âm thầm trừ khi checker chạy trong CI.\n- `typing.get_type_hints(obj)` / `obj.__annotations__` đọc được hint lúc runtime —\n  dataclasses, pydantic, và framework DI dựng hành vi từ annotation theo cách đó.\n- Quy trình chuyên nghiệp: annotate ranh giới trước (chữ ký hàm, model API),\n  để inference lo phần bên trong, chạy checker trong CI, và coi `Any` như một\n  TODO, không phải mặc định.",
).replace(
    "Version note (prose only): Python 3.12 adds PEP 695 type-parameter syntax\n(`def first[T](xs: list[T]) -> T`), and 3.13 adds `typing.TypeIs`. This course's\ngraded code targets 3.11 (`TypeVar`, `Generic`, `TypeGuard`), which runs\nunchanged on 3.12+ sandboxes.",
    "Ghi chú phiên bản (chỉ là văn bản): Python 3.12 thêm cú pháp type-parameter\nPEP 695 (`def first[T](xs: list[T]) -> T`), và 3.13 thêm `typing.TypeIs`. Mã\nđược chấm của khóa này nhắm tới 3.11 (`TypeVar`, `Generic`, `TypeGuard`), chạy\nnguyên vẹn trên sandbox 3.12+.",
)

write_lesson(
    MOD, "typing-philosophy",
    "Types as design: runtime vs static",
    "Understand what annotations promise, who consumes them, and where to draw boundaries.",
    18, L1_EN,
    "Type là thiết kế: runtime vs tĩnh",
    "Hiểu annotation hứa gì, ai tiêu thụ chúng, và vẽ ranh giới ở đâu.",
    L1_VI,
)

L2_EN = """
## Generics, TypeVar, and variance

A **generic** keeps the type relationship between input and output visible:

```python
from typing import TypeVar, Generic, List

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()

def first(xs: List[T]) -> T:
    return xs[0]
```

`first(["a", "b"])` has type `str` — the checker binds `T = str`. At runtime
`Stack[int]()` also works: `Generic` classes support subscription, which some
libraries use for validation.

**Bounded TypeVars** state a contract: `T = TypeVar("T", bound="Shape")` means
"any subtype of Shape" — inside the function you may call Shape's methods.

**Variance** answers "may I use Box[Cat] where Box[Animal] is expected?":

- **Covariant** (`T_co = TypeVar("T_co", covariant=True)`): read-only positions
  (produced values). A producer of Cats is a producer of Animals.
- **Contravariant** (`T_contra`): write-only positions (consumed values). A
  consumer of Animals can consume Cats.
- **Invariant** (default): mutable containers — `Box[Cat]` is NOT a `Box[Animal]`
  because you could `put` a Dog into it.

Rule of thumb: producers covariant, consumers contravariant, mutable containers
invariant. Get this wrong and the checker blocks a real bug — that is the point.
"""

L2_VI = L2_EN.replace(
    "## Generics, TypeVar, and variance",
    "## Generic, TypeVar và variance",
).replace(
    "A **generic** keeps the type relationship between input and output visible:",
    "**Generic** giữ mối quan hệ kiểu giữa đầu vào và đầu ra luôn hiển thị:",
).replace(
    "`first([\"a\", \"b\"])` has type `str` — the checker binds `T = str`. At runtime\n`Stack[int]()` also works: `Generic` classes support subscription, which some\nlibraries use for validation.",
    "`first([\"a\", \"b\"])` có kiểu `str` — checker gán `T = str`. lúc runtime\n`Stack[int]()` cũng chạy được: class `Generic` hỗ trợ subscription, một số thư\nviện dùng điều đó để validate.",
).replace(
    "**Bounded TypeVars** state a contract: `T = TypeVar(\"T\", bound=\"Shape\")` means\n\"any subtype of Shape\" — inside the function you may call Shape's methods.",
    "**TypeVar có bound** phát biểu một hợp đồng: `T = TypeVar(\"T\", bound=\"Shape\")`\nnghĩa là \"bất kỳ subtype nào của Shape\" — trong hàm bạn được gọi method của Shape.",
).replace(
    "**Variance** answers \"may I use Box[Cat] where Box[Animal] is expected?\":",
    "**Variance** trả lời câu hỏi \"có được dùng Box[Cat] nơi kỳ vọng Box[Animal] không?\":",
).replace(
    "- **Covariant** (`T_co = TypeVar(\"T_co\", covariant=True)`): read-only positions\n  (produced values). A producer of Cats is a producer of Animals.\n- **Contravariant** (`T_contra`): write-only positions (consumed values). A\n  consumer of Animals can consume Cats.\n- **Invariant** (default): mutable containers — `Box[Cat]` is NOT a `Box[Animal]`\n  because you could `put` a Dog into it.",
    "- **Covariant** (`T_co = TypeVar(\"T_co\", covariant=True)`): vị trí chỉ đọc\n  (giá trị được sản xuất). Nhà sản xuất Cat cũng là nhà sản xuất Animal.\n- **Contravariant** (`T_contra`): vị trí chỉ ghi (giá trị bị tiêu thụ). Bộ tiêu\n  thụ Animal có thể tiêu thụ Cat.\n- **Invariant** (mặc định): containermutable — `Box[Cat]` KHÔNG phải `Box[Animal]`\n  vì bạn có thể `put` một Dog vào trong.",
).replace(
    "Rule of thumb: producers covariant, consumers contravariant, mutable containers\ninvariant. Get this wrong and the checker blocks a real bug — that is the point.",
    "Kinh nghiệm: producer thì covariant, consumer thì contravariant, container\nmutable thì invariant. Làm sai và checker chặn đúng một bug thật — đó là mục đích.",
)

write_lesson(
    MOD, "generics-variance",
    "Generics, TypeVar bounds, variance",
    "Keep input-output type relationships visible; choose variance deliberately.",
    22, L2_EN,
    "Generic, TypeVar bound, variance",
    "Giữ quan hệ kiểu vào-ra luôn hiển thị; chọn variance một cách có chủ đích.",
    L2_VI,
)

L3_EN = """
## Protocols, overloads, and callables

**`typing.Protocol`** defines structure, not inheritance. Any object with the
right members satisfies the protocol — duck typing that a checker can verify:

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

def render(x: Drawable) -> str:
    return x.draw()

class Circle:                      # no inheritance from Drawable
    def draw(self) -> str:
        return "circle"
```

`render(Circle())` type-checks even though `Circle` never mentions `Drawable`.
`@runtime_checkable` additionally allows `isinstance` checks (method presence
only, not signatures).

**`@overload`** describes input-dependent output types. The implementations
carry the body; the overloads are the contract:

```python
from typing import overload, Union

@overload
def parse(value: str) -> list[str]: ...
@overload
def parse(value: bytes) -> str: ...
def parse(value):
    if isinstance(value, bytes):
        return value.decode()
    return value.split(",")
```

**Callables** get typed with `Callable[[ArgTypes], ReturnType]`. For anything
richer — keyword args, generics, decorated functions — use `ParamSpec`:

```python
from typing import TypeVar, ParamSpec, Callable
P = ParamSpec("P")
R = TypeVar("R")

def logged(fn: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("calling", fn.__name__)
        return fn(*args, **kwargs)
    return wrapper
```

`ParamSpec` preserves the *entire* signature through the decorator — the
decorated function stays as callable as the original, to the checker and to
`inspect.signature` (via `functools.wraps`).
"""

L3_VI = L3_EN.replace(
    "## Protocols, overloads, and callables",
    "## Protocol, overload và callable",
).replace(
    "**`typing.Protocol`** defines structure, not inheritance. Any object with the\nright members satisfies the protocol — duck typing that a checker can verify:",
    "**`typing.Protocol`** định nghĩa cấu trúc, không phải kế thừa. Bất kỳ đối tượng\nnào có đúng các thành viên đều thỏa protocol — duck typing mà checker có thể\nxác minh:",
).replace(
    "`render(Circle())` type-checks even though `Circle` never mentions `Drawable`.\n`@runtime_checkable` additionally allows `isinstance` checks (method presence\nonly, not signatures).",
    "`render(Circle())` qua được kiểm tra kiểu dù `Circle` chưa từng nhắc tới\n`Drawable`. `@runtime_checkable` cộng thêm khả năng `isinstance` (chỉ kiểm tra\ncó method, không kiểm tra chữ ký).",
).replace(
    "**`@overload`** describes input-dependent output types. The implementations\ncarry the body; the overloads are the contract:",
    "**`@overload`** mô tả kiểu đầu ra phụ thuộc đầu vào. Phần implementation giữ\nthân hàm; các overload chính là hợp đồng:",
).replace(
    "**Callables** get typed with `Callable[[ArgTypes], ReturnType]`. For anything\nricher — keyword args, generics, decorated functions — use `ParamSpec`:",
    "**Callable** được đánh kiểu bằng `Callable[[ArgTypes], ReturnType]`. Với những\ndevà richer — keyword args, generic, hàm được trang trí — dùng `ParamSpec`:",
).replace(
    "`ParamSpec` preserves the *entire* signature through the decorator — the\ndecorated function stays as callable as the original, to the checker and to\n`inspect.signature` (via `functools.wraps`).",
    "`ParamSpec` giữ nguyên *toàn bộ* chữ ký xuyên qua decorator — hàm sau trang trí\nvẫn callable như bản gốc, với cả checker lẫn `inspect.signature` (nhờ\n`functools.wraps`).",
)

write_lesson(
    MOD, "protocols-overloads",
    "Protocols, overloads, ParamSpec",
    "Structure over inheritance; input-dependent outputs; signatures that survive decorators.",
    24, L3_EN,
    "Protocol, overload, ParamSpec",
    "Cấu trúc hơn kế thừa; đầu ra phụ thuộc đầu vào; chữ ký sống sót qua decorator.",
    L3_VI,
)

L4_EN = """
## TypedDict, Literal, TypeGuard — typing data at the edges

**`TypedDict`** types dictionary-shaped data — JSON, API payloads, config —
where keys are known and values vary per key:

```python
from typing import TypedDict

class Movie(TypedDict):
    title: str
    year: int
    tags: list[str]

movie: Movie = {"title": "Coco", "year": 2017, "tags": ["animation"]}
```

At runtime it is a plain dict (no validation — that is pydantic's job); the
value is for the checker and for `total=True/False` key requirements.

**`Literal`** narrows a value to exact literals — the type-safe replacement for
magic strings:

```python
from typing import Literal, TypeAlias
Mode: TypeAlias = Literal["r", "w", "a"]

def open_db(mode: Mode) -> None: ...
```

**`TypeGuard`** documents narrowing functions — the predicate returns True and
the checker then treats the argument as the guarded type:

```python
from typing import TypeGuard

def is_str_list(xs: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in xs)
```

Design guidance: type the *edges* of the system precisely (API responses,
config, queue messages) and let internal code flow from those anchors. `cast()`
exists for the rare moment you know more than the checker — treat every cast
as a comment that can lie, and prefer a `TypeGuard` or `assert isinstance`
which actually checks.
"""

L4_VI = L4_EN.replace(
    "## TypedDict, Literal, TypeGuard — typing data at the edges",
    "## TypedDict, Literal, TypeGuard — đánh kiểu dữ liệu ở rìa hệ thống",
).replace(
    "**`TypedDict`** types dictionary-shaped data — JSON, API payloads, config —\nwhere keys are known and values vary per key:",
    "**`TypedDict`** đánh kiểu cho dữ liệu dạng dict — JSON, payload API, config —\nnơi các key đã biết và value khác nhau theo key:",
).replace(
    "At runtime it is a plain dict (no validation — that is pydantic's job); the\nvalue is for the checker and for `total=True/False` key requirements.",
    "Lúc runtime nó chỉ là dict thường (không validate — việc của pydantic); giá trị\ncủa nó là cho checker và cho yêu cầu key qua `total=True/False`.",
).replace(
    "**`Literal`** narrows a value to exact literals — the type-safe replacement for\nmagic strings:",
    "**`Literal`** thu hẹp giá trị về đúng các literal — thay thế an toàn kiểu cho\nmagic string:",
).replace(
    "**`TypeGuard`** documents narrowing functions — the predicate returns True and\nthe checker then treats the argument as the guarded type:",
    "**`TypeGuard`** ghi chú các hàm thu hẹp kiểu — predicate trả True và checker\nsau đó coi đối số như kiểu được bảo vệ:",
).replace(
    "Design guidance: type the *edges* of the system precisely (API responses,\nconfig, queue messages) and let internal code flow from those anchors. `cast()`\nexists for the rare moment you know more than the checker — treat every cast\nas a comment that can lie, and prefer a `TypeGuard` or `assert isinstance`\nwhich actually checks.",
    "Định hướng thiết kế: đánh kiểu *rìa* hệ thống thật chính xác (response API,\nconfig, message trên queue) và để code bên trong chảy từ những mỏ neo đó.\n`cast()` tồn tại cho khoảnh khắc hiếm hoi bạn biết nhiều hơn checker — hãy coi\nmỗi cast như một comment có thể nói dối, và ưu tiên `TypeGuard` hay\n`assert isinstance` — những thứ thực sự kiểm tra.",
)

write_lesson(
    MOD, "typeddict-paramspec",
    "TypedDict, Literal, TypeGuard",
    "Type real-world data shapes: payloads, enums-as-literals, narrowing predicates.",
    20, L4_EN,
    "TypedDict, Literal, TypeGuard",
    "Đánh kiểu cho hình dạng dữ liệu thật: payload, enum-dạng-literal, predicate thu hẹp.",
    L4_VI,
)

# ── practice 1: generics ─────────────────────────────────────────────────────
STACK_REF = (
    "from typing import TypeVar, Generic, List\n\n"
    "T = TypeVar('T')\n\n\n"
    "class Stack(Generic[T]):\n"
    "    def __init__(self) -> None:\n"
    "        self._items: List[T] = []\n\n"
    "    def push(self, item: T) -> None:\n"
    "        self._items.append(item)\n\n"
    "    def pop(self) -> T:\n"
    "        if not self._items:\n"
    "            raise IndexError('pop from empty stack')\n"
    "        return self._items.pop()\n\n"
    "    def peek(self) -> T:\n"
    "        if not self._items:\n"
    "            raise IndexError('peek at empty stack')\n"
    "        return self._items[-1]\n\n"
    "    def __len__(self) -> int:\n"
    "        return len(self._items)\n\n\n"
    "def first(xs: List[T]) -> T:\n"
    "    if not xs:\n"
    "        raise ValueError('empty sequence')\n"
    "    return xs[0]"
)
STACK_WRONG = STACK_REF.replace(
    "    def push(self, item: T) -> None:\n        self._items.append(item)",
    "    def push(self, item) -> None:\n        self._items.append(str(item))  # WRONG: coerces to str, violating T",
)

write_practice(
    MOD, "pa-p3-generics-practice",
    "Generics Practice",
    "Type-preserving containers and functions — the bread and butter of library APIs.",
    "Luyện Generic",
    "Container và hàm giữ nguyên kiểu — cơm bữa của API thư viện.",
    "generics-variance", 20, "advanced",
    [
        challenge(
            "pa-ty-generic-stack",
            "A generic Stack[T]",
            "Implement `Stack(Generic[T])` with `push(item: T)`, `pop() -> T` (IndexError on empty), `peek() -> T` (IndexError on empty), and `__len__`. Also implement `first(xs: List[T]) -> T` raising `ValueError('empty sequence')` on an empty list.\n\nRuntime must behave exactly like the untyped version — the generic parameter is a design contract (your annotations must reference T where relevant).",
            "from typing import TypeVar, Generic, List\n\nT = TypeVar('T')\n\n# TODO: Stack and first",
            [
                ("stack behaves and preserves values",
                 "s = Stack()\ns.push(1)\ns.push('a')\nassert len(s) == 2\nassert s.pop() == 'a'\nassert s.peek() == 1\nassert s.pop() == 1\ntry:\n    Stack().pop()\nexcept IndexError:\n    pass\nelse:\n    raise AssertionError('empty pop must raise IndexError')\nprint('ok')",
                 "Store items in a list; the annotations document the contract (item: T, pop() -> T)."),
                ("first() and runtime subscript",
                 "assert first([3, 1, 2]) == 3\nassert first(['x', 'y']) == 'x'\ntry:\n    first([])\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('first([]) must raise ValueError')\nsub = Stack[int]()\nassert isinstance(sub, Stack), 'Generic classes support runtime subscription'\nprint('ok')",
                 "Raise ValueError with the exact message for empty input; Stack[int]() must work at runtime via Generic."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-ty-generic-stack": vi_challenge(
            "Stack[T] kiểu generic",
            "Cài `Stack(Generic[T])` với `push(item: T)`, `pop() -> T` (IndexError khi rỗng), `peek() -> T` (IndexError khi rỗng), và `__len__`. Đồng thời cài `first(xs: List[T]) -> T` raise `ValueError('empty sequence')` với list rỗng.\n\nRuntime phải hành xử y như bản không đánh kiểu — tham số generic là hợp đồng thiết kế (annotation của bạn phải tham chiếu T ở nơi liên quan).",
            [("Stack hành xử và giữ nguyên giá trị", "Lưu item vào list; annotation ghi lại hợp đồng (item: T, pop() -> T)."),
             ("first() và subscript lúc runtime", "Raise ValueError đúng thông báo với đầu vào rỗng; Stack[int]() phải chạy được lúc runtime nhờ Generic.")],
        ),
    },
    solutions=[("pa-ty-generic-stack", STACK_REF, STACK_WRONG)],
)

# ── practice 2: protocols + overloads ────────────────────────────────────────
PROTO_REF = (
    "from typing import Protocol, overload, Union\n\n\n"
    "class Area(Protocol):\n"
    "    def area(self) -> float: ...\n\n\n"
    "def total_area(shapes) -> float:\n"
    "    return sum(s.area() for s in shapes)\n\n\n"
    "@overload\n"
    "def parse(value: str) -> list: ...\n\n\n"
    "@overload\n"
    "def parse(value: bytes) -> str: ...\n\n\n"
    "def parse(value):\n"
    "    if isinstance(value, bytes):\n"
    "        return value.decode()\n"
    "    return value.split(',')"
)
PROTO_WRONG = (
    "from typing import Protocol, overload, Union\n\n\n"
    "class Area(Protocol):\n"
    "    def area(self) -> float: ...\n\n\n"
    "def total_area(shapes) -> float:\n"
    "    # WRONG: isinstance check against the Protocol class without\n"
    "    # @runtime_checkable raises TypeError at runtime\n"
    "    return sum(s.area() for s in shapes if isinstance(s, Area))\n\n\n"
    "@overload\n"
    "def parse(value: str) -> list: ...\n\n\n"
    "@overload\n"
    "def parse(value: bytes) -> str: ...\n\n\n"
    "def parse(value):\n"
    "    if isinstance(value, bytes):\n"
    "        return value.decode()\n"
    "    return value.split(',')"
)

write_practice(
    MOD, "pa-p3-protocol-practice",
    "Protocols & Overloads Practice",
    "Structure-based contracts and input-dependent output types.",
    "Luyện Protocol & Overload",
    "Hợp đồng dựa trên cấu trúc và kiểu đầu ra phụ thuộc đầu vào.",
    "protocols-overloads", 20, "advanced",
    [
        challenge(
            "pa-ty-protocol-area",
            "Protocol-based area total",
            "Implement:\n\n1. `class Area(Protocol)` with one method `area(self) -> float` (use `...` as the body).\n2. `total_area(shapes)` summing `s.area()` over any objects that satisfy the protocol structurally (no isinstance gate — just call area()).\n3. `parse(value)` with two `@overload` stubs (`str -> list`, `bytes -> str`) and an implementation: bytes decode to str, str splits on ',' into a list.",
            "from typing import Protocol, overload\n\n# TODO: Area protocol, total_area, parse with overloads",
            [
                ("structural satisfaction works",
                 "class Rect:\n    def __init__(self, w, h):\n        self.w, self.h = w, h\n    def area(self):\n        return self.w * self.h\n\nclass Circle:\n    def __init__(self, r):\n        self.r = r\n    def area(self):\n        return 3.14159 * self.r ** 2\n\ntotal = total_area([Rect(2, 3), Circle(1)])\nassert abs(total - (6 + 3.14159)) < 1e-6, f'total: {total}'\nprint('ok')",
                 "total_area never checks types — it calls area() and lets the protocol live in the annotations."),
                ("overloaded parse dispatches on input type",
                 "assert parse('a,b,c') == ['a', 'b', 'c']\nassert parse(b'hello') == 'hello'\ntry:\n    Area()\nexcept TypeError:\n    pass\nelse:\n    raise AssertionError('protocols cannot be instantiated')\nprint('ok')",
                 "Runtime dispatch is a plain isinstance on bytes; overloads are checker-facing contracts."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-ty-protocol-area": vi_challenge(
            "Tổng diện tích theo Protocol",
            "Cài:\n\n1. `class Area(Protocol)` với một method `area(self) -> float` (thân hàm dùng `...`).\n2. `total_area(shapes)` cộng `s.area()` trên bất kỳ đối tượng nào thỏa protocol về mặt cấu trúc (không dùng isinstance chặn — chỉ gọi area()).\n3. `parse(value)` với hai stub `@overload` (`str -> list`, `bytes -> str`) và phần implementation: bytes decode thành str, str split trên ',' thành list.",
            [("Thỏa cấu trúc là đủ", "total_area không bao giờ kiểm tra kiểu — chỉ gọi area() và để protocol sống trong annotation."),
             ("parse overload phân xử theo kiểu đầu vào", "Phân xử runtime chỉ là isinstance trên bytes; overload là hợp đồng phía checker.")],
        ),
    },
    solutions=[("pa-ty-protocol-area", PROTO_REF, PROTO_WRONG)],
)

# ── practice 3 + project: typed API model ────────────────────────────────────
TYPED_REF = (
    "from typing import TypedDict, Literal, TypeGuard, List, Optional\n\n"
    "Status = Literal['pending', 'paid', 'shipped']\n\n\n"
    "class Order(TypedDict, total=False):\n"
    "    id: int\n"
    "    status: Status\n"
    "    items: List[str]\n"
    "    note: Optional[str]\n\n\n"
    "def is_valid_order(data) -> TypeGuard[Order]:\n"
    "    if not isinstance(data, dict):\n"
    "        return False\n"
    "    if not isinstance(data.get('id'), int) or isinstance(data.get('id'), bool):\n"
    "        return False\n"
    "    if data.get('status') not in ('pending', 'paid', 'shipped'):\n"
    "        return False\n"
    "    items = data.get('items')\n"
    "    if not isinstance(items, list) or not all(isinstance(i, str) for i in items):\n"
    "        return False\n"
    "    return True\n\n\n"
    "def status_of(order) -> Status:\n"
    "    return order['status']"
)
TYPED_WRONG = (
    "from typing import TypedDict, Literal, TypeGuard, List, Optional\n\n"
    "Status = Literal['pending', 'paid', 'shipped']\n\n\n"
    "class Order(TypedDict, total=False):\n"
    "    id: int\n"
    "    status: Status\n"
    "    items: List[str]\n"
    "    note: Optional[str]\n\n\n"
    "def is_valid_order(data) -> TypeGuard[Order]:\n"
    "    # WRONG: accepts bool as id (bool is an int) and any string status\n"
    "    if not isinstance(data, dict):\n"
    "        return False\n"
    "    if not isinstance(data.get('id'), int):\n"
    "        return False\n"
    "    if not isinstance(data.get('status'), str):\n"
    "        return False\n"
    "    return True\n\n\n"
    "def status_of(order) -> Status:\n"
    "    return order['status']"
)

write_practice(
    MOD, "pa-p3-typed-project",
    "Project: Typed API Model",
    "A validated order record: TypedDict shape, Literal status set, TypeGuard predicate.",
    "Project: Model API có kiểu",
    "Bản ghi đơn hàng có kiểm chứng: TypedDict, Literal cho status, TypeGuard làm predicate.",
    "typeddict-paramspec", 25, "advanced",
    [
        challenge(
            "pa-ty-typed-order",
            "TypedDict + TypeGuard order validation",
            "Build the typed order model:\n\n1. `Status = Literal['pending', 'paid', 'shipped']`\n2. `class Order(TypedDict, total=False)` with fields `id: int`, `status: Status`, `items: List[str]`, `note: Optional[str]`\n3. `is_valid_order(data) -> TypeGuard[Order]` returning True only when: data is a dict; `id` is a true int (bool rejected); `status` is one of the three literals; `items` is a list of str\n4. `status_of(order) -> Status` returning the status field\n\nBe strict about bool: in Python `isinstance(True, int)` is True, so a bare isinstance check accepts booleans — reject them.",
            "from typing import TypedDict, Literal, TypeGuard, List, Optional\n\n# TODO: Status, Order, is_valid_order, status_of",
            [
                ("valid orders pass, garbage fails",
                 "good = {'id': 7, 'status': 'paid', 'items': ['a', 'b']}\nassert is_valid_order(good)\nassert status_of(good) == 'paid'\nfor bad in (\n    {'id': True, 'status': 'paid', 'items': []},\n    {'id': 1, 'status': 'returned', 'items': []},\n    {'id': 1, 'status': 'paid', 'items': 'ab'},\n    {'id': 1, 'status': 'paid'},\n    'nope',\n    42,\n):\n    assert not is_valid_order(bad), f'must reject: {bad!r}'\nprint('ok')",
                 "Check dict-ness, true-int id (reject bool), literal status membership, and list-of-str items."),
                ("bool rejection is explicit",
                 "assert is_valid_order({'id': 0, 'status': 'pending', 'items': []})\nassert not is_valid_order({'id': False, 'status': 'pending', 'items': []})\nprint('ok')",
                 "id 0 is valid; False is not — the bool check must be explicit."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-ty-typed-order": vi_challenge(
            "TypedDict + TypeGuard kiểm tra đơn hàng",
            "Dựng model đơn hàng có kiểu:\n\n1. `Status = Literal['pending', 'paid', 'shipped']`\n2. `class Order(TypedDict, total=False)` với các field `id: int`, `status: Status`, `items: List[str]`, `note: Optional[str]`\n3. `is_valid_order(data) -> TypeGuard[Order]` trả True chỉ khi: data là dict; `id` là int thật (loại bool); `status` là một trong ba literal; `items` là list của str\n4. `status_of(order) -> Status` trả về field status\n\nNghiêm ngặt với bool: trong Python `isinstance(True, int)` là True, nên isinstance thường sẽ chấp nhận boolean — hãy loại chúng.",
            [("Đơn hợp lệ qua, rác bị chặn", "Kiểm tra dict, id là int thật (loại bool), status thuộc literal, items là list của str."),
             ("Chặn bool phải tường minh", "id 0 hợp lệ; False thì không — phép kiểm bool phải hiện hữu.")],
        ),
    },
    solutions=[("pa-ty-typed-order", TYPED_REF, TYPED_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
REPO_REF = (
    "class User:\n    def __init__(self, uid, name):\n        self.uid, self.name = uid, name\n    def __eq__(self, other):\n        return isinstance(other, User) and self.uid == other.uid and self.name == other.name\n    def __repr__(self):\n        return f'User({self.uid})'\n\n\n"
    "from typing import Protocol, TypeVar, Generic, List, Optional\n\n"
    "T = TypeVar('T')\n\n\n"
    "class Repository(Protocol[T]):\n"
    "    def add(self, item: T) -> None: ...\n"
    "    def get(self, key: str) -> Optional[T]: ...\n"
    "    def all(self) -> List[T]: ...\n\n\n"
    "class MemoryRepository(Generic[T]):\n"
    "    def __init__(self, key_fn) -> None:\n"
    "        self._items = {}\n"
    "        self._key_fn = key_fn\n\n"
    "    def add(self, item: T) -> None:\n"
    "        self._items.setdefault(self._key_fn(item), item)\n\n"
    "    def get(self, key: str) -> Optional[T]:\n"
    "        return self._items.get(key)\n\n"
    "    def all(self) -> List[T]:\n"
    "        return list(self._items.values())\n\n\n"
    "def seed(repo, users) -> None:\n"
    "    for u in users:\n"
    "        repo.add(u)"
)
REPO_WRONG = (
    "class User:\n    def __init__(self, uid, name):\n        self.uid, self.name = uid, name\n    def __eq__(self, other):\n        return isinstance(other, User) and self.uid == other.uid and self.name == other.name\n    def __repr__(self):\n        return f'User({self.uid})'\n\n\n"
    "from typing import Protocol, TypeVar, Generic, List, Optional\n\n"
    "T = TypeVar('T')\n\n\n"
    "class Repository(Protocol[T]):\n"
    "    def add(self, item: T) -> None: ...\n"
    "    def get(self, key: str) -> Optional[T]: ...\n"
    "    def all(self) -> List[T]: ...\n\n\n"
    "class MemoryRepository(Generic[T]):\n"
    "    def __init__(self, key_fn) -> None:\n"
    "        self._items = {}\n"
    "        self._key_fn = key_fn\n\n"
    "    def add(self, item: T) -> None:\n"
    "        # WRONG: silently overwrites duplicates instead of keeping the first,\n"
    "        # so add() order semantics differ from the contract\n"
    "        self._items[self._key_fn(item)] = item\n\n"
    "    def get(self, key: str) -> Optional[T]:\n"
    "        return self._items.get(key)\n\n"
    "    def all(self) -> List[T]:\n"
    "        return list(self._items.values())\n\n\n"
    "def seed(repo, users) -> None:\n"
    "    for u in users:\n"
    "        repo.add(u)"
)

write_checkpoint(
    MOD, "pa-checkpoint-typing",
    "Checkpoint: Typing",
    "Design a generic Repository protocol and its in-memory implementation.",
    30,
    """
## Checkpoint — a typed repository

Build:

1. `class Repository(Protocol[T])` with `add(item: T) -> None`,
   `get(key: str) -> Optional[T]`, `all() -> List[T]` (protocol bodies use `...`).
2. `class MemoryRepository(Generic[T])` implementing it, constructed with a
   `key_fn` used to derive each item's key.
3. `seed(repo, users)` adding every user.

Contract detail: `add` keeps the FIRST item for a key (later duplicates are
ignored — get() and all() still return the first).
""",
    "Checkpoint: Typing",
    "Thiết kế Protocol Repository dạng generic và bản cài trong bộ nhớ.",
    """
## Checkpoint — repository có kiểu

Dựng:

1. `class Repository(Protocol[T])` với `add(item: T) -> None`,
   `get(key: str) -> Optional[T]`, `all() -> List[T]` (thân protocol dùng `...`).
2. `class MemoryRepository(Generic[T])` cài protocol đó, khởi tạo với `key_fn`
   dùng để suy ra key của từng item.
3. `seed(repo, users)` thêm mọi user.

Chi tiết hợp đồng: `add` giữ item ĐẦU TIÊN cho một key (bản sao sau bị bỏ qua —\nget() và all() vẫn trả về item đầu).
""",
    challenge(
        "pa-checkpoint-typing",
        "Generic Repository protocol + memory implementation",
        "Implement Repository(Protocol[T]), MemoryRepository(Generic[T]) (key_fn constructor; first-add-wins on duplicate keys), and seed(repo, users).",
        "from typing import Protocol, TypeVar, Generic, List, Optional\n\nT = TypeVar('T')\n\n# TODO: Repository, MemoryRepository, seed",
        [
            ("protocol-shaped repository works",
             "class User:\n    def __init__(self, uid, name):\n        self.uid, self.name = uid, name\n    def __eq__(self, other):\n        return isinstance(other, User) and self.uid == other.uid and self.name == other.name\n    def __repr__(self):\n        return f'User({self.uid})'\n\nrepo = MemoryRepository(key_fn=lambda u: str(u.uid))\nseed(repo, [User(1, 'a'), User(2, 'b')])\nassert repo.get('1') == User(1, 'a')\nassert repo.get('99') is None\nassert len(repo.all()) == 2\nprint('ok')",
             "Protocol bodies are ...; MemoryRepository stores items keyed by key_fn(item)."),
            ("first-add-wins on duplicate keys",
             "repo = MemoryRepository(key_fn=lambda u: str(u.uid))\nseed(repo, [User(1, 'first'), User(1, 'second'), User(2, 'x')])\nassert repo.get('1').name == 'first', 'duplicate keys must keep the first item'\nassert len(repo.all()) == 2\nprint('ok')",
             "Only insert when the key is absent — setdefault or an explicit check."),
        ],
        level="build",
    ),
    vi_challenge(
        "Protocol Repository generic + bản cài trong bộ nhớ",
        "Cài Repository(Protocol[T]), MemoryRepository(Generic[T]) (constructor nhận key_fn; key trùng thì giữ item đầu), và seed(repo, users).",
        [("Repository hình dạng protocol hoạt động", "Thân protocol là ...; MemoryRepository lưu item theo key_fn(item)."),
         ("Key trùng giữ item đầu", "Chỉ chèn khi key chưa có — setdefault hoặc kiểm tra tường minh.")],
    ),
    solution=REPO_REF,
    wrong=REPO_WRONG,
)

print("module 3 complete")
