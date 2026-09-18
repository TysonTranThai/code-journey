#!/usr/bin/env python3
"""C — Intermediate — Module 15: cint-threads.

C11 threads — verified working in this sandbox (threads.h, mtx_t, cnd_t;
no -pthread needed on musl). Race conditions observed deterministically
via counters, mutexes protecting shared state, condition variables for
producer/consumer. Tests are latch/choreography-based, never
timing-based. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-threads"

write_module(
    M,
    "Concurrency Fundamentals (C11 Threads)",
    "thrd_create, mtx_t, cnd_t: the standard thread vocabulary — and the "
    "discipline that makes shared state survivable.",
    "Nền tảng đồng thời (C11 Threads)",
    "thrd_create, mtx_t, cnd_t: từ vựng thread chuẩn — và kỷ luật khiến "
    "state chia sẻ sống sót.",
    lessons=["threads-basics", "mutexes", "condition-vars", "cint-checkpoint-m15"],
    practices=["cint-p15-races", "cint-p15-procon"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "threads-basics",
    "Threads: thrd_create & thrd_join",
    "A thread is a function that runs elsewhere: create, join, and the "
    "return-value convention.",
    16,
    r"""
## The standard's vocabulary

C11 added `<threads.h>`: `thrd_t` (a thread handle), `thrd_create`
(start one), `thrd_join` (wait for it and collect its return):

```c
int work(void *arg) {                 /* signature is fixed: int(void*) */
    long id = (long)(intptr_t)arg;
    return (int)id;                   /* becomes thrd_join's out value */
}

thrd_t t;
if (thrd_create(&t, work, (void *)(intptr_t)7) == thrd_success) {
    int result;
    thrd_join(t, &result);            /* blocks until work returns */
}
```

Every thread runs the function you hand it; `arg` is how you pass data
(one pointer). **Joining is not optional hygiene** — an unjoined thread
keeps running while main exits (undefined which writes land), and
`thrd_join` is how you *know* the work finished. `thrd_detach` is the
fire-and-forget alternative: the thread cleans itself up, but then you
cannot wait for it or collect anything.

## Sharing is the entire problem

Two threads incrementing the same `int` is the canonical disaster:

```c
/* both threads run: counter++ */
/* counter++ is really: load, add, store — three steps */
```

The three steps interleave. Both threads can load 5, both store 6, and
one increment vanishes — a *lost update*. The fix is not "be careful":
it is making the read-modify-write indivisible (next lesson). The
discipline to build now: name every shared variable in a comment, and
treat every access to one as a design decision.
""",
"Thread: thrd_create & thrd_join",
    "Một thread là một hàm chạy ở nơi khác: tạo, join, và quy ước giá trị "
    "trả về.",
    r"""
## Từ vựng của chuẩn

C11 thêm `<threads.h>`: `thrd_t` (handle thread), `thrd_create` (chạy
một thread), `thrd_join` (chờ và thu kết quả):

```c
int work(void *arg) {                 /* chữ ký cố định: int(void*) */
    long id = (long)(intptr_t)arg;
    return (int)id;                   /* thành giá trị out của thrd_join */
}

thrd_t t;
if (thrd_create(&t, work, (void *)(intptr_t)7) == thrd_success) {
    int result;
    thrd_join(t, &result);            /* chặn đến khi work trả về */
}
```

Mỗi thread chạy hàm bạn đưa; `arg` là cách truyền dữ liệu (một con trỏ).
**Join không phải vệ sinh tùy chọn** — thread chưa join vẫn chạy khi
main thoát (không xác định lần ghi nào kịp đổ), và `thrd_join` là cách
 bạn *biết* việc đã xong. `thrd_detach` là phương án bắn-quên: thread tự
dọn, nhưng bạn không thể chờ hay thu gì cả.

## Chia sẻ là toàn bộ vấn đề

Hai thread tăng cùng một `int` là thảm họa kinh điển:

```c
/* cả hai thread chạy: counter++ */
/* counter++ thực chất là: load, add, store — ba bước */
```

Ba bước kẹp vào nhau. Cả hai thread có thể load 5, cả hai store 6, và
một lần biến mất — *mất mát cập nhật* (lost update). Cách chữa không
phải "cẩn thận": là làm read-modify-write thành bất khả chia (bài sau).
Kỷ luật cần xây ngay: ghi tên mọi biến chia sẻ vào comment, và coi mọi
truy cập vào nó là một quyết định thiết kế.
"""
)

write_lesson(
    M, "mutexes",
    "Mutexes: Making Sections Indivisible",
    "mtx_lock/unlock around shared state: what a critical section is, "
    "deadlock's recipe, and the perimeter rule.",
    17,
    r"""
## The lock makes three steps one

```c
mtx_t m;
mtx_init(&m, mtx_plain);          /* once, before threads exist */

mtx_lock(&m);
counter++;                        /* now indivisible: only one thread
                                     can hold m at a time */
mtx_unlock(&m);
```

A mutex is a token one thread holds at a time. Between `lock` and
`unlock` is the **critical section** — code that touches shared state.
While one thread holds `m`, every other `mtx_lock(&m)` *blocks* until
it is released. The rule: **every** access to the shared variable must
happen under the same mutex. Locking in one place and not another is
worse than no mutex — it is a lie in the code.

## Forgetting unlock is the classic bug

Every early return inside a critical section must unlock on the way
out — the cleanup-goto pattern returns with a new job:

```c
mtx_lock(&m);
if (bad) { rc = -1; goto out; }   /* out: does the unlock */
/* ... */
out:
    mtx_unlock(&m);
    return rc;
```

C11 has no RAII and no `mtx_unlock` destructor — the goto ladder (or
scrupulous pairing) is the discipline.

## Deadlock: the recipe and the only cure

Two mutexes acquired in different orders:

```c
/* thread A: lock(m1); lock(m2); */
/* thread B: lock(m2); lock(m1);   — each holds one, waits forever */
```

The cure is *total ordering*: all threads acquire multiple locks in the
same global order (and release in reverse). The other rule of thumb:
hold a lock for the shortest time possible — never across I/O, never
across `malloc` you can do before locking.
""",
"Mutex: biến đoạn code thành bất khả chia",
    "mtx_lock/unlock quanh state chia sẻ: đoạn găng là gì, công thức "
    "deadlock, và quy tắc chu vi.",
    r"""
## Khóa biến ba bước thành một

```c
mtx_t m;
mtx_init(&m, mtx_plain);          /* một lần, trước khi thread tồn tại */

mtx_lock(&m);
counter++;                        /* giờ bất khả chia: mỗi lúc một thread
                                     giữ m */
mtx_unlock(&m);
```

Mutex là mãnh mốc một thread giữ mỗi lúc một. Giữa `lock` và `unlock`
là **đoạn găng** (critical section) — code đụng vào state chia sẻ. Khi
một thread giữ `m`, mọi `mtx_lock(&m)` khác *chặn* cho tới khi nó được
thả. Quy tắc: **mọi** truy cập vào biến chia sẻ phải diễn ra dưới cùng
một mutex. Khóa ở một nơi mà quên nơi khác tệ hơn không có mutex — đó
là lời nói dối trong code.

## Quên unlock là bug kinh điển

Mọi return sớm trong đoạn găng phải unlock trên đường ra — mẫu
cleanup-goto có việc mới:

```c
mtx_lock(&m);
if (bad) { rc = -1; goto out; }   /* out: làm phần unlock */
/* ... */
out:
    mtx_unlock(&m);
    return rc;
```

C11 không có RAII và không có destructor cho `mtx_unlock` — thang goto
(hoặc ghép cặp cẩn trọng) là kỷ luật.

## Deadlock: công thức và cách chữa duy nhất

Hai mutex lấy theo thứ tự khác nhau:

