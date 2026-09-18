#!/usr/bin/env python3
"""C Advanced — batch 12: modules 23 (security) and 24 (portability + capstone).
Zero typed backslashes: @NL@ = statement separator, @T*/@GS*/@TL*@ tokens are
expanded by ca.py at runtime. Solutions are complete standalone programs."""
from ca import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ================= MODULE 23: ca-security ====================================
M23 = "ca-security"

L23A = "ca-input-bounds"
L23B = "ca-hardened-apis"
L23CP = "ca-checkpoint-m23"

write_module(
    M23,
    "Security Engineering: Bounds, Formats, Hardening",
    "The memory-corruption families (overflow, format strings, TOCTOU, use-after-free) from the defender's seat: what breaks, how to detect it, how to prevent it. Prevention and detection only.",
    "Kỹ thuật an ninh: biên, định dạng, gia cố",
    "Các dòng họ hỏng bộ nhớ (tràn bộ đệm, chuỗi định dạng, TOCTOU, dùng-sau-khi-giải phóng) từ ghế của người phòng thủ: cái gì vỡ, phát hiện thế nào, phòng ngừa thế nào. Chỉ phòng ngừa và phát hiện.",
    [L23A, L23B, L23CP],
    ["ca-p23-security"],
)

write_lesson(
    M23,
    L23A,
    "Buffers, Bounds, and the Attacker's Model",
    "Every `strcpy` is a promise that you checked a length somewhere else. Security is that check, made systematic.",
    20,
    """
## The corruption family

All of these are memory-safety failures the compiler will not stop:

- **Buffer overflow** — writing past an array's end. A fixed `char buf[64]` fed 65 attacker-controlled bytes writes into whatever lives next (return address, heap metadata, another object). C23 Annex K offers `strcpy_s`-style bounds-checked APIs, but portable practice is: **never** copy without a length: `snprintf`, `memcpy` with a computed, checked bound.
- **Format-string injection** — `printf(user_input)` treats `%s`/`%n` in the input as directives: leaks memory (`%s` from a garbage pointer), writes memory (`%n`). The fix is one character: `printf("%s", user_input)`.
- **Integer overflow** — `(size_t)len + 1` when `len` is near SIZE_MAX wraps to 0 and the subsequent `malloc(len+1)` hands out a tiny buffer for a huge copy. Check the addition, or use `__builtin_add_overflow`-style checks where available.
- **TOCTOU** — check-then-use across a system boundary: `access(path, R_OK)` says yes, the file is swapped, `open(path)` opens something else. The durable fix: open first (get an fd), then `fstat` *the fd*, and work through the fd — the check and the use reference the same object.
- **Use-after-free / double free** — ownership discipline from module 6 is the prevention; a deliberate `free(NULL)`-safe, single-owner, null-on-free pattern (`free(p); p = NULL;`) kills the double-free class.

## Uninitialized reads

Reading a local before writing it is undefined behavior — and in practice hands the attacker whatever was in that stack slot (old pointers, keys). Rule: **initialize at declaration** (`int x = 0;`) or structure code so every path writes before any read. Zero-cost discipline, whole bug-class removed.

## The defender's checklist

1. Every copy carries an explicit, checked length.
2. Every format string is a literal.
3. Every size arithmetic is checked before allocation.
4. Every file interaction goes through one descriptor, checked at use time.
5. Every free leaves NULL behind.
6. Every uninitialized variable is a compile-error in review.

None of this requires attacker creativity to justify — only ordinary input.
""",
    "Buffer, biên, và mô hình kẻ tấn công",
    "Mỗi strcpy là một lời hứa rằng bạn đã kiểm tra độ dài ở đâu đó. An ninh là lời kiểm tra đó, được hệ thống hóa.",
    """
## Dòng họ hỏng bộ nhớ

Tất cả những điều này là lỗi an toàn bộ nhớ mà compiler không chặn:

- **Tràn bộ đệm** — ghi quá cuối mảng. Một `char buf[64]` cố định nhận 65 byte do kẻ tấn công điều khiển sẽ ghi đè lên thứ sống kế bên (địa chỉ trả về, metadata heap, đối tượng khác). C23 Annex K có API kiểm soát biên kiểu `strcpy_s`, nhưng thực hành portable là: **không bao giờ** sao chép thiếu độ dài: `snprintf`, `memcpy` với biên được tính và kiểm tra.
- **Tiêm chuỗi định dạng** — `printf(user_input)` coi `%s`/`%n` trong đầu vào là chỉ thị: lộ bộ nhớ (`%s` từ con trỏ rác), ghi bộ nhớ (`%n`). Bản vá là một ký tự: `printf("%s", user_input)`.
- **Tràn số nguyên** — `(size_t)len + 1` khi `len` gần SIZE_MAX sẽ wrap về 0 và `malloc(len+1)` sau đó phát một buffer tí hon cho một bản sao khổng lồ. Kiểm tra phép cộng, hoặc dùng kiểm tra kiểu `__builtin_add_overflow` khi có.
- **TOCTOU** — kiểm-tra-rồi-dùng qua biên hệ thống: `access(path, R_OK)` nói có, tập tin bị thay, `open(path)` mở thứ khác. Bản vá bền: mở trước (nhận fd), rồi `fstat` *chính fd đó*, và làm việc qua fd — kiểm tra và dùng cùng tham chiếu một đối tượng.
- **Dùng-sau-khi-giải phóng / giải phóng hai lần** — kỷ luật sở hữu từ mô-đun 6 là phòng ngừa; pattern một-chủ-sở-hữu, null-sau-free (`free(p); p = NULL;`) tiêu diệt cả lớp double-free.

## Đọc biến chưa khởi tạo

Đọc biến cục bộ trước khi ghi là hành vi không xác định — và trên thực tế trao cho kẻ tấn công thứ đang nằm trong ô stack đó (con trỏ cũ, khóa). Quy tắc: **khởi tạo ngay khi khai báo** (`int x = 0;`) hoặc cấu trúc code để mọi đường ghi trước khi đọc. Kỷ luật không tốn chi phí, cả lớp lỗi biến mất.

## Danh sách kiểm của người phòng thủ

1. Mọi bản sao mang độ dài tường minh, đã kiểm tra.
2. Mọi chuỗi định dạng là literal.
3. Mọi phép toán kích thước được kiểm trước khi cấp phát.
4. Mọi tương tác tập tin đi qua một descriptor, kiểm tra tại thời điểm dùng.
5. Mọi free để lại NULL.
6. Mọi biến chưa khởi tạo là lỗi biên dịch trong review.

Không điều gì trong số này cần sự sáng tạo của kẻ tấn công để biện minh — chỉ cần đầu vào bình thường.
""",
)

