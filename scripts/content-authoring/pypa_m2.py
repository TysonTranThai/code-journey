#!/usr/bin/env python3
"""Module 2: metaprogramming — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "metaprogramming"

write_module(
    MOD,
    "Metaprogramming & Code That Writes Code",
    "Decorators, __init_subclass__, metaclasses, and registries — with a professional bias for the simplest tool that works.",
    "Metaprogramming & mã viết ra mã",
    "Decorator, __init_subclass__, metaclass và registry — với thiên hướng chuyên nghiệp: dùng công cụ đơn giản nhất có thể.",
    ["decorators-deep", "class-hooks-metaclasses", "registries-plugins"],
    ["pa-p2-decorator-practice", "pa-p2-registry-practice", "pa-p2-plugin-project"],
)

# ── lesson 1: decorators deep ────────────────────────────────────────────────
L1_EN = """
## Decorators beyond the basics

You know `@decorator` wraps a function. Advanced usage is about **preserving
identity**, **taking arguments**, and **decorating classes**.

```python
import functools

def timed(fn):
    @functools.wraps(fn)                # keep __name__, __doc__, __wrapped__
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"{fn.__name__}: {time.perf_counter() - start:.6f}s")
    return wrapper
```

Without `functools.wraps`, the wrapper *replaces* the function's metadata —
breaking introspection, docs, and debuggers.

**Decorator factories** take arguments and return the real decorator:

```python
def retry(times):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    if attempt == times:
                        raise
        return wrapper
    return decorator

@retry(times=3)
def flaky(): ...
```

**Class decorators** receive and return the class — a lightweight alternative
to mixins or metaclasses when you only need to patch or register:

```python
def final(cls):
    cls.__final__ = True
    return cls

@final
class Config: ...
```

One subtlety professionals hit in production: a decorator applied to *methods*
must survive descriptor lookup — `functools.wraps` copies `__wrapped__`, so
`inspect.signature` still sees the original parameters. And stacking order is
bottom-up: the decorator closest to the `def` runs first (outermost last).
"""

L1_VI = L1_EN.replace(
    "## Decorators beyond the basics",
    "## Decorator vượt ngoài cơ bản",
).replace(
    "You know `@decorator` wraps a function. Advanced usage is about **preserving\nidentity**, **taking arguments**, and **decorating classes**.",
    "Bạn biết `@decorator` bọc một hàm. Dùng nâng cao là về **giữ nguyên bản thể**,\n**nhận tham số**, và **bọc class**.",
).replace(
    "Without `functools.wraps`, the wrapper *replaces* the function's metadata —\nbreaking introspection, docs, and debuggers.",
    "Không có `functools.wraps`, wrapper *thay thế* metadata của hàm — làm hỏng\nintrospection, tài liệu và debugger.",
).replace(
    "**Decorator factories** take arguments and return the real decorator:",
    "**Decorator factory** nhận tham số và trả về decorator thật:",
).replace(
    "**Class decorators** receive and return the class — a lightweight alternative\nto mixins or metaclasses when you only need to patch or register:",
    "**Decorator class** nhận vào và trả về class — lựa chọn nhẹ nhàng thay cho\nmixin hay metaclass khi bạn chỉ cần vá hoặc đăng ký:",
).replace(
    "One subtlety professionals hit in production: a decorator applied to *methods*\nmust survive descriptor lookup — `functools.wraps` copies `__wrapped__`, so\n`inspect.signature` still sees the original parameters. And stacking order is\nbottom-up: the decorator closest to the `def` runs first (outermost last).",
    "Một điểm tinh vi mà dân production hay gặp: decorator gắn lên *method* phải\nsống sót qua descriptor lookup — `functools.wraps` copy `__wrapped__`, nên\n`inspect.signature` vẫn thấy tham số gốc. Thứ tự xếp lớp là từ dưới lên:\ndecorator gần `def` nhất chạy trước (ngoài cùng chạy sau).",
)

write_lesson(
    MOD, "decorators-deep",
    "Decorators: identity, factories, class decorators",
    "Write decorators that preserve metadata, take arguments, and wrap classes.",
    22, L1_EN,
    "Decorator: bản thể, factory, decorator class",
    "Viết decorator giữ nguyên metadata, nhận tham số, và bọc class.",
    L1_VI,
)

# ── lesson 2: class hooks + metaclasses ──────────────────────────────────────
L2_EN = """
## Class creation hooks — and real metaclasses

Python gives you three hooks into class creation, in increasing power and cost:

1. **`__init_subclass__`** — a plain inherited method called on the parent for
   every new subclass. No magic syntax. Right choice for registration,
   validation, and auto-wiring.
2. **Class decorators** — transform a class after its body executes. Right
   choice for one-shot patching, but nothing runs at *attribute* definition
   time and subclasses do not inherit the effect.
3. **Metaclasses** — control the *type* of the class itself: intercept class
   creation via `Meta.__new__`, modify the namespace before the class exists,
   enforce invariants across a hierarchy.

```python
class FrozenMeta(type):
    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        allowed = set(ns.get("__annotations__", {}))
        def _setattr(self, key, value):
            if key not in allowed:
                raise AttributeError(f"frozen: cannot set {key!r}")
            object.__setattr__(self, key, value)
        cls.__setattr__ = _setattr
        return cls
```

A metaclass is justified when the *contract* belongs to the whole hierarchy and
must hold even for code that forgets to opt in — ORMs, ABCs (`abc.ABCMeta`),
enum (`EnumMeta`), and interface enforcement are the canonical cases.

