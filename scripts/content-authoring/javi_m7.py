#!/usr/bin/env python3
"""Java — Intermediate — Module 7: java-io-formats.

NIO.2 concepts, and hand-rolled CSV/JSON handling (no external deps — the
sandbox is honest about that). File content grading uses the established
string-content contract: lessons and challenges treat file text as
parameters, so tests stay deterministic. House conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-io-formats"

# ── lesson 7.1 — NIO.2 model ────────────────────────────────────────────────
L_NIO_EN = r"""
## NIO.2: Path, Files, and the byte/char divide

`java.nio.file` separates *where* (Path) from *what you do* (Files):

```java
Path p = Path.of("data", "2026", "sales.csv");
Files.exists(p);          // test
Files.createDirectories(p.getParent());   // mkdir -p equivalent
Files.size(p);            // bytes
Files.readAllLines(p);    // small text files (whole file in memory)
Files.lines(p);           // lazy Stream<String> — use for big files
Files.writeString(p, text);
Files.readString(p);
```

Encoding is not optional: bytes → chars needs a charset.
`Files.newBufferedReader(p, StandardCharsets.UTF_8)` — always name it;
the platform-default charset is a portability bug.

Memory discipline: `readAllLines` loads everything; `Files.lines` streams
lazily and must be closed (use try-with-resources) or the file handle
leaks.
"""

L_NIO_VI = r"""
## NIO.2: Path, Files, và ranh giới byte/char

`java.nio.file` tách *ở đâu* (Path) khỏi *làm gì* (Files):

```java
Path p = Path.of("data", "2026", "sales.csv");
Files.exists(p);          // kiểm tra
Files.createDirectories(p.getParent());   // tương đương mkdir -p
Files.size(p);            // byte
Files.readAllLines(p);    // file text nhỏ (cả file trong bộ nhớ)
Files.lines(p);           // Stream<String> lười — dùng cho file lớn
Files.writeString(p, text);
Files.readString(p);
```

Encoding không phải tùy chọn: byte → char cần charset.
`Files.newBufferedReader(p, StandardCharsets.UTF_8)` — luôn chỉ đích danh;
charset mặc định của nền tảng là một bug tính di động.

Kỷ niệm bộ nhớ: `readAllLines` nạp hết; `Files.lines` stream lười và phải
đóng (dùng try-with-resources) nếu không sẽ rò file handle.
"""

# ── lesson 7.2 — CSV by hand ────────────────────────────────────────────────
L_CSV_EN = r"""
## CSV: parsing rules that bite

Real CSV (RFC 4180) has three rules beginners miss:

1. **Quoted fields** — `"hello, world"` is ONE field containing a comma.
2. **Escaped quotes** — `""` inside quotes is a literal `"`.
3. **Newlines in quotes** — a row can span lines.

A split(",") parser fails all three:

```java
// naive — breaks on quoted commas
String[] fields = line.split(",");

// character scanner — the honest parser
List<String> parseRow(String line) {
    List<String> out = new ArrayList<>();
    StringBuilder cur = new StringBuilder();
    boolean inQuotes = false;
    for (int i = 0; i < line.length(); i++) {
        char c = line.charAt(i);
        if (inQuotes) {
            if (c == '"') {
                if (i + 1 < line.length() && line.charAt(i + 1) == '"') { cur.append('"'); i++; }
                else inQuotes = false;
            } else cur.append(c);
        } else if (c == '"') inQuotes = true;
        else if (c == ',') { out.add(cur.toString()); cur.setLength(0); }
        else cur.append(c);
    }
    out.add(cur.toString());
    return out;
}
```

The scanner handles rules 1–2; full rule 3 needs row-merging across
lines — beyond today's scope, but you now know why libraries exist.
"""

L_CSV_VI = r"""
## CSV: những quy tắc cắn người

CSV thật (RFC 4180) có ba quy tắc người mới hay bỏ sót:

1. **Field trong ngoặc kép** — `"hello, world"` là MỘT field chứa dấu phẩy.
2. **Dấu ngoặc kép được escape** — `""` trong ngoặc là một dấu `"` nghĩa chữ.
3. **Xuống dòng trong ngoặc** — một row có thể trải nhiều dòng.

Parser split(",") vi phạm cả ba:

```java
// ngây thơ — vỡ với dấu phẩy trong ngoặc
String[] fields = line.split(",");

// quét ký tự — parser trung thực
List<String> parseRow(String line) {
    List<String> out = new ArrayList<>();
    StringBuilder cur = new StringBuilder();
    boolean inQuotes = false;
    for (int i = 0; i < line.length(); i++) {
        char c = line.charAt(i);
        if (inQuotes) {
            if (c == '"') {
                if (i + 1 < line.length() && line.charAt(i + 1) == '"') { cur.append('"'); i++; }
                else inQuotes = false;
            } else cur.append(c);
        } else if (c == '"') inQuotes = true;
        else if (c == ',') { out.add(cur.toString()); cur.setLength(0); }
        else cur.append(c);
    }
    out.add(cur.toString());
    return out;
}
```

Bộ quét xử lý quy tắc 1–2; quy tắc 3 đầy đủ cần gộp row xuyên dòng — ngoài
phạm vi hôm nay, nhưng giờ bạn biết vì sao thư viện tồn tại.
"""

# ── lesson 7.3 — JSON by hand ───────────────────────────────────────────────
L_JSON_EN = r"""
## JSON: reading structure without a library

In the sandbox you have no Jackson/Gson — and that is a feature: writing
a minimal parser teaches the format's grammar. The subset we handle:

```json
{ "name": "ann", "age": 31, "active": true, "tags": ["a", "b"] }
```

- object: `{` key `:` value (`,` key `:` value)* `}` — keys are strings
- string: `"` chars `"` with `\"` `\\` escapes
- number: integer or decimal
- literals: `true` `false` `null`
- array: `[` value (`,` value)* `]`

Rather than a full recursive-descent parser, you'll practice *flat-object
extraction*: find `"key"` at depth 0 and read its value — enough for
config-style objects, honest about skipping nesting/arrays-in-objects.

The lesson to keep: JSON's grammar is small; most JSON bugs are
*unescaped quotes* and *trailing commas* — both are grammar violations,
so a by-hand parser surfaces them loudly.
"""

L_JSON_VI = r"""
## JSON: đọc cấu trúc không cần thư viện

Trong sandbox bạn không có Jackson/Gson — và đó là một lợi thế: viết parser
tối giản dạy bạn ngữ pháp của định dạng. Tập con ta xử lý:

```json
{ "name": "ann", "age": 31, "active": true, "tags": ["a", "b"] }
```

- object: `{` key `:` value (`,` key `:` value)* `}` — key là string
- string: `"` các ký tự `"` với escape `\"` `\\`
- number: nguyên hoặc thập phân
- literal: `true` `false` `null`
- array: `[` value (`,` value)* `]`

Thay vì parser đệ quy đầy đủ, bạn sẽ luyện *trích xuất object phẳng*:
tìm `"key"` ở độ sâu 0 và đọc giá trị — đủ cho kiểu object cấu hình,
trung thực về việc bỏ qua lồng nhau/array-trong-object.

Bài học cần giữ: ngữ pháp JSON rất nhỏ; hầu hết bug JSON là *dấu ngoặc
chưa escape* và *dấu phẩy thừa* — cả hai đều vi phạm ngữ pháp, nên parser
viết tay làm chúng lộ rõ.
"""

write_module(
    MOD,
    "Files, I/O & Data Formats",
    "NIO.2's Path/Files model, encoding discipline, and hand-rolled CSV/JSON parsing that respects the real grammar.",
    "File, I/O & định dạng dữ liệu",
    "Mô hình Path/Files của NIO.2, kỷ luật encoding, và phân tích CSV/JSON viết tay tôn trọng ngữ pháp thật.",
    ["nio2-path-files", "csv-parsing-rules", "json-structure", "javi-checkpoint-io"],
    ["javi-p7-io"],
)

write_lesson(MOD, "nio2-path-files", "NIO.2: Path & Files", "Separating location from operation, naming your charset, and readAllLines vs lazy Files.lines memory discipline.", 13, L_NIO_EN, "NIO.2: Path & Files", "Tách vị trí khỏi thao tác, chỉ đích danh charset, và kỷ niệm bộ nhớ giữa readAllLines và Files.lines lười.", L_NIO_VI)

write_lesson(MOD, "csv-parsing-rules", "CSV Parsing Rules", "RFC 4180's quoted fields and escaped quotes, and why split(',') is a bug — plus the honest character scanner.", 14, L_CSV_EN, "Quy tắc parse CSV", "Quy tắc quoted field và escaped quote của RFC 4180, và vì sao split(',') là một bug — cùng bộ quét ký tự trung thực.", L_CSV_VI)

write_lesson(MOD, "json-structure", "JSON Structure by Hand", "The JSON grammar subset, flat-object extraction, and the two violations that cause most JSON bugs.", 13, L_JSON_EN, "Cấu trúc JSON viết tay", "Tập con ngữ pháp JSON, trích xuất object phẳng, và hai lỗi vi phạm gây phần lớn bug JSON.", L_JSON_VI)

# ── practice set ────────────────────────────────────────────────────────────
P7_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement methods below.
}
"""

