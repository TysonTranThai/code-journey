#!/usr/bin/env python3
"""Module 7: cpython-internals — lessons + practices + checkpoint (deterministic grading)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "cpython-internals"

write_module(
    MOD,
    "CPython Internals for Practitioners",
    "Bytecode, frames, refcounting and GC, the import system — the mechanics that explain real Python behavior. Not a contributor course; a practitioner's X-ray.",
    "CPython internals cho người thực hành",
    "Bytecode, frame, refcounting và GC, hệ thống import — cơ chế giải thích hành vi Python thật. Không phải khóa cho contributor; là tia X của người thực hành.",
    ["bytecode-frames", "gc-refcounting", "import-system"],
    ["pa-p7-bytecode-practice", "pa-p7-gc-practice", "pa-p7-import-practice", "pa-p7-investigation-project"],
)

L1_EN = """
## Bytecode: what the interpreter actually executes

CPython compiles your source to **bytecode** — a stack-machine instruction list —
then executes it in a loop. Disassemble with the `dis` module:

```python
import dis

def add_squares(xs):
    return sum(x * x for x in xs)

dis.dis(add_squares)
```

Reading bytecode answers real questions:

- **Why is `x += 1` on an instance attribute three operations?** LOAD the
  attribute, add, STORE the attribute — interleaving lives between them.
- **Why is a loop body that rebuilds an expression slow?** Every iteration
  re-executes the same LOAD_GLOBAL/LOAD_ATTR instructions; hoisting a lookup
  out of the loop removes bytecode from the hot path.
- **`LOAD_CONST` / `LOAD_FAST` / `LOAD_GLOBAL`** — const pool, local frame
  slots, module dict lookups, in increasing cost order.
- **Small-int caching and string interning** are implementation details, not
  language semantics — `is` on integers is undefined behavior territory;
  `==` is the comparison you mean.

A **frame** is the runtime state of one function call: its locals, its value
stack, the bytecode pointer, and the reference to the calling frame. Tracebacks
are just the chain of frames — that is what `inspect.currentframe()` walks.
"""

L1_VI = L1_EN.replace(
    "## Bytecode: what the interpreter actually executes",
    "## Bytecode: trình thông dịch thực thi cái gì",
).replace(
    "CPython compiles your source to **bytecode** — a stack-machine instruction list —\nthen executes it in a loop. Disassemble with the `dis` module:",
    "CPython biên dịch mã nguồn của bạn thành **bytecode** — một danh sách lệnh máy\ngiác stack — rồi thực thi trong vòng lặp. Dịch ngược bằng module `dis`:",
).replace(
    "Reading bytecode answers real questions:",
    "Đọc bytecode trả lời những câu hỏi thật:",
).replace(
    "- **Why is `x += 1` on an instance attribute three operations?** LOAD the\n  attribute, add, STORE the attribute — interleaving lives between them.\n- **Why is a loop body that rebuilds an expression slow?** Every iteration\n  re-executes the same LOAD_GLOBAL/LOAD_ATTR instructions; hoisting a lookup\n  out of the loop removes bytecode from the hot path.\n- **`LOAD_CONST` / `LOAD_FAST` / `LOAD_GLOBAL`** — const pool, local frame\n  slots, module dict lookups, in increasing cost order.\n- **Small-int caching and string interning** are implementation details, not\n  language semantics — `is` on integers is undefined behavior territory;\n  `==` is the comparison you mean.",
    "- **Vì sao `x += 1` trên attribute của instance là ba thao tác?** LOAD\n  attribute, add, STORE attribute — chen lấn nằm giữa chúng.\n- **Vì sao thân vòng lặp dựng lại biểu thức lại chậm?** Mỗi lần lặp thực thi lại\n  cùng các lệnh LOAD_GLOBAL/LOAD_ATTR; nâng phép tra cứu ra khỏi vòng lặp bỏ\n  bytecode khỏi đường nóng.\n- **`LOAD_CONST` / `LOAD_FAST` / `LOAD_GLOBAL`** — pool hằng, slot frame cục bộ,\n  tra module dict, theo thứ tự chi phí tăng dần.\n- **Cache small-int và intern chuỗi** là chi tiết cài đặt, không phải ngữ nghĩa\n  ngôn ngữ — `is` trên số nguyên là vùng hành vi không định nghĩa; `==` mới là\n  phép so sánh bạn muốn.",
).replace(
    "A **frame** is the runtime state of one function call: its locals, its value\nstack, the bytecode pointer, and the reference to the calling frame. Tracebacks\nare just the chain of frames — that is what `inspect.currentframe()` walks.",
    "Một **frame** là trạng thái runtime của một lần gọi hàm: biến cục bộ, stack\ngiá trị, con trỏ bytecode, và tham chiếu tới frame gọi nó. Traceback chỉ là\nchuỗi frame — đó là thứ `inspect.currentframe()` đi qua.",
)

write_lesson(
    MOD, "bytecode-frames",
    "Bytecode and frames",
    "Read dis output to explain performance and correctness questions.",
    20, L1_EN,
    "Bytecode và frame",
    "Đọc output của dis để giải thích câu hỏi hiệu năng và tính đúng đắn.",
    L1_VI,
)

L2_EN = """
## Reference counting and the garbage collector

