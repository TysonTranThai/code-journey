"""Module 21 — Advanced security (csa-m21)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-security",
        "Advanced Security",
        "Crypto API discipline, secret handling, injection and deserialization defenses — threat modeling for C# services.",
    )

    csa.register_lesson(
        MID, "csa-m21-crypto", "Cryptographic APIs used correctly",
        "RandomNumberGenerator, password hashing (PBKDF2), AEAD vs plain hashing — the API-level discipline.",
        16, "advanced", _m21_crypto, _m21_crypto_vi,
    )
    csa.register_lesson(
        MID, "csa-m21-secrets", "Secrets and token handling",
        "Where secrets live, how they leak, and the lifetime rules for tokens and keys.",
        15, "advanced", _m21_secrets, _m21_secrets_vi,
    )
    csa.register_lesson(
        MID, "csa-m21-injection", "Injection and unsafe deserialization",
        "SQL/command injection mechanics, safe deserialization posture, and path traversal.",
        16, "advanced", _m21_injection, _m21_injection_vi,
    )
    csa.register_lesson(
        MID, "csa-m21-threat-model", "Threat modeling a service",
        "STRIDE-lite on a concrete API: trust boundaries, the top risks, and the defenses this course taught.",
        15, "advanced", _m21_threat, _m21_threat_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m21", "Checkpoint: security",
        "Synthesis: constant-time verification, safe storage decisions, injection prevention.",
        12, "advanced", _m21_checkpoint, _m21_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m21-task", MID,
        title='Checkpoint: security discipline',
        prompt=(
            'Implement `static byte[] RandomSalt(int bytes)` using RandomNumberGenerator, and `static string HashPassword(string password, byte[] salt)` returning Base64 of Rfc2898DeriveBytes(Pbkdf2) with 100_000 iterations, SHA256, 32-byte output. Then implement `static bool VerifyPassword(string password, byte[] salt, string expectedBase64)` that recomputes and compares with CryptographicOperations.FixedTimeEquals (the timing-safe comparison the lesson mandates). The tests prove the work factor matters: hashing must actually take measurable time (100k iterations is >= 10ms on this runtime) — a 1-iteration stub is a vulnerability even when the outputs match.'
        ),
        difficulty='advanced',
        tests=[
            {
                "name": 'hash-verify',
                "code": (
                    'var salt = Solution.RandomSalt(16);\nCj.Eq(salt.Length, 16, "salt size");\nvar h1 = Solution.HashPassword("correct horse", salt);\nvar h2 = Solution.HashPassword("correct horse", salt);\nCj.Eq(h1, h2, "deterministic for same salt+password");\nCj.True(Solution.VerifyPassword("correct horse", salt, h1), "correct password verifies");\nCj.False(Solution.VerifyPassword("wrong", salt, h1), "wrong password rejected");'
                ),
                "hint": 'Rfc2898DeriveBytes.Pbkdf2(password, salt, 100_000, HashAlgorithmName.SHA256, 32)',
            },
            {
                "name": 'salt-unique',
                "code": (
                    'var s1 = Solution.RandomSalt(16);\nvar s2 = Solution.RandomSalt(16);\nCj.False(s1.SequenceEqual(s2), "two salts differ (cryptographic randomness)");\nvar h1 = Solution.HashPassword("same password", s1);\nvar h2 = Solution.HashPassword("same password", s2);\nCj.False(h1 == h2, "same password + different salt = different hash (rainbow-table defense)");\n// cryptographic RNG must not be seed-replayable: the most common seed (0)\n// must not reproduce the salt stream\nvar replay = new byte[16];\nnew Random(0).NextBytes(replay);\nCj.False(replay.SequenceEqual(s1), "salt must not match a seeded System.Random stream");\nCj.False(replay.SequenceEqual(s2), "salt must not match a seeded System.Random stream (2)");'
                ),
                "hint": 'RandomNumberGenerator.GetBytes(16) — never new Random() for secrets.',
            },
            {
                "name": 'work-factor',
                "code": (
                    '// The 100_000-iteration work factor IS the security: it makes offline guessing expensive.\n// On this runtime one Pbkdf2 pass at 100k iterations takes well over 10ms; a 1-iteration\n// stub (same outputs, "still works") finishes in microseconds.\nvar salt = Solution.RandomSalt(16);\nvar sw = System.Diagnostics.Stopwatch.StartNew();\nSolution.HashPassword("cost matters", salt);\nsw.Stop();\nCj.True(sw.ElapsedMilliseconds >= 10, $"100k iterations must cost real time, got {sw.ElapsedMilliseconds}ms");'
                ),
                "hint": 'Keep the iteration count at 100_000 — the cost is the defense.',
            },
        ],
        reference=(
            'using System.Security.Cryptography;\n\npublic class Solution\n{\n    public static byte[] RandomSalt(int bytes)\n        => RandomNumberGenerator.GetBytes(bytes);\n\n    public static string HashPassword(string password, byte[] salt)\n    {\n        var hash = Rfc2898DeriveBytes.Pbkdf2(password, salt, 100_000, HashAlgorithmName.SHA256, 32);\n        return Convert.ToBase64String(hash);\n    }\n\n    public static bool VerifyPassword(string password, byte[] salt, string expectedBase64)\n    {\n        var computed = Convert.FromBase64String(HashPassword(password, salt));\n        var expected = Convert.FromBase64String(expectedBase64);\n        return CryptographicOperations.FixedTimeEquals(computed, expected);\n    }\n}'
        ),
        wrong=(
            'using System.Security.Cryptography;\n\npublic class Solution\n{\n    public static byte[] RandomSalt(int bytes)\n    {\n        var rng = new Random();   // WRONG: predictable, not cryptographic\n        var salt = new byte[bytes];\n        rng.NextBytes(salt);\n        return salt;\n    }\n\n    public static string HashPassword(string password, byte[] salt)\n    {\n        var hash = Rfc2898DeriveBytes.Pbkdf2(password, salt, 1, HashAlgorithmName.SHA256, 32);   // WRONG: 1 iteration\n        return Convert.ToBase64String(hash);\n    }\n\n    public static bool VerifyPassword(string password, byte[] salt, string expectedBase64)\n        => HashPassword(password, salt) == expectedBase64;   // WRONG: timing-leaky comparison\n}'
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p21-sec", "Security drills",
        "Timing-safe comparison, path traversal defense, deserialization posture, and token-lifetime reasoning.",
        45, "advanced", "csa-m21-injection",
        ["csa-p21-path-traversal", "csa-p21-parameterized-query"],
    )
    csa.register_challenge(
        "csa-p21-path-traversal", MID,
        title="Defeat path traversal",
        prompt=(
            "Implement `static string SafeJoin(string baseDir, string userInput)` that joins a user-supplied "
            "relative filename onto a base directory but REJECTS traversal: normalize the combined path "
            "(Path.GetFullPath) and throw UnauthorizedAccessException if the result does not start with the "
            "normalized base (allowing the base to end with a separator). \"report.pdf\" passes; "
            "\"..\\..\\etc\\passwd\" and absolute paths fail."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "clean-name-passes",
                "code": (
                    "var p = Solution.SafeJoin(\"/srv/data\", \"reports/q1.pdf\");\n"
                    'Cj.True(p.Replace(\'\\\\\', \'/\').EndsWith("reports/q1.pdf"), "subdirectory allowed");'
                ),
                "hint": "var full = Path.GetFullPath(Path.Combine(baseDir, userInput)); var baseFull = Path.GetFullPath(baseDir); if (!full.StartsWith(baseFull)) throw new UnauthorizedAccessException();",
            },
            {
                "name": "traversal-rejected",
                "code": (
                    "var ex1 = await Cj.ThrowsAsync<UnauthorizedAccessException>(() => Task.Run(() => Solution.SafeJoin(\"/srv/data\", \"../../etc/passwd\")));\n"
                    "var ex2 = await Cj.ThrowsAsync<UnauthorizedAccessException>(() => Task.Run(() => Solution.SafeJoin(\"/srv/data\", \"/etc/passwd\")));\n"
                    'Cj.True(ex1 is not null && ex2 is not null, "both traversal forms rejected");'
                ),
                "hint": "Path.Combine + GetFullPath normalizes ..; the prefix check catches both relative traversal and absolute escapes.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static string SafeJoin(string baseDir, string userInput)\n"
            "    {\n"
            "        var baseFull = Path.GetFullPath(baseDir);\n"
            "        if (!baseFull.EndsWith(Path.DirectorySeparatorChar)) baseFull += Path.DirectorySeparatorChar;\n"
            "        var full = Path.GetFullPath(Path.Combine(baseFull, userInput));\n"
            "        if (!full.StartsWith(baseFull, StringComparison.Ordinal))\n"
            "            throw new UnauthorizedAccessException($\"path escapes base: {userInput}\");\n"
            "        return full;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static string SafeJoin(string baseDir, string userInput)\n"
            "    {\n"
            "        // WRONG: blacklisting \"..\" misses encoded/absolute forms and normalized tricks\n"
            "        if (userInput.Contains(\"..\")) throw new UnauthorizedAccessException();\n"
            "        return Path.Combine(baseDir, userInput);\n"
            "    }\n}"
        ),
        level="real-world",
    )
    csa.register_challenge(
        "csa-p21-parameterized-query", MID,
        title="Parameterize or fail",
        prompt=(
            "SQL injection is string concatenation meeting user input. Implement `static string BuildQuery(string "
            "tableName, string userInput)` that returns a SAFE parameterized-style SQL text: \"SELECT * FROM \" + "
            "validated table + \" WHERE name = @name\" — validating the table against an allow-list {\"orders\", "
            "\"customers\"} (throw ArgumentException otherwise) and NEVER embedding userInput into the string "
            "(@name stays a placeholder). Implement `static bool IsSafeQuery(string sql)` that returns false if "
            "the sql contains a quote character (proof that user data was interpolated)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "placeholder-not-interpolated",
                "code": (
                    "var q = Solution.BuildQuery(\"orders\", \"O'Brien; DROP TABLE orders--\");\n"
                    'Cj.True(q.Contains("@name"), "placeholder preserved");\n'
                    'Cj.False(q.Contains("O\'Brien"), "user input never interpolated");\n'
                    'Cj.True(Solution.IsSafeQuery(q), "no quotes = no interpolation");'
                ),
                "hint": "Validate table against allow-list; return $\"SELECT * FROM {table} WHERE name = @name\" — user input never enters the string.",
            },
            {
                "name": "table-allowlist",
                "code": (
                    "var ex = await Cj.ThrowsAsync<ArgumentException>(() => Task.Run(() => Solution.BuildQuery(\"users; DROP TABLE orders\", \"x\")));\n"
                    'Cj.True(ex is not null, "non-allow-listed table rejected");'
                ),
                "hint": "Table names cannot be parameters — allow-list them.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    private static readonly HashSet<string> AllowedTables = new() { \"orders\", \"customers\" };\n\n"
            "    public static string BuildQuery(string tableName, string userInput)\n"
            "    {\n"
            "        if (!AllowedTables.Contains(tableName))\n"
            "            throw new ArgumentException($\"table not allowed: {tableName}\");\n"
            "        // userInput is bound via the @name parameter at execution time — never string-formatted in.\n"
            "        _ = userInput;\n"
            "        return $\"SELECT * FROM {tableName} WHERE name = @name\";\n"
            "    }\n\n"
            "    public static bool IsSafeQuery(string sql) => !sql.Contains('\"') && !sql.Contains('\\'');\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static string BuildQuery(string tableName, string userInput)\n"
            "    {\n"
            "        // WRONG: direct interpolation — the classic injection\n"
            "        return $\"SELECT * FROM {tableName} WHERE name = '{userInput}'\";\n"
            "    }\n\n"
            "    public static bool IsSafeQuery(string sql) => !sql.Contains(\"DROP\");   // WRONG: blacklist miss-prone\n"
            "}"
        ),
        level="guided",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m21_crypto = r"""## Cryptographic APIs used correctly

