#!/usr/bin/env python3
"""C Advanced — batch 9: modules 17 (posix-processes) and 18 (concurrency-deep).
Zero-backslash authoring: @NL@ = statement separator, @CE@ = newline escape
inside C string literals. POSIX challenges define _POSIX_C_SOURCE first in
boilerplate and solutions (verified musl behavior in this sandbox).
Concurrency W-mutants are deterministic (no race-dependent verdicts)."""
from ca import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# POSIX feature macro + include set; prepended to POSIX boilerplate/solutions.
# Verified in-sandbox: macro-first, then unistd/wait/signal, compiles clean
# under -std=c23 with the harness's ISO-only prelude in front of it.
POSIX = (
    "#define _POSIX_C_SOURCE 200809L@NL@"
    "#include <unistd.h>@NL@"
    "#include <sys/wait.h>@NL@"
    "#include <fcntl.h>@NL@"
    "#include <signal.h>@NL@"
    "#include <string.h>@NL@"
    "#include <errno.h>@NL@"
)
PTH = "#define _POSIX_C_SOURCE 200809L@NL@#include <pthread.h>@NL@#include <stdint.h>@NL@"

# Given: child exits with the given code; returns the raw waitpid status word.
GIVEN_EXIT = (
    "static int run_exit_status(int code) {@NL@"
    "    pid_t p = fork();@NL@"
    "    if (p < 0) return -1;@NL@"
    "    if (p == 0) _exit(code);@NL@"
    "    int st = 0;@NL@"
    "    if (waitpid(p, &st, 0) < 0) return -1;@NL@"
    "    return st;@NL@"
    "}@NL@"
)

# Given: run a command with output discarded; returns its exit code (or -1).
GIVEN_CAPTURE = (
    "static int run_capture(const char *cmd) {@NL@"
    "    pid_t p = fork();@NL@"
    "    if (p < 0) return -1;@NL@"
    "    if (p == 0) {@NL@"
    "        int dn = open(@FDNULL@, O_WRONLY);@NL@"
    "        if (dn >= 0) { dup2(dn, STDOUT_FILENO); dup2(dn, STDERR_FILENO); }@NL@"
    "        execl(@FDSH@, @FDsh@, @FDdashc@, cmd, (char *)NULL);@NL@"
    "        _exit(127);@NL@"
    "    }@NL@"
    "    int st = 0;@NL@"
    "    if (waitpid(p, &st, 0) < 0) return -1;@NL@"
    "    if (!WIFEXITED(st)) return -1;@NL@"
    "    return WEXITSTATUS(st);@NL@"
    "}@NL@"
)

# String-literal carriers for GIVEN_CAPTURE (no escapes needed in C source).
SLASHDEVNULL = "/dev/null"
SLASHBINSH = "/bin/sh"
SHARG = "sh"
DASHC = "-c"


def fill_given():
    g = GIVEN_CAPTURE
    Q = chr(34)
    g = g.replace("@FDNULL@", Q + SLASHDEVNULL + Q)
    g = g.replace("@FDSH@", Q + SLASHBINSH + Q)
    g = g.replace("@FDsh@", Q + SHARG + Q)
    g = g.replace("@FDdashc@", Q + DASHC + Q)
    return g


# ================= MODULE 17: ca-posix-processes =============================
M17 = "ca-posix-processes"

L17A = "ca-process-basics"
L17B = "ca-pipes-signals"
L17CP = "ca-checkpoint-m17"

write_module(
    M17,
    "POSIX Processes: fork, exec, wait",
    "Everything above ISO C is labeled as such: fork/exec/wait are POSIX. This module builds the process machinery every shell and server relies on — with the real calls, in the real sandbox.",
    "Tiến trình POSIX: fork, exec, wait",
    "Mọi thứ trên ISO C đều được ghi nhãn: fork/exec/wait là POSIX. Mô-đun này xây cơ chế tiến trình mà mọi shell và server dựa vào — với các lệnh gọi thật, trong sandbox thật.",
    [L17A, L17B, L17CP],
    ["ca-p17-processes"],
)

write_lesson(
    M17,
    L17A,
    "fork, exec, wait — The Process Triple",
    "POSIX, not ISO C: how a process clones itself, replaces itself, and how the parent collects the result.",
    18,
    """
## One call that returns twice

`fork()` (POSIX) duplicates the calling process. It returns once *per process*: 0 in the child, the child's pid in the parent. Everything else — memory, open files, cwd — is copied or shared copy-on-write. The child usually immediately calls one of the `exec*()` functions, which *replaces* the process image with a new program; a successful exec never returns.

## Collecting the result

The parent reaps the child with `waitpid(pid, &status, 0)`. The `status` word is *not* the exit code — it is a bitfield decoded by macros:

- `WIFEXITED(status)` — did the child exit normally?
- `WEXITSTATUS(status)` — the low 8 bits the child passed to `exit()`, `_exit()`, or return.

Two consequences to internalize:

1. **Exit codes are 8 bits.** `_exit(256)` is observed as 0; `_exit(-1)` as 255. Never encode data beyond 0–255 in an exit code.
2. **Killed children did not exit.** If a signal terminated the child, `WIFEXITED` is false and `WEXITSTATUS` is meaningless — check `WIFSIGNALED` and `WTERMSIG`.

Every command-line tool you have ever chained with `&&` was orchestrating exactly this triple.

## POSIX vs ISO C, again

Nothing in this lesson exists in ISO C. `fork`, `exec`, `waitpid`, `_exit` are POSIX. Portable ISO-only programs cannot create processes — and that limitation is itself part of C's story: the standard library stops at `system()` (which *returns an implementation-defined status*), and everything richer is platform work.
""",
    "fork, exec, wait — bộ ba tiến trình",
    "POSIX, không phải ISO C: tiến trình sao chép chính nó, thay thế chính nó, và cha thu kết quả thế nào.",
    """
## Một lệnh gọi trả về hai lần

`fork()` (POSIX) nhân đôi tiến trình đang gọi. Nó trả về một lần *trên mỗi tiến trình*: 0 ở con, pid của con ở cha. Mọi thứ khác — bộ nhớ, file mở, cwd — được sao chép hoặc chia sẻ copy-on-write. Con thường gọi ngay một hàm `exec*()`, hàm *thay thế* ảnh tiến trình bằng chương trình mới; exec thành công không bao giờ trả về.

## Thu kết quả

Cha reap con bằng `waitpid(pid, &status, 0)`. Từ `status` *không phải* mã exit — nó là bitfield giải mã bằng macro:

- `WIFEXITED(status)` — con có kết thúc bình thường không?
- `WEXITSTATUS(status)` — 8 bit thấp mà con truyền cho `exit()`, `_exit()`, hoặc return.

Hai hệ quả cần thấm:

1. **Mã exit chỉ 8 bit.** `_exit(256)` được thấy là 0; `_exit(-1)` là 255. Đừng bao giờ mã hóa dữ liệu ngoài 0–255 vào mã exit.
2. **Con bị tín hiệu giết thì không 'exit'.** Nếu tín hiệu kết thúc con, `WIFEXITED` sai và `WEXITSTATUS` vô nghĩa — kiểm tra `WIFSIGNALED` và `WTERMSIG`.

Mọi công cụ dòng lệnh bạn từng nối bằng `&&` đều đang điều phối đúng bộ ba này.

## POSIX so với ISO C, lần nữa

Không gì trong bài này tồn tại trong ISO C. `fork`, `exec`, `waitpid`, `_exit` là POSIX. Chương trình chỉ-ISO di động không thể tạo tiến trình — và giới hạn đó là một phần câu chuyện của C: thư viện chuẩn dừng ở `system()` (trả trạng thái do hiện thực định nghĩa), mọi thứ giàu hơn là công việc nền tảng.
""",
)

