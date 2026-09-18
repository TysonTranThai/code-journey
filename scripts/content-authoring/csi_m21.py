#!/usr/bin/env python3
"""C# — Intermediate — Module 21: csi-security.

Security fundamentals: input validation, the injection family (SQL-shaped,
path traversal), sensitive-data hygiene, authentication vs authorization,
and salted password storage — all graded behaviorally in the sandbox with
real System.Security.Cryptography primitives.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-security"

write_module(
    M,
    "Security Fundamentals",
    "Where real-world C# code gets breached: string-built queries, unresolved paths, plaintext passwords, and secrets in logs — and the defensive shape for each.",
    "Nền tảng Bảo mật",
    "Nơi code C# ngoài đời bị xâm nhập: query dựng bằng string, đường dẫn chưa xử lý, mật khẩu plaintext, và bí mật trong log — và hình dạng phòng thủ cho từng loại.",
    ["injection-defense", "authn-authz", "csi-checkpoint-m21"],
    ["csi-p21-security"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "injection-defense",
    "Injection: Queries, Paths, and Logs",
    "Every value that crosses a trust boundary — into a query, a path, a log line — needs a barrier. Interpreting user data as structure is the root vulnerability.",
    25,
    r"""
## The one rule

**User input is data, never structure.** The whole injection family comes
from letting data be parsed as code or structure:

- string-concatenated SQL → the data becomes SQL,
- unresolved file paths → the data becomes a location outside the sandbox,
- raw secrets in logs → the log file becomes the leak.

## SQL injection: concatenate = vulnerable

```csharp
// VULNERABLE: input is pasted into the query text
var sql = "SELECT * FROM Users WHERE Name = '" + username + "'";
// username = "' OR '1'='1"  ->  returns every row
// username = "'; DROP TABLE Users; --"  ->  destroys the table
```

The fix is **parameterized queries**: send the query text with placeholders
and the values separately, so the driver can never re-parse values as SQL:

```csharp
// SAFE: value travels as data
var sql = "SELECT * FROM Users WHERE Name = @name";
// command.Parameters.AddWithValue("@name", username);
```

A parameter is honored by every real data API (ADO.NET, EF Core, Dapper).
Building a WHERE clause by concatenation is a bug even when "input is
validated today" — validation drifts, parameters don't.

## Path traversal: resolve, then confine

`Path.Combine(baseDir, userInput)` happily produces
`/app/data/../../etc/passwd`. The defensive shape is **resolve first, then
confine**: expand the combined path with `Path.GetFullPath`, then require
the result to still be under the base directory:

```csharp
var full = Path.GetFullPath(Path.Combine(baseDir, userInput));
bool allowed = full.StartsWith(
    Path.GetFullPath(baseDir) + Path.DirectorySeparatorChar);
if (!allowed) throw new UnauthorizedAccessException();
```

`GetFullPath` is what collapses `..` segments — checking the *unresolved*
string catches nothing.

## Logs are a public interface

Log lines get aggregated, exported, and read by people and tools with no
business knowing users' secrets. Never log: passwords, tokens, full card
numbers, unmasked personal identifiers. Log **what happened**, not the
credential that made it happen. If an identifier is needed for correlation,
mask it (`"email=***"`).
""",
    "Injection: Truy vấn, Đường dẫn, và Log",
    "Mọi giá trị vượt qua ranh giới tin cậy — vào query, đường dẫn, dòng log — đều cần rào chắn. Coi dữ liệu người dùng là cấu trúc là lỗ hổng gốc.",
    r"""
## Một quy tắc duy nhất

**Dữ liệu người dùng là dữ liệu, không bao giờ là cấu trúc.** Cả họ injection
xuất phát từ việc cho dữ liệu được phân tích như code hoặc cấu trúc:

- SQL dựng bằng nối chuỗi → dữ liệu trở thành SQL,
- đường dẫn chưa xử lý → dữ liệu trở thành một vị trí ngoài sandbox,
- bí mật thô trong log → tệp log trở thành nơi rò rỉ.

## SQL injection: nối chuỗi = dễ tổn thương

```csharp
// DỄ TỔN THƯƠNG: input được dán vào văn bản query
var sql = "SELECT * FROM Users WHERE Name = '" + username + "'";
// username = "' OR '1'='1"  ->  trả về mọi dòng
```

Chữa là **truy vấn tham số hóa**: gửi văn bản query với placeholder và giá trị
tách riêng, để driver không bao giờ phân tích lại giá trị thành SQL:

```csharp
// AN TOÀN: giá trị đi dưới dạng dữ liệu
var sql = "SELECT * FROM Users WHERE Name = @name";
// command.Parameters.AddWithValue("@name", username);
```

Mọi data API thật (ADO.NET, EF Core, Dapper) đều hỗ trợ tham số. Dựng WHERE
bằng nối chuỗi là lỗi kể cả khi "input đã được validate hôm nay" — validation
trôi dạt, tham số thì không.

## Path traversal: xử lý trước, giới hạn sau

