#!/usr/bin/env python3
"""Module 8: architecture-patterns — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "architecture-patterns"

write_module(
    MOD,
    "Architecture: Boundaries That Earn Their Keep",
    "Ports & adapters, dependency inversion, repositories, DI containers — every pattern justified by a problem it solves, plus refactoring a tangle without changing behavior.",
    "Kiến trúc: Ranh giới đáng giá",
    "Ports & adapters, dependency inversion, repository, DI container — mỗi pattern đều có vấn đề nó giải quyết, cộng với refactor một mớ hỗn độn mà không đổi hành vi.",
    ["coupling-boundaries", "ports-adapters", "dependency-injection"],
    ["pa-p8-boundary-practice", "pa-p8-repo-practice", "pa-p8-refactor-project"],
)

L1_EN = """
## Coupling: the thing architecture actually manages

Architecture is not folders and diagrams — it is the management of **coupling**:
how much one piece of code must know about another to work.

Two symptoms tell you coupling is too high:

- **Change amplification**: one business rule change forces edits across many
  files ("I touched 14 files to rename a field").
- **Test impossibility**: you cannot exercise business logic without a real
  database, real HTTP, real clock.

Coupling itself is not evil — the *direction* matters. Business rules should
not know about delivery mechanisms (HTTP, CLI), persistence (SQL), or vendors.
Those details should depend on the domain, never the reverse. That is the
whole idea behind **dependency inversion**: high-level policy defines an
interface; low-level detail implements it; the wiring points the dependency
arrow inwards.

The pragmatic test for every abstraction you add: **name the second
implementation.** If there is only ever one implementation and no testing or
boundary need, the interface is ceremony. (The test double in your unit tests
counts as a second implementation.)
"""

L1_VI = L1_EN.replace(
    "## Coupling: the thing architecture actually manages",
    "## Coupling: thứ mà kiến trúc thực sự quản lý",
).replace(
    "Architecture is not folders and diagrams — it is the management of **coupling**:\nhow much one piece of code must know about another to work.",
    "Kiến trúc không phải là thư mục và sơ đồ — nó là việc quản lý **coupling**:\nmột đoạn code phải biết bao nhiêu về đoạn khác để hoạt động.",
).replace(
    "Two symptoms tell you coupling is too high:",
    "Hai triệu chứng cho biết coupling đã quá cao:",
).replace(
    "- **Change amplification**: one business rule change forces edits across many\n  files (\"I touched 14 files to rename a field\").\n- **Test impossibility**: you cannot exercise business logic without a real\n  database, real HTTP, real clock.",
    "- **Khuếch đại thay đổi**: một thay đổi quy tắc nghiệp vụ buộc phải sửa nhiều\n  tệp (\"đổi tên một field mà phải đụng 14 tệp\").\n- **Không thể kiểm thử**: không thể chạy logic nghiệp vụ nếu không có database\n  thật, HTTP thật, đồng hồ thật.",
).replace(
    "Coupling itself is not evil — the *direction* matters. Business rules should\nnot know about delivery mechanisms (HTTP, CLI), persistence (SQL), or vendors.\nThose details should depend on the domain, never the reverse. That is the\nwhole idea behind **dependency inversion**: high-level policy defines an\ninterface; low-level detail implements it; the wiring points the dependency\narrow inwards.",
    "Coupling không xấu — *hướng* mới là điều quan trọng. Quy tắc nghiệp vụ không\nnên biết về cơ chế giao tiếp (HTTP, CLI), lưu trữ (SQL), hay nhà cung cấp.\nNhững chi tiết đó phải phụ thuộc vào domain, không bao giờ ngược lại. Đó là\ntoàn bộ ý tưởng của **dependency inversion**: chính sách cấp cao định nghĩa\ninterface; chi tiết cấp thấp cài đặt nó; phần nối dây hướng mũi tên phụ thuộc\nvào trong.",
).replace(
    "The pragmatic test for every abstraction you add: **name the second\nimplementation.** If there is only ever one implementation and no testing or\nboundary need, the interface is ceremony. (The test double in your unit tests\ncounts as a second implementation.)",
    "Bài thử thực dụng cho mọi abstraction bạn thêm vào: **hãy gọi tên bản cài đặt\nthứ hai.** Nếu chỉ có duy nhất một bản cài và không có nhu cầu kiểm thử hay\nranh giới, interface đó chỉ là nghi lễ. (Test double trong unit test của bạn\nđược tính là bản cài thứ hai.)",
)

write_lesson(
    MOD, "coupling-boundaries",
    "Coupling, change amplification, inversion",
    "Diagnose unhealthy coupling; point dependency arrows inwards.",
    18, L1_EN,
    "Coupling, khuếch đại thay đổi, đảo chiều phụ thuộc",
    "Chẩn đoán coupling không lành mạnh; hướng mũi tên phụ thuộc vào trong.",
    L1_VI,
)

L2_EN = """
## Ports & adapters with real seams