The professional bar, from the standard library's own history: `__init_subclass__`
and `__set_name__` were added precisely so ordinary Python code could do what
previously required a metaclass. Reach for the metaclass only when you must
control the class object itself — namespaces, `__slots__` synthesis, class-level
validation with custom keyword arguments consumed by the metaclass.
"""

L2_VI = L2_EN.replace(
    "## Class creation hooks — and real metaclasses",
    "## Các móc tạo class — và metaclass đích thực",
).replace(
    "Python gives you three hooks into class creation, in increasing power and cost:",
    "Python cho bạn ba móc vào lúc tạo class, quyền lực và cái giá tăng dần:",
).replace(
    "1. **`__init_subclass__`** — a plain inherited method called on the parent for\n   every new subclass. No magic syntax. Right choice for registration,\n   validation, and auto-wiring.\n2. **Class decorators** — transform a class after its body executes. Right\n   choice for one-shot patching, but nothing runs at *attribute* definition\n   time and subclasses do not inherit the effect.\n3. **Metaclasses** — control the *type* of the class itself: intercept class\n   creation via `Meta.__new__`, modify the namespace before the class exists,\n   enforce invariants across a hierarchy.",
    "1. **`__init_subclass__`** — method kế thừa bình thường, được gọi trên cha cho\n   mỗi subclass mới. Không cú pháp đặc biệt. Lựa chọn đúng cho đăng ký,\n   kiểm tra hợp lệ, tự nối dây.\n2. **Decorator class** — biến đổi class sau khi thân class chạy. Đúng cho việc vá\n   một lần, nhưng không có gì chạy lúc *định nghĩa attribute* và subclass không\n   thừa hưởng hiệu ứng.\n3. **Metaclass** — kiểm soát chính *type* của class: chặn việc tạo class qua\n   `Meta.__new__`, sửa namespace trước khi class tồn tại, ép bất biến trên cả\n   hệ thứ tự.",
).replace(
    "A metaclass is justified when the *contract* belongs to the whole hierarchy and\nmust hold even for code that forgets to opt in — ORMs, ABCs (`abc.ABCMeta`),\nenum (`EnumMeta`), and interface enforcement are the canonical cases.",
    "Metaclass chỉ chính đáng khi *hợp đồng* thuộc về cả hệ thứ tự và phải được giữ\nngay cả với code quên chủ động tham gia — ORM, ABC (`abc.ABCMeta`), enum\n(`EnumMeta`), và ép interface là những trường hợp kinh điển.",
).replace(
    "The professional bar, from the standard library's own history: `__init_subclass__`\nand `__set_name__` were added precisely so ordinary Python code could do what\npreviously required a metaclass. Reach for the metaclass only when you must\ncontrol the class object itself — namespaces, `__slots__` synthesis, class-level\nvalidation with custom keyword arguments consumed by the metaclass.",
    "Thước đo chuyên nghiệp, ngay từ lịch sử của thư viện chuẩn: `__init_subclass__`\nvà `__set_name__` được thêm vào chính là để code Python bình thường làm được\nnhững việc trước đây phải cần metaclass. Chỉ chạm tới metaclass khi bạn buộc phải\nkiểm soát bản thân đối tượng class — namespace, tổng hợp `__slots__`, kiểm tra\ncấp class với keyword argument riêng mà metaclass tiêu thụ.",
)

write_lesson(
    MOD, "class-hooks-metaclasses",
    "__init_subclass__, class decorators, metaclasses",
    "Choose the right class-creation hook; write a metaclass when you must.",
    24, L2_EN,
    "__init_subclass__, decorator class, metaclass",
    "Chọn đúng móc tạo class; viết metaclass khi thực sự cần.",
    L2_VI,
)

# ── lesson 3: registries & plugins ───────────────────────────────────────────
L3_EN = """
## Registries and plugin patterns

A **registry** maps keys to implementations discovered at import time. It is
the backbone of plugin systems: the core never imports the plugins; the
plugins import the core and register themselves.

Three registration styles, weakest to strongest:

```python
# 1. explicit registration call
REGISTRY = {}
def register(key):
    def deco(cls):
        REGISTRY[key] = cls
        return cls
    return deco

# 2. __init_subclass__ (auto-registration with inheritance)
class Handler:
    _sub = {}
    def __init_subclass__(cls, scheme=None, **kw):
        super().__init_subclass__(**kw)
        Handler._sub[scheme or cls.__name__.lower()] = cls

# 3. entry points (cross-package, used by pytest and console scripts)
# declared in pyproject.toml:
# [project.entry-points."cj.exporters"]
# csv = "myplug.csv:CsvExporter"
```

Entry points are how *installed distributions* plug into a host without the
host importing them eagerly — `importlib.metadata.entry_points()` loads them
lazily on demand.

Design rules that keep registries sane at scale:

- Fail fast on duplicate keys and missing required methods (validate at class
  creation, not first use).
- Keep the registry keyed by *stable, public* identifiers — never class names,
  which refactors break silently.
- Version the contract: a plugin written against protocol v1 should fail
  loudly, not subtly, on a v2 host.