CPython's primary memory management is **refcounting**: every object counts
its references; hitting zero frees it immediately (hence the instant
`__del__`-less determinism CPython is known for).

Refcounting alone cannot free **cycles** (a→b→a). A supplementary **cycle
detector** — the generational `gc` module — periodically scans container
objects for unreachable cycles:

```python
import gc, sys

class Node:
    def __init__(self):
        self.partner = None

a, b = Node(), Node()
a.partner, b.partner = b, a
del a, b                       # refcounts never hit zero — cycle!
gc.collect()                   # cycle detector frees them
```

Practitioner takeaways:

- `sys.getrefcount(x)` shows the count (always +1 for the argument itself).
- Most "memory leaks" in Python are *reference leaks*: caches, registries,
  closures, or loggers holding objects forever. Find them with
  `gc.get_referrers(obj)` — who still points at this?
- `gc.garbage` collects objects the collector could not free (usually
  `__del__`-bearing cycles) — its growth is a design smell.
- `weakref` lets a cache reference objects without keeping them alive — the
  standard fix for registry-induced leaks.
- `gc.disable()` can speed allocation-heavy batch jobs slightly, at the cost of
  cycle leaks — measure before adopting.
"""

L2_VI = L2_EN.replace(
    "## Reference counting and the garbage collector",
    "## Refcounting và bộ gom rác",
).replace(
    "CPython's primary memory management is **refcounting**: every object counts\nits references; hitting zero frees it immediately (hence the instant\n`__del__`-less determinism CPython is known for).",
    "Quản lý bộ nhớ chính của CPython là **refcounting**: mỗi đối tượng đếm số tham\nchiếu tới nó; chạm 0 là giải phóng ngay lập tức (nên CPython nổi tiếng về tính\nxác định tức thời, không cần `__del__`).",
).replace(
    "Refcounting alone cannot free **cycles** (a→b→a). A supplementary **cycle\ndetector** — the generational `gc` module — periodically scans container\nobjects for unreachable cycles:",
    "Một mình refcounting không thể giải phóng **chu kỳ** (a→b→a). Một **bộ phát hiện\nchu kỳ** bổ trợ — module `gc` thế hệ — định kỳ quét các đối tượng container tìm\nchu kỳ không thể chạm tới:",
).replace(
    "Practitioner takeaways:",
    "Điểm rút ra cho người thực hành:",
).replace(
    "- `sys.getrefcount(x)` shows the count (always +1 for the argument itself).\n- Most \"memory leaks\" in Python are *reference leaks*: caches, registries,\n  closures, or loggers holding objects forever. Find them with\n  `gc.get_referrers(obj)` — who still points at this?\n- `gc.garbage` collects objects the collector could not free (usually\n  `__del__`-bearing cycles) — its growth is a design smell.\n- `weakref` lets a cache reference objects without keeping them alive — the\n  standard fix for registry-induced leaks.\n- `gc.disable()` can speed allocation-heavy batch jobs slightly, at the cost of\n  cycle leaks — measure before adopting.",
    "- `sys.getrefcount(x)` hiển thị số đếm (luôn +1 cho chính đối số).\n- Đa số \"rò rỉ bộ nhớ\" trong Python là *rò rỉ tham chiếu*: cache, registry,\n  closure, hay logger giữ đối tượng mãi mãi. Tìm chúng bằng\n  `gc.get_referrers(obj)` — ai vẫn đang trỏ tới đây?\n- `gc.garbage` gom các đối tượng bộ gom không giải phóng được (thường là chu kỳ\ncó `__del__`) — nó phình to là một dấu hiệu thiết kế xấu.\n- `weakref` cho phép cache tham chiếu đối tượng mà không giữ chúng sống — bản\n  sửa chuẩn cho rò rỉ do registry.\n- `gc.disable()` có thể tăng tốc nhẹ cho batch job cấp phát nặng, đổi lại là\n  rò rỉ chu kỳ — hãy đo trước khi áp dụng.",
)

write_lesson(
    MOD, "gc-refcounting",
    "Refcounting, cycles, weakref",
    "Explain and diagnose memory behavior instead of fearing it.",
    20, L2_EN,
    "Refcounting, chu kỳ, weakref",
    "Giải thích và chẩn đoán hành vi bộ nhớ thay vì sợ nó.",
    L2_VI,
)

L3_EN = """
## The import system: modules, caches, and __main__

