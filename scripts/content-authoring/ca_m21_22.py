#!/usr/bin/env python3
"""C Advanced — batch 11: modules 21 (performance-io) and 22 (performance-tuning).
Zero typed backslashes: @NL@ = statement separator, @CE@ = C string escape,
@T*/@J*/@LV*@ = runtime placeholder tokens expanded by ca.py. Solutions are
complete standalone programs absorbed into test TUs via #define main."""
from ca import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

POSIX21 = (
    "#define _POSIX_C_SOURCE 200809L@NL@"
    "#include <unistd.h>@NL@"
    "#include <fcntl.h>@NL@"
    "#include <sys/mman.h>@NL@"
    "#include <sys/stat.h>@NL@"
    "#include <sys/uio.h>@NL@"
    "#include <time.h>@NL@"
    "#include <errno.h>@NL@"
)

# ================= MODULE 21: ca-performance-io ==============================
M21 = "ca-performance-io"

L21A = "ca-buffered-vs-raw"
L21B = "ca-mmap-and-measure"
L21CP = "ca-checkpoint-m21"

write_module(
    M21,
    "High-Performance I/O: Buffers, writev, mmap",
    "Why I/O dominates real programs: buffering semantics, gathered writes, memory-mapped files, and the measurement discipline that separates real wins from superstition. POSIX mechanisms, labeled as such.",
    "I/O hiệu năng cao: bộ đệm, writev, mmap",
    "Vì sao I/O thống trị chương trình thật: ngữ nghĩa bộ đệm, ghi gom cụm, memory-mapped files, và kỷ luật đo đạc phân biệt thắng lợi thật với mê tín. Cơ chế POSIX, ghi nhãn rõ ràng.",
    [L21A, L21B, L21CP],
    ["ca-p21-io"],
)

write_lesson(
    M21,
    L21A,
    "Buffered vs Raw: Who Talks to the Kernel",
    "Every byte that crosses the syscall boundary costs; buffering is the art of crossing less often without breaking correctness.",
    20,
    """
## The two layers

- **Raw I/O** — `read(fd, buf, n)` / `write(fd, buf, n)`: one syscall per call, exactly as many bytes as the kernel happens to give or take. Unbuffered; you own every boundary.
- **Buffered I/O** — `fwrite`/`fread` on a `FILE *`: the C library collects small requests into a user-space buffer and crosses the kernel boundary rarely. `<stdio.h>` is ISO C; `read`/`write` are POSIX.

A 4096-byte read of 64-byte records costs 64 syscalls raw — or 1 syscall buffered. The kernel transition is thousands of cycles; the copy into your buffer is single-digit cycles per byte. That ratio is the whole game.

## writev: one syscall, many buffers

When your data already lives in N separate buffers (header here, payload there), copying into one scratch buffer costs a pass — `writev` gathers them in the kernel:

```c
#define _POSIX_C_SOURCE 200809L
#include <sys/uio.h>              /* POSIX */

struct iovec iov[2];
iov[0].iov_base = header;  iov[0].iov_len = hlen;
iov[1].iov_base = payload; iov[1].iov_len = plen;
ssize_t n = writev(fd, iov, 2);   /* one syscall, hlen+plen bytes */
```

This is what real servers use to send `length-prefix + body` without a defensive copy.

## When buffering betrays you

- **Ordering**: stdout via stdio vs `write(STDOUT_FILENO, ...)` in the same process can interleave *wrongly* — two independent buffers. One stream per destination, or flush deliberately.
- **Crash semantics**: buffered bytes die in the buffer on `abort()`; raw bytes are already gone with the kernel. Logs that must survive crashes use unbuffered writes (or explicit `fflush`).
- **Interactive prompts**: `printf("input: ")` without `fflush(stdout)` may show nothing before `scanf` blocks on some setups. Prompt, flush, then read.

## The discipline

Never argue from vibes: measure syscall counts (`strace` off-platform; on-platform, reason from the code) and wall time with `CLOCK_MONOTONIC` — module 21's second lesson makes that a habit.
""",
    "Bộ đệm hay thô: ai nói chuyện với kernel",
    "Mỗi byte vượt biên syscall đều tốn kém; buffering là nghệ thuật vượt ít hơn mà không phá tính đúng đắn.",
    """
## Hai lớp

- **I/O thô** — `read(fd, buf, n)` / `write(fd, buf, n)`: một syscall mỗi lần gọi, đúng số byte kernel tình cờ cho hoặc nhận. Không bộ đệm; bạn sở hữu mọi biên.
- **I/O đệm** — `fwrite`/`fread` trên `FILE *`: thư viện C gom các yêu cầu nhỏ vào bộ đệm user-space và hiếm khi vượt biên kernel. `<stdio.h>` là ISO C; `read`/`write` là POSIX.

Một lần đọc 4096 byte của các bản ghi 64-byte tốn 64 syscall kiểu thô — hoặc 1 syscall kiểu đệm. Chuyển tiếp kernel tốn hàng nghìn chu kỳ; sao chép vào bộ đệm của bạn chỉ vài chu kỳ mỗi byte. Tỉ lệ đó là toàn bộ trò chơi.

## writev: một syscall, nhiều buffer

Khi dữ liệu của bạn đã nằm trong N buffer riêng (header đây, payload kia), sao chép vào một buffer tạm tốn một lượt quét — `writev` gom chúng trong kernel:

```c
#define _POSIX_C_SOURCE 200809L
#include <sys/uio.h>              /* POSIX */

struct iovec iov[2];
iov[0].iov_base = header;  iov[0].iov_len = hlen;
iov[1].iov_base = payload; iov[1].iov_len = plen;
ssize_t n = writev(fd, iov, 2);   /* một syscall, hlen+plen byte */
```

Đây là thứ server thật dùng để gửi `length-prefix + body` mà không cần bản sao phòng thủ.

## Khi bộ đệm phản bội bạn

- **Thứ tự**: stdout qua stdio và `write(STDOUT_FILENO, ...)` trong cùng tiến trình có thể trộn lẫn *sai* — hai bộ đệm độc lập. Một stream cho mỗi đích, hoặc flush có chủ đích.
- **Ngữ nghĩa khi crash**: byte trong bộ đệm chết ngay tại bộ đệm khi `abort()`; byte thô đã kịp đi với kernel. Log phải sống sót qua crash dùng ghi không đệm (hoặc `fflush` rõ ràng).
- **Prompt tương tác**: `printf("input: ")` không có `fflush(stdout)` có thể hiện gì trước khi `scanf` chặn, trên một số cấu hình. In prompt, flush, rồi đọc.

## Kỷ luật

Không bao giờ tranh luận bằng cảm tính: đếm syscall (`strace` ngoài nền tảng; trên nền tảng, suy luận từ code) và đo thời gian thực với `CLOCK_MONOTONIC` — bài hai của mô-đun 21 biến điều đó thành thói quen.
""",
)

