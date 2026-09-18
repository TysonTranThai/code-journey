#!/usr/bin/env python3
"""Java — Advanced — Module 10: javaa-files-nio.

Real file I/O in the sandbox's writable /tmp: Path arithmetic, walking and
globbing trees, atomic REPLACE_EXISTING moves, explicit charsets, and the
checkpoint — a JSONL journal with append/rotate/replay semantics. House
conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-files-nio"

L_PATH_EN = """
`Path` is an *immutable description* of a file location — not a handle to an
open file, not a promise the file exists.

```java
Path base = Path.of("/tmp", "cjadv");
Path p = base.resolve("logs/app.log");   // /tmp/cjadv/logs/app.log
p.getParent();  p.getFileName();         // navigation
base.relativize(p);                      // logs/app.log
```

`resolve` joins; `relativize` is the inverse. The sandbox gives each run a
writable `/tmp` — every file operation in this course targets
`Files.createTempDirectory("cjadv")` so runs never collide and never touch
anything outside their sandbox.

Existence is a *state*, not a property: between `Files.exists(p)` and
`Files.createFile(p)` another actor can create the file. The NIO answer is
atomic operations with semantics, not check-then-act:
`Files.createFile(p)` throws if it exists (race-safe creation);
`Files.move(src, dst, REPLACE_EXISTING, ATOMIC_MOVE)` either swaps completely
or throws — no half-copied files ever observable.
"""
L_PATH_VI = """
`Path` là *mô tả bất biến* về vị trí tệp — không phải handle mở tệp, không
phải lời hứa tệp tồn tại.

```java
Path base = Path.of("/tmp", "cjadv");
Path p = base.resolve("logs/app.log");   // /tmp/cjadv/logs/app.log
p.getParent();  p.getFileName();         // điều hướng
base.relativize(p);                      // logs/app.log
```

`resolve` nối; `relativize` là phép nghịch đảo. Sandbox cho mỗi lần chạy một
`/tmp` ghi được — mọi thao tác tệp trong khóa học nhắm vào
`Files.createTempDirectory("cjadv")` để các lần chạy không bao giờ va chạm và
không đụng gì bên ngoài sandbox của chúng.

Tồn tại là một *trạng thái*, không phải thuộc tính: giữa `Files.exists(p)` và
`Files.createFile(p)`, một tác nhân khác có thể tạo tệp. Câu trả lời của NIO
là các phép toán nguyên tử có ngữ nghĩa, không phải check-then-act:
`Files.createFile(p)` ném nếu đã có (tạo an toànrace);
`Files.move(src, dst, REPLACE_EXISTING, ATOMIC_MOVE)` hoặc đổi xong trọn vẹn
hoặc ném — không bao giờ quan sát được tệp chép dở.
"""

L_WALK_EN = """
Walking a tree is a pipeline, not a loop with recursion homework:

```java
try (Stream<Path> paths = Files.walk(root, 3)) {
    List<Path> logs = paths
        .filter(p -> p.toString().endsWith(".log"))
        .collect(toList());
}
```

`Files.walk` lazily streams the tree (depth-bounded); `Files.find` folds a
predicate in; `Files.list` covers a single directory. Glob matching is
built in — `FileSystems.getDefault().getPathMatcher("glob:**/*.{log,tmp}")` —
and must be applied against *both* the path and its filename form depending
on the pattern's shape (`dir/**` matches path-syntax; `*.log` matches
filenames). The stream is LAZY and backed by the directory iterator: closing
it (try-with-resources) releases the handle — leaking it leaks file
descriptors.
"""
L_WALK_VI = """
Duyệt cây là một pipeline, không phải bài tập đệ quy:

```java
try (Stream<Path> paths = Files.walk(root, 3)) {
    List<Path> logs = paths
        .filter(p -> p.toString().endsWith(".log"))
        .collect(toList());
}
```

`Files.walk` stream lười toàn cây (giới hạn độ sâu); `Files.find` gộp sẵn vị
từ; `Files.list` cho một thư mục duy nhất. Khớp glob có sẵn —
`FileSystems.getDefault().getPathMatcher("glob:**/*.{log,tmp}")` — và phải áp
dụng vào *cả* path lẫn dạng filename của nó tùy hình dạng pattern
(`dir/**` khớp cú pháp path; `*.log` khớp filename). Stream là LAZY và được
đỡ bởi iterator thư mục: đóng nó (try-with-resources) trả handle — rò rỉ nó
là rò rỉ file descriptor.
"""

L_JOURNAL_EN = """
An append-only journal is the honest way to persist events: writes are cheap
appends, corruption cannot destroy history (only tail it), and replay
reconstructs state deterministically.