CH_P7_CSV = challenge(
    "javi-p7-csv-scanner",
    "Quoted-CSV Row Scanner",
    r"""Implement `static List<String> parseRow(String line)` — a character
scanner that:
- splits on commas OUTSIDE double quotes
- treats `""` inside a quoted field as a literal `"`
- keeps quoted commas in the field (`"a,b"` → one field `a,b`)
- returns empty field list entries for consecutive commas
(`a,,b` → [a, , b])

The tests hit every rule from the lesson.""",
    P7_BOILER,
    [
        (
            "plain split",
            r"""
checkEq(Solution.parseRow("a,b,c"), List.of("a", "b", "c"), "plain");
""",
            "No quotes — straight comma split.",
        ),
        (
            "quoted comma stays one field",
            r"""
checkEq(Solution.parseRow("\"a,b\",c"), List.of("a,b", "c"), "quoted comma");
""",
            "The quoted comma must not split.",
        ),
        (
            "escaped double quote",
            r"""
checkEq(Solution.parseRow("\"say \"\"hi\"\"\",x"), List.of("say \"hi\"", "x"), "escaped quotes");
""",
            'Inside quotes, "" becomes a single ".',
        ),
        (
            "empty fields preserved",
            r"""
checkEq(Solution.parseRow("a,,b"), List.of("a", "", "b"), "empty middle");
""",
            "Consecutive commas produce an empty field.",
        ),
    ],
    level="independent",
)

CH_P7_ROUNTRIP = challenge(
    "javi-p7-csv-roundtrip",
    "CSV Writer + Round-Trip",
    r"""Implement the writing side:
- `static String writeRow(List<String> fields)` — joins with commas,
  wrapping a field in double quotes only when it contains a comma or
  quote; inside quoted fields, `"` becomes `""`.
- `static List<String> roundTrip(List<String> fields)` — returns
  `parseRow(writeRow(fields))` (you may re-implement the scanner or
  inline it).

Round-trip identity is the real contract: parse(write(x)) == x for any
field content — including commas and quotes.""",
    P7_BOILER,
    [
        (
            "plain fields unquoted",
            r"""
checkEq(Solution.writeRow(List.of("a", "b")), "a,b", "no quotes needed");
""",
            "No comma/quote → no wrapping.",
        ),
        (
            "comma forces quoting",
            r"""
checkEq(Solution.writeRow(List.of("a,b", "c")), "\"a,b\",c", "quoted on comma");
""",
            'Wrap in " when the field contains a comma.',
        ),
        (
            "round-trip identity",
            r"""
List<String> fields = List.of("plain", "with,comma", "say \"hi\"");
checkEq(Solution.roundTrip(fields), fields, "parse(write(x)) == x");
""",
            "The scanner and writer must be mutual inverses.",
        ),
    ],
    level="independent",
)