write_lesson(
    M21,
    L21B,
    "mmap and the Measurement Habit",
    "Mapping files into memory turns I/O into pointer arithmetic — and measurement turns opinions into numbers.",
    20,
    """
## mmap: the file as memory

```c
#define _POSIX_C_SOURCE 200809L
#include <sys/mman.h>       /* POSIX */
#include <fcntl.h>
#include <sys/stat.h>

int fd = open(path, O_RDONLY);
struct stat st;
fstat(fd, &st);
char *p = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
/* use p[0] .. p[st.st_size-1] like any memory */
munmap(p, st.st_size);
close(fd);
```

No `read` call, no buffer sizing: bytes materialize on first touch, one page (4 KiB) at a time. The kernel owns the cache; `munmap` releases the mapping, not the data. `MAP_PRIVATE` forbids writing through; `MAP_SHARED` propagates writes back to the file.

Honest tradeoffs: mmap wins for random access to large files and zero-copy consumption; plain `read` wins for strictly sequential one-pass scans where page-fault overhead exceeds copy cost — and it is simpler to reason about. Measure, then choose.

## Measuring: the only credible witness

```c
#include <time.h>                 /* ISO C clock — POSIX clock_gettime */
struct timespec t0, t1;
clock_gettime(CLOCK_MONOTONIC, &t0);
/* work */
clock_gettime(CLOCK_MONOTONIC, &t1);
double ms = (t1.tv_sec - t0.tv_sec) * 1e3 + (t1.tv_nsec - t0.tv_nsec) / 1e6;
```

`CLOCK_MONOTONIC` never goes backwards and ignores wall-clock adjustments — the only clock for durations. `clock_gettime` is POSIX here (`CLOCK_MONOTONIC` itself is POSIX, not ISO C).

## Three benchmark traps

1. **Dead-code elimination**: a loop whose result is never used may be deleted whole. Consume the result — print it, or accumulate into a `volatile` sink.
2. **The one-shot lie**: first touch pays page-fault and cache-fill costs. Warm up, then measure many iterations, then divide.
3. **Micro vs macro**: an inner-loop win that makes the outer loop cache-hostile is a loss. Measure the whole program path, not the function.

Numbers you did not measure yourself are folklore. This course asserts *mechanisms*, never timings.
""",
    "mmap và thói quen đo đạc",
    "Ánh xạ tập tin vào bộ nhớ biến I/O thành số học con trỏ — và đo đạc biến ý kiến thành con số.",
    """
## mmap: tập tin như bộ nhớ

```c
#define _POSIX_C_SOURCE 200809L
#include <sys/mman.h>       /* POSIX */
#include <fcntl.h>
#include <sys/stat.h>

int fd = open(path, O_RDONLY);
struct stat st;
fstat(fd, &st);
char *p = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
/* dùng p[0] .. p[st.st_size-1] như bất kỳ bộ nhớ nào */
munmap(p, st.st_size);
close(fd);
```

Không lời gọi `read`, không tính cỡ buffer: byte hiện ra khi chạm lần đầu, từng trang (4 KiB) một. Kernel sở hữu cache; `munmap` thu hồi mapping, không thu hồi dữ liệu. `MAP_PRIVATE` cấm ghi qua mapping; `MAP_SHARED` đưa ghi ngược lại tập tin.

Đánh đổi trung thực: mmap thắng với truy cập ngẫu nhiên trên tập tin lớn và tiêu thụ zero-copy; `read` thường thắng với quét tuần tự một lượt, nơi chi tiết page-fault vượt chi phí sao chép — và dễ suy luận hơn. Đo, rồi chọn.

## Đo đạc: nhân chứng duy nhất đáng tin

```c
#include <time.h>
struct timespec t0, t1;
clock_gettime(CLOCK_MONOTONIC, &t0);
/* công việc */
clock_gettime(CLOCK_MONOTONIC, &t1);
double ms = (t1.tv_sec - t0.tv_sec) * 1e3 + (t1.tv_nsec - t0.tv_nsec) / 1e6;
```

`CLOCK_MONOTONIC` không bao giờ đi lùi và bỏ qua chỉnh sửa đồng hồ treo tường — đồng hồ duy nhất đáng tin cho khoảng thời gian. `clock_gettime` là POSIX ở đây (`CLOCK_MONOTONIC` cũng là POSIX, không phải ISO C).

## Ba cái bẫy benchmark

1. **Loại bỏ code chết**: vòng lặp không ai dùng kết quả có thể bị xóa nguyên. Tiêu thụ kết quả — in ra, hoặc cộng dồn vào một `volatile` sink.
2. **Lừa dối một lần chạy**: lần chạm đầu trả chi phí page-fault và làm đầy cache. Làm ấm, rồi đo nhiều lần lặp, rồi chia.
3. **Micro vs macro**: thắng ở vòng trong mà làm vòng ngoài ghét cache là một thất bại. Đo cả đường đi của chương trình, không phải một hàm.

Con số bạn không tự đo là chuyện kể. Khóa học này chỉ khẳng định *cơ chế*, không bao giờ khẳng định thời gian.
""",
)