Application security is 95% using the platform's crypto primitives with
the right parameters — and 5% avoiding homemade ciphers (which is really
part of the 95%: never write crypto).

**Randomness.** `Random` is seeded by time and predictable — fine for
games, fatal for tokens. `RandomNumberGenerator.GetBytes(n)` (or
`GetItems` for chars) is the only source for secrets: session IDs, salts,
nonces, keys.

**Password hashing** is deliberately slow and salted — the opposite of
every other hash use:

```csharp
// PBKDF2 via Rfc2898DeriveBytes (.NET's built-in work-factor KDF):
var hash = Rfc2898DeriveBytes.Pbkdf2(
    password, salt, iterations: 100_000,
    HashAlgorithmName.SHA256, outputLength: 32);
```

Per-user random salt (stored alongside the hash) kills rainbow tables and
identical-password correlation. The iteration count is the work factor:
raise it as hardware improves; 100k+ is the current floor (OWASP's table
is the reference). Password-specific alternatives — bcrypt, scrypt,
Argon2 — come from packages; the discipline (salt, slow, parameterized)
identical.

**Hashing vs encryption vs AEAD:**

| Need | Primitive | Example |
|---|---|---|
| Integrity only (no secret) | SHA-256 | file checksums |
| Password storage | PBKDF2/bcrypt/Argon2 | login credentials |
| Confidentiality + integrity | AEAD (AES-GCM, ChaCha20-Poly1305) | payload encryption |
| MAC with shared key | HMAC | API signatures |