```c
/* thread A: lock(m1); lock(m2); */
/* thread B: lock(m2); lock(m1);   — mỗi bên giữ một, chờ vĩnh viễn */
```

Cách chữa là *thứ tự toàn cục*: mọi thread lấy nhiều khóa theo cùng một
thứ tự (và thả theo thứ tự ngược). Kinh nghiệm khác: giữ khóa ngắn nhất
có thể — không bao giờ xuyên I/O, không xuyên `malloc` có thể làm trước
khi khóa.
"""
)

write_lesson(
    M, "condition-vars",
    "Condition Variables: Producer/Consumer",
    "cnd_wait/cnd_signal: waiting without burning CPU, the spurious-wakeup "
    "while-loop, and the bounded queue that ties the module together.",
    18,
    r"""
## Waiting politely

A thread that needs data has two bad options: spin on a flag (burns
CPU) or sleep blindly (wastes latency). The third option is the
**condition variable** — a wait channel paired with a mutex:

```c
/* consumer: */
mtx_lock(&m);
while (!data_ready)               /* WHILE, not if — see below */
    cnd_wait(&cv, &m);            /* atomically: unlock m + sleep;
                                     re-lock m before returning */
use(data);
mtx_unlock(&m);

/* producer: */
mtx_lock(&m);
data_ready = 1;
cnd_signal(&cv);                  /* wake ONE waiter */
mtx_unlock(&m);
```

`cnd_wait` releases the mutex while sleeping and re-acquires it before
returning — that pairing is why the predicate (`data_ready`) and the
signal both happen under the same mutex.

## The while-loop is not style

`cnd_signal` may wake a thread even when the predicate is false
(*spurious wakeup* — permitted by the standard), and between signal and
wake another consumer may have eaten the data. The `while` re-checks
the predicate after every wake; an `if` proceeds on a lie. This is the
single most-tested line in concurrency teaching — and the most-failed
one in student code.

## The bounded queue: the module's thesis

Producer/consumer with a fixed-size ring: `not_full` and `not_empty`
condition variables over the same mutex; producer waits on `not_full`,
consumer on `not_empty`; each signals the *other* after changing the
state. This is the shape inside every work queue, channel, and
connection pool — and it is the checkpoint's build.
""",
"Condition Variable: Producer/Consumer",
    "cnd_wait/cnd_signal: chờ không đốt CPU, vòng while chống spurious "
    "wakeup, và hàng đợi có giới hạn nối kết module.",
    r"""
## Chờ đợi lịch sự

Thread cần dữ liệu có hai lựa chọn xấu: quay vòng theo cờ (đốt CPU) hoặc
ngủ mù (lãng phí độ trễ). Lựa chọn thứ ba là **condition variable** —
kênh chờ đi cặp với một mutex:

```c
/* consumer: */
mtx_lock(&m);
while (!data_ready)               /* WHILE, không phải if — xem dưới */
    cnd_wait(&cv, &m);            /* all định: unlock m + ngủ;
                                     lock lại m trước khi trả về */
use(data);
mtx_unlock(&m);

/* producer: */
mtx_lock(&m);
data_ready = 1;
cnd_signal(&cv);                  /* đánh thức MỘT thread chờ */
mtx_unlock(&m);
```

`cnd_wait` thả mutex khi ngủ và lấy lại trước khi trả về — sự ghép cặp
đó là lý do vị từ (`data_ready`) và signal đều diễn ra dưới cùng một
mutex.

## Vòng while không phải phong cách

`cnd_signal` có thể đánh thức thread ngay cả khi vị từ sai (*spurious
wakeup* — chuẩn cho phép), và giữa signal và tỉnh dậy, consumer khác
có thể đã ăn hết dữ liệu. `while` kiểm lại vị từ sau mỗi lần tỉnh;
`if` tiến hành trên một lời nói dối. Đây là dòng được test nhiều nhất
trong dạy đồng thời — và dòng học viên fail nhiều nhất.

## Hàng đợi có giới hạn: luận điểm của module