write_practice(
    M21,
    "ca-p21-io",
    "I/O Mechanics Drills",
    "Gathered spans, buffer-flush arithmetic, mmap sums, and a mmap-backed line counter — all verified against real file/kernel behavior.",
    "Bài tập cơ chế I/O",
    "Gom spans, số học flush bộ đệm, tổng qua mmap, và bộ đếm dòng dựa trên mmap — tất cả kiểm chứng với hành vi file/kernel thật.",
    L21A,
    26,
    "advanced",
    [
        challenge(
            "ca21-gather-spans",
            "Gather Spans Like writev",
            "POSIX-flavored design. Given `struct span { const char *base; size_t len; };`, implement `size_t spans_total(const struct span *s, size_t n)` (sum of lens; NULL s with n>0 returns (size_t)-1) and `void spans_gather(const struct span *s, size_t n, char *out)` (concatenate the spans into out in order; assume out is large enough — but skip NULL bases).",
            C_PRELUDE + "struct span { const char *base; size_t len; };@NL@",
            [
                ("total and gather", "struct span s[3];@NL@s[0].base = @GS1@;@NL@s[0].len = 5;@NL@s[1].base = @GS2@;@NL@s[1].len = 1;@NL@s[2].base = @GS3@;@NL@s[2].len = 5;@NL@CHECK_EQ(spans_total(s, 3), 11);@NL@char out[16] = {0};@NL@spans_gather(s, 3, out);@NL@CHECK_STR_EQ(out, @GS4@);", "Three buffers, one pass: gather reproduces the logical byte stream in order."),
                ("empty list", "CHECK_EQ(spans_total(NULL, 0), 0);@NL@CHECK_EQ(spans_total(NULL, 3), (size_t)-1);", "n==0 means nothing to sum (0 is correct); NULL with n>0 is a contract violation."),
                ("NULL base skipped", "struct span t[2];@NL@t[0].base = NULL;@NL@t[0].len = 3;@NL@t[1].base = @GS3@;@NL@t[1].len = 5;@NL@CHECK_EQ(spans_total(t, 2), 8);@NL@char out2[16] = {0};@NL@spans_gather(t, 2, out2);@NL@CHECK_STR_EQ(out2, @GS3@);", "A NULL base contributes nothing to the output — the gather must skip, never dereference."),
            ],
            level="guided",
        ),
        challenge(
            "ca21-buffered-writer",
            "Flush Only When Full",
            "ISO C design of stdio's rule. Given `struct bw { char buf[64]; size_t n; int flushes; };` (zero-initialized before use), implement `void bw_write(struct bw *w, const char *s, size_t len)` — append bytes; the moment one more byte would exceed 64, flush first (flushes++, n=0) and continue. Implement `size_t bw_pending(const struct bw *w)` returning w->n. NULL guards: w or s NULL with len>0 does nothing.",
            C_PRELUDE,
            [
                ("fill exactly then overflow", "struct bw w = {0};@NL@char big[129];@NL@memset(big, 65, 129);@NL@bw_write(&w, big, 128);@NL@CHECK_EQ(bw_pending(&w), 64);@NL@CHECK_EQ(w.flushes, 1);@NL@bw_write(&w, big, 1);@NL@CHECK_EQ(w.flushes, 2);@NL@CHECK_EQ(bw_pending(&w), 1);", "128 bytes fill the 64-buffer exactly once and overflow once: 1 flush, 64 pending. One more byte forces the second flush."),
                ("single small write stays", "struct bw w2 = {0};@NL@bw_write(&w2, @T6@, 8);@NL@CHECK_EQ(bw_pending(&w2), 8);@NL@CHECK_EQ(w2.flushes, 0);", "Nothing overflows: zero flushes — buffering is the whole point."),
                ("NULL guards", "struct bw w3 = {0};@NL@bw_write(&w3, NULL, 4);@NL@bw_write(NULL, @T6@, 4);@NL@bw_write(&w3, NULL, 0);@NL@CHECK_EQ(bw_pending(&w3), 0);@NL@CHECK_EQ(w3.flushes, 0);", "NULL inputs must change nothing — refuse by ignoring, not by crashing."),
            ],
            level="combination",
        ),
        challenge(
            "ca21-mmap-sum",
            "Sum a File Through mmap",
            "POSIX. Implement `long sum_bytes_mmap(const char *path)` — open O_RDONLY, fstat for size, mmap PROT_READ MAP_PRIVATE, sum all bytes as unsigned char, munmap, close, return the sum; return -1 on any failure (open/fstat/mmap/munmap). An empty file sums to 0.",
            C_PRELUDE + POSIX21 + "static const char *GIVEN_PATTERN_PATH = @TPATH@;@NL@"
            + "static long make_pattern_file(void) {@NL@"
            + "    int fd = open(GIVEN_PATTERN_PATH, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@"
            + "    if (fd < 0) return -1;@NL@"
            + "    unsigned char byte[256];@NL@"
            + "    for (int i = 0; i < 256; i++) byte[i] = (unsigned char)i;@NL@"
            + "    for (int r = 0; r < 16; r++) {@NL@"
            + "        if (write(fd, byte, 256) != 256) { close(fd); return -1; }@NL@"
            + "    }@NL@"
            + "    close(fd);@NL@"
            + "    return 0;@NL@"
            + "}@NL@",
            [
                ("sums the 0..255 pattern", "CHECK_EQ(make_pattern_file(), 0);@NL@long s = sum_bytes_mmap(GIVEN_PATTERN_PATH);@NL@CHECK_EQ(s, 522240);", "The file holds sixteen 0..255 ramps: 16 times 32640 — sum 522240."),
                ("missing file", "CHECK_EQ(sum_bytes_mmap(@TMISS@), -1);", "A path that cannot be opened is an error, not a sum of zero."),
            ],
            level="combination",
        ),
    ],
    {
        "ca21-gather-spans": vi_challenge(
            "Gom span như writev",
            "Thiết kế kiểu POSIX. Cho `struct span { const char *base; size_t len; };`, cài `size_t spans_total(const struct span *s, size_t n)` (tổng len; NULL s với n>0 trả (size_t)-1) và `void spans_gather(const struct span *s, size_t n, char *out)` (nối các span vào out theo thứ tự; base NULL thì bỏ qua).",
            [
                ("tổng và gom", "Ba buffer, một lượt: gather tái tạo dòng byte logic đúng thứ tự."),
                ("danh sách rỗng", "n==0 nghĩa là không có gì để cộng (0 là đúng); NULL với n>0 là vi phạm hợp đồng."),
                ("base NULL bị bỏ qua", "base NULL không đóng góp gì vào output — gather phải bỏ qua, không bao giờ dereference."),
            ],
        ),
        "ca21-buffered-writer": vi_challenge(
            "Chỉ flush khi đầy",
            "Thiết kế ISO C cho quy tắc của stdio. Cho `struct bw { char buf[64]; size_t n; int flushes; };` (zero hóa trước khi dùng), cài `void bw_write(struct bw *w, const char *s, size_t len)` — nối byte; ngay khi thêm một byte sẽ vượt 64 thì flush trước (flushes++, n=0) rồi tiếp tục. Cài `size_t bw_pending(const struct bw *w)`. Guard NULL: w hoặc s NULL với len>0 thì không làm gì.",
            [
                ("đầy vừa khít rồi tràn", "128 byte làm đầy buffer 64 đúng một lần và tràn một lần: 1 flush, 64 pending. Thêm một byte ép flush thứ hai."),
                ("ghi nhỏ một lần ở lại", "Không có gì tràn: không flush — buffering chính là điểm mấu chốt."),
                ("guard NULL", "Đầu vào NULL không được đổi gì — từ chối bằng cách bỏ qua, không crash."),
            ],
        ),
        "ca21-mmap-sum": vi_challenge(
            "Tổng tập tin qua mmap",
            "POSIX. Cài `long sum_bytes_mmap(const char *path)` — open O_RDONLY, fstat lấy kích thước, mmap PROT_READ MAP_PRIVATE, cộng mọi byte như unsigned char, munmap, close, trả tổng; trả -1 khi bất kỳ lỗi nào. Tập tin rỗng có tổng 0.",
            [
                ("cộng mẫu 0..255", "Tập tin chứa mười sáu dãy 0..255: tổng 32640."),
                ("tập tin thiếu", "Đường dẫn không mở được là lỗi, không phải tổng không."),
            ],
        ),
    },
    solutions=[
        (
            "ca21-gather-spans",
            C_PRELUDE
            + "struct span { const char *base; size_t len; };@NL@"
            + "size_t spans_total(const struct span *s, size_t n) {@NL@"
            + "    if (s == NULL) return n == 0 ? 0 : (size_t)-1;@NL@"
            + "    size_t t = 0;@NL@"
            + "    for (size_t i = 0; i < n; i++) t += s[i].len;@NL@"
            + "    return t;@NL@"
            + "}@NL@"
            + "void spans_gather(const struct span *s, size_t n, char *out) {@NL@"
            + "    if (s == NULL || out == NULL) return;@NL@"
            + "    size_t k = 0;@NL@"
            + "    for (size_t i = 0; i < n; i++) {@NL@"
            + "        if (s[i].base == NULL) continue;@NL@"
            + "        for (size_t j = 0; j < s[i].len; j++) out[k++] = s[i].base[j];@NL@"
            + "    }@NL@"
            + "    out[k] = 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "struct span { const char *base; size_t len; };@NL@"
            + "size_t spans_total(const struct span *s, size_t n) {@NL@"
            + "    if (s == NULL) return n == 0 ? 0 : (size_t)-1;@NL@"
            + "    size_t t = 0;@NL@"
            + "    for (size_t i = 0; i < n; i++) t += s[i].len;@NL@"
            + "    return t;@NL@"
            + "}@NL@"
            + "void spans_gather(const struct span *s, size_t n, char *out) {@NL@"
            + "    if (s == NULL || out == NULL) return;@NL@"
            + "    size_t k = 0;@NL@"
            + "    for (size_t i = n; i-- > 0;) {@NL@"
            + "        if (s[i].base == NULL) continue;@NL@"
            + "        for (size_t j = 0; j < s[i].len; j++) out[k++] = s[i].base[j];@NL@"
            + "    }@NL@"
            + "    out[k] = 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca21-buffered-writer",
            C_PRELUDE
            + "struct bw { char buf[64]; size_t n; int flushes; };@NL@"
            + "void bw_write(struct bw *w, const char *s, size_t len) {@NL@"
            + "    if (w == NULL || s == NULL || len == 0) return;@NL@"
            + "    for (size_t i = 0; i < len; i++) {@NL@"
            + "        if (w->n == 64) {@NL@"
            + "            w->flushes++;@NL@"
            + "            w->n = 0;@NL@"
            + "        }@NL@"
            + "        w->buf[w->n++] = s[i];@NL@"
            + "    }@NL@"
            + "}@NL@"
            + "size_t bw_pending(const struct bw *w) {@NL@"
            + "    return w == NULL ? 0 : w->n;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "struct bw { char buf[64]; size_t n; int flushes; };@NL@"
            + "void bw_write(struct bw *w, const char *s, size_t len) {@NL@"
            + "    if (w == NULL || s == NULL || len == 0) return;@NL@"
            + "    for (size_t i = 0; i < len; i++) {@NL@"
            + "        w->buf[w->n++] = s[i];@NL@"
            + "        if (w->n >= 8) {@NL@"
            + "            w->flushes++;@NL@"
            + "            w->n = 0;@NL@"
            + "        }@NL@"
            + "    }@NL@"
            + "}@NL@"
            + "size_t bw_pending(const struct bw *w) {@NL@"
            + "    return w == NULL ? 0 : w->n;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca21-mmap-sum",
            C_PRELUDE + POSIX21
            + "static const char *GIVEN_PATTERN_PATH = @TPATH@;@NL@"
            + "static long make_pattern_file(void) {@NL@"
            + "    int fd = open(GIVEN_PATTERN_PATH, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@"
            + "    if (fd < 0) return -1;@NL@"
            + "    unsigned char byte[256];@NL@"
            + "    for (int i = 0; i < 256; i++) byte[i] = (unsigned char)i;@NL@"
            + "    for (int r = 0; r < 16; r++) {@NL@"
            + "        if (write(fd, byte, 256) != 256) { close(fd); return -1; }@NL@"
            + "    }@NL@"
            + "    close(fd);@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "long sum_bytes_mmap(const char *path) {@NL@"
            + "    if (path == NULL) return -1;@NL@"
            + "    int fd = open(path, O_RDONLY);@NL@"
            + "    if (fd < 0) return -1;@NL@"
            + "    struct stat st;@NL@"
            + "    if (fstat(fd, &st) != 0) { close(fd); return -1; }@NL@"
            + "    if (st.st_size == 0) { close(fd); return 0; }@NL@"
            + "    void *mp = mmap(NULL, (size_t)st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);@NL@"
            + "    if (mp == MAP_FAILED) { close(fd); return -1; }@NL@"
            + "    const unsigned char *p = (const unsigned char *)mp;@NL@"
            + "    long total = 0;@NL@"
            + "    for (off_t i = 0; i < st.st_size; i++) total += p[i];@NL@"
            + "    munmap(mp, (size_t)st.st_size);@NL@"
            + "    close(fd);@NL@"
            + "    return total;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + POSIX21
            + "static const char *GIVEN_PATTERN_PATH = @TPATH@;@NL@"
            + "static long make_pattern_file(void) {@NL@"
            + "    int fd = open(GIVEN_PATTERN_PATH, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@"
            + "    if (fd < 0) return -1;@NL@"
            + "    unsigned char byte[256];@NL@"
            + "    for (int i = 0; i < 256; i++) byte[i] = (unsigned char)i;@NL@"
            + "    for (int r = 0; r < 16; r++) {@NL@"
            + "        if (write(fd, byte, 256) != 256) { close(fd); return -1; }@NL@"
            + "    }@NL@"
            + "    close(fd);@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "long sum_bytes_mmap(const char *path) {@NL@"
            + "    if (path == NULL) return -1;@NL@"
            + "    int fd = open(path, O_RDONLY);@NL@"
            + "    if (fd < 0) return -1;@NL@"
            + "    struct stat st;@NL@"
            + "    if (fstat(fd, &st) != 0) { close(fd); return -1; }@NL@"
            + "    if (st.st_size == 0) { close(fd); return 0; }@NL@"
            + "    void *mp = mmap(NULL, (size_t)st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);@NL@"
            + "    if (mp == MAP_FAILED) { close(fd); return -1; }@NL@"
            + "    const unsigned char *p = (const unsigned char *)mp;@NL@"
            + "    long total = 0;@NL@"
            + "    for (off_t i = 0; i < st.st_size - 1; i++) total += p[i];@NL@"
            + "    munmap(mp, (size_t)st.st_size);@NL@"
            + "    close(fd);@NL@"
            + "    return total;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_checkpoint(
    M21,
    L21CP,
    "Checkpoint: mmap Line Counter",
    "One honest file-processing primitive: count lines through a memory mapping, with failure paths that fail loudly.",
    20,
    "See lesson.",
    "Kiểm tra: Bộ đếm dòng qua mmap",
    "Một nguyên thủy xử lý tập tin trung thực: đếm dòng qua memory mapping, với các đường lỗi báo lỗi rõ ràng.",
    "Xem bài học.",
    challenge(
        "ca21-checkpoint-lines",
        "Checkpoint: mmap Line Counter",
        "POSIX. Implement `long count_lines_mmap(const char *path)` — open, fstat, mmap PROT_READ MAP_PRIVATE, count newline bytes, munmap, close; return the count. Empty file returns 0. Any failure (open/fstat/mmap) returns -1. A trailing newline produces no extra phantom line beyond the newlines actually counted.",
        C_PRELUDE + POSIX21
        + "static const char *GIVEN_LINES_PATH = @TLINES@;@NL@"
        + "static long make_lines_file(long n) {@NL@"
        + "    int fd = open(GIVEN_LINES_PATH, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@"
        + "    if (fd < 0) return -1;@NL@"
        + "    for (long i = 0; i < n; i++) {@NL@"
        + "        if (write(fd, @TLINE@, 6) != 6) { close(fd); return -1; }@NL@"
        + "    }@NL@"
        + "    close(fd);@NL@"
        + "    return 0;@NL@"
        + "}@NL@",
        [
            ("counts newlines", "CHECK_EQ(make_lines_file(7), 0);@NL@CHECK_EQ(count_lines_mmap(GIVEN_LINES_PATH), 7);", "Seven newline-terminated records: seven newlines counted through the mapping."),
            ("empty file is zero", "int fd = open(GIVEN_LINES_PATH, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@CHECK(fd >= 0);@NL@close(fd);@NL@CHECK_EQ(count_lines_mmap(GIVEN_LINES_PATH), 0);", "Zero bytes map to nothing to count: 0, not an error."),
            ("missing file fails", "CHECK_EQ(count_lines_mmap(@TMISS@), -1);", "A path that cannot be opened returns -1 — failures must be visible."),
        ],
        level="capstone",
    ),
    {
        "ca21-checkpoint-lines": vi_challenge(
            "Kiểm tra: Bộ đếm dòng qua mmap",
            "POSIX. Cài `long count_lines_mmap(const char *path)` — open, fstat, mmap PROT_READ MAP_PRIVATE, đếm byte newline, munmap, close; trả số đếm. Tập tin rỗng trả 0. Bất kỳ lỗi nào trả -1.",
            [
                ("đếm newline", "Bảy bản ghi kết thúc newline: bảy newline được đếm qua mapping."),
                ("tập tin rỗng là không", "Không byte nào thì không có gì để đếm: 0, không phải lỗi."),
                ("tập tin thiếu thất bại", "Đường dẫn không mở được trả -1 — lỗi phải nhìn thấy được."),
            ],
        ),
    },
    solution=
    C_PRELUDE + POSIX21
    + "static const char *GIVEN_LINES_PATH = @TLINES@;@NL@"
    + "static long make_lines_file(long n) {@NL@"
    + "    int fd = open(GIVEN_LINES_PATH, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@"
    + "    if (fd < 0) return -1;@NL@"
    + "    for (long i = 0; i < n; i++) {@NL@"
    + "        if (write(fd, @TLINE@, 6) != 6) { close(fd); return -1; }@NL@"
    + "    }@NL@"
    + "    close(fd);@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "long count_lines_mmap(const char *path) {@NL@"
    + "    if (path == NULL) return -1;@NL@"
    + "    int fd = open(path, O_RDONLY);@NL@"
    + "    if (fd < 0) return -1;@NL@"
    + "    struct stat st;@NL@"
    + "    if (fstat(fd, &st) != 0) { close(fd); return -1; }@NL@"
    + "    if (st.st_size == 0) { close(fd); return 0; }@NL@"
    + "    void *mp = mmap(NULL, (size_t)st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);@NL@"
    + "    if (mp == MAP_FAILED) { close(fd); return -1; }@NL@"
    + "    const char *p = (const char *)mp;@NL@"
    + "    long lines = 0;@NL@"
    + "    for (off_t i = 0; i < st.st_size; i++) {@NL@"
    + "        if (p[i] == 10) lines++;@NL@"
    + "    }@NL@"
    + "    munmap(mp, (size_t)st.st_size);@NL@"
    + "    close(fd);@NL@"
    + "    return lines;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
    wrong=
    C_PRELUDE + POSIX21
    + "static const char *GIVEN_LINES_PATH = @TLINES@;@NL@"
    + "static long make_lines_file(long n) {@NL@"
    + "    int fd = open(GIVEN_LINES_PATH, O_RDWR | O_CREAT | O_TRUNC, 0600);@NL@"
    + "    if (fd < 0) return -1;@NL@"
    + "    for (long i = 0; i < n; i++) {@NL@"
    + "        if (write(fd, @TLINE@, 6) != 6) { close(fd); return -1; }@NL@"
    + "    }@NL@"
    + "    close(fd);@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "long count_lines_mmap(const char *path) {@NL@"
    + "    if (path == NULL) return -1;@NL@"
    + "    int fd = open(path, O_RDONLY);@NL@"
    + "    if (fd < 0) return -1;@NL@"
    + "    struct stat st;@NL@"
    + "    if (fstat(fd, &st) != 0) { close(fd); return -1; }@NL@"
    + "    if (st.st_size == 0) { close(fd); return 0; }@NL@"
    + "    void *mp = mmap(NULL, (size_t)st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);@NL@"
    + "    if (mp == MAP_FAILED) { close(fd); return -1; }@NL@"
    + "    const char *p = (const char *)mp;@NL@"
    + "    long lines = 0;@NL@"
    + "    for (off_t i = 0; i < st.st_size; i++) {@NL@"
    + "        if (p[i] != 10) lines++;@NL@"
    + "    }@NL@"
    + "    munmap(mp, (size_t)st.st_size);@NL@"
    + "    close(fd);@NL@"
    + "    return lines;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
)

# ================= MODULE 22: ca-performance-tuning ==========================
M22 = "ca-performance-tuning"

L22A = "ca-layout-and-cache"
L22B = "ca-measure-first"
L22CP = "ca-checkpoint-m22"

write_module(
    M22,
    "Performance Tuning: Layout, Locality, Measurement",
    "The performance thinking that survives contact with reality: data layout decides cache behavior, and measurement decides everything else.",
    "Tinh chỉnh hiệu năng: bố cục, locality, đo đạc",
    "Tư duy hiệu năng sống sót qua tiếp xúc thực tế: bố cục dữ liệu quyết định hành vi cache, và đo đạc quyết định mọi thứ còn lại.",
    [L22A, L22B, L22CP],
    ["ca-p22-tuning"],
)

write_lesson(
    M22,
    L22A,
    "Data Layout Is Performance Policy",
    "The compiler cannot fix a data structure that drags dead bytes through the cache.",
    20,
    """
## Hot and cold

Every struct field rides along on every access. A hot loop touching `id` and `score` should not stream 60-byte name arrays through the cache:

```c
struct fat { int id; int score; char name[60]; };   /* 68 bytes, most dead in the loop */
struct hot { int id; int score; };                  /* 8 bytes: 8 records per line */
struct cold { char name[60]; };                     /* kept aside, touched rarely */
```

Splitting hot from cold (AoS-of-two-arrays or an index that links them) multiplies the records per cache line by 8. Same asymptotics, radically different constants — and constants are what you ship.

## Arrays of structures vs structures of arrays

```c
struct particle { double x, y, vx, vy, mass; };   /* AoS */
struct particle p[N];

struct soa { double *x, *y, *vx, *vy, *mass; };   /* SoA: five parallel arrays */
```

A loop that updates only velocities touches 40% of each AoS record's bytes; with SoA it streams exactly the three arrays it needs. SIMD and prefetchers love SoA. Random access by whole record loves AoS. Pick per access pattern, not per fashion.

## The 64-byte lens

Cache lines (typically 64 bytes — hardware reality, not ISO C) are the unit of memory traffic. Layout questions are all the same question: *how many of the bytes in each line do I actually need?* Padding out false sharing (module 19) and splitting hot/cold are the same lever applied at different scales.

## Honest limits

- `sizeof`/`offsetof` are ISO C and deterministic for a given target — assert on them freely.
- Which accesses are fast is target-specific. This sandbox is aarch64 with its cache geometry; a core x86 machine differs. The *method* transfers; the numbers do not.
""",
    "Bố cục dữ liệu là chính sách hiệu năng",
    "Compiler không thể cứu một cấu trúc dữ liệu kéo byte chết qua cache.",
    """
## Nóng và lạnh

Mọi trường của struct đi cùng nhau trên mọi lần truy cập. Vòng lặp nóng chạm `id` và `score` không nên kéo mảng tên 60-byte qua cache:

```c
struct fat { int id; int score; char name[60]; };   /* 68 byte, đa số chết trong vòng lặp */
struct hot { int id; int score; };                  /* 8 byte: 8 bản ghi mỗi line */
struct cold { char name[60]; };                     /* để riêng, hiếm khi chạm */
```

Tách nóng khỏi lạnh (hai mảng riêng hoặc chỉ số nối chúng) nhân số bản ghi mỗi cache line lên gấp 8. Cùng độ phức tạp tiệm cận, khác nhau căn bản về hằng số — và hằng số là thứ bạn giao hàng.

## Mảng struct vs struct mảng

```c
struct particle { double x, y, vx, vy, mass; };   /* AoS */
struct particle p[N];

struct soa { double *x, *y, *vx, *vy, *mass; };   /* SoA: năm mảng song song */
```

Vòng lặp chỉ cập nhật vận tốc chạm 40% byte của mỗi bản ghi AoS; với SoA nó chảy đúng ba mảng cần. SIMD và prefetcher yêu SoA. Truy cập ngẫu nhiên theo toàn bộ bản ghi yêu AoS. Chọn theo pattern truy cập, không theo mốt.

## Lăng kính 64 byte

Cache line (thường 64 byte — thực tế phần cứng, không phải ISO C) là đơn vị giao thông bộ nhớ. Mọi câu hỏi bố cục đều là cùng một câu hỏi: *trong mỗi line, bao nhiêu byte là thứ mình thực sự cần?* Padding chống false sharing (mô-đun 19) và tách nóng/lạnh là cùng một đòn bẩy ở các thang khác nhau.

## Giới hạn trung thực

- `sizeof`/`offsetof` là ISO C và tất định cho một target nhất định — khẳng định tự do trên chúng.
- Truy cập nào nhanh là tùy target. Sandbox này là aarch64 với hình học cache riêng; máy x86 khác. *Phương pháp* chuyển giao được; con số thì không.
""",
)

write_lesson(
    M22,
    L22B,
    "Measure First: Budgets, Sinks, and -O Levels",
    "Optimization without measurement is decoration. The tools: monotonic clocks, iteration budgets, and keeping the optimizer honest.",
    20,
    """
## The budget loop

Work backward from a time budget: if one iteration costs `p` milliseconds and you may spend `B` milliseconds, run `ceil(B / p)` iterations — and guard division by zero. Deriving the iteration count from a budget (instead of a magic constant) is what makes a benchmark stoppable *and* comparable across machines.

## Keeping the optimizer honest

```c
volatile double sink = 0.0;          /* or accumulate-and-print */
for (size_t i = 0; i < iters; i++) sink += work(i);
```

Without a consumed result, the optimizer may delete the entire loop: computing a value nobody uses is not an observable behavior (module 2). The sink (or a printed checksum) makes the work real.

## Optimization levels, honestly

- `-O0`: fast compile, slow code — the debugging mode. Variables live in memory; stepping in a debugger stays sane.
- `-O2`/`-O3`: inlining, vectorization, aggressive reordering. Code may behave observably-identically while executing completely differently.
- The gap between -O0 and -O2 on the same source is routinely large — which is why "it felt slow in debug" is not a performance claim.

ISO C defines none of this: optimization levels are compiler flags (GCC/Clang here, labeled as such). Undefined behavior plus optimization equals module 4's menagerie — measure with the flags you ship.

## The regression habit

A number without a baseline is a anecdote. Keep the benchmark in the repo, record the machine, flags, and input; compare like with like. When a change claims 20%, re-run with and without. If the delta does not reproduce, it did not happen.
""",
    "Đo trước: ngân sách, sink, và các mức -O",
    "Tối ưu hóa không đo đạc chỉ là trang trí. Công cụ: đồng hồ monotonic, ngân sách lần lặp, và giữ optimizer trung thực.",
    """
## Vòng lặp ngân sách

Làm ngược từ ngân sách thời gian: nếu một lần lặp tốn `p` mili giây và bạn được phép tiêu `B` mili giây, hãy chạy `ceil(B / p)` lần lặp — và chặn chia cho không. Suy số lần lặp từ ngân sách (thay vì hằng số thừa số) làm benchmark dừng được *và* so sánh được giữa các máy.

## Giữ optimizer trung thực

```c
volatile double sink = 0.0;          /* hoặc cộng dồn rồi in */
for (size_t i = 0; i < iters; i++) sink += work(i);
```

Không có kết quả được tiêu thụ, optimizer có thể xóa cả vòng lặp: tính một giá trị không ai dùng không phải hành vi quan sát được (mô-đun 2). Sink (hoặc checksum in ra) biến công việc thành thật.

## Các mức tối ưu, nói thẳng

- `-O0`: biên dịch nhanh, code chậm — chế độ debug. Biến sống trên bộ nhớ; bước qua debugger vẫn tỉnh táo.
- `-O2`/`-O3`: inline, vector hóa, sắp xếp lại quyết liệt. Code có thể quan sát được giống hệt mà thực thi khác hẳn.
- Khoảng cách giữa -O0 và -O2 trên cùng mã nguồn thường rất lớn — vì thế "nó cảm giác chậm trong debug" không phải một tuyên bố hiệu năng.

ISO C không định nghĩa gì trong số này: mức tối ưu là cờ compiler (GCC/Clang ở đây, ghi nhãn rõ). Hành vi không xác định cộng tối ưu hóa bằng vườn thú của mô-đun 4 — hãy đo với đúng cờ bạn giao hàng.

## Thói quen chống thoái hóa

Một con số không có đường cơ sở là giai thoại. Giữ benchmark trong repo, ghi lại máy, cờ, và đầu vào; so sánh cùng loại với cùng loại. Khi một thay đổi tự nhận 20%, chạy lại có và không có nó. Nếu độ chênh không tái hiện, nó chưa từng xảy ra.
""",
)

write_practice(
    M22,
    "ca-p22-tuning",
    "Layout and Measurement Drills",
    "Hot/cold arithmetic, blocked transpose, and budget math — deterministic verifications of the layout and measurement disciplines.",
    "Bài tập bố cục và đo đạc",
    "Số học nóng/lạnh, chuyển vị chặn, và toán ngân sách — kiểm chứng tất định cho kỷ luật bố cục và đo đạc.",
    L22A,
    26,
    "advanced",
    [
        challenge(
            "ca22-hot-cold-stride",
            "Prove the Hot/Cold Split",
            "ISO C. Given `struct fat { int id; int score; char name[60]; };` and `struct hot { int id; int score; };` (declared for you), implement `size_t records_per_line(size_t rec_size)` returning how many records of rec_size bytes fit in one 64-byte cache line (integer floor), and `int total_score_hot(const struct hot *h, size_t n)` summing scores (NULL with n>0 returns -1).",
            C_PRELUDE + "struct fat { int id; int score; char name[60]; };@NL@struct hot { int id; int score; };@NL@",
            [
                ("8 hot records per line", "CHECK_EQ(records_per_line(sizeof(struct hot)), 8);", "Two ints are 8 bytes: eight records share a line — the hot/cold win."),
                ("fat record wastes the line", "size_t per = records_per_line(sizeof(struct fat));@NL@CHECK(per < 8);", "The 68-byte struct cannot fit 8 per line — dead bytes dilute the cache."),
                ("sum with guards", "struct hot h[3] = {{1, 10}, {2, 20}, {3, 12}};@NL@CHECK_EQ(total_score_hot(h, 3), 42);@NL@CHECK_EQ(total_score_hot(NULL, 2), -1);@NL@CHECK_EQ(total_score_hot(NULL, 0), 0);", "Summing is trivial; the guards are the engineering."),
            ],
            level="guided",
        ),
        challenge(
            "ca22-blocked-transpose",
            "Blocked Transpose",
            "ISO C. Implement `void transpose_blocked(int *dst, const int *src, size_t n, size_t block)` — standard n-by-n transpose, walking the matrix in block-by-block tiles (the cache-friendly order). For every i,j: dst[j*n+i] = src[i*n+j]. block 0 must be treated as 1. Correctness is what is tested; the tiling is the lesson.",
            C_PRELUDE,
            [
                ("3x3 identity check", "int src[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};@NL@int dst[9] = {0};@NL@transpose_blocked(dst, src, 3, 2);@NL@CHECK_EQ(dst[1], 4);@NL@CHECK_EQ(dst[3], 2);@NL@CHECK_EQ(dst[5], 8);", "Transposition is dst[j*n+i] = src[i*n+j]; tiling must not change the math."),
                ("block smaller than 1 clamps", "int src2[4] = {1, 2, 3, 4};@NL@int dst2[4] = {0};@NL@transpose_blocked(dst2, src2, 2, 0);@NL@CHECK_EQ(dst2[0], 1);@NL@CHECK_EQ(dst2[1], 3);@NL@CHECK_EQ(dst2[3], 4);", "block 0 is nonsense; clamping to 1 keeps the code total."),
                ("block larger than n", "int src3[4] = {9, 8, 7, 6};@NL@int dst3[4] = {0};@NL@transpose_blocked(dst3, src3, 2, 64);@NL@CHECK_EQ(dst3[1], 7);@NL@CHECK_EQ(dst3[2], 8);", "A block bigger than the matrix degenerates to a plain transpose — and stays correct."),
            ],
            level="combination",
        ),
        challenge(
            "ca22-benchmark-budget",
            "Iteration Budget Math",
            "ISO C. Implement `size_t iters_for_budget(double budget_ms, double per_iter_ms)` — return the number of whole iterations that fit the budget, rounding up (a partially affordable iteration still runs once); return 0 when either argument is <= 0. Implement `double bench_sink(size_t iters)` that accumulates a workload into a local `volatile double sink` (sink += (double)i / 4.0 each iteration) and returns the sink — proving the work was not optimized away.",
            C_PRELUDE,
            [
                ("ceil rounding", "CHECK_EQ(iters_for_budget(10.0, 3.0), 4);@NL@CHECK_EQ(iters_for_budget(9.0, 3.0), 3);", "10/3 needs 4 iterations to cover the budget; exact division needs exactly 3."),
                ("degenerate inputs", "CHECK_EQ(iters_for_budget(0.0, 1.0), 0);@NL@CHECK_EQ(iters_for_budget(5.0, 0.0), 0);@NL@CHECK_EQ(iters_for_budget(-1.0, 1.0), 0);", "No budget or no measurable per-iteration cost means run nothing."),
                ("sink proves work happened", "double s = bench_sink(8);@NL@CHECK(s > 0.0);@NL@CHECK_EQ(iters_for_budget(100.0, 0.01) > 0, 1);", "A volatile accumulator survives dead-code elimination: the loop ran."),
            ],
            level="combination",
        ),
    ],
    {
        "ca22-hot-cold-stride": vi_challenge(
            "Chứng minh tách nóng/lạnh",
            "ISO C. Cho `struct fat { int id; int score; char name[60]; };` và `struct hot { int id; int score; };` (đã khai báo), cài `size_t records_per_line(size_t rec_size)` trả số bản ghi rec_size byte vừa trong một line 64 byte (lấy sàn), và `int total_score_hot(const struct hot *h, size_t n)` cộng dồn điểm (NULL với n>0 trả -1).",
            [
                ("8 bản ghi nóng mỗi line", "Hai int là 8 byte: tám bản ghi dùng chung một line — thắng lợi nóng/lạnh."),
                ("bản ghi béo phí line", "Struct 68 byte không thể chứa 8 mỗi line — byte chết pha loãng cache."),
                ("cộng dồn với guard", "Cộng dồn là chuyện nhỏ; guard mới là kỹ thuật."),
            ],
        ),
        "ca22-blocked-transpose": vi_challenge(
            "Chuyển vị theo khối",
            "ISO C. Cài `void transpose_blocked(int *dst, const int *src, size_t n, size_t block)` — chuyển vị n-by-n chuẩn, đi ma trận theo từng khối (thứ tự thân thiện cache). Với mọi i,j: dst[j*n+i] = src[i*n+j]. block 0 coi như 1. Tính đúng đắn là thứ được kiểm; tiling là bài học.",
            [
                ("kiểm tra 3x3", "Chuyển vị là dst[j*n+i] = src[i*n+j]; tiling không được đổi toán học."),
                ("block nhỏ hơn 1 được chặn", "block 0 vô nghĩa; chặn về 1 giữ cho code toàn phần."),
                ("block lớn hơn n", "Khối lớn hơn ma trận suy biến thành chuyển vị thường — và vẫn đúng."),
            ],
        ),
        "ca22-benchmark-budget": vi_challenge(
            "Toán ngân sách lần lặp",
            "ISO C. Cài `size_t iters_for_budget(double budget_ms, double per_iter_ms)` — trả số lần lặp nguyên vừa ngân sách, làm tròn lên (lần lặp không trọn vẫn chạy một lần); trả 0 khi đối số nào <= 0. Cài `double bench_sink(size_t iters)` cộng dồn workload vào `volatile double sink` cục bộ (sink += (double)i / 4.0 mỗi lần) và trả sink — chứng minh công việc không bị tối ưu hóa mất.",
            [
                ("làm tròn lên", "10/3 cần 4 lần lặp để phủ ngân sách; chia hết cần đúng 3."),
                ("đầu vào suy biến", "Không ngân sách hoặc không có chi phí đo được nghĩa là không chạy gì."),
                ("sink chứng minh có việc xảy ra", "Bộ cộng dồn volatile sống sót qua dead-code elimination: vòng lặp đã chạy."),
            ],
        ),
    },
    solutions=[
        (
            "ca22-hot-cold-stride",
            C_PRELUDE
            + "struct fat { int id; int score; char name[60]; };@NL@"
            + "struct hot { int id; int score; };@NL@"
            + "size_t records_per_line(size_t rec_size) {@NL@"
            + "    if (rec_size == 0) return 0;@NL@"
            + "    return 64 / rec_size;@NL@"
            + "}@NL@"
            + "int total_score_hot(const struct hot *h, size_t n) {@NL@"
            + "    if (h == NULL) return n == 0 ? 0 : -1;@NL@"
            + "    int t = 0;@NL@"
            + "    for (size_t i = 0; i < n; i++) t += h[i].score;@NL@"
            + "    return t;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "struct fat { int id; int score; char name[60]; };@NL@"
            + "struct hot { int id; int score; };@NL@"
            + "size_t records_per_line(size_t rec_size) {@NL@"
            + "    if (rec_size == 0) return 0;@NL@"
            + "    return 128 / rec_size;@NL@"
            + "}@NL@"
            + "int total_score_hot(const struct hot *h, size_t n) {@NL@"
            + "    if (h == NULL) return n == 0 ? 0 : -1;@NL@"
            + "    int t = 0;@NL@"
            + "    for (size_t i = 0; i < n; i++) t += h[i].score;@NL@"
            + "    return t;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca22-blocked-transpose",
            C_PRELUDE
            + "void transpose_blocked(int *dst, const int *src, size_t n, size_t block) {@NL@"
            + "    if (dst == NULL || src == NULL || n == 0) return;@NL@"
            + "    if (block == 0) block = 1;@NL@"
            + "    for (size_t bi = 0; bi < n; bi += block) {@NL@"
            + "        size_t iend = bi + block < n ? bi + block : n;@NL@"
            + "        for (size_t bj = 0; bj < n; bj += block) {@NL@"
            + "            size_t jend = bj + block < n ? bj + block : n;@NL@"
            + "            for (size_t i = bi; i < iend; i++) {@NL@"
            + "                for (size_t j = bj; j < jend; j++) {@NL@"
            + "                    dst[j * n + i] = src[i * n + j];@NL@"
            + "                }@NL@"
            + "            }@NL@"
            + "        }@NL@"
            + "    }@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "void transpose_blocked(int *dst, const int *src, size_t n, size_t block) {@NL@"
            + "    if (dst == NULL || src == NULL || n == 0) return;@NL@"
            + "    if (block == 0) block = 1;@NL@"
            + "    for (size_t bi = 0; bi < n; bi += block) {@NL@"
            + "        size_t iend = bi + block < n ? bi + block : n;@NL@"
            + "        for (size_t bj = 0; bj < n; bj += block) {@NL@"
            + "            size_t jend = bj + block < n ? bj + block : n;@NL@"
            + "            for (size_t i = bi; i < iend; i++) {@NL@"
            + "                for (size_t j = bj; j < jend; j++) {@NL@"
            + "                    dst[i * n + j] = src[i * n + j];@NL@"
            + "                }@NL@"
            + "            }@NL@"
            + "        }@NL@"
            + "    }@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca22-benchmark-budget",
            C_PRELUDE
            + "size_t iters_for_budget(double budget_ms, double per_iter_ms) {@NL@"
            + "    if (budget_ms <= 0.0 || per_iter_ms <= 0.0) return 0;@NL@"
            + "    double raw = budget_ms / per_iter_ms;@NL@"
            + "    size_t whole = (size_t)raw;@NL@"
            + "    if ((double)whole < raw) whole++;@NL@"
            + "    return whole;@NL@"
            + "}@NL@"
            + "double bench_sink(size_t iters) {@NL@"
            + "    volatile double sink = 0.0;@NL@"
            + "    for (size_t i = 0; i < iters; i++) {@NL@"
            + "        sink += (double)i / 4.0;@NL@"
            + "    }@NL@"
            + "    return sink;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "size_t iters_for_budget(double budget_ms, double per_iter_ms) {@NL@"
            + "    if (budget_ms <= 0.0 || per_iter_ms <= 0.0) return 0;@NL@"
            + "    double raw = budget_ms / per_iter_ms;@NL@"
            + "    return (size_t)raw;@NL@"
            + "}@NL@"
            + "double bench_sink(size_t iters) {@NL@"
            + "    volatile double sink = 0.0;@NL@"
            + "    for (size_t i = 0; i < iters; i++) {@NL@"
            + "        sink += (double)i / 4.0;@NL@"
            + "    }@NL@"
            + "    return sink;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_checkpoint(
    M22,
    L22CP,
    "Checkpoint: Layout Clinic Verdict",
    "Turn the layout lesson into a function: compute the bytes a scoring pass touches for interleaved versus split layouts.",
    18,
    "See lesson.",
    "Kiểm tra: Phán quyết phòng khám bố cục",
    "Biến bài học bố cục thành hàm: tính số byte mà một lượt chấm điểm chạm tới cho bố cục trộn lẫn so với tách riêng.",
    "Xem bài học.",
    challenge(
        "ca22-checkpoint-clinic",
        "Checkpoint: Layout Clinic Verdict",
        "ISO C. Given `struct fat { int id; int score; char name[60]; };` (declared for you), implement `size_t touched_bytes(const char *layout, size_t n)` — for layout 'interleaved' return n * sizeof(struct fat); for 'split' return n * 2 * sizeof(int) (the hot fields only: id + score, stored in their own array); any other layout (or NULL) returns (size_t)-1. n == 0 returns 0 for any valid layout.",
        C_PRELUDE + "struct fat { int id; int score; char name[60]; };@NL@",
        [
            ("interleaved pays for names", "CHECK_EQ(touched_bytes(@TL1@, 100), 100 * sizeof(struct fat));", "Every record drags its 60-byte name through the pass: n times the fat size."),
            ("split pays hot only", "CHECK_EQ(touched_bytes(@TL2@, 100), 100 * 2 * sizeof(int));", "Scores and ids live in their own arrays: 8 bytes per record, names untouched."),
            ("zero and unknown", "CHECK_EQ(touched_bytes(@TL2@, 0), 0);@NL@CHECK_EQ(touched_bytes(@T3@, 5), (size_t)-1);@NL@CHECK_EQ(touched_bytes(NULL, 5), (size_t)-1);", "Zero records touch nothing; an unknown layout is a caller bug, refused."),
        ],
        level="capstone",
    ),
    {
        "ca22-checkpoint-clinic": vi_challenge(
            "Kiểm tra: Phán quyết phòng khám bố cục",
            "ISO C. Cho `struct fat { int id; int score; char name[60]; };` (đã khai báo), cài `size_t touched_bytes(const char *layout, size_t n)` — layout 'interleaved' trả n * sizeof(struct fat); 'split' trả n * 2 * sizeof(int) (chỉ trường nóng: id + score, nằm trong mảng riêng); layout khác (hoặc NULL) trả (size_t)-1. n == 0 trả 0 với layout hợp lệ.",
            [
                ("trộn lẫn trả giá cho tên", "Mọi bản ghi kéo mảng tên 60 byte qua lượt quét: n lần cỡ béo."),
                ("tách riêng chỉ trả giá cho nóng", "Điểm và id nằm trong mảng riêng: 8 byte mỗi bản ghi, tên không bị đụng."),
                ("không và không rõ", "Không bản ghi thì không chạm gì; layout không rõ là lỗi người gọi, bị từ chối."),
            ],
        ),
    },
    solution=
    C_PRELUDE
    + "struct fat { int id; int score; char name[60]; };@NL@"
    + "size_t touched_bytes(const char *layout, size_t n) {@NL@"
    + "    if (layout == NULL) return (size_t)-1;@NL@"
    + "    if (strcmp(layout, @TL1@) == 0) return n * sizeof(struct fat);@NL@"
    + "    if (strcmp(layout, @TL2@) == 0) return n * 2 * sizeof(int);@NL@"
    + "    return (size_t)-1;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
    wrong=
    C_PRELUDE
    + "struct fat { int id; int score; char name[60]; };@NL@"
    + "size_t touched_bytes(const char *layout, size_t n) {@NL@"
    + "    if (layout == NULL) return (size_t)-1;@NL@"
    + "    if (strcmp(layout, @TL1@) == 0) return n * sizeof(struct fat);@NL@"
    + "    if (strcmp(layout, @TL2@) == 0) return n * sizeof(struct fat);@NL@"
    + "    return (size_t)-1;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
)