`Path.Combine(baseDir, userInput)` sẵn sàng tạo ra `/app/data/../../etc/passwd`.
Hình dạng phòng thủ là **resolve trước, giới hạn sau**: triển khai đường dẫn
gộp bằng `Path.GetFullPath`, rồi yêu cầu kết quả vẫn nằm trong thư mục gốc:

```csharp
var full = Path.GetFullPath(Path.Combine(baseDir, userInput));
bool allowed = full.StartsWith(
    Path.GetFullPath(baseDir) + Path.DirectorySeparatorChar);
if (!allowed) throw new UnauthorizedAccessException();
```

`GetFullPath` là thứ gộp các đoạn `..` — kiểm tra chuỗi *chưa xử lý* không bắt
được gì.

## Log là một giao diện công khai

Dòng log được tổng hợp, xuất đi, và đọc bởi người lẫn công cụ không có lý do gì
biết bí mật của người dùng. Không bao giờ log: mật khẩu, token, số thẻ đầy đủ,
định danh cá nhân không che. Log **chuyện gì xảy ra**, không log thông tin xác
thực khiến nó xảy ra. Nếu cần định danh để đối chiếu, che nó (`"email=***"`).
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "authn-authz",
    "Authentication, Authorization, and Password Storage",
    "Who are you (authn) vs what may you do (authz) — and why passwords are stored as salted, slow hashes, never plaintext or bare digests.",
    24,
    r"""
## Two different questions

- **Authentication** — *who* is this requester? (verify a credential: password
  check, token validation.)
- **Authorization** — *what* is this authenticated identity allowed to do?
  (roles, ownership checks, least privilege.)

They fail differently: a missing authn check lets strangers in; a missing
authz check lets *valid* users do things they shouldn't (IDOR — acting on
someone else's record id). Check both, in that order, at every boundary.

## Password storage: salted slow hashes

Databases get dumped. The stored form must be useless to the attacker:

1. **Never plaintext.** Anyone with the file knows every password.
2. **Never a bare digest** (`SHA256(password)`): digests are fast — GPUs try
   billions per second — and identical passwords produce identical hashes
   (rainbow tables).
3. **Store `salt + slow-KDF(password, salt)`.** The salt is random per user,
   stored in the clear next to the hash; it kills precomputation and makes
   identical passwords hash differently across users. The KDF is a
   *deliberately slow* function — PBKDF2 is in the box:

```csharp
using var kdf = new Rfc2898DeriveBytes(
    password, salt, iterations: 100_000, HashAlgorithmName.SHA256);
byte[] hash = kdf.GetBytes(32);
```

Verification recomputes with the *stored* salt and compares. Per-user salt +
slow KDF are the two halves; either one alone is half a defense.

## Least privilege and secrets

- Run with the narrowest rights that work; a compromised component then
  compromises less. Admin-only operations demand an explicit role check —
  "the UI hides the button" is not a check.
- Secrets (connection strings, API keys) live in configuration/environment,
  referenced by code — never literals in source, and never in logs or
  exception messages.
""",
    "Xác thực, Phân quyền, và Lưu trữ Mật khẩu",
    "Bạn là ai (authn) so với bạn được làm gì (authz) — và vì sao mật khẩu được lưu dưới dạng hash chậm có salt, không bao giờ plaintext hay digest trần.",
    r"""
## Hai câu hỏi khác nhau

- **Xác thực (authentication)** — người yêu cầu *là ai*? (xác minh thông tin
  xác thực: kiểm tra mật khẩu, xác thực token.)
- **Phân quyền (authorization)** — định danh đã xác thực *được làm gì*?
  (vai trò, kiểm tra quyền sở hữu, đặc quyền tối thiểu.)

Chúng thất bại khác nhau: thiếu authn để người lạ vào; thiếu authz cho *người
dùng hợp lệ* làm việc họ không được phép (IDOR — tác động lên bản ghi của
người khác). Kiểm tra cả hai, theo thứ tự đó, tại mọi ranh giới.

## Lưu trữ mật khẩu: hash chậm có salt

Database bị đổ ra. Dạng lưu trữ phải vô dụng với kẻ tấn công:

1. **Không bao giờ plaintext.** Ai có tệp là biết mọi mật khẩu.
2. **Không bao giờ digest trần** (`SHA256(password)`): digest rất nhanh — GPU
   thử hàng tỷ lần mỗi giây — và mật khẩu giống nhau cho hash giống nhau
   (rainbow table).
3. **Lưu `salt + slow-KDF(password, salt)`.** Salt ngẫu nhiên cho từng người
   dùng, lưu rõ cạnh hash; nó vô hiệu hóa tính toán trước và làm mật khẩu
   giống nhau hash khác nhau giữa các người dùng. KDF là hàm *cố ý chậm* —
   PBKDF2 có sẵn trong .NET (xem ví dụ trong bản tiếng Anh).

Xác minh tính lại với *salt đã lưu* rồi so sánh. Salt theo người dùng + KDF
chậm là hai nửa của bài phòng thủ; thiếu một nửa là nửa vời.

## Đặc quyền tối thiểu và bí mật

- Chạy với quyền hẹp nhất còn chạy được; một thành phần bị chiếm sẽ chiếm được
  ít hơn. Thao tác admin-only yêu cầu kiểm tra vai trò tường minh — "UI ẩn nút"
  không phải là kiểm tra.
- Bí mật (connection string, API key) nằm trong cấu hình/biến môi trường, code
  tham chiếu đến — không bao giờ là literal trong source, và không bao giờ
  xuất hiện trong log hay thông báo lỗi.
""",
)

