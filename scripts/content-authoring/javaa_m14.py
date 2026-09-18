#!/usr/bin/env python3
"""Java — Advanced — Module 14: javaa-observability.

Production eyes: logs as structured data (not strings for humans), request
context propagated through an MDC-style map, in-process metrics (counters,
gauges, timers), and the checkpoint — an incident triage that reads a log
stream and answers questions a pager would ask. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-observability"

L_LOG_EN = """
A log line is a *database row* you're writing to stdout: timestamp, level,
event name, and key-value fields. Grep for `userId=42` works when fields are
first-class; parsing English prose at 3 a.m. does not.

```java
record LogEvent(Instant ts, String level, String event, Map<String, String> fields)
```

Levels are a contract: **ERROR** = a human should act (paging threshold);
**WARN** = degraded but self-healing (retries, fallbacks); **INFO** =
state transitions (started, finished); **DEBUG** = the details you wish you'd
logged, enabled per-request. The cardinal sin: `catch (Exception e) {}` —
an exception that vanishes cannot be diagnosed; log it with its stack, at the
level that matches whether a human must act.

Context: the fields every event in one request shares — requestId, userId —
belong in a thread-local (log frameworks call it MDC) that the framework
stamps onto every line. Propagation across async boundaries is the advanced
wrinkle: the context must be *captured* at task submission and re-applied in
the task, because thread-locals do not cross executor hops.
"""
L_LOG_VI = """
Một dòng log là một *hàng trong bảng dữ liệu* bạn ghi ra stdout: timestamp,
level, tên sự kiện, và các cặp key-value. Grep `userId=42` hoạt động khi field
là dữ liệu bậc nhất; việc phân tích văn xuôi tiếng Anh lúc 3 giờ sáng thì không.

```java
record LogEvent(Instant ts, String level, String event, Map<String, String> fields)
```

Level là một hợp đồng: **ERROR** = có người phải hành động (ngưỡng gọi người);
**WARN** = suy giảm nhưng tự phục hồi (retry, fallback); **INFO** = chuyển
trạng thái (bắt đầu, xong); **DEBUG** = chi tiết mà bạn ước mình đã log, bật
theo từng yêu cầu. Tội kinh điển: `catch (Exception e) {}` — exception biến
mất thì không thể chẩn đoán; hãy log nó cùng stack, ở mức khớp với việc có
ai đó phải hành động hay không.

Context: các field mà mọi sự kiện trong một yêu cầu cùng chia sẻ — requestId,
userId — thuộc về một thread-local (các log framework gọi là MDC) được framework
đóng dấu lên mọi dòng. Truyền qua ranh giới async là nếp nhăn nâng cao: context
phải được *chụp* lúc nộp tác vụ và áp lại trong tác vụ, vì thread-local không
vượt qua được các bước nhảy executor.
"""

L_METRIC_EN = """
Three metric primitives cover most systems:

- **Counter** — only ever increases: requests served, errors, retries.
- **Gauge** — a point-in-time value: queue depth, active connections, cache size.
- **Timer** — a distribution of durations: p50/p95/p99 latency.

```java
long p95(List<Long> sortedMicros) {
    int idx = (int) Math.ceil(0.95 * sortedMicros.size()) - 1;
    return sortedMicros.get(Math.max(0, idx));
}
```

Percentiles answer "how bad is the *worst* user's experience" — the average
hides them (half your users are below average, always). A timer that records
the p99 while the average looks fine is telling you: most requests are quick,
and someone is having a terrible day.

Cardinality is the trap: a label per user id creates one time series per
user — millions of series no backend can store. Labels enumerate *classes*
(endpoint, status, region), never *instances* (user, request, URL with ids).
"""
L_METRIC_VI = """
Ba primitive metric bao phủ phần lớn hệ thống:

- **Counter** — chỉ tăng: số yêu cầu, lỗi, retry.
- **Gauge** — giá trị tại một thời điểm: độ sâu hàng đợi, kết nối hoạt động,
  kích thước cache.
- **Timer** — phân phối thời lượng: latency p50/p95/p99.

