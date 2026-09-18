#!/usr/bin/env python3
"""Python Intermediate — module 5 (robust-errors)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

M5 = "robust-errors"
L5A = "exception-design"
L5B = "exception-chaining-boundaries"
L5C = "logging"
L5D = "checkpoint-resilience"

write_module(
    M5,
    "Robust Errors and Logging",
    "Design exception hierarchies, chain causes at boundaries, and log like an operator.",
    "Xử lý lỗi bền vững và Logging",
    "Thiết kế hệ thống exception, nối nguyên nhân tại ranh giới, và log như một kỹ sư vận hành.",
    [L5A, L5B, L5C, L5D],
    ["m5-hierarchy-practice", "m5-chaining-practice", "m5-logging-practice"],
)

write_lesson(
    M5, L5A,
    "Designing an Exception Hierarchy",
    "Custom exceptions callers can catch precisely — and the rule of narrow except.",
    14,
    '''
Beginner code catches `Exception` and hopes. Intermediate code defines a
**hierarchy** so callers choose their precision:

```python
class AppError(Exception):
    """Base for every error this application raises."""


class ValidationError(AppError):
    """Input rejected before touching storage."""

class StorageError(AppError):
    """Persistence layer failed."""

try:
    save(record)
except ValidationError:
    ...   # tell the user, retry is pointless
except StorageError:
    ...   # back off, retry may help
except AppError:
    ...   # our family: log and surface
```

Order matters: Python picks the **first matching** except, so specific
classes come before their base. Catching the base `AppError` is a deliberate
safety net — never a reflex.

## Raise specific, message-rich

```python
def set_quantity(q):
    if q <= 0:
        raise ValidationError(f"quantity must be positive, got {q}")
```

The exception message is documentation at the moment of failure. Include the
offending value; a bare `raise ValueError()` wastes everyone's next hour.

## What NOT to catch

Don't catch `KeyboardInterrupt`/`SystemExit` (they're not `Exception`
subclasses for exactly this reason), and don't catch what you can't handle —
an unhandled exception with a good traceback beats a silently swallowed one.
Bare `except:` is a bug in waiting.
    ''',
    "Thiết kế hệ thống Exception",
    "Exception tùy chỉnh giúp caller bắt chính xác — và quy tắc except hẹp.",
    '''
Code người mới bắt `Exception` rồi cầu may. Code trung cấp định nghĩa một
**hệ phân cấp** để caller chọn độ chính xác khi bắt:

```python
class AppError(Exception):
    """Lỗi gốc cho mọi lỗi ứng dụng này raise."""

class ValidationError(AppError):
    """Input bị từ chối trước khi chạm tới bộ lưu trữ."""

class StorageError(AppError):
    """Tầng lưu trữ gặp sự cố."""

try:
    save(record)
except ValidationError:
    ...   # báo người dùng, thử lại vô ích
except StorageError:
    ...   # lùi lại, thử lại có thể giúp
except AppError:
    ...   # họ lỗi của mình: log và báo lên
```

Thứ tự quan trọng: Python chọn except **khớp đầu tiên**, nên lớp cụ thể
phải đứng trước lớp cha. Bắt lớp cha `AppError` là lưới an toàn có chủ đích —
không bao giờ là phản xạ.

## Raise cụ thể, thông điệp giàu thông tin

```python
def set_quantity(q):
    if q <= 0:
        raise ValidationError(f"quantity must be positive, got {q}")
```

Thông điệp exception là tài liệu tại thời điểm lỗi. Hãy kèm giá trị vi phạm;
một `raise ValueError()` trần trụi đánh cắp giờ của mọi người.

## Những gì KHÔNG nên bắt

Đừng bắt `KeyboardInterrupt`/`SystemExit` (chúng cố tình không kế thừa
`Exception`), và đừng bắt những gì mình không xử lý được — một exception
không xử lý với traceback tốt hơn một exception bị nuốt lặng lẽ. `except:`
trống là một con bọ đang chờ nổ.
    ''',
)

write_lesson(
    M5, L5C,
    "Logging That Operators Read",
    "Logger hierarchy, levels, lazy formatting, and why print is not logging.",
    13,
    """