Producer/consumer với ring cố định: hai condition variable `not_full`
và `not_empty` trên cùng một mutex; producer chờ `not_full`, consumer
chờ `not_empty`; mỗi bên signal cho *bên kia* sau khi đổi state. Đây là
hình dạng bên trong mọi work queue, channel, connection pool — và là
bài build của checkpoint.
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p15-races",
    "Race & Mutex Gym",
    "Observe a lost update, then fix it with a mutex — deterministically.",
    "Phòng gym race & mutex",
    "Quan sát mất mát cập nhật, rồi chữa bằng mutex — một cách all định.",
    after_lesson="mutexes",
    minutes=28,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p15-counters",
            "Lost Updates & Their Cure",
            """The boilerplate declares a tiny work harness:

```c
/* runs `workers` threads, each calling inc_n_times(count_target)
   `per_thread` times; joins them all; returns 0 if all joined ok.
   inc_n_times is YOURS to implement. */
int run_workers(int workers, int per_thread);
/* the shared counter all workers increment */
extern long g_counter;
/* the mutex protecting it — you must USE it in inc_n_times */
extern mtx_t g_counter_mtx;
void inc_n_times(int n);        /* increments g_counter exactly n times */
```

Round 1 of the test runs your implementation with the mutex and expects
the exact total. Round 2 (after you pass) reveals what happens without
it — the harness runs the *reference buggy* counter to demonstrate the
lost update.""",
            C_PRELUDE + "\n#include <threads.h>\n#include <stdatomic.h>\nlong g_counter = 0;\nmtx_t g_counter_mtx;\nstatic int run_workers(int workers, int per_thread);\nvoid inc_n_times(int n) {\n    for (int i = 0; i < n; i++) {\n        mtx_lock(&g_counter_mtx);\n        g_counter++;\n        mtx_unlock(&g_counter_mtx);\n    }\n}\n",
            [
                (
                    "counted exactly",
                    r"""
mtx_init(&g_counter_mtx, mtx_plain);
g_counter = 0;
CHECK_EQ(run_workers(4, 1000), 0);
CHECK_EQ(g_counter, 4000);       /* exact: no lost update */
g_counter = 0;
CHECK_EQ(run_workers(8, 500), 0);
CHECK_EQ(g_counter, 4000);
mtx_destroy(&g_counter_mtx);
""",
                    "Lock around the increment (or the whole n-loop — both pass); the exact total is what timing cannot guarantee.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p15-counters": vi_challenge(
            "Mất mát cập nhật và thuốc chữa",
            "Cài inc_n_times với mutex — tổng phải đúng tuyệt đối sau khi join.",
            [("đếm chính xác", "khóa quanh phép tăng; tổng chính xác là thứ timing không bảo đảm được.")],
        ),
    },
    solutions=[
        (
            "cint-p15-counters",
            r"""
#include <threads.h>
#include <stddef.h>
#define MAXW 16
typedef struct { int per; } WArg;
static WArg g_args[MAXW];
static thrd_t g_ts[MAXW];
static int worker(void *p) {
    WArg *a = p;
    inc_n_times(a->per);
    return 0;
}
int run_workers(int workers, int per_thread) {
    if (workers < 0 || workers > MAXW || per_thread < 0) return -1;
    for (int i = 0; i < workers; i++) {
        g_args[i].per = per_thread;
        if (thrd_create(&g_ts[i], worker, &g_args[i]) != thrd_success)
            return -1;
    }
    for (int i = 0; i < workers; i++) {
        int rc;
        if (thrd_join(g_ts[i], &rc) != thrd_success) return -1;
    }
    return 0;
}""",
            r"""
#include <threads.h>
#include <stddef.h>
#define MAXW 16
typedef struct { int per; } WArg;
static WArg g_args[MAXW];
static thrd_t g_ts[MAXW];
static int worker(void *p) {
    WArg *a = p;
    inc_n_times(a->per);
    return 0;
}
int run_workers(int workers, int per_thread) {
    if (workers < 0 || workers > MAXW || per_thread < 0) return -1;
    for (int i = 0; i < workers; i++) {
        g_args[i].per = per_thread;
        if (thrd_create(&g_ts[i], worker, &g_args[i]) != thrd_success)
            return -1;
    }
    for (int i = 0; i < workers - 1; i++) {   /* wrong: never joins the LAST
                                          worker — main may race ahead of its
                                          final increments, so the total is
                                          short by up to per_thread */
        int rc;
        thrd_join(g_ts[i], &rc);
    }
    return 0;
}""",
        ),
    ],
)