write_lesson(
    M17,
    L17B,
    "Pipes, Signals, and the Environment Boundary",
    "POSIX IPC in miniature: one-way pipes between parent and child, signal handlers that set flags, and env vars as inherited process state.",
    17,
    """
## A pipe is a pair of fds

`pipe(int fds[2])` (POSIX) gives a one-way channel: write to `fds[1]`, read from `fds[0]`. The classic pattern:

1. `pipe()` *before* `fork()` — both processes inherit both ends.
2. Child: `dup2(fds[1], STDOUT_FILENO)`, exec — its stdout flows into the pipe.
3. Parent: close the write end (else `read` never returns 0), read until EOF, then `waitpid`.

Forgetting the parent-side close is the classic bug: the reader blocks forever because a write end is still open somewhere.

## Signals: the async flag discipline

A handler runs between arbitrary two instructions of your program. The contract: the handler touches only `volatile sig_atomic_t` flags and the async-signal-safe functions. Everything else — allocation, stdio, locks — is off-limits. The production shape is always the same:

```c
static volatile sig_atomic_t shutdown_requested = 0;
static void on_term(int sig) { (void)sig; shutdown_requested = 1; }
/* main loop: while (!shutdown_requested) { ... } */
```

## The environment is inherited state

`getenv` (ISO C) reads the process environment each child inherits from its parent. That is the whole mechanism behind `PATH`, `HOME`, and every 12-factor app config: environment is *per-process state, copied at fork and passed through exec*.
""",
    "Pipe, tín hiệu, và ranh giới môi trường",
    "IPC POSIX trong hình nhỏ: pipe một chiều giữa cha và con, handler tín hiệu chỉ đặt cờ, và biến môi trường là trạng thái tiến trình được thừa kế.",
    """
## Pipe là một cặp fd

`pipe(int fds[2])` (POSIX) tạo kênh một chiều: ghi vào `fds[1]`, đọc từ `fds[0]`. Mẫu kinh điển:

1. `pipe()` *trước* `fork()` — cả hai tiến trình thừa kế cả hai đầu.
2. Con: `dup2(fds[1], STDOUT_FILENO)`, exec — stdout của nó chảy vào pipe.
3. Cha: đóng đầu ghi (nếu không `read` không bao giờ trả 0), đọc đến EOF, rồi `waitpid`.

Quên đóng phía cha là bug kinh điển: reader chặn vĩnh viễn vì còn một đầu ghi mở đâu đó.

## Tín hiệu: kỷ luật cờ bất đồng bộ

Handler chạy giữa hai lệnh tùy ý của chương trình. Hợp đồng: handler chỉ đụng cờ `volatile sig_atomic_t` và các hàm async-signal-safe. Mọi thứ khác — cấp phát, stdio, khóa — bị cấm. Hình dạng production luôn như sau:

```c
static volatile sig_atomic_t shutdown_requested = 0;
static void on_term(int sig) { (void)sig; shutdown_requested = 1; }
/* vòng lặp chính: while (!shutdown_requested) { ... } */
```

## Môi trường là trạng thái được thừa kế

`getenv` (ISO C) đọc môi trường tiến trình mà mỗi con thừa kế từ cha. Đó là toàn bộ cơ chế đằng sau `PATH`, `HOME`, và mọi cấu hình 12-factor: môi trường là *trạng thái theo tiến trình, sao chép lúc fork và truyền qua exec*.
""",
)

