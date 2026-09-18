#!/usr/bin/env python3
"""C# — Beginner — Module 14: csb-files.

Files as durable state: Path/File/Directory, write/read/append, the
using-disposal contract, and a line-based persistence format. Verified
in-sandbox: file I/O works under the hardened container. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-files"

write_module(
    M,
    "Files and Persistence",
    "Program state that survives the process: Path, File, and Directory — plus the disposal rule that keeps handles honest.",
    "Tệp và Lưu trữ",
    "Trạng thái chương trình sống sót qua tiến trình: Path, File, và Directory — cộng luật-dispose giữ cho handle trung thực.",
    ["csb-m14-path-file", "csb-m14-read-write", "csb-m14-persistence", "csb-checkpoint-m14"],
    ["csb-p14-files"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m14-path-file",
    "Path, File, Directory",
    "Path manipulates names, File/Directory manipulate reality — and combining them badly is a classic bug.",
    12,
    r"""
## Three static classes

- **`Path`** — string surgery on file names: `Combine`, `GetFileName`, `GetExtension`. It touches no disk.
- **`File`** — one-shot operations: `WriteAllText`, `ReadAllText`, `AppendAllText`, `Exists`, `Delete`.
- **`Directory`** — folders: `CreateDirectory`, `GetFiles`, `Exists`.

```csharp
string path = Path.Combine("/tmp", "cj", "notes.txt");
Directory.CreateDirectory(Path.GetDirectoryName(path));   // /tmp/cj
File.WriteAllText(path, "hello\n");
string again = File.ReadAllText(path);
```

## The rules that prevent bugs

`Path.Combine("a", "/b")` — an absolute second argument **replaces** the first; that's defined behavior, not a bug, but it surprises people. And `File.WriteAllText` **overwrites** without asking: a save-one-line bug can destroy yesterday's data. Check `File.Exists` when history matters, and prefer `AppendAllText` for logs.
""",
    "Path, File, Directory",
    "Path làm phẫu thuật trên tên, File/Directory tác động vào hiện thực — và kết hợp sai là bug kinh điển.",
    r"""
## Ba lớp tĩnh

- **`Path`** — phẫu thuật chuỗi trên tên tệp: `Combine`, `GetFileName`, `GetExtension`. Nó không chạm vào đĩa.
- **`File`** — thao tác một-lần: `WriteAllText`, `ReadAllText`, `AppendAllText`, `Exists`, `Delete`.
- **`Directory`** — thư mục: `CreateDirectory`, `GetFiles`, `Exists`.

```csharp
string path = Path.Combine("/tmp", "cj", "notes.txt");
Directory.CreateDirectory(Path.GetDirectoryName(path));   // /tmp/cj
File.WriteAllText(path, "hello\n");
string again = File.ReadAllText(path);
```

## Các luật chống bug