"""

L3_VI = L3_EN.replace(
    "## Registries and plugin patterns",
    "## Registry và plugin pattern",
).replace(
    "A **registry** maps keys to implementations discovered at import time. It is\nthe backbone of plugin systems: the core never imports the plugins; the\nplugins import the core and register themselves.",
    "**Registry** ánh xạ khóa tới các bản cài đặt được phát hiện lúc import. Nó là\nxương sống của hệ plugin: phần lõi không bao giờ import plugin; plugin import\nlõi và tự đăng ký.",
).replace(
    "Three registration styles, weakest to strongest:",
    "Ba kiểu đăng ký, từ yếu tới mạnh:",
).replace(
    "Entry points are how *installed distributions* plug into a host without the\nhost importing them eagerly — `importlib.metadata.entry_points()` loads them\nlazily on demand.",
    "Entry point là cách các *distribution đã cài* cắm vào host mà host không cần\nimport chủ động — `importlib.metadata.entry_points()` nạp lười theo nhu cầu.",
).replace(
    "Design rules that keep registries sane at scale:",
    "Những nguyên tắc giúp registry không điên loạn khi phóng to:",
).replace(
    "- Fail fast on duplicate keys and missing required methods (validate at class\n  creation, not first use).\n- Keep the registry keyed by *stable, public* identifiers — never class names,\n  which refactors break silently.\n- Version the contract: a plugin written against protocol v1 should fail\n  loudly, not subtly, on a v2 host.",
    "- Thất bại nhanh với khóa trùng và method bắt buộc còn thiếu (kiểm tra lúc tạo\n  class, không phải lần dùng đầu tiên).\n- Giữ khóa registry bằng định danh *ổn định, công khai* — đừng bao giờ dùng tên\n  class, thứ mà refactor phá ngầm.\n- Đánh phiên bản hợp đồng: plugin viết cho protocol v1 phải thất bại ầm ĩ,\n  không phải âm thầm, trên host v2.",
)

write_lesson(
    MOD, "registries-plugins",
    "Registries, auto-registration, entry points",
    "Build the plugin machinery that frameworks are made of.",
    20, L3_EN,
    "Registry và plugin pattern",
    "Xây dựng cơ chế plugin — thứ tạo nên các framework.",
    L3_VI,
)

# ── practice 1: decorators ───────────────────────────────────────────────────
RETRY_REF = (
    "import functools\n\n\n"
    "def retry(times, exceptions=(Exception,)):\n"
    "    def decorator(fn):\n"
    "        @functools.wraps(fn)\n"
    "        def wrapper(*args, **kwargs):\n"
    "            wrapper.attempts = []\n"
    "            last = None\n"
    "            for attempt in range(1, times + 1):\n"
    "                wrapper.attempts.append(attempt)\n"
    "                try:\n"
    "                    return fn(*args, **kwargs)\n"
    "                except exceptions as e:\n"
    "                    last = e\n"
    "            raise last\n"
    "        return wrapper\n"
    "    return decorator"
)
RETRY_WRONG = (
    "import functools\n\n\n"
    "def retry(times, exceptions=(Exception,)):\n"
    "    def decorator(fn):\n"
    "        @functools.wraps(fn)\n"
    "        def wrapper(*args, **kwargs):\n"
    "            wrapper.attempts = []\n"
    "            last = None\n"
    "            for attempt in range(1, times + 1):\n"
    "                wrapper.attempts.append(attempt)\n"
    "                try:\n"
    "                    return fn(*args, **kwargs)\n"
    "                except exceptions as e:\n"
    "                    last = e\n"
    "            # WRONG: swallows the final failure instead of re-raising\n"
    "            return None\n"
    "        return wrapper\n"
    "    return decorator"
)

DATACLASS_REF = (
    "def dataclassish(cls):\n"
    "    fields = list(cls.__annotations__)\n\n"
    "    if '__init__' not in vars(cls):\n"
    "        def __init__(self, *args, __fields=tuple(fields), **kwargs):\n"
    "            if len(args) > len(__fields):\n"
    "                raise TypeError('too many arguments')\n"
    "            for name, value in zip(__fields, args):\n"
    "                setattr(self, name, value)\n"
    "            for name in __fields[len(args):]:\n"
    "                if name not in kwargs:\n"
    "                    raise TypeError(f'missing field: {name}')\n"
    "                setattr(self, name, kwargs.pop(name))\n"
    "            if kwargs:\n"
    "                raise TypeError(f'unexpected fields: {sorted(kwargs)}')\n"
    "        cls.__init__ = __init__\n\n"
    "    def __repr__(self):\n"
    "        inner = ', '.join(f'{f}={getattr(self, f)!r}' for f in fields)\n"
    "        return f'{type(self).__name__}({inner})'\n\n"
    "    def __eq__(self, other):\n"
    "        if not isinstance(other, type(self)) or not isinstance(self, type(other)):\n"
    "            return NotImplemented\n"
    "        return all(getattr(self, f) == getattr(other, f) for f in fields)\n\n"
    "    if '__repr__' not in vars(cls):\n"
    "        cls.__repr__ = __repr__\n"
    "    if '__eq__' not in vars(cls):\n"
    "        cls.__eq__ = __eq__\n"
    "    return cls\n\n\n"
    "@dataclassish\n"
    "class Point:\n"
    "    x: int\n"
    "    y: int\n\n\n"
    "@dataclassish\n"
    "class Named:\n"
    "    name: str\n\n"
    "    def __init__(self, name):\n"
    "        self.name = 'Dr ' + name"
)
DATACLASS_WRONG = (
    "def dataclassish(cls):\n"
    "    fields = list(cls.__annotations__)\n\n"
    "    def __init__(self, *args, **kwargs):\n"
    "        # WRONG: overwrites even a hand-written __init__ (breaks Named)\n"
    "        for name, value in zip(fields, args):\n"
    "            setattr(self, name, value)\n"
    "        for name, value in kwargs.items():\n"
    "            setattr(self, name, value)\n"
    "    cls.__init__ = __init__\n\n"
    "    def __repr__(self):\n"
    "        inner = ', '.join(f'{f}={getattr(self, f)!r}' for f in fields)\n"
    "        return f'{type(self).__name__}({inner})'\n"
    "    cls.__repr__ = __repr__\n"
    "    return cls\n\n\n"
    "@dataclassish\n"
    "class Point:\n"
    "    x: int\n"
    "    y: int\n\n\n"
    "@dataclassish\n"
    "class Named:\n"
    "    name: str\n\n"
    "    def __init__(self, name):\n"
    "        self.name = 'Dr ' + name"
)

write_practice(
    MOD, "pa-p2-decorator-practice",
    "Decorator Engineering",
    "Decorators that survive code review: identity preserved, arguments handled, class-aware.",
    "Kỹ thuật Decorator",
    "Decorator đủ sức qua code review: giữ bản thể, xử lý tham số, hiểu class.",
    "decorators-deep", 20, "advanced",
    [
        challenge(
            "pa-mt-decorator-factory",
            "Retry decorator factory",
            "Implement `retry(times, exceptions=(Exception,))` — a decorator FACTORY that returns a decorator making `fn` retry up to `times` total attempts:\n\n- only the given exception types trigger a retry; anything else propagates immediately\n- if all attempts fail, re-raise the LAST exception\n- preserve the function's metadata: `wrapped.__name__ == fn.__name__`\n- track attempts for observability: expose `wrapped.attempts` (list of ints, one entry per call)",
            "import functools\n\ndef retry(times, exceptions=(Exception,)):\n    # TODO: return a decorator\n    pass",
            [
                ("retries transient failures only",
                 "@retry(times=3, exceptions=(ValueError,))\ndef flaky(counter):\n    counter.append(1)\n    if len(counter) < 3:\n        raise ValueError('transient')\n    return 'ok'\n\nc = []\nassert flaky(c) == 'ok' and len(c) == 3, f'calls: {len(c)}'\nprint('ok')",
                 "Loop attempts inside the wrapper; return on success, re-raise the last error when attempts run out."),
                ("foreign exceptions propagate; metadata kept",
                 "calls = []\n@retry(times=5, exceptions=(ValueError,))\ndef boom():\n    calls.append(1)\n    raise KeyError('nope')\ntry:\n    boom()\nexcept KeyError:\n    pass\nelse:\n    raise AssertionError('KeyError must propagate immediately')\nassert len(calls) == 1, f'calls: {len(calls)}'\nassert boom.__name__ == 'boom'\n\n@retry(times=2, exceptions=(ValueError,))\ndef always_bad():\n    raise ValueError('dead')\ntry:\n    always_bad()\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('exhausted retries must re-raise the last error')\nassert always_bad.attempts == [1, 2], f'attempts: {always_bad.attempts}'\nprint('ok')",
                 "Catch only the declared exception tuple; functools.wraps for metadata; re-raise when attempts run out."),
            ],
            level="combination",
        ),
        challenge(
            "pa-mt-class-decorator",
            "Class decorator: auto-properties",
            "Implement `@dataclassish` — a class decorator that, for every attribute annotated in the class body (use `__annotations__`), synthesizes:\n\n- an `__init__` accepting exactly those fields as keyword-or-positional args in declaration order, assigning each\n- a `__repr__` as `Name(field=repr, ...)` in declaration order\n- an `__eq__` comparing type and all field values (False for other types)\n\nThe class may define its own `__init__` — in that case LEAVE it alone and only add repr/eq if missing.",
            "def dataclassish(cls):\n    # TODO\n    return cls\n\n@dataclassish\nclass Point:\n    x: int\n    y: int\n\n@dataclassish\nclass Named:\n    name: str\n\n    def __init__(self, name):\n        self.name = 'Dr ' + name",
            [
                ("synthesizes init and repr",
                 "p = Point(1, y=2)\nassert (p.x, p.y) == (1, 2)\nassert repr(p) == 'Point(x=1, y=2)', f'repr: {p!r}'\nassert Point(1, 2) == Point(1, 2)\nassert Point(1, 2) != Point(2, 1)\nassert (Point(1, 2) == 'x') is False\nprint('ok')",
                 "Read cls.__annotations__ keys in order; build __init__ via a normal function that assigns each field."),
                ("respects a hand-written __init__",
                 "n = Named('Alice')\nassert n.name == 'Dr Alice', 'user __init__ must win'\nprint('ok')",
                 "Check '__init__' in vars(cls) before synthesizing."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-mt-decorator-factory": vi_challenge(
            "Retry decorator factory",
            "Cài `retry(times, exceptions=(Exception,))` — một decorator FACTORY trả về decorator khiến `fn` thử lại tối đa `times` lần:\n\n- chỉ các kiểu exception đã khai báo mới kích hoạt retry; loại khác lan truyền ngay\n- nếu mọi lần thử đều thất bại, raise lại exception CUỐI\n- giữ metadata của hàm: `wrapped.__name__ == fn.__name__`\n- theo dõi số lần thử: lộ `wrapped.attempts` (danh sách int, một phần tử mỗi lần gọi)",
            [("Chỉ retry lỗi tạm thời", "Vòng lặp các lần thử nằm trong wrapper; thành công thì return, hết lượt thì raise lại lỗi cuối."),
             ("Exception lạ lan truyền; giữ metadata", "Chỉ bắt tuple exception đã khai báo; functools.wraps cho metadata; hết lượt thì raise lại.")],
        ),
        "pa-mt-class-decorator": vi_challenge(
            "Decorator class: tự sinh property",
            "Cài `@dataclassish` — decorator class mà, với mỗi attribute được annotate trong thân class (dùng `__annotations__`), tự sinh:\n\n- một `__init__` nhận đúng các field đó theo thứ tự khai báo, gán từng field\n- một `__repr__` dạng `Name(field=repr, ...)` theo thứ tự khai báo\n- một `__eq__` so sánh kiểu và mọi giá trị field (False với kiểu khác)\n\nNếu class tự định nghĩa `__init__` thì GIỮ NGUYÊN, chỉ thêm repr/eq nếu còn thiếu.",
            [("Tự sinh init và repr", "Đọc các key của cls.__annotations__ theo thứ tự; dựng __init__ bằng hàm thường gán từng field."),
             ("Tôn trọng __init__ viết tay", "Kiểm tra '__init__' in vars(cls) trước khi tự sinh.")],
        ),
    },
    solutions=[
        ("pa-mt-decorator-factory", RETRY_REF, RETRY_WRONG),
        ("pa-mt-class-decorator", DATACLASS_REF, DATACLASS_WRONG),
    ],
)

# ── practice 2: registries / metaclass ───────────────────────────────────────
REGISTRY_REF = (
    "class Handler:\n"
    "    _handlers = {}\n\n"
    "    def __init_subclass__(cls, **kwargs):\n"
    "        super().__init_subclass__(**kwargs)\n"
    "        scheme = getattr(cls, 'scheme', None)\n"
    "        if not isinstance(scheme, str) or not scheme:\n"
    "            raise TypeError(f'{cls.__name__} must define a nonempty scheme')\n"
    "        if 'handle' not in vars(cls):\n"
    "            raise TypeError(f'{cls.__name__} must implement handle()')\n"
    "        if scheme in Handler._handlers:\n"
    "            raise ValueError(f'duplicate scheme: {scheme}')\n"
    "        Handler._handlers[scheme] = cls\n\n"
    "    @classmethod\n"
    "    def dispatch(cls, scheme, value):\n"
    "        return cls._handlers[scheme]().handle(value)\n\n\n"
    "class Upper(Handler):\n"
    "    scheme = 'upper'\n\n"
    "    def handle(self, value):\n"
    "        return value.upper()"
)
REGISTRY_WRONG = REGISTRY_REF.replace(
    "        if scheme in Handler._handlers:\n            raise ValueError(f'duplicate scheme: {scheme}')\n        Handler._handlers[scheme] = cls",
    "        # WRONG: duplicates overwrite silently instead of failing fast\n        Handler._handlers[scheme] = cls",
)

FROZEN_REF = (
    "class FrozenMeta(type):\n"
    "    def __new__(mcls, name, bases, ns):\n"
    "        cls = super().__new__(mcls, name, bases, ns)\n"
    "        declared = set()\n"
    "        for b in reversed(cls.__mro__):\n"
    "            declared.update(getattr(b, '__annotations__', {}) or {})\n"
    "        declared.discard('__module__')\n"
    "        declared.discard('__qualname__')\n\n"
    "        def _setattr(self, key, value):\n"
    "            if key not in declared:\n"
    "                raise AttributeError(f'frozen: cannot set {key!r}')\n"
    "            object.__setattr__(self, key, value)\n"
    "        cls.__setattr__ = _setattr\n"
    "        return cls\n\n"
    "    brand = 'frozen'"
)
FROZEN_WRONG = (
    "class FrozenMeta(type):\n"
    "    def __new__(mcls, name, bases, ns):\n"
    "        cls = super().__new__(mcls, name, bases, ns)\n"
    "        # WRONG: reads only the class's own annotations after creation —\n"
    "        # subclasses lose the parents' declared names\n"
    "        declared = set(getattr(cls, '__annotations__', {}) or {})\n\n"
    "        def _setattr(self, key, value):\n"
    "            if key not in declared:\n"
    "                raise AttributeError(f'frozen: cannot set {key!r}')\n"
    "            object.__setattr__(self, key, value)\n"
    "        cls.__setattr__ = _setattr\n"
    "        return cls\n\n"
    "    brand = 'frozen'"
)

write_practice(
    MOD, "pa-p2-registry-practice",
    "Registry Mechanics",
    "Auto-registration with validation — the small machinery frameworks run on.",
    "Cơ chế Registry",
    "Tự đăng ký kèm kiểm tra hợp lệ — cỗ máy nhỏ mà framework dựa vào.",
    "class-hooks-metaclasses", 20, "advanced",
    [
        challenge(
            "pa-mt-validated-registry",
            "Validated handler registry",
            "Implement `class Handler` with `__init_subclass__` that auto-registers subclasses and VALIDATES them at class-creation time:\n\n- subclass must define `scheme` (a nonempty str) and `handle(value)` — raise `TypeError` at class definition otherwise\n- duplicate `scheme` values raise `ValueError` at class definition\n- `Handler.dispatch(scheme, value)` calls the right handler's `handle` and returns its result; unknown scheme raises `KeyError`\n- the base class itself is not registered",
            "class Handler:\n    _handlers = {}\n\n    # TODO: __init_subclass__ + dispatch\n\nclass Upper(Handler):\n    scheme = 'upper'\n    def handle(self, value):\n        return value.upper()",
            [
                ("registers and dispatches",
                 "u = Upper()\nassert Handler.dispatch('upper', 'hi') == 'HI', 'dispatch must reach the handler'\nprint('ok')",
                 "Registration happens in __init_subclass__; dispatch looks up by scheme and calls an instance method."),
                ("validation fails fast",
                 "try:\n    class NoScheme(Handler):\n        def handle(self, value): return value\nexcept TypeError:\n    pass\nelse:\n    raise AssertionError('missing scheme must raise TypeError at class creation')\ntry:\n    class Dup(Handler):\n        scheme = 'upper'\n        def handle(self, value): return value\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('duplicate scheme must raise ValueError')\nprint('ok')",
                 "Both checks run inside __init_subclass__ — before the class body finishes."),
            ],
            level="independent",
        ),
        challenge(
            "pa-mt-metaclass-frozen",
            "A metaclass, when it is the right tool",
            "Implement `class FrozenMeta(type)` enforcing that instances only ever set the attributes DECLARED in the class body annotations:\n\n- setting an undeclared attribute raises `AttributeError` at ANY time (init or later)\n- declared attributes are freely settable and readable\n- `Vec.brand` must equal 'frozen' on every class using the metaclass (the metaclass itself may set class attributes)\n- this must apply to subclasses too — that is why it is a metaclass, not __init_subclass__",
            "class FrozenMeta(type):\n    # TODO: __new__ installs a strict __setattr__ on each class\n    pass",
            [
                ("declared attrs work, undeclared rejected",
                 "class Vec(metaclass=FrozenMeta):\n    x: int\n    y: int\n\nv = Vec()\nv.x, v.y = 1, 2\nassert (v.x, v.y) == (1, 2)\ntry:\n    v.z = 9\nexcept AttributeError:\n    pass\nelse:\n    raise AssertionError('undeclared attribute must raise AttributeError')\nassert Vec.brand == 'frozen'\nprint('ok')",
                 "In Meta.__new__, read ns['__annotations__'] keys and install a __setattr__ closing over that set."),
                ("inherited by subclasses",
                 "class Vec(metaclass=FrozenMeta):\n    x: int\n\nclass Vec3(Vec):\n    z: int\n\np = Vec3()\np.x = p.z = 1\ntry:\n    p.w = 2\nexcept AttributeError:\n    pass\nelse:\n    raise AssertionError('subclasses must inherit the frozen contract')\nprint('ok')",
                 "Subclass namespaces carry their own __annotations__; merge with the parents' declared names."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-mt-validated-registry": vi_challenge(
            "Registry có kiểm tra hợp lệ",
            "Cài `class Handler` với `__init_subclass__` tự đăng ký subclass và KIỂM TRA ngay khi tạo class:\n\n- subclass phải định nghĩa `scheme` (str khác rỗng) và `handle(value)` — nếu thiếu, raise `TypeError` ngay lúc định nghĩa class\n- `scheme` trùng nhau raise `ValueError` ngay lúc định nghĩa class\n- `Handler.dispatch(scheme, value)` gọi `handle` của handler đúng và trả về kết quả; scheme lạ raise `KeyError`\n- bản thân base class không được đăng ký",
            [("Đăng ký và dispatch", "Đăng ký diễn ra trong __init_subclass__; dispatch tra theo scheme rồi gọi method của instance."),
             ("Kiểm tra hợp lệ thất bại nhanh", "Cả hai phép kiểm tra nằm trong __init_subclass — trước khi thân class kết thúc.")],
        ),
        "pa-mt-metaclass-frozen": vi_challenge(
            "Metaclass, khi nó đúng là công cụ",
            "Cài `class FrozenMeta(type)` ép rằng instance chỉ có thể set những attribute ĐƯỢC KHAI BÁO bằng annotation trong thân class:\n\n- set attribute chưa khai báo raise `AttributeError` ở MỌI thời điểm (khi init hay sau này)\n- attribute đã khai báo được set và đọc tự do\n- `Vec.brand` phải bằng 'frozen' trên mọi class dùng metaclass này (bản thân metaclass có thể đặt attribute của class)\n- điều này phải áp dụng cho cả subclass — vì thế mới là metaclass chứ không phải __init_subclass__",
            [("Attribute khai báo thì ổn, lạ thì bị chặn", "Trong Meta.__new__, đọc các key của ns['__annotations__'] và cài một __setattr__ đóng trên tập tên đó."),
             ("Thừa hưởng qua subclass", "Namespace của subclass mang __annotations__ riêng; hợp nhất với các tên đã khai báo của cha.")],
        ),
    },
    solutions=[
        ("pa-mt-validated-registry", REGISTRY_REF, REGISTRY_WRONG),
        ("pa-mt-metaclass-frozen", FROZEN_REF, FROZEN_WRONG),
    ],
)

# ── practice 3 + project: plugin framework ───────────────────────────────────
PLUGIN_REF = (
    "import json\n\n\n"
    "class ExporterBase:\n"
    "    _registry = {}\n\n"
    "    def __init_subclass__(cls, **kwargs):\n"
    "        super().__init_subclass__(**kwargs)\n"
    "        name = getattr(cls, 'name', None)\n"
    "        if not isinstance(name, str) or not name:\n"
    "            raise TypeError(f'{cls.__name__} must define a nonempty name')\n"
    "        if 'export' not in vars(cls):\n"
    "            raise TypeError(f'{cls.__name__} must implement export()')\n"
    "        if name in ExporterBase._registry:\n"
    "            raise ValueError(f'duplicate exporter name: {name}')\n"
    "        ExporterBase._registry[name] = cls\n\n"
    "    @classmethod\n"
    "    def create(cls, name):\n"
    "        return cls._registry[name]()\n\n"
    "    @classmethod\n"
    "    def names(cls):\n"
    "        return sorted(cls._registry)\n\n\n"
    "class CsvExporter(ExporterBase):\n"
    "    name = 'csv'\n\n"
    "    def export(self, rows):\n"
    "        return '\\n'.join(','.join(f'{k}={v}' for k, v in row.items()) for row in rows)\n\n\n"
    "class JsonLinesExporter(ExporterBase):\n"
    "    name = 'jsonl'\n\n"
    "    def export(self, rows):\n"
    "        return '\\n'.join(json.dumps(row, separators=(',', ':')) for row in rows)"
)
PLUGIN_WRONG = PLUGIN_REF.replace(
    "        if name in ExporterBase._registry:\n            raise ValueError(f'duplicate exporter name: {name}')\n        ExporterBase._registry[name] = cls",
    "        # WRONG: last-writer-wins instead of rejecting duplicates\n        ExporterBase._registry[name] = cls",
)

write_practice(
    MOD, "pa-p2-plugin-project",
    "Project: Plugin Framework",
    "A working exporter plugin system: contract, registration, dispatch, and a hostile registration test.",
    "Project: Plugin Framework",
    "Một hệ plugin exporter hoạt động thật: hợp đồng, đăng ký, dispatch và bài test đăng ký phản chủ.",
    "registries-plugins", 30, "advanced",
    [
        challenge(
            "pa-mt-plugin-framework",
            "Exporter plugin framework",
            "Build a small plugin framework. The host provides `ExporterBase` (below). Plugins subclass it and auto-register.\n\nRequirements:\n\n1. `ExporterBase.__init_subclass__` registers subclasses by their `name` attribute (nonempty str, unique — duplicates raise `ValueError` at definition time).\n2. Every exporter must implement `export(rows)` returning a STRING. If a subclass lacks `export`, raise `TypeError` at definition time.\n3. `ExporterBase.create(name)` returns an instance or raises `KeyError`.\n4. `ExporterBase.names()` returns a sorted list of registered names.\n5. Provide two built-in plugins: `CsvExporter` (name='csv', rows of dicts joined as 'k1=v1,k2=v2' with rows on newlines) and `JsonLinesExporter` (name='jsonl', one compact JSON object per line).\n6. Hostile test: registering a plugin named 'csv' again must raise `ValueError`; a plugin missing `export` must raise `TypeError`.",
            "import json\n\n\nclass ExporterBase:\n    # TODO: registration machinery + create/names\n    pass\n\n\n# TODO: CsvExporter and JsonLinesExporter",
            [
                ("built-ins register and produce output",
                 "assert ExporterBase.names() == ['csv', 'jsonl'], f'names: {ExporterBase.names()}'\ncsv_out = ExporterBase.create('csv').export([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])\nassert csv_out == 'a=1,b=2\\na=3,b=4', f'csv: {csv_out!r}'\njl_out = ExporterBase.create('jsonl').export([{'a': 1}, {'b': 'x'}])\nlines = jl_out.splitlines()\nassert len(lines) == 2 and json.loads(lines[0]) == {'a': 1} and json.loads(lines[1]) == {'b': 'x'}\nprint('ok')",
                 "csv row = fields in dict order joined with ',' as k=v; jsonl = json.dumps(obj, separators=(',', ':')) per line."),
                ("hostile registrations fail fast",
                 "try:\n    class Csv2(ExporterBase):\n        name = 'csv'\n        def export(self, rows): return ''\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('duplicate name must raise ValueError')\ntry:\n    class Broken(ExporterBase):\n        name = 'broken'\nexcept TypeError:\n    pass\nelse:\n    raise AssertionError('missing export must raise TypeError')\ntry:\n    ExporterBase.create('nope')\nexcept KeyError:\n    pass\nelse:\n    raise AssertionError('unknown name must raise KeyError')\nprint('ok')",
                 "All three validations live in __init_subclass__ + a dict lookup in create()."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-mt-plugin-framework": vi_challenge(
            "Framework plugin Exporter",
            "Dựng một framework plugin nhỏ. Host cung cấp `ExporterBase` (bên dưới). Plugin kế thừa và tự đăng ký.\n\nYêu cầu:\n\n1. `ExporterBase.__init_subclass__` đăng ký subclass theo attribute `name` (str khác rỗng, duy nhất — trùng raise `ValueError` ngay lúc định nghĩa).\n2. Mọi exporter phải cài `export(rows)` trả về STRING. Thiếu `export` thì raise `TypeError` lúc định nghĩa.\n3. `ExporterBase.create(name)` trả về một instance hoặc raise `KeyError`.\n4. `ExporterBase.names()` trả về danh sách tên đã đăng ký, đã sort.\n5. Cung cấp hai plugin sẵn có: `CsvExporter` (name='csv', các row là dict nối thành 'k1=v1,k2=v2', row cách nhau bằng xuống dòng) và `JsonLinesExporter` (name='jsonl', mỗi dòng một JSON object gọn).\n6. Test phản chủ: đăng ký plugin tên 'csv' lần nữa phải raise `ValueError`; plugin thiếu `export` phải raise `TypeError`.",
            [("Plugin sẵn có đăng ký và chạy", "csv row = các field theo thứ tự dict nối bằng ',' dạng k=v; jsonl = json.dumps(obj, separators=(',', ':')) mỗi dòng."),
             ("Đăng ký phản chủ thất bại nhanh", "Cả ba phép kiểm tra nằm trong __init_subclass__ + tra dict trong create().")],
        ),
    },
    solutions=[("pa-mt-plugin-framework", PLUGIN_REF, PLUGIN_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
TIMED_REF = (
    "def timed(cls):\n"
    "    import functools, time\n"
    "    for name, fn in list(vars(cls).items()):\n"
    "        if callable(fn) and not name.startswith('_'):\n"
    "            def make(f, fname):\n"
    "                @functools.wraps(f)\n"
    "                def wrapper(self, *a, **kw):\n"
    "                    start = time.perf_counter()\n"
    "                    try:\n"
    "                        return f(self, *a, **kw)\n"
    "                    finally:\n"
    "                        type(self).__timings__.setdefault(fname, []).append(time.perf_counter() - start)\n"
    "                return wrapper\n"
    "            setattr(cls, name, make(fn, name))\n"
    "    if not hasattr(cls, '__timings__'):\n"
    "        cls.__timings__ = {}\n"
    "    return cls\n\n\n"
    "@timed\n"
    "class Service:\n"
    "    def work(self, n):\n"
    "        total = 0\n"
    "        for i in range(n):\n"
    "            total += i\n"
    "        return total\n\n"
    "    def _private(self):\n"
    "        return 'hidden'"
)
TIMED_WRONG = (
    "def timed(cls):\n"
    "    import functools, time\n"
    "    for name, fn in list(vars(cls).items()):\n"
    "        if callable(fn) and not name.startswith('_'):\n"
    "            # WRONG: wraps but never records any timing\n"
    "            def make(f):\n"
    "                @functools.wraps(f)\n"
    "                def wrapper(self, *a, **kw):\n"
    "                    return f(self, *a, **kw)\n"
    "                return wrapper\n"
    "            setattr(cls, name, make(fn))\n"
    "    if not hasattr(cls, '__timings__'):\n"
    "        cls.__timings__ = {}\n"
    "    return cls\n\n\n"
    "@timed\n"
    "class Service:\n"
    "    def work(self, n):\n"
    "        total = 0\n"
    "        for i in range(n):\n"
    "            total += i\n"
    "        return total\n\n"
    "    def _private(self):\n"
    "        return 'hidden'"
)

write_checkpoint(
    MOD, "pa-checkpoint-metaprogramming",
    "Checkpoint: Metaprogramming",
    "A class decorator that instruments every public method — the bridge between decorators and frameworks.",
    30,
    """
