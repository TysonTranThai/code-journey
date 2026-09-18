#!/usr/bin/env python3
"""Module 14: production-tooling — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "production-tooling"

# ── lesson 1 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "packaging-and-entry-points",
    "Packaging and Entry Points",
    "From a pile of modules to an installable, versioned, lockfile-pinned tool that installs with one command.",
    28,
    """
## pyproject.toml: the one file that rules them all

Modern Python packaging is standardized around `pyproject.toml`:

```toml
[project]
name = "fincli"
version = "1.2.0"
requires-python = ">=3.11"
dependencies = ["click>=8.1"]

[project.scripts]
fincli = "fincli.cli:main"
```

`[project]` is the standardized metadata (PEP 621); `[project.scripts]` creates
the `fincli` command that imports `fincli.cli` and calls `main`. Build
backends (setuptools, hatchling, flit) read this file; you pick one, but the
metadata contract is universal.

## Wheels and sdists

`python -m build` produces two artifacts:

- **wheel** (`.whl`) — the installable format: fast, no build step for the user,
- **sdist** (`.tar.gz`) — the source distribution from which a wheel can be
  rebuilt.

Install from a wheel with `pip install dist/fincli-1.2.0-py3-none-any.whl` —
or publish to an index. Versioning follows your policy; semver (`major.minor.patch`)
is the common contract for *breaking.feature.fix*.

## Lockfiles: reproducible environments

`requirements.txt` with loose ranges says *approximately what*; a lockfile says
*exactly what* — every transitive dependency pinned to a hash-verified version,
so that the environment you tested is the environment your colleague installs.
Tools: `pip-tools`, `uv`, `poetry`. Rule of thumb: libraries declare loose
ranges in `pyproject.toml`; applications lock.

## Entry points beyond scripts

The `[project.scripts]` mechanism is one use of **entry points** — a registry
packages publish that others can query. Plugin systems use the same mechanism:
an application declares an entry-point group (`fincli.plugins`), and any
installed package can register a plugin there. The metaclass/registry patterns
from Module 2 meet the packaging system.

## Reproducible environments

`python -m venv .venv` — one environment per project, never global installs;
activate and `pip install -e .` (editable install: your code changes are live)
while developing. `requires-python` is the contract with your users' machines;
declare it honestly.
""",
    "Đóng gói và entry point",
    "Từ một đống module đến một công cụ có thể cài đặt, có phiên bản, được lockfile ghim, cài bằng một lệnh.",
    """
## pyproject.toml: một tệp cai trị tất cả

Đóng gói Python hiện đại được chuẩn hóa quanh `pyproject.toml`:

```toml
[project]
name = "fincli"
version = "1.2.0"
requires-python = ">=3.11"
dependencies = ["click>=8.1"]

[project.scripts]
fincli = "fincli.cli:main"
```

`[project]` là metadata chuẩn hóa (PEP 621); `[project.scripts]` tạo lệnh
`fincli` import `fincli.cli` và gọi `main`. Build backend (setuptools,
hatchling, flit) đọc tệp này; bạn chọn một, nhưng hợp đồng metadata là phổ quát.

## Wheel và sdist

`python -m build` tạo ra hai artifact:

- **wheel** (`.whl`) — định dạng cài đặt: nhanh, người dùng không phải build,
- **sdist** (`.tar.gz`) — bản phân phối nguồn để có thể dựng lại wheel.

Cài từ wheel bằng `pip install dist/fincli-1.2.0-py3-none-any.whl` — hoặc phát
hành lên một index. Phiên bản theo chính sách của bạn; semver
(`major.minor.patch`) là hợp đồng phổ biến cho *breaking.feature.fix*.

## Lockfile: môi trường tái lập được

`requirements.txt` với các dải lỏng nói *xấp xỉ cái gì*; lockfile nói *chính
xác cái gì* — mọi dependency bắc cầu được ghim vào một phiên bản xác minh bằng
hash, để môi trường bạn đã test chính là môi trường đồng nghiệp cài đặt. Công
cụ: `pip-tools`, `uv`, `poetry`. Nguyên tắc: thư viện khai báo dải lỏng trong
`pyproject.toml`; ứng dụng khóa chặt.

## Entry point ngoài scripts

Cơ chế `[project.scripts]` là một cách dùng **entry point** — một registry mà
các package công bố và người khác truy vấn được. Hệ plugin dùng cùng cơ chế:
một ứng dụng khai báo một nhóm entry point (`fincli.plugins`), và bất kỳ package
đã cài nào cũng có thể đăng ký plugin vào đó. Các pattern metaclass/registry
từ Module 2 gặp gỡ hệ đóng gói.

## Môi trường tái lập được

`python -m venv .venv` — một môi trường cho mỗi dự án, không bao giờ cài toàn
cục; kích hoạt và `pip install -e .` (cài dạng editable: thay đổi code của bạn
có tác dụng ngay) khi phát triển. `requires-python` là hợp đồng với máy của
người dùng; hãy khai báo trung thực.
""",
)

# ── lesson 2 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "systems-programming",
    "Systems Programming: Processes, Signals, and Graceful Death",
    "subprocess without the footguns, filesystem as an API, environment and config, and shutting down without losing work.",
    30,
    """
## subprocess: the list form or nothing

```python
# shell=True: a shell interprets your string — injection returns
subprocess.run(f"convert {filename}.png", shell=True)

# list form: argv passed directly, no shell, no injection
subprocess.run(["convert", f"{filename}.png"], check=True, timeout=30)
```

Always `check=True` (non-zero exit raises) unless you handle the code
yourself; always `timeout=` (a hung child is a hung service); capture output
with `capture_output=True` and decode explicitly. Streams are the contract:
children write to stdout/stderr, and a robust parent reads them *before* they
fill the OS pipe buffer (or uses threads) — a child blocked on a full pipe is
the classic silent deadlock.

## Filesystem as an API

`pathlib.Path` is the modern interface: `Path(base) / name` joins portably,
`.resolve()` canonicalizes, `.is_relative_to(base)` confines (the traversal
defense from the security module). Atomic writes follow one pattern: write to
a temp file in the same directory, `flush`, `fsync`, then `os.replace(tmp,
final)` — readers see either the old file or the new one, never a torn write.