`Path.Combine("a", "/b")` — đối số thứ hai tuyệt đối sẽ **thay thế** đối số đầu; đó là hành vi được định nghĩa, không phải bug, nhưng gây bất ngờ. Và `File.WriteAllText` **ghi đè** không hỏi: một bug lưu-một-dòng có thể phá dữ liệu hôm qua. Hãy kiểm tra `File.Exists` khi lịch sử quan trọng, và ưu tiên `AppendAllText` cho nhật ký.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m14-read-write",
    "Reading and writing line by line",
    "Whole-file helpers are for small data; readers/writers stream it — and both need disposal.",
    13,
    r"""
## Whole-file convenience

```csharp
string all = File.ReadAllText(path);          // one big string
string[] lines = File.ReadAllLines(path);     // split for you
File.WriteAllLines(path, new[] { "a", "b" }); // joins with newlines
```

`ReadAllLines` also strips line-ending differences: Windows CRLF or Unix LF, you get clean lines. For config files and small datasets, these helpers are the right tool.

## Streaming with using

For anything potentially large — or when you process as you read — stream:

```csharp
using (var reader = new StreamReader(path))
{
    string line;
    while ((line = reader.ReadLine()) != null)
    {
        Console.WriteLine(line);
    }
}
```

`StreamReader.ReadLine()` returns the next line or `null` at end-of-file. The `using` block guarantees the file handle closes even if the loop body throws — an open handle leaks a resource the OS grants in limited supply.
""",
    "Đọc và ghi theo dòng",
    "Helper cả-tệp cho dữ liệu nhỏ; reader/writer cho dữ liệu dòng chảy — và cả hai đều cần dispose.",
    r"""
## Tiện lợi cả-tệp

```csharp
string all = File.ReadAllText(path);          // một chuỗi lớn
string[] lines = File.ReadAllLines(path);     // tách sẵn cho bạn
File.WriteAllLines(path, new[] { "a", "b" }); // nối bằng ký tự xuống dòng
```

`ReadAllLines` cũng chuẩn hóa khác biệt line-ending: CRLF Windows hay LF Unix, bạn nhận được các dòng sạch. Với tệp cấu hình và bộ dữ liệu nhỏ, những helper này là đúng công cụ.

## Streaming với using

Với dữ liệu có thể lớn — hoặc khi xử lý trong lúc đọc — hãy stream:

```csharp
using (var reader = new StreamReader(path))
{
    string line;
    while ((line = reader.ReadLine()) != null)
    {
        Console.WriteLine(line);
    }
}
```

`StreamReader.ReadLine()` trả dòng kế tiếp hoặc `null` khi hết tệp. Khối `using` bảo đảm handle tệp được đóng ngay cả khi thân vòng lặp ném ngoại lệ — handle hở làm rò rỉ tài nguyên mà hệ điều hành cấp có hạn.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m14-persistence",
    "A persistence format of your own",
    "One record per line with an escaping rule is a database you fully understand — and can test.",
    12,
    r"""
## The format

The simplest honest persistence format is **line-oriented**: one record per line, fields separated by a delimiter chosen to never appear in the data:

```csharp
// save: id|name|score
File.WriteAllLines(path, players.Select(p => $"{p.Id}|{p.Name}|{p.Score}"));
```

Loading is the mirror:

```csharp
foreach (string line in File.ReadAllLines(path))
{
    string[] parts = line.Split('|');
    players.Add(new Player(int.Parse(parts[0]), parts[1], int.Parse(parts[2])));
}
```

## Design honestly, test both directions

Choose `|` (or tab) over `,` when your data is free text — commas live inside prose. Decide the corrupt-line policy **before** it happens: skip-and-count, or fail loudly? Round-trip testing is the non-negotiable part: **save, load, assert equal**. If a format can't survive its own save/load cycle, nothing built on it can.
""",
    "Định dạng lưu trữ của riêng bạn",
    "Một bản ghi mỗi dòng với luật escape là một cơ sở dữ liệu bạn hoàn toàn hiểu — và kiểm chứng được.",
    r"""
## Định dạng

Định dạng lưu trữ trung thực đơn giản nhất là **theo dòng**: một bản ghi mỗi dòng, các trường ngăn bởi ký tự được chọn sao cho không bao giờ xuất hiện trong dữ liệu:

```csharp
// lưu: id|name|score
File.WriteAllLines(path, players.Select(p => $"{p.Id}|{p.Name}|{p.Score}"));
```

Tải là hình ảnh phản chiếu:

```csharp
foreach (string line in File.ReadAllLines(path))
{
    string[] parts = line.Split('|');
    players.Add(new Player(int.Parse(parts[0]), parts[1], int.Parse(parts[2])));
}
```

## Thiết kế trung thực, kiểm thử hai chiều

