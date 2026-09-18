#!/usr/bin/env python3
"""Module 1: data-model-protocols — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "data-model-protocols"

write_module(
    MOD,
    "The Data Model & Advanced Object Mechanics",
    "Advanced Python starts under the hood: how attribute lookup really works, what descriptors do to classes, how MRO resolves multiple inheritance, and how to build objects that behave like the built-ins.",
    "Data Model & cơ chế đối tượng nâng cao",
    "Python nâng cao bắt đầu từ bên dưới: attribute lookup thực sự hoạt động thế nào, descriptor thay đổi class ra sao, MRO xử lý đa kế thừa thế nào, và cách xây dựng đối tượng hành xử như built-in.",
    ["datamodel-attribute-lookup", "descriptors", "mro-cooperative-inheritance", "protocols-slots"],
    ["pa-p1-lookup-practice", "pa-p1-descriptor-practice", "pa-p1-mro-practice", "pa-p1-container-practice"],
)

# ── lesson 1: attribute lookup ───────────────────────────────────────────────
L1 = """
## Everything is a namespace lookup

You already know `obj.x` reads an attribute. Advanced Python means knowing the
**exact order** Python consults when resolving `obj.x`, and using that order as
a design tool.

For `obj.x` on an instance, Python (conceptually) tries, in order:

1. **Data descriptor** on the type (a descriptor defining `__set__` or
   `__delete__`) — e.g. `property`, most validators.
2. **Instance dictionary** — `obj.__dict__`.
3. **Non-data descriptor** on the type (defines only `__get__`) — e.g. plain
   functions (that is how bound methods are created!), `staticmethod`,
   `classmethod`, `functools.cached_property` before first call.
4. **`__getattr__` fallback** (if defined) — called only when normal lookup
   fails. Great for delegation, dangerous for hiding typos.

Two consequences worth internalizing:

- A data descriptor **beats** an instance `__dict__` entry. That is why
  `property` setters can validate even though you could assign `obj.x = 5`.
- Functions are non-data descriptors; the "bound method" you call is produced
  at lookup time by `__get__`. Nothing magic is stored on the instance.

```python
class Loud:
    def __getattr__(self, name):      # only called on MISS
        return f"<fallback for {name}>"

loud = Loud()
loud.real = 1
print(loud.real)                     # 1  (found normally)
print(loud.anything)                 # <fallback for anything>
```

Use `vars(obj)` / `obj.__dict__` to inspect the instance side, and
`type(obj).__mro__` to see the class side. When behavior surprises you, ask:
"which step of the lookup produced this?"
"""

write_lesson(
    MOD, "datamodel-attribute-lookup",
    "Attribute lookup, step by step",
    "Trace the four-stage lookup order and exploit it deliberately.",
    22, L1,
    "Attribute lookup từng bước",
    "Truy vết thứ tự bốn bước của attribute lookup và lợi dụng nó một cách có chủ đích.",
    L1.replace(
        "## Everything is a namespace lookup",
        "## Mọi thứ đều là tra cứu namespace",
    ).replace(
        "You already know `obj.x` reads an attribute. Advanced Python means knowing the\n**exact order** Python consults when resolving `obj.x`, and using that order as\na design tool.",
        "Bạn đã biết `obj.x` đọc một attribute. Python nâng cao nghĩa là biết **thứ tự\nchính xác** Python hỏi khi phân giải `obj.x`, và dùng thứ tự đó như một công cụ\nthiết kế.",
    ).replace(
        "Two consequences worth internalizing:",
        "Hai hệ quả đáng khắc cốt khắc da:",
    ).replace(
        "- A data descriptor **beats** an instance `__dict__` entry. That is why\n  `property` setters can validate even though you could assign `obj.x = 5`.\n- Functions are non-data descriptors; the \"bound method\" you call is produced\n  at lookup time by `__get__`. Nothing magic is stored on the instance.",
        "- Data descriptor **thắng** mục trong `__dict__` của instance. Đó là lý do\n  setter của `property` có thể kiểm tra dữ liệu dù bạn vẫn gán `obj.x = 5` được.\n- Hàm là non-data descriptor; \"bound method\" bạn gọi được tạo ra **tại thời điểm\n  tra cứu** bởi `__get__`. Không có gì kỳ diệu được lưu trên instance.",
    ).replace(
        "Use `vars(obj)` / `obj.__dict__` to inspect the instance side, and\n`type(obj).__mro__` to see the class side. When behavior surprises you, ask:\n\"which step of the lookup produced this?\"",
        "Dùng `vars(obj)` / `obj.__dict__` để xem phía instance, và `type(obj).__mro__`\nđể xem phía class. Khi hành vi khiến bạn ngạc nhiên, hãy hỏi: \"bước nào trong\nlookup đã tạo ra cái này?\"",
    ),
)

# ── lesson 2: descriptors ────────────────────────────────────────────────────
L2 = """
## Descriptors: the machinery behind properties, methods, and ORM fields

A **descriptor** is any object whose class defines `__get__` (and optionally
`__set__`/`__delete__`). Python calls it automatically during attribute access
on *instances* of the class that holds it.

- **Data descriptor** = defines `__set__` or `__delete__` (takes priority over
  `obj.__dict__`). Think `property`, validation fields.
- **Non-data descriptor** = only `__get__` (loses to `obj.__dict__`). Think
  methods, `cached_property`.

```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = "_" + name          # runs ONCE at class creation

    def __get__(self, obj, objtype=None):
        if obj is None:                 # accessed on the class itself
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.name[1:]} must be positive")
        setattr(obj, self.name, value)

class Order:
    qty = Positive()
    price = Positive()

    def __init__(self, qty, price):
        self.qty = qty                  # goes through Positive.__set__
        self.price = price
```

`Order(0, 5)` raises immediately. One descriptor, reused across every field —
this is exactly how SQLAlchemy columns, pydantic fields, and Django's
`IntegerField` work (their real versions add metaclass bookkeeping, but the
attribute magic is the descriptor protocol).

Key details professionals rely on:

- `__set_name__` receives the owning class and attribute name at class-body
  time — no metaclass needed for most field machinery.
- Returning `self` when `obj is None` makes `Order.qty` on the *class* return
  the descriptor — useful for ORMs building queries.
- Store per-instance state under a mangled name (`_qty`) so the descriptor
  keeps control of the public name.
"""

write_lesson(
    MOD, "descriptors",
    "Descriptors: properties, ORM fields, and validation",
    "Write reusable attribute machinery with __get__/__set__/__set_name__.",
    26, L2,
    "Descriptor: properties, trường ORM và validation",
    "Viết cơ chế attribute tái sử dụng bằng __get__/__set__/__set_name__.",
    L2.replace(
        "## Descriptors: the machinery behind properties, methods, and ORM fields",
        "## Descriptor: cỗ máy đằng sau property, method và trường ORM",
    ).replace(
        "A **descriptor** is any object whose class defines `__get__` (and optionally\n`__set__`/`__delete__`). Python calls it automatically during attribute access\non *instances* of the class that holds it.",
        "**Descriptor** là bất kỳ đối tượng nào mà class của nó định nghĩa `__get__`\n(và tùy chọn `__set__`/`__delete__`). Python tự gọi nó khi truy cập attribute\ntrên *instance* của class chứa nó.",
    ).replace(
        "Key details professionals rely on:",
        "Những chi tiết chuyên gia dựa vào:",
    ).replace(
        "- `__set_name__` receives the owning class and attribute name at class-body\n  time — no metaclass needed for most field machinery.\n- Returning `self` when `obj is None` makes `Order.qty` on the *class* return\n  the descriptor — useful for ORMs building queries.\n- Store per-instance state under a mangled name (`_qty`) so the descriptor\n  keeps control of the public name.",
        "- `__set_name__` nhận class sở hữu và tên attribute ngay khi tạo class — đa số\n  cơ chế field không cần metaclass.\n- Trả về `self` khi `obj is None` để `Order.qty` trên *class* trả về descriptor —\n  hữu ích cho ORM khi dựng truy vấn.\n- Lưu trạng thái từng instance dưới tên được biến đổi (`_qty`) để descriptor\n  tiếp tục kiểm soát tên công khai.",
    ),
)

# ── lesson 3: MRO + cooperative inheritance ──────────────────────────────────
L3 = """
## MRO and cooperative `super()`