`import foo` performs a search, then a cached load:

1. Check `sys.modules` — the module cache. Already imported? Reuse the SAME
   module object (imports are cached per-process).
2. Find a **finder** willing to handle the name (`sys.meta_path`); default
   finders search `sys.path` for packages (directories with `__init__.py`) and
   modules (`.py` files).
3. **Execute** the module body in a fresh namespace, cache it in
   `sys.modules`, and bind the name in your namespace.

Consequences that explain everyday mysteries:

- **Import side effects run exactly once** per process — the second `import`
  is a dict lookup.
- **Circular imports** break when module A (mid-execution) triggers import of
  B, which imports A back and gets the half-built namespace. Fixes: reorder
  imports, import inside functions, or restructure the dependency.
- `__name__ == "__main__"` is true only when the file is run as the entry
  script; when *imported*, `__name__` is the module path — that is why the
  idiom guards CLI/demo code.
- **`.pyc` bytecode caches** (`__pycache__`) skip recompilation per source
  version — they are an optimization, invalidated by mtime/size.
- `sys.path` manipulation and namespace packages exist; prefer proper
  packaging (next module) over `sys.path.append` hacks.
"""

L3_VI = L3_EN.replace(
    "## The import system: modules, caches, and __main__",
    "## Hệ thống import: module, cache và __main__",
).replace(
    "`import foo` performs a search, then a cached load:",
    "`import foo` thực hiện tìm kiếm, rồi nạp từ cache:",
).replace(
    "1. Check `sys.modules` — the module cache. Already imported? Reuse the SAME\n   module object (imports are cached per-process).\n2. Find a **finder** willing to handle the name (`sys.meta_path`); default\n   finders search `sys.path` for packages (directories with `__init__.py`) and\n   modules (`.py` files).\n3. **Execute** the module body in a fresh namespace, cache it in\n   `sys.modules`, and bind the name in your namespace.",
    "1. Tra `sys.modules` — cache module. Đã import? Dùng lại ĐÚNG đối tượng module\n   đó (import được cache theo tiến trình).\n2. Tìm một **finder** chịu xử lý tên đó (`sys.meta_path`); các finder mặc định\n   tìm package (thư mục có `__init__.py`) và module (tệp `.py`) trên `sys.path`.\n3. **Thực thi** thân module trong namespace mới, cache vào `sys.modules`, và\n   gắn tên vào namespace của bạn.",
).replace(
    "Consequences that explain everyday mysteries:",
    "Những hệ quả giải thích các điều bí ẩn thường ngày:",
).replace(
    "- **Import side effects run exactly once** per process — the second `import`\n  is a dict lookup.\n- **Circular imports** break when module A (mid-execution) triggers import of\n  B, which imports A back and gets the half-built namespace. Fixes: reorder\n  imports, import inside functions, or restructure the dependency.\n- `__name__ == \"__main__\"` is true only when the file is run as the entry\n  script; when *imported*, `__name__` is the module path — that is why the\n  idiom guards CLI/demo code.\n- **`.pyc` bytecode caches** (`__pycache__`) skip recompilation per source\n  version — they are an optimization, invalidated by mtime/size.\n- `sys.path` manipulation and namespace packages exist; prefer proper\n  packaging (next module) over `sys.path.append` hacks.",
    "- **Side effect của import chạy đúng một lần** mỗi tiến trình — lần `import`\n  thứ hai chỉ là tra dict.\n- **Circular import** gãy khi module A (đang giữa chừng thực thi) kích hoạt\n  import B, mà B lại import A và nhận về namespace dở dang. Cách sửa: đổi thứ tự\n  import, import bên trong hàm, hoặc tái cấu trúc phụ thuộc.\n- `__name__ == \"__main__\"` chỉ đúng khi tệp được chạy làm script đầu vào; khi\n  bị *import*, `__name__` là đường dẫn module — vì thế idiom này canh code\n  CLI/demo.\n- **Cache bytecode `.pyc`** (`__pycache__`) bỏ qua bước biên dịch lại cho từng\n  phiên bản mã nguồn — chỉ là tối ưu, bị vô hiệu theo mtime/kích thước.\n- Có `sys.path` manipulation và namespace package; hãy ưu tiên đóng gói đúng\n  cách (module kế tiếp) thay các mẹo `sys.path.append`.",
)

write_lesson(
    MOD, "import-system",
    "Imports, sys.modules, circularity",
    "Explain import once-ness, circular failures, and __main__ semantics.",
    20, L3_EN,
    "Import, sys.modules, tính vòng",
    "Giải thích tính một-lần của import, lỗi vòng, và ngữ nghĩa __main__.",
    L3_VI,
)

# ── practice 1: bytecode ─────────────────────────────────────────────────────
BC_REF = (
    "import dis\n\n\n"
    "def instruction_names(func):\n"
    "    '''Return the list of instruction opnames for func, in order.'''\n"
    "    return [ins.opname for ins in dis.get_instructions(func)]\n\n\n"
    "def loop_loads_global(func, name):\n"
    "    hits = 0\n"
    "    for ins in dis.get_instructions(func):\n"
    "        if ins.opname == 'LOAD_GLOBAL' and ins.argrepr == name:\n"
    "            hits += 1\n"
    "    return hits >= 2"
)
BC_WRONG = (
    "import dis\n\n\n"
    "def instruction_names(func):\n"
    "    # WRONG: dis.dis PRINTS; it returns None — the list comprehension\n"
    "    # yields None values and crashes downstream\n"
    "    return [ins for ins in dis.dis(func)]\n\n\n"
    "def loop_loads_global(func, name):\n"
    "    # WRONG: counts ALL LOAD_GLOBALs (len/range included) — the hoisted\n"
    "    # variant also has 3, so it reports True for everything\n"
    "    return sum(1 for ins in dis.get_instructions(func) if ins.opname == 'LOAD_GLOBAL') >= 2"
)

write_practice(
    MOD, "pa-p7-bytecode-practice",
    "Bytecode Practice",
    "Drive the dis module programmatically: opname lists and global-lookup counting.",
    "Luyện Bytecode",
    "Điều khiển module dis bằng mã: danh sách opname và đếm tra cứu global.",
    "bytecode-frames", 18, "advanced",
    [
        challenge(
            "pa-int-dis-opnames",
            "Programmatic disassembly",
            "Implement two helpers using `dis.get_instructions` (NOT `dis.dis`, which prints):\n\n1. `instruction_names(func)` — list of `opname` strings in execution order.\n2. `loop_loads_global(func, name)` — True when the bytecode contains at least two `LOAD_GLOBAL` instructions (i.e. a lookup likely inside a loop rather than one-time setup).\n\nThe graded cases include a function that re-loads a global per iteration and one that binds it to a local first.",
            "import dis\n\n# TODO: instruction_names(func), loop_loads_global(func, name)",
            [
                ("opnames in order",
                 "def twice(x):\n    return helper(x) + helper(x)\n\nnames = instruction_names(twice)\nassert names.count('LOAD_GLOBAL') == 2, f'names: {names}'\nassert 'RETURN_VALUE' in names or 'RETURN' in names\nprint('ok')",
                 "dis.get_instructions(func) yields instruction objects with .opname."),
                ("loop-load detection via argrepr",
                 "G = list(range(10))\n\ndef loads_in_loop():\n    out = []\n    for i in range(3):\n        out.append(len(G))\n        out.append(G[i])\n    return out\n\ndef hoisted():\n    g = G\n    out = []\n    for i in range(3):\n        out.append(len(g))\n        out.append(g[i])\n    return out\n\nassert loop_loads_global(loads_in_loop, 'G'), 'loop version must load G inside the loop'\nassert not loop_loads_global(hoisted, 'G'), 'hoisted version loads G only once in setup'\nprint('ok')",
                 "Two G references inside the loop vs one in setup — argrepr distinguishes G from len/range."),
            ],
            level="independent",
        ),
    ],
    {
        "pa-int-dis-opnames": vi_challenge(
            "Dịch ngược bằng mã",
            "Cài hai helper dùng `dis.get_instructions` (KHÔNG phải `dis.dis` — nó chỉ print):\n\n1. `instruction_names(func)` — danh sách chuỗi `opname` theo thứ tự thực thi.\n2. `loop_loads_global(func, name)` — True khi bytecode chứa ít nhất hai lệnh `LOAD_GLOBAL` (tức tra cứu nằm trong vòng lặp chứ không phải setup một lần).\n\nCác case được chấm gồm một hàm nạp lại global mỗi vòng lặp và một hàm gắn nó vào biến local trước.",
            [("Opname theo thứ tự", "dis.get_instructions(func) sinh các đối tượng instruction có .opname."),
             ("Phát hiện nạp trong vòng lặp", "Đếm số lần xuất hiện LOAD_GLOBAL: bản đã hoisted chỉ tham chiếu G một lần.")],
        ),
    },
    solutions=[("pa-int-dis-opnames", BC_REF, BC_WRONG)],
)

# ── practice 2: refcounting/weakref ──────────────────────────────────────────
WK_REF = (
    "import weakref\n\n\n"
    "class WeakCache:\n"
    "    '''Caches objects by key WITHOUT keeping them alive; missing or\n"
    "    collected entries return None (via default_factory when given).'''\n"
    "    def __init__(self, default_factory=None):\n"
    "        self._refs = {}\n"
    "        self._factory = default_factory\n\n"
    "    def get(self, key):\n"
    "        ref = self._refs.get(key)\n"
    "        obj = ref() if ref is not None else None\n"
    "        if obj is None:\n"
    "            if self._factory is not None:\n"
    "                obj = self._factory(key)\n"
    "                self._refs[key] = weakref.ref(obj)\n"
    "            return obj\n"
    "        return obj\n\n"
    "    def put(self, key, obj):\n"
    "        self._refs[key] = weakref.ref(obj)"
)
WK_WRONG = (
    "import weakref\n\n\n"
    "class WeakCache:\n"
    "    def __init__(self, default_factory=None):\n"
    "        # WRONG: stores STRONG references — objects never become collectable\n"
    "        self._refs = {}\n"
    "        self._factory = default_factory\n\n"
    "    def get(self, key):\n"
    "        obj = self._refs.get(key)\n"
    "        if obj is None and self._factory is not None:\n"
    "            obj = self._factory(key)\n"
    "            self._refs[key] = obj\n"
    "        return obj\n\n"
    "    def put(self, key, obj):\n"
    "        self._refs[key] = obj"
)

write_practice(
    MOD, "pa-p7-gc-practice",
    "Memory Practice",
    "Weakrefs that let go: a cache that never leaks, verified with gc counts.",
    "Luyện Bộ nhớ",
    "Weakref biết buông tay: cache không bao giờ rò rỉ, kiểm chứng bằng bộ đếm gc.",
    "gc-refcounting", 20, "advanced",
    [
        challenge(
            "pa-int-weak-cache",
            "A cache that does not leak",
            "Implement `class WeakCache`:\n\n- `put(key, obj)` stores a WEAK reference to obj under key\n- `get(key)` returns the live object, or None once it has been garbage-collected (or was never put)\n- optional `default_factory(key)` builds and caches the object on a miss (also weakly)\n\nGraded probe: objects are created with no strong references left; after `gc.collect()`, `get` must return None — a strong-reference cache fails this.",
            "import weakref\n\n# TODO: WeakCache",
            [
                ("collected objects vanish from the cache",
                 "import gc\n\nclass Thing:\n    pass\n\nc = WeakCache()\nt = Thing()\nc.put('k', t)\nassert c.get('k') is t\ndel t\ngc.collect()\nassert c.get('k') is None, 'weak cache must let collected objects go'\nprint('ok')",
                 "weakref.ref(obj) stored per key; call the ref to get the object or None."),
                ("default_factory builds on miss",
                 "import gc\n\nclass Payload:\n    def __init__(self, key):\n        self.key = key\n    def __eq__(self, other):\n        return isinstance(other, Payload) and self.key == other.key\n\nmade = []\ndef factory(key):\n    made.append(key)\n    return Payload(key)\n\nc = WeakCache(factory)\nv1 = c.get('a')\nassert v1.key == 'a' and made == ['a']\nassert c.get('a') is v1  # still alive → same object, no rebuild\nassert made == ['a']\nprint('ok')",
                 "On miss with a factory: build, store weakly, return. (Payload keeps __weakref__ — plain dicts cannot be weak-referenced.)"),
            ],
            level="combination",
        ),
    ],
    {
        "pa-int-weak-cache": vi_challenge(
            "Cache không rò rỉ",
            "Cài `class WeakCache`:\n\n- `put(key, obj)` lưu tham chiếu YẾU tới obj theo key\n- `get(key)` trả về đối tượng còn sống, hoặc None khi nó đã bị gom rác (hoặc chưa từng put)\n- `default_factory(key)` tùy chọn sẽ dựng và cache đối tượng khi miss (cũng bằng weak)\n\nProbe chấm: đối tượng được tạo rồi không còn tham chiếu mạnh nào; sau `gc.collect()`, `get` phải trả None — cache dùng tham chiếu mạnh sẽ trượt.",
            [("Đối tượng bị gom thì biến mất khỏi cache", "weakref.ref(obj) lưu theo key; gọi ref để nhận đối tượng hoặc None."),
             ("default_factory dựng khi miss", "Khi miss có factory: dựng, lưu yếu, trả về.")],
        ),
    },
    solutions=[("pa-int-weak-cache", WK_REF, WK_WRONG)],
)

# ── practice 3: import system ────────────────────────────────────────────────
IMP_REF = (
    "import sys\n"
    "import types\n\n\n"
    "def fresh_import_counter():\n"
    "    '''Returns (module_obj, counter_getter). Re-importing an already-loaded\n"
    "    module must NOT re-execute its body: the body writes to a shared log\n"
    "    so the test can verify once-only execution.'''\n"
    "    log = []\n"
    "    mod = types.ModuleType('counter_demo')\n"
    "    mod.__dict__['__log__'] = log\n"
    "    mod.__dict__['bump'] = lambda: log.append(1)\n"
    "    sys.modules['counter_demo'] = mod\n"
    "    return mod, lambda: len(log)"
)
IMP_WRONG = IMP_REF  # identical reference (the challenge is about the test's import behavior)
IMP_WRONG = (
    "import sys\n"
    "import types\n\n\n"
    "def fresh_import_counter():\n"
    "    '''WRONG: registers a NEW module object on every call — the import\n"
    "    cache contract (same module object per process) is broken.'''\n"
    "    log = []\n"
    "    mod = types.ModuleType('counter_demo')\n"
    "    mod.__dict__['__log__'] = log\n"
    "    mod.__dict__['bump'] = lambda: log.append(1)\n"
    "    sys.modules['counter_demo'] = mod\n"
    "    return mod, lambda: len(log)"
)

write_practice(
    MOD, "pa-p7-import-practice",
    "Import System Practice",
    "Prove import caching semantics against sys.modules — once-per-process execution.",
    "Luyện Hệ thống Import",
    "Chứng minh ngữ nghĩa cache của import với sys.modules — thực thi một lần mỗi tiến trình.",
    "import-system", 20, "advanced",
    [
        challenge(
            "pa-int-import-cache",
            "Module identity and once-only bodies",
            "Implement `class ReloadableModule` demonstrating import-cache semantics:\n\n1. `install(name)` creates a `types.ModuleType(name)`, sets `mod.exec_count = 0`, registers it in `sys.modules[name]`, and stores it on `self.modules[name]`.\n2. `import_again(name)` returns `sys.modules[name]` WITHOUT re-executing anything.\n3. `simulate_body_execution(name)` increments that module's `exec_count += 1` (simulating a module body run).\n4. `identity_stable(name)` returns True when repeated `import_again` calls always return the SAME object.\n\nGraded checks: identity is stable; exec_count only changes when simulate_body_execution is explicitly called — mirroring real import-once semantics.",
            "import sys\nimport types\n\n# TODO: ReloadableModule",
            [
                ("identity is stable, body runs once",
                 "rm = ReloadableModule()\nrm.install('demo')\nrm.simulate_body_execution('demo')\nm1 = rm.import_again('demo')\nm2 = rm.import_again('demo')\nm3 = rm.import_again('demo')\nassert m1 is m2 is m3, 'import must return the same module object'\nassert m1.exec_count == 1, f'exec_count: {m1.exec_count}'\nassert rm.identity_stable('demo')\nprint('ok')",
                 "sys.modules[name] is the cache: import_again is a dict lookup, nothing executes."),
            ],
            level="independent",
        ),
    ],
    {
        "pa-int-import-cache": vi_challenge(
            "Bản thể module và thân hàm chạy một lần",
            "Cài `class ReloadableModule` mô phỏng ngữ nghĩa cache của import:\n\n1. `install(name)` tạo `types.ModuleType(name)`, đặt `mod.exec_count = 0`, đăng ký vào `sys.modules[name]`, và lưu vào `self.modules[name]`.\n2. `import_again(name)` trả về `sys.modules[name]` mà KHÔNG thực thi lại gì cả.\n3. `simulate_body_execution(name)` tăng `exec_count += 1` của module đó (mô phỏng một lần chạy thân module).\n4. `identity_stable(name)` trả True khi các lần `import_again` liên tiếp luôn trả về CÙNG đối tượng.\n\nKiểm tra chấm: bản thể ổn định; exec_count chỉ đổi khi simulate_body_execution được gọi tường minh — đúng ngữ nghĩa import-một-lần thật.",
            [("Bản thể ổn định, thân chạy một lần", "sys.modules[name] là cache: import_again chỉ tra dict, không gì được thực thi.")],
        ),
    },
    solutions=[("pa-int-import-cache",
                "import sys\nimport types\n\n\nclass ReloadableModule:\n    def __init__(self):\n        self.modules = {}\n\n    def install(self, name):\n        mod = types.ModuleType(name)\n        mod.exec_count = 0\n        sys.modules[name] = mod\n        self.modules[name] = mod\n        return mod\n\n    def import_again(self, name):\n        return sys.modules[name]\n\n    def simulate_body_execution(self, name):\n        sys.modules[name].exec_count += 1\n\n    def identity_stable(self, name):\n        target = sys.modules[name]\n        return all(self.import_again(name) is target for _ in range(3))",
                "import sys\nimport types\n\n\nclass ReloadableModule:\n    def __init__(self):\n        self.modules = {}\n\n    def install(self, name):\n        mod = types.ModuleType(name)\n        mod.exec_count = 0\n        sys.modules[name] = mod\n        self.modules[name] = mod\n        return mod\n\n    def import_again(self, name):\n        # WRONG: creates a fresh module object each call — breaks identity\n        mod = types.ModuleType(name)\n        mod.exec_count = 0\n        sys.modules[name] = mod\n        return mod\n\n    def simulate_body_execution(self, name):\n        sys.modules[name].exec_count += 1\n\n    def identity_stable(self, name):\n        target = sys.modules[name]\n        return all(self.import_again(name) is target for _ in range(3))")],
)

# ── practice 4 + project: internals investigation ────────────────────────────
INV_REF = (
    "import gc\n\n\n"
    "class Node:\n"
    "    def __init__(self):\n"
    "        self.partner = None\n\n\n"
    "def cycle_probe():\n"
    "    a, b = Node(), Node()\n"
    "    a.partner, b.partner = b, a\n"
    "    partners_wired = a.partner is b and b.partner is a\n"
    "    del a, b\n"
    "    collected = gc.collect()\n"
    "    return collected, partners_wired"
)
INV_WRONG = (
    "import gc\n\n\n"
    "class Node:\n"
    "    def __init__(self):\n"
    "        self.partner = None\n\n\n"
    "def cycle_probe():\n"
    "    # WRONG: never wires the cycle — refcounting frees both nodes and\n"
    "    # collect() has nothing cycle-related to reclaim\n"
    "    a, b = Node(), Node()\n"
    "    partners_wired = a.partner is b and b.partner is a\n"
    "    del a, b\n"
    "    collected = gc.collect()\n"
    "    return collected, partners_wired"
)

write_practice(
    MOD, "pa-p7-investigation-project",
    "Project: Internals Investigation",
    "Prove cycle-GC behavior with measurements — the scientific method applied to your runtime.",
    "Project: Khảo sát internals",
    "Chứng minh hành vi của cycle-GC bằng đo đạc — phương pháp khoa học áp lên runtime của bạn.",
    "import-system", 28, "advanced",
    [
        challenge(
            "pa-int-cycle-gc",
            "Prove the cycle collector works",
            "Implement `cycle_probe()`:\n\n1. Create two `Node` instances (class defined below has `partner = None`).\n2. Wire the cycle: `a.partner = b` and `b.partner = a`.\n3. Record `partners_wired = a.partner is b and b.partner is a`.\n4. Drop your local references to BOTH nodes.\n5. Run `gc.collect()` and capture its return value.\n6. Return `(collected, partners_wired)`.\n\nGrading asserts `partners_wired is True` AND `collected >= 2` — the two mutually-referencing nodes are only reclaimable by the cycle collector.",
            "import gc\n\nclass Node:\n    def __init__(self):\n        self.partner = None\n\n# TODO: cycle_probe()",
            [
                ("cycle is wired and reclaimed by collect()",
                 "collected, wired = cycle_probe()\nassert wired is True, f'wired: {wired}'\nassert collected >= 2, f'collected: {collected} — cycle must be collected'\nprint('ok')",
                 "Wire a.partner = b and b.partner = a BEFORE dropping references; then gc.collect()."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-int-cycle-gc": vi_challenge(
            "Chứng minh bộ gom chu kỳ hoạt động",
            "Cài `cycle_probe()`:\n\n1. Tạo hai instance `Node` (class bên dưới có `partner = None`).\n2. Nối chu kỳ: `a.partner = b` và `b.partner = a`.\n3. Ghi `partners_wired = a.partner is b and b.partner is a`.\n4. Bỏ tham chiếu cục bộ tới CẢ HAI node.\n5. Chạy `gc.collect()` và giữ giá trị trả về.\n6. Trả về `(collected, partners_wired)`.\n\nPhần chấm khẳng định `partners_wired là True` VÀ `collected >= 2` — hai node trỏ chéo nhau chỉ bộ gom chu kỳ thu hồi được.",
            [("Chu kỳ được nối và được thu hồi bởi collect()", "Nối a.partner = b và b.partner = a TRƯỚC khi bỏ tham chiếu; rồi gc.collect().")],
        ),
    },
    solutions=[("pa-int-cycle-gc", INV_REF, INV_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_REF = (
    "import dis\n\n\n"
    "def count_attr_loads(func):\n"
    "    '''Number of LOAD_ATTR instructions in func's bytecode.'''\n"
    "    return sum(1 for ins in dis.get_instructions(func) if ins.opname == 'LOAD_ATTR')\n\n\n"
    "def hoistable(func):\n"
    "    '''True when the same attribute is loaded more than once — i.e. a\n"
    "    lookup is repeated and could be hoisted out of a loop.'''\n"
    "    return count_attr_loads(func) > 1"
)
CK_WRONG = (
    "import dis\n\n\n"
    "def count_attr_loads(func):\n"
    "    # WRONG: counts ALL instructions — every function is 'hoistable'\n"
    "    return sum(1 for ins in dis.get_instructions(func))\n\n\n"
    "def hoistable(func):\n"
    "    return count_attr_loads(func) > 1"
)

write_checkpoint(
    MOD, "pa-checkpoint-internals",
    "Checkpoint: Internals",
    "Detect a hoistable attribute load from bytecode — internals applied to performance.",
    25,
    """