# ---------------------------------------------------------------- practice
KDF_NOTE = (
    "\n"
    "// Provided infrastructure — do not modify. The course's PBKDF2 contract:\n"
    "// 32-byte key, SHA-256, iteration count passed in. Tests use the same\n"
    "// primitive as the reference, so this is the agreed hash shape.\n"
    "public static class KdfShape\n"
    "{\n"
    "    public static byte[] Derive(string password, byte[] salt, int iterations)\n"
    "    {\n"
    "        using var kdf = new System.Security.Cryptography.Rfc2898DeriveBytes(\n"
    "            password, salt, iterations, System.Security.Cryptography.HashAlgorithmName.SHA256);\n"
    "        return kdf.GetBytes(32);\n"
    "    }\n"
    "\n"
    "    public static string Hex(byte[] bytes)\n"
    "    {\n"
    "        var sb = new System.Text.StringBuilder(bytes.Length * 2);\n"
    "        foreach (var b in bytes) sb.Append(b.ToString(\"x2\"));\n"
    "        return sb.ToString();\n"
    "    }\n"
    "}\n"
)

QUERY_ENGINE = (
    "\n"
    "// Provided infrastructure — do not modify. A toy SQL-shaped engine:\n"
    "// Run(sql, parameterValues) matches @pN placeholders with the given values\n"
    "// and reports how many Users rows the WHERE clause matched. Concatenated\n"
    "// \"values\" arrive as query TEXT and match everything — exactly like a real\n"
    "// injection.\n"
    "public static class CjQuery\n"
    "{\n"
    "    public static int TotalUsers = 25;\n"
    "\n"
    "    public static int MatchedUsers(string sql, params string[] parameterValues)\n"
    "    {\n"
    "        if (!sql.Contains(\"WHERE\")) return TotalUsers;\n"
    "        int where = sql.IndexOf(\"WHERE\");\n"
    "        var clause = sql.Substring(where);\n"
    "        // real parameter placeholders (@p0, @p1, ...) mean the value is data\n"
    "        foreach (var pv in parameterValues)\n"
    "            clause = clause.Replace(\"'\" + pv + \"'\", \"\");\n"
    "        if (clause.Contains(\"'\")) return TotalUsers;   // a quote made it into query text\n"
    "        return 1;   // one user matched by value\n"
    "    }\n"
    "}\n"
)