Every class has a **method resolution order** — the C3-linearized list of
classes Python searches left-to-right for an attribute. Inspect it with
`Cls.__mro__`; reason about it, never memorize individual cases.

Three rules cover almost everything:

1. Children come before parents.
2. Base classes appear in the order written in the class statement.
3. The linearization is consistent: no class appears before one of its own
   bases in a way that would break the first two rules (C3 rejects such
   hierarchies with a `TypeError` at class-creation time).

`super()` does **not** mean "my parent". It means "the *next* class in the MRO
after me, for whoever is currently resolving". That is what makes **mixin**
cooperation work:

```python
class ReprMixin:
    def __repr__(self):
        return f"{type(self).__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})"

class JSONMixin:
    def to_json(self):
        import json
        return json.dumps(vars(self))

class Point(ReprMixin, JSONMixin):
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
print(p)              # Point(x=1, y=2)
print(p.to_json())    # {"x": 1, "y": 2}
```

`__init_subclass__` is the cooperative hook: the *parent* class runs code each
time a subclass is defined — registering subclasses, validating class
attributes, or auto-generating methods. It runs without any metaclass:

```python
class Registry:
    _registry = {}

    def __init_subclass__(cls, key=None, **kw):
        super().__init_subclass__(**kw)
        Registry._registry[key or cls.__name__.lower()] = cls

class RedisCache(Registry, key="redis"): pass
print(Registry._registry)   # {'redis': <class RedisCache>}
```

Advanced habit: when a hierarchy grows weird, print
`[c.__name__ for c in Cls.__mro__]` and ask what each `super()` call forwards to.
"""

write_lesson(
    MOD, "mro-cooperative-inheritance",
    "MRO, mixins, and __init_subclass__",
    "Reason about C3 linearization and cooperative super() instead of guessing.",
    24, L3,
    "MRO, mixin và __init_subclass__",
    "Suy luận về C3 linearization và super() hợp tác thay vì đoán mò.",
    L3.replace(
        "## MRO and cooperative `super()`",
        "## MRO và `super()` hợp tác",
    ).replace(
        "Every class has a **method resolution order** — the C3-linearized list of\nclasses Python searches left-to-right for an attribute. Inspect it with\n`Cls.__mro__`; reason about it, never memorize individual cases.",
        "Mọi class đều có **method resolution order** — danh sách các class được C3\nlinearize mà Python duyệt từ trái sang phải để tìm attribute. Xem bằng\n`Cls.__mro__`; hãy suy luận, đừng học thuộc từng trường hợp riêng lẻ.",
    ).replace(
        "`super()` does **not** mean \"my parent\". It means \"the *next* class in the MRO\nafter me, for whoever is currently resolving\". That is what makes **mixin**\ncooperation work:",
        "`super()` **không** nghĩa là \"cha của tôi\". Nó nghĩa là \"class *tiếp theo* trong\nMRO sau tôi, cho bất cứ ai đang phân giải hiện tại\". Đó là điều làm cho mixin\n**hợp tác** được với nhau:",
    ).replace(
        "`__init_subclass__` is the cooperative hook: the *parent* class runs code each\ntime a subclass is defined — registering subclasses, validating class\nattributes, or auto-generating methods. It runs without any metaclass:",
        "`__init_subclass__` là móc hợp tác: class *cha* chạy mã mỗi khi có subclass được\nđịnh nghĩa — đăng ký subclass, kiểm tra attribute của class, hoặc tự sinh method.\nNó chạy mà không cần metaclass nào:",
    ).replace(
        "Advanced habit: when a hierarchy grows weird, print\n`[c.__name__ for c in Cls.__mro__]` and ask what each `super()` call forwards to.",
        "Thói quen nâng cao: khi hệ thứ tự trở nên kỳ lạ, in\n`[c.__name__ for c in Cls.__mro__]` và tự hỏi mỗi lời `super()` sẽ chuyển tới đâu.",
    ),
)

# ── lesson 4: protocols + __slots__ ──────────────────────────────────────────
L4 = """
## Protocols, special methods, and `__slots__`

Python's built-in behaviors are all data-model hooks. Objects "become"
iterable, sized, comparable, or callable by defining the right special method:

| You write | Python calls | Enables |
|---|---|---|
| `len(x)` | `x.__len__` | sizing |
| `for a in x` | `iter(x)` → `x.__iter__` | iteration |
| `x[k]` | `x.__getitem__` | indexing / sequences |
| `k in x` | `x.__contains__` (or falls back to `__iter__`) | membership |
| `x == y` | `x.__eq__` | equality |
| `x()` | `x.__call__` | callable objects |
| `with x:` | `x.__enter__` / `x.__exit__` | context managers |

Slicing arrives as **slice objects**: `x[1:5]` calls
`__getitem__(slice(1, 5, None))`. A robust `__getitem__` handles both `int`
and `slice`:

```python
def __getitem__(self, index):
    if isinstance(index, slice):
        return type(self)(self._data[index])
    return self._data[index]
```

**Structural typing with `typing.Protocol`** (3.8+) lets a checker verify "has
these methods" without inheritance — duck typing, statically checked:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

def shutdown(x: Closeable) -> None:
    x.close()