write_lesson(
    M23,
    L23B,
    "Hardened APIs and Honest Verification",
    "Choosing the API that cannot overflow, and verifying the fix without ever writing an exploit.",
    20,
    """
## The hardened set

| risky | hardened | why |
|-------|----------|-----|
| `strcpy(dst, src)` | `snprintf(dst, dstsize, "%s", src)` | truncates at dstsize, always NUL-terminates, returns the would-be length so you can detect loss |
| `strcat(a, b)` | `strncat` with computed room, or track length yourself | classic `strncat` off-by-one: its `n` is *bytes to copy*, not total size |
| `sprintf(buf, ...)` | `snprintf` | sprintf has no bound at all |
| `atoi(s)` | `strtol(s, &end, 10)` + errno/range checks | atoi has no error report; `strtol` reports overflow via ERANGE |
| `gets` | never; removed from the language (C11) | the historic exhibits-A; `fgets(buf, size, stdin)` instead |

`snprintf`'s return value is the security-relevant part: it returns the length the string *wanted*. If it is >= dstsize, output was truncated — treat that as an error, not a shrug:

```c
char buf[16];
int need = snprintf(buf, sizeof buf, "%s", user);
if (need < 0 || (size_t)need >= sizeof buf) { /* refuse */ }
```

## Hardening flags (compiler-specific, labeled)

GCC/Clang offer defense-in-depth flags: `-fstack-protector-strong` (canary on arrays), `-D_FORTIFY_SOURCE=2` (libc checks when sizes are known), `-Wformat-security` (warn on non-literal formats), `-fPIE`/ASLR (address randomization). None fix a broken program — they convert *some* exploits into loud crashes. The flags are GCC/Clang-specific engineering practice, not ISO C.

## Verification without exploits

Defensive testing asks one question per hazard: *does the guard fire?*

- Overflow guard: feed one byte past the boundary, expect the refusal path (not a crash — a refusal).
- Truncation guard: expect the `need >= sizeof buf` branch to be taken and handled.
- TOCTOU: structure review — is there any window between access-check and use? If the code checks `access()` then `open()`s, the answer is yes, and the fix is the fd-based pattern.
- Double-free: free, null, free again — the second call must be a harmless no-op.

An exploit proves an attacker can win; a test proves the guard fires. We write the second thing only.
""",
    "API gia cố và kiểm chứng trung thực",
    "Chọn API không thể tràn, và kiểm chứng bản vá mà không bao giờ viết khai thác.",
    """
## Bộ API gia cố

|rủi ro|gia cố|vì sao|
|------|------|------|
|`strcpy(dst, src)`|`snprintf(dst, dstsize, "%s", src)`|cắt tại dstsize, luôn kết thúc NUL, trả độ dài mong muốn để phát hiện mất mát|
|`strcat(a, b)`|`strncat` với chỗ trống đã tính, hoặc tự theo dõi độ dài|lỗi lệch-một kinh điển của `strncat`: `n` là *byte cần sao*, không phải tổng cỡ|
|`sprintf(buf, ...)`|`snprintf`|sprintf không có biên nào cả|
|`atoi(s)`|`strtol(s, &end, 10)` + kiểm tra errno/phan vi|atoi không báo lỗi; `strtol` báo tràn qua ERANGE|
|`gets`|không bao giờ; đã bị loại khỏi ngôn ngữ (C11)|bằng chứng lịch sử; `fgets(buf, size, stdin)` thay thế|

Giá trị trả về của `snprintf` là phần quan trọng về an ninh: nó trả độ dài mà chuỗi *muốn*. Nếu >= dstsize, output đã bị cắt — coi đó là lỗi, không phải nhún vai:

```c
char buf[16];
int need = snprintf(buf, sizeof buf, "%s", user);
if (need < 0 || (size_t)need >= sizeof buf) { /* từ chối */ }
```

## Cờ gia cố (riêng compiler, ghi nhãn)

GCC/Clang có các cờ phòng thủ theo tầng: `-fstack-protector-strong` (canary cho mảng), `-D_FORTIFY_SOURCE=2` (kiểm tra libc khi biết kích thước), `-Wformat-security` (cảnh báo định dạng không phải literal), `-fPIE`/ASLR (xáo trộn địa chỉ). Không cờ nào sửa chương trình hỏng — chúng biến *một số* khai thác thành crash ồn ào. Cờ là thực hành kỹ thuật riêng của GCC/Clang, không phải ISO C.

## Kiểm chứng mà không viết khai thác

Kiểm thử phòng thủ hỏi một câu cho mỗi nguy cơ: *guard có kích hoạt không?*

- Guard tràn: đưa một byte quá biên, kỳ vọng đường từ chối (không phải crash — một sự từ chối).
- Guard cắt cụt: kỳ vọng nhánh `need >= sizeof buf` được đi vào và xử lý.
- TOCTOU: review cấu trúc — có khoảng trống nào giữa kiểm tra và dùng không? Nếu code kiểm `access()` rồi mới `open()`, câu trả lời là có, và bản vá là pattern dựa trên fd.
- Double-free: free, gán NULL, free lần nữa — lần gọi thứ hai phải là no-op vô hại.

Khai thác chứng minh kẻ tấn công có thể thắng; kiểm thử chứng minh guard kích hoạt. Chúng ta chỉ viết thứ thứ hai.
""",
)