write_practice(
    M, "cint-p15-procon",
    "Producer/Consumer Gym",
    "A bounded queue with two condition variables.",
    "Phòng gym producer/consumer",
    "Hàng đợi có giới hạn với hai condition variable.",
    after_lesson="condition-vars",
    minutes=30,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p15-bounded-queue",
            "The Bounded Queue",
            """Implement the bounded queue. The boilerplate declares:

```c
#define QCAP 4
typedef struct {
    long items[QCAP];
    size_t head, count;
    mtx_t m;
    cnd_t not_full, not_empty;
} BQ;
void bq_init(BQ *q);            /* inits mutex + cnds */
void bq_destroy(BQ *q);
/* push: blocks while full; 0 ok */
int bq_push(BQ *q, long v);
/* pop: blocks while empty; 0 ok */
int bq_pop(BQ *q, long *out);
size_t bq_count(BQ *q);         /* call only when no workers run */
```

Producers/consumers will run against it in tests — the predicate
re-check MUST be a while loop.""",
            C_PRELUDE + "\n#include <threads.h>\n#include <stddef.h>\n#define QCAP 4\ntypedef struct {\n    long items[QCAP];\n    size_t head, count;\n    mtx_t m;\n    cnd_t not_full, not_empty;\n} BQ;\nvoid bq_init(BQ *q);\nvoid bq_destroy(BQ *q);\nint bq_push(BQ *q, long v);\nint bq_pop(BQ *q, long *out);\nsize_t bq_count(BQ *q);\n",
            [
                (
                    "bounded handoff",
                    r"""
BQ q;
bq_init(&q);
/* single-threaded sanity: push 4 = full capacity */
for (long i = 0; i < 4; i++) CHECK_EQ(bq_push(&q, i), 0);
CHECK_EQ(bq_count(&q), 4u);
long v;
CHECK_EQ(bq_pop(&q, &v), 0); CHECK_EQ(v, 0);   /* FIFO */
CHECK_EQ(bq_push(&q, 99), 0);
CHECK_EQ(bq_count(&q), 4u);
CHECK_EQ(bq_pop(&q, &v), 0); CHECK_EQ(v, 1);
CHECK_EQ(bq_pop(&q, &v), 0); CHECK_EQ(v, 2);
CHECK_EQ(bq_pop(&q, &v), 0); CHECK_EQ(v, 3);
CHECK_EQ(bq_pop(&q, &v), 0); CHECK_EQ(v, 99);
CHECK_EQ(bq_count(&q), 0u);
bq_destroy(&q);
""",
                    "push: lock, while (count == QCAP) cnd_wait(not_full), store at (head+count)%QCAP, count++, cnd_signal(not_empty), unlock. Mirror for pop.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p15-bounded-queue": vi_challenge(
            "Hàng đợi có giới hạn",
            "Cài BQ: push/pop chặn với hai cnd, FIFO qua ring, while kiểm vị từ.",
            [("chuyển giao có giới hạn", "lock, while đầy thì wait, lưu, đếm++, signal bên kia, unlock.")],
        ),
    },
    solutions=[
        (
            "cint-p15-bounded-queue",
            r"""
#include <threads.h>
#include <stddef.h>
void bq_init(BQ *q) {
    if (!q) return;
    q->head = 0;
    q->count = 0;
    mtx_init(&q->m, mtx_plain);
    cnd_init(&q->not_full);
    cnd_init(&q->not_empty);
}
void bq_destroy(BQ *q) {
    if (!q) return;
    mtx_destroy(&q->m);
    cnd_destroy(&q->not_full);
    cnd_destroy(&q->not_empty);
}
int bq_push(BQ *q, long v) {
    if (!q) return -1;
    mtx_lock(&q->m);
    while (q->count == QCAP)
        cnd_wait(&q->not_full, &q->m);
    q->items[(q->head + q->count) % QCAP] = v;
    q->count++;
    cnd_signal(&q->not_empty);
    mtx_unlock(&q->m);
    return 0;
}
int bq_pop(BQ *q, long *out) {
    if (!q || !out) return -1;
    mtx_lock(&q->m);
    while (q->count == 0)
        cnd_wait(&q->not_empty, &q->m);
    *out = q->items[q->head];
    q->head = (q->head + 1) % QCAP;
    q->count--;
    cnd_signal(&q->not_full);
    mtx_unlock(&q->m);
    return 0;
}
size_t bq_count(BQ *q) {
    if (!q) return 0;
    mtx_lock(&q->m);
    size_t n = q->count;
    mtx_unlock(&q->m);
    return n;
}""",                    r"""
#include <threads.h>
#include <stddef.h>
void bq_init(BQ *q) {
    if (!q) return;
    q->head = 0;
    q->count = 0;
    mtx_init(&q->m, mtx_plain);
    cnd_init(&q->not_full);
    cnd_init(&q->not_empty);
}
void bq_destroy(BQ *q) {
    if (!q) return;
    mtx_destroy(&q->m);
    cnd_destroy(&q->not_full);
    cnd_destroy(&q->not_empty);
}
int bq_push(BQ *q, long v) {
    if (!q) return -1;
    mtx_lock(&q->m);
    q->items[q->head] = v;         /* wrong: stores at head — the oldest
                                          slot — instead of the tail; with a
                                          full ring this OVERWRITES the oldest
                                          value, so FIFO order is destroyed
                                          deterministically */
    q->head = (q->head + 1) % QCAP;
    if (q->count < QCAP) q->count++;
    cnd_signal(&q->not_empty);
    mtx_unlock(&q->m);
    return 0;
}
int bq_pop(BQ *q, long *out) {
    if (!q || !out) return -1;
    mtx_lock(&q->m);
    if (q->count == 0) {           /* wrong: IF, not WHILE — a spurious
                                          wakeup pops garbage; also returns
                                          WITHOUT unlocking on this path */
        return -1;
    }
    q->head = (q->head + 1) % QCAP;   /* wrong: advances head BEFORE reading —
                                          pops return the NEXT element, so
                                          the first pop loses the oldest */
    *out = q->items[q->head];
    q->count--;
    cnd_signal(&q->not_full);
    mtx_unlock(&q->m);
    return 0;
}
size_t bq_count(BQ *q) {
    if (!q) return 0;
    return q->count;               /* wrong: unlocked read — fine when no
                                       workers run, but the contract here
                                       is a locked read */
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m15-task",
    "Threaded Sum Pipeline",
    """The checkpoint: a two-stage pipeline. One producer thread pushes
0..n-1 into the bounded queue; one consumer thread pops everything and
sums. The boilerplate wires the queue (a correct reference
implementation), the thread entry wrappers, and a run_pipeline harness;
YOU implement only the two worker bodies:

```c
/* producer body: push 0..n-1 into q, then signal completion by
   incrementing producers_done under done_m with cnd_broadcast.
   0 ok, -1 bad args. */
int producer_body(BQ *q, int n);
/* consumer body: pop exactly `expected` items (bq_ref_pop BLOCKS until
   data exists — that blocking IS the synchronization), summing them
   into *sum. 0 ok, -1 bad args. */
int consumer_body(BQ *q, int expected, long *sum);
```

The harness starts both threads, joins them, and reports *total — it
must equal the exact sum of 0..n-1.""",
    C_PRELUDE + "\n#include <threads.h>\n#include <stddef.h>\n#define QCAP 4\ntypedef struct {\n    long items[QCAP];\n    size_t head, count;\n    mtx_t m;\n    cnd_t not_full, not_empty;\n} BQ;\n/* ---- reference queue (correct; defined here) ---- */\nstatic void bq_ref_init(BQ *q) {\n    q->head = 0; q->count = 0;\n    mtx_init(&q->m, mtx_plain);\n    cnd_init(&q->not_full);\n    cnd_init(&q->not_empty);\n}\nstatic void bq_ref_destroy(BQ *q) {\n    mtx_destroy(&q->m);\n    cnd_destroy(&q->not_full);\n    cnd_destroy(&q->not_empty);\n}\nstatic int bq_ref_push(BQ *q, long v) {\n    if (!q) return -1;\n    mtx_lock(&q->m);\n    while (q->count == QCAP)\n        cnd_wait(&q->not_full, &q->m);\n    q->items[(q->head + q->count) % QCAP] = v;\n    q->count++;\n    cnd_signal(&q->not_empty);\n    mtx_unlock(&q->m);\n    return 0;\n}\nstatic int bq_ref_pop(BQ *q, long *out) {\n    if (!q || !out) return -1;\n    mtx_lock(&q->m);\n    while (q->count == 0)\n        cnd_wait(&q->not_empty, &q->m);\n    *out = q->items[q->head];\n    q->head = (q->head + 1) % QCAP;\n    q->count--;\n    cnd_signal(&q->not_full);\n    mtx_unlock(&q->m);\n    return 0;\n}\n/* ---- completion latch (shared, non-static) ---- */\nint producers_done = 0;\nmtx_t done_m;\ncnd_t done_cv;\nstatic void pipeline_reset(void) {\n    static int inited = 0;\n    if (!inited) { mtx_init(&done_m, mtx_plain); cnd_init(&done_cv); inited = 1; }\n    producers_done = 0;\n}\n/* ---- YOUR worker bodies ---- */\nint producer_body(BQ *q, int n);\nint consumer_body(BQ *q, int expected, long *sum);\n/* ---- harness (reference; defined here) ---- */\ntypedef struct { BQ *q; int n; } PArgs;\ntypedef struct { BQ *q; int expected; long *sum; } CArgs;\nstatic int producer_entry(void *p) { PArgs *a = p; return producer_body(a->q, a->n); }\nstatic int consumer_entry(void *p) { CArgs *a = p; return consumer_body(a->q, a->expected, a->sum); }\nstatic int run_pipeline(BQ *q, int n, long *total) {\n    if (!q || !total || n < 0) return -1;\n    pipeline_reset();\n    PArgs pa = { q, n };\n    CArgs ca = { q, n, total };\n    thrd_t pt, ct;\n    if (thrd_create(&ct, consumer_entry, &ca) != thrd_success) return -1;\n    if (thrd_create(&pt, producer_entry, &pa) != thrd_success) return -1;\n    thrd_join(pt, NULL);\n    thrd_join(ct, NULL);\n    return 0;\n}\n",
    [
        (
            "exact total through the pipe",
            r"""
BQ q;
bq_ref_init(&q);
long total = 0;
CHECK_EQ(run_pipeline(&q, 100, &total), 0);
CHECK_EQ(total, 4950);                        /* sum of 0..99, exact */
pipeline_reset();
CHECK_EQ(run_pipeline(&q, 50, &total), 0);
CHECK_EQ(total, 1225);                        /* sum of 0..49 */
CHECK_EQ(producers_done, 1);                  /* producer signalled */
pipeline_reset();
CHECK_EQ(run_pipeline(&q, 0, &total), 0);     /* empty pipeline */
CHECK_EQ(total, 0);
CHECK_EQ(run_pipeline(NULL, 5, &total), -1);
CHECK_EQ(run_pipeline(&q, 5, NULL), -1);
bq_ref_destroy(&q);
""",
            "Producer: push 0..n-1, then lock done_m, producers_done++, cnd_broadcast, unlock. Consumer: pop expected times — bq_ref_pop blocks, so the blocking IS the synchronization.",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Đường ống tổng có thread",
        "Cài producer_body/consumer_body: tổng 0..n-1 chảy qua queue 4 slot — đúng tuyệt đối.",
        [("tổng chính xác qua đường ống", "producer đẩy xong đặt cờ + broadcast; consumer pop expected lần (pop chặn = đồng bộ hóa).")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m15",
    "Checkpoint: The Pipeline",
    "Prove the concurrency discipline: exact results through a bounded queue with real threads.",
    30,
    r"""
## The task

Implement `producer_body` and `consumer_body` (see the challenge). The
queue and harness are given (correct); the graded work is the
choreography: producers signal completion, the consumer relies on the
queue's blocking pop — and the total comes out *exact*: 4950 through a
4-slot pipe, then 1225, then 0 for an empty pipeline. No timing
assumptions survive this test; only correct synchronization does.

Passing this proves you can wire real threads around a shared bounded
resource — the pattern behind every worker pool and channel in
production C.

Next module: the capstone — every module's discipline in one program.
""",
    "Kiểm tra: Đường ống",
    "Chứng minh kỷ luật đồng thời: kết quả chính xác qua hàng đợi có giới hạn với thread thật.",
    r"""
## Bài toán

Cài `producer_body` và `consumer_body` (xem challenge). Queue và harness
đã cho (đúng); phần được chấm là bài dựng sân khấu: producer báo hoàn
thành, consumer dựa vào pop chặn của queue — và tổng ra *chính xác*:
4950 chảy qua ống 4 slot, rồi 1225, rồi 0 cho đường ống rỗng. Không giả
định timing nào sống sót qua test này; chỉ có đồng bộ đúng.

Vượt qua chứng minh bạn nối được thread thật quanh một tài nguyên có
giới hạn chia sẻ — mẫu đứng sau mọi worker pool và channel trong C
production.

Module sau: capstone — kỷ luật của mọi module trong một chương trình.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <threads.h>
#include <stddef.h>
int producer_body(BQ *q, int n) {
    if (!q || n < 0) return -1;
    for (int i = 0; i < n; i++)
        if (bq_ref_push(q, i) != 0) return -1;
    mtx_lock(&done_m);
    producers_done++;
    cnd_broadcast(&done_cv);
    mtx_unlock(&done_m);
    return 0;
}
int consumer_body(BQ *q, int expected, long *sum) {
    if (!q || !sum || expected < 0) return -1;
    long acc = 0;
    for (int i = 0; i < expected; i++) {
        long v;
        if (bq_ref_pop(q, &v) != 0) return -1;
        acc += v;
    }
    *sum = acc;
    return 0;
}""",
    wrong=r"""
#include <threads.h>
#include <stddef.h>
int producer_body(BQ *q, int n) {
    if (!q || n < 0) return -1;
    for (int i = 0; i < n; i++)
        if (bq_ref_push(q, i) != 0) return -1;
    return 0;                      /* wrong: never signals producers_done */
}
int consumer_body(BQ *q, int expected, long *sum) {
    if (!q || !sum || expected < 0) return -1;
    mtx_lock(&done_m);
    int done = producers_done > 0;   /* wrong: reads the latch ONCE, before
                                          the producer can finish — and since
                                          this consumer never pops, the
                                          producer blocks on the full queue
                                          and can NEVER signal. Deterministic
                                          deadlock of intent. */
    mtx_unlock(&done_m);
    if (!done) {
        *sum = -1;
        return 0;
    }
    long acc = 0;
    for (int i = 0; i < expected; i++) {
        long v;
        if (bq_ref_pop(q, &v) != 0) return -1;
        acc += v;
    }
    *sum = acc;
    return 0;
}""",
)

print("module 15 complete")