```java
Files.writeString(file, line + "\\n",
    StandardCharsets.UTF_8, CREATE, APPEND);
for (String line : Files.readAllLines(file, StandardCharsets.UTF_8)) { ... }
```

Three disciplines: (1) **explicit charset everywhere** — UTF-8 in and out;
the platform-default overloads are deprecated precisely because "default"
differs between machines. (2) **one record per line** (JSONL): the newline is
the frame, so a truncated final line is detectable and skippable. (3) rotation
by policy — when the file exceeds a bound, `Files.move` it aside atomically
and keep appending to a fresh file. Kafka, databases, and every log shipper
in existence run on this shape.
"""
L_JOURNAL_VI = """
Journal chỉ-ghi-thêm là cách trung thực để lưu sự kiện: ghi là append rẻ,
hỏng hóc không thể phá lịch sử (chỉ cắt đuôi), và replay tái dựng trạng thái
một cách tất định.

```java
Files.writeString(file, line + "\\n",
    StandardCharsets.UTF_8, CREATE, APPEND);
for (String line : Files.readAllLines(file, StandardCharsets.UTF_8)) { ... }
```

Ba kỷ luật: (1) **charset tường minh mọi nơi** — UTF-8 vào ra; các overload
mặc định nền đã bị đánh dấu deprecated đúng vì "mặc định" khác nhau giữa các
máy. (2) **một bản ghi mỗi dòng** (JSONL): newline là khung, nên dòng cuối bị
cắt là phát hiện được và bỏ qua được. (3) xoay theo chính sách — khi tệp vượt
giới hạn, `Files.move` nó đi một cách nguyên tử rồi tiếp tục ghi vào tệp mới.
Kafka, database, và mọi log shipper trên đời chạy trên hình dạng này.
"""

write_module(
    M, "Files & NIO",
    "Path arithmetic, tree walking with globs, atomic moves, explicit charsets, and a JSONL journal.",
    "Tệp & NIO",
    "Phép toán Path, duyệt cây với glob, move nguyên tử, charset tường minh, và journal JSONL.",
    ["javaa-path-semantics", "javaa-tree-walking", "javaa-jsonl-journal"],
    ["javaa-p10-files"],
)

write_lesson(M, "javaa-path-semantics",
    "Path semantics and atomic operations",
    "Immutable paths, resolve/relativize, and operations that carry their guarantees in their signature.",
    15, L_PATH_EN,
    "Ngữ nghĩa Path và phép toán nguyên tử",
    "Path bất biến, resolve/relativize, và các phép toán mang cam kết ngay trong chữ ký.",
    L_PATH_VI)

write_lesson(M, "javaa-tree-walking",
    "Walking trees with globs",
    "Lazy streams over directory trees, glob matchers, and descriptor hygiene.",
    15, L_WALK_EN,
    "Duyệt cây với glob",
    "Stream lười trên cây thư mục, glob matcher, và vệ sinh descriptor.",
    L_WALK_VI)

write_lesson(M, "javaa-jsonl-journal",
    "The append-only journal",
    "JSONL framing, explicit charsets, and rotation by policy.",
    16, L_JOURNAL_EN,
    "Journal chỉ ghi thêm",
    "Đóng khung JSONL, charset tường minh, và xoay theo chính sách.",
    L_JOURNAL_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_PATH = challenge(
    "javaa-p10-path",
    "Path arithmetic, executed",
    "1. `static Path buildLogPath(Path base)` — return `base.resolve(\"logs\").resolve(\"app.log\")`.\n"
    "2. `static String relativeShape(Path base, Path child)` — return\n"
    "`base.relativize(child).toString()`.\n"
    "3. `static int nameCount(Path p)` — p.getNameCount().\n"
    "4. `static boolean atomicSwap(Path src, Path dst)` — write \"new\" to src, then\n"
    "`Files.move(src, dst, REPLACE_EXISTING)`; return true iff dst now contains \"new\"\n"
    "and src no longer exists. (Create dst with old content \"old\" first.)",
    P_BOILER,
    [
        ("resolve joins, relativize inverts", r"""