write_practice(
    M17,
    "ca-p17-processes",
    "Process Machinery Drills",
    "fork/exec/wait status decoding, pipe capture, signal flags, and the environment boundary — all executable in the sandbox.",
    "Bài tập cơ chế tiến trình",
    "Giải mã trạng thái fork/exec/wait, thu dữ liệu qua pipe, cờ tín hiệu, và ranh giới môi trường — tất cả chạy được trong sandbox.",
    L17A,
    22,
    "advanced",
    [
        challenge(
            "ca17-exit-status-decode",
            "Decode the Exit Status",
            "POSIX. `run_exit_status(code)` (given) forks a child that exits with `code` and returns the raw waitpid status word. Implement `int decode_exit(int status)` returning the child's exit code if it exited normally, or -1 if it did not exit normally. Remember: exit codes are the low 8 bits.",
            C_PRELUDE + POSIX + GIVEN_EXIT,
            [
                ("normal exit", "CHECK_EQ(decode_exit(run_exit_status(7)), 7);", "WIFEXITED holds and WEXITSTATUS extracts the low byte: 7."),
                ("zero exit", "CHECK_EQ(decode_exit(run_exit_status(0)), 0);", "Success is exit code 0 — the exact value every script tests."),
                ("truncation to 8 bits", "CHECK_EQ(decode_exit(run_exit_status(256)), 0);", "_exit(256) keeps only the low 8 bits: 256 = 0x100, low byte 0."),
            ],
            level="guided",
        ),
        challenge(
            "ca17-pipe-echo-capture",
            "Capture Child Output Through a Pipe",
            "POSIX. Implement `int capture_child(const char *cmd, char *out, size_t cap)` — fork, redirect the child's stdout into a pipe created before the fork, exec `/bin/sh -c cmd`, read until EOF into out (at most cap-1 bytes, NUL-terminate), waitpid, and return the child's exit code (or -1 on any setup failure).",
            C_PRELUDE + POSIX,
            [
                ("captures stdout", "char buf[64] = {0};@NL@CHECK_EQ(capture_child(@T1@, buf, 64), 0);@NL@CHECK(strstr(buf, @T2@) != NULL);", "Pipe before fork, dup2 in the child, read to EOF in the parent: the child's stdout lands in buf."),
                ("propagates exit code", "char buf2[64] = {0};@NL@CHECK_EQ(capture_child(@T3@, buf2, 64), 3);", "The shell exits 3; waitpid + WEXITSTATUS report it."),
                ("empty output on silent child", "char buf3[16] = {0};@NL@CHECK_EQ(capture_child(@T4@, buf3, 16), 0);@NL@CHECK_EQ((int)strlen(buf3), 0);", "A child that writes nothing yields an empty, terminated buffer."),
            ],
            level="combination",
        ),
        challenge(
            "ca17-signal-clinic",
            "Count Signal Deliveries",
            "POSIX. A handler (given) increments a `volatile sig_atomic_t` counter for SIGUSR1. Implement `int install_usr1_handler(void)` — install it with sigaction, return 0 on success and -1 on failure — and `int usr1_count(void)` returning the counter. Handler-touches-flags-only is the whole discipline.",
            C_PRELUDE + POSIX
            + "static volatile sig_atomic_t g_usr1 = 0;@NL@"
            + "static void on_usr1(int sig) { (void)sig; g_usr1++; }@NL@",
            [
                ("install succeeds", "CHECK_EQ(install_usr1_handler(), 0);", "sigaction with a handler for SIGUSR1 returns 0."),
                ("delivery counted", "CHECK_EQ(install_usr1_handler(), 0);@NL@raise(SIGUSR1);@NL@CHECK_EQ(usr1_count(), 1);", "raise sends the signal to the calling process; the handler bumps the sig_atomic_t flag."),
                ("three deliveries", "CHECK_EQ(install_usr1_handler(), 0);@NL@raise(SIGUSR1);@NL@raise(SIGUSR1);@NL@raise(SIGUSR1);@NL@CHECK_EQ(usr1_count(), 3);", "Each raise is one synchronous delivery; the counter sees all three."),
            ],
            level="imitation",
        ),
        challenge(
            "ca17-env-boundary",
            "Environment or Default?",
            "Implement `const char *env_or_default(const char *name, const char *dflt)` — return the environment value if `name` is set (getenv, ISO C), otherwise return dflt. NULL name or NULL dflt returns NULL. This is the inherited-state boundary every 12-factor program leans on.",
            C_PRELUDE,
            [
                ("unset variable falls back", "CHECK_STR_EQ(env_or_default(@T5@, @T6@), @T6@);", "No such environment variable exists in the sandbox: the default is returned."),
                ("PATH is inherited", "CHECK(env_or_default(@T7@, @T8@) != NULL);", "The sandbox process environment carries PATH — the value survives fork/exec into your test process."),
                ("NULL guards", "CHECK(env_or_default(NULL, @T9@) == NULL);@NL@CHECK(env_or_default(@T10@, NULL) == NULL);", "Refuse to guess when the contract is incomplete."),
            ],
            level="imitation",
        ),
    ],
    {
        "ca17-exit-status-decode": vi_challenge(
            "Giải mã trạng thái exit",
            "run_exit_status (cho sẵn) fork con exit với mã và trả từ trạng thái thô. Cài decode_exit: trả mã exit nếu con kết thúc bình thường, hoặc -1 nếu không.",
            [
                ("exit bình thường", "WIFEXITED đúng và WEXITSTATUS rút byte thấp: 7."),
                ("exit 0", "Thành công là mã exit 0 — giá trị mọi script kiểm tra."),
                ("cắt xuống 8 bit", "_exit(256) chỉ giữ 8 bit thấp: 256 = 0x100, byte thấp 0."),
            ],
        ),
        "ca17-pipe-echo-capture": vi_challenge(
            "Thu output con qua pipe",
            "Cài capture_child: fork, chuyển stdout con vào pipe tạo trước fork, exec /bin/sh -c cmd, đọc đến EOF (tối đa cap-1 byte, kết thúc NUL), waitpid, trả mã exit.",
            [
                ("thu được stdout", "Pipe trước fork, dup2 ở con, đọc đến EOF ở cha: stdout con nằm trong buf."),
                ("truyền mã exit", "Shell exit 3; waitpid + WEXITSTATUS báo lại."),
                ("output rỗng", "Con không ghi gì cho buffer rỗng, có NUL kết thúc."),
            ],
        ),
        "ca17-signal-clinic": vi_challenge(
            "Đếm lần phát tín hiệu",
            "Handler (cho sẵn) tăng cờ sig_atomic_t cho SIGUSR1. Cài install_usr1_handler (sigaction, trả 0/-1) và usr1_count.",
            [
                ("cài thành công", "sigaction với handler cho SIGUSR1 trả 0."),
                ("bị đếm", "raise gửi tín hiệu tới tiến trình gọi; handler tăng cờ sig_atomic_t."),
                ("ba lần phát", "Mỗi raise là một lần phát đồng bộ; bộ đếm thấy cả ba."),
            ],
        ),
        "ca17-env-boundary": vi_challenge(
            "Môi trường hoặc mặc định",
            "Cài env_or_default: trả giá trị môi trường nếu name được đặt (getenv), nếu không trả dflt. NULL tên hoặc NULL dflt trả NULL.",
            [
                ("biến chưa đặt về mặc định", "Không có biến môi trường này trong sandbox: trả mặc định."),
                ("PATH được thừa kế", "Môi trường tiến trình sandbox mang PATH — giá trị sống sót qua fork/exec."),
                ("chặn NULL", "Từ chối đoán khi hợp đồng thiếu."),
            ],
        ),
    },
    solutions=[
        (
            "ca17-exit-status-decode",
            C_PRELUDE + POSIX + GIVEN_EXIT
            + "int decode_exit(int status) {@NL@"
            + "    if (WIFEXITED(status)) return WEXITSTATUS(status);@NL@"
            + "    return -1;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + POSIX + GIVEN_EXIT
            + "int decode_exit(int status) {@NL@"
            + "    (void)status;@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca17-pipe-echo-capture",
            C_PRELUDE + POSIX
            + "int capture_child(const char *cmd, char *out, size_t cap) {@NL@"
            + "    if (cmd == NULL || out == NULL || cap == 0) return -1;@NL@"
            + "    int fds[2];@NL@"
            + "    if (pipe(fds) != 0) return -1;@NL@"
            + "    pid_t p = fork();@NL@"
            + "    if (p < 0) { close(fds[0]); close(fds[1]); return -1; }@NL@"
            + "    if (p == 0) {@NL@"
            + "        close(fds[0]);@NL@"
            + "        dup2(fds[1], STDOUT_FILENO);@NL@"
            + "        close(fds[1]);@NL@"
            + "        execl(@FDSH@, @FDsh@, @FDdashc@, cmd, (char *)NULL);@NL@"
            + "        _exit(127);@NL@"
            + "    }@NL@"
            + "    close(fds[1]);@NL@"
            + "    size_t got = 0;@NL@"
            + "    for (;;) {@NL@"
            + "        char chunk[64];@NL@"
            + "        ssize_t n = read(fds[0], chunk, sizeof chunk);@NL@"
            + "        if (n <= 0) break;@NL@"
            + "        for (ssize_t i = 0; i < n && got + 1 < cap; i++) out[got++] = chunk[i];@NL@"
            + "        if (got + 1 >= cap) break;@NL@"
            + "    }@NL@"
            + "    out[got] = 0;@NL@"
            + "    close(fds[0]);@NL@"
            + "    int st = 0;@NL@"
            + "    waitpid(p, &st, 0);@NL@"
            + "    if (!WIFEXITED(st)) return -1;@NL@"
            + "    return WEXITSTATUS(st);@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + POSIX
            + "int capture_child(const char *cmd, char *out, size_t cap) {@NL@"
            + "    (void)cmd;@NL@"
            + "    if (out != NULL && cap > 0) out[0] = 0;@NL@"
            + "    return -1;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca17-signal-clinic",
            C_PRELUDE + POSIX
            + "static volatile sig_atomic_t g_usr1 = 0;@NL@"
            + "static void on_usr1(int sig) { (void)sig; g_usr1++; }@NL@"
            + "int install_usr1_handler(void) {@NL@"
            + "    struct sigaction sa;@NL@"
            + "    memset(&sa, 0, sizeof sa);@NL@"
            + "    sa.sa_handler = on_usr1;@NL@"
            + "    if (sigaction(SIGUSR1, &sa, NULL) != 0) return -1;@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int usr1_count(void) { return (int)g_usr1; }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + POSIX
            + "static volatile sig_atomic_t g_usr1 = 0;@NL@"
            + "static void on_usr1(int sig) { (void)sig; g_usr1++; }@NL@"
            + "int install_usr1_handler(void) {@NL@"
            + "    struct sigaction sa;@NL@"
            + "    memset(&sa, 0, sizeof sa);@NL@"
            + "    sa.sa_handler = on_usr1;@NL@"
            + "    if (sigaction(SIGUSR2, &sa, NULL) != 0) return -1;@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int usr1_count(void) { return (int)g_usr1; }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca17-env-boundary",
            C_PRELUDE
            + "const char *env_or_default(const char *name, const char *dflt) {@NL@"
            + "    if (name == NULL || dflt == NULL) return NULL;@NL@"
            + "    const char *v = getenv(name);@NL@"
            + "    return (v != NULL) ? v : dflt;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "const char *env_or_default(const char *name, const char *dflt) {@NL@"
            + "    if (name == NULL || dflt == NULL) return NULL;@NL@"
            + "    return name;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

# Checkpoint M17: job runner over the module's machinery.
write_checkpoint(
    M17,
    L17CP,
    "Checkpoint: Job Runner",
    "One program over the module's machinery: run a sequence of shell commands through a given runner, record every exit code, and count the failures.",
    16,
    "See lesson.",
    "Kiểm tra: Bộ chạy công việc",
    "Một chương trình trên cơ chế của mô-đun: chạy chuỗi lệnh shell qua bộ chạy cho sẵn, ghi mọi mã exit, và đếm số thất bại.",
    "Xem bài học.",
    challenge(
        "ca17-checkpoint-jobs",
        "Checkpoint: Job Runner",
        "One program over the module's machinery. Given `run_capture(cmd)` (runs `/bin/sh -c cmd`, discards output, returns the exit code). Implement `size_t run_sequence(const char *const *cmds, size_t n, int *codes)` — run each command in order, store its exit code in codes[i], and return the number of failing commands (nonzero exit). NULL cmds with n>0 returns (size_t)-1 without touching codes.",
        C_PRELUDE + POSIX + fill_given(),
        [
            ("all succeed", "const char *c1[2] = {@J1@, @J2@};@NL@int code1[2] = {-9, -9};@NL@CHECK_EQ((int)run_sequence(c1, 2, code1), 0);@NL@CHECK_EQ(code1[0], 0);@NL@CHECK_EQ(code1[1], 0);", "Two successful commands: zero failures and both codes recorded as 0."),
            ("one of three fails", "const char *c2[3] = {@J1@, @J3@, @J1@};@NL@int code2[3] = {-9, -9, -9};@NL@CHECK_EQ((int)run_sequence(c2, 3, code2), 1);@NL@CHECK_EQ(code2[1], 5);", "Only the middle command fails; its code is kept and the failure is counted once."),
            ("NULL guard", "int code3[1] = {-9};@NL@CHECK_EQ((int)run_sequence(NULL, 1, code3), -1);", "A NULL command list with nonzero n is a caller-contract violation: refuse without touching codes."),
        ],
        level="capstone",
    ),
    {
        "ca17-checkpoint-jobs": vi_challenge(
            "Kiểm tra: Bộ chạy công việc",
            "Cho run_capture (chạy /bin/sh -c, bỏ output, trả mã exit). Cài run_sequence: chạy từng lệnh theo thứ tự, ghi mã vào codes[i], trả số lệnh thất bại. NULL cmds với n>0 trả (size_t)-1.",
            [
                ("tất cả thành công", "Không thất bại nào và cả hai mã được ghi là 0."),
                ("một trong ba thất bại", "Chỉ lệnh giữa thất bại; mã của nó được giữ và thất bại được đếm một lần."),
                ("chặn NULL", "Danh sách lệnh NULL với n>0 là vi phạm hợp đồng: từ chối, không đụng codes."),
            ],
        ),
    },
    solution=
            C_PRELUDE + POSIX + fill_given()
            + "size_t run_sequence(const char *const *cmds, size_t n, int *codes) {@NL@"
            + "    if (cmds == NULL && n > 0) return (size_t)-1;@NL@"
            + "    size_t failures = 0;@NL@"
            + "    for (size_t i = 0; i < n; i++) {@NL@"
            + "        int rc = run_capture(cmds[i]);@NL@"
            + "        if (codes != NULL) codes[i] = rc;@NL@"
            + "        if (rc != 0) failures++;@NL@"
            + "    }@NL@"
            + "    return failures;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
    wrong=
            C_PRELUDE + POSIX + fill_given()
            + "size_t run_sequence(const char *const *cmds, size_t n, int *codes) {@NL@"
            + "    if (cmds == NULL && n > 0) return (size_t)-1;@NL@"
            + "    size_t failures = 0;@NL@"
            + "    for (size_t i = 0; i < n; i++) {@NL@"
            + "        int rc = run_capture(cmds[i]);@NL@"
            + "        if (codes != NULL) codes[i] = rc;@NL@"
            + "        if (rc == 0) failures++;@NL@"
            + "    }@NL@"
            + "    return failures;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
)

# ================= MODULE 18: ca-concurrency-deep ============================
M18 = "ca-concurrency-deep"

L18A = "ca-locks-and-cost"
L18B = "ca-deadlock-clinic"
L18CP = "ca-checkpoint-m18"

write_module(
    M18,
    "Concurrency Deep: Locks, Conditions, Barriers",
    "Beyond the beginner mutex: readers/writer locks, condition variables with spurious wakeups, barriers, and the lock-order rule that prevents deadlock. pthreads is POSIX, not ISO C — labeled as such throughout.",
    "Đồng thời nâng cao: khóa, điều kiện, rào chắn",
    "Vượt ngoài mutex của người mới: khóa đọc/ghi, biến điều kiện với wakeup spurious, rào chắn, và quy tắc thứ-tự-khóa chống deadlock. pthreads là POSIX, không phải ISO C — ghi nhãn xuyên suốt.",
    [L18A, L18B, L18CP],
    ["ca-p18-sync"],
)

write_lesson(
    M18,
    L18A,
    "Mutexes, rwlocks, condvars — and what each one costs",
    "Choosing a synchronization primitive is an engineering decision: correctness first, then contention, then complexity.",
    18,
    """
## The three primitives

- **Mutex** — one holder at a time. The default choice. Cheap when uncontended (musl: a single CAS in the fast path), expensive under contention.
- **Reader/writer lock** — many readers OR one writer. Wins only when reads vastly outnumber writes *and* the critical section is long enough to matter; otherwise its bookkeeping loses to a plain mutex.
- **Condition variable** — lets a thread sleep until state changes. Always paired with a mutex, always waited on in a loop:

```c
pthread_mutex_lock(&mtx);
while (!ready) {                       /* while, not if */
    pthread_cond_wait(&cv, &mtx);
}
pthread_mutex_unlock(&mtx);
```

The `while` is not style: `pthread_cond_wait` may return without anyone signaling (a *spurious wakeup* is allowed by POSIX), and another thread may consume the condition between signal and wake. The loop re-checks the predicate under the lock.

## Barriers

`pthread_barrier_wait` lets N threads meet at a phase boundary; exactly one caller receives `PTHREAD_BARRIER_SERIAL_THREAD`. Phases are how parallel algorithms express "nobody proceeds until everyone arrived".

## What they cost

Every lock serializes *something*. The discipline this module drills: keep critical sections small, hold locks across no I/O, and measure contention before reaching for anything fancier.
""",
    "Mutex, rwlock, condvar — và cái giá của từng cái",
    "Chọn nguyên thủy đồng bộ là quyết định kỹ thuật: đúng đắn trước, contention sau, độ phức tạp cuối.",
    """
## Ba nguyên thủy

- **Mutex** — một người giữ tại một thời điểm. Lựa chọn mặc định. Rẻ khi không tranh chấp (musl: một CAS trong fast path), đắt dưới contention.
- **Khóa đọc/ghi** — nhiều reader HOẶC một writer. Chỉ thắng khi đọc áp đảo ghi *và* vùng tới hạn đủ dài để đáng kể; nếu không, sổ sách của nó thua mutex thường.
- **Biến điều kiện** — cho thread ngủ đến khi trạng thái đổi. Luôn đi cặp với mutex, luôn chờ trong vòng lặp:

```c
pthread_mutex_lock(&mtx);
while (!ready) {                       /* while, không phải if */
    pthread_cond_wait(&cv, &mtx);
}
pthread_mutex_unlock(&mtx);
```

`while` không phải phong cách: `pthread_cond_wait` có thể trả về mà không ai signal (*spurious wakeup* được POSIX cho phép), và thread khác có thể tiêu thụ điều kiện giữa signal và thức dậy. Vòng lặp kiểm tra lại vị từ dưới khóa.

## Rào chắn

`pthread_barrier_wait` cho N thread gặp nhau tại biên pha; đúng một caller nhận `PTHREAD_BARRIER_SERIAL_THREAD`. Pha là cách thuật toán song song nói 'không ai đi tiếp đến khi mọi người đã đến'.

## Cái giá của chúng

Mọi khóa serialize *một cái gì đó*. Kỷ luật mô-đun này rèn: giữ vùng tới hạn nhỏ, không giữ khóa qua I/O, và đo contention trước khi đua đòi thứ gì phức tạp hơn.
""",
)

write_lesson(
    M18,
    L18B,
    "Deadlock and the Lock-Order Rule",
    "Four conditions produce deadlock; break any one. In practice you break circular wait — with a global lock order.",
    16,
    """
## The four conditions

Deadlock requires ALL of: mutual exclusion, hold-and-wait, no preemption, and **circular wait**. You rarely get to change the first three. The one you control is circular wait.

## The lock-order rule

If every thread acquires the same mutexes in the same global order (say, always A before B), no cycle can form — the holder of B never waits for A while someone holds A and waits for B, because nobody acquires B first. Enforce it by convention and by review: the classic production deadlock is two new features acquiring the same two locks in opposite orders.

Escape hatches when order is genuinely hard:

- `pthread_mutex_trylock` on the second lock; if it fails, release and retry — converts deadlock into livelock-or-progress, and livelock is at least diagnosable.
- Lock hierarchies with `assert`-able levels, checked in debug builds.

## The clinic mindset

Diagnosis questions, in order: Which two threads? Which two locks? Who holds what while waiting for what? If you cannot fill in that grid, you do not have a deadlock diagnosis — you have a deadlock suspicion.
""",
    "Deadlock và quy tắc thứ tự khóa",
    "Bốn điều kiện tạo deadlock; phá một cái là đủ. Thực tế bạn phá circular wait — bằng thứ tự khóa toàn cục.",
    """
## Bốn điều kiện

Deadlock cần ĐỦ: loại trừ tương hỗ, hold-and-wait, không chiếm đoạt, và **circular wait**. Bạn hiếm khi đổi được ba cái đầu. Cái bạn kiểm soát là circular wait.

## Quy tắc thứ tự khóa

Nếu mọi thread lấy các mutex theo cùng thứ tự toàn cục (luôn A trước B), không thể tạo chu trình — người giữ B không bao giờ chờ A trong khi người khác giữ A và chờ B, vì không ai lấy B trước. Thi hành bằng quy ước và review: deadlock production kinh điển là hai tính năng mới lấy cùng hai khóa theo hai thứ tự ngược nhau.

Lối thoát khi thứ tự khó:

- `pthread_mutex_trylock` trên khóa thứ hai; nếu thất bại, nhả và thử lại — biến deadlock thành livelock-hoặc-tiến-trình, và livelock ít nhất còn chẩn đoán được.
- Phân cấp khóa với mức assert-able, kiểm tra trong build debug.

## Tư duy phòng khám

Câu hỏi chẩn đoán, theo thứ tự: Hai thread nào? Hai khóa nào? Ai giữ gì trong khi chờ gì? Nếu không điền được bảng đó, bạn chưa có chẩn đoán deadlock — bạn mới chỉ có nghi ngờ deadlock.
""",
)

write_practice(
    M18,
    "ca-p18-sync",
    "Synchronization Drills",
    "Mutexed accounts, condvar queues, rwlock metrics, lock-order diagnosis, and a deterministic pool core.",
    "Bài tập đồng bộ",
    "Tài khoản có mutex, hàng đợi condvar, chỉ số rwlock, chẩn đoán thứ tự khóa, và lõi pool tất định.",
    L18A,
    22,
    "advanced",
    [
        challenge(
            "ca18-mutex-counter",
            "The Contended Account",
            "Given a mutex and a global `long long account` (both in your editor). Implement `void deposit(long long amount)` — add amount to account under the mutex — and `long long balance(void)` returning it. The grader hammers it from many threads; a lost update means a lost test.",
            C_PRELUDE + PTH
            + "static pthread_mutex_t cnt_mtx = PTHREAD_MUTEX_INITIALIZER;@NL@"
            + "static long long account = 0;@NL@"
            + "void deposit(long long);@NL@"
            + "static void *dep_worker(void *arg) { deposit((long long)(intptr_t)arg); return NULL; }@NL@"
            + "static long long concurrent_deposits(int nthreads, long long each) {@NL@"
            + "    pthread_t th[8];@NL@"
            + "    if (nthreads > 8) nthreads = 8;@NL@"
            + "    for (int i = 0; i < nthreads; i++) {@NL@"
            + "        if (pthread_create(&th[i], NULL, dep_worker, (void *)(intptr_t)each) != 0) return -1;@NL@"
            + "    }@NL@"
            + "    for (int i = 0; i < nthreads; i++) pthread_join(th[i], NULL);@NL@"
            + "    return 0;@NL@"
            + "}@NL@",
            [
                ("single-thread deposit", "deposit(250);@NL@CHECK_EQ(balance(), 250);", "One deposit, one update: the account reflects it exactly."),
                ("four threads hammer it", "CHECK_EQ(concurrent_deposits(4, 500), 0);@NL@CHECK_EQ(balance(), 2000);", "concurrent_deposits (given) spawns 4 threads depositing 500 each; the mutex makes every update land: exactly 2000."),
                ("balance is read-only", "deposit(7);@NL@long long b1 = balance();@NL@long long b2 = balance();@NL@CHECK_EQ(b1, b2);", "Observing the balance must not change it."),
            ],
            level="guided",
        ),
        challenge(
            "ca18-condvar-queue",
            "Bounded FIFO Queue",
            "Given: mutex, condvar, `int slots[8]`, head/tail/count. Implement `int qpush(int v)` (append FIFO; -1 when full) and `int qpop(void)` (remove oldest; -1 when empty). Push/pop must maintain the mutex and the invariant count equals live elements.",
            C_PRELUDE + PTH
            + "static pthread_mutex_t q_mtx = PTHREAD_MUTEX_INITIALIZER;@NL@"
            + "static pthread_cond_t q_cv = PTHREAD_COND_INITIALIZER;@NL@"
            + "static int slots[8];@NL@static size_t q_head = 0;@NL@"
            + "static size_t q_tail = 0;@NL@static size_t q_count = 0;@NL@",
            [
                ("FIFO order", "CHECK_EQ(qpush(1), 0);@NL@CHECK_EQ(qpush(2), 0);@NL@CHECK_EQ(qpush(3), 0);@NL@CHECK_EQ(qpop(), 1);@NL@CHECK_EQ(qpop(), 2);@NL@CHECK_EQ(qpop(), 3);", "Oldest in, first out: the queue is a ring, not a stack."),
                ("empty pop refused", "CHECK_EQ(qpop(), -1);", "Popping an empty queue is refused, not garbage."),
                ("fill then refuse, drain then refuse", "for (int i = 0; i < 8; i++) CHECK_EQ(qpush(i), 0);@NL@CHECK_EQ(qpush(99), -1);@NL@for (int i = 0; i < 8; i++) CHECK_EQ(qpop(), i);@NL@CHECK_EQ(qpop(), -1);", "Eight slots exactly: the ninth push is refused, and a full drain leaves the queue empty."),
            ],
            level="combination",
        ),
        challenge(
            "ca18-rwlock-metric",
            "rwlock with a Live Reader Count",
            "Given: a `pthread_rwlock_t` and `int active_readers`. Implement `void lock_read(void)` (rdlock AND increment active_readers), `void unlock_read(void)` (decrement, then unlock), `void lock_write(void)` / `void unlock_write(void)` wrapping wrlock. The metric is how tests observe concurrency — keep it truthful.",
            C_PRELUDE + PTH
            + "static pthread_rwlock_t g_rwl = PTHREAD_RWLOCK_INITIALIZER;@NL@"
            + "static int active_readers = 0;@NL@",
            [
                ("reader count tracks", "lock_read();@NL@CHECK_EQ(active_readers, 1);@NL@lock_read();@NL@CHECK_EQ(active_readers, 2);@NL@unlock_read();@NL@CHECK_EQ(active_readers, 1);@NL@unlock_read();@NL@CHECK_EQ(active_readers, 0);", "Two readers hold the lock simultaneously — rdlock allows that — and the count follows exactly."),
                ("write path works", "lock_write();@NL@unlock_write();@NL@CHECK_EQ(active_readers, 0);", "The write path locks and releases without touching the reader metric."),
            ],
            level="imitation",
        ),
        challenge(
            "ca18-lock-order-clinic",
            "Deadlock or Safe?",
            "Implement `const char *lock_verdict(int kind)`: 0 two threads acquire mutexes A then B, and B then A → a deadlock risk; 1 all threads acquire A then B → safe; 2 second lock taken with try-lock, released and retried on failure → safe; 3 blocking acquisition of a second lock while an outer lock is held by the same thread that another thread needs first → a deadlock risk; 4 a single mutex, no nesting → safe.",
            C_PRELUDE,
            [
                ("inversion is the risk", "CHECK_STR_EQ(lock_verdict(0), @LV0@);", "Opposite acquisition orders can form a cycle: the definition of a deadlock risk."),
                ("consistent order is safe", "CHECK_STR_EQ(lock_verdict(1), @LV1@);@NL@CHECK_STR_EQ(lock_verdict(4), @LV1@);", "A global order (or a single lock) cannot cycle."),
                ("try-lock escapes", "CHECK_STR_EQ(lock_verdict(2), @LV1@);@NL@CHECK_STR_EQ(lock_verdict(3), @LV0@);", "try-lock converts deadlock into retry; blocking second acquisition while holding the first keeps the risk."),
            ],
            level="imitation",
        ),
    ],
    {
        "ca18-mutex-counter": vi_challenge(
            "Tài khoản tranh chấp",
            "Cho mutex và biến toàn cục account. Cài deposit (cộng dưới khóa) và balance. Grader dồn từ nhiều thread; update mất nghĩa là mất test.",
            [
                ("một thread", "Một lần deposit, một lần cập nhật: tài khoản phản ánh đúng."),
                ("bốn thread dồn", "concurrent_deposits (cho sẵn trong test) tạo 4 thread gửi 500 mỗi thread; mutex làm mọi cập nhật đứng vững: đúng 2000."),
                ("balance chỉ đọc", "Quan sát số dư không được làm thay đổi nó."),
            ],
        ),
        "ca18-condvar-queue": vi_challenge(
            "Hàng đợi FIFO giới hạn",
            "Cho mutex, condvar, slots[8], head/tail/count. Cài qpush (nối cuối FIFO; -1 khi đầy) và qpop (lấy cũ nhất; -1 khi rỗng).",
            [
                ("thứ tự FIFO", "Vào trước ra trước: hàng đợi là vòng tròn, không phải ngăn xếp."),
                ("pop rỗng bị từ chối", "Pop hàng đợi rỗng bị từ chối, không phải dữ liệu rác."),
                ("đầy rồi từ chối, rút cạn rồi từ chối", "Đúng tám slot: push thứ chín bị từ chối, rút cạn để hàng đợi rỗng."),
            ],
        ),
        "ca18-rwlock-metric": vi_challenge(
            "rwlock với số reader trực tuyến",
            "Cho pthread_rwlock_t và active_readers. Cài lock_read (rdlock VÀ tăng bộ đếm), unlock_read (giảm rồi mở), lock_write/unlock_write.",
            [
                ("bộ đếm theo sát", "Hai reader giữ khóa đồng thời — rdlock cho phép — và bộ đếm theo đúng từng bước."),
                ("nhánh write chạy", "Nhánh ghi khóa và nhả mà không đụng chỉ số reader."),
            ],
        ),
        "ca18-lock-order-clinic": vi_challenge(
            "Deadlock hay an toàn?",
            "Cài lock_verdict: hai thứ tự lấy khóa ngược nhau → rủi ro; thứ tự nhất quán hoặc try-lock → an toàn; lấy khóa thứ hai chặn trong khi đang giữ khóa ngoài → rủi ro.",
            [
                ("nghịch đảo là rủi ro", "Hai thứ tự lấy khóa ngược nhau có thể tạo chu trình: định nghĩa rủi ro deadlock."),
                ("thứ tự nhất quán an toàn", "Thứ tự toàn cục (hoặc một khóa duy nhất) không thể tạo chu trình."),
                ("try-lock thoát ra", "try-lock biến deadlock thành retry; lấy khóa thứ hai chặn trong khi giữ khóa đầu giữ nguyên rủi ro."),
            ],
        ),
    },
    solutions=[
        (
            "ca18-mutex-counter",
            C_PRELUDE + PTH
            + "static pthread_mutex_t cnt_mtx = PTHREAD_MUTEX_INITIALIZER;@NL@"
            + "static long long account = 0;@NL@"
            + "void deposit(long long);@NL@"
            + "static void *dep_worker(void *arg) { deposit((long long)(intptr_t)arg); return NULL; }@NL@"
            + "static long long concurrent_deposits(int nthreads, long long each) {@NL@"
            + "    pthread_t th[8];@NL@"
            + "    if (nthreads > 8) nthreads = 8;@NL@"
            + "    for (int i = 0; i < nthreads; i++) {@NL@"
            + "        if (pthread_create(&th[i], NULL, dep_worker, (void *)(intptr_t)each) != 0) return -1;@NL@"
            + "    }@NL@"
            + "    for (int i = 0; i < nthreads; i++) pthread_join(th[i], NULL);@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "void deposit(long long amount) {@NL@"
            + "    pthread_mutex_lock(&cnt_mtx);@NL@"
            + "    account += amount;@NL@"
            + "    pthread_mutex_unlock(&cnt_mtx);@NL@"
            + "}@NL@"
            + "long long balance(void) {@NL@"
            + "    pthread_mutex_lock(&cnt_mtx);@NL@"
            + "    long long v = account;@NL@"
            + "    pthread_mutex_unlock(&cnt_mtx);@NL@"
            + "    return v;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + PTH
            + "static pthread_mutex_t cnt_mtx = PTHREAD_MUTEX_INITIALIZER;@NL@"
            + "static long long account = 0;@NL@"
            + "void deposit(long long);@NL@"
            + "static void *dep_worker(void *arg) { deposit((long long)(intptr_t)arg); return NULL; }@NL@"
            + "static long long concurrent_deposits(int nthreads, long long each) {@NL@"
            + "    pthread_t th[8];@NL@"
            + "    if (nthreads > 8) nthreads = 8;@NL@"
            + "    for (int i = 0; i < nthreads; i++) {@NL@"
            + "        if (pthread_create(&th[i], NULL, dep_worker, (void *)(intptr_t)each) != 0) return -1;@NL@"
            + "    }@NL@"
            + "    for (int i = 0; i < nthreads; i++) pthread_join(th[i], NULL);@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "static long long shadow = 0;@NL@"
            + "void deposit(long long amount) {@NL@"
            + "    pthread_mutex_lock(&cnt_mtx);@NL@"
            + "    shadow += amount;@NL@"
            + "    pthread_mutex_unlock(&cnt_mtx);@NL@"
            + "}@NL@"
            + "long long balance(void) {@NL@"
            + "    pthread_mutex_lock(&cnt_mtx);@NL@"
            + "    long long v = account;@NL@"
            + "    pthread_mutex_unlock(&cnt_mtx);@NL@"
            + "    return v;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca18-condvar-queue",
            C_PRELUDE + PTH
            + "static pthread_mutex_t q_mtx = PTHREAD_MUTEX_INITIALIZER;@NL@"
            + "static pthread_cond_t q_cv = PTHREAD_COND_INITIALIZER;@NL@"
            + "static int slots[8];@NL@static size_t q_head = 0;@NL@"
            + "static size_t q_tail = 0;@NL@static size_t q_count = 0;@NL@"
            + "int qpush(int v) {@NL@"
            + "    pthread_mutex_lock(&q_mtx);@NL@"
            + "    if (q_count == 8) { pthread_mutex_unlock(&q_mtx); return -1; }@NL@"
            + "    slots[q_tail] = v;@NL@"
            + "    q_tail = (q_tail + 1) % 8;@NL@"
            + "    q_count++;@NL@"
            + "    pthread_cond_signal(&q_cv);@NL@"
            + "    pthread_mutex_unlock(&q_mtx);@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int qpop(void) {@NL@"
            + "    pthread_mutex_lock(&q_mtx);@NL@"
            + "    if (q_count == 0) { pthread_mutex_unlock(&q_mtx); return -1; }@NL@"
            + "    int v = slots[q_head];@NL@"
            + "    q_head = (q_head + 1) % 8;@NL@"
            + "    q_count--;@NL@"
            + "    pthread_mutex_unlock(&q_mtx);@NL@"
            + "    return v;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + PTH
            + "static pthread_mutex_t q_mtx = PTHREAD_MUTEX_INITIALIZER;@NL@"
            + "static pthread_cond_t q_cv = PTHREAD_COND_INITIALIZER;@NL@"
            + "static int slots[8];@NL@static size_t q_head = 0;@NL@"
            + "static size_t q_tail = 0;@NL@static size_t q_count = 0;@NL@"
            + "int qpush(int v) {@NL@"
            + "    pthread_mutex_lock(&q_mtx);@NL@"
            + "    if (q_count == 8) { pthread_mutex_unlock(&q_mtx); return -1; }@NL@"
            + "    slots[q_tail] = v;@NL@"
            + "    q_tail = (q_tail + 1) % 8;@NL@"
            + "    q_count++;@NL@"
            + "    pthread_cond_signal(&q_cv);@NL@"
            + "    pthread_mutex_unlock(&q_mtx);@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "int qpop(void) {@NL@"
            + "    pthread_mutex_lock(&q_mtx);@NL@"
            + "    if (q_count == 0) { pthread_mutex_unlock(&q_mtx); return -1; }@NL@"
            + "    q_tail = (q_tail + 7) % 8;@NL@"
            + "    int v = slots[q_tail];@NL@"
            + "    q_count--;@NL@"
            + "    pthread_mutex_unlock(&q_mtx);@NL@"
            + "    return v;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca18-rwlock-metric",
            C_PRELUDE + PTH
            + "static pthread_rwlock_t g_rwl = PTHREAD_RWLOCK_INITIALIZER;@NL@"
            + "static int active_readers = 0;@NL@"
            + "void lock_read(void) {@NL@"
            + "    pthread_rwlock_rdlock(&g_rwl);@NL@"
            + "    active_readers++;@NL@"
            + "}@NL@"
            + "void unlock_read(void) {@NL@"
            + "    active_readers--;@NL@"
            + "    pthread_rwlock_unlock(&g_rwl);@NL@"
            + "}@NL@"
            + "void lock_write(void) { pthread_rwlock_wrlock(&g_rwl); }@NL@"
            + "void unlock_write(void) { pthread_rwlock_unlock(&g_rwl); }@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + PTH
            + "static pthread_rwlock_t g_rwl = PTHREAD_RWLOCK_INITIALIZER;@NL@"
            + "static int active_readers = 0;@NL@"
            + "void lock_read(void) {@NL@"
            + "    pthread_rwlock_rdlock(&g_rwl);@NL@"
            + "}@NL@"
            + "void unlock_read(void) {@NL@"
            + "    pthread_rwlock_unlock(&g_rwl);@NL@"
            + "}@NL@"
            + "void lock_write(void) { pthread_rwlock_wrlock(&g_rwl); }@NL@"
            + "void unlock_write(void) { pthread_rwlock_unlock(&g_rwl); }@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca18-lock-order-clinic",
            C_PRELUDE
            + "const char *lock_verdict(int kind) {@NL@"
            + "    switch (kind) {@NL@"
            + "    case 0: return @LV0@;@NL@"
            + "    case 1: return @LV1@;@NL@"
            + "    case 2: return @LV1@;@NL@"
            + "    case 3: return @LV0@;@NL@"
            + "    case 4: return @LV1@;@NL@"
            + "    default: return @LV1@;@NL@"
            + "    }@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE
            + "const char *lock_verdict(int kind) {@NL@"
            + "    switch (kind) {@NL@"
            + "    case 0: return @LV1@;@NL@"
            + "    case 1: return @LV0@;@NL@"
            + "    case 2: return @LV1@;@NL@"
            + "    case 3: return @LV0@;@NL@"
            + "    case 4: return @LV1@;@NL@"
            + "    default: return @LV1@;@NL@"
            + "    }@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

# Checkpoint M18: deterministic thread-pool core.
write_checkpoint(
    M18,
    L18CP,
    "Checkpoint: Pool Work Queue",
    "One program: the deterministic core of a thread pool — a FIFO work queue with submit and drain, the shape every real pool wraps in threads.",
    16,
    "See lesson.",
    "Kiểm tra: Hàng đợi công việc của pool",
    "Một chương trình: lõi tất định của thread pool — hàng đợi công việc FIFO với submit và drain, hình dạng mọi pool thật bọc bằng thread.",
    "Xem bài học.",
    challenge(
        "ca18-checkpoint-pool",
        "Checkpoint: Pool Work Queue",
        "Given: `static task_fn pending[8]; static void *pending_arg[8]; static size_t n_pending;` (typedef for `void (*task_fn)(void *)` included). Implement `int pool_submit(task_fn fn, void *arg)` (append; 0 on success, -1 when full or fn NULL) and `size_t pool_execute(void)` (run every pending task in FIFO order, empty the queue, return how many ran).",
        C_PRELUDE + "#include <stdint.h>@NL@" + "typedef void (*task_fn)(void *);@NL@"
        + "static task_fn pending[8];@NL@static void *pending_arg[8];@NL@static size_t n_pending = 0;@NL@",
        [
            ("submit and drain in order", "CHECK_EQ(pool_submit(log_task, (void *)1), 0);@NL@CHECK_EQ(pool_submit(log_task, (void *)2), 0);@NL@CHECK_EQ(pool_submit(log_task, (void *)3), 0);@NL@CHECK_EQ((int)pool_execute(), 3);@NL@CHECK_EQ(g_log_n, 3);@NL@CHECK_EQ(g_log[0], 1);@NL@CHECK_EQ(g_log[2], 3);", "FIFO: the drain runs tasks in submission order — a pool that reorders work breaks consumers."),
            ("drain empties the queue", "CHECK_EQ((int)pool_execute(), 0);", "A second drain finds nothing: the queue was emptied by the first run."),
            ("refuse bad submissions", "CHECK_EQ(pool_submit(NULL, (void *)1), -1);@NL@CHECK_EQ((int)pool_execute(), 0);", "A NULL task is refused and the queue stays consistent."),
        ],
        level="capstone",
    ),
    {
        "ca18-checkpoint-pool": vi_challenge(
            "Kiểm tra: Hàng đợi công việc của pool",
            "Cho pending[8], pending_arg[8], n_pending. Cài pool_submit (nối cuối; 0/-1) và pool_execute (chạy mọi task theo thứ tự FIFO, dọn hàng đợi, trả số task đã chạy).",
            [
                ("nạp và rút theo thứ tự", "FIFO: lần rút chạy task theo thứ tự nạp — pool đảo thứ tự sẽ phá consumer."),
                ("rút dọn hàng đợi", "Lần rút thứ hai không còn gì: lần đầu đã dọn sạch."),
                ("từ chối nạp xấu", "Task NULL bị từ chối và hàng đợi vẫn nhất quán."),
            ],
        ),
    },
    solution=
            C_PRELUDE + "#include <stdint.h>@NL@" + "typedef void (*task_fn)(void *);@NL@"
            + "static task_fn pending[8];@NL@static void *pending_arg[8];@NL@static size_t n_pending = 0;@NL@"
            + "static int g_log[16];@NL@static size_t g_log_n = 0;@NL@"
            + "static void log_task(void *arg) { g_log[g_log_n++] = (int)(intptr_t)arg; }@NL@"
            + "int pool_submit(task_fn fn, void *arg) {@NL@"
            + "    if (fn == NULL || n_pending == 8) return -1;@NL@"
            + "    pending[n_pending] = fn;@NL@"
            + "    pending_arg[n_pending] = arg;@NL@"
            + "    n_pending++;@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "size_t pool_execute(void) {@NL@"
            + "    size_t ran = n_pending;@NL@"
            + "    for (size_t i = 0; i < n_pending; i++) {@NL@"
            + "        pending[i](pending_arg[i]);@NL@"
            + "    }@NL@"
            + "    n_pending = 0;@NL@"
            + "    return ran;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
    wrong=
            C_PRELUDE + "#include <stdint.h>@NL@" + "typedef void (*task_fn)(void *);@NL@"
            + "static task_fn pending[8];@NL@static void *pending_arg[8];@NL@static size_t n_pending = 0;@NL@"
            + "static int g_log[16];@NL@static size_t g_log_n = 0;@NL@"
            + "static void log_task(void *arg) { g_log[g_log_n++] = (int)(intptr_t)arg; }@NL@"
            + "int pool_submit(task_fn fn, void *arg) {@NL@"
            + "    if (fn == NULL || n_pending == 8) return -1;@NL@"
            + "    pending[n_pending] = fn;@NL@"
            + "    pending_arg[n_pending] = arg;@NL@"
            + "    n_pending++;@NL@"
            + "    return 0;@NL@"
            + "}@NL@"
            + "size_t pool_execute(void) {@NL@"
            + "    size_t ran = n_pending;@NL@"
            + "    for (size_t i = n_pending; i-- > 0;) {@NL@"
            + "        pending[i](pending_arg[i]);@NL@"
            + "    }@NL@"
            + "    n_pending = 0;@NL@"
            + "    return ran;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
)