A **port** is an interface owned by the application core. An **adapter** is a
piece of infrastructure that fulfills it. The core defines `NotificationSender`
and `OrderRepository`; the adapters are `SendGridSender`, `SmtpSender`,
`PostgresOrderRepository`, `InMemoryOrderRepository` (for tests).

```python
from typing import Protocol

class OrderRepository(Protocol):
    def get(self, order_id: str) -> "Order | None": ...
    def save(self, order: "Order") -> None: ...

class PlaceOrder:                      # application service — the core
    def __init__(self, repo: OrderRepository, notify: NotificationSender):
        self._repo = repo
        self._notify = notify

    def __call__(self, order: "Order") -> None:
        self._repo.save(order)
        self._notify.order_placed(order)
```

What this buys, concretely:

- **Business logic tests run in-memory** — no Postgres, no HTTP, no mocks of
  the *domain*, only fakes at the port.
- **Swapping infrastructure is a wiring change**, not a rewrite: Postgres →
  DynamoDB touches one adapter.
- **The core compiles without knowing HTTP exists.**

The failure mode to avoid: a repository per table leaking SQL-shaped shapes
(`QuerySet`, `Row`) into the domain. The port speaks the *domain's* language
(`Order`, `OrderNotFound`), and the adapter translates.
"""

L2_VI = L2_EN.replace(
    "## Ports & adapters with real seams",
    "## Ports & adapters với đường nối thật",
).replace(
    "A **port** is an interface owned by the application core. An **adapter** is a\npiece of infrastructure that fulfills it. The core defines `NotificationSender`\nand `OrderRepository`; the adapters are `SendGridSender`, `SmtpSender`,\n`PostgresOrderRepository`, `InMemoryOrderRepository` (for tests).",
    "**Port** là interface thuộc sở hữu của phần lõi ứng dụng. **Adapter** là mảnh\nhạ tầng thực hiện nó. Lõi định nghĩa `NotificationSender` và `OrderRepository`;\ncác adapter là `SendGridSender`, `SmtpSender`, `PostgresOrderRepository`,\n`InMemoryOrderRepository` (cho test).",
).replace(
    "What this buys, concretely:",
    "Điều này mua được gì, một cách cụ thể:",
).replace(
    "- **Business logic tests run in-memory** — no Postgres, no HTTP, no mocks of\n  the *domain*, only fakes at the port.\n- **Swapping infrastructure is a wiring change**, not a rewrite: Postgres →\n  DynamoDB touches one adapter.\n- **The core compiles without knowing HTTP exists.**",
    "- **Test logic nghiệp vụ chạy trong bộ nhớ** — không Postgres, không HTTP,\n  không mock *domain*, chỉ fake ở các port.\n- **Đổi hạ tầng là đổi chỗ nối dây**, không phải viết lại: Postgres → DynamoDB\n  chỉ đụng một adapter.\n- **Lõi biên dịch được mà không biết HTTP tồn tại.**",
).replace(
    "The failure mode to avoid: a repository per table leaking SQL-shaped shapes\n(`QuerySet`, `Row`) into the domain. The port speaks the *domain's* language\n(`Order`, `OrderNotFound`), and the adapter translates.",
    "Kiểu thất bại cần tránh: repository-mỗi-bảng làm rò rỉ các hình dạng kiểu SQL\n(`QuerySet`, `Row`) vào domain. Port phải nói *ngôn ngữ của domain*\n(`Order`, `OrderNotFound`), adapter là người phiên dịch.",
)

write_lesson(
    MOD, "ports-adapters",
    "Ports, adapters, repositories",
    "Own the interface in the core; translate at the edge.",
    22, L2_EN,
    "Port, adapter, repository",
    "Sở hữu interface trong lõi; phiên dịch ở rìa.",
    L2_VI,
)

L3_EN = """
## Dependency injection without a framework