CH_P7_JSON = challenge(
    "javi-p7-json-flat",
    "Flat JSON Extractor",
    r"""Implement flat-object JSON extraction in `Solution`:
- `static String str(String json, String key)` — value of `"key"` when
  it's a string (unescaped), else null.
- `static Integer num(String json, String key)` — integer value, else
  null.
- `static Boolean bool(String json, String key)` — true/false, else null.

Assume flat objects (no nested braces between the target key and its
value) with `", "`-style spacing variations. Missing key → null for all
three.""",
    P7_BOILER,
    [
        (
            "string value",
            r"""
checkEq(Solution.str("{ \"name\": \"ann\", \"city\": \"hanoi\" }", "city"), "hanoi", "string field");
""",
            'Read the token after "city":.',
        ),
        (
            "numeric value",
            r"""
checkEq(Solution.num("{ \"age\": 31, \"zip\": 10000 }", "age"), 31, "number field");
""",
            "Parse the token as an integer.",
        ),
        (
            "boolean value",
            r"""
checkEq(Solution.bool("{ \"active\": true, \"admin\": false }", "admin"), false, "bool field");
""",
            "Recognize true/false literals.",
        ),
        (
            "missing key → null",
            r"""
checkEq(Solution.str("{ \"a\": \"b\" }", "nope"), null, "missing string");
checkEq(Solution.num("{ \"a\": \"b\" }", "nope"), null, "missing number");
""",
            "Absent keys return null rather than throwing.",
        ),
        (
            "non-boolean is not coerced",
            r"""
checkEq(Solution.bool("{ \"label\": \"taco\" }", "label"), null, "string is not true");
""",
            'A string value ("taco") is not a boolean — only exact true/false literals count.',
        ),
    ],
    level="independent",
)

VI_CH_P7_CSV = vi_challenge(
    "Bộ quét CSV có ngoặc kép",
    r"""Cài `static List<String> parseRow(String line)` — một bộ quét ký tự:
- tách tại dấu phẩy NGOÀI dấu ngoặc kép
- coi `""` trong field có ngoặc là dấu `"` nghĩa chữ
- giữ dấu phẩy trong ngoặc làm một field (`"a,b"` → một field `a,b`)
- trả field rỗng cho dấu phẩy liền nhau (`a,,b` → [a, , b])

Test chạm mọi quy tắc trong bài học.""",
    [
        ("Tách thuần túy", "Không ngoặc — tách comma thuần."),
        ("Dấu phẩy trong ngoặc giữ nguyên một field", "Dấu phẩy có ngoặc không được tách."),
        ("Dấu ngoặc kép escape", 'Trong ngoặc, "" thành một dấu ".'),
        ("Giữ field rỗng", "Dấu phẩy liền nhau tạo field rỗng."),
    ],
)

VI_CH_P7_ROUNTRIP = vi_challenge(
    "Writer CSV + round-trip",
    r"""Cài phía ghi:
- `static String writeRow(List<String> fields)` — nối bằng dấu phẩy,
  bọc field trong ngoặc kép chỉ khi nó chứa dấu phẩy hoặc ngoặc; trong
  field có ngoặc, `"` thành `""`.
- `static List<String> roundTrip(List<String> fields)` — trả
  `parseRow(writeRow(fields))` (có thể viết lại bộ quét hoặc nội tuyến).

Danh tính round-trip là hợp đồng thật: parse(write(x)) == x với mọi nội
dung field — kể cả dấu phẩy và ngoặc.""",
    [
        ("Field thuần không ngoặc", "Không comma/quote → không bọc."),
        ("Có comma thì bọc ngoặc", 'Bọc trong " khi field chứa dấu phẩy.'),
        ("Danh tính round-trip", "Bộ quét và writer phải nghịch đảo lẫn nhau."),
    ],
)

VI_CH_P7_JSON = vi_challenge(
    "Trích xuất JSON phẳng",
    r"""Cài trích xuất JSON phẳng trong `Solution`:
- `static String str(String json, String key)` — giá trị của `"key"`
  khi là string (đã unescape), không thì null.
- `static Integer num(String json, String key)` — giá trị số nguyên,
  không thì null.
- `static Boolean bool(String json, String key)` — true/false, không thì
  null.

Giả định object phẳng (không có ngoặc lồng giữa key mục tiêu và giá trị)
với kiểu khoảng cách `", "` linh hoạt. Key thiếu → null cho cả ba.""",
    [
        ("Giá trị string", 'Đọc token sau "city":.'),
        ("Giá trị số", "Parse token thành số nguyên."),
        ("Giá trị boolean", "Nhận diện literal true/false."),
        ("Key thiếu → null", "Key vắng mặt trả null thay vì ném."),
        ("Không ép kiểu chuỗi thành boolean", 'Giá trị string ("taco") không phải boolean — chỉ literal true/false chính xác được tính.'),
    ],
)