java.nio.file.Path base = java.nio.file.Path.of("root", "proj");
checkEq(Solution.buildLogPath(base).toString(), "root/proj/logs/app.log", "resolve chains");
checkEq(Solution.relativeShape(base, base.resolve("a").resolve("b")), "a/b", "relativize");
checkEq(Solution.nameCount(java.nio.file.Path.of("a", "b", "c")), 3, "three names");
""", "Pure path algebra."),
        ("atomic move replaces wholesale", r"""
java.nio.file.Path dir = java.nio.file.Files.createTempDirectory("cjadv");
checkTrue(Solution.atomicSwap(dir.resolve("s"), dir.resolve("d")), "dst has new content, src gone");
""", "No half-states observable."),
    ],
    level="guided",
)
CH_PATH_VI = vi_challenge(
    "Phép toán Path, chạy thật",
    "buildLogPath/relativeShape/nameCount/atomicSwap: đại số path thuần và move thay thế trọn vẹn.",
    [("Resolve nối, relativize đảo", "Đại số path thuần túy."),
     ("Move nguyên tử thay thế toàn phần", "Không quan sát được trạng thái nửa vời.")],
)

CH_WALK = challenge(
    "javaa-p10-walk",
    "Walk, match, clean up",
    "1. `static List<String> findLogs(Path root)` — walk the tree depth 3, collect the\n"
    "FILE NAMES (not full paths) of every regular file ending in .log, SORTED\n"
    "alphabetically. Use try-with-resources on the stream.\n"
    "2. `static long totalBytes(Path root)` — sum file sizes of regular files at ANY\n"
    "depth (Files.size; skip directories).\n"
    "3. `static boolean globMatches(String pattern, Path candidate)` — use\n"
    "`FileSystems.getDefault().getPathMatcher(\"glob:\" + pattern)` and\n"
    "`matcher.matches(candidate)`.",
    P_BOILER,
    [
        ("tree walked, names collected", r"""
java.nio.file.Path root = java.nio.file.Files.createTempDirectory("cjadv");
java.nio.file.Files.writeString(root.resolve("a.log"), "x");
java.nio.file.Path sub = root.resolve("sub");
java.nio.file.Files.createDirectories(sub);
java.nio.file.Files.writeString(sub.resolve("b.log"), "yy");
java.nio.file.Files.writeString(sub.resolve("note.txt"), "z");
checkEq(Solution.findLogs(root), java.util.List.of("a.log", "b.log"), "both logs, sorted, no txt");
checkEq(Solution.totalBytes(root), 4L, "1 + 2 + 1 bytes");
""", "Depth does not hide files; extensions filter."),
        ("glob semantics", r"""
checkTrue(Solution.globMatches("*.log", java.nio.file.Path.of("a.log")), "filename glob");
checkTrue(Solution.globMatches("**/*.log", java.nio.file.Path.of("x", "y", "a.log")), "path glob");
checkTrue(!Solution.globMatches("*.log", java.nio.file.Path.of("a.txt")), "txt rejected");
""", "Glob shape matches target shape."),
    ],
    level="independent",
)
CH_WALK_VI = vi_challenge(
    "Duyệt, khớp, dọn dẹp",
    "findLogs/totalBytes/globMatches: độ sâu không giấu tệp, phần mở rộng lọc, glob khớp theo hình dạng.",
    [("Duyệt cây, thu tên", "Cả hai log, có sắp xếp, không txt."),
     ("Ngữ nghĩa glob", "Hình dạng glob khớp hình dạng mục tiêu.")],
)

write_practice(M, "javaa-p10-files",
    "File I/O drills",
    "Path algebra, lazy tree streams, and byte accounting — all against real temp files.",
    "Bài tập I/O tệp",
    "Đại số Path, stream cây lười, và kế toán byte — tất cả trên tệp tạm thật.",
    "javaa-jsonl-journal", 55, "advanced",
    [CH_PATH, CH_WALK],
    {"javaa-p10-path": CH_PATH_VI, "javaa-p10-walk": CH_WALK_VI},
    solutions=[
        ("javaa-p10-path", r"""
import java.nio.file.*;

