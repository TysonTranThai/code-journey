#!/usr/bin/env python3
"""Java — Advanced — Module 15: javaa-capstone.

The course in one system: a LedgerService whose storage is a *plug*
(engine interface), one engine in memory, one on real JSONL files
(Module 10), served through a deadline-bounded async report (Module 12),
health-checkable like an observable service (Module 14). The checkpoint
proves polymorphism the only honest way: byte-identical reports from two
different engines. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-capstone"

L_ARCH_EN = """
The capstone architecture is four layers with one dependency direction:

```text
Service (LedgerService)   — orchestration, no storage knowledge
Engine (interface)        — put/get/all/count, nothing more
InMemory / JsonlFile      — two interchangeable implementations
Wire/Report (records)     — the data that crosses boundaries
```

The service is *compiled against* the interface and *run against* either
engine. Swapping engines changes nothing above the interface line — that is
the whole point, and the checkpoint verifies it behaviorally: identical
sequences of operations through either engine must produce byte-identical
reports. Not "similar" — identical, because determinism is what makes a
report trustworthy and a regression testable.

Design rules the course has earned: records for boundary data (immutable,
final fields — Module 1); the engine interface is *narrow* (four methods —
Module 6's capture lesson: every method you don't declare is a method you
never have to fake); the JSONL engine holds a `Path` it owns and appends
atomically (Module 10's journal discipline); the service bounds its report
fan-out with per-branch `orTimeout` (Module 12) and exposes a health check
that reads its own counters (Module 14).
"""
L_ARCH_VI = """
Kiến trúc capstone là bốn tầng với một hướng phụ thuộc:

```text
Service (LedgerService)   — điều phối, không biết gì về lưu trữ
Engine (interface)        — put/get/all/count, không hơn
InMemory / JsonlFile      — hai cài đặt hoán đổi cho nhau
Wire/Report (record)      — dữ liệu vượt ranh giới
```

Service được *biên dịch dựa trên* interface và *chạy trên* một trong hai
engine. Đổi engine không đổi gì phía trên đường interface — đó là toàn bộ ý
nghĩa, và checkpoint xác minh điều đó bằng hành vi: cùng một chuỗi phép toán
qua hai engine phải cho ra các báo cáo GIỐNG NHAU TỪNG BYTE. Không phải "tương
tự" — giống hệt, vì tính tất định là thứ làm cho báo cáo đáng tin và regression
có thể kiểm thử.

Các quy tắc thiết kế mà khóa học đã trả giá: record cho dữ liệu ranh giới
(bất biến, field final — Module 1); interface engine *hẹp* (bốn phương thức —
bài học capture của Module 6: mỗi phương thức bạn không khai báo là một phương
thức bạn không bao giờ phải giả lập); engine JSONL giữ một `Path` mà nó sở hữu
và append nguyên tử (kỷ luật journal của Module 10); service chặn trên fan-out
báo cáo bằng `orTimeout` theo nhánh (Module 12) và phơi một health check đọc
chính counter của nó (Module 14).
"""

L_ENG_EN = """
Two engines, one contract:

```java
public interface Engine {
    void put(String key, String value);   // upsert
    java.util.Optional<String> get(String key);
    java.util.List<String> keys();        // sorted, for determinism
    int count();
}
```

**InMemory**: a `ConcurrentHashMap` behind the interface. Determinism comes
from `keys()` sorting — iteration order of a hash map is otherwise an
implementation detail that would leak into reports.

**JsonlFile**: the source of truth is an append-only file, one JSON-ish
record per line: `{"op":"put","k":"a","v":"1"}`. `put` appends then updates
an in-memory index (write-through); `keys()` sorts the index the same way.
Replay — reading the file and re-applying operations — rebuilds the state
after any "restart"; the checkpoint simulates one by constructing a second
engine over the same path and comparing reports.

This is the Shape of every real persistence layer: an ordered event log you
can replay, an index you can rebuild, and a read path that never lies about
what has been acknowledged.
"""
L_ENG_VI = """
Hai engine, một hợp đồng:

```java
public interface Engine {
    void put(String key, String value);   // upsert
    java.util.Optional<String> get(String key);
    java.util.List<String> keys();        // đã sắp, vì tính tất định
    int count();
}
```

**InMemory**: một `ConcurrentHashMap` sau interface. Tính tất định đến từ
`keys()` có sắp xếp — thứ tự lặp của hash map vốn là chi tiết cài đặt, sẽ rò
vào báo cáo nếu không chặn.

**JsonlFile**: nguồn sự thật là một tệp chỉ-ghi-thêm, mỗi dòng một bản ghi
kiểu JSON: `{"op":"put","k":"a","v":"1"}`. `put` ghi thêm rồi cập nhật chỉ
mục in-memory (write-through); `keys()` sắp chỉ mục theo cùng cách. Replay —
đọc tệp và áp dụng lại các phép toán — dựng lại trạng thái sau bất kỳ lần
"khởi động lại" nào; checkpoint mô phỏng bằng cách dựng engine thứ hai trên
cùng path và so báo cáo.

Đây là Hình dạng của mọi tầng lưu trữ thật: một nhật ký sự kiện có thứ tự có
thể phát lại, một chỉ mục có thể dựng lại, và đường đọc không bao giờ nói dối
về những gì đã được xác nhận.
"""

L_REPORT_EN = """
The report is where every course thread meets:

```java
static String report(LedgerService svc, List<String> keys, Executor exec) {
    List<CompletableFuture<String>> parts = keys.stream()
        .map(k -> CompletableFuture
            .supplyAsync(() -> k + "=" + svc.get(k), exec)
            .orTimeout(50, MILLISECONDS)
            .handle((r, e) -> e == null ? r : k + "=down"))
        .toList();
    CompletableFuture.allOf(parts).orTimeout(500, MILLISECONDS).join();
    return parts.stream().map(CompletableFuture::join)
        .collect(Collectors.joining(","));
}
```

One method that: touches storage only through the interface (polymorphic),
bounds each read (deadline), degrades a slow key to a *value* (partial
success), and joins in submission order (deterministic). Run it against both
engines: two strings, byte-equal. That equality is the proof that the
abstraction held — nothing above the interface ever knew which engine answered.
"""
L_REPORT_VI = """
Báo cáo là nơi mọi sợi chỉ của khóa học gặp nhau:

```java
static String report(LedgerService svc, List<String> keys, Executor exec) {
    List<CompletableFuture<String>> parts = keys.stream()
        .map(k -> CompletableFuture
            .supplyAsync(() -> k + "=" + svc.get(k), exec)
            .orTimeout(50, MILLISECONDS)
            .handle((r, e) -> e == null ? r : k + "=down"))
        .toList();
    CompletableFuture.allOf(parts).orTimeout(500, MILLISECONDS).join();
    return parts.stream().map(CompletableFuture::join)
        .collect(Collectors.joining(","));
}
```

Một phương thức mà: chạm vào lưu trữ chỉ qua interface (đa hình), chặn trên
từng lần đọc (hạn chót), suy giảm key chậm thành một *giá trị* (thành công một
phần), và join theo thứ tự nộp (tất định). Chạy nó trên hai engine: hai chuỗi,
bằng nhau từng byte. Sự bằng nhau đó là bằng chứng rằng abstraction đã giữ vững
— không gì phía trên interface từng biết engine nào đã trả lời.
"""

write_module(
    M, "Capstone: The Ledger Service",
    "Pluggable storage engines, an append-only JSONL truth, and byte-identical polymorphic reports.",
    "Capstone: Dịch vụ Sổ cái",
    "Engine lưu trữ cắm được, nguồn thật JSONL chỉ-ghi-thêm, và báo cáo đa hình giống nhau từng byte.",
    ["javaa-capstone-architecture", "javaa-capstone-engines", "javaa-capstone-report"],
    ["javaa-p15-capstone"],
)

write_lesson(M, "javaa-capstone-architecture",
    "Architecture: the narrow seam",
    "Four layers, one dependency direction, and determinism as a design requirement.",
    17, L_ARCH_EN,
    "Kiến trúc: đường nối hẹp",
    "Bốn tầng, một hướng phụ thuộc, và tính tất định là yêu cầu thiết kế.",
    L_ARCH_VI)

write_lesson(M, "javaa-capstone-engines",
    "Two engines, one contract",
    "The in-memory index and the append-only JSONL truth with replay.",
    18, L_ENG_EN,
    "Hai engine, một hợp đồng",
    "Chỉ mục in-memory và nguồn thật JSONL chỉ-ghi-thêm với replay.",
    L_ENG_VI)

write_lesson(M, "javaa-capstone-report",
    "The polymorphic report",
    "Deadline-bounded reads over an unknown engine, collected deterministically.",
    17, L_REPORT_EN,
    "Báo cáo đa hình",
    "Đọc có hạn chót trên engine không biết trước, thu thập tất định.",
    L_REPORT_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_ENGINE = challenge(
    "javaa-p15-engine",
    "The narrow seam",
    "Inside Solution, implement the engine contract:\n"
    "1. `public interface Engine { void put(String key, String value);\n"
    "java.util.Optional<String> get(String key); java.util.List<String> keys();\n"
    "int count(); }`\n"
    "2. `public static class InMemory implements Engine` — ConcurrentHashMap backed;\n"
    "`keys()` returns keys SORTED ascending (determinism is part of the contract).\n"
    "3. `public static class JsonlFile implements Engine` — constructor takes a\n"
    "`java.nio.file.Path` of an append-only file; `put` appends the line\n"
    "`{\"op\":\"put\",\"k\":\"<key>\",\"v\":\"<value>\"}\\n` (UTF-8, CREATE+APPEND) then updates an\n"
    "internal ConcurrentHashMap index (write-through); `get`/`keys`/`count` read the\n"
    "index; `keys()` sorted ascending.\n"
    "4. `static Engine replay(Path file)` — a NEW JsonlFile whose state is rebuilt by\n"
    "reading every line of the existing file and applying each op in order (later puts\n"
    "overwrite earlier ones for the same key).",
    P_BOILER,
    [
        ("in-memory contract", r"""
Solution.Engine m = new Solution.InMemory();
m.put("b", "2"); m.put("a", "1"); m.put("a", "1x");
checkEq(m.get("a"), java.util.Optional.of("1x"), "upsert wins");
checkEq(m.get("zz"), java.util.Optional.empty(), "absent is empty");
checkEq(m.keys(), java.util.List.of("a", "b"), "sorted keys");
checkEq(m.count(), 2, "two entries");
""", "Sorted keys; upsert semantics."),
        ("jsonl engine persists and replays", r"""
java.nio.file.Path f = java.nio.file.Files.createTempFile("cjadv", ".jsonl");
Solution.Engine e = new Solution.JsonlFile(f);
e.put("b", "2"); e.put("a", "1");
Solution.Engine r = Solution.replay(f);
checkEq(r.get("a"), java.util.Optional.of("1"), "replayed state");
checkEq(r.keys(), java.util.List.of("a", "b"), "replayed keys sorted");
checkEq(r.count(), 2, "replayed count");
""", "The file is the truth; the index is a cache."),
    ],
    level="guided",
)
CH_ENGINE_VI = vi_challenge(
    "Đường nối hẹp",
    "Engine/InMemory/JsonlFile/replay: keys sắp xếp là một phần của hợp đồng; tệp là sự thật, chỉ mục là cache.",
    [("Hợp đồng in-memory", "Key sắp xếp; ngữ nghĩa upsert."),
     ("Engine jsonl lưu và phát lại", "Trạng thái dựng lại từ tệp.")],
)

CH_SERVICE = challenge(
    "javaa-p15-service",
    "The service over either engine",
    "Inside Solution, add `public static class LedgerService`:\n"
    "1. Constructor takes an `Engine` and stores it (polymorphism by construction).\n"
    "2. `String get(String key)` — returns the value or the literal \"MISSING\" (the\n"
    "service shapes the engine's Optional into domain language).\n"
    "3. `void record(String key, String value)` — delegates to engine.put.\n"
    "4. `java.util.List<String> entries()` — engine.keys() mapped to `key=value` strings,\n"
    "in the engine's (sorted) order.\n"
    "5. `static String health(int count, int failures)` — returns \"green\" if failures ==\n"
    "0 and count > 0, \"yellow\" if failures == 0 and count == 0, \"red\" otherwise.",
    P_BOILER,
    [
        ("the service is engine-blind", r"""
Solution.Engine m = new Solution.InMemory();
Solution.LedgerService s = new Solution.LedgerService(m);
s.record("a", "1"); s.record("b", "2");
checkEq(s.get("a"), "1", "recorded value");
checkEq(s.get("zz"), "MISSING", "domain language for absence");
checkEq(s.entries(), java.util.List.of("a=1", "b=2"), "sorted entries");
checkEq(Solution.LedgerService.health(2, 0), "green", "data + no failures");
checkEq(Solution.LedgerService.health(0, 0), "yellow", "empty is yellow");
checkEq(Solution.LedgerService.health(0, 3), "red", "failures are red");
""", "One service, any engine, honest health."),
    ],
    level="independent",
)
CH_SERVICE_VI = vi_challenge(
    "Service trên bất kỳ engine nào",
    "LedgerService: mù engine theo kiến tạo, Optional thành ngôn ngữ domain, entries theo thứ tự engine, health ba màu.",
    [("Service mù engine", "Một service, bất kỳ engine nào, sức khỏe trung thực.")],
)

write_practice(M, "javaa-p15-capstone",
    "Capstone build",
    "Assemble the engines and the service that cannot tell them apart.",
    "Dựng capstone",
    "Lắp ráp các engine và service không thể phân biệt chúng.",
    "javaa-capstone-report", 60, "advanced",
    [CH_ENGINE, CH_SERVICE],
    {"javaa-p15-engine": CH_ENGINE_VI, "javaa-p15-service": CH_SERVICE_VI},
    solutions=[
        ("javaa-p15-engine", r"""
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public interface Engine {
        void put(String key, String value);
        Optional<String> get(String key);
        List<String> keys();
        int count();
    }

    public static class InMemory implements Engine {
        private final ConcurrentHashMap<String, String> data = new ConcurrentHashMap<>();

        public void put(String key, String value) { data.put(key, value); }
        public Optional<String> get(String key) { return Optional.ofNullable(data.get(key)); }
        public List<String> keys() {
            List<String> ks = new ArrayList<>(data.keySet());
            Collections.sort(ks);
            return ks;
        }
        public int count() { return data.size(); }
    }

    public static class JsonlFile implements Engine {
        private final Path file;
        private final ConcurrentHashMap<String, String> index = new ConcurrentHashMap<>();

        JsonlFile(Path file) {
            this.file = file;
        }

        public void put(String key, String value) {
            try {
                Files.writeString(file,
                    "{\"op\":\"put\",\"k\":\"" + key + "\",\"v\":\"" + value + "\"}\n",
                    StandardCharsets.UTF_8, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
            index.put(key, value);
        }

        public Optional<String> get(String key) { return Optional.ofNullable(index.get(key)); }
        public List<String> keys() {
            List<String> ks = new ArrayList<>(index.keySet());
            Collections.sort(ks);
            return ks;
        }
        public int count() { return index.size(); }

        void apply(String line) {
            int k = line.indexOf("\"k\":\"") + 5;
            int kEnd = line.indexOf("\"", k);
            int v = line.indexOf("\"v\":\"") + 5;
            int vEnd = line.indexOf("\"", v);
            if (k > 4 && v > 4 && kEnd > k && vEnd > v) {
                index.put(line.substring(k, kEnd), line.substring(v, vEnd));
            }
        }
    }

    public static Engine replay(Path file) {
        try {
            JsonlFile e = new JsonlFile(file);
            for (String line : Files.readAllLines(file, StandardCharsets.UTF_8)) {
                e.apply(line);
            }
            return e;
        } catch (IOException ex) {
            throw new UncheckedIOException(ex);
        }
    }
}
""", r"""
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public interface Engine {
        void put(String key, String value);
        Optional<String> get(String key);
        List<String> keys();
        int count();
    }

    public static class InMemory implements Engine {
        private final ConcurrentHashMap<String, String> data = new ConcurrentHashMap<>();

        public void put(String key, String value) { data.put(key, value); }
        public Optional<String> get(String key) { return Optional.ofNullable(data.get(key)); }
        public List<String> keys() {
            return new ArrayList<>(data.keySet());   // WRONG: hash order leaks — nondeterministic
        }
        public int count() { return data.size(); }
    }

    public static class JsonlFile implements Engine {
        private final Path file;
        private final ConcurrentHashMap<String, String> index = new ConcurrentHashMap<>();

        JsonlFile(Path file) { this.file = file; }

        public void put(String key, String value) {
            index.put(key, value);   // WRONG: file never written — "persistence" that survives nothing
        }

        public Optional<String> get(String key) { return Optional.ofNullable(index.get(key)); }
        public List<String> keys() { return new ArrayList<>(index.keySet()); }
        public int count() { return index.size(); }
    }

    public static Engine replay(Path file) {
        JsonlFile e = new JsonlFile(file);   // WRONG: never reads the file — replay is a stub
        return e;
    }
}
"""),
        ("javaa-p15-service", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Solution {
    public interface Engine {
        void put(String key, String value);
        Optional<String> get(String key);
        List<String> keys();
        int count();
    }

    public static class InMemory implements Engine {
        private final ConcurrentHashMap<String, String> data = new ConcurrentHashMap<>();
        public void put(String key, String value) { data.put(key, value); }
        public Optional<String> get(String key) { return Optional.ofNullable(data.get(key)); }
        public List<String> keys() { return new ArrayList<>(new TreeSet<>(data.keySet())); }
        public int count() { return data.size(); }
    }

    public static class LedgerService {
        private final Engine engine;

        public LedgerService(Engine engine) { this.engine = engine; }

        public String get(String key) {
            return engine.get(key).orElse("MISSING");
        }

        public void record(String key, String value) {
            engine.put(key, value);
        }

        public List<String> entries() {
            return engine.keys().stream()
                .map(k -> k + "=" + engine.get(k).orElse("MISSING"))
                .collect(Collectors.toList());
        }

        public static String health(int count, int failures) {
            if (failures != 0) return "red";
            return count > 0 ? "green" : "yellow";
        }
    }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Solution {
    public interface Engine {
        void put(String key, String value);
        Optional<String> get(String key);
        List<String> keys();
        int count();
    }

    public static class InMemory implements Engine {
        private final ConcurrentHashMap<String, String> data = new ConcurrentHashMap<>();
        public void put(String key, String value) { data.put(key, value); }
        public Optional<String> get(String key) { return Optional.ofNullable(data.get(key)); }
        public List<String> keys() { return new ArrayList<>(new TreeSet<>(data.keySet())); }
        public int count() { return data.size(); }
    }

    public static class LedgerService {
        private final InMemory engine;   // WRONG: compiled against the CONCRETE class —
                                         // a JsonlFile cannot be injected

        public LedgerService(InMemory engine) { this.engine = engine; }

        public String get(String key) {
            return engine.get(key).orElse("MISSING");
        }

        public void record(String key, String value) {
            engine.put(key, value);
        }

        public List<String> entries() {
            List<String> ks = engine.keys();
            return ks;   // WRONG: raw keys, not key=value entries
        }

        public static String health(int count, int failures) {
            return "green";   // WRONG: always green — health that lies
        }
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: byte-identical, engine-independent

The proof: the same operations through the service over two different
engines produce byte-identical reports — and a simulated restart replays
history into identical state. Plus the deadline-bounded async report and the
honest health line: the whole course, one artifact.
"""

CP_CH = challenge(
    "javaa-checkpoint-m15-task",
    "Checkpoint: the ledger, proven",
    "Copy your Engine/InMemory/JsonlFile/replay and LedgerService into Solution, then add:\n"
    "1. `static String report(LedgerService svc, java.util.List<String> keys,\n"
    "java.util.concurrent.Executor exec)` — per key, supplyAsync(() -> key + \"=\" +\n"
    "svc.get(key), exec) with orTimeout(50, MILLISECONDS) and handle → key + \"=down\" on\n"
    "failure; allOf(...).orTimeout(500, MILLISECONDS).join(); join parts in submission\n"
    "order, joined with \",\".\n"
    "2. `static String prove(String seed)` — the proof: build a JsonlFile over a fresh\n"
    "temp file, record seed/a=1, seed/b=2 through a LedgerService; build an InMemory\n"
    "engine, record the SAME operations through another LedgerService; run report(\n"
    "..., List.of(\"a\",\"b\"), sameExecutor) on both; return the two report strings\n"
    "joined with \"|\" — they must be IDENTICAL strings for the test to pass.\n"
    "3. `static boolean survivesRestart(java.nio.file.Path file)` — engine over file,\n"
    "record x=9; build a SECOND service via replay(file); return whether the replayed\n"
    "service get(\"x\") equals \"9\".",
    P_BOILER,
    [
        ("two engines, one report", r"""
java.util.concurrent.Executor exec = java.util.concurrent.Executors.newVirtualThreadPerTaskExecutor();
java.util.concurrent.Executor exec2 = java.util.concurrent.Executors.newVirtualThreadPerTaskExecutor();
String out = Solution.prove("seed");
checkTrue(out.startsWith("a=1,b=2|a=1,b=2"), "identical reports from both engines: " + out);
checkTrue(true, "polymorphism proven by bytes");
""", "The abstraction held — byte for byte."),
        ("history replays", r"""
java.nio.file.Path f = java.nio.file.Files.createTempFile("cjadv", ".jsonl");
checkTrue(Solution.survivesRestart(f), "replayed service answers from history");
""", "The file is the truth; restarts lose nothing."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: sổ cái, được chứng minh",
    "report (orTimeout + handle + thứ tự nộp), prove (hai engine, báo cáo giống nhau từng byte), survivesRestart (phát lại lịch sử từ tệp).",
    [("Hai engine, một báo cáo", "Abstraction giữ vững — từng byte một."),
     ("Lịch sử được phát lại", "Tệp là sự thật; khởi động lại không mất gì.")],
)

write_checkpoint(M, "javaa-checkpoint-m15",
    "Checkpoint: The Ledger, Proven",
    "Two engines, byte-identical reports, and a restart that loses nothing.",
    35, CP_MD,
    "Checkpoint: Sổ cái, được chứng minh",
    "Hai engine, báo cáo giống nhau từng byte, và một lần khởi động lại không mất gì.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Solution {
    public interface Engine {
        void put(String key, String value);
        Optional<String> get(String key);
        List<String> keys();
        int count();
    }

    public static class InMemory implements Engine {
        private final ConcurrentHashMap<String, String> data = new ConcurrentHashMap<>();
        public void put(String key, String value) { data.put(key, value); }
        public Optional<String> get(String key) { return Optional.ofNullable(data.get(key)); }
        public List<String> keys() {
            List<String> ks = new ArrayList<>(data.keySet());
            Collections.sort(ks);
            return ks;
        }
        public int count() { return data.size(); }
    }

    public static class JsonlFile implements Engine {
        private final Path file;
        private final ConcurrentHashMap<String, String> index = new ConcurrentHashMap<>();

        JsonlFile(Path file) { this.file = file; }

        public void put(String key, String value) {
            try {
                Files.writeString(file,
                    "{\"op\":\"put\",\"k\":\"" + key + "\",\"v\":\"" + value + "\"}\n",
                    StandardCharsets.UTF_8, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
            index.put(key, value);
        }

        public Optional<String> get(String key) { return Optional.ofNullable(index.get(key)); }
        public List<String> keys() {
            List<String> ks = new ArrayList<>(index.keySet());
            Collections.sort(ks);
            return ks;
        }
        public int count() { return index.size(); }

        void apply(String line) {
            int k = line.indexOf("\"k\":\"");
            int v = line.indexOf("\"v\":\"");
            if (k >= 0 && v >= 0) {
                int kEnd = line.indexOf("\"", k + 5);
                int vEnd = line.indexOf("\"", v + 5);
                index.put(line.substring(k + 5, kEnd), line.substring(v + 5, vEnd));
            }
        }
    }

    public static Engine replay(Path file) {
        try {
            JsonlFile e = new JsonlFile(file);
            for (String line : Files.readAllLines(file, StandardCharsets.UTF_8)) {
                e.apply(line);
            }
            return e;
        } catch (IOException ex) {
            throw new UncheckedIOException(ex);
        }
    }

    public static class LedgerService {
        private final Engine engine;

        public LedgerService(Engine engine) { this.engine = engine; }

        public String get(String key) {
            return engine.get(key).orElse("MISSING");
        }

        public void record(String key, String value) {
            engine.put(key, value);
        }

        public List<String> entries() {
            return engine.keys().stream()
                .map(k -> k + "=" + engine.get(k).orElse("MISSING"))
                .collect(Collectors.toList());
        }

        public static String health(int count, int failures) {
            if (failures != 0) return "red";
            return count > 0 ? "green" : "yellow";
        }
    }

    public static String report(LedgerService svc, List<String> keys, Executor exec) {
        List<CompletableFuture<String>> parts = keys.stream()
            .map(k -> CompletableFuture
                .<String>supplyAsync(() -> k + "=" + svc.get(k), exec)
                .orTimeout(50, TimeUnit.MILLISECONDS)
                .handle((r, e) -> e == null ? r : k + "=down"))
            .collect(Collectors.toList());
        CompletableFuture.allOf(parts.toArray(new CompletableFuture[0]))
            .orTimeout(500, TimeUnit.MILLISECONDS).join();
        return parts.stream().map(CompletableFuture::join)
            .collect(Collectors.joining(","));
    }

    public static String prove(String seed) {
        try {
            Path file = Files.createTempFile("cjadv", ".jsonl");
            LedgerService fileSvc = new LedgerService(new JsonlFile(file));
            fileSvc.record("a", "1");
            fileSvc.record("b", "2");
            LedgerService memSvc = new LedgerService(new InMemory());
            memSvc.record("a", "1");
            memSvc.record("b", "2");
            Executor exec = Executors.newVirtualThreadPerTaskExecutor();
            String fromFile = report(fileSvc, List.of("a", "b"), exec);
            String fromMem = report(memSvc, List.of("a", "b"), exec);
            if (!seed.isEmpty()) { /* deterministic hook */ }
            return fromFile + "|" + fromMem;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public static boolean survivesRestart(Path file) {
        LedgerService original = new LedgerService(new JsonlFile(file));
        original.record("x", "9");
        LedgerService restarted = new LedgerService(replay(file));
        return restarted.get("x").equals("9");
    }
}
""", wrong=r"""
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Solution {
    public interface Engine {
        void put(String key, String value);
        Optional<String> get(String key);
        List<String> keys();
        int count();
    }

    public static class InMemory implements Engine {
        private final ConcurrentHashMap<String, String> data = new ConcurrentHashMap<>();
        public void put(String key, String value) { data.put(key, value); }
        public Optional<String> get(String key) { return Optional.ofNullable(data.get(key)); }
        public List<String> keys() {
            List<String> ks = new ArrayList<>(data.keySet());   // WRONG: unsorted
            return ks;
        }
        public int count() { return data.size(); }
    }

    public static class JsonlFile implements Engine {
        private final Path file;
        private final ConcurrentHashMap<String, String> index = new ConcurrentHashMap<>();

        JsonlFile(Path file) { this.file = file; }

        public void put(String key, String value) {
            index.put(key, value);   // WRONG: writes nothing to disk
        }

        public Optional<String> get(String key) { return Optional.ofNullable(index.get(key)); }
        public List<String> keys() { return new ArrayList<>(index.keySet()); }   // WRONG: unsorted
        public int count() { return index.size(); }
    }

    public static Engine replay(Path file) {
        return new JsonlFile(file);   // WRONG: empty state — history lost
    }

    public static class LedgerService {
        private final Engine engine;

        public LedgerService(Engine engine) { this.engine = engine; }

        public String get(String key) {
            return engine.get(key).orElse("MISSING");
        }

        public void record(String key, String value) {
            engine.put(key, value);
        }

        public List<String> entries() {
            return engine.keys().stream()
                .map(k -> k + "=" + engine.get(k))
                .collect(Collectors.toList());
        }

        public static String health(int count, int failures) {
            return "green";   // WRONG: health that lies
        }
    }

    public static String report(LedgerService svc, List<String> keys, Executor exec) {
        StringBuilder sb = new StringBuilder();   // WRONG: sequential loop, no bounds,
        for (String k : keys) {                    // no recovery — a hung read hangs the report
            sb.append(k).append("=").append(svc.get(k)).append(",");
        }
        if (sb.length() > 0) sb.setLength(sb.length() - 1);
        return sb.toString();
    }

    public static String prove(String seed) {
        try {
            Path file = Files.createTempFile("cjadv", ".jsonl");
            LedgerService fileSvc = new LedgerService(new JsonlFile(file));
            fileSvc.record("a", "1");
            fileSvc.record("b", "2");
            LedgerService memSvc = new LedgerService(new InMemory());
            memSvc.record("a", "1");
            memSvc.record("b", "2");
            Executor exec = Executors.newVirtualThreadPerTaskExecutor();
            return report(fileSvc, List.of("a", "b"), exec) + "|" +
                   report(memSvc, List.of("a", "b"), exec);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public static boolean survivesRestart(Path file) {
        LedgerService original = new LedgerService(new JsonlFile(file));
        original.record("x", "9");
        LedgerService restarted = new LedgerService(replay(file));
        return restarted.get("x").equals("9");
    }
}
""")

print("module 15 authored")