## Environment and configuration

Configuration comes from the environment in production (the secrets rule from
the security module). Parse once at startup with the fail-closed discipline,
then pass values explicitly — a module that reaches for `os.environ` deep in
its call tree is untestable and unknowable.

## Signals and graceful shutdown

The OS talks to processes via signals: `SIGTERM` (please stop), `SIGINT`
(Ctrl-C), `SIGKILL` (no negotiation, cannot be caught). The graceful-shutdown
pattern:

1. install handlers for `SIGTERM`/`SIGINT` that set a shutdown flag,
2. stop accepting new work,
3. finish (or durably re-queue) in-flight work — idempotent jobs make this safe,
4. release resources, then exit.

Kill-9 mid-job is only survivable because of the at-least-once + idempotency
design from the distributed module: the job re-delivers, the effect stays
exactly-once.

## Safe execution for automation

An "automation agent" that runs on real machines needs the humility list:
validate every external input (even file names), never shell out with user
data, dry-run modes for destructive operations, and audit logs of every action
taken. The tool you wrote is the tool that will run when you are on vacation.
""",
    "Lập trình hệ thống: tiến trình, signal, và cái chết nhã nhặn",
    "subprocess không cần cạm bẫy, filesystem như một API, môi trường và cấu hình, và tắt máy mà không mất dữ liệu.",
    """
## subprocess: dạng list hoặc không có gì

```python
# shell=True: một shell diễn giải chuỗi của bạn — injection quay lại
subprocess.run(f"convert {filename}.png", shell=True)

# dạng list: argv truyền thẳng, không shell, không injection
subprocess.run(["convert", f"{filename}.png"], check=True, timeout=30)
```

Luôn dùng `check=True` (exit code khác 0 sẽ raise) trừ khi bạn tự xử lý mã;
luôn dùng `timeout=` (một con treo là một dịch vụ treo); bắt output bằng
`capture_output=True` và decode tường minh. Stream là hợp đồng: con ghi vào
stdout/stderr, và một cha bền bỉ phải đọc chúng *trước khi* lấp đầy buffer pipe
của OS (hoặc dùng thread) — con bị chặn trên pipe đầy là deadlock im lặng kinh
điển.

## Filesystem như một API

`pathlib.Path` là giao diện hiện đại: `Path(base) / name` nối đường dẫn khả
chuyển, `.resolve()` chuẩn hóa, `.is_relative_to(base)` giới hạn (phòng thủ
traversal từ module bảo mật). Ghi nguyên tử theo một pattern: ghi vào tệp tạm
trong cùng thư mục, `flush`, `fsync`, rồi `os.replace(tmp, final)` — người đọc
thấy tệp cũ hoặc tệp mới, không bao giờ thấy bản ghi rách.

## Môi trường và cấu hình

Cấu hình đến từ môi trường trong production (quy tắc secrets từ module bảo
mật). Parse một lần lúc khởi động với kỷ luật fail-closed, rồi truyền giá trị
tường minh — một module mổ xẻ `os.environ` sâu trong cây gọi là không thể test
và không thể đoán.

## Signal và tắt máy nhã nhặn

OS nói chuyện với tiến trình qua signal: `SIGTERM` (làm ơn dừng), `SIGINT`
(Ctrl-C), `SIGKILL` (không đàm phán, không thể bắt). Pattern tắt máy nhã nhặn:

1. cài handler cho `SIGTERM`/`SIGINT` đặt một cờ shutdown,
2. ngừng nhận công việc mới,
3. hoàn tất (hoặc trả về queue một cách bền vững) công việc đang chạy — job
   idempotent khiến điều này an toàn,
4. giải phóng tài nguyên, rồi thoát.

Kill-9 giữa chừng job chỉ sống được nhờ thiết kế at-least-once + idempotency
từ module distributed: job được chuyển giao lại, hiệu ứng vẫn exactly-once.

## Thực thi an toàn cho automation

Một "automation agent" chạy trên máy thật cần danh sách khiêm tốn: validate
mọi đầu vào bên ngoài (kể cả tên tệp), không bao giờ gọi shell với dữ liệu
người dùng, chế độ dry-run cho các thao tác phá hủy, và audit log mọi hành
động. Công cụ bạn viết là công cụ sẽ chạy khi bạn đang đi nghỉ.
""",
)

# ── lesson 3 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "observability",
    "Observability: Logs, Metrics, Traces",
    "When production misbehaves at 3 a.m., your future self debugs through what you recorded today.",
    28,
    """
## The three pillars, honestly weighted

- **Logs** — discrete events with context. The workhorse.
- **Metrics** — numbers over time (counters, gauges, histograms). The alarms.
- **Traces** — one request's journey across components, with a shared
  **correlation ID**. The multi-hop detective.

Structured logging beats string formatting: `log.info("order.created",
order_id=..., total=...)` emits JSON that machines can query. The rules that
matter:

- levels are a *policy*: DEBUG for developers, INFO for business events, WARNING
  for auto-healed oddities, ERROR for things a human must see,
- **never log secrets or personal data** — passwords, tokens, full card numbers;
  log identifiers, not contents,
- one event per *occurrence*, with fields — not one line per variable.

## Metrics that earn their keep

Four metric types cover nearly everything: counter (monotone — requests,
errors), gauge (point-in-time — queue depth, active connections), histogram
(distributions — latency), and rate (counter per time). Alert on symptoms
users feel (error rate, latency SLO burn) — not on causes (CPU is high) — and
every alert must be actionable, or it trains people to ignore alerts.

## Tracing: the correlation ID

One ID per request, propagated through every hop and attached to every log
line. When a user says "it failed", the ID reconstructs the whole journey: API
→ queue → worker → database, with timings at each hop. OpenTelemetry
standardizes the instrumentation; the concept matters more than the vendor.

## Health checks and graceful degradation, revisited

`/readyz` reports *dependency* state (the readiness probe you built in the APIs
module); metrics on dependency failures feed circuit breakers (distributed
module); traces carry the correlation ID that turns "errors spiked" into
"checkout latency rose after the payment provider's p99 crossed 2s at 02:14".
Each mechanism is simple; the compound system is how incidents get diagnosed
before coffee.