public class Solution {
    public static Path buildLogPath(Path base) {
        return base.resolve("logs").resolve("app.log");
    }

    public static String relativeShape(Path base, Path child) {
        return base.relativize(child).toString();
    }

    public static int nameCount(Path p) {
        return p.getNameCount();
    }

    public static boolean atomicSwap(Path src, Path dst) throws Exception {
        Files.writeString(dst, "old");
        Files.writeString(src, "new");
        Files.move(src, dst, StandardCopyOption.REPLACE_EXISTING);
        return Files.readString(dst).equals("new") && !Files.exists(src);
    }
}
""", r"""
import java.nio.file.*;

public class Solution {
    public static Path buildLogPath(Path base) {
        return Path.of(base + "/logs/app.log");   // WRONG: string concat — breaks on separators
    }

    public static String relativeShape(Path base, Path child) {
        return child.toString();                   // WRONG: absolute shape, not relative
    }

    public static int nameCount(Path p) {
        return p.toString().length();              // WRONG: not a name count
    }

    public static boolean atomicSwap(Path src, Path dst) throws Exception {
        Files.copy(src, dst);                      // WRONG: copy (src survives, no replace, no atomicity)
        return Files.exists(dst);
    }
}
"""),
        ("javaa-p10-walk", r"""
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static List<String> findLogs(Path root) throws Exception {
        try (Stream<Path> paths = Files.walk(root, 3)) {
            return paths
                .filter(Files::isRegularFile)
                .map(p -> p.getFileName().toString())
                .filter(n -> n.endsWith(".log"))
                .sorted()
                .collect(Collectors.toList());
        }
    }

    public static long totalBytes(Path root) throws Exception {
        try (Stream<Path> paths = Files.walk(root)) {
            return paths
                .filter(Files::isRegularFile)
                .mapToLong(p -> {
                    try { return Files.size(p); }
                    catch (Exception e) { return 0L; }
                })
                .sum();
        }
    }

    public static boolean globMatches(String pattern, Path candidate) {
        return FileSystems.getDefault().getPathMatcher("glob:" + pattern)
            .matches(candidate);
    }
}
""", r"""
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

public class Solution {
    public static List<String> findLogs(Path root) throws Exception {
        Stream<Path> paths = Files.walk(root, 3);        // WRONG: stream never closed (descriptor leak)
        return paths
            .map(p -> p.toString())                       // WRONG: full paths, not file names
            .filter(p -> p.contains(".log"))
            .collect(Collectors.toList());                // WRONG: unsorted, no depth/regular filter
    }

    public static long totalBytes(Path root) throws Exception {
        return 0;                                         // WRONG: claims files are free
    }