## Checkpoint — bytecode forensics

Implement:

- `count_attr_loads(func)` — how many `LOAD_ATTR` instructions does the
  function's bytecode contain? (Use `dis.get_instructions`.)
- `hoistable(func)` — True when an attribute lookup repeats (>1 LOAD_ATTR),
  i.e. hoisting it out of a loop is a candidate optimization.

This is the practical payoff of reading bytecode: spotting repeated work the
profiler only hints at.
""",
    "Checkpoint: Internals",
    "Phát hiện phép tra attribute có thể hoist từ bytecode — internals áp dụng cho hiệu năng.",
    """
## Checkpoint — pháp y bytecode

Cài:

- `count_attr_loads(func)` — bytecode của hàm chứa bao nhiêu lệnh `LOAD_ATTR`?\n  (Dùng `dis.get_instructions`.)
- `hoistable(func)` — True khi một phép tra attribute lặp lại (>1 LOAD_ATTR),\n  tức việc hoist nó ra khỏi vòng lặp là một ứng viên tối ưu.

Đây là phần thưởng thực dụng của việc đọc bytecode: phát hiện công việc lặp lại\nmà profiler chỉ mới gợi ý.
""",
    challenge(
        "pa-checkpoint-internals",
        "LOAD_ATTR forensics",
        "Implement count_attr_loads (exact count of LOAD_ATTR instructions) and hoistable (True iff more than one).",
        "import dis\n\n# TODO: count_attr_loads(func), hoistable(func)",
        [
            ("counts and flags correctly",
             "class Config:\n    def __init__(self):\n        self.f = [1, 2, 3]\n        self.g = [4]\n\ndef repeats(cfg):\n    return sum(cfg.f) + sum(cfg.f)  # two LOAD_ATTR on the same attr\n\ndef once(cfg):\n    return sum(cfg.f)            # one LOAD_ATTR\n\ndef plain(x):\n    return x + 1                 # no attributes at all\n\nr = count_attr_loads(repeats)\nassert r == 2, f'count: {r}'\nassert count_attr_loads(once) == 1\nassert count_attr_loads(plain) == 0\nassert hoistable(repeats)\nassert not hoistable(once)\nassert not hoistable(plain)\nprint('ok')",
             "LOAD_ATTR appears once per attribute access on an object; in 3.11 method calls also use LOAD_ATTR (LOAD_METHOD merged)."),
        ],
        level="build",
    ),
    vi_challenge(
        "Pháp y LOAD_ATTR",
        "Cài count_attr_loads (đếm chính xác số lệnh LOAD_ATTR) và hoistable (True khi và chỉ khi nhiều hơn một).",
        [("Đếm và cờ đúng", "LOAD_ATTR xuất hiện một lần cho mỗi lần truy cập attribute trên đối tượng; gắn vào biến local xóa sạch chúng.")],
    ),
    solution=CK_REF,
    wrong=CK_WRONG,
)

print("module 7 complete")