```java
long p95(List<Long> sortedMicros) {
    int idx = (int) Math.ceil(0.95 * sortedMicros.size()) - 1;
    return sortedMicros.get(Math.max(0, idx));
}
```

Phân vị trả lời "trải nghiệm của người dùng *tệ nhất* tệ đến mức nào" — trung
bình che giấu họ (một nửa người dùng của bạn luôn dưới trung bình). Một timer
cho thấy p99 cao trong khi trung bình đẹp là đang nói: đa số yêu cầu nhanh,
và có ai đó đang có một ngày tồi tệ.

Cardinality là cái bẫy: một label cho mỗi user id tạo ra một time series mỗi
người dùng — hàng triệu series mà không backend nào lưu nổi. Label liệt kê
*lớp* (endpoint, trạng thái, vùng), không bao giờ *thực thể* (người dùng,
yêu cầu, URL có chứa id).
"""

L_TRIAGE_EN = """
Incident triage is reading a log stream backwards from a symptom:

1. **Localize**: find the error events, group by the context fields
   (requestId, endpoint) — one poisoned request or an entire endpoint?
2. **Correlate**: for each affected request, pull its complete event
   timeline — what happened before the error? Timeout after retry after
   degradation is a *cascade*, not an isolated bug.
3. **Quantify**: how many requests, which endpoints, since when? One user is
   support; a pattern is an incident.
4. **Hypothesize**: propose the smallest change consistent with ALL evidence —
   and name the observation that would REFUTE it.

The output of triage is not "the fix" — it's a *narrowed search space* and a
monitoring query you can watch. The checkpoint assembles all four steps as
pure functions over a structured event stream: no grep, no guessing, just
data in, questions answered.
"""
L_TRIAGE_VI = """
Giải quyết sự cố là đọc ngược luồng log từ một triệu chứng:

1. **Định vị**: tìm các sự kiện lỗi, nhóm theo field context (requestId,
   endpoint) — một yêu cầu độc hay cả một endpoint?
2. **Tương quan**: với mỗi yêu cầu bị ảnh hưởng, kéo ra toàn bộ dòng thời gian
   sự kiện — chuyện gì xảy ra trước lỗi? Timeout sau retry sau suy giảm là một
   *thác đổ*, không phải bug đơn lẻ.
3. **Định lượng**: bao nhiêu yêu cầu, endpoint nào, từ khi nào? Một người dùng
   là chuyện support; một quy luật là sự cố.
4. **Giả thuyết**: đề xuất thay đổi nhỏ nhất khớp với TOÀN BỘ bằng chứng — và
   nêu quan sát sẽ BÁC BỎ nó.

Sản phẩm của việc giải sự cố không phải "bản sửa" — mà là *không gian tìm kiếm
thu hẹp* và một truy vấn giám sát để theo dõi. Checkpoint lắp cả bốn bước thành
các hàm thuần trên luồng sự kiện có cấu trúc: không grep, không đoán, chỉ dữ
liệu vào, câu hỏi được trả lời.
"""

write_module(
    M, "Observability & Diagnosis",
    "Structured logs, request context, metric primitives, and incident triage as pure functions.",
    "Quan sát & Chẩn đoán",
    "Log có cấu trúc, context yêu cầu, primitive metric, và giải sự cố bằng hàm thuần.",
    ["javaa-structured-logs", "javaa-metric-primitives", "javaa-incident-triage"],
    ["javaa-p14-observability"],
)

write_lesson(M, "javaa-structured-logs",
    "Logs are data",
    "Event fields, level contracts, swallowed exceptions, and context propagation across executors.",
    16, L_LOG_EN,
    "Log là dữ liệu",
    "Field sự kiện, hợp đồng level, exception bị nuốt, và truyền context qua executor.",
    L_LOG_VI)

write_lesson(M, "javaa-metric-primitives",
    "Metric primitives",
    "Counters, gauges, timers, percentile math, and the cardinality trap.",
    15, L_METRIC_EN,
    "Primitive metric",
    "Counter, gauge, timer, phép toán phân vị, và cái bẫy cardinality.",
    L_METRIC_VI)

write_lesson(M, "javaa-incident-triage",
    "Incident triage",
    "Localize, correlate, quantify, hypothesize — a method for 3 a.m.",
    17, L_TRIAGE_EN,
    "Giải quyết sự cố",
    "Định vị, tương quan, định lượng, giả thuyết — một phương pháp cho lúc 3 giờ sáng.",
    L_TRIAGE_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_LOGS = challenge(
    "javaa-p14-logs",
    "Structured logging, executed",
    "1. `static String format(java.util.Map<String, String> fields)` — return a\n"
    "deterministic line: keys SORTED alphabetically, each as `key=value`, joined by a\n"
    "single space. Empty map → empty string.\n"
    "2. `static java.util.Map<String, String> parse(String line)` — the inverse: split on\n"
    "single spaces, split each token on the FIRST '=', build the map.\n"
    "3. `static List<String> levelOf(List<String> lines)` — extract the value of \"level\"\n"
    "from each line via parse().\n"
    "4. `static List<String> actionFor(String level)` — the level contract as data:\n"
    "\"ERROR\"→[\"page\"], \"WARN\"→[\"watch\"], \"INFO\"→[\"ignore\"], unknown→[\"investigate\"].",
    P_BOILER,
    [
        ("fields round-trip deterministically", r"""