    public static boolean globMatches(String pattern, Path candidate) {
        return candidate.toString().contains(pattern.replace("*", ""));  // WRONG: substring, not glob
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the JSONL journal

Append events, rotate by size, replay deterministically, and survive a
truncated tail — the exact contract of every production log before it was a
product.
"""

CP_CH = challenge(
    "javaa-checkpoint-m10-task",
    "Checkpoint: append, rotate, replay",
    "Inside Solution, implement the journal over a temp directory you create in each call:\n"
    "1. `static Path append(Path file, String event)` — appends `event + \"\\n\"` in UTF-8\n"
    "with CREATE + APPEND; returns the file.\n"
    "2. `static List<String> replay(Path file)` — returns every complete line (a\n"
    "TRUNCATED final line — one lacking its newline — must be dropped; use\n"
    "Files.readString and split on \"\\n\" carefully, or readAllLines and drop a final\n"
    "fragment you detect by re-reading raw bytes).\n"
    "3. `static Path rotate(Path file, int maxLines)` — if the file holds more than\n"
    "maxLines complete lines, move it to a sibling named by appending \".1\"\n"
    "(file.1) atomically, and leave a fresh empty file at the original path; return\n"
    "the ARCHIVE path (or the original if no rotation happened).\n"
    "4. `static int countEvents(Path file)` — number of complete lines.",
    P_BOILER,
    [
        ("append and replay", r"""
java.nio.file.Path f = java.nio.file.Files.createTempFile("cjadv", ".jsonl");
Solution.append(f, "{\"e\":1}");
Solution.append(f, "{\"e\":2}");
checkEq(Solution.replay(f), java.util.List.of("{\"e\":1}", "{\"e\":2}"), "both events");
checkEq(Solution.countEvents(f), 2, "two complete lines");
""", "Appends frame on newlines."),
        ("truncated tail is dropped", r"""
java.nio.file.Path f = java.nio.file.Files.createTempFile("cjadv", ".jsonl");
java.nio.file.Files.writeString(f, "{\"e\":1}\n{\"trun");
checkEq(Solution.replay(f), java.util.List.of("{\"e\":1}"), "fragment dropped");
checkEq(Solution.countEvents(f), 1, "only complete lines count");
""", "A torn tail never becomes an event."),
        ("rotation by policy", r"""
java.nio.file.Path f = java.nio.file.Files.createTempFile("cjadv", ".jsonl");
Solution.append(f, "a"); Solution.append(f, "b"); Solution.append(f, "c");
java.nio.file.Path arch = Solution.rotate(f, 2);
checkEq(Solution.countEvents(arch), 3, "archive holds the history");
checkEq(Solution.countEvents(f), 0, "live file fresh");
""", "History moved aside atomically; appends continue fresh."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: ghi thêm, xoay, phát lại",
    "append (UTF-8, CREATE+APPEND), replay bỏ đuôi bị cắt, rotate chuyển lịch sử sang .1 nguyên tử, countEvents đếm dòng hoàn chỉnh.",
    [("Ghi thêm và phát lại", "Append đóng khung bằng newline."),
     ("Đuôi bị cắt bị bỏ", "Đuôi rách không bao giờ thành sự kiện."),
     ("Xoay theo chính sách", "Lịch sử được chuyển đi nguyên tử; ghi tiếp vào tệp mới.")],
)

write_checkpoint(M, "javaa-checkpoint-m10",
    "Checkpoint: The JSONL Journal",
    "Append-only history, torn-tail tolerance, and atomic rotation.",
    28, CP_MD,
    "Checkpoint: Journal JSONL",
    "Lịch sử chỉ ghi thêm, chịu đựng đuôi rách, và xoay nguyên tử.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Solution {
    public static Path append(Path file, String event) throws Exception {
        Files.writeString(file, event + "\n", StandardCharsets.UTF_8,
            StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        return file;
    }

    public static List<String> replay(Path file) throws Exception {
        String raw = Files.readString(file, StandardCharsets.UTF_8);
        if (raw.isEmpty()) return List.of();
        boolean torn = !raw.endsWith("\n");
        String[] lines = raw.split("\n", -1);
        List<String> out = new ArrayList<>();
        int limit = lines.length - (torn ? 1 : 0) - (raw.endsWith("\n") && lines.length > 0 && lines[lines.length - 1].isEmpty() ? 1 : 0);
        for (int i = 0; i < limit; i++) {
            if (!lines[i].isEmpty()) out.add(lines[i]);
        }
        return out;
    }

    public static int countEvents(Path file) throws Exception {
        return replay(file).size();
    }

    public static Path rotate(Path file, int maxLines) throws Exception {
        if (countEvents(file) <= maxLines) return file;
        Path archive = file.resolveSibling(file.getFileName().toString() + ".1");
        Files.move(file, archive, StandardCopyOption.REPLACE_EXISTING,
            StandardCopyOption.ATOMIC_MOVE);
        Files.createFile(file);
        return archive;
    }
}
""", wrong=r"""
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Solution {
    public static Path append(Path file, String event) throws Exception {
        Files.writeString(file, event + "\n", StandardCharsets.UTF_8,
            CREATE, APPEND);
        return file;
    }

    public static List<String> replay(Path file) throws Exception {
        String raw = Files.readString(file, StandardCharsets.UTF_8);
        if (raw.isEmpty()) return List.of();
        return new ArrayList<>(List.of(raw.split("\n")));   // WRONG: torn tail becomes an "event"
    }

    public static int countEvents(Path file) throws Exception {
        return replay(file).size();
    }

    public static Path rotate(Path file, int maxLines) throws Exception {
        if (countEvents(file) <= maxLines) return file;
        Path archive = file.resolveSibling(file.getFileName().toString() + ".1");
        Files.write(archive, Files.readAllBytes(file));   // WRONG: copy, then delete —
        Files.delete(file);                                // a non-atomic window where history exists twice or not at all
        Files.createFile(file);
        return archive;
    }
}
""")

print("module 10 authored")