`AesGcm` (.NET's built-in AEAD) encrypts AND authenticates: tampering
fails the tag check. Plain AES-CBC without a MAC is the classic
padding-oracle bug — if you cannot name why, use AesGcm and move on.

**Comparison**: `CryptographicOperations.FixedTimeEquals` compares
secrets in constant time. `==` on byte arrays short-circuits at the first
differing byte — a timing side channel that leaks how much of a MAC is
correct. The checkpoint enforces the discipline.
"""

_m21_crypto_vi = r"""## Dùng đúng API mật mã

An toàn ứng dụng là 95% dùng primitive mật mã của platform với tham số
đúng — và 5% tránh tự chế thuật toán mã hóa (thực ra 5% đó nằm trong 95%:
không bao giờ tự viết crypto).

**Số ngẫu nhiên.** `Random` được seed theo thời gian và đoán được — ổn cho
game, chết người cho token. `RandomNumberGenerator.GetBytes(n)` (hoặc
`GetItems` cho ký tự) là nguồn duy nhất cho mật mã: session ID, salt,
nonce, key.

**Hash mật khẩu** cố ý chậm và có muối — ngược với mọi cách dùng hash khác:

```csharp
// PBKDF2 qua Rfc2898DeriveBytes (KDF có work-factor của .NET):
var hash = Rfc2898DeriveBytes.Pbkdf2(
    password, salt, iterations: 100_000,
    HashAlgorithmName.SHA256, outputLength: 32);
```

Salt ngẫu nhiên cho từng user (lưu cạnh hash) tiêu diệt rainbow table và
việc liên kết mật khẩu giống nhau. Số vòng lặp là work factor: nâng dần
khi phần cứng tiến bộ; 100k+ là sàn hiện tại (bảng của OWASP là tham
chiếu). Các lựa chọn chuyên cho mật khẩu — bcrypt, scrypt, Argon2 — đến từ
package; kỷ luật (salt, chậm, tham số hóa) thì giống hệt.

**Hash vs mã hóa vs AEAD:**

| Nhu cầu | Primitive | Ví dụ |
|---|---|---|
| Chỉ toàn vẹn (không bí mật) | SHA-256 | checksum file |
| Lưu mật khẩu | PBKDF2/bcrypt/Argon2 | thông tin đăng nhập |
| Bảo mật + toàn vẹn | AEAD (AES-GCM, ChaCha20-Poly1305) | mã hóa payload |
| MAC với key dùng chung | HMAC | chữ ký API |

`AesGcm` (AEAD có sẵn trong .NET) mã hóa VÀ xác thực: can thiệp sẽ fail ở
phần kiểm tra tag. AES-CBC thuần không có MAC là bug padding-oracle kinh
điển — nếu bạn không gọi được tên lý do, dùng AesGcm và đi tiếp.

**So sánh**: `CryptographicOperations.FixedTimeEquals` so sánh bí mật trong
thời gian không đổi. `==` trên mảng byte thoát sớm ở byte khác đầu tiên —
một kênh phụ timing làm lộ bao nhiêu phần trăm của một MAC là đúng.
Checkpoint ép kỷ luật này.
"""

_m21_secrets = r"""## Secrets and token handling

Secrets are credentials: passwords, API keys, connection strings,
certificates, signing keys. The lifecycle rules that keep them yours:

**Storage.** Secrets never live in source control (`.env` files in repos
are how keys leak — the repo outlives the rotation schedule), never in
logs, never in exception messages, never in URLs. In production: a secret
store (cloud key vaults, Docker secrets, mounted files) injected as
environment or file references the app reads at startup. In development:
user-secrets (`dotnet user-secrets`), which lives outside the repo.

**Rotataion and blast radius.** Assume every secret leaks eventually. The
design questions: how fast can it be rotated (minutes, not redeploys), and
what else does it unlock (one scoped key per dependency beats one
master key)? Short-lived credentials beat long-lived ones — that is the
entire pitch of workload identity / OIDC federation.

**Tokens.** Bearer tokens (JWT or opaque) are time-boxed authority:

- Short expiry (minutes) with refresh — a leaked access token dies quickly.
- Audience + issuer checks on every verification — a token minted for
  service A must not authorize service B (the confused-deputy bug).
- Sign, never encrypt-then-forget-verification; verify algorithm
  allow-list explicitly (`alg: none` and algorithm-confusion attacks are
  real).
- Opaque tokens verified server-side trade a lookup for revocability; JWTs
  trade revocability for zero lookup. Pick per use case — but pick, and
  write the decision down.

**Logging discipline** is half of secret safety in practice: structured
log scrubbers that redact keys before emission, and the code-review rule
that `ToString()` on a credentials object never goes near a log line.
"""

_m21_secrets_vi = r"""## Quản lý secret và token

Secret là thông tin xác thực: mật khẩu, API key, connection string,
chứng thư, key ký. Các luật vòng đời giữ chúng thuộc về bạn:

**Lưu trữ.** Secret không bao giờ nằm trong source control (file `.env`
trong repo là cách key rò rỉ — repo sống lâu hơn lịch xoay vòng), không
bao giờ trong log, không bao giờ trong exception message, không bao giờ
trong URL. Trong production: secret store (key vault trên cloud, Docker
secrets, file mount) được inject qua environment hoặc tham chiếu file mà
app đọc khi khởi động. Trong phát triển: user-secrets (`dotnet
user-secrets`), nằm ngoài repo.

**Xoay vòng và bán kính thiệt hại.** Hãy giả định mọi secret cuối cùng
cũng rò rỉ. Các câu hỏi thiết kế: xoay vòng nhanh được bao nhiêu (vài phút,
không phải redeploy), và nó mở khóa được những gì (một key có phạm vi hẹp
cho mỗi phụ thuộc đánh bại một master key)? Credential ngắn hạn đánh bại
credential dài hạn — đó là toàn bộ thông điệp của workload identity /
OIDC federation.

**Token.** Bearer token (JWT hoặc opaque) là quyền hạn có thời hạn:

- Hết hạn ngắn (vài phút) kèm refresh — token truy cập bị lộ chết nhanh.
- Kiểm tra audience + issuer cho mọi lần xác minh — token cấp cho service A
  không được cấp quyền cho service B (bug confused-deputy).
- Ký, đừng mã-hóa-rồi-quên-xác-minh; xác minh danh sách thuật toán được
  phép tường minh (tấn công `alg: none` và algorithm-confusion là có thật).
- Token opaque xác minh phía server đổi một lần tra DB lấy khả năng thu hồi;
  JWT đổi khả năng thu hồi lấy việc không cần tra. Chọn theo use case —
  nhưng phải chọn, và ghi quyết định ra.

**Kỷ luật logging** chiếm một nửa sự an toàn của secret trong thực tế: bộ
scrubber log có cấu trúc xóa key trước khi phát, và luật review rằng
`ToString()` trên object credential không bao giờ đến gần một dòng log.
"""

_m21_injection = r"""## Injection and unsafe deserialization

Injection is the bug class where data becomes code. Three families this
course drills:

**SQL injection.** User input concatenated into SQL text changes its
meaning (`' OR '1'='1`, `'; DROP TABLE x--`). The defense is structural,
not string-shaped: **parameterized queries** — the driver ships values
out-of-band, so data can never re-enter the SQL grammar. The practice
drill shows the shape: the user input lives in `@name`, never in the
string. Table/column names cannot be parameters (they are identifiers) —
so they come from allow-lists, never from users. ORMs (EF Core) parameterize
by default; the risk resurfaces in raw-SQL escape hatches.

**Path traversal.** `Path.Combine(base, "../../etc/passwd")` escapes the
base. The defense is *normalize-then-verify*: GetFullPath the combined
path and require it to start with the (normalized) base — the checkpoint's
`SafeJoin`. Blacklisting `..` misses URL-encoded, double-encoded, and
absolute-path forms; the prefix check does not.

**Unsafe deserialization.** Deserializing attacker-controlled data into
types that EXECUTE (`BinaryFormatter` — the canonical .NET disaster,
removed from the platform for a reason) hands over control. The posture:

1. Never deserialize untrusted data with type-autonomous formatters.
2. JSON (System.Text.Json) to POCOs is safe by default — data becomes
   data. Configure limits: max depth, max content.
3. Deserialization still needs validation: a 2GB string field is a DoS
   without a size cap.

**Command injection** rounds the family out: `Process.Start("sh", "-c "
+ userInput)` is SQL injection with a shell. Argument arrays (no shell)
and allow-lists are the fix.

The unifying principle: **the grammar boundary is the defense.** Keep data
on its side of the grammar — parameters for values, allow-lists for
identifiers, validators for paths — and no payload can cross it. Defense
in depth (least-privilege DB users, WAFs) buys time, but the boundary is
the fix.
"""

_m21_injection_vi = r"""## Injection và deserialization không an toàn

Injection là lớp bug nơi dữ liệu trở thành code. Ba họ mà khóa học luyện:

**SQL injection.** User input được nối vào chuỗi SQL thay đổi ý nghĩa của
nó (`' OR '1'='1`, `'; DROP TABLE x--`). Phòng thủ mang tính cấu trúc,
không phải dạng chuỗi: **parameterized query** — driver vận chuyển giá trị
ngoài luồng, nên dữ liệu không thể quay lại ngữ pháp SQL. Drill practice
cho thấy hình dạng: user input nằm trong `@name`, không bao giờ trong
chuỗi. Tên bảng/cột không thể là tham số (chúng là định danh) — nên chúng
đến từ allow-list, không bao giờ từ user. ORM (EF Core) parameterize theo
mặc định; rủi ro quay lại ở các lối thoát raw-SQL.

**Path traversal.** `Path.Combine(base, "../../etc/passwd")` thoát khỏi
base. Phòng thủ là *chuẩn hóa-rồi-xác-minh*: GetFullPath đường dẫn kết hợp
và yêu cầu nó bắt đầu bằng (bản chuẩn hóa của) base — `SafeJoin` trong
checkpoint. Blacklist `..` bỏ sót các dạng URL-encoded, double-encoded, và
đường tuyệt đối; phép kiểm tra tiền tố thì không.

**Deserialization không an toàn.** Deserializing dữ liệu do kẻ tấn công
kiểm soát vào các kiểu THỰC THI (`BinaryFormatter` — thảm họa kinh điển
của .NET, bị loại khỏi platform vì một lý do) là giao nòi quyền kiểm soát.
Thế phòng thủ:

1. Không bao giờ deserializing dữ liệu không tin cậy bằng formatter tự do
   chọn kiểu.
2. JSON (System.Text.Json) vào POCO an toàn theo mặc định — dữ liệu thành
   dữ liệu. Cấu hình giới hạn: độ sâu tối đa, dung lượng tối đa.
3. Deserialization vẫn cần xác thực: một trường string 2GB là DoS nếu
   không có trần kích thước.

**Command injection** khép lại họ: `Process.Start("sh", "-c " + userInput)`
là SQL injection có shell. Mảng đối số (không shell) và allow-list là cách
sửa.

Nguyên tắc thống nhất: **biên ngữ pháp là phòng thủ.** Giữ dữ liệu ở phía
của nó trong ngữ pháp — tham số cho giá trị, allow-list cho định danh,
validator cho đường dẫn — và không payload nào vượt qua được. Phòng thủ
tầng sâu (user DB đặc-quyền-tối-thiểu, WAF) mua thời gian, nhưng biên
ngữ pháp mới là bản sửa.
"""

_m21_threat = r"""## Threat modeling a service

Threat modeling is deciding where you are worth attacking and what you
owe each attacker. The lite version that fits in a design doc:

**1. Diagram the trust boundaries.** Internet → API gateway → service →
database. Cache, queue, secret store are actors too. Every arrow is a
place data crosses authority.

**2. Enumerate per boundary (STRIDE-lite):**

| Threat | Question | Typical defense |
|---|---|---|
| Spoofing | can someone claim an identity? | authn (tokens, mTLS) |
| Tampering | can data be modified in transit/at rest? | TLS, AEAD, signatures |
| Repudiation | can actions be denied? | audit logs, correlation IDs |
| Information disclosure | can data leak? | authz, encryption, log scrubbing |
| Denial of service | can resources be exhausted? | rate limits, timeouts, quotas |
| Elevation of privilege | can a user become more? | least privilege, allow-lists |

**3. Rank by (impact, likelihood)** and spend engineering where the
product implies exposure. An internal analytics tool and a payment API
have different top-three lists — modeling is per system, not per industry.

**4. Write the invariants down.** "No unauthenticated request reaches the
database." "Every secret rotates in under 15 minutes." "PII never appears
in logs." Invariants are testable — the good ones become automated checks
(this course's challenges are exactly that, miniaturized).

The failure mode of threat modeling is the exercise that happens once and
expires. The working version: a living diagram, a top-risks list reviewed
per feature, and invariants expressed as tests. Security is then a property
the build verifies — which is the only kind that survives team turnover.
"""

_m21_threat_vi = r"""## Threat modeling cho một service

Threat modeling là quyết định bạn đáng bị tấn công ở đâu và bạn nợ mỗi kẻ
tấn công điều gì. Bản lite vừa đủ trong một tài liệu thiết kế:

**1. Vẽ các biên tin cậy.** Internet → API gateway → service → database.
Cache, queue, secret store cũng là tác nhân. Mọi mũi tên là một nơi dữ liệu
vượt qua thẩm quyền.

**2. Kể tên theo từng biên (STRIDE-lite):**

| Mối đe dọa | Câu hỏi | Phòng thủ điển hình |
|---|---|---|
| Spoofing | ai đó có thể nhận danh tính? | authn (token, mTLS) |
| Tampering | dữ liệu có thể bị sửa khi truyền/khi lưu? | TLS, AEAD, chữ ký |
| Repudiation | hành động có thể bị chối bỏ? | audit log, correlation ID |
| Information disclosure | dữ liệu có thể rò rỉ? | authz, mã hóa, scrub log |
| Denial of service | tài nguyên có thể bị cạn? | rate limit, timeout, quota |
| Elevation of privilege | user có thể thành người lớn hơn? | đặc quyền tối thiểu, allow-list |

**3. Xếp hạng theo (tác động, khả năng)** và tiêu engineering nơi sản phẩm
ngụ ý mức phơi bày. Một công cụ phân tích nội bộ và một API thanh toán có
hai danh sách top-3 khác nhau — modeling là theo hệ thống, không phải theo
ngành.

**4. Ghi các bất biến ra giấy.** "Không request chưa xác thực tới được
database." "Mọi secret xoay vòng trong 15 phút." "PII không bao giờ xuất
hiện trong log." Bất biến là thứ test được — những cái tốt trở thành kiểm
tra tự động (các thử thách của khóa học chính xác là điều đó, ở bản thu
nhỏ).

Kiểu thất bại của threat modeling là bài tập diễn ra một lần rồi hết hạn.
Bản đang hoạt động: sơ đồ sống, danh sách rủi ro hàng đầu được rà mỗi
feature, và bất biến được diễn đạt thành test. Khi đó an toàn là một tính
chất mà build xác minh — loại duy nhất sống sót qua các lần thay đổi nhân
sự.
"""

_m21_checkpoint = r"""## Checkpoint: security

The graded task pairs PBKDF2 password hashing with the timing-safe
verification discipline, then proves salt uniqueness. Practice adds the
normalize-then-verify path traversal defense and the parameterized-query
boundary — the grammar rule made executable.
"""

_m21_checkpoint_vi = r"""## Checkpoint: an toàn

Bài được chấm ghép hash mật khẩu PBKDF2 với kỷ luật xác minh an-toàn-timing,
rồi chứng minh tính duy nhất của salt. Practice thêm phòng thủ path
traversal theo kiểu chuẩn-hóa-rồi-xác-minh và biên parameterized-query —
luật ngữ pháp trở thành thứ thực thi được."""