java.util.Map<String, String> f = new java.util.HashMap<>();
f.put("userId", "42"); f.put("event", "login"); f.put("level", "INFO");
checkEq(Solution.format(f), "event=login level=INFO userId=42", "sorted fields");
checkEq(Solution.parse("event=login level=INFO"), java.util.Map.of("event", "login", "level", "INFO"), "parse inverse");
checkEq(Solution.levelOf(java.util.List.of("level=ERROR event=crash")), java.util.List.of("ERROR"), "level extracted");
checkEq(Solution.actionFor("ERROR"), java.util.List.of("page"), "errors page");
checkEq(Solution.actionFor("WARN"), java.util.List.of("watch"), "warns watch");
checkEq(Solution.actionFor("mystery"), java.util.List.of("investigate"), "unknown investigates");
""", "Logs in, structured answers out."),
    ],
    level="guided",
)
CH_LOGS_VI = vi_challenge(
    "Structured logging, chạy thật",
    "format/parse/levelOf/actionFor: field sắp xếp tất định, parse là nghịch đảo, hợp đồng level thành dữ liệu.",
    [("Field khép kín tất định", "Key sắp xếp theo bảng chữ cái."),
     ("Hợp đồng level", "ERROR gọi người, WARN theo dõi, INFO bỏ qua.")],
)

CH_METRICS = challenge(
    "javaa-p14-metrics",
    "Counters, gauges, percentiles",
    "1. `static long p(List<Long> sortedMicros, double q)` — the q-th percentile of a\n"
    "SORTED list: index = ceil(q * n) - 1, clamped to >= 0. p(x, 0.5) is the median.\n"
    "2. `static java.util.Map<String, Long> summarize(java.util.List<Long> durations)` —\n"
    "sort internally, return {\"p50\":..., \"p95\":..., \"p99\":..., \"count\": n}.\n"
    "3. `static boolean avgHides(List<Long> durations)` — return true iff the MEAN is\n"
    "less than p95 (the classic 'average looks fine' lie). Empty list → false.\n"
    "4. `static boolean cardinalityOk(String labelKey)` — true iff labelKey is a CLASS\n"
    "(one of \"endpoint\", \"status\", \"region\"), false for instance labels\n"
    "(\"userId\", \"requestId\", \"url\").",
    P_BOILER,
    [
        ("percentile math and the average lie", r"""