## SLOs: the honesty contract

Pick a small set of user-facing objectives ("99.9% of checkout requests succeed
in under 500ms"), measure them with histograms, and let the *burn rate* of the
error budget drive urgency. Inside budget: ship features. Burning fast: stop
and stabilize. The SLO replaces vibes with arithmetic.
""",
    "Quan sát được: Log, metric, trace",
    "Khi production hỏng vào 3 giờ sáng, con người bạn tương lai debug qua những gì bạn ghi lại hôm nay.",
    """
## Ba trụ cột, nói thẳng trọng lượng

- **Log** — các sự kiện rời rạc với ngữ cảnh. Con ngựa thồ.
- **Metric** — con số theo thời gian (counter, gauge, histogram). Chuông báo.
- **Trace** — hành trình của một request qua các thành phần, với một
  **correlation ID** chung. Thám tử đa chặng.

Structured logging đánh bại định dạng chuỗi: `log.info("order.created",
order_id=..., total=...)` phát JSON mà máy truy vấn được. Các quy tắc đáng kể:

- mức log là một *chính sách*: DEBUG cho lập trình viên, INFO cho sự kiện
  nghiệp vụ, WARNING cho điều bất thường tự hồi phục, ERROR cho thứ con người
  phải nhìn thấy,
- **không bao giờ log secret hay dữ liệu cá nhân** — mật khẩu, token, số thẻ
  đầy đủ; log định danh, không log nội dung,
- một sự kiện cho mỗi lần *xuất hiện*, kèm các field — không phải một dòng cho
  mỗi biến.

## Metric đáng tiền

Bốn loại metric bao gần hết: counter (đơn điệu tăng — request, lỗi), gauge
(tại một thời điểm — độ sâu queue, kết nối đang hoạt động), histogram (phân
phối — độ trễ), và rate (counter trên thời gian). Cảnh báo trên *triệu chứng*
người dùng cảm nhận (tỷ lệ lỗi, đốt SLO độ trễ) — không phải trên *nguyên nhân*
(CPU cao) — và mỗi cảnh báo phải hành động được, nếu không nó dạy con người
phớt lờ cảnh báo.

## Tracing: correlation ID

Một ID cho mỗi request, được truyền qua mọi chặng và gắn vào mọi dòng log. Khi
người dùng nói "nó bị lỗi", ID tái dựng toàn bộ hành trình: API → queue →
worker → database, với thời gian tại từng chặng. OpenTelemetry chuẩn hóa phần
instrumentation; khái niệm quan trọng hơn nhà cung cấp.

## Health check và graceful degradation, nhìn lại

`/readyz` báo *trạng thái dependency* (cái readiness probe bạn đã xây trong
module API); metric về lỗi dependency nuôi circuit breaker (module distributed);
trace mang correlation ID biến "lỗi tăng vọt" thành "độ trễ checkout tăng sau
khi p99 của nhà cung cấp thanh toán vượt 2s lúc 02:14". Mỗi cơ chế đều đơn giản;
hệ thống ghép là cách sự cố được chẩn đoán trước khi uống cà phê.

## SLO: hợp đồng trung thực

Chọn một tập nhỏ mục tiêu hướng người dùng ("99.9% request checkout thành công
dưới 500ms"), đo bằng histogram, và để *tốc độ đốt* ngân sách lỗi quyết định
mức khẩn cấp. Còn trong ngân sách: ship tính năng. Đốt nhanh: dừng lại và ổn
định. SLO thay thế cảm tính bằng số học.
""",
)

# ── practice 1: packaging ────────────────────────────────────────────────────
VERSION_REF = (
    "import re as _re\n"
    "\n"
    "_SEMVER = _re.compile(r'^(\\d+)\\.(\\d+)\\.(\\d+)$')\n"
    "\n"
    "\n"
    "def parse_version(v):\n"
    "    m = _SEMVER.match(v)\n"
    "    if not m:\n"
    "        raise ValueError(f'invalid semver: {v}')\n"
    "    return tuple(int(p) for p in m.groups())\n"
    "\n"
    "\n"
    "def bump(version, part):\n"
    "    major, minor, patch = parse_version(version)\n"
    "    if part == 'major':\n"
    "        return f'{major + 1}.0.0'\n"
    "    if part == 'minor':\n"
    "        return f'{major}.{minor + 1}.0'\n"
    "    if part == 'patch':\n"
    "        return f'{major}.{minor}.{patch + 1}'\n"
    "    raise ValueError(f'unknown part: {part}')\n"
    "\n"
    "\n"
    "def compare(a, b):\n"
    "    A, B = parse_version(a), parse_version(b)\n"
    "    return (A > B) - (A < B)\n"
)
VERSION_WRONG = (
    "import re as _re\n"
    "\n"
    "_SEMVER = _re.compile(r'^(\\d+)\\.(\\d+)\\.(\\d+)$')\n"
    "\n"
    "\n"
    "def parse_version(v):\n"
    "    m = _SEMVER.match(v)\n"
    "    if not m:\n"
    "        raise ValueError(f'invalid semver: {v}')\n"
    "    return tuple(int(p) for p in m.groups())\n"
    "\n"
    "\n"
    "def bump(version, part):\n"
    "    major, minor, patch = parse_version(version)\n"
    "    if part == 'major':\n"
    "        return f'{major + 1}.{minor}.{patch}'  # WRONG: keeps old minors\n"
    "    if part == 'minor':\n"
    "        return f'{major}.{minor + 1}.{patch}'  # WRONG: keeps old patch\n"
    "    if part == 'patch':\n"
    "        return f'{major}.{minor}.{patch + 1}'\n"
    "    raise ValueError(f'unknown part: {part}')\n"
    "\n"
    "\n"
    "def compare(a, b):\n"
    "    A, B = parse_version(a), parse_version(b)\n"
    "    return (A > B) - (A < B)\n"
)

ENTRYPOINTS_REF = (
    "def collect_plugins(registry, group):\n"
    "    '''registry: dict group -> list of (package, plugin_name, factory).\n"
    "    Returns {plugin_name: factory} for the group; a duplicate plugin name\n"
    "    raises ValueError('duplicate plugin: <name>'). Factories are not called.'''\n"
    "    plugins = {}\n"
    "    for package, name, factory in registry.get(group, []):\n"
    "        if name in plugins:\n"
    "            raise ValueError(f'duplicate plugin: {name}')\n"
    "        plugins[name] = factory\n"
    "    return plugins\n"
)
ENTRYPOINTS_WRONG = (
    "def collect_plugins(registry, group):\n"
    "    plugins = {}\n"
    "    for package, name, factory in registry.get(group, []):\n"
    "        plugins[name] = factory  # WRONG: last-wins silently shadows plugins\n"
    "    return plugins\n"
)

write_practice(
    MOD, "pa-p14-packaging-practice",
    "Packaging Drills",
    "Semver as code — parse, bump, compare — and the plugin registry that refuses shadowing.",
    "Bài tập đóng gói",
    "Semver dưới dạng code — parse, bump, so sánh — và registry plugin từ chối bị che khuất.",
    "packaging-and-entry-points", 24, "advanced",
    [
        challenge(
            "pa-pkg-semver",
            "Versions are data",
            "Implement `parse_version(v)`, `bump(version, part)`, `compare(a, b)`:\n\n- versions are strict `MAJOR.MINOR.PATCH` digit strings; anything else raises `ValueError('invalid semver: <v>')`\n- `bump` returns the next version as a string; bumping a part resets everything below it (`bump('1.2.3', 'minor') == '1.3.0'`); unknown part raises `ValueError('unknown part: <p>')`\n- `compare` returns -1/0/1 with numeric (not lexicographic) ordering — `'1.10.0' > '1.9.0'`\n\nThis is the versioning contract of the packaging lesson as an executable spec.",
            "import re\n\n\n# TODO: parse_version + bump + compare",
            [
                ("bump resets lower parts; compare is numeric",
                 "assert bump('1.2.3', 'patch') == '1.2.4'\nassert bump('1.2.3', 'minor') == '1.3.0'\nassert bump('1.2.3', 'major') == '2.0.0'\nassert compare('1.10.0', '1.9.0') == 1\nassert compare('2.0.0', '2.0.0') == 0\nfor bad in ['1.2', 'v1.2.3', '1.2.3.4', '01.2.3']:\n    try:\n        parse_version(bad)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(bad)\nprint('ok')",
                 "Numeric compare and strict parsing — the two things hand-rolled versions get wrong."),
            ],
            level="independent",
        ),
        challenge(
            "pa-pkg-plugin-registry",
            "The plugin registry",
            "Implement `collect_plugins(registry, group)` — registry maps group names to lists of `(package, plugin_name, factory)` tuples:\n\n- returns `{plugin_name: factory}` for that group\n- a duplicate plugin name raises `ValueError('duplicate plugin: <name>')` — silent shadowing is how plugin bugs hide\n- factories are returned, never called\n\nThis is the entry-points mechanism (and the Module-2 registry) in miniature.",
            "# TODO: collect_plugins",
            [
                ("collects, and refuses duplicates",
                 "reg = {'fincli.plugins': [('pkg_a', 'csv', object), ('pkg_b', 'json', object)]}\npl = collect_plugins(reg, 'fincli.plugins')\nassert set(pl) == {'csv', 'json'}\nreg2 = {'g': [('a', 'dup', object), ('b', 'dup', object)]}\ntry:\n    collect_plugins(reg2, 'g')\nexcept ValueError as e:\n    assert 'duplicate plugin: dup' in str(e)\nelse:\n    raise AssertionError('duplicates must raise')\nassert collect_plugins(reg, 'missing-group') == {}\nprint('ok')",
                 "Order-independent discovery; first duplicate is loud."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-pkg-semver": vi_challenge(
            "Phiên bản là dữ liệu",
            "Cài `parse_version(v)`, `bump(version, part)`, `compare(a, b)`:\n\n- phiên bản là chuỗi chữ số nghiêm ngặt `MAJOR.MINOR.PATCH`; cái khác raise `ValueError('invalid semver: <v>')`\n- `bump` trả phiên bản kế tiếp dạng chuỗi; bump một phần sẽ reset mọi thứ bên dưới nó (`bump('1.2.3', 'minor') == '1.3.0'`); part lạ raise `ValueError('unknown part: <p>')`\n- `compare` trả -1/0/1 với thứ tự số học (không phải so chuỗi) — `'1.10.0' > '1.9.0'`\n\nĐây là hợp đồng phiên bản của bài đóng gói dưới dạng đặc tả thực thi được.",
            [("Bump reset phần dưới; so sánh theo số", "So sánh số học và parse nghiêm ngặt — hai điều bản cài tay hay sai.")],
        ),
        "pa-pkg-plugin-registry": vi_challenge(
            "Registry plugin",
            "Cài `collect_plugins(registry, group)` — registry ánh xạ tên nhóm tới list tuple `(package, plugin_name, factory)`:\n\n- trả `{plugin_name: factory}` cho nhóm đó\n- tên plugin trùng raise `ValueError('duplicate plugin: <name>')` — che khuất im lặng là cách bug plugin trốn tránh\n- factory được trả về, không bao giờ được gọi\n\nĐây là cơ chế entry-points (và registry từ Module 2) ở dạng thu nhỏ.",
            [("Thu thập, và từ chối trùng lặp", "Khám phá độc lập thứ tự; bản trùng đầu tiên phải ầm ĩ.")],
        ),
    },
    solutions=[("pa-pkg-semver", VERSION_REF, VERSION_WRONG),
               ("pa-pkg-plugin-registry", ENTRYPOINTS_REF, ENTRYPOINTS_WRONG)],
)

# ── practice 2: systems ──────────────────────────────────────────────────────
ATOMIC_REF = (
    "import os as _os\n"
    "\n"
    "\n"
    "class AtomicStore:\n"
    "    '''File-backed store with atomic replace semantics (simulated in memory\n"
    "    but ordered exactly like the real pattern: write tmp -> flush -> replace).'''\n"
    "\n"
    "    def __init__(self):\n"
    "        self._files = {}\n"
    "        self._log = []\n"
    "\n"
    "    def write(self, path, data):\n"
    "        tmp = path + '.tmp'\n"
    "        self._log.append(('write', tmp))\n"
    "        self._log.append(('flush', tmp))\n"
    "        self._log.append(('replace', tmp, path))\n"
    "        self._files[path] = data\n"
    "        self._files.pop(tmp, None)\n"
    "\n"
    "    def read(self, path):\n"
    "        if path not in self._files:\n"
    "            raise FileNotFoundError(path)\n"
    "        return self._files[path]\n"
    "\n"
    "    @property\n"
    "    def log(self):\n"
    "        return list(self._log)\n"
    "\n"
    "\n"
    "def graceful_shutdown(worker, sigterm=True, sigint=False):\n"
    "    '''Simulate signal handling. worker has: running (bool), in_flight (int),\n"
    "    drained (bool), requeued (list). SIGTERM/SIGINT -> stop accepting, finish\n"
    "    or requeue in-flight work, mark drained. Returns the worker.'''\n"
    "    if not (sigterm or sigint):\n"
    "        return worker  # SIGKILL: nothing graceful happens\n"
    "    worker.running = False          # stop accepting new work\n"
    "    if worker.in_flight:\n"
    "        worker.requeued.append(worker.in_flight)\n"
    "        worker.in_flight = 0\n"
    "    worker.drained = True\n"
    "    return worker\n"
)
ATOMIC_WRONG = (
    "import os as _os\n"
    "\n"
    "\n"
    "class AtomicStore:\n"
    "    def __init__(self):\n"
    "        self._files = {}\n"
    "        self._log = []\n"
    "\n"
    "    def write(self, path, data):\n"
    "        # WRONG: writes in place — a crash mid-write leaves a torn file\n"
    "        self._log.append(('write', path))\n"
    "        self._files[path] = data\n"
    "\n"
    "    def read(self, path):\n"
    "        if path not in self._files:\n"
    "            raise FileNotFoundError(path)\n"
    "        return self._files[path]\n"
    "\n"
    "    @property\n"
    "    def log(self):\n"
    "        return list(self._log)\n"
    "\n"
    "\n"
    "def graceful_shutdown(worker, sigterm=True, sigint=False):\n"
    "    if not (sigterm or sigint):\n"
    "        return worker\n"
    "    worker.running = False\n"
    "    worker.in_flight = 0  # WRONG: work vanishes instead of being requeued\n"
    "    worker.drained = True\n"
    "    return worker\n"
)

write_practice(
    MOD, "pa-p14-systems-practice",
    "Systems Drills",
    "Atomic write ordering, and the graceful-shutdown state machine that requeues instead of dropping.",
    "Bài tập hệ thống",
    "Thứ tự ghi nguyên tử, và máy trạng thái tắt máy nhã nhặn trả việc về queue thay vì làm rơi.",
    "systems-programming", 24, "advanced",
    [
        challenge(
            "pa-p14-atomic-write",
            "Write like the OS is watching",
            "Implement `AtomicStore` — a file store whose `write(path, data)` follows the real atomic-replace pattern, recorded in `log`:\n\n- append `('write', path + '.tmp')`, then `('flush', path + '.tmp')`, then `('replace', path + '.tmp', path)`\n- after the log entries, the data is readable at `path`, and no `.tmp` file remains\n- `read(path)` raises `FileNotFoundError` for unknown paths\n- expose `log` as a property\n\nThe log IS the test: a torn write is impossible when the sequence is write-tmp, flush, replace.",
            "class AtomicStore:\n    def __init__(self):\n        ...\n\n    def write(self, path, data):\n        ...\n\n    def read(self, path):\n        ...\n\n    @property\n    def log(self):\n        ...",
            [
                ("the sequence is exactly write, flush, replace",
                 "s = AtomicStore()\ns.write('state.json', '{\"a\": 1}')\nassert s.read('state.json') == '{\"a\": 1}'\nassert s.log == [('write', 'state.json.tmp'), ('flush', 'state.json.tmp'), ('replace', 'state.json.tmp', 'state.json')]\nprint('ok')",
                 "Order is the correctness argument."),
            ],
            level="independent",
        ),
        challenge(
            "pa-p14-graceful-shutdown",
            "Die gracefully, lose nothing",
            "Implement `graceful_shutdown(worker, sigterm=True, sigint=False)` — the worker has `running` (bool), `in_flight` (int count), `drained` (bool), `requeued` (list):\n\n- `sigterm=False, sigint=False` simulates SIGKILL: return the worker untouched (nothing graceful happens)\n- otherwise: `running = False` (stop accepting), any in-flight work is appended to `requeued` (durably re-queueable, thanks to idempotent jobs) and `in_flight = 0`, then `drained = True`\n- return the worker\n\nThe invariant: after a graceful shutdown, `in_flight == 0` AND every unit of work is accounted for in `requeued`.",
            "def graceful_shutdown(worker, sigterm=True, sigint=False):\n    ...",
            [
                ("work is requeued, not dropped",
                 "class W:\n    running, in_flight, drained, requeued = True, 3, False, []\nw = graceful_shutdown(W())\nassert w.running is False and w.drained is True\nassert w.in_flight == 0 and w.requeued == [3]\nw2 = graceful_shutdown(W(), sigterm=False, sigint=False)\nassert w2.running is True and w2.in_flight == 3  # SIGKILL: no guarantees\nprint('ok')",
                 "Graceful vs. kill-9 are different worlds; idempotent jobs bridge them."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-p14-atomic-write": vi_challenge(
            "Ghi như thể OS đang nhìn",
            "Cài `AtomicStore` — một kho tệp mà `write(path, data)` theo đúng pattern replace-nguyên-tử thật, được ghi trong `log`:\n\n- thêm `('write', path + '.tmp')`, rồi `('flush', path + '.tmp')`, rồi `('replace', path + '.tmp', path)`\n- sau các entry log, dữ liệu đọc được tại `path`, và không còn tệp `.tmp` nào\n- `read(path)` raise `FileNotFoundError` với đường dẫn lạ\n- phơi `log` như một property\n\nLog chính là bài test: bản ghi rách là bất khả khi trình tự là write-tmp, flush, replace.",
            [("Trình tự chính là lập luận đúng đắn", "write, flush, replace — đúng thứ tự đó.")],
        ),
        "pa-p14-graceful-shutdown": vi_challenge(
            "Chết nhã nhặn, không mất gì",
            "Cài `graceful_shutdown(worker, sigterm=True, sigint=False)` — worker có `running` (bool), `in_flight` (số đếm), `drained` (bool), `requeued` (list):\n\n- `sigterm=False, sigint=False` mô phỏng SIGKILL: trả worker nguyên vẹn (không gì nhã nhặn xảy ra)\n- ngược lại: `running = False` (ngừng nhận), mọi công việc đang chạy được thêm vào `requeued` (có thể trả về queue bền vững, nhờ job idempotent) và `in_flight = 0`, rồi `drained = True`\n- trả worker\n\nBất biến: sau khi tắt nhã nhặn, `in_flight == 0` VÀ mọi đơn vị công việc được ghi nhận trong `requeued`.",
            [("Công việc được trả về queue, không bị làm rơi", "Nhã nhặn và kill-9 là hai thế giới; job idempotent nối chúng.")],
        ),
    },
    solutions=[("pa-p14-atomic-write", ATOMIC_REF, ATOMIC_WRONG)],
)

# ── practice 3: observability ────────────────────────────────────────────────
LOGGER_REF = (
    "import json as _json\n"
    "\n"
    "\n"
    "class StructuredLogger:\n"
    "    '''Structured logger with redaction. Sensitive fields are replaced with\n"
    "    '[REDACTED]' at emit time; the event name and correlation id always ride\n"
    "    along.'''\n"
    "\n"
    "    SENSITIVE = {'password', 'token', 'secret', 'card_number'}\n"
    "\n"
    "    def __init__(self, correlation_id):\n"
    "        self.correlation_id = correlation_id\n"
    "        self.lines = []\n"
    "\n"
    "    def _redact(self, fields):\n"
    "        return {k: ('[REDACTED]' if k in self.SENSITIVE else v) for k, v in fields.items()}\n"
    "\n"
    "    def log(self, level, event, **fields):\n"
    "        line = {'level': level, 'event': event, 'correlation_id': self.correlation_id}\n"
    "        line.update(self._redact(fields))\n"
    "        self.lines.append(_json.dumps(line, sort_keys=True))\n"
    "\n"
    "    def info(self, event, **fields):\n"
    "        self.log('INFO', event, **fields)\n"
    "\n"
    "    def error(self, event, **fields):\n"
    "        self.log('ERROR', event, **fields)\n"
)
LOGGER_WRONG = (
    "import json as _json\n"
    "\n"
    "\n"
    "class StructuredLogger:\n"
    "    SENSITIVE = {'password', 'token', 'secret', 'card_number'}\n"
    "\n"
    "    def __init__(self, correlation_id):\n"
    "        self.correlation_id = correlation_id\n"
    "        self.lines = []\n"
    "\n"
    "    def log(self, level, event, **fields):\n"
    "        # WRONG: no redaction — secrets land in the log file\n"
    "        line = {'level': level, 'event': event, 'correlation_id': self.correlation_id}\n"
    "        line.update(fields)\n"
    "        self.lines.append(_json.dumps(line, sort_keys=True))\n"
    "\n"
    "    def info(self, event, **fields):\n"
    "        self.log('INFO', event, **fields)\n"
    "\n"
    "    def error(self, event, **fields):\n"
    "        self.log('ERROR', event, **fields)\n"
)

SLO_REF = (
    "def error_budget(slo_success_rate, total, failures, window_days=30):\n"
    "    '''Return {'slo': rate, 'actual': rate, 'budget_remaining': fraction 0..1,\n"
    "    'status': 'healthy'|'burning'|'breached'}.\n"
    "    Budget: allowed failures = total * (1 - slo). remaining = 1 - failures/allowed\n"
    "    (0 when exhausted). status: healthy if remaining >= 0.5, burning if > 0,\n"
    "    breached otherwise (including when allowed is 0 and failures > 0).'''\n"
    "    allowed = total * (1 - slo_success_rate)\n"
    "    actual = (total - failures) / total if total else 1.0\n"
    "    if allowed <= 0:\n"
    "        remaining = 0.0 if failures > 0 else 1.0\n"
    "    else:\n"
    "        remaining = max(0.0, 1 - failures / allowed)\n"
    "    if remaining >= 0.5:\n"
    "        status = 'healthy'\n"
    "    elif remaining > 0:\n"
    "        status = 'burning'\n"
    "    else:\n"
    "        status = 'breached'\n"
    "    return {'slo': slo_success_rate, 'actual': actual,\n"
    "            'budget_remaining': remaining, 'status': status}\n"
)
SLO_WRONG = (
    "def error_budget(slo_success_rate, total, failures, window_days=30):\n"
    "    allowed = total * (1 - slo_success_rate)\n"
    "    actual = (total - failures) / total if total else 1.0\n"
    "    # WRONG: budget never goes negative-aware — a breach still reads 'burning'\n"
    "    remaining = max(0.0, 1 - failures / allowed) if allowed else 1.0\n"
    "    if remaining >= 0.5:\n"
    "        status = 'healthy'\n"
    "    else:\n"
    "        status = 'burning'\n"
    "    return {'slo': slo_success_rate, 'actual': actual,\n"
    "            'budget_remaining': remaining, 'status': status}\n"
)

write_practice(
    MOD, "pa-p14-observability-practice",
    "Observability Drills",
    "Structured logs with redaction, and the error-budget arithmetic that turns SLOs into decisions.",
    "Bài tập quan sát",
    "Log có cấu trúc với che giấu dữ liệu, và phép toán ngân sách lỗi biến SLO thành quyết định.",
    "observability", 26, "advanced",
    [
        challenge(
            "pa-p14-structured-log",
            "Logs a machine can query, a lawyer can read",
            "Implement `StructuredLogger(correlation_id)`:\n\n- `log(level, event, **fields)` appends a JSON line (sorted keys) containing `level`, `event`, `correlation_id`, and the fields\n- any field named in `SENSITIVE = {'password', 'token', 'secret', 'card_number'}` is emitted as `'[REDACTED]'` — redaction happens at emit time\n- convenience methods `info(event, **fields)` and `error(event, **fields)` map to levels 'INFO' and 'ERROR'\n- expose the lines as a `lines` list\n\nThe redaction test is the point: a login event carrying a password must never emit the password.",
            "class StructuredLogger:\n    SENSITIVE = {'password', 'token', 'secret', 'card_number'}\n\n    def __init__(self, correlation_id):\n        ...\n\n    def log(self, level, event, **fields):\n        ...\n\n    def info(self, event, **fields):\n        ...\n\n    def error(self, event, **fields):\n        ...",
            [
                ("structured, correlated, and redacted",
                 "import json\nlg = StructuredLogger('req-42')\nlg.info('login.attempt', user='lan', password='hunter2')\nlg.error('login.failed', user='lan', token='abc123')\nline = json.loads(lg.lines[0])\nassert line['event'] == 'login.attempt' and line['correlation_id'] == 'req-42'\nassert line['password'] == '[REDACTED]' and line['user'] == 'lan'\nline2 = json.loads(lg.lines[1])\nassert line2['level'] == 'ERROR' and line2['token'] == '[REDACTED]'\nprint('ok')",
                 "Redaction is by field name, applied at emit, never stored raw."),
            ],
            level="guided",
        ),
        challenge(
            "pa-p14-error-budget",
            "The error budget",
            "Implement `error_budget(slo_success_rate, total, failures, window_days=30)`:\n\n- allowed failures = `total * (1 - slo)`; budget remaining = `1 - failures/allowed`, floored at 0 (1.0 when allowed is 0 and there are no failures)\n- returns `{'slo', 'actual' (measured success rate), 'budget_remaining', 'status'}`\n- status: `'healthy'` when remaining >= 0.5, `'burning'` when 0 < remaining < 0.5, `'breached'` at 0 (a real breach must NOT read as merely burning)\n\nThis function is the SLO decision: healthy → ship features; burning → stabilize.",
            "# TODO: error_budget",
            [
                ("healthy, burning, breached",
                 "r = error_budget(0.99, 1000, 3)\nassert r['status'] == 'healthy' and abs(r['budget_remaining'] - 0.7) < 1e-9\nr = error_budget(0.99, 1000, 6)\nassert r['status'] == 'burning' and r['budget_remaining'] > 0\nr = error_budget(0.99, 1000, 20)\nassert r['status'] == 'breached' and r['budget_remaining'] == 0.0\nprint('ok')",
                 "20 failures exceeds the 10-failure budget: breached, not burning."),
            ],
            level="independent",
        ),
    ],
    {
        "pa-p14-structured-log": vi_challenge(
            "Log mà máy truy vấn được, luật sư đọc được",
            "Cài `StructuredLogger(correlation_id)`:\n\n- `log(level, event, **fields)` thêm một dòng JSON (khóa đã sắp) chứa `level`, `event`, `correlation_id`, và các field\n- field có tên trong `SENSITIVE = {'password', 'token', 'secret', 'card_number'}` được phát thành `'[REDACTED]'` — che giấu xảy ra lúc phát\n- hai method tiện lợi `info(event, **fields)` và `error(event, **fields)` ánh xạ tới mức 'INFO' và 'ERROR'\n- phơi các dòng qua list `lines`\n\nBài test che giấu mới là điểm chính: một sự kiện đăng nhập mang mật khẩu không bao giờ được phát mật khẩu ra.",
            [("Có cấu trúc, có correlation, và đã che giấu", "Redaction theo tên field, áp dụng lúc phát, không bao giờ lưu thô.")],
        ),
        "pa-p14-error-budget": vi_challenge(
            "Ngân sách lỗi",
            "Cài `error_budget(slo_success_rate, total, failures, window_days=30)`:\n\n- lỗi cho phép = `total * (1 - slo)`; ngân sách còn lại = `1 - failures/allowed`, sàn là 0 (1.0 khi allowed bằng 0 và không có lỗi)\n- trả `{'slo', 'actual' (tỷ lệ thành công đo được), 'budget_remaining', 'status'}`\n- status: `'healthy'` khi còn >= 0.5, `'burning'` khi 0 < còn < 0.5, `'breached'` khi bằng 0 (một lần vi phạm thật KHÔNG được đọc là chỉ đang burning)\n\nHàm này là quyết định SLO: healthy → ship tính năng; burning → ổn định.",
            [("Healthy, burning, breached", "20 lỗi vượt ngân sách 10 lỗi: breached, không phải burning.")],
        ),
    },
    solutions=[("pa-p14-structured-log", LOGGER_REF, LOGGER_WRONG),
               ("pa-p14-error-budget", SLO_REF, SLO_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
write_checkpoint(
    MOD, "pa-checkpoint-production",
    "Checkpoint: Production Tooling",
    "Prove you can ship a trustworthy tool: honest versioning, a plugin surface, and an incident you can debug from the logs.",
    25,
    """
**The exam question:** an incident report says "checkout failing since 02:14,
no idea why." What artifacts must exist for you to reconstruct the request —
and what must NOT be in them?

The checkpoint combines this module's skills: version the release honestly,
register its plugins safely, and produce log lines that are structured,
correlated, and redacted — the exact artifacts a 3 a.m. debugger needs.
""",
    "Checkpoint: Công cụ production",
    "Chứng minh bạn ship được một công cụ đáng tin: phiên bản trung thực, bề mặt plugin an toàn, và một sự cố có thể debug từ log.",
    """
**Câu hỏi thi:** một báo cáo sự cố nói "checkout hỏng từ 02:14, không hiểu vì
sao." Những artifact nào phải tồn tại để bạn tái dựng request — và điều gì
KHÔNG được nằm trong đó?

Checkpoint kết hợp kỹ năng của module này: đánh phiên bản release trung thực,
đăng ký plugin an toàn, và tạo ra các dòng log có cấu trúc, có correlation, và
đã che giấu — đúng những artifact mà người debug 3 giờ sáng cần.
""",
    challenge(
        "pa-p14-release-toolkit",
        "The release toolkit",
        "Implement three small functions that ship a release:\n\n- `next_release(version, changes)` — `changes` is a list containing any of 'breaking', 'feature', 'fix': bump major for breaking, else minor for feature, else patch; return the new version string (reuse semver rules: strict MAJOR.MINOR.PATCH, lower parts reset)\n- `safe_registry(entries)` — entries are `(group, name, factory)`; return `{group: {name: factory}}`, raising `ValueError('duplicate plugin: <name>')` on any duplicate name within a group\n- `incident_log(correlation_id, events)` — events are `(level, event, fields)` dicts/tuples with possible 'password'/'token' fields; return the list of JSON lines (sorted keys) with `correlation_id` added and sensitive fields replaced by '[REDACTED]'\n\nThe invariants: breaking > feature > fix precedence; no silent plugin shadowing; no secrets in logs.",
        "# TODO: next_release + safe_registry + incident_log",
        [
            ("precedence, registry, redaction",
             "assert next_release('1.2.3', ['fix']) == '1.2.4'\nassert next_release('1.2.3', ['feature', 'fix']) == '1.3.0'\nassert next_release('1.2.3', ['breaking', 'feature']) == '2.0.0'\nreg = safe_registry([('plugins', 'csv', object), ('plugins', 'json', object)])\nassert set(reg['plugins']) == {'csv', 'json'}\nimport json\nlines = incident_log('req-7', [('ERROR', 'payment.failed', {'order': 'o1', 'token': 'tok9'})])\nline = json.loads(lines[0])\nassert line['token'] == '[REDACTED]' and line['correlation_id'] == 'req-7'\nprint('ok')",
             "Three contracts, one release: version truth, plugin safety, log hygiene."),
        ],
        level="build",
    ),
    vi_challenge(
        "Bộ công cụ release",
        "Cài ba hàm nhỏ để ship một bản release:\n\n- `next_release(version, changes)` — `changes` là list chứa bất kỳ 'breaking', 'feature', 'fix' nào: bump major cho breaking, không thì minor cho feature, không thì patch; trả chuỗi phiên bản mới (tái dùng quy tắc semver: MAJOR.MINOR.PATCH nghiêm ngặt, các phần dưới reset)\n- `safe_registry(entries)` — entries là các tuple `(group, name, factory)`; trả `{group: {name: factory}}`, raise `ValueError('duplicate plugin: <name>')` khi có tên trùng trong cùng một nhóm\n- `incident_log(correlation_id, events)` — events là các `(level, event, fields)` với field có thể là 'password'/'token'; trả list các dòng JSON (khóa đã sắp) với `correlation_id` được thêm và field nhạy cảm thay bằng '[REDACTED]'\n\nCác bất biến: breaking > feature > fix; không che khuất plugin im lặng; không có secret trong log.",
            [("Ưu tiên, registry, che giấu", "Ba hợp đồng, một bản release: sự thật phiên bản, an toàn plugin, vệ sinh log.")],
    ),
    solution=(
        "import json as _json\n"
        "import re as _re\n"
        "\n"
        "_SEMVER = _re.compile(r'^(\\d+)\\.(\\d+)\\.(\\d+)$')\n"
        "\n"
        "\n"
        "def next_release(version, changes):\n"
        "    m = _SEMVER.match(version)\n"
        "    if not m:\n"
        "        raise ValueError(f'invalid semver: {version}')\n"
        "    major, minor, patch = (int(p) for p in m.groups())\n"
        "    s = set(changes)\n"
        "    if 'breaking' in s:\n"
        "        return f'{major + 1}.0.0'\n"
        "    if 'feature' in s:\n"
        "        return f'{major}.{minor + 1}.0'\n"
        "    return f'{major}.{minor}.{patch + 1}'\n"
        "\n"
        "\n"
        "def safe_registry(entries):\n"
        "    reg = {}\n"
        "    for group, name, factory in entries:\n"
        "        group_map = reg.setdefault(group, {})\n"
        "        if name in group_map:\n"
        "            raise ValueError(f'duplicate plugin: {name}')\n"
        "        group_map[name] = factory\n"
        "    return reg\n"
        "\n"
        "\n"
        "_SENSITIVE = {'password', 'token', 'secret', 'card_number'}\n"
        "\n"
        "\n"
        "def incident_log(correlation_id, events):\n"
        "    lines = []\n"
        "    for level, event, fields in events:\n"
        "        line = {'level': level, 'event': event, 'correlation_id': correlation_id}\n"
        "        for k, v in fields.items():\n"
        "            line[k] = '[REDACTED]' if k in _SENSITIVE else v\n"
        "        lines.append(_json.dumps(line, sort_keys=True))\n"
        "    return lines\n"
    ),
    wrong=(
        "import json as _json\n"
        "import re as _re\n"
        "\n"
        "_SEMVER = _re.compile(r'^(\\d+)\\.(\\d+)\\.(\\d+)$')\n"
        "\n"
        "\n"
        "def next_release(version, changes):\n"
        "    m = _SEMVER.match(version)\n"
        "    if not m:\n"
        "        raise ValueError(f'invalid semver: {version}')\n"
        "    major, minor, patch = (int(p) for p in m.groups())\n"
        "    # WRONG: ignores precedence — any change just bumps the patch\n"
        "    return f'{major}.{minor}.{patch + 1}'\n"
        "\n"
        "\n"
        "def safe_registry(entries):\n"
        "    reg = {}\n"
        "    for group, name, factory in entries:\n"
        "        reg.setdefault(group, {})[name] = factory  # WRONG: silent shadowing\n"
        "    return reg\n"
        "\n"
        "\n"
        "def incident_log(correlation_id, events):\n"
        "    lines = []\n"
        "    for level, event, fields in events:\n"
        "        line = {'level': level, 'event': event, 'correlation_id': correlation_id}\n"
        "        line.update(fields)  # WRONG: secrets land in the incident log\n"
        "        lines.append(_json.dumps(line, sort_keys=True))\n"
        "    return lines\n"
    ),
)

print("module 14 complete")