write_practice(
    M23,
    "ca-p23-security",
    "Hardening Drills",
    "Safe copies, refusal paths, checked arithmetic, and fd-based TOCTOU elimination — every guard tested by feeding it exactly the input it exists for.",
    "Bài tập gia cố",
    "Bản sao an toàn, đường từ chối, số học được kiểm, và xóa TOCTOU bằng fd — mọi guard được kiểm bằng đúng đầu vào mà nó tồn tại cho.",
    L23A,
    26,
    "advanced",
    [
        challenge(
            "ca23-safe-copy",
            "The Refusing Copy",
            "ISO C. Implement `int safe_copy(char *dst, size_t dstsize, const char *src)` — copy src into dst with NUL-termination only if it fits (including the terminator); return 0 on success, -1 on truncation-or-error (dst NULL, dstsize 0, src NULL, or src longer than dstsize-1). On refusal dst is left untouched. This is snprintf's semantics, hand-rolled.",
            C_PRELUDE,
            [
                ("fits exactly", "char b[6] = {0};@NL@CHECK_EQ(safe_copy(b, 6, @GS3@), 0);@NL@CHECK_STR_EQ(b, @GS3@);", "world is 5 chars + NUL = 6: fits exactly, success."),
                ("one too many refuses", "char b2[5] = {0};@NL@CHECK_EQ(safe_copy(b2, 5, @GS3@), -1);@NL@CHECK_EQ(b2[0], 0);", "5 chars need 6 slots: refusal, and dst keeps its original bytes."),
                ("empty and NULL", "char b3[4] = {0};@NL@CHECK_EQ(safe_copy(b3, 4, @GS2@), 0);@NL@CHECK_EQ(safe_copy(b3, 4, NULL), -1);@NL@CHECK_EQ(safe_copy(NULL, 4, @GS2@), -1);@NL@CHECK_EQ(safe_copy(b3, 0, @GS2@), -1);", "An empty source copies fine; NULL or zero-size destinations refuse."),
            ],
            level="guided",
        ),
        challenge(
            "ca23-size-check",
            "Checked Size Arithmetic",
            "ISO C. Implement `int alloc_safe(size_t count, size_t elemsz, size_t *out_bytes)` — compute count*elemsz for allocation; on overflow of the multiplication, or count/elemsz 0 (refuse zero-size asks), return -1 and leave *out_bytes alone; else store the product and return 0. (On this platform you may detect overflow via division: count > SIZE_MAX / elemsz.)",
            C_PRELUDE,
            [
                ("normal sizing", "size_t b1 = 0;@NL@CHECK_EQ(alloc_safe(100, 64, &b1), 0);@NL@CHECK_EQ(b1, 6400);", "Plain multiplication: 100 elements of 64 bytes."),
                ("overflow detected", "size_t b2 = 7;@NL@CHECK_EQ(alloc_safe((size_t)-1, 2, &b2), -1);@NL@CHECK_EQ(b2, 7);", "(size_t)-1 times 2 wraps: the division check catches it and *out_bytes is untouched."),
                ("zero refuses", "size_t b3 = 9;@NL@CHECK_EQ(alloc_safe(0, 8, &b3), -1);@NL@CHECK_EQ(alloc_safe(8, 0, &b3), -1);@NL@CHECK_EQ(b3, 9);", "Zero-sized allocations are a caller bug: refuse, never hand out a 0-byte pointer to loop over."),
            ],
            level="combination",
        ),
        challenge(
            "ca23-fd-not-path",
            "Open Once, Then Ask the fd",
            "POSIX. Implement `int file_has_size(int fd, long want)` — fstat the fd (never a path) and return 1 when the file's size equals want, 0 when it differs, -1 on fstat failure. This is the TOCTOU-elimination primitive: the check is bound to the very object being used.",
            C_PRELUDE + "#define _POSIX_C_SOURCE 200809L@NL@#include <fcntl.h>@NL@#include <unistd.h>@NL@#include <sys/stat.h>@NL@",
            [
                ("size match", "int fd1 = open(@TLINES@, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@CHECK(fd1 >= 0);@NL@CHECK_EQ((int)write(fd1, @GS1@, 5), 5);@NL@CHECK_EQ(file_has_size(fd1, 5), 1);@NL@close(fd1);", "fstat on the fd sees the object this descriptor names: size 5 matches."),
                ("size mismatch", "int fd2 = open(@TLINES@, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@CHECK(fd2 >= 0);@NL@CHECK_EQ((int)write(fd2, @GS1@, 5), 5);@NL@CHECK_EQ(file_has_size(fd2, 4), 0);@NL@close(fd2);", "The same primitive reports a difference instead of a match."),
                ("bad fd refuses", "CHECK_EQ(file_has_size(-1, 5), -1);", "An invalid descriptor fails loudly — no guessing, no path fallback."),
            ],
            level="combination",
        ),
    ],
    {
        "ca23-safe-copy": vi_challenge(
            "Bản sao từ chối",
            "ISO C. Cài `int safe_copy(char *dst, size_t dstsize, const char *src)` — sao chép src vào dst với kết thúc NUL chỉ khi vừa (tính cả terminator); trả 0 khi thành công, -1 khi cắt cụt-hoặc-lỗi (dst NULL, dstsize 0, src NULL, hoặc src dài hơn dstsize-1). Khi từ chối, dst không bị đụng.",
            [
                ("vừa khít", "world là 5 ký tự + NUL = 6: vừa đúng, thành công."),
                ("thừa một từ chối", "5 ký tự cần 6 ô: từ chối, và dst giữ nguyên byte cũ."),
                ("rỗng và NULL", "Nguồn rỗng sao chép tốt; đích NULL hoặc cỡ không từ chối."),
            ],
        ),
        "ca23-size-check": vi_challenge(
            "Số học kích thước được kiểm",
            "ISO C. Cài `int alloc_safe(size_t count, size_t elemsz, size_t *out_bytes)` — tính count*elemsz để cấp phát; khi phép nhân tràn, hoặc count/elemsz bằng 0 (từ chối yêu cầu cỡ không), trả -1 và không đụng *out_bytes; ngược lại lưu tích và trả 0. (Trên nền tảng này có thể phát hiện tràn qua phép chia: count > SIZE_MAX / elemsz.)",
            [
                ("tính cỡ thường", "Phép nhân thuần: 100 phần tử, mỗi phần tử 64 byte."),
                ("phát hiện tràn", "(size_t)-1 nhân 2 sẽ wrap: kiểm tra bằng chia chặn được và *out_bytes không bị đụng."),
                ("không từ chối", "Cấp phát cỡ không là lỗi người gọi: từ chối, không bao giờ phát con trỏ 0 byte cho vòng lặp."),
            ],
        ),
        "ca23-fd-not-path": vi_challenge(
            "Mở một lần, rồi hỏi fd",
            "POSIX. Cài `int file_has_size(int fd, long want)` — fstat fd (không bao giờ đường dẫn) và trả 1 khi kích thước bằng want, 0 khi khác, -1 khi fstat lỗi. Đây là nguyên thủy xóa TOCTOU: kiểm tra gắn với chính đối tượng đang dùng.",
            [
                ("kích thước khớp", "fstat trên fd thấy đối tượng mà descriptor này gọi tên: cỡ 5 khớp."),
                ("kích thước khác", "Cùng nguyên thủy báo khác biệt thay vì khớp."),
                ("fd xấu từ chối", "Descriptor không hợp lệ báo lỗi rõ ràng — không đoán, không fallback theo path."),
            ],
        ),
    },
    solutions=[
        (
            "ca23-safe-copy",
            C_PRELUDE
            + "int safe_copy(char *dst, size_t dstsize, const char *src) {@NL@"
            + "    if (dst == NULL || dstsize == 0 || src == NULL) return -1;@NL@"
            + "    size_t need = strlen(src) + 1;@NL@"
            + "    if (need > dstsize) return -1;@NL@"
            + "    for (size_t i = 0; i < need; i++) dst[i] = src[i];@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int safe_copy(char *dst, size_t dstsize, const char *src) {@NL@"
            + "    if (dst == NULL || dstsize == 0 || src == NULL) return -1;@NL@"
            + "    size_t need = strlen(src);@NL@"
            + "    if (need > dstsize) return -1;@NL@"
            + "    for (size_t i = 0; i <= need; i++) dst[i] = src[i];@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca23-size-check",
            C_PRELUDE
            + "int alloc_safe(size_t count, size_t elemsz, size_t *out_bytes) {@NL@"
            + "    if (out_bytes == NULL) return -1;@NL@"
            + "    if (count == 0 || elemsz == 0) return -1;@NL@"
            + "    if (count > (size_t)-1 / elemsz) return -1;@NL@"
            + "    *out_bytes = count * elemsz;@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int alloc_safe(size_t count, size_t elemsz, size_t *out_bytes) {@NL@"
            + "    if (out_bytes == NULL) return -1;@NL@"
            + "    if (count == 0 || elemsz == 0) return -1;@NL@"
            + "    *out_bytes = count * elemsz;@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca23-fd-not-path",
            C_PRELUDE + "#define _POSIX_C_SOURCE 200809L@NL@#include <fcntl.h>@NL@#include <unistd.h>@NL@#include <sys/stat.h>@NL@"
            + "int file_has_size(int fd, long want) {@NL@"
            + "    struct stat st;@NL@"
            + "    if (fstat(fd, &st) != 0) return -1;@NL@"
            + "    return st.st_size == want ? 1 : 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + "#define _POSIX_C_SOURCE 200809L@NL@#include <fcntl.h>@NL@#include <unistd.h>@NL@#include <sys/stat.h>@NL@"
            + "int file_has_size(int fd, long want) {@NL@"
            + "    struct stat st;@NL@"
            + "    if (fstat(fd, &st) != 0) return 1;@NL@"
            + "    return st.st_size <= want ? 1 : 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_checkpoint(
    M23,
    L23CP,
    "Checkpoint: Hardened Field Parser",
    "One defensive component, fully specified: a fixed-size record parser that refuses instead of crashing.",
    22,
    "See lesson.",
    "Kiểm tra: Bộ phân tích trường được gia cố",
    "Một thành phần phòng thủ, đặc tả trọn vẹn: bộ phân tích bản ghi cỡ cố định mà từ chối thay vì crash.",
    "Xem bài học.",
    challenge(
        "ca23-checkpoint-parser",
        "Checkpoint: Hardened Field Parser",
        "ISO C. A record is `name:score` (name up to 15 chars, score a decimal integer). Implement `int parse_record(const char *line, char *name, size_t namesz, int *score)` — split on the FIRST ':'; copy the name into name only if it fits (NUL included), parse the score with the strictness of strtol (digits only between optional leading +/-; empty or trailing garbage refuses). Return 0 on success; -1 on any refusal (NULL args, no colon, name too long, bad score). Refused outputs are untouched.",
        C_PRELUDE,
        [
            ("happy path", "char nm[16] = {0};@NL@int sc = -9;@NL@CHECK_EQ(parse_record(@TPR@, nm, 16, &sc), 0);@NL@CHECK_STR_EQ(nm, @GS3@);@NL@CHECK_EQ(sc, 42);", "world:42 parses cleanly into both outputs."),
            ("name overflows", "char nm2[4] = {0};@NL@int sc2 = -9;@NL@CHECK_EQ(parse_record(@TPR@, nm2, 4, &sc2), -1);@NL@CHECK_EQ(sc2, -9);", "A 5-char name does not fit 4 bytes: refusal, score untouched."),
            ("bad score refuses", "char nm3[16] = {0};@NL@int sc3 = -9;@NL@CHECK_EQ(parse_record(@TBAD@, nm3, 16, &sc3), -1);@NL@CHECK_EQ(sc3, -9);", "exit:3 has no digits after the colon prefix — a refusal, never atoi's silent zero."),
            ("no colon", "char nm4[16] = {0};@NL@int sc4 = -9;@NL@CHECK_EQ(parse_record(@GS1@, nm4, 16, &sc4), -1);@NL@CHECK_EQ(sc4, -9);", "A line without a colon is not a record: refuse."),
        ],
        level="capstone",
    ),
    {
        "ca23-checkpoint-parser": vi_challenge(
            "Kiểm tra: Bộ phân tích trường được gia cố",
            "ISO C. Một bản ghi là `name:score` (tên tối đa 15 ký tự, score là số nguyên thập phân). Cài `int parse_record(const char *line, char *name, size_t namesz, int *score)` — tách tại dấu ':' ĐẦU TIÊN; sao tên vào name chỉ khi vừa (tính NUL), phân tích score với độ nghiêm ngặt của strtol (chỉ chữ số, cho phép +/- đầu; rỗng hoặc rác phía sau thì từ chối). Trả 0 khi thành công; -1 khi bất kỳ từ chối nào (NULL, không có dấu hai chấm, tên quá dài, score xấu). Output khi bị từ chối không bị đụng.",
            [
                ("đường vui", "world:42 phân tích sạch vào cả hai output."),
                ("tên tràn", "Tên 5 ký tự không vừa 4 byte: từ chối, score không bị đụng."),
                ("score xấu từ chối", "exit:3 không có chữ số sau tiền tố dấu hai chấm — từ chối, không bao giờ zero câm lặng của atoi."),
                ("không có dấu hai chấm", "Dòng không có dấu hai chấm không phải bản ghi: từ chối."),
            ],
        ),
    },
    solution=
    C_PRELUDE
    + "int parse_record(const char *line, char *name, size_t namesz, int *score) {@NL@"
    + "    if (line == NULL || name == NULL || namesz == 0 || score == NULL) return -1;@NL@"
    + "    const char *colon = strchr(line, ':');@NL@"
    + "    if (colon == NULL || colon == line) return -1;@NL@"
    + "    size_t nlen = (size_t)(colon - line);@NL@"
    + "    if (nlen + 1 > namesz) return -1;@NL@"
    + "    for (size_t i = 0; i < nlen; i++) name[i] = line[i];@NL@"
    + "    name[nlen] = 0;@NL@"
    + "    const char *s = colon + 1;@NL@"
    + "    if (*s == 0) return -1;@NL@"
    + "    int sign = 1;@NL@"
    + "    if (*s == '+' || *s == '-') {@NL@"
    + "        if (*s == '-') sign = -1;@NL@"
    + "        s++;@NL@"
    + "    }@NL@"
    + "    if (*s == 0) return -1;@NL@"
    + "    long val = 0;@NL@"
    + "    for (; *s; s++) {@NL@"
    + "        if (*s < '0' || *s > '9') return -1;@NL@"
    + "        val = val * 10 + (*s - '0');@NL@"
    + "        if (val > 1000000000L) return -1;@NL@"
    + "    }@NL@"
    + "    *score = (int)(sign * val);@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
    wrong=
    C_PRELUDE
    + "int parse_record(const char *line, char *name, size_t namesz, int *score) {@NL@"
    + "    if (line == NULL || name == NULL || namesz == 0 || score == NULL) return -1;@NL@"
    + "    const char *colon = strchr(line, ':');@NL@"
    + "    if (colon == NULL || colon == line) return -1;@NL@"
    + "    size_t nlen = (size_t)(colon - line);@NL@"
    + "    for (size_t i = 0; i < nlen; i++) name[i] = line[i];@NL@"
    + "    name[nlen] = 0;@NL@"
    + "    *score = atoi(colon + 1);@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
)

# ================= MODULE 24: ca-portability-capstone ========================
M24 = "ca-portability-capstone"

L24A = "ca-implementation-defined"
L24B = "ca-capstone-design"
L24CP = "ca-checkpoint-m24"

write_module(
    M24,
    "Portability and the Systems Capstone",
    "What the standard leaves to the implementation, how to detect it at compile time and run time, and the final integration project that uses every module before it.",
    "Tính khả chuyển và capstone hệ thống",
    "Những gì chuẩn để dành cho implementation, cách phát hiện nó lúc biên dịch và lúc chạy, và dự án tích hợp cuối dùng mọi mô-đun phía trước.",
    [L24A, L24B, L24CP],
    ["ca-p24-portability"],
)

write_lesson(
    M24,
    L24A,
    "Implementation-Defined, Unspecified, Undefined",
    "Three different escape hatches in the standard — only one of them is a bug.",
    20,
    """
## The three categories

- **Implementation-defined behavior** — the standard lets each implementation pick and *document* a choice: `sizeof(int)`, plain `char` signedness, two's-complement representation (C23 made this required, ending a 35-year debate). Writing code that depends on the choice is legal if you check the documentation and code defensively.
- **Unspecified behavior** — several valid choices, no documentation duty, the implementation may differ call-to-call: evaluation order of function arguments. Correct code does not depend on it.
- **Undefined behavior** — no requirements at all: signed overflow, out-of-bounds access, data races. Modules 2 and 4 covered why the optimizer treats UB as permission.

The trap for professionals: implementation-defined is *portable if asked for*. `sizeof(int) == 4` is a fact about this target, not a law of C — ask via `<limits.h>`/`<stdint.h>` types (`int32_t`) when the width matters.

## Endianness, honestly

Byte order inside a multi-byte object is implementation-defined. This sandbox (aarch64 Linux) is **little-endian**, and GCC exposes `__BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__` for compile-time detection. But the honest portable move is the runtime probe: place `1` in an `unsigned int` and inspect its first byte — that works on every C implementation, no macro required. Detect, then branch; never assume.

## Feature detection, two clocks

- **Compile time**: `#if defined(__BYTE_ORDER__) && __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__` — zero runtime cost, but tied to the compiler's macros (compiler-specific, labeled).
- **Run time**: the byte probe, or `stdbit.h`'s C23 endian utilities where available. Costs a branch once, portable everywhere.

Choose compile-time for hot paths, run-time for guaranteed portability. Document the choice; that documentation *is* the portability layer.

## The capstone contract

Module 24's checkpoint assembles the course: a portable utility core (endian detection + checked arithmetic + safe copy) plus integration of earlier modules' discipline. Every function it asks for has been built and tested in an earlier module — the capstone is composition under specification, the actual work of systems engineering.
""",
    "Implementation-defined, unspecified, undefined",
    "Ba lối thoát khác nhau trong chuẩn — chỉ một trong số chúng là lỗi.",
    """
## Ba loại hành vi

- **Hành vi tùy implementation** — chuẩn để mỗi implementation chọn và *tài liệu hóa* lựa chọn: `sizeof(int)`, dấu của `char` thường, biểu diễn bù-hai (C23 bắt buộc, chấm dứt 35 năm tranh cãi). Viết code phụ thuộc lựa chọn là hợp pháp nếu bạn đọc tài liệu và code phòng thủ.
- **Hành vi không xác định rõ (unspecified)** — vài lựa chọn hợp lệ, không nghĩa vụ tài liệu, implementation có thể khác nhau giữa các lần gọi: thứ tự đánh giá tham số hàm. Code đúng không phụ thuộc nó.
- **Hành vi không xác định (undefined)** — không yêu cầu gì cả: tràn số có dấu, truy cập quá biên, data race. Mô-đun 2 và 4 đã giải thích vì sao optimizer coi UB là giấy phép.

Bẫy của dân chuyên: implementation-defined là *khả chuyển nếu được hỏi*. `sizeof(int) == 4` là sự thật về target này, không phải luật của C — hỏi qua `<limits.h>`/kiểu `<stdint.h>` (`int32_t`) khi độ rộng quan trọng.

## Endianness, nói thẳng

Thứ tự byte trong đối tượng nhiều byte là tùy implementation. Sandbox này (aarch64 Linux) là **little-endian**, và GCC lộ `__BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__` để phát hiện lúc biên dịch. Nhưng nước đi portable trung thực là thăm dò lúc chạy: đặt `1` vào một `unsigned int` và xem byte đầu — chạy trên mọi implementation C, không cần macro. Phát hiện, rồi rẽ nhánh; không bao giờ giả định.

## Phát hiện tính năng, hai đồng hồ

- **Lúc biên dịch**: `#if defined(__BYTE_ORDER__) && __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__` — chi phí runtime bằng không, nhưng buộc vào macro của compiler (riêng compiler, ghi nhãn).
- **Lúc chạy**: thăm dò byte, hoặc tiện ích endian của `stdbit.h` C23 khi có sẵn. Tốn một nhánh một lần, portable mọi nơi.

Chọn compile-time cho đường nóng, run-time cho tính khả chuyển được bảo đảm. Tài liệu hóa lựa chọn; tài liệu đó *chính là* lớp khả chuyển.

## Hợp đồng capstone

Checkpoint của mô-đun 24 lắp ráp cả khóa học: một lõi tiện ích portable (phát hiện endian + số học được kiểm + bản sao an toàn) cộng tích hợp kỷ luật của các mô-đun trước. Mọi hàm nó yêu cầu đã được xây và kiểm trong mô-đun trước — capstone là sự kết hợp dưới đặc tả, công việc thật của kỹ nghệ hệ thống.
""",
)

write_lesson(
    M24,
    L24B,
    "Capstone: Composing the Course",
    "No new machinery — the final project proves the old machinery composes.",
    16,
    """
## What the capstone asks

A **portable systems utility core** — the skeleton every real service grows from — built from four pieces you have already written in isolation:

1. **Endian detector** (module 24A) — runtime byte probe returning a stable verdict.
2. **Checked size arithmetic** (module 23) — multiplication that refuses overflow instead of wrapping into a tiny allocation.
3. **Safe copy** (module 23) — snprintf's semantics: refuse, never truncate silently.
4. **A framed record writer** (modules 20/21) — length-prefix then bytes, gathered into one logical write (module 21's spans).

The checkpoint assembles them under one specification and verifies the composition: detection that matches the platform truth (little-endian here), arithmetic that refuses, copies that refuse, and a framed payload that round-trips.

## Why composition is the test

Each piece passes its own tests; the capstone asks whether the *contracts* hold together:

- the framer trusts the size checker (a refusal upstream becomes a clean -1 downstream, not a crash);
- the detector's verdict decides byte order in the frame header — so a wrong detector makes a wrong-but-consistent frame, which the round-trip catches;
- every failure path returns a code, so the caller can always distinguish "did nothing" from "did partially" from "refused".

That distinction — clean refusal vs partial work vs silent corruption — is the whole subject of this course, dressed in one function.

## After this course

C Intermediate/Advanced territory beyond: concurrency at scale, allocator engineering, kernel interfaces. The modules named those doors; this course made sure you can walk to them — reading C the way tools see it, reasoning about UB like a compiler engineer, measuring like an experimentalist, and refusing like a security engineer.
""",
    "Capstone: kết hợp cả khóa học",
    "Không có máy móc mới — dự án cuối chứng minh máy móc cũ kết hợp được.",
    """
## Capstone yêu cầu gì

Một **lõi tiện ích hệ thống portable** — bộ khung mọi service thật lớn lên từ đó — xây từ bốn mảnh bạn đã viết riêng lẻ:

1. **Bộ dò endian** (mô-đun 24A) — thăm dò byte lúc chạy trả phán quyết ổn định.
2. **Số học kích thước được kiểm** (mô-đun 23) — phép nhân từ chối tràn thay vì wrap thành cấp phát tí hon.
3. **Bản sao an toàn** (mô-đun 23) — ngữ nghĩa của snprintf: từ chối, không bao giờ cắt cụt câm lặng.
4. **Bộ ghi bản ghi có khung** (mô-đun 20/21) — length-prefix rồi byte, gom thành một lần ghi logic (span của mô-đun 21).

Checkpoint lắp chúng dưới một đặc tả và kiểm chứng sự kết hợp: dò endian khớp sự thật nền tảng (little-endian tại đây), số học từ chối, bản sao từ chối, và payload có khung khép vòng được.

## Vì sao kết hợp mới là bài kiểm

Từng mảnh vượt bài kiểm riêng; capstone hỏi liệu các *hợp đồng* có cầm nhau:

- framer tin bộ kiểm kích thước (một lời từ chối thượng nguồn trở thành -1 sạch sẽ hạ nguồn, không phải crash);
- phán quyết của bộ dò quyết định thứ tự byte trong header khung — bộ dò sai cho ra khung sai-nhưng-nhất-quán, và vòng lặp khép bắt được điều đó;
- mọi đường lỗi trả mã, nên người gọi luôn phân biệt được "không làm gì" với "làm dở" với "từ chối".

Sự phân biệt đó — từ chối sạch vs công việc dở vs hỏng câm lặng — là toàn bộ chủ đề của khóa học này, khoác lên mình một hàm.

## Sau khóa học

Vùng đất C Intermediate/Advanced xa hơn: đồng thời ở quy mô lớn, kỹ nghệ allocator, giao diện kernel. Các mô-đun đã gọi tên những cánh cửa đó; khóa học này bảo đảm bạn có thể đi đến chúng — đọc C theo cách công cụ thấy, suy luận về UB như kỹ sư compiler, đo đạc như nhà thực nghiệm, và từ chối như kỹ sư an ninh.
""",
)

write_practice(
    M24,
    "ca-p24-portability",
    "Portability Probes",
    "Runtime endianness, compile-time detection, width-independent code — the portable toolkit, verified against this target's documented truth.",
    "Thăm dò tính khả chuyển",
    "Endianness lúc chạy, phát hiện lúc biên dịch, code độc lập độ rộng — bộ công cụ portable, kiểm chứng với sự thật đã tài liệu hóa của target này.",
    L24A,
    24,
    "advanced",
    [
        challenge(
            "ca24-endian-probe",
            "Runtime Endianness Verdict",
            "ISO C. Implement `int byte_order(void)` — place 1 in an unsigned int, inspect its first byte, return 1 for little-endian, 0 for big-endian. (Other orders are vanishingly rare; the probe may legitimately report either of the two it can distinguish.) Implement `const char *order_name(void)` returning the fixed string 'little' or 'big' via byte_order().",
            C_PRELUDE,
            [
                ("probe matches platform truth", "int o = byte_order();@NL@CHECK(o == 0 || o == 1);@NL@unsigned int probe = 1;@NL@unsigned char first = ((unsigned char *)&probe)[0];@NL@CHECK_EQ(o, (int)first);", "The function's verdict must agree with the raw byte probe on this machine (little-endian: 1)."),
                ("name agrees with verdict", "const char *n1 = order_name();@NL@int o2 = byte_order();@NL@if (o2 == 1) {@NL@CHECK_STR_EQ(n1, @T8@);@NL@} else {@NL@CHECK_STR_EQ(n1, @TBIG@);@NL@}", "The name is a pure function of the verdict — no hidden state."),
            ],
            level="guided",
        ),
        challenge(
            "ca24-width-independent",
            "Width-Independent Loop",
            "ISO C. Implement `unsigned long long checksum_upto(unsigned long long n)` — sum i from 0 to n-1 using unsigned long long (the widest unsigned this course assumes) and return the total. The point: the math must be correct for any n representable in unsigned long long, without ever falling into signed-overflow UB.",
            C_PRELUDE,
            [
                ("small sums", "CHECK_EQ(checksum_upto(4), 6ULL);@NL@CHECK_EQ(checksum_upto(1), 0ULL);@NL@CHECK_EQ(checksum_upto(0), 0ULL);", "0+1+2+3 = 6; zero iterations sum to zero."),
                ("known large sum", "CHECK_EQ(checksum_upto(1000000ULL), 499999500000ULL);", "Sum 0..999999 = n(n-1)/2 = 499999500000 — the formula check."),
                ("unsigned arithmetic stays defined", "unsigned long long big = 18446744073709551615ULL;@NL@unsigned long long wrapped = big + 1ULL;@NL@CHECK_EQ(wrapped, 0ULL);", "Unsigned wraparound is defined modular arithmetic — the one overflow that is never UB."),
            ],
            level="combination",
        ),
        challenge(
            "ca24-static-assert-layout",
            "Compile-Time Layout Contract",
            "ISO C11. Given `struct packet { unsigned char tag; unsigned short len; unsigned int crc; };` (declared for you), implement `size_t packet_min_size(void)` returning sizeof(struct packet) — it must be at least 7 (tag + len + crc with no padding can compress to 7 on some ABIs, but padding may grow it). Then `int packet_layout_sane(void)` returns 1 when offsetof(packet, crc) >= offsetof(packet, len) + sizeof(unsigned short) and 0 otherwise — the members must not overlap.",
            C_PRELUDE + "#include <stddef.h>@NL@struct packet { unsigned char tag; unsigned short len; unsigned int crc; };@NL@",
            [
                ("size covers all members", "CHECK(packet_min_size() >= 7);", "One byte plus two plus four is the floor: 7. Padding may make it larger — that is the ABI's documented choice."),
                ("members never overlap", "CHECK_EQ(packet_layout_sane(), 1);", "crc must start at or after the end of len — the compiler never overlaps members."),
            ],
            level="combination",
        ),
    ],
    {
        "ca24-endian-probe": vi_challenge(
            "Phán quyết endian lúc chạy",
            "ISO C. Cài `int byte_order(void)` — đặt 1 vào một unsigned int, xem byte đầu, trả 1 cho little-endian, 0 cho big-endian. Cài `const char *order_name(void)` trả chuỗi cố định 'little' hoặc 'big' qua byte_order().",
            [
                ("thăm dò khớp sự thật nền tảng", "Phán quyết của hàm phải đồng thuận với thăm dò byte thô trên máy này (little-endian: 1)."),
                ("tên đồng thuận với phán quyết", "Tên là hàm thuần của phán quyết — không trạng thái ẩn."),
            ],
        ),
        "ca24-width-independent": vi_challenge(
            "Vòng lặp độc lập độ rộng",
            "ISO C. Cài `unsigned long long checksum_upto(unsigned long long n)` — cộng i từ 0 đến n-1 dùng unsigned long long (kiểu unsigned rộng nhất khóa học giả định) và trả tổng. Điểm mấu chốt: phép toán phải đúng với mọi n biểu diễn được trong unsigned long long, không bao giờ rơi vào UB tràn số có dấu.",
            [
                ("tổng nhỏ", "0+1+2+3 = 6; không lần lặp nào cộng ra không."),
                ("tổng lớn đã biết", "Tổng 0..999999 = n(n-1)/2 = 499999500000 — kiểm tra bằng công thức."),
                ("số học unsigned luôn xác định", "Wraparound của unsigned là số học mô-đun xác định — phép tràn duy nhất không bao giờ là UB."),
            ],
        ),
        "ca24-static-assert-layout": vi_challenge(
            "Hợp đồng bố cục lúc biên dịch",
            "ISO C11. Cho `struct packet { unsigned char tag; unsigned short len; unsigned int crc; };` (đã khai báo), cài `size_t packet_min_size(void)` trả sizeof(struct packet) — phải ít nhất 7 (padding có thể làm lớn hơn). Rồi `int packet_layout_sane(void)` trả 1 khi offsetof(packet, crc) >= offsetof(packet, len) + sizeof(unsigned short), 0 nếu ngược lại — các thành viên không được chồng lấn.",
            [
                ("kích thước phủ mọi thành viên", "Một byte cộng hai cộng bốn là sàn: 7. Padding có thể làm lớn hơn — lựa chọn được tài liệu hóa của ABI."),
                ("thành viên không bao giờ chồng lấn", "crc phải bắt đầu từ hoặc sau cuối của len — compiler không bao giờ chồng lấn thành viên."),
            ],
        ),
    },
    solutions=[
        (
            "ca24-endian-probe",
            C_PRELUDE
            + "int byte_order(void) {@NL@"
            + "    unsigned int probe = 1;@NL@"
            + "    unsigned char first = ((unsigned char *)&probe)[0];@NL@"
            + "    return first == 1 ? 1 : 0;@NL@"
            + "}@NL@"
            + "const char *order_name(void) {@NL@"
            + "    return byte_order() == 1 ? @T8@ : @TBIG@;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "int byte_order(void) {@NL@"
            + "    unsigned int probe = 1;@NL@"
            + "    unsigned char last = ((unsigned char *)&probe)[sizeof(unsigned int) - 1];@NL@"
            + "    return last == 1 ? 1 : 0;@NL@"
            + "}@NL@"
            + "const char *order_name(void) {@NL@"
            + "    return byte_order() == 1 ? @T8@ : @TBIG@;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca24-width-independent",
            C_PRELUDE
            + "unsigned long long checksum_upto(unsigned long long n) {@NL@"
            + "    unsigned long long t = 0;@NL@"
            + "    for (unsigned long long i = 0; i < n; i++) t += i;@NL@"
            + "    return t;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "unsigned long long checksum_upto(unsigned long long n) {@NL@"
            + "    unsigned long long t = 0;@NL@"
            + "    for (unsigned long long i = 0; i <= n; i++) t += i;@NL@"
            + "    return t;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca24-static-assert-layout",
            C_PRELUDE + "#include <stddef.h>@NL@"
            + "struct packet { unsigned char tag; unsigned short len; unsigned int crc; };@NL@"
            + "size_t packet_min_size(void) {@NL@"
            + "    return sizeof(struct packet);@NL@"
            + "}@NL@"
            + "int packet_layout_sane(void) {@NL@"
            + "    return offsetof(struct packet, crc) >= offsetof(struct packet, len) + sizeof(unsigned short) ? 1 : 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + "#include <stddef.h>@NL@"
            + "struct packet { unsigned char tag; unsigned short len; unsigned int crc; };@NL@"
            + "size_t packet_min_size(void) {@NL@"
            + "    return sizeof(struct packet) / 2;@NL@"
            + "}@NL@"
            + "int packet_layout_sane(void) {@NL@"
            + "    return offsetof(struct packet, crc) >= offsetof(struct packet, len) + sizeof(unsigned short) ? 1 : 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_checkpoint(
    M24,
    L24CP,
    "Checkpoint: Portable Utility Core",
    "The course in one contract: detect, check, copy, frame — composed and verified end to end.",
    24,
    "See lesson.",
    "Kiểm tra: Lõi tiện ích portable",
    "Cả khóa học trong một hợp đồng: dò, kiểm, sao, đóng khung — kết hợp và kiểm chứng đầu-cuối.",
    "Xem bài học.",
    challenge(
        "ca24-checkpoint-core",
        "Checkpoint: Portable Utility Core",
        "ISO C. Implement the composed utility: `int core_init(void)` runs the endianness probe (1 little, 0 big) and stores it (see given static); `int core_safe_copy(char *dst, size_t dstsize, const char *src)` — module 23's refusing copy (0 ok, -1 refuse, dst untouched on refusal); `int core_frame(const char *payload, size_t plen, unsigned char *out, size_t outsz)` — write a 4-byte header (payload length, this platform's byte order via core_init's stored verdict, least-significant-byte-first when little-endian) then the payload bytes; refuse (-1) if 4+plen exceeds outsz or args are NULL; return 4+(int)plen on success. Implement `int core_unframe(const unsigned char *in, size_t insz, char *out, size_t outsz)` — read the 4-byte header (same order rules), refuse if the claimed length exceeds insz-4 or outsz-1, copy payload and NUL-terminate; return the payload length, -1 on refusal.",
        C_PRELUDE
        + "static int g_order = -1;@NL@",
        [
            ("frame round-trips", "CHECK_EQ(core_init(), 1);@NL@unsigned char fr[64];@NL@int flen = core_frame(@GS1@, 5, fr, sizeof fr);@NL@CHECK_EQ(flen, 9);@NL@char back[64] = {0};@NL@int ulen = core_unframe(fr, (size_t)flen, back, sizeof back);@NL@CHECK_EQ(ulen, 5);@NL@CHECK_STR_EQ(back, @GS1@);", "Little-endian header (05 00 00 00) then hello: the round trip restores the payload exactly."),
            ("refuses oversized frame", "unsigned char fr2[8];@NL@CHECK_EQ(core_frame(@GS1@, 5, fr2, sizeof fr2), -1);", "4 header + 5 payload = 9 > 8: refusal, no partial write semantics claimed."),
            ("unframe rejects bad header", "unsigned char fr3[16] = {255, 255, 255, 255, 104, 105};@NL@char out3[16] = {0};@NL@CHECK_EQ(core_unframe(fr3, 6, out3, sizeof out3), -1);", "A claimed length of 0xFFFFFFFF exceeds the 2 remaining bytes: refuse."),
            ("NULL discipline", "unsigned char frn[64];@NL@char backn[64] = {0};@NL@CHECK_EQ(core_frame(NULL, 5, frn, 64), -1);@NL@CHECK_EQ(core_unframe(NULL, 9, backn, 64), -1);", "NULL inputs refuse — the composed API keeps module 23's discipline."),
        ],
        level="capstone",
    ),
    {
        "ca24-checkpoint-core": vi_challenge(
            "Kiểm tra: Lõi tiện ích portable",
            "ISO C. Cài tiện ích kết hợp: `core_init` chạy thăm dò endian (1 little, 0 big) và lưu nó; `core_safe_copy` — bản sao từ chối của mô-đun 23; `core_frame` — ghi header 4 byte (độ dài payload theo thứ tự byte của nền tảng, byte-thấp-nhất-trước khi little-endian) rồi payload; từ chối (-1) nếu 4+plen vượt outsz hoặc args NULL; trả 4+(int)plen khi thành công. Cài `core_unframe` — đọc header 4 byte (cùng quy tắc), từ chối nếu độ dài tuyên bố vượt insz-4 hoặc outsz-1, sao payload và kết thúc NUL; trả độ dài payload, -1 khi từ chối.",
            [
                ("khung khép vòng", "Header little-endian (05 00 00 00) rồi hello: vòng lặp khôi phục payload chính xác."),
                ("từ chối khung quá cỡ", "4 header + 5 payload = 9 > 8: từ chối, không tự nhận ngữ nghĩa ghi một phần."),
                ("unframe chặn header xấu", "Độ dài tuyên bố 0xFFFFFFFF vượt 2 byte còn lại: từ chối."),
                ("kỷ luật NULL", "Đầu vào NULL từ chối — API kết hợp giữ kỷ luật của mô-đun 23."),
            ],
        ),
    },
    solution=
    C_PRELUDE
    + "static int g_order = -1;@NL@"
    + "int core_init(void) {@NL@"
    + "    unsigned int probe = 1;@NL@"
    + "    unsigned char first = ((unsigned char *)&probe)[0];@NL@"
    + "    g_order = first == 1 ? 1 : 0;@NL@"
    + "    return g_order;@NL@"
    + "}@NL@"
    + "int core_safe_copy(char *dst, size_t dstsize, const char *src) {@NL@"
    + "    if (dst == NULL || dstsize == 0 || src == NULL) return -1;@NL@"
    + "    size_t need = strlen(src) + 1;@NL@"
    + "    if (need > dstsize) return -1;@NL@"
    + "    for (size_t i = 0; i < need; i++) dst[i] = src[i];@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "int core_frame(const char *payload, size_t plen, unsigned char *out, size_t outsz) {@NL@"
    + "    if (payload == NULL || out == NULL) return -1;@NL@"
    + "    if (4 + plen > outsz || 4 + plen < 4) return -1;@NL@"
    + "    unsigned int n = (unsigned int)plen;@NL@"
    + "    if (g_order == 1) {@NL@"
    + "        out[0] = (unsigned char)(n & 255u);@NL@"
    + "        out[1] = (unsigned char)((n >> 8) & 255u);@NL@"
    + "        out[2] = (unsigned char)((n >> 16) & 255u);@NL@"
    + "        out[3] = (unsigned char)((n >> 24) & 255u);@NL@"
    + "    } else {@NL@"
    + "        out[0] = (unsigned char)((n >> 24) & 255u);@NL@"
    + "        out[1] = (unsigned char)((n >> 16) & 255u);@NL@"
    + "        out[2] = (unsigned char)((n >> 8) & 255u);@NL@"
    + "        out[3] = (unsigned char)(n & 255u);@NL@"
    + "    }@NL@"
    + "    for (size_t i = 0; i < plen; i++) out[4 + i] = (unsigned char)payload[i];@NL@"
    + "    return (int)(4 + plen);@NL@"
    + "}@NL@"
    + "int core_unframe(const unsigned char *in, size_t insz, char *out, size_t outsz) {@NL@"
    + "    if (in == NULL || out == NULL) return -1;@NL@"
    + "    if (insz < 4) return -1;@NL@"
    + "    unsigned int n;@NL@"
    + "    if (g_order == 1) {@NL@"
    + "        n = (unsigned int)in[0] | ((unsigned int)in[1] << 8) | ((unsigned int)in[2] << 16) | ((unsigned int)in[3] << 24);@NL@"
    + "    } else {@NL@"
    + "        n = ((unsigned int)in[0] << 24) | ((unsigned int)in[1] << 16) | ((unsigned int)in[2] << 8) | (unsigned int)in[3];@NL@"
    + "    }@NL@"
    + "    if (n > insz - 4) return -1;@NL@"
    + "    if (n + 1 > outsz) return -1;@NL@"
    + "    for (unsigned int i = 0; i < n; i++) out[i] = (char)in[4 + i];@NL@"
    + "    out[n] = 0;@NL@"
    + "    return (int)n;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
    wrong=
    C_PRELUDE
    + "static int g_order = -1;@NL@"
    + "int core_init(void) {@NL@"
    + "    unsigned int probe = 1;@NL@"
    + "    unsigned char first = ((unsigned char *)&probe)[0];@NL@"
    + "    g_order = first == 1 ? 1 : 0;@NL@"
    + "    return g_order;@NL@"
    + "}@NL@"
    + "int core_safe_copy(char *dst, size_t dstsize, const char *src) {@NL@"
    + "    if (dst == NULL || dstsize == 0 || src == NULL) return -1;@NL@"
    + "    size_t need = strlen(src) + 1;@NL@"
    + "    if (need > dstsize) return -1;@NL@"
    + "    for (size_t i = 0; i < need; i++) dst[i] = src[i];@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "int core_frame(const char *payload, size_t plen, unsigned char *out, size_t outsz) {@NL@"
    + "    if (payload == NULL || out == NULL) return -1;@NL@"
    + "    unsigned int n = (unsigned int)plen;@NL@"
    + "    out[0] = (unsigned char)(n & 255u);@NL@"
    + "    out[1] = (unsigned char)((n >> 8) & 255u);@NL@"
    + "    out[2] = (unsigned char)((n >> 16) & 255u);@NL@"
    + "    out[3] = (unsigned char)((n >> 24) & 255u);@NL@"
    + "    for (size_t i = 0; i < plen; i++) out[4 + i] = (unsigned char)payload[i];@NL@"
    + "    return (int)(4 + plen);@NL@"
    + "}@NL@"
    + "int core_unframe(const unsigned char *in, size_t insz, char *out, size_t outsz) {@NL@"
    + "    if (in == NULL || out == NULL) return -1;@NL@"
    + "    if (insz < 4) return -1;@NL@"
    + "    unsigned int n = (unsigned int)in[0] | ((unsigned int)in[1] << 8) | ((unsigned int)in[2] << 16) | ((unsigned int)in[3] << 24);@NL@"
    + "    if (n > insz - 4) return -1;@NL@"
    + "    for (unsigned int i = 0; i < n; i++) out[i] = (char)in[4 + i];@NL@"
    + "    out[n] = 0;@NL@"
    + "    return (int)n;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
)