DI means dependencies arrive from outside instead of being constructed inside.
Python needs no framework for this — an `__init__` is a container:

```python
class ReportService:
    def __init__(self, repo, clock, mailer):     # all seams visible
        self._repo, self._clock, self._mailer = repo, clock, mailer
```

- **Constructor injection** is the default: required collaborators are
  arguments. Everything the object needs is visible in the signature.
- **Functional core, imperative shell**: keep decisions in pure functions
  `(data) -> data`, push I/O to the edges. The shell is thin and boring;
  the core is trivially testable.
- **Composition root**: one place (often `main()` or a tiny factory) builds
  real objects and wires them. Tests build a different graph with fakes.
- **The clock, the RNG, the UUID factory are dependencies.** Time-dependent
  logic is untestable only because `datetime.now()` is hidden inside. Inject
  `clock` and pass a fixed fake in tests.
- When construction graphs grow large, a tiny factory function beats a DI
  framework: explicit, greppable, debuggable.
"""

L3_VI = L3_EN.replace(
    "## Dependency injection without a framework",
    "Dependency injection không cần framework",
).replace(
    "DI means dependencies arrive from outside instead of being constructed inside.\nPython needs no framework for this — an `__init__` is a container:",
    "DI nghĩa là các phụ thuộc đến từ bên ngoài thay vì được dựng bên trong.\nPython không cần framework cho việc này — một `__init__` chính là container:",
).replace(
    "- **Constructor injection** is the default: required collaborators are\n  arguments. Everything the object needs is visible in the signature.\n- **Functional core, imperative shell**: keep decisions in pure functions\n  `(data) -> data`, push I/O to the edges. The shell is thin and boring;\n  the core is trivially testable.\n- **Composition root**: one place (often `main()` or a tiny factory) builds\n  real objects and wires them. Tests build a different graph with fakes.\n- **The clock, the RNG, the UUID factory are dependencies.** Time-dependent\n  logic is untestable only because `datetime.now()` is hidden inside. Inject\n  `clock` and pass a fixed fake in tests.\n- When construction graphs grow large, a tiny factory function beats a DI\n  framework: explicit, greppable, debuggable.",
    "- **Constructor injection** là mặc định: cộng tác viên bắt buộc là tham số.\n  Mọi thứ đối tượng cần đều hiện hữu trong chữ ký.\n- **Lõi hàm thuần, vỏ mệnh lệnh**: giữ các quyết định trong hàm thuần\n  `(data) -> data`, đẩy I/O ra rìa. Vỏ mỏng và nhàm chán; lõi thì dễ kiểm thử\n  vô cùng.\n- **Composition root**: một nơi duy nhất (thường là `main()` hay một factory\n  nhỏ) dựng đối tượng thật và nối chúng. Test dựng một đồ thị khác bằng fake.\n- **Đồng hồ, RNG, UUID factory là phụ thuộc.** Logic phụ thuộc thời gian chỉ\n  khó kiểm thử vì `datetime.now()` bị giấu bên trong. Hãy inject `clock` và\n  truyền một fake cố định trong test.\n- Khi đồ thị dựng对象 phình to, một hàm factory nhỏ thắng mọi DI framework:\n  tường minh, grep được, debug được.",
).replace("dựng đối tượng phình to", "dựng đối tượng phình to")

write_lesson(
    MOD, "dependency-injection",
    "DI, composition root, the clock",
    "Make dependencies visible in signatures; test time itself by injecting it.",
    20, L3_EN,
    "DI, composition root, đồng hồ",
    "Biến phụ thuộc thành hiện hữu trong chữ ký; kiểm thử chính thời gian bằng cách inject nó.",
    L3_VI,
)

# ── practice 1: boundaries / inversion ───────────────────────────────────────
BOUNDARY_REF = (
    "from typing import Protocol\n\n\n"
    "class Notifier(Protocol):\n"
    "    def send(self, to: str, message: str) -> None: ...\n\n\n"
    "class PasswordResetService:\n"
    "    '''Core service. Depends on the Notifier PORT — never on a concrete\n"
    "    email vendor. Errors from the port propagate.'''\n"
    "    def __init__(self, notifier):\n"
    "        self._notifier = notifier\n\n"
    "    def reset(self, user, token):\n"
    "        if not user.get('email'):\n"
    "            raise ValueError('user has no email')\n"
    "        self._notifier.send(user['email'], f'reset token: {token}')\n"
    "        return True"
)
BOUNDARY_WRONG = (
    "from typing import Protocol\n\n\n"
    "class Notifier(Protocol):\n"
    "    def send(self, to: str, message: str) -> None: ...\n\n\n"
    "class PasswordResetService:\n"
    "    def __init__(self, notifier):\n"
    "        self._notifier = notifier\n\n"
    "    def reset(self, user, token):\n"
    "        if not user.get('email'):\n"
    "            # WRONG: silently skips — caller can't tell success from skip\n"
    "            return False\n"
    "        self._notifier.send(user['email'], f'reset token: {token}')\n"
    "        return True"
)

write_practice(
    MOD, "pa-p8-boundary-practice",
    "Boundary Practice",
    "Point the dependency arrow inwards: a core service that owns its port.",
    "Luyện Ranh giới",
    "Hướng mũi tên phụ thuộc vào trong: service lõi sở hữu port của nó.",
    "coupling-boundaries", 20, "advanced",
    [
        challenge(
            "pa-arch-inverted-service",
            "The service owns the port",
            "Implement `PasswordResetService(notifier)`:\n\n- `notifier` is ANY object with `send(to, message)` (define a `Notifier` Protocol in the solution for documentation)\n- `reset(user, token)` sends `'reset token: <token>'` to `user['email']` and returns True\n- a user without an email raises `ValueError('user has no email')`\n- the service must never import or name a concrete vendor — graded by running it against two DIFFERENT notifier implementations",
            "from typing import Protocol\n\n# TODO: Notifier protocol + PasswordResetService",
            [
                ("works with any port implementation",
                 "class SpyNotifier:\n    def __init__(self):\n        self.sent = []\n    def send(self, to, message):\n        self.sent.append((to, message))\n\nclass SmsNotifier:\n    def __init__(self):\n        self.sent = []\n    def send(self, to, message):\n        self.sent.append((to, 'SMS:' + message))\n\nsvc = PasswordResetService(SpyNotifier())\nassert svc.reset({'email': 'a@x.y'}, 'tok1') is True\nsvc2 = PasswordResetService(SmsNotifier())\nassert svc2.reset({'email': 'b@x.y'}, 'tok2') is True\nprint('ok')",
                 "The constructor takes the port; the service calls only send()."),
                ("missing email fails loudly",
                 "class SpyNotifier:\n    def __init__(self):\n        self.sent = []\n    def send(self, to, message):\n        self.sent.append((to, message))\n\nspy = SpyNotifier()\nsvc = PasswordResetService(spy)\ntry:\n    svc.reset({}, 'tok')\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('missing email must raise ValueError')\nassert spy.sent == [], 'nothing may be sent on failure'\nprint('ok')",
                 "Validate before any side effect."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-arch-inverted-service": vi_challenge(
            "Service sở hữu port",
            "Cài `PasswordResetService(notifier)`:\n\n- `notifier` là BẤT KỲ đối tượng nào có `send(to, message)` (định nghĩa Protocol `Notifier` trong lời giải để làm tài liệu)\n- `reset(user, token)` gửi `'reset token: <token>'` tới `user['email']` và trả True\n- user không có email raise `ValueError('user has no email')`\n- service không được import hay nhắc tới một vendor cụ thể nào — chấm bằng cách chạy nó với HAI bản cài notifier khác nhau",
            [("Chạy được với mọi bản cài port", "Constructor nhận port; service chỉ gọi send()."),
             ("Thiếu email phải fail ầm ĩ", "Kiểm tra trước mọi side effect.")],
        ),
    },
    solutions=[("pa-arch-inverted-service", BOUNDARY_REF, BOUNDARY_WRONG)],
)

# ── practice 2: repository ───────────────────────────────────────────────────
REPO_REF = (
    "class InMemoryOrderRepository:\n"
    "    '''Domain-shaped repository. Stores Order dicts; raises domain errors.'''\n"
    "    class OrderNotFound(Exception):\n"
    "        pass\n\n"
    "    def __init__(self):\n"
    "        self._orders = {}\n\n"
    "    def get(self, order_id):\n"
    "        try:\n"
    "            return dict(self._orders[order_id])\n"
    "        except KeyError:\n"
    "            raise self.OrderNotFound(order_id) from None\n\n"
    "    def save(self, order):\n"
    "        self._orders[order['id']] = dict(order)\n\n"
    "    def all(self):\n"
    "        return [dict(o) for o in self._orders.values()]"
)
REPO_WRONG = (
    "class InMemoryOrderRepository:\n"
    "    class OrderNotFound(Exception):\n"
    "        pass\n\n"
    "    def __init__(self):\n"
    "        self._orders = {}\n\n"
    "    def get(self, order_id):\n"
    "        try:\n"
    "            # WRONG: returns the STORED object itself — callers mutate\n"
    "            # repository state through the returned reference\n"
    "            return self._orders[order_id]\n"
    "        except KeyError:\n"
    "            raise self.OrderNotFound(order_id) from None\n\n"
    "    def save(self, order):\n"
    "        self._orders[order['id']] = order\n\n"
    "    def all(self):\n"
    "        return list(self._orders.values())"
)

write_practice(
    MOD, "pa-p8-repo-practice",
    "Repository Practice",
    "A repository that speaks the domain's language — and defends its own state.",
    "Luyện Repository",
    "Repository nói ngôn ngữ của domain — và tự vệ trước trạng thái của chính nó.",
    "ports-adapters", 20, "advanced",
    [
        challenge(
            "pa-arch-repository",
            "InMemoryOrderRepository",
            "Implement `InMemoryOrderRepository`:\n\n- nested exception `OrderNotFound`\n- `save(order)` stores a COPY of the order dict (keyed by `order['id']`)\n- `get(order_id)` returns a COPY; unknown id raises `OrderNotFound`\n- `all()` returns a list of copies\n\nGraded probe: mutating the dict you received from `get()` must NOT change repository state — storage leaks through shared references are the classic repository bug.",
            "class InMemoryOrderRepository:\n    # TODO",
            [
                ("copy semantics on the way in and out",
                 "repo = InMemoryOrderRepository()\norder = {'id': 'o1', 'total': 10}\nrepo.save(order)\norder['total'] = 999  # caller mutates their own dict\nstored = repo.get('o1')\nassert stored['total'] == 10, f'stored: {stored}'\nstored['total'] = 42   # caller mutates the returned copy\nassert repo.get('o1')['total'] == 10, 'repository state must not leak'\nprint('ok')",
                 "dict(order) on save and on get — defensive copies both ways."),
                ("domain error for unknown ids",
                 "repo = InMemoryOrderRepository()\ntry:\n    repo.get('nope')\nexcept InMemoryOrderRepository.OrderNotFound:\n    pass\nelse:\n    raise AssertionError('unknown id must raise OrderNotFound')\nassert repo.all() == []\nprint('ok')",
                 "Translate KeyError into the domain exception."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-arch-repository": vi_challenge(
            "InMemoryOrderRepository",
            "Cài `InMemoryOrderRepository`:\n\n- exception lồng nhau `OrderNotFound`\n- `save(order)` lưu một BẢN SAO của order dict (keyed theo `order['id']`)\n- `get(order_id)` trả về một BẢN SAO; id lạ raise `OrderNotFound`\n- `all()` trả về danh sách các bản sao\n\nProbe chấm: việc mutate dict bạn nhận từ `get()` KHÔNG được đổi trạng thái repository — rò rỉ trạng thái qua tham chiếu dùng chung là bug kinh điển của repository.",
            [("Ngữ nghĩa bản sao vào và ra", "dict(order) khi lưu và khi lấy — bản sao phòng thủ theo cả hai hướng."),
             ("Lỗi domain cho id lạ", "Chuyển KeyError thành exception domain.")],
        ),
    },
    solutions=[("pa-arch-repository", REPO_REF, REPO_WRONG)],
)

# ── practice 3 + project: refactor without behavior change ───────────────────
REFACTOR_REF = (
    "def process_orders(orders, notifier, audit):\n"
    "    '''Refactored contract (behavior preserved):\n"
    "    - orders with total <= 0 are SKIPPED (still logged to audit as 'skipped')\n"
    "    - valid orders are notified then audited as 'sent'\n"
    "    - notification failure aborts the batch: audit gets 'failed', and the\n"
    "      exception PROPAGATES after logging\n"
    "    Returns the audit list.'''\n"
    "    for order in orders:\n"
    "        if order['total'] <= 0:\n"
    "            audit.append({'id': order['id'], 'status': 'skipped'})\n"
    "            continue\n"
    "        try:\n"
    "            notifier.send(order['email'], f\"order {order['id']} confirmed\")\n"
    "        except Exception:\n"
    "            audit.append({'id': order['id'], 'status': 'failed'})\n"
    "            raise\n"
    "        audit.append({'id': order['id'], 'status': 'sent'})\n"
    "    return audit"
)
REFACTOR_WRONG = (
    "def process_orders(orders, notifier, audit):\n"
    "    '''WRONG: swallows the notification failure — the batch continues and\n"
    "    no exception propagates, breaking the documented behavior.'''\n"
    "    for order in orders:\n"
    "        if order['total'] <= 0:\n"
    "            audit.append({'id': order['id'], 'status': 'skipped'})\n"
    "            continue\n"
    "        try:\n"
    "            notifier.send(order['email'], f\"order {order['id']} confirmed\")\n"
    "        except Exception:\n"
    "            audit.append({'id': order['id'], 'status': 'failed'})\n"
    "            continue\n"
    "        audit.append({'id': order['id'], 'status': 'sent'})\n"
    "    return audit"
)

write_practice(
    MOD, "pa-p8-refactor-project",
    "Project: Refactor Without Behavior Change",
    "Untangle a procedural order pipeline into a testable seam — byte-for-byte compatible behavior.",
    "Project: Refactor không đổi hành vi",
    "Gỡ rối pipeline order kiểu thủ tục thành một seam kiểm thử được — hành vi tương thích từng byte.",
    "dependency-injection", 30, "advanced",
    [
        challenge(
            "pa-arch-refactor-pipeline",
            "Preserve the contract, restructure the code",
            "Implement `process_orders(orders, notifier, audit)` per this EXACT contract (given as the refactored behavior):\n\n- for each order: total <= 0 → append `{'id': id, 'status': 'skipped'}` to `audit`, continue\n- otherwise `notifier.send(order['email'], 'order <id> confirmed')`; success → append `'sent'`\n- on notification failure → append `'failed'` to audit, then RE-RAISE the exception (batch aborts)\n- return the audit list\n\nThe hidden probe verifies three different notifier behaviors (happy, one failure mid-batch, all-skipped) — your implementation must match the contract exactly, in order.",
            "def process_orders(orders, notifier, audit):\n    # audit: list mutated in place; returns audit\n    pass",
            [
                ("happy path appends in order",
                 "class Spy:\n    def __init__(self):\n        self.sent = []\n    def send(self, to, message):\n        self.sent.append((to, message))\n\nspy = Spy()\naudit = []\nout = process_orders(\n    [\n        {'id': 'a', 'total': 5, 'email': 'a@x'},\n        {'id': 'b', 'total': 0, 'email': 'b@x'},\n        {'id': 'c', 'total': 7, 'email': 'c@x'},\n    ],\n    spy,\n    audit,\n)\nassert out is audit\nassert out == [\n    {'id': 'a', 'status': 'sent'},\n    {'id': 'b', 'status': 'skipped'},\n    {'id': 'c', 'status': 'sent'},\n], f'audit: {out}'\nassert spy.sent == [('a@x', 'order a confirmed'), ('c@x', 'order c confirmed')]\nprint('ok')",
                 "Skip invalid totals BEFORE sending; append statuses in encounter order."),
                ("failure aborts the batch after auditing",
                 "class Flaky:\n    def __init__(self):\n        self.calls = 0\n    def send(self, to, message):\n        self.calls += 1\n        if self.calls == 2:\n            raise RuntimeError('smtp down')\n\naudit = []\ntry:\n    process_orders(\n        [\n            {'id': 'a', 'total': 1, 'email': 'a@x'},\n            {'id': 'b', 'total': 1, 'email': 'b@x'},\n            {'id': 'c', 'total': 1, 'email': 'c@x'},\n        ],\n        Flaky(),\n        audit,\n    )\nexcept RuntimeError:\n    pass\nelse:\n    raise AssertionError('failure must propagate')\nassert audit == [\n    {'id': 'a', 'status': 'sent'},\n    {'id': 'b', 'status': 'failed'},\n], f'audit: {audit}'\nprint('ok')",
                 "Append 'failed' to audit, then re-raise — the third order must never be touched."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-arch-refactor-pipeline": vi_challenge(
            "Giữ hợp đồng, tái cấu trúc code",
            "Cài `process_orders(orders, notifier, audit)` theo ĐÚNG hợp đồng này (đưa ra như hành vi đã refactor):\n\n- với mỗi order: total <= 0 → append `{'id': id, 'status': 'skipped'}` vào `audit`, tiếp tục\n- ngược lại `notifier.send(order['email'], 'order <id> confirmed')`; thành công → append `'sent'`\n- khi thông báo lỗi → append `'failed'` vào audit, rồi RE-RAISE exception (cả lô dừng)\n- trả về danh sách audit\n\nProbe ẩn kiểm tra ba hành vi notifier khác nhau (suôn sẻ, lỗi một lần giữa lô, tất cả bị bỏ qua) — bản cài của bạn phải khớp hợp đồng chính xác, đúng thứ tự.",
            [("Đường vui append đúng thứ tự", "Bỏ qua total không hợp lệ TRƯỚC khi gửi; append trạng thái theo thứ tự gặp phải."),
             ("Lỗi dừng cả lô sau khi ghi audit", "Append 'failed' vào audit, rồi re-raise — order thứ ba không bao giờ bị đụng tới.")],
        ),
    },
    solutions=[("pa-arch-refactor-pipeline", REFACTOR_REF, REFACTOR_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_REF = (
    "class CheckoutService:\n"
    "    '''Constructor-injected service: repo + clock. No hidden dependencies.'''\n"
    "    def __init__(self, repo, clock):\n"
    "        self._repo = repo\n"
    "        self._clock = clock\n\n"
    "    def checkout(self, cart):\n"
    "        if not cart:\n"
    "            raise ValueError('empty cart')\n"
    "        order = {\n"
    "            'id': f\"o-{self._clock.now():.0f}\",\n"
    "            'items': list(cart),\n"
    "            'total': sum(cart),\n"
    "        }\n"
    "        self._repo.save(order)\n"
    "        return order"
)
CK_WRONG = (
    "class CheckoutService:\n"
    "    def __init__(self, repo, clock):\n"
    "        self._repo = repo\n"
    "        self._clock = clock\n\n"
    "    def checkout(self, cart):\n"
    "        # WRONG: accepts the empty cart and stores a zero-total order\n"
    "        order = {\n"
    "            'id': f\"o-{self._clock.now():.0f}\",\n"
    "            'items': list(cart),\n"
    "            'total': sum(cart),\n"
    "        }\n"
    "        self._repo.save(order)\n"
    "        return order"
)

write_checkpoint(
    MOD, "pa-checkpoint-architecture",
    "Checkpoint: Architecture",
    "Assemble an injected service: repository + injected clock, deterministic ids.",
    28,
    """