```

**`__slots__`** replaces the per-instance `__dict__` with fixed slots:
less memory for millions of instances, faster attribute access, and a typo
becomes `AttributeError` instead of a silent new attribute. Cost: no dynamic
attributes unless you add `__dict__` back, and care needed with multiple
inheritance (two slotted parents with nonempty slots conflict).

```python
class Vector:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y
```
"""

write_lesson(
    MOD, "protocols-slots",
    "Protocols, special methods, and __slots__",
    "Make your objects indistinguishable from built-ins — then make them lean.",
    25, L4,
    "Protocol, special method và __slots__",
    "Biến đối tượng của bạn khác gì built-in — rồi làm nó gọn lại.",
    L4.replace(
        "## Protocols, special methods, and `__slots__`",
        "## Protocol, special method và `__slots__`",
    ).replace(
        "Python's built-in behaviors are all data-model hooks. Objects \"become\"\niterable, sized, comparable, or callable by defining the right special method:",
        "Mọi hành vi built-in của Python đều là móc của data model. Đối tượng \"trở nên\"\niterable, có độ dài, so sánh được hay gọi được chỉ bằng cách định nghĩa đúng\nspecial method:",
    ).replace(
        "Slicing arrives as **slice objects**: `x[1:5]` calls\n`__getitem__(slice(1, 5, None))`. A robust `__getitem__` handles both `int`\nand `slice`:",
        "Slicing đến dưới dạng **slice object**: `x[1:5]` gọi\n`__getitem__(slice(1, 5, None))`. Một `__getitem__` vững vàng phải xử lý cả\n`int` lẫn `slice`:",
    ).replace(
        "**Structural typing with `typing.Protocol`** (3.8+) lets a checker verify \"has\nthese methods\" without inheritance — duck typing, statically checked:",
        "**Structural typing với `typing.Protocol`** (3.8+) cho phép checker xác nhận\n\"có các method này\" mà không cần kế thừa — duck typing được kiểm tra tĩnh:",
    ).replace(
        "**`__slots__`** replaces the per-instance `__dict__` with fixed slots:\nless memory for millions of instances, faster attribute access, and a typo\nbecomes `AttributeError` instead of a silent new attribute. Cost: no dynamic\nattributes unless you add `__dict__` back, and care needed with multiple\ninheritance (two slotted parents with nonempty slots conflict).",
        "**`__slots__`** thay `__dict__` từng instance bằng các slot cố định: ít bộ nhớ\nhơn cho hàng triệu instance, truy cập attribute nhanh hơn, và lỗi gõ tên trở\nthành `AttributeError` thay vì attribute thừa im lặng. Cái giá: không thuộc tính\nđộng trừ khi thêm lại `__dict__`, và cần cẩn thận với đa kế thừa (hai cha có\nslots khác rỗng sẽ xung đột).",
    ),
)

# ── practice 1: attribute lookup ─────────────────────────────────────────────
write_practice(
    MOD, "pa-p1-lookup-practice",
    "Attribute Lookup Practice",
    "Predict, then prove, how Python resolves attributes through the lookup chain.",
    "Luyện Attribute Lookup",
    "Dự đoán rồi chứng minh Python phân giải attribute qua chuỗi lookup thế nào.",
    "datamodel-attribute-lookup", 18, "advanced",
    [
        challenge(
            "pa-dm-lookup-order",
            "Who wins the lookup?",
            "Implement a data descriptor `Guarded` that stores its value in the instance dict under the mangled name `_value`.\n\nAlso implement `def probe(obj)` that returns the string 'descriptor' if `obj.value` resolves through the descriptor's `__get__` (i.e. the descriptor increments its own `reads` counter), or 'instance' otherwise.\n\nThe test will create an instance, set BOTH `obj.value = 99` (a plain instance attribute attempt) and the descriptor state, and check that reading `obj.value` still goes through the descriptor.",
            "class Guarded:\n    reads = 0\n\n    def __set_name__(self, owner, name):\n        self.name = '_' + name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None:\n            return self\n        type(self).reads += 1\n        return getattr(obj, self.name)\n\n    def __set__(self, obj, value):\n        setattr(obj, self.name, value)\n\n\nclass Box:\n    value = Guarded()\n\n    def __init__(self):\n        self.value = 1\n\n\ndef probe(obj):\n    # TODO: return 'descriptor' or 'instance'\n    pass",
            [
                ("descriptor beats instance dict",
                 "b = Box()\nb.value = 5\nbefore = Guarded.reads\n_ = b.value\nassert Guarded.reads == before + 1, 'instance read must go through the data descriptor'\nassert probe(b) == 'descriptor', f\"probe returned {probe(b)!r}\"\nprint('ok')",
                 "A data descriptor has priority over obj.__dict__, so the read must hit __get__."),
                ("probe reports instance when descriptor absent",
                 "class Plain:\n    def __init__(self):\n        self.value = 7\n\np = Plain()\nassert probe(p) == 'instance', f\"probe returned {probe(p)!r}\"\nprint('ok')",
                 "With no descriptor on the class, the read resolves from the instance dict."),
            ],
            level="independent",
        ),
        challenge(
            "pa-dm-getattr-fallback",
            "Delegating proxy with __getattr__",
            "Implement `class Proxy` that wraps any object passed to `__init__`:\n\n- attribute reads that fail on the Proxy itself must be **delegated** to the wrapped object via `__getattr__`\n- `Proxy.real(obj)` must return the wrapped object\n- calls on delegated methods must work (e.g. `Proxy('hi').upper()` returns 'HI')\n- reads of attributes the wrapper defines directly must NOT be delegated (define `sniff` on Proxy returning 'proxy')",
            "class Proxy:\n    def __init__(self, target):\n        # store target WITHOUT triggering delegation\n        pass\n\n    def sniff(self):\n        return 'proxy'\n\n    def __getattr__(self, name):\n        # TODO: delegate to the wrapped object\n        pass\n\n    @staticmethod\n    def real(obj):\n        pass",
            [
                ("delegates missing attributes",
                 "p = Proxy('hi')\nassert p.upper() == 'HI', 'upper() must be delegated to str'\nassert p.sniff() == 'proxy', 'Proxy-owned attrs must not delegate'\nprint('ok')",
                 "__getattr__ is called only on normal-lookup misses; delegate there."),
                ("real() unwraps",
                 "inner = [1, 2]\np = Proxy(inner)\nassert Proxy.real(p) is inner, 'real must return the wrapped object'\nprint('ok')",
                 "Keep the target in __dict__ under a name that cannot collide, e.g. '_target' set via object.__setattr__ or plain dict key."),
            ],
            level="independent",
        ),
        challenge(
            "pa-dm-predict-super",
            "Predict the MRO chain",
            "Without running it first (then run it!), implement the classes so that `chain()` returns the exact call order of `who()` across the hierarchy when called on a `D` instance.\n\nClasses: A defines `who` returning 'A' and logs to a shared list. B(A) overrides `who` to log 'B' then `super().who()`. C(A) overrides `who` to log 'C' then `super().who()`. D(B, C) overrides `who` to log 'D' then `super().who()`.\n\n`chain()` must reset the log, call `D().who()`, and return the list — expected `['D', 'B', 'C', 'A']` following the MRO D→B→C→A.",
            "LOG = []\n\nclass A:\n    def who(self):\n        LOG.append('A')\n        return 'A'\n\n# TODO: define B(A), C(A), D(B, C) with cooperative who()\n\ndef chain():\n    LOG.clear()\n    D().who()\n    return list(LOG)",
            [
                ("cooperative super follows MRO",
                 "assert chain() == ['D', 'B', 'C', 'A'], f\"got {chain()}\"\nprint('ok')",
                 "super() follows the MRO of the *instance's* class, not the textual parent."),
                ("mro is linearized as expected",
                 "assert [c.__name__ for c in D.__mro__] == ['D', 'B', 'C', 'A', 'object'], f\"MRO: {D.__mro__}\"\nprint('ok')",
                 "C3 linearization of D(B, C) puts B before C, both before A."),
            ],
            level="independent",
        ),
    ],
    {
        "pa-dm-lookup-order": vi_challenge(
            "Ai thắng trong lookup?",
            "Cài đặt data descriptor `Guarded` lưu giá trị trong `__dict__` của instance dưới tên biến đổi `_value`.\n\nCũng cài `def probe(obj)` trả về chuỗi 'descriptor' nếu `obj.value` được phân giải qua `__get__` của descriptor (nghĩa là descriptor tự tăng bộ đếm `reads`), hoặc 'instance' nếu ngược lại.",
            [("descriptor thắng instance dict", "Data descriptor có ưu tiên cao hơn obj.__dict__, nên lần đọc phải đi qua __get__."),
             ("probe báo 'instance' khi không có descriptor", "Không có descriptor trên class thì lần đọc lấy từ __dict__ của instance.")],
        ),
        "pa-dm-getattr-fallback": vi_challenge(
            "Proxy ủy quyền bằng __getattr__",
            "Cài `class Proxy` bao bọc bất kỳ đối tượng nào truyền vào `__init__`:\n\n- những lần đọc attribute thất bại trên Proxy phải được **ủy quyền** cho đối tượng được bao qua `__getattr__`\n- `Proxy.real(obj)` trả về đối tượng bên trong\n- gọi method được ủy quyền phải hoạt động (ví dụ `Proxy('hi').upper()` trả về 'HI')\n- đọc attribute mà Proxy tự định nghĩa thì KHÔNG được ủy quyền (định nghĩa `sniff` trên Proxy trả về 'proxy')",
            [("Ủy quyền attribute còn thiếu", "__getattr__ chỉ được gọi khi tra cứu thường thất bại; hãy ủy quyền ở đó."),
             ("real() bóc lớp bao", "Giữ đối tượng bên trong __dict__ dưới tên không thể trùng, ví dụ '_target'.")],
        ),
        "pa-dm-predict-super": vi_challenge(
            "Dự đoán chuỗi MRO",
            "Chưa chạy thì đoán trước (rồi chạy thử!), cài các class sao cho `chain()` trả về đúng thứ tự gọi `who()` xuyên qua hệ thứ tự khi gọi trên instance `D`.\n\nCác class: A định nghĩa `who` trả về 'A' và ghi vào một danh sách dùng chung. B(A) ghi đè `who` để ghi 'B' rồi `super().who()`. C(A) ghi đè `who` để ghi 'C' rồi `super().who()`. D(B, C) ghi đè `who` để ghi 'D' rồi `super().who()`.\n\n`chain()` phải xóa log, gọi `D().who()`, và trả về danh sách — kỳ vọng `['D', 'B', 'C', 'A']` theo MRO D→B→C→A.",
            [("super() hợp tác theo MRO", "super() đi theo MRO của class *của instance*, không phải cha theo văn bản."),
             ("MRO được linearize như kỳ vọng", "C3 linearization của D(B, C) đặt B trước C, cả hai trước A.")],
        ),
    },
    solutions=[
        ("pa-dm-lookup-order",
         "class Guarded:\n    reads = 0\n\n    def __set_name__(self, owner, name):\n        self.name = '_' + name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None:\n            return self\n        type(self).reads += 1\n        return getattr(obj, self.name)\n\n    def __set__(self, obj, value):\n        setattr(obj, self.name, value)\n\n\nclass Box:\n    value = Guarded()\n\n    def __init__(self):\n        self.value = 1\n\n\ndef probe(obj):\n    Guarded.reads = 0\n    _ = obj.value\n    return 'descriptor' if Guarded.reads > 0 else 'instance'",
         "class Guarded:\n    reads = 0\n\n    def __set_name__(self, owner, name):\n        self.name = '_' + name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None:\n            return self\n        type(self).reads += 1\n        return getattr(obj, self.name)\n\n    def __set__(self, obj, value):\n        setattr(obj, self.name, value)\n\n\nclass Box:\n    value = Guarded()\n\n    def __init__(self):\n        self.value = 1\n\n\ndef probe(obj):\n    # WRONG: looks at the instance dict instead of observing the descriptor\n    return 'instance' if 'value' in vars(obj) or '_value' in vars(obj) else 'instance'"),
        ("pa-dm-getattr-fallback",
         "class Proxy:\n    def __init__(self, target):\n        object.__setattr__(self, '_target', target)\n\n    def sniff(self):\n        return 'proxy'\n\n    def __getattr__(self, name):\n        return getattr(object.__getattribute__(self, '_target'), name)\n\n    @staticmethod\n    def real(obj):\n        return object.__getattribute__(obj, '_target')",
         "class Proxy:\n    def __init__(self, target):\n        object.__setattr__(self, '_target', target)\n\n    def sniff(self):\n        return 'proxy'\n\n    def __getattr__(self, name):\n        # WRONG: real() forgets to unwrap — see below; delegation itself is fine\n        return getattr(self._target, name)\n\n    @staticmethod\n    def real(obj):\n        return obj  # WRONG: returns the proxy, not the wrapped object"),
        ("pa-dm-predict-super",
         "LOG = []\n\nclass A:\n    def who(self):\n        LOG.append('A')\n        return 'A'\n\n\nclass B(A):\n    def who(self):\n        LOG.append('B')\n        return super().who()\n\n\nclass C(A):\n    def who(self):\n        LOG.append('C')\n        return super().who()\n\n\nclass D(B, C):\n    def who(self):\n        LOG.append('D')\n        return super().who()\n\n\ndef chain():\n    LOG.clear()\n    D().who()\n    return list(LOG)",
         "LOG = []\n\nclass A:\n    def who(self):\n        LOG.append('A')\n        return 'A'\n\n\nclass B(A):\n    def who(self):\n        LOG.append('B')\n        return super().who()\n\n\nclass C(A):\n    def who(self):\n        LOG.append('C')\n        return super().who()\n\n\nclass D(B, C):\n    def who(self):\n        LOG.append('D')\n        return A.who(self)  # WRONG: skips C entirely, breaking cooperation\n\n\ndef chain():\n    LOG.clear()\n    D().who()\n    return list(LOG)"),
    ],
)

# ── practice 2: descriptors ──────────────────────────────────────────────────
write_practice(
    MOD, "pa-p1-descriptor-practice",
    "Descriptor Practice",
    "Build reusable attribute machinery the way ORMs and validators do.",
    "Luyện Descriptor",
    "Xây dựng cơ chế attribute tái sử dụng theo cách ORM và validator làm.",
    "descriptors", 20, "advanced",
    [
        challenge(
            "pa-dm-descriptor-field",
            "Build a Validated field",
            "Implement a data descriptor `Validated(min_value, max_value)` usable as a class attribute:\n\n- stores the value under a mangled name chosen in `__set_name__`\n- `__set__` raises `ValueError` when the value is not an `int` or is outside `[min_value, max_value]`\n- `__get__` on the class (obj is None) returns the descriptor itself\n- the class access must expose the declared bounds: `Model.age.min_value == 0`",
            "class Validated:\n    def __init__(self, min_value, max_value):\n        self.min_value = min_value\n        self.max_value = max_value\n\n    # TODO: __set_name__, __get__, __set__\n\n\nclass Model:\n    age = Validated(0, 150)",
            [
                ("rejects out-of-range and wrong types",
                 "m = Model()\nm.age = 42\nassert m.age == 42\nfor bad in (-1, 999, 'x', 3.5):\n    try:\n        m.age = bad\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(f'value {bad!r} must be rejected')\nprint('ok')",
                 "Validate type first (must be int — bool is not allowed here, treat non-int as ValueError), then range."),
                ("descriptor visible on the class with bounds",
                 "assert isinstance(Model.age, Validated), 'class access must return the descriptor'\nassert Model.age.min_value == 0 and Model.age.max_value == 150\nprint('ok')",
                 "When obj is None, return self."),
            ],
            level="guided",
        ),
        challenge(
            "pa-dm-cached-property",
            "Implement cached_property",
            "Implement a non-data descriptor `CachedProperty` that computes once and caches per instance:\n\n- constructed with the computing function: `CachedProperty(fn)`\n- first access calls `fn(instance)` and caches the result in `instance.__dict__` under the attribute name (use `__set_name__` to learn it)\n- later accesses return the cached value WITHOUT calling `fn` again (track call count via a list wrapper in the test)\n- because it is non-data, a later direct assignment `obj.name = x` overrides the cache — that behavior must work",
            "class CachedProperty:\n    def __init__(self, fn):\n        self.fn = fn\n\n    # TODO: __set_name__, __get__\n\n\nclass Report:\n    def __init__(self, rows):\n        self.rows = rows\n\n    @CachedProperty\n    def total(self):\n        return sum(self.rows)",
            [
                ("computes once then reuses",
                 "r = Report([1, 2, 3])\nassert r.total == 6\nassert r.total == 6\nassert Report.total.fn_calls == [1], f'fn called {Report.total.fn_calls} times'\nprint('ok')",
                 "Store the cache in obj.__dict__[self.name]; __dict__ is checked before non-data descriptors."),
                ("instance assignment overrides cache",
                 "r = Report([1, 2, 3])\nr.total = 100\nassert r.total == 100, 'instance dict must win over a non-data descriptor'\nprint('ok')",
                 "That is the definition of non-data: only __get__."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-dm-descriptor-field": vi_challenge(
            "Xây field Validated",
            "Cài data descriptor `Validated(min_value, max_value)` dùng như attribute của class:\n\n- lưu giá trị dưới tên biến đổi được chọn trong `__set_name__`\n- `__set__` raise `ValueError` khi giá trị không phải `int` hoặc ngoài `[min_value, max_value]`\n- `__get__` trên class (obj là None) trả về chính descriptor\n- truy cập qua class phải lộ ra biên đã khai báo: `Model.age.min_value == 0`",
            [("Từ chối ngoài khoảng và sai kiểu", "Kiểm tra kiểu trước (phải là int — bool không được chấp nhận, coi non-int là ValueError), rồi tới khoảng giá trị."),
             ("Descriptor hiện trên class kèm biên", "Khi obj là None, trả về self.")],
        ),
        "pa-dm-cached-property": vi_challenge(
            "Tự cài cached_property",
            "Cài non-data descriptor `CachedProperty` tính một lần và cache theo từng instance:\n\n- khởi tạo bằng hàm tính: `CachedProperty(fn)`\n- lần truy cập đầu gọi `fn(instance)` và cache kết quả trong `instance.__dict__` dưới tên attribute (dùng `__set_name__` để biết tên)\n- những lần sau trả về giá trị cache KHÔNG gọi lại `fn`\n- vì là non-data, gán trực tiếp `obj.name = x` sau đó sẽ ghi đè cache — hành vi này phải hoạt động",
            [("Tính một lần rồi tái sử dụng", "Lưu cache vào obj.__dict__[self.name]; __dict__ được tra trước non-data descriptor."),
             ("Gán trên instance ghi đè cache", "Đó chính là định nghĩa của non-data: chỉ có __get__.")],
        ),
    },
    solutions=[
        ("pa-dm-descriptor-field",
         "class Validated:\n    def __init__(self, min_value, max_value):\n        self.min_value = min_value\n        self.max_value = max_value\n\n    def __set_name__(self, owner, name):\n        self.name = '_' + name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None:\n            return self\n        return getattr(obj, self.name)\n\n    def __set__(self, obj, value):\n        if not isinstance(value, int) or isinstance(value, bool):\n            raise ValueError('must be an int')\n        if not (self.min_value <= value <= self.max_value):\n            raise ValueError('out of range')\n        setattr(obj, self.name, value)\n\n\nclass Model:\n    age = Validated(0, 150)",
         "class Validated:\n    def __init__(self, min_value, max_value):\n        self.min_value = min_value\n        self.max_value = max_value\n\n    def __set_name__(self, owner, name):\n        self.name = '_' + name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None:\n            return self\n        return getattr(obj, self.name)\n\n    def __set__(self, obj, value):\n        # WRONG: accepts floats and booleans, and clamps instead of raising\n        value = max(self.min_value, min(self.max_value, int(value)))\n        setattr(obj, self.name, value)\n\n\nclass Model:\n    age = Validated(0, 150)"),
        ("pa-dm-cached-property",
         "class CachedProperty:\n    def __init__(self, fn):\n        self.fn = fn\n        self.fn_calls = []\n\n    def __set_name__(self, owner, name):\n        self.name = name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None:\n            return self\n        if self.name not in vars(obj):\n            self.fn_calls.append(1)\n            vars(obj)[self.name] = self.fn(obj)\n        return vars(obj)[self.name]\n\n\nclass Report:\n    def __init__(self, rows):\n        self.rows = rows\n\n    @CachedProperty\n    def total(self):\n        return sum(self.rows)",
         "class CachedProperty:\n    def __init__(self, fn):\n        self.fn = fn\n        self.fn_calls = []\n\n    def __set_name__(self, owner, name):\n        self.name = name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None:\n            return self\n        # WRONG: recomputes every time — never consults the instance dict\n        self.fn_calls.append(1)\n        return self.fn(obj)\n\n\nclass Report:\n    def __init__(self, rows):\n        self.rows = rows\n\n    @CachedProperty\n    def total(self):\n        return sum(self.rows)"),
    ],
)

# ── practice 3: MRO / mixins ─────────────────────────────────────────────────
write_practice(
    MOD, "pa-p1-mro-practice",
    "MRO & Mixin Practice",
    "Design hierarchies that cooperate — and repair ones that don't.",
    "Luyện MRO & Mixin",
    "Thiết kế hệ thứ tự biết hợp tác — và sửa lại những hệ thứ tự không hợp tác.",
    "mro-cooperative-inheritance", 18, "advanced",
    [
        challenge(
            "pa-dm-mixin-order",
            "Mixin that must come first",
            "You are given a base `Base` with `label()` returning 'base'. Build a class `Widget` from mixins and Base such that `Widget().label()` returns 'widget+base':\n\n- `LabelMixin` overrides `label()` to return `'widget+' + super().label()`\n- the class statement must be `class Widget(<one or more mixins>, Base)` — the mixin must run BEFORE Base's method\n- also return the MRO class names (excluding object) from `mro_names()` as a list",
            "class Base:\n    def label(self):\n        return 'base'\n\n# TODO: define LabelMixin and Widget\ndef widget_label():\n    return Widget().label()\n\ndef mro_names():\n    return [c.__name__ for c in Widget.__mro__ if c is not object]",
            [
                ("mixin wraps the base result",
                 "assert widget_label() == 'widget+base', f\"got {widget_label()}\"\nprint('ok')",
                 "In the class statement, earlier bases are earlier in the MRO."),
                ("MRO places the mixin before Base",
                 "names = mro_names()\nassert names == ['Widget', 'LabelMixin', 'Base'], f\"MRO: {names}\"\nprint('ok')",
                 "class Widget(LabelMixin, Base) linearizes to Widget, LabelMixin, Base, object."),
            ],
            level="independent",
        ),
        challenge(
            "pa-dm-init-subclass-registry",
            "Auto-registering subclasses",
            "Implement `class Registered` whose subclasses are collected automatically:\n\n- use `__init_subclass__` (no metaclass)\n- each subclass registers itself in `Registered.registry` (a dict) keyed by a class attribute `key` if present, else its lowercase class name\n- the base class itself must NOT appear in the registry\n- `Registered.get(key)` returns the class or raises `KeyError`",
            "class Registered:\n    registry = {}\n\n    # TODO: __init_subclass__ + get()\n\nclass Alpha(Registered):\n    pass\n\nclass Beta(Registered, key='beta-2'):\n    pass",
            [
                ("subclasses auto-register",
                 "assert Registered.registry.get('alpha') is Alpha, f\"registry: {Registered.registry}\"\nassert Registered.registry.get('beta-2') is Beta\nassert len(Registered.registry) == 2, 'base must not register itself'\nprint('ok')",
                 "__init_subclass__ runs on the parent for each new subclass; cls is the new subclass."),
                ("get() resolves and raises",
                 "assert Registered.get('alpha') is Alpha\ntry:\n    Registered.get('nope')\nexcept KeyError:\n    pass\nelse:\n    raise AssertionError('missing key must raise KeyError')\nprint('ok')",
                 "A plain dict lookup with [] is enough."),
            ],
            level="combination",
        ),
        challenge(
            "pa-dm-fix-diamond",
            "Repair a broken diamond",
            "The hierarchy below initializes `Base.__init__` TWICE when `D` is constructed (the effects list gets two entries): A and B bypass cooperation with direct calls, and D adds a belt-and-braces direct call on top of its own super() chain.\n\nFix A, B, and D so that every construction — D(), A(), or B() — appends exactly one 'base' entry, using cooperative `super()` throughout. Do not change `Base`.\n\nGiven broken code:\n\n```python\nclass A(Base):\n    def __init__(self):\n        Base.__init__(self)\n\nclass B(Base):\n    def __init__(self):\n        Base.__init__(self)\n\nclass D(B, A):\n    def __init__(self):\n        super().__init__()\n        Base.__init__(self)\n```",
            "class Base:\n    effects = []\n\n    def __init__(self):\n        Base.effects.append('base')\n\n# TODO: redefine A(Base), B(Base), D(B, A) with cooperative __init__\n\ndef construct():\n    Base.effects.clear()\n    D()\n    return list(Base.effects)\n\ndef construct_each():\n    out = []\n    for cls in (A, B):\n        Base.effects.clear()\n        cls()\n        out.append(list(Base.effects))\n    return out",
            [
                ("single cooperative init for D",
                 "assert construct() == ['base'], f\"effects: {construct()}\"\nprint('ok')",
                 "The MRO D→B→A→Base must pass through Base.__init__ exactly once."),
                ("single init for every class",
                 "assert construct_each() == [['base'], ['base']], f\"each: {construct_each()}\"\nprint('ok')",
                 "Cooperative super() must not skip or repeat Base for any single-parent class either."),
            ],
            level="debugging",
        ),
    ],
    {
        "pa-dm-mixin-order": vi_challenge(
            "Mixin phải đứng trước",
            "Bạn được cho class `Base` với `label()` trả về 'base'. Dựng class `Widget` từ mixin và Base sao cho `Widget().label()` trả về 'widget+base':\n\n- `LabelMixin` ghi đè `label()` để trả về `'widget+' + super().label()`\n- câu lệnh class phải là `class Widget(<một hoặc nhiều mixin>, Base)` — mixin phải chạy TRƯỚC method của Base\n- đồng thời `mro_names()` trả về danh sách tên class trong MRO (loại trừ object)",
            [("Mixin bọc kết quả của Base", "Trong câu lệnh class, base đứng trước thì đứng trước trong MRO."),
             ("MRO đặt mixin trước Base", "class Widget(LabelMixin, Base) linearize thành Widget, LabelMixin, Base, object.")],
        ),
        "pa-dm-init-subclass-registry": vi_challenge(
            "Tự đăng ký subclass",
            "Cài `class Registered` thu thập subclass một cách tự động:\n\n- dùng `__init_subclass__` (không metaclass)\n- mỗi subclass tự đăng ký vào `Registered.registry` (một dict) với khóa là attribute `key` nếu có, ngược lại là tên class viết thường\n- bản thân base class KHÔNG được xuất hiện trong registry\n- `Registered.get(key)` trả về class hoặc raise `KeyError`",
            [("Subclass tự đăng ký", "__init_subclass__ chạy trên cha mỗi khi có subclass mới; cls chính là subclass mới."),
             ("get() phân giải và raise", "Một phép tra dict thông thường với [] là đủ.")],
        ),
        "pa-dm-fix-diamond": vi_challenge(
            "Sửa hình thoi bị lỗi",
            "Hệ thứ tự dưới đây khởi tạo `Base.__init__` HAI LẦN khi dựng `D` (danh sách effects nhận hai phần tử): A và B bỏ qua hợp tác bằng lệnh gọi trực tiếp, còn D thêm một lệnh gọi trực tiếp 'belt-and-braces' bên trên chuỗi super() của nó.\n\nSửa A, B và D sao cho mọi lần dựng — D(), A() hay B() — chỉ thêm đúng một phần tử 'base', dùng `super()` hợp tác xuyên suốt. Không được đổi `Base`.",
            [("Một lần init hợp tác cho D", "MRO D→B→A→Base phải đi qua Base.__init__ đúng một lần."),
             ("Một lần init cho mọi class", "super() hợp tác không được bỏ qua hay lặp Base với class đơn cha cũng vậy.")],
        ),
    },
    solutions=[
        ("pa-dm-mixin-order",
         "class Base:\n    def label(self):\n        return 'base'\n\n\nclass LabelMixin:\n    def label(self):\n        return 'widget+' + super().label()\n\n\nclass Widget(LabelMixin, Base):\n    pass\n\n\ndef widget_label():\n    return Widget().label()\n\n\ndef mro_names():\n    return [c.__name__ for c in Widget.__mro__ if c is not object]",
         "class Base:\n    def label(self):\n        return 'base'\n\n\nclass LabelMixin:\n    def label(self):\n        return 'widget+' + super().label()\n\n\nclass Widget(Base, LabelMixin):  # WRONG: Base wins the MRO, super().label() inside the mixin finds object\n    pass\n\n\ndef widget_label():\n    return Widget().label()\n\n\ndef mro_names():\n    return [c.__name__ for c in Widget.__mro__ if c is not object]"),
        ("pa-dm-init-subclass-registry",
         "class Registered:\n    registry = {}\n\n    def __init_subclass__(cls, key=None, **kwargs):\n        super().__init_subclass__(**kwargs)\n        Registered.registry[key or cls.__name__.lower()] = cls\n\n    @classmethod\n    def get(cls, key):\n        return cls.registry[key]\n\n\nclass Alpha(Registered):\n    pass\n\n\nclass Beta(Registered, key='beta-2'):\n    pass",
         "class Registered:\n    registry = {}\n\n    def __init_subclass__(cls, key=None, **kwargs):\n        super().__init_subclass__(**kwargs)\n        # WRONG: also registers the base itself, so the count test fails\n        Registered.registry[key or cls.__name__.lower()] = cls\n\n    @classmethod\n    def get(cls, key):\n        return cls.registry[key]\n\n\nRegistered.registry['registered'] = Registered\n\n\nclass Alpha(Registered):\n    pass\n\n\nclass Beta(Registered, key='beta-2'):\n    pass"),
        ("pa-dm-fix-diamond",
         "class Base:\n    effects = []\n\n    def __init__(self):\n        Base.effects.append('base')\n\n\nclass A(Base):\n    def __init__(self):\n        super().__init__()\n\n\nclass B(Base):\n    def __init__(self):\n        super().__init__()\n\n\nclass D(B, A):\n    def __init__(self):\n        super().__init__()\n\n\ndef construct():\n    Base.effects.clear()\n    D()\n    return list(Base.effects)\n\ndef construct_each():\n    out = []\n    for cls in (A, B):\n        Base.effects.clear()\n        cls()\n        out.append(list(Base.effects))\n    return out",
         "class Base:\n    effects = []\n\n    def __init__(self):\n        Base.effects.append('base')\n\n\nclass A(Base):\n    def __init__(self):\n        super().__init__()\n\n\nclass B(Base):\n    def __init__(self):\n        super().__init__()\n\n\nclass D(B, A):\n    def __init__(self):\n        super().__init__()\n        Base.__init__(self)  # WRONG: belt-and-braces double init survives\n\n\ndef construct():\n    Base.effects.clear()\n    D()\n    return list(Base.effects)\n\ndef construct_each():\n    out = []\n    for cls in (A, B):\n        Base.effects.clear()\n        cls()\n        out.append(list(Base.effects))\n    return out"),
    ],
)

# ── practice 4: containers + slots ───────────────────────────────────────────
write_practice(
    MOD, "pa-p1-container-practice",
    "Custom Container Practice",
    "Build a collection that behaves like a built-in — then make it lean with __slots__.",
    "Luyện Container tự viết",
    "Xây một collection hành xử như built-in — rồi làm gọn bằng __slots__.",
    "protocols-slots", 22, "advanced",
    [
        challenge(
            "pa-dm-custom-deque",
            "Protocol-complete Stack",
            "Implement `class Stack` that supports:\n\n- `push(x)`, `pop()` (raise `IndexError` on empty), `peek()` (raise `IndexError` on empty)\n- `len(stack)`, `stack[i]` (int indexing, negative included), `x in stack`, iteration (bottom→top)\n- slicing: `stack[1:3]` returns a NEW Stack\n- `__eq__` against another Stack comparing element order (return NotImplemented for non-Stack)\n- `__repr__` as `Stack(<items joined by ', '>)`",
            "class Stack:\n    def __init__(self, items=()):\n        self._items = list(items)\n\n    # TODO: push, pop, peek, __len__, __getitem__, __contains__, __iter__, __eq__, __repr__",
            [
                ("core operations",
                 "s = Stack()\ns.push(1); s.push(2)\nassert s.pop() == 2\nassert s.peek() == 1\nassert len(s) == 1\nempty = Stack()\ntry:\n    empty.pop()\nexcept IndexError:\n    pass\nelse:\n    raise AssertionError('pop on empty must raise IndexError')\nprint('ok')",
                 "list-based storage is fine; just obey the protocol signatures."),
                ("sequence protocol incl. slicing",
                 "s = Stack([10, 20, 30])\nassert 20 in s\nassert [x for x in s] == [10, 20, 30]\nassert s[1] == 20 and s[-1] == 30\nsliced = s[0:2]\nassert isinstance(sliced, Stack) and list(sliced) == [10, 20]\nassert s == Stack([10, 20, 30])\nassert (s == [10, 20, 30]) is False\nassert repr(s) == 'Stack(10, 20, 30)'\nprint('ok')",
                 "__getitem__ must accept both int and slice; return NotImplemented (not False) for foreign types in __eq__."),
            ],
            level="mini-build",
        ),
        challenge(
            "pa-dm-slots-memory",
            "Slotted points",
            "Implement `class Point` with `__slots__ = ('x', 'y')`:\n\n- constructor takes x, y\n- instances must NOT support arbitrary attributes (`p.z = 1` raises `AttributeError`)\n- `__eq__`/`__hash__` consistent: equal points share a hash (define both)\n- `distance_to(other)` returns the Euclidean distance (use math.hypot)",
            "import math\n\nclass Point:\n    __slots__ = ('x', 'y')\n\n    # TODO: __init__, __eq__, __hash__, distance_to",
            [
                ("slots enforce the shape",
                 "p = Point(1, 2)\nassert p.x == 1 and p.y == 2\ntry:\n    p.z = 9\nexcept AttributeError:\n    pass\nelse:\n    raise AssertionError('arbitrary attributes must fail with __slots__')\nassert not hasattr(p, '__dict__')\nprint('ok')",
                 "__slots__ removes the per-instance __dict__ — that is the point."),
                ("eq/hash/distance",
                 "assert Point(1, 2) == Point(1, 2)\nassert hash(Point(1, 2)) == hash(Point(1, 2))\nassert Point(1, 2) != Point(2, 1)\nassert abs(Point(0, 0).distance_to(Point(3, 4)) - 5.0) < 1e-9\nassert hash(Point(1, 2)) in {hash(Point(1, 2))}\nprint('ok')",
                 "Define __eq__ and __hash__ together (tuple hash of the coordinates)."),
            ],
            level="independent",
        ),
        challenge(
            "pa-dm-context-manager",
            "Reusable context manager",
            "Implement `class Timer` usable as a context manager AND reusable across runs:\n\n- `with Timer() as t:` — on exit, `t.elapsed` is a float ≥ 0 seconds\n- `t.runs` counts completed blocks\n- nested usage of two Timers must be independent\n- entering must return the timer itself",
            "import time\n\nclass Timer:\n    def __init__(self):\n        self.runs = 0\n        self.elapsed = 0.0\n\n    # TODO: __enter__, __exit__",
            [
                ("measures a block once",
                 "t = Timer()\nwith t:\n    time.sleep(0.01)\nassert t.elapsed >= 0.01, f'elapsed={t.elapsed}'\nassert t.runs == 1\nprint('ok')",
                 "__exit__ receives (exc_type, exc, tb); return False/None so exceptions still propagate."),
                ("reusable and independent",
                 "t = Timer()\nwith t:\n    pass\nwith t:\n    time.sleep(0.005)\nassert t.runs == 2\n\na, b = Timer(), Timer()\nwith a:\n    with b:\n        pass\nassert a.runs == 1 and b.runs == 1\nassert b.elapsed < a.elapsed or b.elapsed >= 0\nprint('ok')",
                 "Reset the clock in __enter__, finalize in __exit__."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-dm-custom-deque": vi_challenge(
            "Stack đủ protocol",
            "Cài `class Stack` hỗ trợ:\n\n- `push(x)`, `pop()` (raise `IndexError` khi rỗng), `peek()` (raise `IndexError` khi rỗng)\n- `len(stack)`, `stack[i]` (chỉ số int, kể cả âm), `x in stack`, iteration (đáy→đỉnh)\n- slicing: `stack[1:3]` trả về Stack MỚI\n- `__eq__` với Stack khác so sánh thứ tự phần tử (trả NotImplemented cho kiểu lạ)\n- `__repr__` dạng `Stack(<các phần tử nối bằng ', '>)`",
            [("Thao tác cốt lõi", "Lưu bằng list là được; chỉ cần đúng chữ ký của từng protocol."),
             ("Sequence protocol kể cả slicing", "__getitem__ phải nhận cả int lẫn slice; với kiểu lạ trong __eq__ hãy trả NotImplemented (không phải False).")],
        ),
        "pa-dm-slots-memory": vi_challenge(
            "Point có __slots__",
            "Cài `class Point` với `__slots__ = ('x', 'y')`:\n\n- constructor nhận x, y\n- instance KHÔNG được hỗ trợ attribute tùy ý (`p.z = 1` raise `AttributeError`)\n- `__eq__`/`__hash__` nhất quán: point bằng nhau có hash bằng nhau (định nghĩa cả hai)\n- `distance_to(other)` trả về khoảng cách Euclid (dùng math.hypot)",
            [("__slots__ ép hình dạng", "__slots__ loại bỏ __dict__ từng instance — đó chính là mục đích."),
             ("eq/hash/khoảng cách", "Định nghĩa __eq__ và __hash__ cùng nhau (hash tuple của tọa độ).")],
        ),
        "pa-dm-context-manager": vi_challenge(
            "Context manager tái sử dụng",
            "Cài `class Timer` dùng được như context manager VÀ dùng lại được nhiều lần:\n\n- `with Timer() as t:` — khi thoát, `t.elapsed` là số thực ≥ 0 giây\n- `t.runs` đếm số block đã hoàn tất\n- hai Timer lồng nhau phải độc lập\n- vào block phải trả về chính timer đó",
            [("Đo một block", "__exit__ nhận (exc_type, exc, tb); trả False/None để exception vẫn lan truyền."),
             ("Tái sử dụng và độc lập", "Reset đồng hồ trong __enter__, chốt kết quả trong __exit__.")],
        ),
    },
    solutions=[
        ("pa-dm-custom-deque",
         "class Stack:\n    def __init__(self, items=()):\n        self._items = list(items)\n\n    def push(self, x):\n        self._items.append(x)\n\n    def pop(self):\n        if not self._items:\n            raise IndexError('pop from empty stack')\n        return self._items.pop()\n\n    def peek(self):\n        if not self._items:\n            raise IndexError('peek at empty stack')\n        return self._items[-1]\n\n    def __len__(self):\n        return len(self._items)\n\n    def __getitem__(self, index):\n        if isinstance(index, slice):\n            return Stack(self._items[index])\n        return self._items[index]\n\n    def __contains__(self, x):\n        return x in self._items\n\n    def __iter__(self):\n        return iter(self._items)\n\n    def __eq__(self, other):\n        if not isinstance(other, Stack):\n            return NotImplemented\n        return self._items == other._items\n\n    def __repr__(self):\n        return 'Stack(' + ', '.join(repr(x) for x in self._items) + ')'",
         "class Stack:\n    def __init__(self, items=()):\n        self._items = list(items)\n\n    def push(self, x):\n        self._items.append(x)\n\n    def pop(self):\n        if not self._items:\n            raise IndexError('pop from empty stack')\n        return self._items.pop()\n\n    def peek(self):\n        if not self._items:\n            raise IndexError('peek at empty stack')\n        return self._items[-1]\n\n    def __len__(self):\n        return len(self._items)\n\n    def __getitem__(self, index):\n        # WRONG: slices become lists, breaking \"returns a NEW Stack\"\n        return self._items[index]\n\n    def __contains__(self, x):\n        return x in self._items\n\n    def __iter__(self):\n        return iter(self._items)\n\n    def __eq__(self, other):\n        if not isinstance(other, Stack):\n            return NotImplemented\n        return self._items == other._items\n\n    def __repr__(self):\n        return 'Stack(' + ', '.join(repr(x) for x in self._items) + ')'"),
        ("pa-dm-slots-memory",
         "import math\n\n\nclass Point:\n    __slots__ = ('x', 'y')\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __eq__(self, other):\n        if not isinstance(other, Point):\n            return NotImplemented\n        return (self.x, self.y) == (other.x, other.y)\n\n    def __hash__(self):\n        return hash((self.x, self.y))\n\n    def distance_to(self, other):\n        return math.hypot(self.x - other.x, self.y - other.y)",
         "import math\n\n\nclass Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __eq__(self, other):\n        if not isinstance(other, Point):\n            return NotImplemented\n        return (self.x, self.y) == (other.x, other.y)\n\n    def distance_to(self, other):\n        return math.hypot(self.x - other.x, self.y - other.y)\n\n# WRONG: no __slots__ (has __dict__, arbitrary attrs allowed) and no __hash__ (unhashable once __eq__ is defined)"),
        ("pa-dm-context-manager",
         "import time\n\n\nclass Timer:\n    def __init__(self):\n        self.runs = 0\n        self.elapsed = 0.0\n        self._start = None\n\n    def __enter__(self):\n        self._start = time.perf_counter()\n        return self\n\n    def __exit__(self, exc_type, exc, tb):\n        self.elapsed = time.perf_counter() - self._start\n        self.runs += 1\n        return False",
         "import time\n\n\nclass Timer:\n    def __init__(self):\n        self.runs = 0\n        self.elapsed = 0.0\n        self._start = None\n\n    def __enter__(self):\n        self._start = time.perf_counter()\n        return self\n\n    def __exit__(self, exc_type, exc, tb):\n        # WRONG: swallows every exception and forgets to record the run\n        return True"),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_SOLUTION = (
    "class Node:\n"
    "    __slots__ = ('value', 'next')\n"
    "\n"
    "    def __init__(self, value, next=None):\n"
    "        self.value = value\n"
    "        self.next = next\n"
    "\n"
    "\n"
    "class LinkedList:\n"
    "    __slots__ = ('_head',)\n"
    "\n"
    "    def __init__(self, items=()):\n"
    "        self._head = None\n"
    "        for x in reversed(list(items)):\n"
    "            self._head = Node(x, self._head)\n"
    "\n"
    "    def __len__(self):\n"
    "        n = 0\n"
    "        cur = self._head\n"
    "        while cur is not None:\n"
    "            n += 1\n"
    "            cur = cur.next\n"
    "        return n\n"
    "\n"
    "    def __iter__(self):\n"
    "        cur = self._head\n"
    "        while cur is not None:\n"
    "            yield cur.value\n"
    "            cur = cur.next\n"
    "\n"
    "    def __getitem__(self, index):\n"
    "        if isinstance(index, slice):\n"
    "            start, stop, step = index.indices(len(self))\n"
    "            out = LinkedList()\n"
    "            for i, v in enumerate(self):\n"
    "                if start <= i < stop and (i - start) % step == 0:\n"
    "                    out._append(v)\n"
    "            return out\n"
    "        if index < 0:\n"
    "            index += len(self)\n"
    "        for i, v in enumerate(self):\n"
    "            if i == index:\n"
    "                return v\n"
    "        raise IndexError('index out of range')\n"
    "\n"
    "    def __contains__(self, x):\n"
    "        return any(v == x for v in self)\n"
    "\n"
    "    def __repr__(self):\n"
    "        return 'LinkedList(' + ' -> '.join(repr(v) for v in self) + ')'\n"
    "\n"
    "    def _append(self, x):\n"
    "        node = Node(x)\n"
    "        if self._head is None:\n"
    "            self._head = node\n"
    "            return\n"
    "        cur = self._head\n"
    "        while cur.next is not None:\n"
    "            cur = cur.next\n"
    "        cur.next = node\n"
    "\n"
    "    def prepend(self, x):\n"
    "        self._head = Node(x, self._head)\n"
    "\n"
    "    def reverse(self):\n"
    "        out = LinkedList()\n"
    "        for v in self:\n"
    "            out.prepend(v)\n"
    "        return out"
)

CK_WRONG = CK_SOLUTION.replace(
    "    def __getitem__(self, index):\n        if isinstance(index, slice):",
    "    def __getitem__(self, index):\n        # WRONG: negative indexes not supported; slices return a list\n        if isinstance(index, slice):\n            return list(self)[index]",
).replace(
    "        if index < 0:\n            index += len(self)\n        for i, v in enumerate(self):",
    "        for i, v in enumerate(self):",
)

write_checkpoint(
    MOD, "pa-checkpoint-datamodel",
    "Checkpoint: The Data Model",
    "Implement a protocol-complete, slotted linked list — the module's skills in one object.",
    35,
    """
## Checkpoint — build a protocol-complete linked list

No starter code beyond the class shells. Requirements:

- `LinkedList(items=())` builds from any iterable
- `len()`, iteration (head→tail), `x in list`, `repr` as `LinkedList(1 -> 2 -> 3)`
- indexing: `l[i]` with **negative** indexes supported; `l[1:3]` returns a new
  `LinkedList` (support a `step` too)
- `prepend(x)` is O(1); `reverse()` returns a new list, original untouched
- both classes use `__slots__` — no `__dict__` on instances

Grading runs the full protocol battery against your implementation, plus a
plausible-but-wrong variant to make sure the tests bite.
""",
    "Checkpoint: Data Model",
    "Cài danh sách liên kết đủ protocol, có __slots__ — gói trọn kỹ năng của module trong một đối tượng.",
    """
## Checkpoint — dựng danh sách liên kết đủ protocol

Không có mã khởi đầu ngoài khung class. Yêu cầu:

- `LinkedList(items=())` dựng từ bất kỳ iterable nào
- `len()`, iteration (đầu→đuôi), `x in list`, `repr` dạng `LinkedList(1 -> 2 -> 3)`
- indexing: `l[i]` hỗ trợ **chỉ số âm**; `l[1:3]` trả về `LinkedList` mới (hỗ trợ cả `step`)
- `prepend(x)` là O(1); `reverse()` trả về danh sách mới, bản gốc không đổi
- cả hai class đều dùng `__slots__` — không có `__dict__` trên instance

Phần chấm chạy trọn bộ kiểm tra protocol với bản của bạn, cộng thêm một biến thể
"hợp lý nhưng sai" để chắc chắn bộ test không dễ dãi.
""",
    challenge(
        "pa-checkpoint-datamodel",
        "LinkedList, protocol-complete",
        "Implement Node and LinkedList per the checkpoint specification: len, iteration, membership, repr 'LinkedList(1 -> 2 -> 3)', int indexing with negatives, slicing to a new LinkedList (with step), O(1) prepend, non-mutating reverse, and __slots__ on both classes.",
        "class Node:\n    __slots__ = ('value', 'next')\n    # TODO\n\n\nclass LinkedList:\n    __slots__ = ('_head',)\n    # TODO",
        [
            ("construction, len, iter, repr",
             "l = LinkedList([1, 2, 3])\nassert len(l) == 3\nassert list(l) == [1, 2, 3]\nassert repr(l) == 'LinkedList(1 -> 2 -> 3)'\nassert LinkedList() .__len__() == 0\nassert 2 in l and 99 not in l\nprint('ok')",
             "Iterate nodes from _head; build repr with ' -> '.join(repr(v))."),
            ("indexing with negatives and slices",
             "l = LinkedList([1, 2, 3, 4, 5])\nassert l[0] == 1 and l[4] == 5 and l[-1] == 5 and l[-2] == 4\ns = l[1:3]\nassert isinstance(s, LinkedList) and list(s) == [2, 3]\nst = l[0:5:2]\nassert list(st) == [1, 3, 5]\ntry:\n    l[99]\nexcept IndexError:\n    pass\nelse:\n    raise AssertionError('out-of-range must raise IndexError')\nprint('ok')",
             "slice.indices(len(self)) converts a slice to concrete bounds; handle negative ints before scanning."),
            ("prepend, reverse, slots",
             "l = LinkedList([2, 3])\nl.prepend(1)\nassert list(l) == [1, 2, 3]\nr = l.reverse()\nassert list(r) == [3, 2, 1] and list(l) == [1, 2, 3]\nassert not hasattr(l, '__dict__') and not hasattr(Node(1), '__dict__')\nprint('ok')",
             "reverse() must not mutate the original — build a new list by prepending."),
        ],
        level="build",
    ),
    vi_challenge(
        "LinkedList, đủ protocol",
        "Cài Node và LinkedList theo đặc tả của checkpoint: len, iteration, membership, repr 'LinkedList(1 -> 2 -> 3)', indexing int có hỗ trợ số âm, slicing trả LinkedList mới (kèm step), prepend O(1), reverse không đổi bản gốc, và __slots__ trên cả hai class.",
        [("Dựng, len, iter, repr", "Duyệt node từ _head; dựng repr bằng ' -> '.join(repr(v))."),
         ("Indexing với số âm và slice", "slice.indices(len(self)) quy slice về biên cụ thể; xử lý số âm trước khi duyệt."),
         ("prepend, reverse, slots", "reverse() không được làm đổi bản gốc — dựng danh sách mới bằng cách prepend.")],
    ),
    solution=CK_SOLUTION,
    wrong=CK_WRONG,
)

print("module 1 complete")