`print` goes to stdout and dies there. The `logging` module routes events to
handlers, formats them uniformly, and carries **levels** for severity:

```python
import logging

log = logging.getLogger(__name__)          # one logger per module

log.debug("cache size: %d", len(cache))    # detail for developers
log.info("imported %d rows", count)        # normal milestones
log.warning("retrying request (%d/3)", attempt)
log.error("failed to save %s", task_id, exc_info=True)   # + traceback
```

Professional habits baked into that snippet:

- **`getLogger(__name__)`** names loggers after modules (`app.storage`), so operators can silence or amplify each area independently.
- **Lazy `%` formatting**, not f-strings — the string is only built if the level is enabled.
- **`exc_info=True`** attaches the traceback to error logs; losing it is how "it worked locally" mysteries are born.

## Levels are a contract

DEBUG → INFO → WARNING → ERROR → CRITICAL. Choose by *who must react*:
developers tune DEBUG out in production; INFO is the operational heartbeat;
WARNING means degraded-but-working; ERROR means an operation failed. Emitting
everything as INFO is how logs become unreadable.

## Configuration belongs to the entry point

Libraries only **get** loggers; the application **configures** them
(`logging.basicConfig(level=..., format=...)`) in one place — usually
`__main__`. That split is why a library can never spam a host app's console.
""",
    "Logging mà người vận hành đọc được",
    "Hệ logger phân cấp, các mức, định dạng lười, và vì sao print không phải logging.",
    """
`print` đổ ra stdout và chết tại đó. Module `logging` định tuyến sự kiện tới
handler, định dạng đồng nhất, và mang theo **mức độ** cho mức nghiêm trọng:

```python
import logging

log = logging.getLogger(__name__)          # một logger cho mỗi module

log.debug("cache size: %d", len(cache))    # chi tiết cho dev
log.info("imported %d rows", count)        # cột mốc bình thường
log.warning("retrying request (%d/3)", attempt)
log.error("failed to save %s", task_id, exc_info=True)   # + traceback
```

Những thói quen chuyên nghiệp nằm ngay trong đoạn trên:

- **`getLogger(__name__)`** đặt tên logger theo module (`app.storage`), để người vận hành có thể tắt hoặc mở từng vùng độc lập.
- **Định dạng `%` lười biếng**, không f-string — chuỗi chỉ được dựng nếu mức đó được bật.
- **`exc_info=True`** gắn traceback vào log lỗi; đánh mất nó là cách các vụ "máy tôi chạy mà" được sinh ra.

## Các mức là một hợp đồng

DEBUG → INFO → WARNING → ERROR → CRITICAL. Chọn theo *ai phải phản ứng*:
dev tắt DEBUG trong production; INFO là nhịp tim vận hành; WARNING nghĩa là
giảm hiệu năng nhưng vẫn chạy; ERROR nghĩa là một thao tác đã thất bại. Gửi
tất cả dưới dạng INFO là cách làm log trở nên không thể đọc.

## Cấu hình thuộc về entry point

