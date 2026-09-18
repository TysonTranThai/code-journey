#!/usr/bin/env python3
"""Java — Advanced — Module 13: javaa-security-threats.

Security as engineering: canonicalization before validation (path traversal),
constant-time comparison and salted hashing (auth), allowlist-vs-blacklist
(SSRF), least privilege, and secret hygiene. The checkpoint — a request
firewall with a threat-model registry. All examples are safe, deterministic,
educational constructions. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-security-threats"

L_VALID_EN = """
**Validate the canonical form, never the input string.** Path traversal:
`..%2F..%2Fetc%2Fpasswd` decoded and normalized is `/etc/passwd` — a filter
that rejects `..` on the RAW string sees neither the dots nor the slashes.

```java
Path root = baseDir.toAbsolutePath().normalize();
Path target = root.resolve(userPath).normalize();
if (!target.startsWith(root)) throw new SecurityException("traversal");
```

`resolve` + `normalize` produce the canonical path; the *containment check*
then answers the only question that matters: is the result still inside the
root? Note what this rejects that string filters miss: `docs/../secrets`,
absolute escapes, encoding tricks (already decoded by the time you see the
String), symlinks resolved by the filesystem itself.

The same shape applies to SSRF: never blacklist bad hosts (infinite), allowlist
the hosts you mean (finite). `URL.openStream()` on a user-supplied URL can
reach `http://169.254.169.254/` (cloud metadata) or `http://localhost:8080/`
(your own admin) — the fix is resolving the host against an allowlist BEFORE
any I/O.
"""
L_VALID_VI = """
**Kiểm duyệt dạng chuẩn, không bao giờ duyệt chuỗi thô.** Path traversal:
`..%2F..%2Fetc%2Fpasswd` sau khi decode và normalize là `/etc/passwd` — bộ lọc
từ chối `..` trên chuỗi RAW không thấy chấm nào lẫn slash nào.

```java
Path root = baseDir.toAbsolutePath().normalize();
Path target = root.resolve(userPath).normalize();
if (!target.startsWith(root)) throw new SecurityException("traversal");
```

`resolve` + `normalize` tạo ra path chuẩn; *kiểm tra bao chứa* rồi trả lời câu
hỏi duy nhất quan trọng: kết quả còn nằm trong root không? Chú ý điều này từ
chối mà bộ lọc chuỗi bỏ lỡ: `docs/../secrets`, thoát bằng đường tuyệt đối, mẹo
mã hóa (đã decode trước khi bạn thấy String), symlink do chính filesystem giải.

Hình dạng tương tự áp dụng cho SSRF: không bao giờ blacklist host xấu (vô hạn),
allowlist những host bạn muốn (hữu hạn). `URL.openStream()` trên URL do người
dùng cung cấp có thể chạm tới `http://169.254.169.254/` (cloud metadata) hoặc
`http://localhost:8080/` (admin của chính bạn) — cách sửa là kiểm tra host với
allowlist TRƯỚC mọi I/O.
"""

L_AUTH_EN = """
Two primitives, both about *information leakage*:

**Timing attacks** compare secrets character-by-character and stop early —
the TIME of the failure leaks how many characters matched. String.equals is
an early-exit compare. Secrets must be compared in **constant time**:

```java
static boolean safeEquals(byte[] a, byte[] b) {
    return MessageDigest.isEqual(a, b);   // JDK built-in: constant-time
}
```

**Rainbow tables** attack unsalted hashes: a precomputed digest of "hunter2"
matches every user who ever used "hunter2". The fix is a PER-USER random salt
mixed into the digest — same password, different stored bytes per user:

```java
byte[] salt = SecureRandom.getInstanceStrong()
    .generateSeed(16);
byte[] hash = sha256(salt, passwordBytes);   // store BOTH
```

Verify by recomputing with the STORED salt and comparing constant-time. For
production password storage the stronger shape is a *slow* KDF (bcrypt/
scrypt/Argon2/PBKDF2) — the sandbox course teaches the salted-digest shape;
the principle scales: cost per guess is a design parameter.
"""
L_AUTH_VI = """
Hai primitive, đều về *rò rỉ thông tin*:

**Tấn công thời gian** so sánh bí mật từng ký tự và dừng sớm — THỜI GIAN thất
bại lộ số ký tự đã khớp. String.equals là so sánh thoát sớm. Bí mật phải được
so sánh theo **thời gian hằng**:

```java
static boolean safeEquals(byte[] a, byte[] b) {
    return MessageDigest.isEqual(a, b);   // có sẵn trong JDK: thời gian hằng
}
```

**Rainbow table** tấn công hash không salt: digest tính sẵn của "hunter2" khớp
với mọi người từng dùng "hunter2". Cách sửa là salt NGẪU NHIÊN theo từng
người dùng trộn vào digest — cùng mật khẩu, byte lưu khác nhau mỗi người:

```java
byte[] salt = SecureRandom.getInstanceStrong()
    .generateSeed(16);
byte[] hash = sha256(salt, passwordBytes);   // lưu CẢ HAI
```

Xác minh bằng cách tính lại với salt ĐÃ LƯU và so sánh thời gian hằng. Cho lưu
mật khẩu production, hình dạng mạnh hơn là KDF *chậm* (bcrypt/scrypt/Argon2/
PBKDF2) — khóa học dạy hình dạng salted-digest trong sandbox; nguyên tắc mở
rộng được: chi phí mỗi lần đoán là một tham số thiết kế.
"""

L_THREAT_EN = """
A threat model is a table you can argue with: *asset* (what's valuable),
*threat* (who/what attacks it), *vector* (how they reach it), *control* (what
stops them), *residual risk* (what remains). Example — a file export feature:

| asset | threat | vector | control | residual |
|---|---|---|---|---|
| user files | traversal read | `..` in name | canonicalize + contain | symlink race |
| session token | replay | stolen cookie | HTTPS + expiry | device theft |
| export job | DoS | 10^9-row export | row cap + timeout | slow-loris |

Least privilege is the cross-cutting control: the export job runs as a
principal that can read user files and NOTHING ELSE — a traversal bug in it
then reads files the principal could reach anyway (still bad, no longer
catastrophic). Secrets (DB URLs, API keys) arrive as environment variables,
never literals; code that logs a secret is a bug even when the secret "was
only internal".

STRIDE is the checklist vocabulary — Spoofing, Tampering, Repudiation,
Information disclosure, Denial of service, Elevation of privilege — not a
substitute for the table, but a prompt that keeps you from missing a column.
"""
L_THREAT_VI = """
Mô hình mối đe dọa là một bảng bạn có thể tranh luận: *tài sản* (cái gì đáng
giá), *mối đe dọa* (ai/cái gì tấn công), *vector* (chúng tới bằng cách nào),
*biện pháp kiểm soát* (cái gì chặn), *rủi ro dư* (cái gì còn lại). Ví dụ —
tính năng xuất tệp:

| tài sản | đe dọa | vector | kiểm soát | dư |
|---|---|---|---|---|
| tệp người dùng | đọc traversal | `..` trong tên | canonicalize + bao chứa | race symlink |
| token phiên | phát lại | cookie bị đánh cắp | HTTPS + hết hạn | mất thiết bị |
| job xuất | DoS | xuất 10^9 dòng | giới hạn dòng + timeout | slow-loris |

Đặc quyền tối thiểu là kiểm soát xuyên suốt: job xuất chạy dưới một principal
chỉ đọc được tệp người dùng và KHÔNG CÓ GÌ KHÁC — lỗi traversal trong nó khi
đó chỉ đọc được những tệp principal vốn chạm tới (vẫn tệ, nhưng không còn thảm
họa). Bí mật (DB URL, API key) đến từ biến môi trường, không bao giờ là literal;
code log ra bí mật là bug ngay cả khi bí mật đó "chỉ nội bộ".

STRIDE là vốn từ checklist — Spoofing, Tampering, Repudiation, Information
disclosure, Denial of service, Elevation of privilege — không thay thế bảng,
chỉ là nhắc nhở để bạn không bỏ sót một cột.
"""

write_module(
    M, "Security & Threat Modeling",
    "Canonicalization, constant-time auth, allowlists, least privilege, and threat models you can argue with.",
    "Bảo mật & Mô hình mối đe dọa",
    "Chuẩn hóa, xác thực thời gian hằng, allowlist, đặc quyền tối thiểu, và mô hình đe dọa có thể tranh luận.",
    ["javaa-canonical-validation", "javaa-auth-primitives", "javaa-threat-modeling"],
    ["javaa-p13-security"],
)

write_lesson(M, "javaa-canonical-validation",
    "Canonicalize, then validate",
    "Path traversal via canonical containment, and SSRF via finite allowlists.",
    16, L_VALID_EN,
    "Chuẩn hóa rồi kiểm duyệt",
    "Path traversal qua bao chứa chuẩn hóa, và SSRF qua allowlist hữu hạn.",
    L_VALID_VI)

write_lesson(M, "javaa-auth-primitives",
    "Auth primitives",
    "Timing-safe comparison and per-user salts — the two primitives behind every credential store.",
    16, L_AUTH_EN,
    "Primitive xác thực",
    "So sánh an toàn thời gian và salt theo người dùng — hai primitive đằng sau mọi kho thông tin đăng nhập.",
    L_AUTH_VI)

write_lesson(M, "javaa-threat-modeling",
    "Threat modeling",
    "Assets, threats, vectors, controls, residual risk — and least privilege as the cross-cutting control.",
    15, L_THREAT_EN,
    "Mô hình mối đe dọa",
    "Tài sản, đe dọa, vector, kiểm soát, rủi ro dư — và đặc quyền tối thiểu là kiểm soát xuyên suốt.",
    L_THREAT_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_TRAVERSAL = challenge(
    "javaa-p13-traversal",
    "Containment, not string matching",
    "1. `static boolean contained(java.nio.file.Path root, String userPath)` — resolve\n"
    "userPath against root, NORMALIZE, and return whether the result is still inside\n"
    "root (startsWith on normalized paths). Must reject \"../../etc/passwd\" but accept\n"
    "\"docs/report.txt\" and even \"docs/../docs/report.txt\" (it normalizes INSIDE).\n"
    "2. `static boolean allowsHost(String host, java.util.Set<String> allowlist)` —\n"
    "exact-match membership (no substring tricks); lowercase both sides.\n"
    "3. `static String classifyUrl(String url, java.util.Set<String> allowlist)` — parse\n"
    "the host out of `http://HOST/...` (between \"://\" and the next \"/\"), return\n"
    "\"allowed\" if the host is in the allowlist else \"blocked\". Malformed (no ://) →\n"
    "\"blocked\".",
    P_BOILER,
    [
        ("canonical containment", r"""
java.nio.file.Path root = java.nio.file.Path.of("/srv/data");
checkTrue(Solution.contained(root, "docs/report.txt"), "ordinary file inside");
checkTrue(Solution.contained(root, "docs/../docs/report.txt"), "normalizes back inside");
checkTrue(!Solution.contained(root, "../secrets.txt"), "traversal rejected");
checkTrue(!Solution.contained(root, "/etc/passwd"), "absolute escape rejected");
""", "The filesystem's view, not the string's."),
        ("finite allowlists", r"""
java.util.Set<String> hosts = java.util.Set.of("api.example.com");
checkTrue(Solution.allowsHost("API.example.COM", hosts), "case-insensitive exact");
checkTrue(!Solution.allowsHost("evil-api.example.com.attacker.io", hosts), "suffix trick rejected");
checkEq(Solution.classifyUrl("http://api.example.com/v1", hosts), "allowed", "known host");
checkEq(Solution.classifyUrl("http://169.254.169.254/latest", hosts), "blocked", "metadata blocked");
checkEq(Solution.classifyUrl("not a url", hosts), "blocked", "malformed blocked");
""", "Allowlists are finite; blacklists are not."),
    ],
    level="guided",
)
CH_TRAVERSAL_VI = vi_challenge(
    "Bao chứa, không phải so khớp chuỗi",
    "contained/allowsHost/classifyUrl: góc nhìn của filesystem chứ không phải của chuỗi; allowlist hữu hạn chặn mẹo hậu tố và metadata.",
    [("Bao chứa chuẩn hóa", "Traversal bị từ chối, file thường được chấp nhận."),
     ("Allowlist hữu hạn", "Mẹo hậu tố và host lạ bị chặn.")],
)

CH_AUTH = challenge(
    "javaa-p13-auth",
    "Credentials done right",
    "1. `static byte[] salt()` — 16 random bytes (SecureRandom).\n"
    "2. `static byte[] hash(byte[] salt, String password)` — SHA-256 over salt bytes\n"
    "followed by UTF-8 password bytes (concatenate the two arrays; MessageDigest from\n"
    "java.security).\n"
    "3. `static boolean verify(byte[] salt, String password, byte[] expectedHash)` —\n"
    "recompute hash(salt, password) and compare with MessageDigest.isEqual (constant\n"
    "time).\n"
    "4. `static boolean samePasswordDifferentSalt(byte[] s1, byte[] s2, String pw)` —\n"
    "true iff hash(s1,pw) differs from hash(s2,pw) — demonstrating that two users with\n"
    "the same password produce different stored bytes.\n"
    "5. `static boolean timingSafe(byte[] a, byte[] b)` — MessageDigest.isEqual(a, b).",
    P_BOILER,
    [
        ("salted hashes and constant-time verify", r"""
byte[] s = Solution.salt();
checkEq(s.length, 16, "16-byte salt");
byte[] h = Solution.hash(s, "hunter2");
checkEq(h.length, 32, "SHA-256 is 32 bytes");
checkTrue(Solution.verify(s, "hunter2", h), "correct password verifies");
checkTrue(!Solution.verify(s, "hunter3", h), "wrong password fails");
checkTrue(Solution.samePasswordDifferentSalt(Solution.salt(), Solution.salt(), "same-pw"),
    "same password, different bytes per salt");
checkTrue(Solution.timingSafe(h, Solution.hash(s, "hunter2")), "constant-time compare agrees");
""", "The full credential round-trip."),
    ],
    level="independent",
)
CH_AUTH_VI = vi_challenge(
    "Thông tin đăng nhập đúng chuẩn",
    "salt/hash/verify/samePasswordDifferentSalt/timingSafe: salt 16 byte, SHA-256, xác minh thời gian hằng, salt khác nhau tạo byte khác nhau.",
    [("Vòng tròn thông tin đăng nhập đầy đủ", "Đúng mật khẩu xác minh, sai mật khẩu từ chối."),
     ("Cùng mật khẩu, byte khác nhau", "Mỗi salt tạo byte lưu khác nhau.")],
)

write_practice(M, "javaa-p13-security",
    "Security drills",
    "Containment checks, allowlists, salted digests, and the secrets-hygiene scan.",
    "Bài tập bảo mật",
    "Kiểm tra bao chứa, allowlist, digest có salt, và quét vệ sinh bí mật.",
    "javaa-threat-modeling", 55, "advanced",
    [CH_TRAVERSAL, CH_AUTH],
    {"javaa-p13-traversal": CH_TRAVERSAL_VI, "javaa-p13-auth": CH_AUTH_VI},
    solutions=[
        ("javaa-p13-traversal", r"""
import java.nio.file.*;
import java.util.*;

public class Solution {
    public static boolean contained(Path root, String userPath) {
        Path base = root.toAbsolutePath().normalize();
        Path target = base.resolve(userPath).normalize();
        return target.startsWith(base);
    }

    public static boolean allowsHost(String host, Set<String> allowlist) {
        return allowlist.contains(host.toLowerCase());
    }

    public static String classifyUrl(String url, Set<String> allowlist) {
        int schemeEnd = url.indexOf("://");
        if (schemeEnd < 0) return "blocked";
        int hostStart = schemeEnd + 3;
        int slash = url.indexOf('/', hostStart);
        String host = (slash < 0 ? url.substring(hostStart) : url.substring(hostStart, slash))
            .toLowerCase();
        return allowsHost(host, allowlist) ? "allowed" : "blocked";
    }
}
""", r"""
import java.nio.file.*;
import java.util.*;

public class Solution {
    public static boolean contained(Path root, String userPath) {
        return !userPath.contains("..");   // WRONG: raw-string filter — misses decoding,
    }                                      // absolute escapes, and blocks harmless names

    public static boolean allowsHost(String host, Set<String> allowlist) {
        for (String allowed : allowlist) {
            if (host.contains(allowed)) return true;   // WRONG: substring — evil-api.example.com.attacker.io passes
        }
        return false;
    }

    public static String classifyUrl(String url, Set<String> allowlist) {
        return url.contains("api.example.com") ? "allowed" : "blocked";   // WRONG: substring on raw URL
    }
}
"""),
        ("javaa-p13-auth", r"""
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Arrays;

public class Solution {
    private static final SecureRandom RNG = new SecureRandom();

    public static byte[] salt() {
        byte[] s = new byte[16];
        RNG.nextBytes(s);
        return s;
    }

    public static byte[] hash(byte[] salt, String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            md.update(salt);
            md.update(password.getBytes(StandardCharsets.UTF_8));
            return md.digest();
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    public static boolean verify(byte[] salt, String password, byte[] expectedHash) {
        return MessageDigest.isEqual(hash(salt, password), expectedHash);
    }

    public static boolean samePasswordDifferentSalt(byte[] s1, byte[] s2, String pw) {
        return !MessageDigest.isEqual(hash(s1, pw), hash(s2, pw));
    }

    public static boolean timingSafe(byte[] a, byte[] b) {
        return MessageDigest.isEqual(a, b);
    }
}
""", r"""
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Arrays;

public class Solution {
    public static byte[] salt() {
        return new byte[16];   // WRONG: all zeros — deterministic, rainbow-tableable
    }

    public static byte[] hash(byte[] salt, String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            md.update(password.getBytes(StandardCharsets.UTF_8));   // WRONG: salt never mixed in
            return md.digest();
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    public static boolean verify(byte[] salt, String password, byte[] expectedHash) {
        return MessageDigest.isEqual(hash(salt, password), expectedHash);
    }

    public static boolean samePasswordDifferentSalt(byte[] s1, byte[] s2, String pw) {
        return false;   // WRONG: saltless digests are IDENTICAL — but claiming "false" outright
    }                   // fails the demo instead of proving the bug

    public static boolean timingSafe(byte[] a, byte[] b) {
        return java.util.Arrays.equals(a, b);   // WRONG: early-exit compare (timing leak)
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the request firewall

Canonical containment, host allowlisting, credential verification, and a
threat-model registry — one component where every control is a value you can
inspect, and the security review is a function.
"""

CP_CH = challenge(
    "javaa-checkpoint-m13-task",
    "Checkpoint: the request firewall",
    "Inside Solution, implement `public static class Firewall`:\n"
    "1. Constructor `Firewall(Path root, Set<String> allowedHosts)`; expose\n"
    "`public final Path root` and `public final Set<String> allowedHosts`.\n"
    "2. `boolean canRead(String userPath)` — canonical containment against root.\n"
    "3. `boolean canCall(String url)` — host extraction + allowlist.\n"
    "4. `boolean authenticate(byte[] salt, String password, byte[] stored)` — salted\n"
    "recompute + constant-time verify.\n"
    "5. `static String review(java.util.Map<String, String> findings)` — given findings\n"
    "like {\"sql\":\"parameterized\", \"secret\":\"env\", \"depends\":\"audited\"}, return\n"
    "\"pass\" iff every value is one of the accepted controls:\n"
    "sql∈{parameterized}, secret∈{env}, depends∈{audited}; otherwise return the FIRST\n"
    "key whose control is unacceptable. Unknown keys count as unacceptable.\n"
    "6. `static String threatOf(String control)` — map each control to the STRIDE\n"
    "letter it primarily addresses: \"canonicalization\"→\"T\", \"allowlist\"→\"I\",\n"
    "\"parameterized\"→\"T\", \"least-privilege\"→\"E\", \"rate-limit\"→\"D\"; unknown → \"?\".",
    P_BOILER,
    [
        ("firewall answers the three questions", r"""
Solution.Fw fw = new Solution.Fw(java.nio.file.Path.of("/srv/data").toAbsolutePath().normalize(),
    java.util.Set.of("api.example.com"));
checkTrue(fw.canRead("docs/a.txt"), "inside root");
checkTrue(!fw.canRead("../etc/passwd"), "traversal blocked");
checkTrue(fw.canCall("http://api.example.com/x"), "allowed host");
checkTrue(!fw.canCall("http://169.254.169.254/"), "metadata host blocked");
byte[] s = Solution.Fw.salt();
byte[] stored = Solution.Fw.hash(s, "pw");
checkTrue(fw.authenticate(s, "pw", stored), "good credentials");
checkTrue(!fw.authenticate(s, "wrong", stored), "bad credentials");
""", "Containment, egress, identity."),
        ("the review is a function", r"""
java.util.Map<String, String> good = java.util.Map.of("sql", "parameterized", "secret", "env");
checkEq(Solution.Fw.review(good), "pass", "all controls accepted");
java.util.Map<String, String> bad = java.util.Map.of("sql", "string-concat", "secret", "env");
checkEq(Solution.Fw.review(bad), "sql", "first offender named");
checkEq(Solution.Fw.threatOf("rate-limit"), "D", "denial of service");
checkEq(Solution.Fw.threatOf("least-privilege"), "E", "elevation");
checkEq(Solution.Fw.threatOf("vibes"), "?", "unknown control");
""", "Findings map to STRIDE letters."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: tường lửa yêu cầu",
    "Fw: bao chứa, allowlist, xác thực có salt; review trả pass hoặc tên phạm nhân đầu tiên; threatOf ánh xạ kiểm soát sang chữ STRIDE.",
    [("Tường lửa trả lời ba câu hỏi", "Bao chứa, egress, danh tính."),
     ("Việc rà soát là một hàm", "Phát hiện ánh xạ sang chữ STRIDE.")],
)

write_checkpoint(M, "javaa-checkpoint-m13",
    "Checkpoint: The Request Firewall",
    "Containment, egress, identity, and a security review that is a function.",
    30, CP_MD,
    "Checkpoint: Tường lửa yêu cầu",
    "Bao chứa, egress, danh tính, và việc rà soát bảo mật là một hàm.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.*;

public class Solution {
    public static class Fw {
        public final Path root;
        public final Set<String> allowedHosts;

        public Fw(Path root, Set<String> allowedHosts) {
            this.root = root;
            this.allowedHosts = allowedHosts;
        }

        public boolean canRead(String userPath) {
            Path base = root.toAbsolutePath().normalize();
            Path target = base.resolve(userPath).normalize();
            return target.startsWith(base);
        }

        public boolean canCall(String url) {
            int schemeEnd = url.indexOf("://");
            if (schemeEnd < 0) return false;
            int hostStart = schemeEnd + 3;
            int slash = url.indexOf('/', hostStart);
            String host = (slash < 0 ? url.substring(hostStart) : url.substring(hostStart, slash))
                .toLowerCase();
            return allowedHosts.contains(host);
        }

        public boolean authenticate(byte[] salt, String password, byte[] stored) {
            return MessageDigest.isEqual(hash(salt, password), stored);
        }

        public static byte[] salt() {
            byte[] s = new byte[16];
            new SecureRandom().nextBytes(s);
            return s;
        }

        public static byte[] hash(byte[] salt, String password) {
            try {
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                md.update(salt);
                md.update(password.getBytes(StandardCharsets.UTF_8));
                return md.digest();
            } catch (Exception e) {
                throw new IllegalStateException(e);
            }
        }

        public static String review(Map<String, String> findings) {
            Map<String, Set<String>> accepted = Map.of(
                "sql", Set.of("parameterized"),
                "secret", Set.of("env"),
                "depends", Set.of("audited"));
            for (Map.Entry<String, String> e : findings.entrySet()) {
                Set<String> ok = accepted.get(e.getKey());
                if (ok == null || !ok.contains(e.getValue())) return e.getKey();
            }
            return "pass";
        }

        public static String threatOf(String control) {
            return switch (control) {
                case "canonicalization", "parameterized" -> "T";
                case "allowlist" -> "I";
                case "least-privilege" -> "E";
                case "rate-limit" -> "D";
                default -> "?";
            };
        }
    }
}
""", wrong=r"""
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;

public class Solution {
    public static class Fw {
        public final Path root;
        public final Set<String> allowedHosts;

        public Fw(Path root, Set<String> allowedHosts) {
            this.root = root;
            this.allowedHosts = allowedHosts;
        }

        public boolean canRead(String userPath) {
            return !userPath.contains("..");   // WRONG: raw-string filter, not containment
        }

        public boolean canCall(String url) {
            return url.contains("api.example.com");   // WRONG: substring allowlist
        }

        public boolean authenticate(byte[] salt, String password, byte[] stored) {
            try {
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                md.update(password.getBytes(StandardCharsets.UTF_8));   // WRONG: salt ignored
                return Arrays.equals(md.digest(), stored);              // WRONG: early-exit compare
            } catch (Exception e) {
                throw new IllegalStateException(e);
            }
        }

        public static byte[] salt() { return new byte[16]; }   // WRONG: zeros

        public static byte[] hash(byte[] salt, String password) {
            try {
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                md.update(password.getBytes(StandardCharsets.UTF_8));
                return md.digest();
            } catch (Exception e) { throw new IllegalStateException(e); }
        }

        public static String review(Map<String, String> findings) {
            return "pass";   // WRONG: review approves everything
        }

        public static String threatOf(String control) {
            return "?";   // WRONG: no STRIDE mapping
        }
    }
}
""")

print("module 13 authored")
