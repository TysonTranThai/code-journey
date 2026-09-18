#!/usr/bin/env python3
"""C# — Beginner — Module 6: csb-strings.

Strings as immutable objects you probe and rebuild: indexing/iteration,
the slicing-and-querying API surface, and char work including the escape
and numeric-conversion traps. House conventions: ISO boilerplate carries
usings, Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-strings"

write_module(
    M,
    "Strings and Characters",
    "Text is data: indexing and iterating strings, the core string API, and char-level work with its conversion traps.",
    "Chuỗi và ký tự",
    "Văn bản là dữ liệu: đánh chỉ số và duyệt chuỗi, bộ API chuỗi cốt lõi, và làm việc với char cùng các bẫy chuyển đổi.",
    ["csb-m6-index", "csb-m6-api", "csb-m6-char", "csb-checkpoint-m6"],
    ["csb-p6-strings"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m6-index",
    "Strings: indexing and immutability",
    "A string is an immutable sequence of chars — what that buys you, and how to walk it.",
    14,
    r"""
## Strings are sequences of char

```csharp
string lang = "C#";
char first = lang[0];      // 'C'
char last  = lang[^1];     // '#'  — ^1 is "one from the end"
int  len   = lang.Length;  // 2
```

Indexing starts at 0; `[i]` returns a `char` (single quotes: `'C'`), not a string. `lang[^1]` uses the **hat operator** — count from the end. An out-of-range index throws `IndexOutOfRangeException` immediately; there is no silent clamping.

`foreach (char c in text)` walks every character without an index — use it when you don't need the position; use a `for` loop when you do.

## Immutable: strings never change

```csharp
string name = "code";
name.ToUpper();        // produces "CODE" ... and throws it away
string upper = name.ToUpper();   // name is STILL "code"
```

Every string "modification" method (`ToUpper`, `Replace`, `Trim`, `Substring`, ...) **returns a new string** and leaves the original untouched. Forgetting to capture the result is the single most common string bug:

```csharp
line = line.Trim();    // correct: rebind the variable
```