## Checkpoint — instrument a class

Write `@timed`, a **class decorator** that wraps every public method
(not starting with `_`) of the decorated class so that each call's wall time
is appended to `cls.__timings__[method_name]` (a list, created on demand).

Requirements:

- method names stay correct on the wrapper (`__name__` preserved)
- private/dunder methods are untouched
- works for any class (the decorator must not hardcode names)
- timings must accumulate across instances

This is the exact pattern profilers, metrics libraries, and tracing hooks use
when they cannot ask you to edit every method.
""",
    "Checkpoint: Metaprogramming",
    "Decorator class đo mọi public method — cây cầu giữa decorator và framework.",
    """
## Checkpoint — đo đạc một class

Viết `@timed`, một **decorator class** bọc mọi public method (không bắt đầu bằng\n`_`) của class được trang trí sao cho thời gian thực thi của mỗi lần gọi được\nappend vào `cls.__timings__[tên_method]` (một list, tạo khi cần).

Yêu cầu:

- tên method vẫn đúng trên wrapper (`__name__` được giữ)
- method riêng tư/dunder không bị đụng tới
- hoạt động với mọi class (decorator không được hardcode tên)
- timings cộng dồn qua nhiều instance

Đây chính là pattern mà profiler, thư viện metrics và tracing hook dùng khi\nkhông thể yêu cầu bạn sửa từng method một.
""",
    challenge(
        "pa-checkpoint-metaprogramming",
        "@timed class instrumentation",
        "Implement the @timed class decorator per the checkpoint spec: wraps every public method, appends per-call durations (seconds, float) to cls.__timings__[name], preserves __name__, skips dunder/private methods, accumulates across instances.",
        "# TODO: implement timed(cls)\n\n\n@timed\nclass Service:\n    def work(self, n):\n        total = 0\n        for i in range(n):\n            total += i\n        return total\n\n    def _private(self):\n        return 'hidden'",
        [
            ("public methods are timed, dunders not",
             "s = Service()\ns.work(1000)\ns.work(50000)\nassert 'work' in Service.__timings__, f'timings: {getattr(Service, \"__timings__\", None)}'\nassert len(Service.__timings__['work']) == 2\nassert all(isinstance(t, float) and t >= 0 for t in Service.__timings__['work'])\nassert '_private' not in Service.__timings__\nassert Service.work.__name__ == 'work'\nprint('ok')",
             "Iterate vars(cls) once, wrap callables whose name does not start with '_', store timings on the CLASS."),
            ("accumulates across instances; private untouched",
             "Service.__timings__.clear()\nService().work(10)\nService().work(10)\nassert len(Service.__timings__['work']) == 2, 'must accumulate across instances'\np = Service()\nassert p._private() == 'hidden'\nassert '_private' not in Service.__timings__\nprint('ok')",
             "Timings live on the class attribute, shared by all instances."),
        ],
        level="build",
    ),
    vi_challenge(
        "@timed đo đạc class",
        "Cài decorator class @timed theo đặc tả checkpoint: bọc mọi public method, append thời gian từng lần gọi (giây, số thực) vào cls.__timings__[name], giữ __name__, bỏ qua method dunder/riêng tư, cộng dồn qua nhiều instance.",
        [("Method public được đo, dunder thì không", "Duyệt vars(cls) một lần, bọc các callable có tên không bắt đầu bằng '_', lưu timings trên CLASS."),
         ("Cộng dồn qua nhiều instance; riêng tư không đụng tới", "Timings nằm trên attribute của class, dùng chung cho mọi instance.")],
    ),
    solution=TIMED_REF,
    wrong=TIMED_WRONG,
)

print("module 2 complete")