write_practice(
    M,
    "csi-p21-security",
    "Security Practice: Barriers at the Boundary",
    "Turn a string-built query into a parameterized one, confine path resolution, store passwords with PBKDF2 + per-user salt, and keep secrets out of log lines.",
    "Luyện Bảo mật: Rào chắn tại Ranh giới",
    "Biến query dựng bằng string thành truy vấn tham số hóa, giới hạn resolve đường dẫn, lưu mật khẩu với PBKDF2 + salt theo người dùng, và giữ bí mật khỏi dòng log.",
    "authn-authz",
    32,
    "intermediate",
    [
        challenge(
            "csi-p21-param-query",
            "Parameterize the Query",
            r"""`LoginQuery(sql)` builds a login lookup by pasting the username into
the query text — the classic injection. Write
`Solution.BuildLoginQuery(string username)` returning the safe pair
`(sql, parameterValue)`:

```csharp
public static class Solution
{
    public static (string Sql, string Value) BuildLoginQuery(string username);
}
```

Contract, graded through the provided `CjQuery` engine (which mimics a real
driver: placeholders mean "data", pasted text means "query"):

- the SQL contains a `@p0` placeholder — the username never appears in the
  SQL text,
- the username travels as the parameter value,
- `CjQuery.MatchedUsers(sql, value)` returns `1` for a normal username and
  for the injection attempt `"' OR '1'='1"` — the attack must be treated as
  just a (nonexistent) username, never as "match everything".""",
            CS_PRELUDE + QUERY_ENGINE,
            [
                (
                    "normal user matches exactly one row",
                    r"""
var (sql, val) = Solution.BuildLoginQuery("ada");
Cj.True(sql.Contains("@p0"), "placeholder in SQL");
Cj.Eq(val, "ada", "username travels as the value");
Cj.Eq(CjQuery.MatchedUsers(sql, val), 1, "one row");
""",
                    "The placeholder is in the SQL; the username is the parameter.",
                ),
                (
                    "injection attempts match one row, not all",
                    r"""
var (sql, val) = Solution.BuildLoginQuery("' OR '1'='1");
Cj.True(!sql.Contains("' OR"), "attack text never enters the SQL");
Cj.Eq(CjQuery.MatchedUsers(sql, val), 1, "treated as a (nonexistent) username");
""",
                    "If a quote reaches the query text, the engine matches everything.",
                ),
                (
                    "sql shape stays parameterized for any input",
                    r"""
var (sql, val) = Solution.BuildLoginQuery("'; DROP TABLE Users; --");
Cj.True(sql.Contains("@p0"), "still a placeholder");
Cj.True(!sql.Contains(";"), "no terminator smuggled into SQL");
Cj.Eq(val, "'; DROP TABLE Users; --", "value carried intact as data");
""",
                    "The value may be anything; the SQL must stay placeholder-shaped.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p21-path-safe",
            "Confine the Path",
            r"""`FileLoader.Read(baseDir, userPath)` serves files by combining
`baseDir` with whatever the request carries — `../../secrets.txt` escapes the
sandbox. Write `Solution.SafeResolve(string baseDir, string userPath)`
returning the fully-resolved path **or `null` when it escapes `baseDir`**:

```csharp
public static class Solution
{
    public static string SafeResolve(string baseDir, string userPath);
}
```

Rules:

- resolve with `Path.GetFullPath(Path.Combine(...))`, then require the result
  to stay under the resolved base directory (`GetFullPath(baseDir)` +
  separator),
- plain names and nested subpaths (`"reports/2026.csv"`, `"a/../b.txt"` as
  long as the result stays inside) are allowed and returned fully resolved,
- any escape — leading `/`, drive root, `..` past the top — returns `null`,
- `userPath` that resolves exactly to `baseDir` itself is `null` (only files
  under it are served).""",
            CS_PRELUDE,
            [
                (
                    "normal paths resolve under the base",
                    r"""
var p = Solution.SafeResolve("/app/data", "reports/2026.csv");
Cj.True(p != null && p.EndsWith("reports/2026.csv"), "nested file allowed");
var p2 = Solution.SafeResolve("/app/data", "a/../b.txt");
Cj.True(p2 != null && p2.EndsWith("b.txt"), "inner .. that stays inside is fine");
""",
                    "GetFullPath collapses inner .. segments; the result stays inside.",
                ),
                (
                    "traversal escapes are rejected",
                    r"""
Cj.Eq(Solution.SafeResolve("/app/data", "../../etc/passwd"), null, "up and out");
Cj.Eq(Solution.SafeResolve("/app/data", "/etc/passwd"), null, "absolute escape");
""",
                    "Resolve, then require the prefix — unresolved checks see nothing.",
                ),
                (
                    "the base itself is not a servable file",
                    r"""
Cj.Eq(Solution.SafeResolve("/app/data", "."), null, "the directory is not a file path");
Cj.True(Solution.SafeResolve("/app/data", "notes.txt") != null, "a direct child still works");
""",
                    "Exactly-base resolves to the base — refuse it.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p21-password-hash",
            "Salted, Slow, and Recomputable",
            r"""`UserStore` stores `SHA256(password)` directly — fast, unsalted,
reversible by lookup tables. Replace it with the standard shape using the
provided `KdfShape` primitive (PBKDF2-SHA256, 32 bytes):

```csharp
public static class Solution
{
    public static string HashPassword(string password, byte[] salt);   // hex, 100_000 iterations
    public static bool Verify(string password, byte[] salt, string storedHex);
    public static void RequireSalt(byte[] salt);   // throws ArgumentException when salt is null or shorter than 16 bytes
}
```

Rules:

- `HashPassword` calls `RequireSalt` first, then derives via
  `KdfShape.Derive(password, salt, 100_000)` and returns the lowercase hex —
  the test computes the same reference and compares exactly,
- `Verify` treats a null or too-short salt as a failed verification
  (`false`) — it must never throw for bad inputs; otherwise it recomputes
  with the stored salt and returns whether the hex matches,
- wrong password → `false`, never an exception.""",
            CS_PRELUDE + KDF_NOTE,
            [
                (
                    "hash matches the PBKDF2 reference",
                    r"""
var salt = new byte[16]; for (int i = 0; i < 16; i++) salt[i] = (byte)i;
var expected = KdfShape.Hex(KdfShape.Derive("correct horse", salt, 100_000));
Cj.Eq(Solution.HashPassword("correct horse", salt), expected, "PBKDF2-SHA256, 100k, 32 bytes");
""",
                    "One primitive, one iteration count, one key length — exactly.",
                ),
                (
                    "verify accepts the password and rejects others",
                    r"""
var salt = new byte[16]; for (int i = 0; i < 16; i++) salt[i] = (byte)(i + 1);
var stored = Solution.HashPassword("hunter2", salt);
Cj.True(Solution.Verify("hunter2", salt, stored), "right password");
Cj.True(!Solution.Verify("hunter3", salt, stored), "wrong password");
""",
                    "Verification is the same derivation plus a comparison.",
                ),
                (
                    "short or missing salt is refused",
                    r"""
var shortSalt = new byte[8];
bool threw = false;
try { Solution.HashPassword("pw", shortSalt); }
catch (System.ArgumentException) { threw = true; }
Cj.True(threw, "8-byte salt throws");
Cj.True(!Solution.Verify("pw", null, "ab"), "null salt -> false, not crash");
""",
                    "HashPassword validates the salt; Verify treats a bad salt as a failure.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p21-log-scrub",
            "Audit Without Leaking",
            r"""`AuditLog.Write(action, email)` pastes the raw email into every
line — the log file becomes a personal-data store. Write
`Solution.Audit(string action, string email)` returning the safe line:

```csharp
public static class Solution
{
    public static string Audit(string action, string email);
}
```

Contract:

- the line is exactly `"<action> email=***"` — the email never appears,
  not even partially, whatever its content,
- `email` of `null` or empty produces the same `email=***` (nothing to
  correlate, nothing to leak),
- the action text is preserved verbatim (including spaces).""",
            CS_PRELUDE,
            [
                (
                    "the raw email never reaches the line",
                    r"""
var line = Solution.Audit("LOGIN_OK", "ada@example.com");
Cj.Eq(line, "LOGIN_OK email=***", "masked");
Cj.True(!line.Contains("ada"), "no fragment of the identity");
""",
                    "Mask fully; partial masking leaks partial identities.",
                ),
                (
                    "empty or missing email still logs the action",
                    r"""
Cj.Eq(Solution.Audit("LOGOUT", ""), "LOGOUT email=***", "empty email");
Cj.Eq(Solution.Audit("LOGOUT", null), "LOGOUT email=***", "null email");
""",
                    "No identity is not an error — it is just nothing to leak.",
                ),
                (
                    "action text is preserved verbatim",
                    r"""
Cj.Eq(Solution.Audit("PWD RESET REQUESTED", "x@y.z"), "PWD RESET REQUESTED email=***", "verbatim action");
""",
                    "The event description is the useful part — keep it exact.",
                ),
            ],
            level="imitation",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p21-param-query": vi_challenge(
            "Tham số hóa truy vấn",
            "`LoginQuery(sql)` dựng lookup đăng nhập bằng cách dán username vào văn bản query — injection kinh điển. Viết `Solution.BuildLoginQuery(string username)` trả cặp an toàn `(sql, parameterValue)`: SQL chứa placeholder `@p0`, username đi với tư cách giá trị tham số. Chấm qua engine `CjQuery` cấp sẵn: `MatchedUsers(sql, value)` phải trả 1 cho username thường và cho chuỗi tấn công `\"' OR '1'='1\"` — tấn công chỉ là một username (không tồn tại), không bao giờ là \"match mọi hàng\".",
            [
                ("normal user matches exactly one row", "Placeholder nằm trong SQL; username là tham số."),
                ("injection attempts match one row, not all", "Dấu nháy lọt vào văn bản query thì engine match tất cả."),
                ("sql shape stays parameterized for any input", "Giá trị có thể là bất cứ gì; SQL phải giữ dạng placeholder."),
            ],
        ),
        "csi-p21-path-safe": vi_challenge(
            "Giới hạn đường dẫn",
            "`FileLoader.Read(baseDir, userPath)` phục vụ tệp bằng cách gộp `baseDir` với bất cứ gì request mang theo — `../../secrets.txt` thoát ra ngoài. Viết `Solution.SafeResolve(string baseDir, string userPath)` trả đường dẫn đã resolve đầy đủ **hoặc `null` khi thoát khỏi `baseDir`**: resolve bằng `Path.GetFullPath(Path.Combine(...))`, rồi yêu cầu kết quả nằm dưới base đã resolve; đường dẫn trong (`\"reports/2026.csv\"`, `\"a/../b.txt\"` còn ở trong) hợp lệ; mọi lối thoát trả `null`; đường dẫn resolve đúng bằng `baseDir` cũng là `null`.",
            [
                ("normal paths resolve under the base", "GetFullPath gộp các đoạn .. bên trong; kết quả vẫn ở trong."),
                ("traversal escapes are rejected", "Resolve rồi yêu cầu prefix — kiểm tra chuỗi chưa resolve không thấy gì."),
                ("the base itself is not a servable file", "Đường dẫn đúng bằng base là thư mục — từ chối."),
            ],
        ),
        "csi-p21-password-hash": vi_challenge(
            "Có salt, chậm, và tính lại được",
            "`UserStore` lưu thẳng `SHA256(password)` — nhanh, không salt, bị phá bằng bảng tra. Thay bằng hình dạng chuẩn với primitive `KdfShape` cấp sẵn (PBKDF2-SHA256, 32 byte): `HashPassword(password, salt)` gọi `RequireSalt` trước rồi trả hex từ `KdfShape.Derive(password, salt, 100_000)`; `Verify(password, salt, storedHex)` coi salt null/quá ngắn là xác minh thất bại (`false`, không ném exception), còn lại tính lại và so sánh; sai mật khẩu -> `false`, không bao giờ ném exception; `RequireSalt(salt)` ném `System.ArgumentException` khi salt là null hoặc ngắn hơn 16 byte.",
            [
                ("hash matches the PBKDF2 reference", "Một primitive, một iteration count, một độ dài khóa — chính xác."),
                ("verify accepts the password and rejects others", "Xác minh là cùng phép đạo hàm cộng một phép so sánh."),
                ("short or missing salt is refused", "HashPassword validate salt; Verify coi salt xấu là thất bại."),
            ],
        ),
        "csi-p21-log-scrub": vi_challenge(
            "Audit mà không rò rỉ",
            "`AuditLog.Write(action, email)` dán email thô vào mọi dòng — tệp log trở thành kho dữ liệu cá nhân. Viết `Solution.Audit(string action, string email)` trả dòng an toàn đúng `\"<action> email=***\"`: email không bao giờ xuất hiện, kể cả một phần; email null/rỗng vẫn ra `email=***`; văn bản hành động được giữ nguyên verbatim.",
            [
                ("the raw email never reaches the line", "Che trọn vẹn; che một phần vẫn rò một phần định danh."),
                ("empty or missing email still logs the action", "Không có định danh không phải là lỗi — chỉ là không có gì để rò."),
                ("action text is preserved verbatim", "Mô tả sự kiện mới là phần hữu ích — giữ chính xác."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p21-param-query",
            'public static class Solution\n{\n    public static (string Sql, string Value) BuildLoginQuery(string username)\n    {\n        // the value travels as data; the SQL keeps a placeholder\n        return ("SELECT * FROM Users WHERE Name = @p0", username);\n    }\n}\n',
            'public static class Solution\n{\n    public static (string Sql, string Value) BuildLoginQuery(string username)\n    {\n        // near-miss: "escaped" the input but still pastes it into query text —\n        // quoting is data-mangling, not a parameter\n        var safe = username.Replace("\'", "\'\'");\n        return ("SELECT * FROM Users WHERE Name = \'" + safe + "\'", username);\n    }\n}\n',
        ),
        (
            "csi-p21-path-safe",
            'public static class Solution\n{\n    public static string SafeResolve(string baseDir, string userPath)\n    {\n        if (string.IsNullOrEmpty(userPath)) return null;\n        var baseFull = System.IO.Path.GetFullPath(baseDir);\n        var full = System.IO.Path.GetFullPath(\n            System.IO.Path.Combine(baseFull, userPath));\n        var allowedPrefix = baseFull.EndsWith(\n            System.IO.Path.DirectorySeparatorChar.ToString())\n            ? baseFull\n            : baseFull + System.IO.Path.DirectorySeparatorChar;\n        if (!full.StartsWith(allowedPrefix)) return null;\n        if (full == baseFull) return null;\n        return full;\n    }\n}\n',
            'public static class Solution\n{\n    public static string SafeResolve(string baseDir, string userPath)\n    {\n        // near-miss: blocks the *string* "../" but never resolves the path —\n        // encoded or composed escapes slip through, and nothing is confined\n        if (userPath.Contains("..")) return null;\n        return System.IO.Path.Combine(baseDir, userPath);\n    }\n}\n',
        ),
        (
            "csi-p21-password-hash",
            'public static class Solution\n{\n    public static void RequireSalt(byte[] salt)\n    {\n        if (salt == null || salt.Length < 16)\n            throw new System.ArgumentException("salt must be at least 16 bytes");\n    }\n\n    public static string HashPassword(string password, byte[] salt)\n    {\n        RequireSalt(salt);\n        return KdfShape.Hex(KdfShape.Derive(password, salt, 100_000));\n    }\n\n    public static bool Verify(string password, byte[] salt, string storedHex)\n    {\n        if (salt == null || salt.Length < 16 || storedHex == null) return false;\n        return KdfShape.Hex(KdfShape.Derive(password, salt, 100_000)) == storedHex;\n    }\n}\n',
            'public static class Solution\n{\n    public static void RequireSalt(byte[] salt)\n    {\n        if (salt == null || salt.Length < 16)\n            throw new System.ArgumentException("salt must be at least 16 bytes");\n    }\n\n    public static string HashPassword(string password, byte[] salt)\n    {\n        RequireSalt(salt);\n        // near-miss: validates the salt, then hashes with a bare fast digest —\n        // no KDF, no iterations; the shape is right, the crypto is wrong\n        using var sha = System.Security.Cryptography.SHA256.Create();\n        var bytes = System.Text.Encoding.UTF8.GetBytes(password);\n        return KdfShape.Hex(sha.ComputeHash(bytes));\n    }\n\n    public static bool Verify(string password, byte[] salt, string storedHex)\n    {\n        if (salt == null || salt.Length < 16 || storedHex == null) return false;\n        using var sha = System.Security.Cryptography.SHA256.Create();\n        return KdfShape.Hex(sha.ComputeHash(\n            System.Text.Encoding.UTF8.GetBytes(password))) == storedHex;\n    }\n}\n',
        ),
        (
            "csi-p21-log-scrub",
            'public static class Solution\n{\n    public static string Audit(string action, string email)\n    {\n        // identity is never echoed; absence of identity is fine\n        return action + " email=***";\n    }\n}\n',
            'public static class Solution\n{\n    public static string Audit(string action, string email)\n    {\n        // near-miss: masks when the email "looks like" an email — everything\n        // else (ids, names, anything at all) is pasted raw\n        if (email != null && email.Contains("@"))\n            return action + " email=***";\n        return action + " email=" + (email ?? "");\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m21",
    "Checkpoint — The Hardened User Store",
    "Compose the module: register users with per-user salts and PBKDF2, verify credentials, keep the lookup data-only, and confine every file request — one store, all the barriers.",
    30,
    r"""
## The gate (mini-build)

A `SecureUserStore` + file gateway, security-graded:

1. `Register(username, password, byte[] salt)` — stores the PBKDF2 hash
   (`KdfShape.Derive(password, salt, 100_000)`, hex via `KdfShape.Hex`);
   registering an existing username throws `System.InvalidOperationException`.
2. `Validate(username, password)` — true only for an existing user whose
   recomputed hash matches; unknown user or wrong password → `false`, never
   throws.
3. Per-user salting — two users with the same password but different salts
   must end up with *different* stored hashes (the test reads the store via
   `HashOf(username)` and compares against the PBKDF2 reference).
4. `FindUsername(string raw)` — treats the input strictly as data and returns
   the matching username or `null` (an injection-shaped input is just a
   non-existent username — the store is parameterized by construction).
5. `OpenFile(string baseDir, string userPath)` — returns the resolved path or
   `null` when it escapes (same rule as the practice set).

```csharp
public static class Solution
{
    public static void Register(string username, string password, byte[] salt);
    public static bool Validate(string username, string password);
    public static string HashOf(string username);          // stored hash, for the test
    public static string FindUsername(string raw);         // data, not query text
    public static string OpenFile(string baseDir, string userPath);
}
// provided: KdfShape.Derive / KdfShape.Hex (PBKDF2-SHA256, 32 bytes)
```""",
    "Checkpoint — Kho Người Dùng Được Gia cố",
    "Ghép cả module: đăng ký người dùng với salt theo từng người và PBKDF2, xác minh thông tin xác thực, giữ lookup thuần dữ liệu, và giới hạn mọi yêu cầu tệp — một kho, đầy đủ rào chắn.",
    r"""
## Cổng kiểm tra (mini-build)

`SecureUserStore` + cổng tệp, chấm theo bảo mật:

1. `Register(username, password, byte[] salt)` — lưu hash PBKDF2
   (`KdfShape.Derive(password, salt, 100_000)`, hex qua `KdfShape.Hex`);
   đăng ký username đã tồn tại ném `System.InvalidOperationException`.
2. `Validate(username, password)` — true chỉ khi người dùng tồn tại và hash
   tính lại khớp; người lạ hoặc sai mật khẩu → `false`, không ném exception.
3. Salt theo người dùng — hai người dùng cùng mật khẩu, salt khác nhau phải có
   hash *khác nhau* (test đọc qua `HashOf(username)` và đối chiếu với tham
   chiếu PBKDF2).
4. `FindUsername(string raw)` — coi input thuần là dữ liệu, trả username khớp
   hoặc `null` (input dạng injection chỉ là username không tồn tại — kho được
   tham số hóa từ gốc).
5. `OpenFile(string baseDir, string userPath)` — trả đường dẫn đã resolve hoặc
   `null` khi thoát ra ngoài (cùng quy tắc với practice set).

Xem chữ ký `Solution` trong bản tiếng Anh.
""",
    challenge(
        "csi-checkpoint-m21-task",
        "Build the Hardened User Store",
        "Register/Validate with per-user salted PBKDF2, duplicate-register rejection, data-only lookup, and confined file resolution.",
        CS_PRELUDE + KDF_NOTE,
        [
            (
                "register then validate, right and wrong",
                r"""
var salt = new byte[16]; for (int i = 0; i < 16; i++) salt[i] = (byte)i;
Solution.Register("ada", "lovelace", salt);
Cj.True(Solution.Validate("ada", "lovelace"), "correct credentials");
Cj.True(!Solution.Validate("ada", "lovelace2"), "wrong password");
Cj.True(!Solution.Validate("grace", "lovelace"), "unknown user");
""",
                "Validation is recompute-with-stored-salt and compare.",
            ),
            (
                "stored hash is the PBKDF2 reference, salted per user",
                r"""
var s1 = new byte[16]; for (int i = 0; i < 16; i++) s1[i] = (byte)(i + 1);
var s2 = new byte[16]; for (int i = 0; i < 16; i++) s2[i] = (byte)(i + 2);
Solution.Register("u1", "same-pass", s1);
Solution.Register("u2", "same-pass", s2);
Cj.Eq(Solution.HashOf("u1"), KdfShape.Hex(KdfShape.Derive("same-pass", s1, 100_000)), "u1 hash");
Cj.True(Solution.HashOf("u1") != Solution.HashOf("u2"), "same password, different salt, different hash");
""",
                "Per-user salt makes identical passwords hash differently.",
            ),
            (
                "duplicate registration throws",
                r"""
var salt = new byte[16]; for (int i = 0; i < 16; i++) salt[i] = 7;
Solution.Register("dup", "pw", salt);
bool threw = false;
try { Solution.Register("dup", "other", salt); }
catch (System.InvalidOperationException) { threw = true; }
Cj.True(threw, "duplicate user rejected");
""",
                "Registration is create-only; conflicts throw.",
            ),
            (
                "lookup treats input as data",
                r"""
var salt = new byte[16]; for (int i = 0; i < 16; i++) salt[i] = 9;
Solution.Register("lookup-me", "pw", salt);
Cj.Eq(Solution.FindUsername("lookup-me"), "lookup-me", "exact match found");
Cj.Eq(Solution.FindUsername("' OR '1'='1"), null, "injection text is just an unknown username");
""",
                "The store has no query text to inject into.",
            ),
            (
                "file gateway confines traversal",
                r"""
var ok = Solution.OpenFile("/app/data", "notes/today.txt");
Cj.True(ok != null && ok.EndsWith("notes/today.txt"), "inside is served");
Cj.Eq(Solution.OpenFile("/app/data", "../../etc/passwd"), null, "escape refused");
""",
                "Resolve, then confine — same barrier as the practice set.",
            ),
        ],
        level="mini-build",
        difficulty="intermediate",
    ),
    vi_challenge(
        "Dựng kho người dùng được gia cố",
        "Register/Validate với PBKDF2 có salt theo từng người dùng, từ chối đăng ký trùng, lookup thuần dữ liệu (không phải SQL), và resolve tệp có giới hạn.",
        [
            ("register then validate, right and wrong", "Xác minh là tính lại với salt đã lưu rồi so sánh."),
            ("stored hash is the PBKDF2 reference, salted per user", "Salt theo người dùng làm mật khẩu giống nhau hash khác nhau."),
            ("duplicate registration throws", "Đăng ký là create-only; xung đột ném exception."),
            ("lookup treats input as data", "Kho không có văn bản query để injection vào."),
            ("file gateway confines traversal", "Resolve rồi giới hạn — cùng rào chắn với practice set."),
        ],
    ),
    solution='public static class Solution\n{\n    private static readonly System.Collections.Generic.Dictionary<string, (byte[] Salt, string Hash)> Users\n        = new System.Collections.Generic.Dictionary<string, (byte[], string)>();\n\n    private static void Require(byte[] salt)\n    {\n        if (salt == null || salt.Length < 16)\n            throw new System.ArgumentException("salt must be at least 16 bytes");\n    }\n\n    public static void Register(string username, string password, byte[] salt)\n    {\n        Require(salt);\n        if (Users.ContainsKey(username))\n            throw new System.InvalidOperationException("user exists");\n        Users[username] = (salt, KdfShape.Hex(KdfShape.Derive(password, salt, 100_000)));\n    }\n\n    public static bool Validate(string username, string password)\n    {\n        if (!Users.TryGetValue(username, out var rec)) return false;\n        return KdfShape.Hex(KdfShape.Derive(password, rec.Salt, 100_000)) == rec.Hash;\n    }\n\n    public static string HashOf(string username)\n    {\n        return Users.TryGetValue(username, out var rec) ? rec.Hash : null;\n    }\n\n    public static string FindUsername(string raw)\n    {\n        // input is data: an exact dictionary lookup, no query text involved\n        return Users.ContainsKey(raw) ? raw : null;\n    }\n\n    public static string OpenFile(string baseDir, string userPath)\n    {\n        if (string.IsNullOrEmpty(userPath)) return null;\n        var baseFull = System.IO.Path.GetFullPath(baseDir);\n        var full = System.IO.Path.GetFullPath(\n            System.IO.Path.Combine(baseFull, userPath));\n        var prefix = baseFull.EndsWith(System.IO.Path.DirectorySeparatorChar.ToString())\n            ? baseFull\n            : baseFull + System.IO.Path.DirectorySeparatorChar;\n        if (!full.StartsWith(prefix) || full == baseFull) return null;\n        return full;\n    }\n}\n',
    wrong='public static class Solution\n{\n    private static readonly System.Collections.Generic.Dictionary<string, string> Users\n        = new System.Collections.Generic.Dictionary<string, string>();\n\n    public static void Register(string username, string password, byte[] salt)\n    {\n        if (Users.ContainsKey(username))\n            throw new System.InvalidOperationException("user exists");\n        // near-miss: validates the salt, then ignores it — hashes depend only\n        // on the password, so identical passwords collide across users\n        if (salt == null || salt.Length < 16)\n            throw new System.ArgumentException("salt must be at least 16 bytes");\n        Users[username] = KdfShape.Hex(KdfShape.Derive(password, new byte[16], 100_000));\n    }\n\n    public static bool Validate(string username, string password)\n    {\n        if (!Users.TryGetValue(username, out var hash)) return false;\n        return KdfShape.Hex(KdfShape.Derive(password, new byte[16], 100_000)) == hash;\n    }\n\n    public static string HashOf(string username)\n    {\n        return Users.TryGetValue(username, out var hash) ? hash : null;\n    }\n\n    public static string FindUsername(string raw)\n    {\n        return Users.ContainsKey(raw) ? raw : null;\n    }\n\n    public static string OpenFile(string baseDir, string userPath)\n    {\n        // near-miss: string-level rejection, no resolution, no confinement\n        if (userPath != null && userPath.Contains("..")) return null;\n        return System.IO.Path.Combine(baseDir, userPath ?? "");\n    }\n}\n',
)

print("module 21 authored")