## Checkpoint — an injected checkout

Implement `CheckoutService(repo, clock)`:

- `checkout(cart)` builds `{'id': f'o-{clock.now():.0f}', 'items': list(cart), 'total': sum(cart)}`, saves it via the repository, and returns it
- an empty cart raises `ValueError('empty cart')` — nothing saved
- the clock is INJECTED (`clock.now()` returns a float) — the graded test uses
  a fixed fake clock and asserts the id and totals exactly

Constructor injection + injected time = deterministic tests. That is the lesson.
""",
    "Checkpoint: Kiến trúc",
    "Lắp ráp một service được inject: repository + đồng hồ inject, id tất định.",
    """
## Checkpoint — checkout được inject

Cài `CheckoutService(repo, clock)`:

- `checkout(cart)` dựng `{'id': f'o-{clock.now():.0f}', 'items': list(cart), 'total': sum(cart)}`, lưu qua repository, và trả về nó
- giỏ rỗng raise `ValueError('empty cart')` — không lưu gì cả
- đồng hồ được INJECT (`clock.now()` trả một số thực) — test được chấm dùng\n  một fake clock cố định và khẳng định id và tổng chính xác

Constructor injection + thời gian inject = test tất định. Đó chính là bài học.
""",
    challenge(
        "pa-checkpoint-architecture",
        "Injected checkout service",
        "Implement CheckoutService(repo, clock) per the spec: injected clock drives ids; empty carts raise before saving; totals are sums of the cart.",
        "class CheckoutService:\n    def __init__(self, repo, clock):\n        pass\n\n    def checkout(self, cart):\n        pass",
        [
            ("deterministic order with fixed clock",
             "class FakeClock:\n    def __init__(self, t):\n        self.t = t\n    def now(self):\n        return self.t\n\nclass MemRepo:\n    def __init__(self):\n        self.saved = []\n    def save(self, order):\n        self.saved.append(dict(order))\n\nrepo = MemRepo()\nsvc = CheckoutService(repo, FakeClock(1712345678.9))\norder = svc.checkout([10, 20, 12])\nassert order['id'] == 'o-1712345679', f'id: {order[\"id\"]}'\nassert order['total'] == 42 and order['items'] == [10, 20, 12]\nassert repo.saved == [order]\nprint('ok')",
                 "Build the id from clock.now(); save then return the same dict."),
            ("empty cart raises before saving",
             "class FakeClock:\n    def __init__(self, t):\n        self.t = t\n    def now(self):\n        return self.t\n\nclass MemRepo:\n    def __init__(self):\n        self.saved = []\n    def save(self, order):\n        self.saved.append(dict(order))\n\nrepo = MemRepo()\nsvc = CheckoutService(repo, FakeClock(1.0))\ntry:\n    svc.checkout([])\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('empty cart must raise ValueError')\nassert repo.saved == [], 'nothing may be saved'\nprint('ok')",
                 "Validate before constructing or persisting anything."),
        ],
        level="build",
    ),
    vi_challenge(
        "Service checkout được inject",
        "Cài CheckoutService(repo, clock) theo đặc tả: đồng hồ inject điều khiển id; giỏ rỗng raise trước khi lưu; tổng là tổng của giỏ.",
        [("Order tất định với đồng hồ cố định", "Dựng id từ clock.now(); lưu rồi trả về cùng dict đó."),
         ("Giỏ rỗng raise trước khi lưu", "Kiểm tra trước khi dựng hay lưu bất cứ gì.")],
    ),
    solution=CK_REF,
    wrong=CK_WRONG,
)

print("module 8 complete")