write_practice(
    MOD,
    "javi-p7-io",
    "I/O & Formats Lab",
    "A rule-respecting CSV scanner and writer, and flat JSON extraction without a library.",
    "Xưởng I/O & định dạng",
    "Bộ quét và writer CSV tôn trọng quy tắc, và trích xuất JSON phẳng không cần thư viện.",
    "json-structure",
    40,
    "intermediate",
    [CH_P7_CSV, CH_P7_ROUNTRIP, CH_P7_JSON],
    {CH_P7_CSV["id"]: VI_CH_P7_CSV, CH_P7_ROUNTRIP["id"]: VI_CH_P7_ROUNTRIP, CH_P7_JSON["id"]: VI_CH_P7_JSON},
    solutions=[
        (
            CH_P7_CSV["id"],
            r"""
import java.util.*;

public class Solution {
    public static List<String> parseRow(String line) {
        List<String> out = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (inQuotes) {
                if (c == '"') {
                    if (i + 1 < line.length() && line.charAt(i + 1) == '"') { cur.append('"'); i++; }
                    else inQuotes = false;
                } else cur.append(c);
            } else if (c == '"') inQuotes = true;
            else if (c == ',') { out.add(cur.toString()); cur.setLength(0); }
            else cur.append(c);
        }
        out.add(cur.toString());
        return out;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    // W: naive split — quoted commas break fields and "" is copied
    // literally. Exactly the bug the lesson warns about.
    public static List<String> parseRow(String line) {
        return new ArrayList<>(Arrays.asList(line.split(",", -1)));
    }
}
""",
        ),
        (
            CH_P7_ROUNTRIP["id"],
            r"""
import java.util.*;

public class Solution {
    public static String writeRow(List<String> fields) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < fields.size(); i++) {
            if (i > 0) out.append(',');
            String f = fields.get(i);
            boolean needsQuote = f.indexOf(',') >= 0 || f.indexOf('"') >= 0;
            if (needsQuote) {
                out.append('"');
                out.append(f.replace("\"", "\"\""));
                out.append('"');
            } else out.append(f);
        }
        return out.toString();
    }

    public static List<String> roundTrip(List<String> fields) {
        return parseRow(writeRow(fields));
    }

    static List<String> parseRow(String line) {
        List<String> out = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (inQuotes) {
                if (c == '"') {
                    if (i + 1 < line.length() && line.charAt(i + 1) == '"') { cur.append('"'); i++; }
                    else inQuotes = false;
                } else cur.append(c);
            } else if (c == '"') inQuotes = true;
            else if (c == ',') { out.add(cur.toString()); cur.setLength(0); }
            else cur.append(c);
        }
        out.add(cur.toString());
        return out;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    // W: quotes only on comma, ignores embedded quotes — a field like
    // say "hi" round-trips WRONG (the quote escapes nothing).
    public static String writeRow(List<String> fields) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < fields.size(); i++) {
            if (i > 0) out.append(',');
            String f = fields.get(i);
            if (f.indexOf(',') >= 0) out.append('"').append(f).append('"');
            else out.append(f);
        }
        return out.toString();
    }

    public static List<String> roundTrip(List<String> fields) {
        return parseRow(writeRow(fields));
    }

    static List<String> parseRow(String line) {
        List<String> out = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (inQuotes) {
                if (c == '"') {
                    if (i + 1 < line.length() && line.charAt(i + 1) == '"') { cur.append('"'); i++; }
                    else inQuotes = false;
                } else cur.append(c);
            } else if (c == '"') inQuotes = true;
            else if (c == ',') { out.add(cur.toString()); cur.setLength(0); }
            else cur.append(c);
        }
        out.add(cur.toString());
        return out;
    }
}
""",
        ),
        (
            CH_P7_JSON["id"],
            r"""
import java.util.*;

public class Solution {
    static String valueAfter(String json, String key) {
        String needle = "\"" + key + "\"";
        int k = json.indexOf(needle);
        if (k < 0) return null;
        int colon = json.indexOf(':', k + needle.length());
        if (colon < 0) return null;
        int i = colon + 1;
        while (i < json.length() && Character.isWhitespace(json.charAt(i))) i++;
        int end = i;
        if (json.charAt(i) == '"') {
            end++;
            while (json.charAt(end) != '"') {
                if (json.charAt(end) == '\\') end++;
                end++;
            }
            return json.substring(i, end + 1);   // keep quotes; callers interpret
        }
        while (end < json.length() && ",}] \n\t".indexOf(json.charAt(end)) < 0) end++;
        return json.substring(i, end);
    }

    public static String str(String json, String key) {
        String v = valueAfter(json, key);
        if (v == null || !v.startsWith("\"")) return null;
        return v.substring(1, v.length() - 1);
    }

    public static Integer num(String json, String key) {
        String v = valueAfter(json, key);
        if (v == null || v.startsWith("\"")) return null;
        try { return Integer.parseInt(v); } catch (NumberFormatException e) { return null; }
    }

    public static Boolean bool(String json, String key) {
        String v = valueAfter(json, key);
        if ("true".equals(v)) return true;
        if ("false".equals(v)) return false;
        return null;
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    static String valueAfter(String json, String key) {
        String needle = "\"" + key + "\"";
        int k = json.indexOf(needle);
        if (k < 0) return null;
        int colon = json.indexOf(':', k + needle.length());
        if (colon < 0) return null;
        int i = colon + 1;
        while (i < json.length() && Character.isWhitespace(json.charAt(i))) i++;
        int end = i;
        if (json.charAt(i) == '"') {
            end++;
            while (json.charAt(end) != '"') {
                if (json.charAt(end) == '\\') end++;
                end++;
            }
            return json.substring(i, end + 1);
        }
        while (end < json.length() && ",}] \n\t".indexOf(json.charAt(end)) < 0) end++;
        return json.substring(i, end);
    }

    // W: bool() reports true for any value starting with 't' — including
    // the string "taco". Real booleans must match true/false exactly.
    public static Boolean bool(String json, String key) {
        String v = valueAfter(json, key);
        if (v == null) return null;
        return v.startsWith("t");
    }

    public static String str(String json, String key) {
        String v = valueAfter(json, key);
        if (v == null || !v.startsWith("\"")) return null;
        return v.substring(1, v.length() - 1);
    }

    public static Integer num(String json, String key) {
        String v = valueAfter(json, key);
        if (v == null || v.startsWith("\"")) return null;
        try { return Integer.parseInt(v); } catch (NumberFormatException e) { return null; }
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — files & formats

You can now: separate Path from Files operations, parse CSV per the real
rules, and extract JSON without a library. Prove it with a record
normalizer over a CSV payload.
"""

CP_MDX_VI = r"""
## Checkpoint — file & định dạng

Giờ bạn có thể: tách thao tác Path khỏi Files, parse CSV theo quy tắc
thật, và trích xuất JSON không cần thư viện. Chứng minh bằng một bộ chuẩn
hóa record trên payload CSV.
"""

CH_CP7 = challenge(
    "javi-checkpoint-m7-io",
    "CSV Payload Normalizer",
    r"""Build `Solution`:
- `static List<String> parseRow(String line)` — the quoted-CSV scanner
  from the practice (reuse your implementation).
- `record Record(String name, int qty)` in `Solution`.
- `static List<Record> normalize(List<String> rows, String header)`:
  parse each row with the scanner; SKIP rows that fail numeric parsing
  of the qty column (index 1); the header row (matching `header` exactly)
  is skipped too. Return the records in order.

Edge cases: fields may contain quoted commas; `qty` may have
surrounding spaces (trim before parse).""",
    r"""
import java.util.*;

public class Solution {
    // Provide parseRow + Record + normalize here.
}
""",
    [
        (
            "clean payload",
            r"""
List<Solution.Record> out = Solution.normalize(
    List.of("name,qty", "pen,3", "ink,1"), "name,qty");
checkEq(out.size(), 2, "two records");
""",
            "Header skipped, two data rows parsed.",
        ),
        (
            "quoted commas survive",
            r"""
List<Solution.Record> out = Solution.normalize(
    List.of("name,qty", "\"pen, blue\",2"), "name,qty");
checkEq(out.get(0).name(), "pen, blue", "quoted name");
checkEq(out.get(0).qty(), 2, "qty parsed");
""",
            "The scanner keeps 'pen, blue' as one field.",
        ),
        (
            "bad qty skipped",
            r"""
List<Solution.Record> out = Solution.normalize(
    List.of("name,qty", "pen,3", "ghost,xyz", "ink,1"), "name,qty");
checkEq(out.size(), 2, "ghost dropped");
""",
            "Non-numeric qty rows are skipped, not fatal.",
        ),
        (
            "qty with spaces",
            r"""
List<Solution.Record> out = Solution.normalize(
    List.of("name,qty", "pen, 3"), "name,qty");
checkEq(out.get(0).qty(), 3, "trimmed qty");
""",
            "Trim before Integer.parseInt.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP7 = vi_challenge(
    "Chuẩn hóa payload CSV",
    r"""Xây `Solution`:
- `static List<String> parseRow(String line)` — bộ quét CSV có ngoặc kép
  từ phần luyện (tái sử dụng bản của bạn).
- `record Record(String name, int qty)` trong `Solution`.
- `static List<Record> normalize(List<String> rows, String header)`:
  parse từng row bằng bộ quét; BỎ qua row lỗi khi parse cột qty (index 1)
  thành số; row header (khớp `header` chính xác) cũng bị bỏ. Trả các
  record theo thứ tự.

Trường biên: field có thể chứa dấu phẩy trong ngoặc; `qty` có thể có
khoảng trắng hai bên (trim trước khi parse).""",
    [
        ("Payload sạch", "Header bị bỏ, hai row dữ liệu được parse."),
        ("Dấu phẩy trong ngoặc sống sót", "Bộ quét giữ 'pen, blue' làm một field."),
        ("qty lỗi bị bỏ", "Row qty không phải số bị bỏ qua, không fatal."),
        ("qty có khoảng trắng", "Trim trước Integer.parseInt."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-io",
    "Checkpoint: Files & Formats",
    "Graded checkpoint: a CSV normalizer combining the scanner, records, and tolerant parsing.",
    15,
    CP_MDX,
    "Checkpoint: File & định dạng",
    "Checkpoint chấm điểm: bộ chuẩn hóa CSV kết hợp bộ quét, record, và parse khoan dung.",
    CP_MDX_VI,
    CH_CP7,
    VI_CH_CP7,
    solution=r"""
import java.util.*;

public class Solution {
    public record Record(String name, int qty) {}

    public static List<String> parseRow(String line) {
        List<String> out = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (inQuotes) {
                if (c == '"') {
                    if (i + 1 < line.length() && line.charAt(i + 1) == '"') { cur.append('"'); i++; }
                    else inQuotes = false;
                } else cur.append(c);
            } else if (c == '"') inQuotes = true;
            else if (c == ',') { out.add(cur.toString()); cur.setLength(0); }
            else cur.append(c);
        }
        out.add(cur.toString());
        return out;
    }

    public static List<Record> normalize(List<String> rows, String header) {
        List<Record> out = new ArrayList<>();
        for (String row : rows) {
            if (row.equals(header)) continue;
            List<String> fields = parseRow(row);
            if (fields.size() < 2) continue;
            try {
                out.add(new Record(fields.get(0), Integer.parseInt(fields.get(1).trim())));
            } catch (NumberFormatException ignored) {
                // skip malformed qty rows — documented behavior
            }
        }
        return out;
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public record Record(String name, int qty) {}

    public static List<String> parseRow(String line) {
        List<String> out = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (inQuotes) {
                if (c == '"') {
                    if (i + 1 < line.length() && line.charAt(i + 1) == '"') { cur.append('"'); i++; }
                    else inQuotes = false;
                } else cur.append(c);
            } else if (c == '"') inQuotes = true;
            else if (c == ',') { out.add(cur.toString()); cur.setLength(0); }
            else cur.append(c);
        }
        out.add(cur.toString());
        return out;
    }

    // W: uses naive split for normalize (not the scanner), so quoted
    // commas split the name field; also treats bad qty as fatal.
    public static List<Record> normalize(List<String> rows, String header) {
        List<Record> out = new ArrayList<>();
        for (String row : rows) {
            if (row.equals(header)) continue;
            String[] fields = row.split(",");
            out.add(new Record(fields[0], Integer.parseInt(fields[1].trim())));
        }
        return out;
    }
}
""",
)