Thư viện chỉ **lấy** logger; ứng dụng **cấu hình** chúng
(`logging.basicConfig(level=..., format=...)`) ở một nơi — thường là
`__main__`. Sự tách biệt đó là lý do một thư viện không bao giờ có thể spam
console của ứng dụng chủ.
""",
)

# --- module 5 practice sets ---

write_practice(
    M5, "m5-hierarchy-practice",
    "Exception Hierarchy Drills",
    "Build app exception families and catch precisely.",
    "Luyện Hệ Exception",
    "Dựng họ exception cho ứng dụng và bắt chính xác.",
    L5A, 25, "intermediate",
    [
        challenge(
            "pi5-exc-family", "App Exception Family",
            "Define AppError(Exception), ValidationError(AppError), and NotFoundError(AppError). Then implement get_item(items: dict, key) that raises NotFoundError (message must contain the key) for missing keys and returns the value otherwise.",
            "class AppError(Exception):\n    pass\n\nclass ValidationError(AppError):\n    pass\n\nclass NotFoundError(AppError):\n    pass\n\ndef get_item(items, key):\n    pass\n",
            [
                ("found returns value",
                 "assert get_item({'a': 1}, 'a') == 1",
                 "Plain lookup when present."),
                ("missing raises NotFoundError",
                 "try:\n    get_item({}, 'x')\n    failed = False\nexcept NotFoundError as e:\n    failed = 'x' in str(e)\nexcept Exception:\n    failed = False\nassert failed",
                 "Raise NotFoundError with the key in the message."),
                ("hierarchy is real",
                 "try:\n    get_item({}, 'x')\nexcept AppError:\n    pass\nelse:\n    raise AssertionError('must be an AppError')",
                 "NotFoundError must be catchable as AppError."),
            ],
            level="guided",
        ),
        challenge(
            "pi5-exc-order", "Catch Order Matters",
            "Given the family above, implement classify(fn) that calls fn() and returns 'validation' if it raises ValidationError, 'notfound' if NotFoundError, 'app' for any other AppError, and 'unknown' for anything else.",
            "def classify(fn):\n    pass\n",
            [
                ("specific before base",
                 "def f(): raise ValidationError('v')\nassert classify(f) == 'validation'",
                 "The ValidationError handler must come before the AppError handler."),
                ("falls back through the family",
                 "def f(): raise NotFoundError('n')\nassert classify(f) == 'notfound'\ndef g(): raise AppError('a')\nassert classify(g) == 'app'",
                 "Each family member maps to its own label."),
                ("foreign errors are unknown",
                 "def f(): raise KeyError('k')\nassert classify(f) == 'unknown'",
                 "Only AppError family maps to app labels."),
            ],
            level="independent",
        ),
    ],
    {
        "pi5-exc-family": vi_challenge("Họ Exception cho ứng dụng", "Định nghĩa AppError(Exception), ValidationError(AppError), và NotFoundError(AppError). Sau đó viết get_item(items: dict, key) raise NotFoundError (thông điệp phải chứa key) cho key thiếu và trả về giá trị nếu có.", [("Có thì trả giá trị", "Tra cứu bình thường khi key tồn tại."), ("Thiếu thì raise NotFoundError", "Raise NotFoundError với key nằm trong thông điệp."), ("Hệ phân cấp phải có thật", "NotFoundError phải bắt được với vai trò AppError.")]),
        "pi5-exc-order": vi_challenge("Thứ tự bắt quyết định tất cả", "Với họ exception trên, viết classify(fn) gọi fn() và trả về 'validation' nếu nó raise ValidationError, 'notfound' nếu NotFoundError, 'app' với bất kỳ AppError khác, và 'unknown' cho mọi thứ khác.", [("Cụ thể trước lớp cha", "Handler ValidationError phải đứng trước handler AppError."), ("Rơi dọc theo họ exception", "Mỗi thành viên trong họ map về nhãn riêng."), ("Lỗi ngoài là unknown", "Chỉ họ AppError mới map sang nhãn app.")]),
    },
    solutions=[
        ("pi5-exc-family", "class AppError(Exception):\n    pass\n\nclass ValidationError(AppError):\n    pass\n\nclass NotFoundError(AppError):\n    pass\n\ndef get_item(items, key):\n    if key not in items:\n        raise NotFoundError(f'key not found: {key}')\n    return items[key]", "class AppError(Exception):\n    pass\n\nclass ValidationError(AppError):\n    pass\n\nclass NotFoundError(AppError):\n    pass\n\ndef get_item(items, key):\n    if key not in items:\n        raise ValueError(f'key not found: {key}')\n    return items[key]"),
        ("pi5-exc-order", "def classify(fn):\n    try:\n        fn()\n    except ValidationError:\n        return 'validation'\n    except NotFoundError:\n        return 'notfound'\n    except AppError:\n        return 'app'\n    except Exception:\n        return 'unknown'", "def classify(fn):\n    try:\n        fn()\n    except AppError:\n        return 'app'\n    except ValidationError:\n        return 'validation'\n    except NotFoundError:\n        return 'notfound'\n    except Exception:\n        return 'unknown'"),
    ],
)

write_practice(
    M5, "m5-chaining-practice",
    "Chaining Drills",
    "Translate errors at boundaries and preserve the cause.",
    "Luyện Nối Chuỗi Lỗi",
    "Dịch lỗi tại ranh giới và giữ nguyên nguyên nhân.",
    L5B, 25, "intermediate",
    [
        challenge(
            "pi5-chain-translate", "Translate the Cause",
            "Implement parse_count(text) that converts text to int, raising ValidationError('not a count: <text>') when it fails — chained from the original error (raise ... from exc).",
            "class ValidationError(Exception):\n    pass\n\ndef parse_count(text):\n    pass\n",
            [
                ("valid text parses",
                 "assert parse_count('42') == 42",
                 "int() does the work when the text is a count."),
                ("invalid raises with message",
                 "try:\n    parse_count('abc')\n    failed = False\nexcept ValidationError as e:\n    failed = 'abc' in str(e)\nassert failed",
                 "The message must include the offending text."),
                ("cause is preserved",
                 "try:\n    parse_count('abc')\nexcept ValidationError as e:\n    assert e.__cause__ is not None and isinstance(e.__cause__, ValueError)",
                 "raise ... from exc sets __cause__ — the chain is the point."),
            ],
            level="guided",
        ),
        challenge(
            "pi5-chain-retry", "Bounded Retry",
            "Implement retry(fn, attempts) that calls fn() up to `attempts` times, returning the first successful result. If fn raises, sleep-free retry; when all attempts fail, re-raise the LAST exception.",
            "def retry(fn, attempts):\n    pass\n",
            [
                ("succeeds on a later attempt",
                 "calls = []\ndef flaky():\n    calls.append(1)\n    if len(calls) < 3:\n        raise ValueError('nope')\n    return 'ok'\nassert retry(flaky, 5) == 'ok'\nassert len(calls) == 3",
                 "Keep calling until success or attempts exhausted."),
                ("last exception surfaces",
                 "def always_bad():\n    raise KeyError('final')\ntry:\n    retry(always_bad, 2)\n    failed = False\nexcept KeyError:\n    failed = True\nassert failed",
                 "The final error propagates — swallowed errors hide reality."),
                ("zero attempts still tries once? No — attempts is a hard cap",
                 "calls = []\ndef f():\n    calls.append(1)\n    raise ValueError('x')\ntry:\n    retry(f, 1)\nexcept ValueError:\n    pass\nassert len(calls) == 1",
                 "attempts=1 means exactly one try."),
            ],
            level="combination",
        ),
    ],
    {
        "pi5-chain-translate": vi_challenge("Dịch nguyên nhân", "Viết parse_count(text) chuyển text thành int, raise ValidationError('not a count: <text>') khi thất bại — nối chuỗi từ lỗi gốc (raise ... from exc).", [("Text hợp lệ thì parse", "int() làm việc khi text là số đếm."), ("Lỗi thì raise kèm thông điệp", "Thông điệp phải chứa text vi phạm."), ("Nguyên nhân được giữ", "raise ... from exc đặt __cause__ — chuỗi lỗi chính là điểm chính.")]),
        "pi5-chain-retry": vi_challenge("Retry có giới hạn", "Viết retry(fn, attempts) gọi fn() tối đa `attempts` lần, trả về kết quả thành công đầu tiên. Nếu fn raise, thử lại (không cần sleep); khi mọi lần đều fail, ném lại exception CUỐI cùng.", [("Thành công ở lần sau", "Gọi tiếp cho đến khi thành công hoặc hết số lần."), ("Exception cuối được đưa lên", "Lỗi cuối cùng lan ra ngoài — nuốt lỗi là che giấu thực tế."), ("attempts là giới hạn cứng", "attempts=1 nghĩa là đúng một lần thử.")]),
    },
    solutions=[
        ("pi5-chain-translate", "class ValidationError(Exception):\n    pass\n\ndef parse_count(text):\n    try:\n        return int(text)\n    except ValueError as exc:\n        raise ValidationError(f'not a count: {text}') from exc", "class ValidationError(Exception):\n    pass\n\ndef parse_count(text):\n    try:\n        return int(text)\n    except ValueError:\n        raise ValidationError(f'not a count: {text}')"),
        ("pi5-chain-retry", "def retry(fn, attempts):\n    last = None\n    for _ in range(attempts):\n        try:\n            return fn()\n        except Exception as exc:\n            last = exc\n    raise last", "def retry(fn, attempts):\n    for _ in range(attempts):\n        try:\n            return fn()\n        except Exception:\n            continue\n    return None"),
    ],
)

write_practice(
    M5, "m5-logging-practice",
    "Logging Drills",
    "Log with the right logger, level, and lazy formatting.",
    "Luyện Logging",
    "Log đúng logger, đúng mức, và định dạng lười.",
    L5C, 20, "intermediate",
    [
        challenge(
            "pi5-log-record", "Emit and Verify",
            "Configure a logger named 'app.checkpoint' with a StreamHandler writing to a StringIO and a formatter '%(levelname)s:%(name)s:%(message)s' (assign it to LOG_OUTPUT so the grader can read it). Then implement warn_twice(msg) that emits msg twice at WARNING level using lazy %-formatting.",
            "import io, logging\n\nLOG_OUTPUT = io.StringIO()\n\nlog = logging.getLogger('app.checkpoint')\n# configure handler + formatter here\n\ndef warn_twice(msg):\n    pass\n",
            [
                ("warning appears with level and name",
                 "warn_twice('disk 80%')\nout = LOG_OUTPUT.getvalue()\nassert 'WARNING:app.checkpoint:disk 80%' in out",
                 "The formatter string decides the shape: LEVEL:NAME:MESSAGE."),
                ("exactly two emissions",
                 "LOG_OUTPUT.seek(0); LOG_OUTPUT.truncate(0)\nwarn_twice('x')\nassert LOG_OUTPUT.getvalue().count('x') == 2",
                 "Call log.warning twice, not a loop of four."),
                ("uses lazy formatting (no f-string in the call)",
                 "import inspect\nsrc = inspect.getsource(warn_twice)\nassert 'f\"' not in src and \"f'\" not in src\nassert 'log.warning(' in src",
                 "log.warning('... %s', value) defers string building."),
            ],
            level="guided",
        ),
        challenge(
            "pi5-log-error-exc", "Error with Traceback",
            "Reusing the LOG_OUTPUT logger config, implement safe_run(fn) that calls fn(); on exception it must log at ERROR level with exc_info=True and return the string 'handled'. On success it returns fn's result.",
            "import io, logging\n\nLOG_OUTPUT = io.StringIO()\nlog = logging.getLogger('app.safe')\n# configure handler + formatter\n\ndef safe_run(fn):\n    pass\n",
            [
                ("success returns the value",
                 "assert safe_run(lambda: 7) == 7",
                 "No exception path — plain return."),
                ("failure logs and returns 'handled'",
                 "def bad(): raise ValueError('boom')\nassert safe_run(bad) == 'handled'\nout = LOG_OUTPUT.getvalue()\nassert 'ERROR:app.safe' in out\nassert 'Traceback' in out",
                 "exc_info=True is what puts the traceback in the record."),
            ],
            level="independent",
        ),
    ],
    {
        "pi5-log-record": vi_challenge("Phát và kiểm chứng log", "Cấu hình logger tên 'app.checkpoint' với StreamHandler ghi vào StringIO và formatter '%(levelname)s:%(name)s:%(message)s' (gán StringIO vào LOG_OUTPUT để trình chấm đọc). Sau đó viết warn_twice(msg) phát msg hai lần ở mức WARNING bằng định dạng %-lười.", [("Warning hiện với level và tên", "Chuỗi formatter quyết định hình dạng: LEVEL:NAME:MESSAGE."), ("Đúng hai lần phát", "Gọi log.warning hai lần, không phải vòng lặp bốn lần."), ("Dùng định dạng lười (không f-string trong lời gọi)", "log.warning('... %s', value) hoãn việc dựng chuỗi.")]),
        "pi5-log-error-exc": vi_challenge("Log lỗi kèm Traceback", "Dùng lại cấu hình logger LOG_OUTPUT, viết safe_run(fn) gọi fn(); khi có exception phải log ở mức ERROR với exc_info=True và trả về chuỗi 'handled'. Khi thành công trả kết quả của fn.", [("Thành công trả giá trị", "Đường không exception — return bình thường."), ("Thất bại log và trả 'handled'", "exc_info=True là thứ đưa traceback vào bản ghi.")]),
    },
    solutions=[
        ("pi5-log-record", "import io, logging\n\nLOG_OUTPUT = io.StringIO()\n\nlog = logging.getLogger('app.checkpoint')\n_handler = logging.StreamHandler(LOG_OUTPUT)\n_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))\nlog.addHandler(_handler)\nlog.setLevel(logging.WARNING)\n\ndef warn_twice(msg):\n    log.warning('%s', msg)\n    log.warning('%s', msg)", "import io, logging\n\nLOG_OUTPUT = io.StringIO()\n\nlog = logging.getLogger('app.checkpoint')\n_handler = logging.StreamHandler(LOG_OUTPUT)\n_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))\nlog.addHandler(_handler)\nlog.setLevel(logging.WARNING)\n\ndef warn_twice(msg):\n    log.warning(f'{msg}')\n    log.warning(msg)"),
        ("pi5-log-error-exc", "import io, logging\n\nLOG_OUTPUT = io.StringIO()\nlog = logging.getLogger('app.safe')\n_handler = logging.StreamHandler(LOG_OUTPUT)\n_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))\nlog.addHandler(_handler)\nlog.setLevel(logging.ERROR)\n\ndef safe_run(fn):\n    try:\n        return fn()\n    except Exception:\n        log.error('operation failed', exc_info=True)\n        return 'handled'", "import io, logging\n\nLOG_OUTPUT = io.StringIO()\nlog = logging.getLogger('app.safe')\n_handler = logging.StreamHandler(LOG_OUTPUT)\n_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))\nlog.addHandler(_handler)\nlog.setLevel(logging.ERROR)\n\ndef safe_run(fn):\n    try:\n        return fn()\n    except Exception:\n        print('operation failed')\n        return 'handled'"),
    ],
)

# --- module 5 checkpoint ---
write_checkpoint(
    M5, L5D,
    "Checkpoint: A Resilient Importer",
    "Combine hierarchy, chaining, retry, and logging into one defensible function.",
    20,
    """