Chọn `|` (hoặc tab) thay vì `,` khi dữ liệu là văn bản tự do — dấu phẩy sống trong lời văn. Quyết định chính sách dòng-hỏng **trước khi** nó xảy ra: bỏ-qua-và-đếm, hay báo lỗi to? Kiểm thử khứ-hồi là phần không thể thương lượng: **lưu, tải, khẳng định bằng nhau**. Nếu một định dạng không sống sót qua chu kỳ lưu/tải của chính nó, thứ gì dựng trên nó cũng vậy.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p14-files",
    "File I/O workout",
    "Writers, readers, appends, and a round-trip store — durability under discriminating tests.",
    "Luyện tập File I/O",
    "Bộ ghi, bộ đọc, nối-dòng, và kho khứ-hồi — độ bền dưới các bài kiểm tra phân biệt.",
    "csb-m14-persistence",
    40,
    "beginner",
    [
        challenge(
            "csb-p14-writeread",
            "Write, read, and overwrite",
            "Implement `static void WriteNote(string path, string note)` (create parent directory if missing, overwrite the file with the note text) and `static string ReadNote(string path)` (return the file's text; `FileNotFoundException` when the file doesn't exist).",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var dir = Path.Combine(Path.GetTempPath(), \"cj-p14a\", Guid.NewGuid().ToString());\nvar path = Path.Combine(dir, \"note.txt\");\nSolution.WriteNote(path, \"hello files\");\nCj.Eq(Solution.ReadNote(path), \"hello files\", \"round trip\");\nSolution.WriteNote(path, \"second\");\nCj.Eq(Solution.ReadNote(path), \"second\", \"overwrite replaces\");",
                    "Write must create missing directories and replace existing content.",
                ),
                (
                    "missing",
                    "var dir = Path.Combine(Path.GetTempPath(), \"cj-p14b\", Guid.NewGuid().ToString());\nDirectory.CreateDirectory(dir);\nvar path = Path.Combine(dir, \"ghost.txt\");\nbool t = false;\ntry { Solution.ReadNote(path); } catch (FileNotFoundException) { t = true; }\nCj.True(t, \"missing file throws, no silent null\");",
                    "Reading what was never written is an exceptional condition.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p14-loglines",
            "Append-only log",
            "Implement `static void AppendLine(string path, string line)` (appends one line, creating the file if needed) and `static string[] ReadLines(string path)` (all lines; empty array for a missing file, never null).",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var path = Path.Combine(Path.GetTempPath(), \"cj-p14c\", Guid.NewGuid().ToString() + \".log\");\nSolution.AppendLine(path, \"first\");\nSolution.AppendLine(path, \"second\");\nCj.Eq(string.Join(\"|\", Solution.ReadLines(path)), \"first|second\", \"append order kept\");\nCj.Eq(Solution.ReadLines(path).Length, 2, \"two entries\");",
                    "Each append lands after the last; order survives.",
                ),
                (
                    "missing",
                    "var path = Path.Combine(Path.GetTempPath(), \"cj-p14d\", Guid.NewGuid().ToString() + \".log\");\nvar lines = Solution.ReadLines(path);\nCj.False(lines == null, \"missing file yields empty, not null\");\nCj.Eq(lines.Length, 0, \"zero lines\");\nSolution.AppendLine(path, \"seed\");\nCj.Eq(Solution.ReadLines(path)[0], \"seed\", \"append creates the file\");",
                    "Read-before-write must not crash the log viewer; append bootstraps the file.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p14-csv",
            "Delimiter CSV",
            "Implement `static void SaveScores(string path, List<(int Id, string Name, int Score)> rows)` writing one `id|name|score` line per row, and `static List<(int Id, string Name, int Score)> LoadScores(string path)` parsing them back (missing file → empty list).",
            CS_PRELUDE,
            [
                (
                    "roundtrip",
                    "var path = Path.Combine(Path.GetTempPath(), \"cj-p14e\", Guid.NewGuid().ToString() + \".csv\");\nvar rows = new List<(int, string, int)> { (1, \"An\", 90), (2, \"Binh\", 75) };\nSolution.SaveScores(path, rows);\nvar back = Solution.LoadScores(path);\nCj.Eq(back.Count, 2, \"two rows\");\nCj.Eq(back[0].Item1, 1, \"id\");\nCj.Eq(back[0].Item2, \"An\", \"name\");\nCj.Eq(back[1].Item3, 75, \"score\");",
                    "Save then load must reproduce the data — the round-trip contract.",
                ),
                (
                    "empty",
                    "var path = Path.Combine(Path.GetTempPath(), \"cj-p14f\", Guid.NewGuid().ToString() + \".csv\");\nCj.Eq(Solution.LoadScores(path).Count, 0, \"missing file -> empty\");\nSolution.SaveScores(path, new List<(int, string, int)>());\nCj.Eq(Solution.LoadScores(path).Count, 0, \"empty save -> empty load\");",
                    "Both empty cases normalize to an empty list.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p14-corrupt",
            "Corrupt-line policy",
            "Implement `static (int Loaded, int Skipped) LoadScoresLenient(string path, List<(int Id, string Name, int Score)> into)`: parses each `id|name|score` line; well-formed lines load, malformed lines (wrong field count, non-numeric id/score) are skipped and counted. Returns both counts.",
            CS_PRELUDE,
            [
                (
                    "mixed",
                    "var path = Path.Combine(Path.GetTempPath(), \"cj-p14g\", Guid.NewGuid().ToString() + \".csv\");\nDirectory.CreateDirectory(Path.GetDirectoryName(path));\nFile.WriteAllLines(path, new[] { \"1|An|90\", \"garbage\", \"2|Binh|abc\", \"3|Chi|70\" });\nvar into = new List<(int, string, int)>();\nvar r = Solution.LoadScoresLenient(path, into);\nCj.Eq(r.Loaded, 2, \"two good rows\");\nCj.Eq(r.Skipped, 2, \"two bad rows\");\nCj.Eq(into[0].Item2, \"An\", \"first good row intact\");",
                    "Good rows survive bad neighbors — skip, don't crash, don't lose data.",
                ),
                (
                    "edge",
                    "var path = Path.Combine(Path.GetTempPath(), \"cj-p14h\", Guid.NewGuid().ToString() + \".csv\");\nDirectory.CreateDirectory(Path.GetDirectoryName(path));\nFile.WriteAllText(path, \"\");\nvar into = new List<(int, string, int)>();\nvar r = Solution.LoadScoresLenient(path, into);\nCj.Eq(r.Loaded, 0, \"empty file loads nothing\");\nCj.Eq(r.Skipped, 0, \"and skips nothing — blank is not corrupt\");",
                    "An empty file is not corruption; the counts must say exactly that.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p14-writeread": vi_challenge(
            "Ghi, đọc, và ghi đè",
            "Hiện thực `static void WriteNote(string path, string note)` (tạo thư mục cha nếu thiếu, ghi đè tệp bằng nội dung note) và `static string ReadNote(string path)` (trả nội dung tệp; ném `FileNotFoundException` khi tệp không tồn tại).",
            [
                ("normal", "Write phải tạo thư mục còn thiếu và thay thế nội dung sẵn có."),
                ("missing", "Đọc thứ chưa từng được viết là điều kiện ngoại lệ."),
            ],
        ),
        "csb-p14-loglines": vi_challenge(
            "Nhật ký chỉ-nối-thêm",
            "Hiện thực `static void AppendLine(string path, string line)` (nối một dòng, tự tạo tệp nếu cần) và `static string[] ReadLines(string path)` (mọi dòng; mảng rỗng cho tệp thiếu, không bao giờ null).",
            [
                ("normal", "Mỗi lần nối nằm sau lần cuối; thứ tự sống sót."),
                ("missing", "Đọc-trước-khi-ghi không được làm sập trình xem log; nối sẽ tự dựng tệp."),
            ],
        ),
        "csb-p14-csv": vi_challenge(
            "CSV có ký tự phân cách",
            "Hiện thực `static void SaveScores(string path, List<(int Id, string Name, int Score)> rows)` ghi mỗi dòng `id|name|score`, và `static List<(int Id, string Name, int Score)> LoadScores(string path)` phân tích ngược lại (tệp thiếu → danh sách rỗng).",
            [
                ("roundtrip", "Lưu rồi tải phải tái tạo dữ liệu — hợp đồng khứ-hồi."),
                ("empty", "Cả hai trường hợp rỗng chuẩn hóa thành danh sách rỗng."),
            ],
        ),
        "csb-p14-corrupt": vi_challenge(
            "Chính sách dòng-hỏng",
            "Hiện thực `static (int Loaded, int Skipped) LoadScoresLenient(string path, List<(int Id, string Name, int Score)> into)`: phân tích từng dòng `id|name|score`; dòng hợp lệ được nạp, dòng dị dạng (sai số trường, id/score không phải số) bị bỏ qua và đếm. Trả cả hai con số.",
            [
                ("mixed", "Dòng tốt sống sót cạnh dòng xấu — bỏ qua, không sập, không mất dữ liệu."),
                ("edge", "Tệp rỗng không phải hỏng dữ liệu; hai con số phải nói đúng điều đó."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p14-writeread",
            'public class Solution\n{\n    public static void WriteNote(string path, string note)\n    {\n        string dir = Path.GetDirectoryName(path);\n        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);\n        File.WriteAllText(path, note);\n    }\n    public static string ReadNote(string path)\n    {\n        return File.ReadAllText(path);\n    }\n}\n',
            'public class Solution\n{\n    public static void WriteNote(string path, string note)\n    {\n        string dir = Path.GetDirectoryName(path);\n        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);\n        // near-miss: appends instead of overwriting — "second write" tests\n        // see concatenated text instead of replacement\n        File.AppendAllText(path, note);\n    }\n    public static string ReadNote(string path)\n    {\n        return File.ReadAllText(path);\n    }\n}\n',
        ),
        (
            "csb-p14-loglines",
            'public class Solution\n{\n    public static void AppendLine(string path, string line)\n    {\n        string dir = Path.GetDirectoryName(path);\n        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);\n        File.AppendAllText(path, line + Environment.NewLine);\n    }\n    public static string[] ReadLines(string path)\n    {\n        if (!File.Exists(path)) return new string[0];\n        return File.ReadAllLines(path);\n    }\n}\n',
            'public class Solution\n{\n    public static void AppendLine(string path, string line)\n    {\n        string dir = Path.GetDirectoryName(path);\n        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);\n        // near-miss: no newline separator — appends glue lines together and\n        // ReadLines sees "firstsecond" as one entry\n        File.AppendAllText(path, line);\n    }\n    public static string[] ReadLines(string path)\n    {\n        if (!File.Exists(path)) return new string[0];\n        return File.ReadAllLines(path);\n    }\n}\n',
        ),
        (
            "csb-p14-csv",
            'public class Solution\n{\n    public static void SaveScores(string path, List<(int Id, string Name, int Score)> rows)\n    {\n        string dir = Path.GetDirectoryName(path);\n        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);\n        File.WriteAllLines(path, rows.Select(r => $"{r.Id}|{r.Name}|{r.Score}").ToArray());\n    }\n    public static List<(int Id, string Name, int Score)> LoadScores(string path)\n    {\n        var result = new List<(int, string, int)>();\n        if (!File.Exists(path)) return result;\n        foreach (string line in File.ReadAllLines(path))\n        {\n            string[] p = line.Split(\'|\');\n            result.Add((int.Parse(p[0]), p[1], int.Parse(p[2])));\n        }\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static void SaveScores(string path, List<(int Id, string Name, int Score)> rows)\n    {\n        string dir = Path.GetDirectoryName(path);\n        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);\n        File.WriteAllLines(path, rows.Select(r => $"{r.Id}|{r.Name}|{r.Score}").ToArray());\n    }\n    public static List<(int Id, string Name, int Score)> LoadScores(string path)\n    {\n        var result = new List<(int, string, int)>();\n        if (!File.Exists(path)) return result;\n        foreach (string line in File.ReadAllLines(path))\n        {\n            string[] p = line.Split(\'|\');\n            // near-miss: swaps name and score on parse — ids load, scores\n            // land in the name slot, and round-trip tests expose it\n            result.Add((int.Parse(p[0]), p[2], int.Parse(p[1])));\n        }\n        return result;\n    }\n}\n',
        ),
        (
            "csb-p14-corrupt",
            'public class Solution\n{\n    public static (int Loaded, int Skipped) LoadScoresLenient(string path, List<(int Id, string Name, int Score)> into)\n    {\n        int loaded = 0, skipped = 0;\n        if (!File.Exists(path)) return (0, 0);\n        foreach (string line in File.ReadAllLines(path))\n        {\n            string[] p = line.Split(\'|\');\n            if (p.Length != 3 || !int.TryParse(p[0], out int id) || !int.TryParse(p[2], out int score))\n            {\n                skipped++;\n                continue;\n            }\n            into.Add((id, p[1], score));\n            loaded++;\n        }\n        return (loaded, skipped);\n    }\n}\n',
            'public class Solution\n{\n    public static (int Loaded, int Skipped) LoadScoresLenient(string path, List<(int Id, string Name, int Score)> into)\n    {\n        int loaded = 0, skipped = 0;\n        if (!File.Exists(path)) return (0, 0);\n        foreach (string line in File.ReadAllLines(path))\n        {\n            string[] p = line.Split(\'|\');\n            // near-miss: checks the field count but not the numbers —\n            // int.Parse on "abc" throws and kills the whole load\n            if (p.Length != 3)\n            {\n                skipped++;\n                continue;\n            }\n            into.Add((int.Parse(p[0]), p[1], int.Parse(p[2])));\n            loaded++;\n        }\n        return (loaded, skipped);\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m14",
    "Checkpoint — Files",
    "A notes store: append, load with a lenient corrupt-line policy, and search — durable across process restarts.",
    20,
    r"""
## Checkpoint: the notes store

**Task:** implement in `Solution` a tiny notes store over `id|title|body` lines:

1. `static int SaveNote(string path, int nextId, string title, string body)` — appends `nextId|title|body` as one line and returns `nextId + 1` (the caller's running id).
2. `static List<(int Id, string Title, string Body)> LoadNotes(string path)` — parses the file; malformed lines skipped; missing file → empty list.
3. `static List<(int Id, string Title, string Body)> Search(List<(int Id, string Title, string Body)> notes, string term)` — notes whose title OR body contains `term` (case-insensitive), preserving order.
""",
    "Checkpoint — Tệp",
    "Kho ghi chú: nối-thêm, tải với chính sách dòng-hỏng khoan dung, và tìm kiếm — bền vững qua các lần khởi động lại.",
    r"""
## Checkpoint: kho ghi chú

**Nhiệm vụ:** hiện thực trong `Solution` một kho ghi chú nhỏ trên các dòng `id|title|body`:

1. `static int SaveNote(string path, int nextId, string title, string body)` — nối `nextId|title|body` thành một dòng và trả `nextId + 1` (id chạy dần của người gọi).
2. `static List<(int Id, string Title, string Body)> LoadNotes(string path)` — phân tích tệp; bỏ qua dòng dị dạng; tệp thiếu → danh sách rỗng.
3. `static List<(int Id, string Title, string Body)> Search(List<(int Id, string Title, string Body)> notes, string term)` — các ghi chú có title HOẶC body chứa `term` (không phân biệt chữ hoa/thường), giữ nguyên thứ tự.
""",
    challenge(
        "csb-checkpoint-m14-task",
        "NotesStore",
        "Implement `SaveNote`, `LoadNotes`, and `Search` — one line per note, lenient loading, case-insensitive search over both fields.",
        CS_PRELUDE,
        [
            (
                "save-load",
                "var path = Path.Combine(Path.GetTempPath(), \"cj-cp14\", Guid.NewGuid().ToString() + \".notes\");\nint next = Solution.SaveNote(path, 1, \"Shopping\", \"buy oat milk\");\nnext = Solution.SaveNote(path, next, \"Ideas\", \"learn C# generics\");\nCj.Eq(next, 3, \"id advanced twice\");\nvar notes = Solution.LoadNotes(path);\nCj.Eq(notes.Count, 2, \"two notes\");\nCj.Eq(notes[0].Item2, \"Shopping\", \"first title\");\nCj.Eq(notes[1].Item3, \"learn C# generics\", \"second body\");",
                "Append-save and the running id, then a faithful reload.",
            ),
            (
                "search-and-skip",
                "var path = Path.Combine(Path.GetTempPath(), \"cj-cp14b\", Guid.NewGuid().ToString() + \".notes\");\nDirectory.CreateDirectory(Path.GetDirectoryName(path));\nFile.WriteAllLines(path, new[] { \"1|Shopping|buy oat milk\", \"bad line\", \"2|Ideas|OAT milk forever\" });\nvar notes = Solution.LoadNotes(path);\nCj.Eq(notes.Count, 2, \"corrupt line skipped\");\nvar hits = Solution.Search(notes, \"oat\");\nCj.Eq(hits.Count, 2, \"case-insensitive over title AND body\");\nvar none = Solution.Search(notes, \"zzz\");\nCj.Eq(none.Count, 0, \"no hits, empty list\");",
                "Lenient load plus search that checks both fields without case sensitivity.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "NotesStore",
        "Hiện thực `SaveNote`, `LoadNotes`, và `Search` — một dòng mỗi ghi chú, tải khoan dung, tìm kiếm không phân biệt chữ trên cả hai trường.",
        [
            ("save-load", "Nối-thêm và id chạy dần, rồi tải lại trung thực."),
            ("search-and-skip", "Tải khoan dung cộng tìm kiếm trên cả hai trường, không phân biệt chữ hoa/thường."),
        ],
    ),
    solution='public class Solution\n{\n    public static int SaveNote(string path, int nextId, string title, string body)\n    {\n        string dir = Path.GetDirectoryName(path);\n        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);\n        File.AppendAllText(path, $"{nextId}|{title}|{body}" + Environment.NewLine);\n        return nextId + 1;\n    }\n    public static List<(int Id, string Title, string Body)> LoadNotes(string path)\n    {\n        var result = new List<(int, string, string)>();\n        if (!File.Exists(path)) return new List<(int, string, string)>();\n        foreach (string line in File.ReadAllLines(path))\n        {\n            string[] p = line.Split(\'|\');\n            if (p.Length != 3 || !int.TryParse(p[0], out int id)) continue;\n            result.Add((id, p[1], p[2]));\n        }\n        return result;\n    }\n    public static List<(int Id, string Title, string Body)> Search(List<(int Id, string Title, string Body)> notes, string term)\n    {\n        var result = new List<(int, string, string)>();\n        foreach (var n in notes)\n        {\n            if (n.Item2.IndexOf(term, StringComparison.OrdinalIgnoreCase) >= 0\n                || n.Item3.IndexOf(term, StringComparison.OrdinalIgnoreCase) >= 0)\n                result.Add(n);\n        }\n        return result;\n    }\n}\n',
    wrong='public class Solution\n{\n    public static int SaveNote(string path, int nextId, string title, string body)\n    {\n        string dir = Path.GetDirectoryName(path);\n        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);\n        File.AppendAllText(path, $"{nextId}|{title}|{body}" + Environment.NewLine);\n        return nextId + 1;\n    }\n    public static List<(int Id, string Title, string Body)> LoadNotes(string path)\n    {\n        var result = new List<(int, string, string)>();\n        if (!File.Exists(path)) return new List<(int, string, string)>();\n        foreach (string line in File.ReadAllLines(path))\n        {\n            string[] p = line.Split(\'|\');\n            if (p.Length != 3 || !int.TryParse(p[0], out int id)) continue;\n            result.Add((id, p[1], p[2]));\n        }\n        return result;\n    }\n    public static List<(int Id, string Title, string Body)> Search(List<(int Id, string Title, string Body)> notes, string term)\n    {\n        var result = new List<(int, string, string)>();\n        foreach (var n in notes)\n        {\n            // near-miss: case-SENSITIVE search — "oat" misses "OAT milk"\n            if (n.Item2.Contains(term) || n.Item3.Contains(term))\n                result.Add(n);\n        }\n        return result;\n    }\n}\n',
)

print("module 14 authored")