java.util.List<Long> d = java.util.List.of(1L, 2L, 3L, 4L, 100L);
checkEq(Solution.p(d, 0.5), 3L, "median of five");
checkEq(Solution.p(d, 0.95), 100L, "p95 is the outlier");
java.util.Map<String, Long> s = Solution.summarize(d);
checkEq(s.get("count"), 5L, "count present");
checkEq(s.get("p99"), 100L, "p99 present");
checkTrue(Solution.avgHides(d), "mean (22) is below p95 (100)");
checkTrue(!Solution.avgHides(java.util.List.of(5L, 5L, 5L)), "flat distribution: no lie");
""", "Averages hide tails; percentiles expose them."),
        ("label discipline", r"""
checkTrue(Solution.cardinalityOk("endpoint"), "class label");
checkTrue(!Solution.cardinalityOk("userId"), "instance label");
""", "Classes yes, instances never."),
    ],
    level="independent",
)
CH_METRICS_VI = vi_challenge(
    "Counter, gauge, phân vị",
    "p/summarize/avgHides/cardinalityOk: phép toán phân vị, trung bình che đuôi phân phối, và kỷ luật label.",
    [("Phép toán phân vị và lời nói dối của trung bình", "Trung bình che đuôi; phân vị phơi bày."),
     ("Kỷ luật label", "Lớp được, thực thể không bao giờ.")],
)

write_practice(M, "javaa-p14-observability",
    "Observability drills",
    "Structure logs, compute percentiles, and carry context across executor hops.",
    "Bài tập quan sát",
    "Cấu trúc log, tính phân vị, và mang context qua các bước nhảy executor.",
    "javaa-incident-triage", 55, "advanced",
    [CH_LOGS, CH_METRICS],
    {"javaa-p14-logs": CH_LOGS_VI, "javaa-p14-metrics": CH_METRICS_VI},
    solutions=[
        ("javaa-p14-logs", r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static String format(Map<String, String> fields) {
        return fields.entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining(" "));
    }

    public static Map<String, String> parse(String line) {
        Map<String, String> out = new HashMap<>();
        if (line == null || line.isEmpty()) return out;
        for (String token : line.split(" ")) {
            int eq = token.indexOf('=');
            if (eq > 0) out.put(token.substring(0, eq), token.substring(eq + 1));
        }
        return out;
    }

    public static List<String> levelOf(List<String> lines) {
        return lines.stream()
            .map(l -> parse(l).get("level"))
            .filter(Objects::nonNull)
            .collect(Collectors.toList());
    }

    public static List<String> actionFor(String level) {
        return switch (level) {
            case "ERROR" -> List.of("page");
            case "WARN" -> List.of("watch");
            case "INFO" -> List.of("ignore");
            default -> List.of("investigate");
        };
    }
}
""", r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static String format(Map<String, String> fields) {
        return fields.entrySet().stream()
            .map(e -> e.getKey() + "=" + e.getValue())   // WRONG: HashMap order — nondeterministic lines
            .collect(Collectors.joining(" "));
    }

    public static Map<String, String> parse(String line) {
        Map<String, String> out = new HashMap<>();
        for (String token : line.split(" ")) {           // WRONG: null/empty input crashes
            out.put(token, token);                        // WRONG: no '=' split — key is the whole token
        }
        return out;
    }

    public static List<String> levelOf(List<String> lines) {
        return lines;   // WRONG: returns lines, not levels
    }

    public static List<String> actionFor(String level) {
        return List.of("ignore");   // WRONG: everything ignored — including errors
    }
}
"""),
        ("javaa-p14-metrics", r"""
import java.util.*;

public class Solution {
    public static long p(List<Long> sortedMicros, double q) {
        if (sortedMicros.isEmpty()) return 0;
        int idx = (int) Math.ceil(q * sortedMicros.size()) - 1;
        return sortedMicros.get(Math.max(0, idx));
    }

    public static Map<String, Long> summarize(List<Long> durations) {
        List<Long> sorted = new ArrayList<>(durations);
        Collections.sort(sorted);
        Map<String, Long> out = new LinkedHashMap<>();
        out.put("p50", p(sorted, 0.5));
        out.put("p95", p(sorted, 0.95));
        out.put("p99", p(sorted, 0.99));
        out.put("count", (long) sorted.size());
        return out;
    }