Why immutable? One string object can be safely shared everywhere — no method can reach into your string and change it behind your back. The cost: heavy rebuild-in-a-loop code allocates a new string each pass (that's the `StringBuilder` discussion, later).

## Building strings: interpolation wins

```csharp
var user = "minh"; var score = 97;
Console.WriteLine($"{user} scored {score} points");     // interpolation
Console.WriteLine(user + " scored " + score + " points"); // concatenation
```

String interpolation (`$"..."`) reads in output order and converts each expression with its `ToString`. Prefer it to `+` chains — and note the `$` prefix is what enables the `{}` holes.
""",
    "Chuỗi: chỉ số và tính bất biến",
    "Một chuỗi là dãy char bất biến — điều đó mang lại gì, và cách đi qua nó.",
    r"""
## Chuỗi là dãy các char

```csharp
string lang = "C#";
char first = lang[0];      // 'C'
char last  = lang[^1];     // '#'  — ^1 là "tính từ cuối một"
int  len   = lang.Length;  // 2
```

Chỉ số bắt đầu từ 0; `[i]` trả về một `char` (nháy đơn: `'C'`), không phải string. `lang[^1]` dùng **toán tử mũ (^)** — đếm từ cuối. Chỉ số ngoài phạm vi ném `IndexOutOfRangeException` ngay lập tức; không có kẹp âm thầm.

`foreach (char c in text)` đi qua từng ký tự mà không cần chỉ số — dùng khi không cần vị trí; dùng `for` khi cần vị trí.

## Bất biến: chuỗi không bao giờ thay đổi

```csharp
string name = "code";
name.ToUpper();        // tạo ra "CODE" ... rồi vứt nó đi
string upper = name.ToUpper();   // name VẪN là "code"
```

Mọi phương thức "sửa" chuỗi (`ToUpper`, `Replace`, `Trim`, `Substring`, ...) **trả về một chuỗi mới** và giữ nguyên bản gốc. Quên gán lại kết quả là bug chuỗi phổ biến nhất:

```csharp
line = line.Trim();    // đúng: gán lại biến
```

Vì sao bất biến? Một đối tượng chuỗi có thể được chia sẻ an toàn ở mọi nơi — không phương thức nào chạm vào chuỗi của bạn và thay đổi nó sau lưng. Cái giá: code dựng chuỗi nặng trong vòng lặp cấp phát một chuỗi mới mỗi vòng (chuyện `StringBuilder`, sau này).

## Dựng chuỗi: interpolation thắng

```csharp
var user = "minh"; var score = 97;
Console.WriteLine($"{user} scored {score} points");     // interpolation
Console.WriteLine(user + " scored " + score + " points"); // nối chuỗi
```

String interpolation (`$"..."`) đọc theo thứ tự đầu ra và chuyển mỗi biểu thức bằng `ToString` của nó. Ưu tiên hơn chuỗi `+` — và nhớ tiền tố `$` là thứ bật các lỗ `{}`.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m6-api",
    "The string API you'll use daily",
    "Query, slice, split, and rejoin: the methods that cover most real text work.",
    15,
    r"""
## Asking questions

```csharp
string file = "report.PDF";
file.EndsWith(".pdf")              // false — case matters!
file.EndsWith(".pdf", StringComparison.OrdinalIgnoreCase)  // true
file.Contains("port")              // true
file.StartsWith("rep")             // true
string.Empty == file.Trim()        // is it blank?
```

String comparisons are **case-sensitive by default** — `"PDF"` does not end with `".pdf"`. For user-facing input, say what you mean with a `StringComparison` argument. Equality (`==` and `Equals`) compares *contents*, not references — strings are the reference type where `==` does what beginners expect.

## Slicing and transforming

```csharp
string s = "  Code Journey  ";
s.Trim()                       // "Code Journey"      — new string
s.Substring(5)                 // "Journey"           — from index 5 on
s.Substring(5, 3)              // "Jou"               — 3 chars from index 5
s.Replace(" ", "-")            // "  Code-Journey-  "
s.Trim().Replace(" ", "-")     // "Code-Journey"      — chained
```

`Substring(start)` takes everything from `start`; `Substring(start, length)` takes exactly `length` chars — and throws if the range leaves the string. `Replace` swaps **every** occurrence, not the first.

## Split and join

```csharp
string csv = "rice,beans,oil";
string[] items = csv.Split(',');          // ["rice", "beans", "oil"]
string re = string.Join(" | ", items);    // "rice | beans | oil"
```

`Split` cuts a string into an array at each separator; empty fields become empty strings, and you can pass `char[]` or `string[]` separators. `string.Join` is the inverse — glue an array (of strings) with a separator. Together they're the backbone of line- and record-based text processing (CSV-ish files, logs, user records).

## The number↔string boundary

```csharp
int n = 42;
string t = n.ToString();          // "42"
string f = n.ToString("D5");      // "00042" — format codes exist
int back = int.Parse("42");       // throws on garbage
bool ok  = int.TryParse("42", out int value);  // false + value=0 on garbage
```

`Parse` throws `FormatException` on bad input; `TryParse` reports success as a `bool` — remember it from Module 3, this is where it lives conceptually.
""",
    "Bộ API chuỗi dùng hằng ngày",
    "Hỏi, cắt, tách, và nối lại: những phương thức phủ phần lớn công việc văn bản thực tế.",
    r"""
## Đặt câu hỏi

```csharp
string file = "report.PDF";
file.EndsWith(".pdf")              // false — phân biệt hoa thường!
file.EndsWith(".pdf", StringComparison.OrdinalIgnoreCase)  // true
file.Contains("port")              // true
file.StartsWith("rep")             // true
string.Empty == file.Trim()        // có trống không?
```

So sánh chuỗi **phân biệt hoa thường theo mặc định** — `"PDF"` không kết thúc bằng `".pdf"`. Với input người dùng, hãy nói rõ ý bạn bằng đối số `StringComparison`. Phép bằng (`==` và `Equals`) so *nội dung*, không phải tham chiếu — string là kiểu tham chiếu mà `==` làm đúng điều người mới mong đợi.

## Cắt và biến đổi

```csharp
string s = "  Code Journey  ";
s.Trim()                       // "Code Journey"      — chuỗi mới
s.Substring(5)                 // "Journey"           — từ chỉ số 5 trở đi
s.Substring(5, 3)              // "Jou"               — 3 ký tự từ chỉ số 5
s.Replace(" ", "-")            // "  Code-Journey-  "
s.Trim().Replace(" ", "-")     // "Code-Journey"      — xích nhau
```

`Substring(start)` lấy mọi thứ từ `start`; `Substring(start, length)` lấy đúng `length` ký tự — và ném nếu khoảng vượt khỏi chuỗi. `Replace` thay **mọi** lần xuất hiện, không chỉ lần đầu.

## Split và join

```csharp
string csv = "rice,beans,oil";
string[] items = csv.Split(',');          // ["rice", "beans", "oil"]
string re = string.Join(" | ", items);    // "rice | beans | oil"
```

`Split` cắt một chuỗi thành mảng tại mỗi dấu phân cách; trường rỗng thành chuỗi rỗng, và bạn có thể truyền `char[]` hoặc `string[]` làm phân cách. `string.Join` là chiều ngược lại — dán một mảng (các chuỗi) bằng dấu phân cách. Cùng nhau, chúng là xương sống của xử lý văn bản theo dòng và bản ghi (tệp kiểu CSV, log, bản ghi người dùng).

## Biên giới số↔chuỗi

```csharp
int n = 42;
string t = n.ToString();          // "42"
string f = n.ToString("D5");      // "00042" — có các mã định dạng
int back = int.Parse("42");       // ném khi gặp rác
bool ok  = int.TryParse("42", out int value);  // false + value=0 khi gặp rác
```

`Parse` ném `FormatException` với input xấu; `TryParse` báo thành công bằng `bool` — bạn đã gặp nó ở Module 3, đây là nơi nó nằm về mặt khái niệm.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m6-char",
    "Working with char",
    "Single characters, their escape codes, and the classifier methods that power validators.",
    12,
    r"""
## char is a small integer

```csharp
char c = 'A';
Console.WriteLine((int)c);     // 65 — the code point
char next = (char)(c + 1);     // 'B'
```

A `char` holds a UTF-16 code unit — for everyday ASCII work, think "a small number with a costume." Casting to `int` reveals the code; arithmetic shifts the code. That's how case conversion and letter checks work underneath.

## Escapes you'll actually use

```csharp
"a\tb"      // tab
"line\n"    // newline
"quote: \"" // a literal double quote
"backslash: \\" 
'a'         // char literal: single quotes, no escape needed
```

Inside a `char` literal, `'\n'` and `'\t'` work the same way; `'\\''` escapes a single quote. (`"\u00e9"` gives 'é' by code point — worth knowing it exists.)

## Classifiers: the validator toolkit

```csharp
char.IsDigit(c)      // '0'..'9'
char.IsLetter(c)     // letters, including accented ones
char.IsLetterOrDigit(c)
char.IsWhiteSpace(c) // spaces, tabs, newlines
char.IsUpper(c) / char.IsLower(c)
char.ToLower(c) / char.ToUpper(c)
```

These return `bool` and take a `char`. A username validator, a digit counter, a "does this line start with whitespace" check — all one-liners over these classifiers plus a loop. Prefer `char.IsDigit` over `'0' <= c && c <= '9'`: it says what it does, and it's correct for more than ASCII.
""",
    "Làm việc với char",
    "Ký tự đơn, các mã escape, và những phương thức phân loại làm nên bộ kiểm tra hợp lệ.",
    r"""
## char là một số nguyên nhỏ

```csharp
char c = 'A';
Console.WriteLine((int)c);     // 65 — mã ký tự
char next = (char)(c + 1);     // 'B'
```

Một `char` chứa một đơn vị mã UTF-16 — với công việc ASCII thường ngày, hãy nghĩ "một số nhỏ khoác trang phục." Ép kiểu sang `int` lộ ra mã; phép toán dịch mã. Đó là cách đổi chữ hoa/thường và kiểm tra chữ cái hoạt động bên dưới.

## Các escape bạn sẽ thực sự dùng

```csharp
"a\tb"      // tab
"line\n"    // xuống dòng
"quote: \"" // dấu nháy kép literal
"backslash: \\" 
'a'         // char literal: nháy đơn, không cần escape
```

Bên trong một literal `char`, `'\n'` và `'\t'` hoạt động như vậy; `'\'''` escape một nháy đơn. (`"\u00e9"` cho 'é' theo mã ký tự — biết nó tồn tại là được.)

## Bộ phân loại: hộp công cụ của trình kiểm tra hợp lệ

```csharp
char.IsDigit(c)      // '0'..'9'
char.IsLetter(c)     // chữ cái, kể cả có dấu
char.IsLetterOrDigit(c)
char.IsWhiteSpace(c) // khoảng trắng, tab, xuống dòng
char.IsUpper(c) / char.IsLower(c)
char.ToLower(c) / char.ToUpper(c)
```

Chúng trả `bool` và nhận một `char`. Trình kiểm tra tên người dùng, bộ đếm chữ số, câu hỏi "dòng này có bắt đầu bằng khoảng trắng không" — tất cả là một dòng lặp với các bộ phân loại này. Ưu tiên `char.IsDigit` hơn `'0' <= c && c <= '9'`: nó nói rõ việc nó làm, và đúng cho nhiều hơn ASCII.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p6-strings",
    "Text workshop",
    "Immutability discipline, case-aware searching, record splitting, and char-level validation.",
    "Xưởng văn bản",
    "Kỷ luật bất biến, tìm kiếm có phân biệt hoa thường, tách bản ghi, và kiểm tra hợp lệ mức char.",
    "csb-m6-char",
    38,
    "beginner",
    [
        challenge(
            "csb-p6-normalize",
            "Name normalizer",
            "Implement `static string Normalize(string name)` — trim surrounding whitespace, then collapse every run of internal whitespace to a single space. `\"  Minh   Van  \"` becomes `\"Minh Van\"`. Null yields `\"\"`.",
            CS_PRELUDE,
            [
                (
                    "basic",
                    "Cj.Eq(Solution.Normalize(\"  Minh   Van  \"), \"Minh Van\", \"spaces\");\nCj.Eq(Solution.Normalize(\"clean\"), \"clean\", \"untouched\");",
                    "Trim outside; internal runs — not single spaces — collapse to one.",
                ),
                (
                    "whitespace-kinds",
                    "Cj.Eq(Solution.Normalize(\"a\\tb\\nc\"), \"a b c\", \"tabs/newlines count\");\nCj.Eq(Solution.Normalize(null), \"\", \"null\");\nCj.Eq(Solution.Normalize(\"   \"), \"\", \"blank\");",
                    "Whitespace is more than the space character; blank input collapses to empty.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p6-contains",
            "Case-insensitive extension check",
            "Implement `static bool HasExtension(string fileName, string ext)` — true when `fileName` ends with `ext` ignoring letter case. `HasExtension(\"photo.JPG\", \".jpg\")` is true. Null on either side yields false.",
            CS_PRELUDE,
            [
                (
                    "case",
                    "Cj.True(Solution.HasExtension(\"photo.JPG\", \".jpg\"), \"JPG vs jpg\");\nCj.False(Solution.HasExtension(\"photo.png\", \".jpg\"), \"wrong ext\");",
                    "The default comparison would fail the first — say OrdinalIgnoreCase.",
                ),
                (
                    "edges",
                    "Cj.True(Solution.HasExtension(\"archive.tar.gz\", \".gz\"), \"multi-dot\");\nCj.False(Solution.HasExtension(null, \".jpg\"), \"null file\");\nCj.False(Solution.HasExtension(\"a.png\", null), \"null ext\");",
                    "Dots inside the name are fine; nulls are false, not crashes.",
                ),
            ],
            level="imitation",
        ),
        challenge(
            "csb-p6-csv",
            "CSV field picker",
            "Implement `static string Field(string line, int index)` — return the `index`-th comma-separated field of `line` (0-based), or `\"\"` when the index is out of range. `Field(\"rice,beans,,oil\", 2)` is `\"\"` — empty fields are real fields.",
            CS_PRELUDE,
            [
                (
                    "basic",
                    "Cj.Eq(Solution.Field(\"rice,beans,oil\", 1), \"beans\", \"middle\");\nCj.Eq(Solution.Field(\"rice\", 0), \"rice\", \"single\");",
                    "Split, index, done — but mind the no-separator case.",
                ),
                (
                    "empty-fields",
                    "Cj.Eq(Solution.Field(\"rice,beans,,oil\", 2), \"\", \"empty field\");\nCj.Eq(Solution.Field(\"a,,b\", 5), \"\", \"out of range\");\nCj.Eq(Solution.Field(\"a,,b\", -1), \"\", \"negative\");",
                    "An empty field is still a field; out-of-range indices yield \"\" — no throw.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p6-digit-count",
            "Digit counter",
            "Implement `static int CountDigits(string s)` — how many characters are decimal digits (use `char.IsDigit`, so `'٥'`-style Unicode digits count too — any `char.IsDigit` true). Null or empty yields 0.",
            CS_PRELUDE,
            [
                (
                    "basic",
                    "Cj.Eq(Solution.CountDigits(\"abc123\"), 3, \"mixed\");\nCj.Eq(Solution.CountDigits(\"no digits!\"), 0, \"none\");\nCj.Eq(Solution.CountDigits(\"007\"), 3, \"leading zeros\");",
                    "Plain ASCII digits first.",
                ),
                (
                    "unicode",
                    "Cj.Eq(Solution.CountDigits(\"1\\u06652\"), 3, \"Arabic-Indic digit counts\");\nCj.Eq(Solution.CountDigits(\"\"), 0, \"empty\");\nCj.Eq(Solution.CountDigits(null), 0, \"null\");",
                    "char.IsDigit (not '0'<=c&&c<='9') is what makes the Unicode digit count — that's the lesson.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p6-normalize": vi_challenge(
            "Chuẩn hóa tên",
            "Hiện thực `static string Normalize(string name)` — trim khoảng trắng hai đầu, rồi gộp mọi dải khoảng trắng ở giữa thành một dấu cách. `\"  Minh   Van  \"` thành `\"Minh Van\"`. Null cho `\"\"`.",
            [
                ("basic", "Trim bên ngoài; các dải ở giữa — không phải dấu cách đơn — gộp thành một."),
                ("whitespace-kinds", "Khoảng trắng không chỉ là dấu cách; input trống gộp thành rỗng."),
            ],
        ),
        "csb-p6-contains": vi_challenge(
            "Kiểm tra phần mở rộng không phân biệt hoa thường",
            "Hiện thực `static bool HasExtension(string fileName, string ext)` — true khi `fileName` kết thúc bằng `ext` bất chấp chữ hoa/thường. `HasExtension(\"photo.JPG\", \".jpg\")` là true. Null một bên nào đó cho false.",
            [
                ("case", "So sánh mặc định sẽ trượt lần đầu — hãy nói OrdinalIgnoreCase."),
                ("edges", "Dấu chấm trong tên là chuyện bình thường; null là false, không phải crash."),
            ],
        ),
        "csb-p6-csv": vi_challenge(
            "Lấy trường CSV",
            "Hiện thực `static string Field(string line, int index)` — trả trường thứ `index` (đếm từ 0) phân tách bởi dấu phẩy của `line`, hoặc `\"\"` khi chỉ số vượt phạm vi. `Field(\"rice,beans,,oil\", 2)` là `\"\"` — trường rỗng là trường thật.",
            [
                ("basic", "Split, lấy chỉ số, xong — nhưng chú ý trường hợp không có dấu phân cách."),
                ("empty-fields", "Trường rỗng vẫn là trường; chỉ số ngoài phạm vi cho \"\" — không ném."),
            ],
        ),
        "csb-p6-digit-count": vi_challenge(
            "Bộ đếm chữ số",
            "Hiện thực `static int CountDigits(string s)` — bao nhiêu ký tự là chữ số thập phân (dùng `char.IsDigit`, nên chữ số kiểu Unicode cũng được đếm). Null hoặc rỗng cho 0.",
            [
                ("basic", "Chữ số ASCII đơn giản trước."),
                ("unicode", "char.IsDigit (không phải '0'<=c&&c<='9') là thứ làm nên việc đếm chữ số Unicode — đó chính là bài học."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p6-normalize",
            'public class Solution\n{\n    public static string Normalize(string name)\n    {\n        if (name == null) return "";\n        var parts = name.Split((char[])null, StringSplitOptions.RemoveEmptyEntries);\n        return string.Join(" ", parts);\n    }\n}\n',
            'public class Solution\n{\n    public static string Normalize(string name)\n    {\n        if (name == null) return "";\n        // near-miss: trims but never collapses internal runs\n        return name.Trim();\n    }\n}\n',
        ),
        (
            "csb-p6-contains",
            'public class Solution\n{\n    public static bool HasExtension(string fileName, string ext)\n    {\n        if (fileName == null || ext == null) return false;\n        return fileName.EndsWith(ext, StringComparison.OrdinalIgnoreCase);\n    }\n}\n',
            'public class Solution\n{\n    public static bool HasExtension(string fileName, string ext)\n    {\n        if (fileName == null || ext == null) return false;\n        // near-miss: case-sensitive default — "photo.JPG" fails ".jpg"\n        return fileName.EndsWith(ext);\n    }\n}\n',
        ),
        (
            "csb-p6-csv",
            'public class Solution\n{\n    public static string Field(string line, int index)\n    {\n        if (line == null || index < 0) return "";\n        string[] parts = line.Split(\',\');\n        return index < parts.Length ? parts[index] : "";\n    }\n}\n',
            'public class Solution\n{\n    public static string Field(string line, int index)\n    {\n        if (line == null || index < 0) return "";\n        string[] parts = line.Split(\',\');\n        // near-miss: index == Length would throw, but so does forgetting\n        // that empty fields exist — this skips empties via RemoveEmptyEntries\n        string[] compact = line.Split(new[] { \',\' }, StringSplitOptions.RemoveEmptyEntries);\n        return index < compact.Length ? compact[index] : "";\n    }\n}\n',
        ),
        (
            "csb-p6-digit-count",
            'public class Solution\n{\n    public static int CountDigits(string s)\n    {\n        if (string.IsNullOrEmpty(s)) return 0;\n        int count = 0;\n        foreach (char c in s)\n            if (char.IsDigit(c)) count++;\n        return count;\n    }\n}\n',
            'public class Solution\n{\n    public static int CountDigits(string s)\n    {\n        if (string.IsNullOrEmpty(s)) return 0;\n        int count = 0;\n        foreach (char c in s)\n        {\n            // near-miss: ASCII-range check misses Unicode digits like \'\\u0665\'\n            if (c >= \'0\' && c <= \'9\') count++;\n        }\n        return count;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m6",
    "Checkpoint — Strings",
    "Initials and a password strength probe: slicing, classification, and case discipline in one program.",
    20,
    r"""
## Checkpoint: identity utilities

**Task:** implement two methods:

1. `static string Initials(string fullName)` — the first letter of each whitespace-separated word, uppercased, joined. `"nguyen van an"` → `"NVA"`. Null/empty/blank yields `""`.
2. `static int PasswordScore(string pw)` — score: 1 if length ≥ 8, plus 1 if it contains any digit, plus 1 if it contains any uppercase letter. Null or empty scores 0. So `"Abcdefgh1"` scores 3; `"abcdefgh"` scores 1.
""",
    "Checkpoint — Chuỗi",
    "Viết tắt và thăm dò độ mạnh mật khẩu: cắt, phân loại, và kỷ luật hoa thường trong một chương trình.",
    r"""
## Checkpoint: tiện ích định danh

**Nhiệm vụ:** hiện thực hai phương thức:

1. `static string Initials(string fullName)` — chữ cái đầu của mỗi từ phân tách bằng khoảng trắng, in hoa, nối lại. `"nguyen van an"` → `"NVA"`. Null/rỗng/toàn khoảng trắng cho `""`.
2. `static int PasswordScore(string pw)` — điểm: 1 nếu độ dài ≥ 8, cộng 1 nếu chứa chữ số nào đó, cộng 1 nếu chứa chữ in hoa nào đó. Null hoặc rỗng được 0 điểm. Vậy `"Abcdefgh1"` được 3; `"abcdefgh"` được 1.
""",
    challenge(
        "csb-checkpoint-m6-task",
        "Identity utilities",
        "Implement `Initials` and `PasswordScore` as described. Initials uppercases each word's first letter and joins them; the password score has exactly three independent criteria.",
        CS_PRELUDE,
        [
            (
                "initials",
                'Cj.Eq(Solution.Initials("nguyen van an"), "NVA", "three words");\nCj.Eq(Solution.Initials("ada"), "A", "one word");\nCj.Eq(Solution.Initials(""), "", "empty");\nCj.Eq(Solution.Initials(null), "", "null");\nCj.Eq(Solution.Initials("  "), "", "blank");',
                "Lowercase input must come out uppercase; blank inputs yield the empty string.",
            ),
            (
                "password",
                'Cj.Eq(Solution.PasswordScore("Abcdefgh1"), 3, "all three");\nCj.Eq(Solution.PasswordScore("abcdefgh"), 1, "length only");\nCj.Eq(Solution.PasswordScore("abcdefgh1"), 2, "length+digit");\nCj.Eq(Solution.PasswordScore("Ab1"), 2, "short but digit+upper still score");\nCj.Eq(Solution.PasswordScore(""), 0, "empty");\nCj.Eq(Solution.PasswordScore(null), 0, "null");',
                "Careful: the \"Ab1\" assertion expects 2 — it fails the length rule but earns digit and uppercase points.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Tiện ích định danh",
        "Hiện thực `Initials` và `PasswordScore` như mô tả. Initials in hóa chữ cái đầu mỗi từ rồi nối lại; điểm mật khẩu có đúng ba tiêu chí độc lập.",
        [
            ("initials", "Input thường phải ra in hoa; input trống cho chuỗi rỗng."),
            ("password", "Kỳ vọng \"Ab1\" là 2: trượt luật độ dài nhưng vẫn được điểm chữ số và chữ in hoa."),
        ],
    ),
    solution='public class Solution\n{\n    public static string Initials(string fullName)\n    {\n        if (string.IsNullOrWhiteSpace(fullName)) return "";\n        var parts = fullName.Split((char[])null, StringSplitOptions.RemoveEmptyEntries);\n        var sb = new System.Text.StringBuilder();\n        foreach (string word in parts)\n            sb.Append(char.ToUpperInvariant(word[0]));\n        return sb.ToString();\n    }\n\n    public static int PasswordScore(string pw)\n    {\n        if (string.IsNullOrEmpty(pw)) return 0;\n        int score = pw.Length >= 8 ? 1 : 0;\n        bool digit = false, upper = false;\n        foreach (char c in pw)\n        {\n            if (char.IsDigit(c)) digit = true;\n            if (char.IsUpper(c)) upper = true;\n        }\n        if (digit) score++;\n        if (upper) score++;\n        return score;\n    }\n}\n',
    wrong='public class Solution\n{\n    public static string Initials(string fullName)\n    {\n        if (string.IsNullOrWhiteSpace(fullName)) return "";\n        var parts = fullName.Split((char[])null, StringSplitOptions.RemoveEmptyEntries);\n        var sb = new System.Text.StringBuilder();\n        foreach (string word in parts)\n            // near-miss: takes the word as-is — no uppercase, so "nguyen..."\n            // yields "nva" and the case test fails\n            sb.Append(word[0]);\n        return sb.ToString();\n    }\n\n    public static int PasswordScore(string pw)\n    {\n        if (string.IsNullOrEmpty(pw)) return 0;\n        int score = pw.Length >= 8 ? 1 : 0;\n        // near-miss: only checks the FIRST character for digit/uppercase —\n        // "abcdefgh1" scores 1 instead of 2\n        if (char.IsDigit(pw[0])) score++;\n        if (char.IsUpper(pw[0])) score++;\n        return score;\n    }\n}\n',
)

print("module 6 authored")