The module's checkpoint is a miniature of real integration work: pull records
from an unreliable source, translate failures, retry transients, log the
journey, and never lie to the caller.

**Working with AI:** pasting a broken function and asking "why does this
swallow errors?" is a great mentor prompt — diagnosing error-swallowing is a
skill interviewers test.
""",
    "Checkpoint: Bộ nhập liệu bền vững",
    "Kết hợp hệ phân cấp, nối chuỗi, retry, và logging thành một hàm đáng tin.",
    """
Checkpoint của module là phiên bản thu nhỏ của công việc tích hợp thật: kéo
bản ghi từ một nguồn hay trục trặc, dịch lỗi, retry các lỗi tạm thời, log
hành trình, và không bao giờ nói dối caller.

**Làm việc cùng AI:** dán một hàm lỗi và hỏi "vì sao hàm này nuốt lỗi?" là
một prompt mentor tuyệt vời — chẩn đoán lỗi bị nuốt là kỹ năng phỏng vấn hay hỏi.
""",
    challenge(
        "pi5-ckpt-importer", "Resilient Record Importer",
        "Implement import_records(sources) where sources is a list of callables, each returning a list of dicts or raising. For each source: retry up to 2 times on failure; on final failure, log it (logger 'pi.importer', any level >= WARNING) and continue. Return the concatenated list of successfully fetched dicts. Preserve order. If EVERY source fails, raise ImportError-like error: raise RuntimeError('all sources failed').",
        "import logging\n\nlog = logging.getLogger('pi.importer')\n\ndef import_records(sources):\n    pass\n",
        [
            ("concatenates successes in order",
             "srcs = [lambda: [{'i': 1}], lambda: [{'i': 2}]]\nassert import_records(srcs) == [{'i': 1}, {'i': 2}]",
             "Extend results in source order."),
            ("retries a transient source",
             "calls = []\ndef flaky():\n    calls.append(1)\n    if len(calls) < 2:\n        raise ValueError('transient')\n    return [{'i': 9}]\nassert import_records([flaky]) == [{'i': 9}]\nassert len(calls) == 2",
             "One retry rescues a transient failure."),
            ("skips a dead source, keeps others",
             "def dead(): raise ValueError('gone')\nsrcs = [dead, lambda: [{'i': 3}]]\nassert import_records(srcs) == [{'i': 3}]",
             "A failing source must not abort the import."),
            ("all sources dead raises",
             "def dead(): raise ValueError('gone')\ntry:\n    import_records([dead, dead])\n    failed = False\nexcept RuntimeError:\n    failed = True\nassert failed",
             "Never return partial data silently — raise RuntimeError when nothing succeeded."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Bộ nhập bản ghi bền vững",
        "Viết import_records(sources) với sources là list các hàm, mỗi hàm trả về list dict hoặc raise. Với từng source: retry tối đa 2 lần khi lỗi; khi lỗi cuối cùng, log lại (logger 'pi.importer', mức >= WARNING bất kỳ) rồi tiếp tục. Trả về list các dict nhập thành công ghép lại. Giữ đúng thứ tự. Nếu MỌI source đều lỗi, raise RuntimeError('all sources failed').",
        [
            ("Ghép các thành công theo thứ tự", "Extend kết quả theo thứ tự source."),
            ("Retry một source tạm trục trặc", "Một lần retry cứu được lỗi tạm thời."),
            ("Bỏ qua source đã chết, giữ phần còn lại", "Source lỗi không được làm hỏng toàn bộ lần nhập."),
            ("Mọi source đều chết thì raise", "Không bao giờ trả dữ liệu một phần một cách lặng lẽ — raise RuntimeError khi không có gì thành công."),
        ],
    ),
    solution="import logging\n\nlog = logging.getLogger('pi.importer')\n\ndef import_records(sources):\n    results = []\n    for source in sources:\n        fetched = None\n        for attempt in range(2):\n            try:\n                fetched = source()\n                break\n            except Exception:\n                if attempt == 1:\n                    log.warning('source failed after retries')\n        if fetched:\n            results.extend(fetched)\n    if not results and sources:\n        raise RuntimeError('all sources failed')\n    return results",
    wrong="import logging\n\nlog = logging.getLogger('pi.importer')\n\ndef import_records(sources):\n    results = []\n    for source in sources:\n        try:\n            results.extend(source())\n        except Exception:\n            continue\n    return results",
)

print("module 5 done")