    public static boolean avgHides(List<Long> durations) {
        if (durations.isEmpty()) return false;
        double mean = durations.stream().mapToLong(Long::longValue).average().orElse(0);
        List<Long> sorted = new ArrayList<>(durations);
        Collections.sort(sorted);
        return mean < p(sorted, 0.95);
    }

    public static boolean cardinalityOk(String labelKey) {
        return labelKey.equals("endpoint") || labelKey.equals("status") || labelKey.equals("region");
    }
}
""", r"""
import java.util.*;

public class Solution {
    public static long p(List<Long> sortedMicros, double q) {
        return sortedMicros.get(0);   // WRONG: always the minimum
    }

    public static Map<String, Long> summarize(List<Long> durations) {
        Map<String, Long> out = new LinkedHashMap<>();
        out.put("p50", 0L); out.put("p95", 0L); out.put("p99", 0L);
        out.put("count", 0L);   // WRONG: hardcoded zeros
        return out;
    }

    public static boolean avgHides(List<Long> durations) {
        return true;   // WRONG: claims the lie always — even for flat data
    }

    public static boolean cardinalityOk(String labelKey) {
        return true;   // WRONG: user-id labels allowed — cardinality explosion
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the incident triage

Read a structured event stream and answer what a pager would ask: which
requests, which endpoints, what cascaded, and what would refute the leading
hypothesis.
"""

CP_CH = challenge(
    "javaa-checkpoint-m14-task",
    "Checkpoint: triage the incident",
    "Events are lines `ts=<n> level=<L> event=<E> requestId=<R> endpoint=<P>` (already\n"
    "parsed for you as records). Inside Solution, implement `static class Ev` with\n"
    "`long ts; String level, event, requestId, endpoint;` and a constructor\n"
    "`Ev(long, String, String, String, String)`, then:\n"
    "1. `static List<String> affectedRequests(List<Ev> events)` — requestIds that have at\n"
    "least one level=ERROR event, in first-appearance order, deduplicated.\n"
    "2. `static Map<String, Long> byEndpoint(List<Ev> events)` — count of ERROR events\n"
    "per endpoint.\n"
    "3. `static List<String> cascadeOf(List<Ev> events, String requestId)` — the event\n"
    "names for that request in ts order (its full timeline).\n"
    "4. `static String verdict(List<Ev> events)` — return \"isolated\" if exactly one\n"
    "request is affected, \"endpoint-outage\" if one endpoint accounts for ALL errors and\n"
    "there are 2+ affected requests, else \"widespread\".\n"
    "5. `static String refutes(String hypothesis)` — the observation that would kill each\n"
    "leading hypothesis: \"endpoint-outage\"→\"an error on a different endpoint\",\n"
    "\"isolated\"→\"a second affected request\", \"widespread\"→\"errors stop after deploy\".",
    P_BOILER,
    [
        ("localize, correlate, quantify", r"""
java.util.List<Solution.Ev> events = java.util.List.of(
    new Solution.Ev(1, "INFO", "start", "r1", "/a"),
    new Solution.Ev(2, "ERROR", "timeout", "r1", "/a"),
    new Solution.Ev(3, "INFO", "start", "r2", "/b"),
    new Solution.Ev(4, "ERROR", "timeout", "r2", "/b"),
    new Solution.Ev(5, "ERROR", "db-down", "r3", "/a"));
checkEq(Solution.affectedRequests(events), java.util.List.of("r1", "r2", "r3"), "three requests, in order");
checkEq(Solution.byEndpoint(events), java.util.Map.of("/a", 2L, "/b", 1L), "endpoint counts");
checkEq(Solution.cascadeOf(events, "r1"), java.util.List.of("start", "timeout"), "r1 timeline");
checkEq(Solution.verdict(events), "widespread", "two endpoints, 3 requests");
""", "Triage as functions over the stream."),
        ("hypotheses are refutable", r"""
checkEq(Solution.refutes("endpoint-outage"), "an error on a different endpoint", "outage refuter");
checkEq(Solution.refutes("isolated"), "a second affected request", "isolation refuter");
checkEq(Solution.refutes("widespread"), "errors stop after deploy", "spread refuter");
""", "Every hypothesis names its own killer."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: giải quyết sự cố",
    "affectedRequests/byEndpoint/cascadeOf/verdict/refutes: định vị, tương quan, định lượng, và mọi giả thuyết đều nêu được manh mối bác bỏ.",
    [("Định vị, tương quan, định lượng", "Giải sự cố bằng hàm trên luồng sự kiện."),
     ("Giả thuyết có thể bác bỏ", "Mỗi giả thuyết nêu chính kẻ giết mình.")],
)

write_checkpoint(M, "javaa-checkpoint-m14",
    "Checkpoint: The Incident Triage",
    "Localize, correlate, quantify — and name what would refute you.",
    28, CP_MD,
    "Checkpoint: Giải quyết sự cố",
    "Định vị, tương quan, định lượng — và nêu cái gì sẽ bác bỏ bạn.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static class Ev {
        public final long ts;
        public final String level, event, requestId, endpoint;
        public Ev(long ts, String level, String event, String requestId, String endpoint) {
            this.ts = ts; this.level = level; this.event = event;
            this.requestId = requestId; this.endpoint = endpoint;
        }
    }

    public static List<String> affectedRequests(List<Ev> events) {
        Set<String> seen = new LinkedHashSet<>();
        for (Ev e : events) {
            if (e.level.equals("ERROR")) seen.add(e.requestId);
        }
        return new ArrayList<>(seen);
    }

    public static Map<String, Long> byEndpoint(List<Ev> events) {
        return events.stream()
            .filter(e -> e.level.equals("ERROR"))
            .collect(Collectors.groupingBy(e -> e.endpoint, Collectors.counting()));
    }

    public static List<String> cascadeOf(List<Ev> events, String requestId) {
        return events.stream()
            .filter(e -> e.requestId.equals(requestId))
            .sorted(Comparator.comparingLong(e -> e.ts))
            .map(e -> e.event)
            .collect(Collectors.toList());
    }

    public static String verdict(List<Ev> events) {
        List<String> affected = affectedRequests(events);
        Map<String, Long> byEp = byEndpoint(events);
        if (affected.size() == 1) return "isolated";
        if (byEp.size() == 1 && affected.size() >= 2) return "endpoint-outage";
        return "widespread";
    }

    public static String refutes(String hypothesis) {
        return switch (hypothesis) {
            case "endpoint-outage" -> "an error on a different endpoint";
            case "isolated" -> "a second affected request";
            case "widespread" -> "errors stop after deploy";
            default -> "no refuter defined";
        };
    }
}
""", wrong=r"""
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static class Ev {
        public final long ts;
        public final String level, event, requestId, endpoint;
        public Ev(long ts, String level, String event, String requestId, String endpoint) {
            this.ts = ts; this.level = level; this.event = event;
            this.requestId = requestId; this.endpoint = endpoint;
        }
    }

    public static List<String> affectedRequests(List<Ev> events) {
        Set<String> seen = new HashSet<>();     // WRONG: HashSet scrambles first-appearance order
        for (Ev e : events) {
            if (e.level.equals("ERROR")) seen.add(e.requestId);
        }
        return new ArrayList<>(seen);
    }

    public static Map<String, Long> byEndpoint(List<Ev> events) {
        Map<String, Long> out = new HashMap<>();
        for (Ev e : events) {                    // WRONG: counts ALL events, not errors
            out.merge(e.endpoint, 1L, Long::sum);
        }
        return out;
    }

    public static List<String> cascadeOf(List<Ev> events, String requestId) {
        return events.stream()
            .filter(e -> e.level.equals("ERROR"))   // WRONG: only errors — timeline loses context
            .map(e -> e.event)
            .collect(Collectors.toList());
    }

    public static String verdict(List<Ev> events) {
        return "widespread";   // WRONG: one verdict for every incident
    }

    public static String refutes(String hypothesis) {
        return "unknown";   // WRONG: unfalsifiable analysis
    }
}
""")

print("module 14 authored")
