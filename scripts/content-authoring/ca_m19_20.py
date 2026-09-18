#!/usr/bin/env python3
"""C Advanced — batch 10: modules 19 (memory-model) and 20 (sockets).
Zero typed backslashes: @NL@ = statement separator, @CE@ = newline escape
inside C string literals, @T*/@J*/@LV*/@FDSH@/@FDsh@/@FDdashc@ = runtime
placeholder tokens expanded by ca.py. Solutions are complete standalone
programs (own includes + main) absorbed into test TUs via #define main."""
from ca import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

POSIX = (
    "#define _POSIX_C_SOURCE 200809L@NL@"
    "#include <unistd.h>@NL@"
    "#include <sys/socket.h>@NL@"
    "#include <sys/time.h>@NL@"
    "#include <netinet/in.h>@NL@"
    "#include <arpa/inet.h>@NL@"
    "#include <signal.h>@NL@"
    "#include <errno.h>@NL@"
)

ATOMICS = (
    "#include <stdatomic.h>@NL@"
)

THREADS = (
    "#include <pthread.h>@NL@"
)

# ================= MODULE 19: ca-memory-model ================================
M19 = "ca-memory-model"

L19A = "ca-atomics-orderings"
L19B = "ca-cas-aba-false-sharing"
L19CP = "ca-checkpoint-m19"

write_module(
    M19,
    "The C11 Memory Model: Atomics and Ordering",
    "What the standard actually promises about concurrent visibility: atomic operations, the six orderings, compare-exchange, the ABA hazard, and false sharing. C11 atomics are ISO C — pthreads is POSIX; the distinction is labeled throughout.",
    "Mô hình bộ nhớ C11: atomic và thứ tự",
    "Những gì chuẩn thật sự hứa về khả năng hiển thị đồng thời: thao tác atomic, sáu thứ tự bộ nhớ, compare-exchange, nguy cơ ABA, và false sharing. C11 atomics là ISO C — pthreads là POSIX; phân biệt được ghi nhãn xuyên suốt.",
    [L19A, L19B, L19CP],
    ["ca-p19-memory-model"],
)

write_lesson(
    M19,
    L19A,
    "Atomics and the Six Orderings",
    "Non-atomic data races are undefined behavior; atomics are the language's built-in way to share data across threads with defined visibility.",
    20,
    """
## The problem atomics solve

Two threads incrementing a plain `int` is a **data race** — undefined behavior in ISO C (C11 §5.1.2.4). The compiler may load once, add twice, store once; the hardware may interleave reads and writes mid-word. Atomics fix this by making read-modify-write **indivisible** and by letting you choose how strongly visibility propagates.

```c
#include <stdatomic.h>          /* ISO C — not POSIX */

atomic_int counter = 0;         /* initialized to 0, no race on init */

void bump(void) {
    atomic_fetch_add(&counter, 1);   /* returns the PREVIOUS value */
}
```

`atomic_fetch_add` returns the value *before* the addition — the classic `x++` race is gone because the whole load-add-store is one atomic operation.

## The six orderings, honestly ranked

| ordering | promise | use it when |
|----------|---------|-------------|
| `memory_order_relaxed` | atomicity only; no ordering of other memory | statistics counters, sequence numbers |
| `memory_order_acquire` | later reads/writes cannot move before this load | the *reading* side of a lock-free publish |
| `memory_order_release` | earlier reads/writes cannot move after this store | the *writing* side of a lock-free publish |
| `memory_order_acq_rel` | both, for read-modify-write ops | CAS loops that read and write |
| `memory_order_seq_cst` | one total order every thread agrees on | default; use unless profiling says otherwise |
| `memory_order_consume` | deprecated in practice; compilers promote to acquire | do not use |

The **release/acquire pair** is the workhorse: a release store that writes flag=1 *synchronizes-with* an acquire load that observes flag=1, making everything written before the release visible after the acquire. This sandbox (gcc on aarch64) honors both; `ATOMIC_INT_LOCK_FREE == 2` here, so `atomic_int` needs no lock.

## Relaxed is not broken — it is narrower

The default `seq_cst` is total order across *all* atomic operations. `relaxed` keeps atomicity but allows different threads to *disagree about the order of different variables*. It is the right tool for a miss counter nobody coordinates on — and the wrong tool for publishing a pointer (the data behind the pointer needs the release/acquire fence).

## Rule of the module

**ISO C atomics define visibility; POSIX pthreads defines threads.** `pthread_create` is POSIX (feature macro required); `atomic_int` is ISO C. Keep the labels straight and the code portable.
""",
    "Atomics và sáu thứ tự bộ nhớ",
    "Data race không atomic là hành vi không xác định; atomic là cách ngôn ngữ chia sẻ dữ liệu giữa các thread với khả năng hiển thị xác định.",
    """
## Vấn đề atomic giải quyết

Hai thread tăng một `int` thường là **data race** — hành vi không xác định trong ISO C (C11 §5.1.2.4). Compiler có thể load một lần, cộng hai lần, store một lần; phần cứng có thể xen kẽ đọc/ghi giữa từ. Atomic sửa điều này bằng cách làm read-modify-write **vẹn nguyên** và cho bạn chọn mức truyền-ba-thấy.

```c
#include <stdatomic.h>          /* ISO C — không phải POSIX */

atomic_int counter = 0;

void bump(void) {
    atomic_fetch_add(&counter, 1);   /* trả về giá trị TRƯỚC khi cộng */
}
```

`atomic_fetch_add` trả về giá trị *trước* phép cộng — race kinh điển của `x++` biến mất vì toàn bộ load-cộng-store là một thao tác atomic.

## Sáu thứ tự, xếp hạng thẳng thắn

| thứ tự | hứa hẹn | dùng khi |
|--------|---------|----------|
| `memory_order_relaxed` | chỉ atomicity; không thứ tự bộ nhớ khác | bộ đếm thống kê, số thứ tự |
| `memory_order_acquire` | đọc/ghi sau không trôi lên trước load này | phía *đọc* của publish lock-free |
| `memory_order_release` | đọc/ghi trước không trôi xuống sau store này | phía *ghi* của publish lock-free |
| `memory_order_acq_rel` | cả hai, cho read-modify-write | vòng CAS vừa đọc vừa ghi |
| `memory_order_seq_cst` | một thứ tự toàn cục mọi thread đồng ý | mặc định; dùng trừ khi profiling nói khác |
| `memory_order_consume` | thực tế bị bỏ; compiler nâng thành acquire | không dùng |

Cặp **release/acquire** là ngựa thồ: release store đặt flag=1 *synchronizes-with* acquire load thấy flag=1, khiến mọi thứ viết trước release hiển thị sau acquire. Sandbox này (gcc trên aarch64) tôn trọng cả hai; `ATOMIC_INT_LOCK_FREE == 2`, nên `atomic_int` không cần khóa.

## Relaxed không hỏng — nó hẹp hơn

Mặc định `seq_cst` là thứ tự toàn cục qua *mọi* thao tác atomic. `relaxed` giữ atomicity nhưng cho phép các thread *không đồng thuận về thứ tự giữa các biến khác nhau*. Đúng cho bộ đếm miss không ai phối hợp — sai cho publish con trỏ (dữ liệu sau con trỏ cần hàng rào release/acquire).

## Quy tắc của mô-đun

**ISO C atomics định nghĩa khả năng hiển thị; POSIX pthreads định nghĩa thread.** `pthread_create` là POSIX (cần feature macro); `atomic_int` là ISO C. Giữ nhãn rõ và code vẫn portable.
""",
)

write_lesson(
    M19,
    L19B,
    "CAS Loops, ABA, and False Sharing",
    "Compare-exchange is the atom behind every lock-free algorithm — and behind two of its most instructive failure modes.",
    20,
    """
## Compare-exchange, the universal atom

```c
atomic_int v = 10;
int expected = 10;
atomic_compare_exchange_strong(&v, &expected, 20);
/* if v == expected: v = 20, returns true (expected untouched)
   else:             expected = current v, returns false */
```

CAS reads, compares, and conditionally writes as **one** atomic step. Every lock-free structure is a loop: load, compute a new value, CAS; on failure the exchange gives you the fresh value and you retry:

```c
int old = atomic_load(&v);
while (!atomic_compare_exchange_weak(&v, &old, old * 2)) {
    /* old was refreshed by the failed CAS; just loop */
}
```

`weak` may fail spuriously (cheaper on some architectures) — always use it inside a loop; use `strong` for one-shot decisions.

## ABA: the comparison lies

CAS compares *values*, not *histories*. Thread 1 reads A, stalls; thread 2 replaces A with B, then B with A again. Thread 1's CAS sees value A and succeeds — but the object behind the value is not the one it inspected. Classic victim: lock-free stacks recycling nodes through a free list.

Honest beginner-grade mitigations, in ascending cost:

1. **Never reclaim while readers may hold pointers** (epoch/RCU discipline — Intermediate/Advanced pattern).
2. **Tag the value**: pack a version counter alongside (per-CAS `atomic_fetch_add` on a second word, or a double-width CAS).
3. **Pool per thread** so a node cannot be freed and re-allocated by another thread mid-operation.

We practice the tag pattern because it is implementable and testable here; RCU is named so you know it exists.

## False sharing: the cache-line tax

Cores exchange memory in cache lines (typically 64 bytes; `atomic_is_lock_free` aside, this is hardware reality, not a C standard term). Two hot atomics placed side by side ping-pong one line between cores even though no thread ever touches the other variable — correctness intact, throughput wrecked.

```c
struct counts {
    atomic_int a;    /* thread 0 hammers a */
    atomic_int b;    /* thread 1 hammers b — same 64B line as a! */
};

struct counts_padded {
    atomic_int a;
    char pad[64 - sizeof(atomic_int)];   /* b moves to the next line */
    atomic_int b;
};
```

Padding is the fix. Measuring is the discipline: pad only when contention measurement shows the line is the problem.

## Field notes

- CAS loops are starvation-prone under contention — bound retries and fall back to a lock if you must guarantee progress.
- `atomic_exchange` swaps unconditionally and returns the old value; handy for "take the latest" patterns.
- This image reports `ATOMIC_POINTER_LOCK_FREE == 2`: pointer-sized atomics are hardware lock-free here.
""",
    "Vòng CAS, ABA, và false sharing",
    "Compare-exchange là nguyên tử đằng sau mọi thuật toán lock-free — và đằng sau hai failure mode giáo dục nhất của nó.",
    """
## Compare-exchange, nguyên tử phổ quát

```c
atomic_int v = 10;
int expected = 10;
atomic_compare_exchange_strong(&v, &expected, 20);
/* nếu v == expected: v = 20, trả true (expected giữ nguyên)
   else:              expected = v hiện tại, trả false */
```

CAS đọc, so sánh, và ghi có điều kiện trong **một** bước atomic. Mọi cấu trúc lock-free là một vòng lặp: load, tính giá trị mới, CAS; thất bại thì CAS đưa giá trị mới về cho bạn và bạn thử lại:

```c
int old = atomic_load(&v);
while (!atomic_compare_exchange_weak(&v, &old, old * 2)) {
    /* old đã được CAS thất bại làm mới; cứ lặp */
}
```

`weak` có thể thất bại giả (rẻ hơn trên vài kiến trúc) — luôn dùng trong vòng lặp; dùng `strong` cho quyết định một lần.

## ABA: sự so sánh nói dối

CAS so sánh *giá trị*, không phải *lịch sử*. Thread 1 đọc A rồi bị treo; thread 2 thay A bằng B, rồi B bằng A trở lại. CAS của thread 1 thấy giá trị A và thành công — nhưng đối tượng sau giá trị không còn là đối tượng nó từng xem xét. Nạn nhân kinh điển: stack lock-free tái chế node qua free list.

Giảm nhẹ ở mức người mới, theo giá tăng dần:

1. **Không thu hồi khi reader còn giữ con trỏ** (kỷ luật epoch/RCU — pattern Intermediate/Advanced).
2. **Gắn thẻ giá trị**: đóng gói bộ đếm phiên bản cạnh đó (atomic_fetch_add trên từ thứ hai, hoặc CAS kép).
3. **Pool theo thread** để node không thể bị thread khác giải phóng và cấp lại giữa thao tác.

Chúng ta luyện pattern gắn thẻ vì nó cài đặt và kiểm thử được ở đây; RCU được nêu tên để bạn biết nó tồn tại.

## False sharing: thuế cache-line

Các core trao đổi bộ nhớ theo cache line (thường 64 byte; đây là thực tế phần cứng, không phải thuật ngữ chuẩn C). Hai atomic nóng đặt cạnh nhau đá một line qua lại giữa các core dù không thread nào đụng biến kia — đúng đắn nhưng thông lượng sập.

```c
struct counts {
    atomic_int a;    /* thread 0 đập a */
    atomic_int b;    /* thread 1 đập b — cùng line 64B với a! */
};

struct counts_padded {
    atomic_int a;
    char pad[64 - sizeof(atomic_int)];   /* b sang line kế */
    atomic_int b;
};
```

Padding là bản vá. Đo đạc là kỷ luật: chỉ pad khi số liệu contention cho thấy line là vấn đề.

## Ghi chú thực địa

- Vòng CAS dễ đói dưới contention — chặn số lần thử và lùi về khóa nếu cần bảo đảm tiến trình.
- `atomic_exchange` hoán đổi vô điều kiện và trả giá trị cũ; tiện cho pattern "lấy mới nhất".
- Ảnh này báo `ATOMIC_POINTER_LOCK_FREE == 2`: atomic cỡ con trỏ là hardware lock-free tại đây.
""",
)

write_practice(
    M19,
    "ca-p19-memory-model",
    "Atomics and Ordering Drills",
    "Implement CAS loops, orderings, and padded counters against the real C11 semantics of this toolchain.",
    "Bài tập atomic và thứ tự",
    "Cài vòng CAS, thứ tự bộ nhớ, và bộ đếm có padding trên ngữ nghĩa C11 thật của toolchain này.",
    L19A,
    24,
    "advanced",
    [
        challenge(
            "ca19-cas-doubling-loop",
            "CAS Loop: Double Until Even",
            "ISO C11. Implement `void double_until_even(atomic_int *v)` — repeatedly double `*v` using a compare-exchange loop until the new value is even. Every doubling must go through one atomic CAS (no plain `*v = *v * 2`).",
            C_PRELUDE + ATOMICS,
            [
                ("doubles odd values once", "atomic_int v = 3;@NL@double_until_even(&v);@NL@CHECK_EQ(atomic_load(&v), 6);", "3 doubled is 6 — even, so exactly one CAS round."),
                ("already even stays", "atomic_int w = 4;@NL@double_until_even(&w);@NL@CHECK_EQ(atomic_load(&w), 8);", "4 is even but the contract is double-then-check: 8, still one round."),
                ("zero stays zero", "atomic_int z = 0;@NL@double_until_even(&z);@NL@CHECK_EQ(atomic_load(&z), 0);", "0 doubled is 0 — the loop must terminate on the zero fixed point."),
            ],
            level="guided",
        ),
        challenge(
            "ca19-release-publish",
            "Publish with Release, Observe with Acquire",
            "ISO C11. Implement the publish pattern: `void publish(atomic_int *flag, atomic_int *data, int payload)` stores payload into data (relaxed), then stores 1 into flag (release). `int observe(const atomic_int *flag, const atomic_int *data)` loads flag with acquire; when it sees 1 it must see the payload — return the data value, or -1 when flag is not yet 1.",
            C_PRELUDE + ATOMICS,
            [
                ("publish then observe", "atomic_int f = 0;@NL@atomic_int d = 0;@NL@publish(&f, &d, 42);@NL@CHECK_EQ(observe(&f, &d), 42);", "Release store to flag synchronizes-with the acquire load: 42 is visible."),
                ("before publish", "atomic_int f2 = 0;@NL@atomic_int d2 = 99;@NL@CHECK_EQ(observe(&f2, &d2), -1);", "flag is still 0 — the observer must report not-ready as -1."),
                ("payload survives republish", "atomic_int f3 = 0;@NL@atomic_int d3 = 0;@NL@publish(&f3, &d3, 7);@NL@publish(&f3, &d3, 9);@NL@CHECK_EQ(observe(&f3, &d3), 9);", "A second publish overwrites; the acquire load observes the newest release."),
            ],
            level="combination",
        ),
        challenge(
            "ca19-padded-counters",
            "Split the Cache Lines",
            "ISO C11 + hardware reality. Two counters sit in one struct: `struct hot { atomic_int a; atomic_int b; };` Given a padded variant `struct padded { atomic_int a; char pad[60]; atomic_int b; };` (sizeof(atomic_int)==4 on this target), implement `int same_line(const void *p, size_t offset_a, size_t offset_b)` — return 1 when the two byte offsets share the same 64-byte cache line, 0 otherwise. Then the checkpoint question: which member offsets in `struct hot` are same-line?",
            C_PRELUDE + ATOMICS + "#include <stddef.h>@NL@",
            [
                ("adjacent members share a line", "struct hot h = {0};@NL@size_t oa = (size_t)((char *)&h.a - (char *)&h);@NL@size_t ob = (size_t)((char *)&h.b - (char *)&h);@NL@CHECK_EQ(same_line(&h, oa, ob), 1);", "4-byte atomics at offsets 0 and 4: same 64-byte line — the false-sharing setup."),
                ("padded members differ", "struct padded p = {0};@NL@size_t pa = (size_t)((char *)&p.a - (char *)&p);@NL@size_t pb = (size_t)((char *)&p.b - (char *)&p);@NL@CHECK_EQ(same_line(&p, pa, pb), 0);", "The 56-byte pad pushes b past offset 64: separate lines."),
                ("same offset is same line", "struct hot h2 = {0};@NL@CHECK_EQ(same_line(&h2, 0, 0), 1);", "An offset against itself is trivially same-line — the degenerate case must not crash."),
            ],
            level="combination",
        ),
    ],
    {
        "ca19-cas-doubling-loop": vi_challenge(
            "Vòng CAS: Nhân đôi đến khi chẵn",
            "ISO C11. Cài `void double_until_even(atomic_int *v)` — lặp nhân đôi `*v` bằng vòng compare-exchange đến khi giá trị mới chẵn. Mọi phép nhân đôi phải qua một CAS atomic (không `*v = *v * 2`).",
            [
                ("nhân đôi số lẻ một lần", "3 nhân đôi là 6 — chẵn nên đúng một vòng CAS."),
                ("đã chẵn vẫn nhân", "4 chẵn nhưng hợp đồng là nhân- rồi-kiểm: 8, một vòng."),
                ("không đổi giữ nguyên", "0 nhân đôi là 0 — vòng lặp phải dừng tại điểm bất động 0."),
            ],
        ),
        "ca19-release-publish": vi_challenge(
            "Publish với Release, quan sát với Acquire",
            "ISO C11. Cài pattern publish: `void publish(...)` store payload vào data (relaxed), rồi store 1 vào flag (release). `int observe(...)` load flag với acquire; khi thấy 1 phải thấy payload — trả giá trị data, hoặc -1 khi flag chưa là 1.",
            [
                ("publish rồi observe", "Release store lên flag synchronizes-with acquire load: 42 hiển thị."),
                ("trước khi publish", "flag vẫn 0 — observer phải báo chưa sẵn sàng bằng -1."),
                ("payload sống qua republish", "Publish thứ hai ghi đè; acquire load thấy release mới nhất."),
            ],
        ),
        "ca19-padded-counters": vi_challenge(
            "Tách cache line",
            "ISO C11 + thực tế phần cứng. Hai counter cùng struct. Cho biến thể có pad 56 byte, cài `int same_line(const void *p, size_t offset_a, size_t offset_b)` — trả 1 khi hai offset byte dùng chung line 64 byte, 0 nếu ngược lại.",
            [
                ("thành viên kề nhau dùng chung line", "Atomic 4 byte tại offset 0 và 4: cùng line 64 byte — kịch bản false sharing."),
                ("thành viên có pad khác line", "Pad 56 byte đẩy b qua offset 64: hai line riêng."),
                ("offset trùng là cùng line", "Offset với chính nó hiển nhiên cùng line — trường hợp suy biến không được crash."),
            ],
        ),
    },
    solutions=[
        (
            "ca19-cas-doubling-loop",
            C_PRELUDE + ATOMICS
            + "void double_until_even(atomic_int *v) {@NL@"
            + "    int old = atomic_load(v);@NL@"
            + "    int next = old * 2;@NL@"
            + "    while (!atomic_compare_exchange_strong(v, &old, next)) {@NL@"
            + "        next = old * 2;@NL@"
            + "    }@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + ATOMICS
            + "void double_until_even(atomic_int *v) {@NL@"
            + "    int old = atomic_load(v);@NL@"
            + "    if (old % 2 == 0) atomic_store(v, old * 2);@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca19-release-publish",
            C_PRELUDE + ATOMICS
            + "void publish(atomic_int *flag, atomic_int *data, int payload) {@NL@"
            + "    atomic_store_explicit(data, payload, memory_order_relaxed);@NL@"
            + "    atomic_store_explicit(flag, 1, memory_order_release);@NL@"
            + "}@NL@"
            + "int observe(const atomic_int *flag, const atomic_int *data) {@NL@"
            + "    if (atomic_load_explicit(flag, memory_order_acquire) != 1) return -1;@NL@"
            + "    return atomic_load(data);@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + ATOMICS
            + "void publish(atomic_int *flag, atomic_int *data, int payload) {@NL@"
            + "    atomic_store_explicit(data, payload, memory_order_relaxed);@NL@"
            + "    atomic_store_explicit(flag, 1, memory_order_relaxed);@NL@"
            + "}@NL@"
            + "int observe(const atomic_int *flag, const atomic_int *data) {@NL@"
            + "    if (atomic_load_explicit(flag, memory_order_relaxed) != 1) return 0;@NL@"
            + "    return atomic_load(data);@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca19-padded-counters",
            C_PRELUDE + ATOMICS + "#include <stddef.h>@NL@"
            + "struct hot {@NL@"
            + "    atomic_int a;@NL@"
            + "    atomic_int b;@NL@"
            + "};@NL@"
            + "struct padded {@NL@"
            + "    atomic_int a;@NL@"
            + "    char pad[60];@NL@"
            + "    atomic_int b;@NL@"
            + "};@NL@"
            + "int same_line(const void *p, size_t offset_a, size_t offset_b) {@NL@"
            + "    if (p == NULL) return -1;@NL@"
            + "    size_t la = offset_a / 64;@NL@"
            + "    size_t lb = offset_b / 64;@NL@"
            + "    return la == lb ? 1 : 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + ATOMICS + "#include <stddef.h>@NL@"
            + "struct hot {@NL@"
            + "    atomic_int a;@NL@"
            + "    atomic_int b;@NL@"
            + "};@NL@"
            + "struct padded {@NL@"
            + "    atomic_int a;@NL@"
            + "    char pad[60];@NL@"
            + "    atomic_int b;@NL@"
            + "};@NL@"
            + "int same_line(const void *p, size_t offset_a, size_t offset_b) {@NL@"
            + "    if (p == NULL) return -1;@NL@"
            + "    size_t la = offset_a / 128;@NL@"
            + "    size_t lb = offset_b / 128;@NL@"
            + "    return la == lb ? 1 : 0;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_checkpoint(
    M19,
    L19CP,
    "Checkpoint: SPSC Ring Buffer Core",
    "The single-producer/single-consumer ring is the smallest honest lock-free design: one producer index, one consumer index, no CAS needed.",
    20,
    "See lesson.",
    "Kiểm tra: Lõi ring buffer SPSC",
    "Ring single-producer/single-consumer là thiết kế lock-free nhỏ nhất: một chỉ số producer, một chỉ số consumer, không cần CAS.",
    "Xem bài học.",
    challenge(
        "ca19-checkpoint-spsc",
        "Checkpoint: SPSC Ring Buffer Core",
        "ISO C11. Given a pre-filled ring state `struct ring { atomic_size_t head; atomic_size_t tail; int buf[8]; }; r` (head/tail both start at 0; empty means head==tail; full means (head+1)%8==tail — one slot sacrificed). Implement `int ring_push(struct ring *r, int v)` (store v at buf[head % 8], then advance head with release ordering; return 0, or -1 when full) and `int ring_pop(struct ring *r, int *out)` (load tail with acquire, check emptiness, read buf[tail % 8] into *out, advance tail relaxed; return 0, or -1 when empty). NULL r (or NULL out for pop) returns -1.",
        C_PRELUDE + ATOMICS
        + "struct ring {@NL@"
        + "    atomic_size_t head;@NL@"
        + "    atomic_size_t tail;@NL@"
        + "    int buf[8];@NL@"
        + "};@NL@"
        + "static struct ring given_ring;@NL@",
        [
            ("push then pop in order", "struct ring r;@NL@atomic_init(&r.head, 0);@NL@atomic_init(&r.tail, 0);@NL@CHECK_EQ(ring_push(&r, 11), 0);@NL@CHECK_EQ(ring_push(&r, 22), 0);@NL@int out1 = -9;@NL@CHECK_EQ(ring_pop(&r, &out1), 0);@NL@CHECK_EQ(out1, 11);@NL@int out2 = -9;@NL@CHECK_EQ(ring_pop(&r, &out2), 0);@NL@CHECK_EQ(out2, 22);", "FIFO: head writes, tail reads — the producer/consumer pair stays in submission order."),
            ("empty pop refuses", "struct ring e;@NL@atomic_init(&e.head, 0);@NL@atomic_init(&e.tail, 0);@NL@int out3 = -9;@NL@CHECK_EQ(ring_pop(&e, &out3), -1);@NL@CHECK_EQ(out3, -9);", "head==tail is empty: pop must refuse and leave *out untouched."),
            ("full push refuses", "struct ring f;@NL@atomic_init(&f.head, 0);@NL@atomic_init(&f.tail, 0);@NL@for (int i = 0; i < 7; i++) {@NL@CHECK_EQ(ring_push(&f, i), 0);@NL@}@NL@CHECK_EQ(ring_push(&f, 99), -1);", "One slot is sacrificed to distinguish full from empty: the 8th push must fail."),
            ("NULL guard", "CHECK_EQ(ring_push(NULL, 1), -1);@NL@int out4 = 0;@NL@CHECK_EQ(ring_pop(NULL, &out4), -1);", "A NULL ring is a caller-contract violation: refuse, never dereference."),
        ],
        level="capstone",
    ),
    {
        "ca19-checkpoint-spsc": vi_challenge(
            "Kiểm tra: Lõi ring buffer SPSC",
            "ISO C11. Cho struct ring với head/tail atomic (empty: head==tail; full: (head+1)%8==tail — hi sinh một ô). Cài `ring_push` (ghi buf[head%8] rồi tăng head với release; 0 hoặc -1 khi đầy) và `ring_pop` (load tail với acquire, kiểm tra rỗng, đọc buf[tail%8] vào *out, tăng tail relaxed; 0 hoặc -1 khi rỗng). NULL trả -1.",
            [
                ("push rồi pop theo thứ tự", "FIFO: head ghi, tail đọc — cặp producer/consumer giữ thứ tự nạp."),
                ("pop khi rỗng từ chối", "head==tail là rỗng: pop phải từ chối và không đụng *out."),
                ("push khi đầy từ chối", "Một ô bị hi sinh để phân biệt đầy với rỗng: lần push thứ 8 phải thất bại."),
                ("chặn NULL", "NULL là vi phạm hợp đồng: từ chối, không bao giờ dereference."),
            ],
        ),
    },
    solution=
    C_PRELUDE + ATOMICS
    + "struct ring {@NL@"
    + "    atomic_size_t head;@NL@"
    + "    atomic_size_t tail;@NL@"
    + "    int buf[8];@NL@"
    + "};@NL@"
    + "static struct ring given_ring;@NL@"
    + "int ring_push(struct ring *r, int v) {@NL@"
    + "    if (r == NULL) return -1;@NL@"
    + "    size_t h = atomic_load_explicit(&r->head, memory_order_relaxed);@NL@"
    + "    if ((h + 1) % 8 == atomic_load_explicit(&r->tail, memory_order_acquire)) return -1;@NL@"
    + "    r->buf[h % 8] = v;@NL@"
    + "    atomic_store_explicit(&r->head, h + 1, memory_order_release);@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "int ring_pop(struct ring *r, int *out) {@NL@"
    + "    if (r == NULL || out == NULL) return -1;@NL@"
    + "    size_t t = atomic_load_explicit(&r->tail, memory_order_acquire);@NL@"
    + "    if (t == atomic_load_explicit(&r->head, memory_order_acquire)) return -1;@NL@"
    + "    *out = r->buf[t % 8];@NL@"
    + "    atomic_store_explicit(&r->tail, t + 1, memory_order_relaxed);@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
    wrong=
    C_PRELUDE + ATOMICS
    + "struct ring {@NL@"
    + "    atomic_size_t head;@NL@"
    + "    atomic_size_t tail;@NL@"
    + "    int buf[8];@NL@"
    + "};@NL@"
    + "static struct ring given_ring;@NL@"
    + "int ring_push(struct ring *r, int v) {@NL@"
    + "    if (r == NULL) return -1;@NL@"
    + "    size_t h = atomic_load_explicit(&r->head, memory_order_relaxed);@NL@"
    + "    if ((h + 1) % 8 == atomic_load_explicit(&r->tail, memory_order_acquire)) return -1;@NL@"
    + "    r->buf[h % 8] = v;@NL@"
    + "    atomic_store_explicit(&r->head, h + 1, memory_order_relaxed);@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "int ring_pop(struct ring *r, int *out) {@NL@"
    + "    if (r == NULL || out == NULL) return -1;@NL@"
    + "    size_t h = atomic_load_explicit(&r->head, memory_order_relaxed);@NL@"
    + "    if (h == atomic_load_explicit(&r->tail, memory_order_acquire)) return -1;@NL@"
    + "    *out = r->buf[(h - 1) % 8];@NL@"
    + "    atomic_store_explicit(&r->head, h - 1, memory_order_relaxed);@NL@"
    + "    return 0;@NL@"
    + "}@NL@"
    + "int main(void) { return 0; }",
)

# ================= MODULE 20: ca-sockets =====================================
M20 = "ca-sockets"

L20A = "ca-tcp-echo"
L20B = "ca-framing-timeouts"
L20CP = "ca-checkpoint-m20"

write_module(
    M20,
    "Loopback Sockets: TCP, UDP, Framing",
    "Sockets against 127.0.0.1 in the sandbox: connection lifecycle, byte-stream framing, timeouts, and UDP datagrams. POSIX/BSD sockets — never part of ISO C; labeled as such.",
    "Socket loopback: TCP, UDP, đóng khung",
    "Socket qua 127.0.0.1 trong sandbox: vòng đời kết nối, đóng khung byte-stream, timeout, và datagram UDP. Socket POSIX/BSD — không bao giờ thuộc ISO C; ghi nhãn rõ ràng.",
    [L20A, L20B, L20CP],
    ["ca-p20-sockets"],
)

write_lesson(
    M20,
    L20A,
    "The TCP Loopback Lifecycle",
    "Every server is the same six calls; the sandbox's loopback is where they are safe to practice.",
    20,
    """
## The six calls

```c
#define _POSIX_C_SOURCE 200809L
#include <sys/socket.h>       /* POSIX */
#include <netinet/in.h>       /* POSIX */
#include <arpa/inet.h>        /* POSIX */

int lfd = socket(AF_INET, SOCK_STREAM, 0);
struct sockaddr_in sa = {0};
sa.sin_family = AF_INET;
sa.sin_addr.s_addr = htonl(INADDR_LOOPBACK);  /* 127.0.0.1 only */
sa.sin_port = 0;                              /* 0 = kernel assigns */
bind(lfd, (struct sockaddr *)&sa, sizeof sa);
listen(lfd, 16);
int cfd = accept(lfd, NULL, NULL);            /* blocks until connect */
```

The client mirrors it: `socket` then `connect` to the same `sockaddr_in`. Reading and writing on `cfd` is `recv`/`send` — the same bytes cross the loopback interface without touching a network.

**Port 0 is the sandbox superpower.** Binding to port 0 makes the kernel hand you a free ephemeral port; `getsockname` reports which. No fixed port means no collisions between parallel test runs — every challenge here uses this pattern.

## TCP is a byte stream, not a message bus

`send(s, "hello", 5, 0)` does not create a "hello message". TCP may deliver those 5 bytes glued to the next send's bytes (coalescing) or split them (fragmentation). The receiver's `recv` returns *whatever is in the pipe* — 1 byte, 5, or 50 from three different sends.

This single fact motivates every protocol ever built on TCP:

- **Delimiter framing**: newline-terminated lines (HTTP/1, SMTP) — scan for the byte.
- **Length-prefix framing**: a fixed-width count then exactly that many bytes (HTTP/2, most binary protocols) — read the count, then read the count's worth.

## Half-close is a feature

`shutdown(cfd, SHUT_WR)` sends EOF in the client→server direction while keeping the server→client direction open. A `recv` returning 0 means the peer closed *its* write side — that is how a server learns "the request is complete" without closing the response path. Note the contrast: `recv == 0` is orderly EOF; `recv < 0` with `errno == EAGAIN` means "nothing yet" when the socket is non-blocking or timeout-armed.

## Honesty labels

- **ISO C**: none of this. `<stdio.h>` knows no sockets.
- **POSIX**: everything above — the feature macro is not decoration; without it musl/glibc hide the declarations.
- **Sandbox**: loopback only (`--network none` verified). External hosts are unreachable by design; code that must reach them belongs to a real environment, not this course.
""",
    "Vòng đời TCP loopback",
    "Mọi server là cùng sáu lời gọi; loopback của sandbox là nơi an toàn để luyện chúng.",
    """
## Sáu lời gọi

```c
#define _POSIX_C_SOURCE 200809L
#include <sys/socket.h>       /* POSIX */
#include <netinet/in.h>       /* POSIX */
#include <arpa/inet.h>        /* POSIX */

int lfd = socket(AF_INET, SOCK_STREAM, 0);
struct sockaddr_in sa = {0};
sa.sin_family = AF_INET;
sa.sin_addr.s_addr = htonl(INADDR_LOOPBACK);  /* chỉ 127.0.0.1 */
sa.sin_port = 0;                              /* 0 = kernel cấp */
bind(lfd, (struct sockaddr *)&sa, sizeof sa);
listen(lfd, 16);
int cfd = accept(lfd, NULL, NULL);            /* chặn đến khi connect */
```

Phía client đối xứng: `socket` rồi `connect` tới cùng `sockaddr_in`. Đọc/ghi trên `cfd` là `recv`/`send` — cùng byte đi qua giao diện loopback, không chạm mạng nào.

**Port 0 là siêu năng lực của sandbox.** Bind port 0 khiến kernel cấp một port ephemeral rảnh; `getsockname` báo port nào. Không port cố định nghĩa không xung đột giữa các lần chạy test song song — mọi challenge ở đây dùng pattern này.

## TCP là byte stream, không phải bus tin nhắn

`send(s, "hello", 5, 0)` không tạo ra "tin nhắn hello". TCP có thể dán 5 byte đó vào byte của lần send kế (coalescing) hoặc cắt nhỏ chúng (fragmentation). `recv` của máy nhận trả về *bất cứ gì trong ống* — 1 byte, 5, hoặc 50 từ ba lần send khác nhau.

Một sự thật này sinh ra mọi protocol xây trên TCP:

- **Đóng khung bằng delimiter**: dòng kết thúc bằng newline (HTTP/1, SMTP) — quét tìm byte đó.
- **Đóng khung bằng length-prefix**: một số đếm độ rộng cố định rồi đúng bấy nhiêu byte (HTTP/2, đa số protocol nhị phân) — đọc số đếm, rồi đọc đúng số byte đó.

## Half-close là một tính năng

`shutdown(cfd, SHUT_WR)` gửi EOF theo hướng client→server trong khi giữ hướng server→client. `recv` trả 0 nghĩa là peer đã đóng *phía ghi của nó* — đó là cách server biết "request đã xong" mà không đóng đường trả lời. Phân biệt: `recv == 0` là EOF trật tự; `recv < 0` với `errno == EAGAIN` là "chưa có gì" khi socket non-blocking hoặc có timeout.

## Nhãn trung thực

- **ISO C**: không có gì trong số này. `<stdio.h>` không biết socket.
- **POSIX**: tất cả ở trên — feature macro không phải trang trí; thiếu nó musl/glibc ẩn các khai báo.
- **Sandbox**: chỉ loopback (`--network none` đã kiểm chứng). Host ngoài không with tới by design; code phải tới host ngoài thuộc môi trường thật, không thuộc khóa học này.
""",
)

write_lesson(
    M20,
    L20B,
    "Framing, Timeouts, and UDP Datagrams",
    "Turning a byte stream into messages, bounding waits, and knowing when UDP's no-guarantees model is the right one.",
    20,
    """
## Length-prefix framing on a stream

A 4-byte big-endian length then the payload is the classic binary envelope:

```c
/* sender */
uint32_t n = htonl((uint32_t)len);
send(cfd, &n, 4, 0);
send(cfd, payload, len, 0);

/* receiver: loop until you have exactly 4, decode, then loop until len */
```

The receiver **must** loop: a single `recv(fd, buf, 4, 0)` may return 1, 2, or 3 bytes. "Read exactly N" is a loop around recv, accumulating into a buffer — write it once, use it forever.

## Bounding waits with SO_RCVTIMEO

A blocking `recv` on a socket that never receives hangs forever. `SO_RCVTIMEO` bounds the wait:

```c
struct timeval tv = { .tv_sec = 0, .tv_usec = 200000 };  /* 200 ms */
setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof tv);

ssize_t n = recv(fd, buf, sizeof buf, 0);
if (n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
    /* timed out with no data — retry, log, or give up */
}
```

Verified on this image: an idle UDP socket with a 200 ms timeout returns -1/`EAGAIN`. Timeouts turn "hang" into an error you can handle — the same idea `poll()` generalizes.

## UDP: messages, unguaranteed

UDP preserves **message boundaries** — one `sendto`, one `recvfrom`, no coalescing — and guarantees nothing else: no delivery, no order, no duplicates-removed. On loopback, delivery is reliable in practice, which makes it honest practice ground for the API without pretending the internet behaves the same.

```c
sendto(ufd, "ping", 4, 0, (struct sockaddr *)&dest, sizeof dest);
ssize_t n = recvfrom(ufd, buf, sizeof buf, 0, (struct sockaddr *)&from, &fromlen);
```

`recvfrom` also hands back the sender's address — the piece a UDP server needs to reply.

## Choosing honestly

- Need every byte, in order, with congestion control: **TCP**.
- Need message boundaries, can tolerate loss, want minimum latency: **UDP** (DNS, games, telemetry).
- Need both message boundaries *and* reliability: TCP plus a framing layer, or a protocol that already did that for you.

All of it: POSIX, loopback here, labeled as such.
""",
    "Đóng khung, timeout, và UDP",
    "Biến byte stream thành tin nhắn, giới hạn thời gian chờ, và biết khi nào mô hình không-đảm-bảo của UDP là lựa chọn đúng.",
    """
## Đóng khung length-prefix trên stream

Một số đếm 4-byte big-endian rồi payload là phong bì nhị phân kinh điển:

```c
/* phía gửi */
uint32_t n = htonl((uint32_t)len);
send(cfd, &n, 4, 0);
send(cfd, payload, len, 0);

/* phía nhận: lặp đến khi có đủ 4, giải mã, rồi lặp đến khi đủ len */
```

Máy nhận **phải** lặp: một `recv(fd, buf, 4, 0)` có thể trả 1, 2, hoặc 3 byte. "Đọc đúng N" là một vòng lặp quanh recv, tích lũy vào buffer — viết một lần, dùng mãi mãi.

## Chặn thời gian chờ với SO_RCVTIMEO

`recv` chặn trên socket không bao giờ nhận sẽ treo vĩnh viễn. `SO_RCVTIMEO` chặn thời gian chờ:

```c
struct timeval tv = { .tv_sec = 0, .tv_usec = 200000 };  /* 200 ms */
setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof tv);

ssize_t n = recv(fd, buf, sizeof buf, 0);
if (n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
    /* hết giờ không có dữ liệu — thử lại, log, hoặc bỏ cuộc */
}
```

Đã kiểm chứng trên ảnh này: socket UDP nhàn rỗi với timeout 200 ms trả -1/`EAGAIN`. Timeout biến "treo" thành lỗi xử lý được — cùng tư tưởng mà `poll()` khái quát hóa.

## UDP: tin nhắn, không đảm bảo

UDP giữ **biên tin nhắn** — một `sendto`, một `recvfrom`, không coalescing — và không đảm bảo gì khác: không giao hàng, không thứ tự, không khử trùng lặp. Trên loopback, giao hàng đáng tin trong thực tế — sân tập trung thực cho API mà không giả vờ internet behaves tương tự.

```c
sendto(ufd, "ping", 4, 0, (struct sockaddr *)&dest, sizeof dest);
ssize_t n = recvfrom(ufd, buf, sizeof buf, 0, (struct sockaddr *)&from, &fromlen);
```

`recvfrom` còn trả về địa chỉ người gửi — mảnh mà server UDP cần để trả lời.

## Chọn cách trung thực

- Cần từng byte, đúng thứ tự, có kiểm soát nghẽn: **TCP**.
- Cần biên tin nhắn, chịu được mất mát, muốn độ trễ tối thiểu: **UDP** (DNS, game, telemetry).
- Cần cả biên tin nhắn *lẫn* độ tin cậy: TCP cộng lớp đóng khung, hoặc một protocol đã làm sẵn điều đó.

Tất cả: POSIX, loopback tại đây, ghi nhãn rõ ràng.
""",
)

write_practice(
    M20,
    "ca-p20-sockets",
    "Socket Drills on Loopback",
    "Server/client pairs, exact-read framing, and timeout discipline — all on the sandbox's verified loopback.",
    "Bài tập socket trên loopback",
    "Cặp server/client, đóng khung đọc-đúng, và kỷ luật timeout — tất cả trên loopback đã kiểm chứng của sandbox.",
    L20A,
    26,
    "advanced",
    [
        challenge(
            "ca20-sockaddr-encode",
            "Encode the Loopback Address",
            "POSIX. Implement `void fill_loopback(struct sockaddr_in *sa, int port)` — zero the struct, set family AF_INET, address to INADDR_LOOPBACK (network byte order), and port (network byte order). Then implement `int decode_port(const struct sockaddr_in *sa)` returning the host-order port. NULL sa returns -1 from decode_port and does nothing in fill.",
            C_PRELUDE + POSIX,
            [
                ("roundtrip port", "struct sockaddr_in s1;@NL@fill_loopback(&s1, 8080);@NL@CHECK_EQ(decode_port(&s1), 8080);", "htons on the way in, ntohs on the way out — the byte order cancels."),
                ("loopback address set", "struct sockaddr_in s2;@NL@fill_loopback(&s2, 1);@NL@CHECK_EQ(s2.sin_addr.s_addr, htonl(INADDR_LOOPBACK));", "INADDR_LOOPBACK is 127.0.0.1 — stored in network byte order exactly as given."),
                ("zeroed padding and family", "struct sockaddr_in s3;@NL@memset(&s3, 0xAB, sizeof s3);@NL@fill_loopback(&s3, 9);@NL@CHECK_EQ(s3.sin_family, AF_INET);", "A memset-poisoned struct must come out clean: the contract says zero the struct first."),
                ("NULL guard", "CHECK_EQ(decode_port(NULL), -1);", "NULL is a caller bug: refuse with -1, never dereference."),
            ],
            level="guided",
        ),
        challenge(
            "ca20-exact-read",
            "Read Exactly N Bytes",
            "POSIX. Implement `ssize_t read_exact(int fd, void *buf, size_t n)` — loop recv until exactly n bytes are accumulated; return n, or -1 on EOF-before-complete (peer closed mid-message), error, or NULL/zero-argument misuse (n==0 returns 0 immediately). Partial data stays in buf on failure — the tests only check return values.",
            C_PRELUDE + POSIX,
            [
                ("complete read", "int sv[2];@NL@CHECK_EQ(socketpair(AF_UNIX, SOCK_STREAM, 0, sv), 0);@NL@CHECK_EQ((int)send(sv[0], @T10@, 3, 0), 3);@NL@char b1[8] = {0};@NL@CHECK_EQ(read_exact(sv[1], b1, 3), 3);@NL@close(sv[0]);@NL@close(sv[1]);", "3 bytes arrive; read_exact returns 3 after one recv — the trivial case."),
                ("split delivery", "int sv2[2];@NL@CHECK_EQ(socketpair(AF_UNIX, SOCK_STREAM, 0, sv2), 0);@NL@CHECK_EQ((int)send(sv2[0], @T10@, 1, 0), 1);@NL@CHECK_EQ((int)send(sv2[0], @T10@, 1, 0), 1);@NL@CHECK_EQ((int)send(sv2[0], @T10@, 1, 0), 1);@NL@char b2[8] = {0};@NL@CHECK_EQ(read_exact(sv2[1], b2, 3), 3);@NL@close(sv2[0]);@NL@close(sv2[1]);", "Three 1-byte sends: the loop must keep recv-ing until 3 accumulate."),
                ("EOF before complete", "int sv3[2];@NL@CHECK_EQ(socketpair(AF_UNIX, SOCK_STREAM, 0, sv3), 0);@NL@CHECK_EQ((int)send(sv3[0], @T10@, 1, 0), 1);@NL@close(sv3[0]);@NL@char b3[8] = {0};@NL@CHECK_EQ(read_exact(sv3[1], b3, 3), -1);@NL@close(sv3[1]);", "1 byte then EOF: a message cut short is an error, not a success."),
                ("zero is immediate", "int sv4[2];@NL@CHECK_EQ(socketpair(AF_UNIX, SOCK_STREAM, 0, sv4), 0);@NL@char b4[1] = {0};@NL@CHECK_EQ(read_exact(sv4[1], b4, 0), 0);@NL@close(sv4[0]);@NL@close(sv4[1]);", "n==0 asks for nothing: return 0 without touching the socket."),
            ],
            level="combination",
        ),
        challenge(
            "ca20-udp-roundtrip",
            "UDP Send and Receive",
            "POSIX. Implement `ssize_t udp_roundtrip(int ufd, const char *msg, char *out, size_t cap)` — sendto msg to the loopback address and the socket's OWN bound port (getsockname), then recvfrom into out (at most cap-1 bytes, NUL-terminated) and return the byte count, or -1 on any failure (NULL args, cap 0). Bind ufd to port 0 before calling — the tests do.",
            C_PRELUDE + POSIX,
            [
                ("echo to self", "int u1 = socket(AF_INET, SOCK_DGRAM, 0);@NL@struct sockaddr_in a1;@NL@memset(&a1, 0, sizeof a1);@NL@a1.sin_family = AF_INET;@NL@a1.sin_addr.s_addr = htonl(INADDR_LOOPBACK);@NL@a1.sin_port = 0;@NL@CHECK_EQ(bind(u1, (struct sockaddr *)&a1, sizeof a1), 0);@NL@char o1[32] = {0};@NL@CHECK_EQ(udp_roundtrip(u1, @T9@, o1, 32), 1);@NL@CHECK_EQ(o1[0], 120);@NL@close(u1);", "The datagram leaves and returns through the loopback: one byte, value 'x'."),
                ("message boundary kept", "int u2 = socket(AF_INET, SOCK_DGRAM, 0);@NL@struct sockaddr_in a2;@NL@memset(&a2, 0, sizeof a2);@NL@a2.sin_family = AF_INET;@NL@a2.sin_addr.s_addr = htonl(INADDR_LOOPBACK);@NL@a2.sin_port = 0;@NL@CHECK_EQ(bind(u2, (struct sockaddr *)&a2, sizeof a2), 0);@NL@char o2[32] = {0};@NL@CHECK_EQ(udp_roundtrip(u2, @T6@, o2, 32), 8);@NL@CHECK_EQ(o2[7], 'k');@NL@close(u2);", "UDP preserves message boundaries: the whole 8-byte word arrives as one datagram."),
                ("NULL message refused", "int u3 = socket(AF_INET, SOCK_DGRAM, 0);@NL@char o3[8] = {0};@NL@CHECK_EQ(udp_roundtrip(u3, NULL, o3, 8), -1);@NL@close(u3);", "NULL msg is a contract violation: -1, no send."),
            ],
            level="combination",
        ),
    ],
    {
        "ca20-sockaddr-encode": vi_challenge(
            "Mã hóa địa chỉ loopback",
            "POSIX. Cài `void fill_loopback(struct sockaddr_in *sa, int port)` — zero struct, đặt family AF_INET, địa chỉ INADDR_LOOPBACK (network byte order), và port (network byte order). Rồi `int decode_port(const struct sockaddr_in *sa)` trả port theo host order. NULL: decode trả -1, fill không làm gì.",
            [
                ("roundtrip port", "htons lúc vào, ntohs lúc ra — thứ tự byte triệt tiêu."),
                ("địa chỉ loopback", "INADDR_LOOPBACK là 127.0.0.1 — lưu theo network byte order đúng như cho."),
                ("zero hóa padding và family", "Struct bị memset đầu độc phải ra sạch: hợp đồng nói zero struct trước."),
                ("chặn NULL", "NULL là lỗi người gọi: từ chối bằng -1, không dereference."),
            ],
        ),
        "ca20-exact-read": vi_challenge(
            "Đọc đúng N byte",
            "POSIX. Cài `ssize_t read_exact(int fd, void *buf, size_t n)` — lặp recv đến khi tích đủ n byte; trả n, hoặc -1 khi EOF trước khi đủ, lỗi, hoặc NULL (n==0 trả 0 ngay).",
            [
                ("đọc trọn vẹn", "3 byte đến; read_exact trả 3 sau một recv — trường hợp tầm thường."),
                ("giao phân mảnh", "Ba lần gửi 1 byte: vòng lặp phải recv tiếp đến khi đủ 3."),
                ("EOF trước khi đủ", "1 byte rồi EOF: tin nhắn bị cắt là lỗi, không phải thành công."),
                ("không là ngay lập tức", "n==0 không xin gì: trả 0 không đụng socket."),
            ],
        ),
        "ca20-udp-roundtrip": vi_challenge(
            "UDP gửi và nhận",
            "POSIX. Cài `ssize_t udp_roundtrip(int ufd, const char *msg, char *out, size_t cap)` — sendto msg tới địa chỉ loopback và chính port đã bind của socket (getsockname), rồi recvfrom vào out (tối đa cap-1 byte, kết thúc NUL) và trả số byte, hoặc -1 khi bất kỳ lỗi nào.",
            [
                ("echo về chính mình", "Datagram đi rồi về qua loopback: một byte, giá trị 'x'."),
                ("biên tin nhắn được giữ", "UDP giữ biên tin nhắn: cả từ 8 byte đến như một datagram."),
                ("tin nhắn NULL bị từ chối", "NULL msg là vi phạm hợp đồng: -1, không gửi."),
            ],
        ),
    },
    solutions=[
        (
            "ca20-sockaddr-encode",
            C_PRELUDE + POSIX
            + "void fill_loopback(struct sockaddr_in *sa, int port) {@NL@"
            + "    if (sa == NULL) return;@NL@"
            + "    memset(sa, 0, sizeof *sa);@NL@"
            + "    sa->sin_family = AF_INET;@NL@"
            + "    sa->sin_addr.s_addr = htonl(INADDR_LOOPBACK);@NL@"
            + "    sa->sin_port = htons((unsigned short)port);@NL@"
            + "}@NL@"
            + "int decode_port(const struct sockaddr_in *sa) {@NL@"
            + "    if (sa == NULL) return -1;@NL@"
            + "    return (int)ntohs(sa->sin_port);@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + POSIX
            + "void fill_loopback(struct sockaddr_in *sa, int port) {@NL@"
            + "    if (sa == NULL) return;@NL@"
            + "    memset(sa, 0, sizeof *sa);@NL@"
            + "    sa->sin_family = AF_INET;@NL@"
            + "    sa->sin_addr.s_addr = htonl(INADDR_LOOPBACK);@NL@"
            + "    sa->sin_port = (unsigned short)port;@NL@"
            + "}@NL@"
            + "int decode_port(const struct sockaddr_in *sa) {@NL@"
            + "    if (sa == NULL) return -1;@NL@"
            + "    return (int)ntohs(sa->sin_port);@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca20-exact-read",
            C_PRELUDE + POSIX
            + "ssize_t read_exact(int fd, void *buf, size_t n) {@NL@"
            + "    if (buf == NULL && n > 0) return -1;@NL@"
            + "    if (n == 0) return 0;@NL@"
            + "    char *p = (char *)buf;@NL@"
            + "    size_t got = 0;@NL@"
            + "    while (got < n) {@NL@"
            + "        ssize_t r = recv(fd, p + got, n - got, 0);@NL@"
            + "        if (r == 0) return -1;@NL@"
            + "        if (r < 0) return -1;@NL@"
            + "        got += (size_t)r;@NL@"
            + "    }@NL@"
            + "    return (ssize_t)n;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + POSIX
            + "ssize_t read_exact(int fd, void *buf, size_t n) {@NL@"
            + "    if (buf == NULL && n > 0) return -1;@NL@"
            + "    if (n == 0) return -1;@NL@"
            + "    char *p = (char *)buf;@NL@"
            + "    ssize_t r = recv(fd, p, n, 0);@NL@"
            + "    if (r <= 0) return 0;@NL@"
            + "    return r - 1;@NL@"
            + "    return (ssize_t)n;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
        (
            "ca20-udp-roundtrip",
            C_PRELUDE + POSIX
            + "ssize_t udp_roundtrip(int ufd, const char *msg, char *out, size_t cap) {@NL@"
            + "    if (ufd < 0 || msg == NULL || out == NULL || cap == 0) return -1;@NL@"
            + "    struct sockaddr_in self;@NL@"
            + "    socklen_t sl = sizeof self;@NL@"
            + "    if (getsockname(ufd, (struct sockaddr *)&self, &sl) != 0) return -1;@NL@"
            + "    size_t mlen = strlen(msg);@NL@"
            + "    if (sendto(ufd, msg, mlen, 0, (struct sockaddr *)&self, sizeof self) != (ssize_t)mlen) return -1;@NL@"
            + "    ssize_t n = recvfrom(ufd, out, cap - 1, 0, NULL, NULL);@NL@"
            + "    if (n < 0) return -1;@NL@"
            + "    out[n] = 0;@NL@"
            + "    return n;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
            C_PRELUDE + POSIX
            + "ssize_t udp_roundtrip(int ufd, const char *msg, char *out, size_t cap) {@NL@"
            + "    if (ufd < 0 || msg == NULL || out == NULL || cap == 0) return -1;@NL@"
            + "    struct sockaddr_in self;@NL@"
            + "    socklen_t sl = sizeof self;@NL@"
            + "    if (getsockname(ufd, (struct sockaddr *)&self, &sl) != 0) return -1;@NL@"
            + "    size_t mlen = strlen(msg);@NL@"
            + "    if (sendto(ufd, msg, mlen, 0, (struct sockaddr *)&self, sizeof self) != (ssize_t)mlen) return -1;@NL@"
            + "    ssize_t n = recvfrom(ufd, out, cap - 1, 0, NULL, NULL);@NL@"
            + "    if (n < 0) return -1;@NL@"
            + "    out[0] = 0;@NL@"
            + "    return mlen;@NL@"
            + "}@NL@"
            + "int main(void) { return 0; }",
        ),
    ],
)

write_checkpoint(
    M20,
    L20CP,
    "Checkpoint: Echo Server Core",
    "The module in one program: a threaded TCP echo server over loopback, plus a client that verifies the round trip.",
    22,
    "See lesson.",
    "Kiểm tra: Lõi echo server",
    "Cả mô-đun trong một chương trình: threaded TCP echo server trên loopback, cùng client kiểm chứng vòng lặp.",
    "Xem bài học.",
    challenge(
        "ca20-checkpoint-echo",
        "Checkpoint: Echo Server Core",
        "POSIX. Implement `int echo_serve(int lfd)` — accept ONE connection on the already-bound/listening socket lfd, echo every byte received back to the client until the client half-closes (recv returns 0), close the connection, and return 0 (-1 on accept failure). The tests build a loopback listener, run echo_serve on a thread, connect, send, verify the echo, and half-close.",
        C_PRELUDE + POSIX + THREADS
        + "struct serve_arg {@NL@"
        + "    int lfd;@NL@"
        + "};@NL@"
        + "static void *serve_thread(void *arg) {@NL@"
        + "    struct serve_arg *a = (struct serve_arg *)arg;@NL@"
        + "    echo_serve(a->lfd);@NL@"
        + "    return NULL;@NL@"
        + "};@NL@"
        + "static int make_loopback_listener(void) {@NL@"
        + "    int fd = socket(AF_INET, SOCK_STREAM, 0);@NL@"
        + "    if (fd < 0) return -1;@NL@"
        + "    struct sockaddr_in sa;@NL@"
        + "    memset(&sa, 0, sizeof sa);@NL@"
        + "    sa.sin_family = AF_INET;@NL@"
        + "    sa.sin_addr.s_addr = htonl(INADDR_LOOPBACK);@NL@"
        + "    sa.sin_port = 0;@NL@"
        + "    if (bind(fd, (struct sockaddr *)&sa, sizeof sa) != 0) { close(fd); return -1; }@NL@"
        + "    if (listen(fd, 16) != 0) { close(fd); return -1; }@NL@"
        + "    return fd;@NL@"
        + "};@NL@"
        + "static int connect_to_listener(int lfd) {@NL@"
        + "    struct sockaddr_in sa;@NL@"
        + "    socklen_t sl = sizeof sa;@NL@"
        + "    if (getsockname(lfd, (struct sockaddr *)&sa, &sl) != 0) return -1;@NL@"
        + "    int cfd = socket(AF_INET, SOCK_STREAM, 0);@NL@"
        + "    if (cfd < 0) return -1;@NL@"
        + "    if (connect(cfd, (struct sockaddr *)&sa, sizeof sa) != 0) { close(cfd); return -1; }@NL@"
        + "    return cfd;@NL@"
        + "};@NL@",
        [
            ("echo roundtrip", "int lf = make_loopback_listener();@NL@pthread_t t;@NL@struct serve_arg sa = { lf };@NL@CHECK_EQ(pthread_create(&t, NULL, serve_thread, &sa), 0);@NL@int cf = connect_to_listener(lf);@NL@const char *m = @T1@;@NL@CHECK_EQ((int)send(cf, m, strlen(m), 0), (int)strlen(m));@NL@char b[64] = {0};@NL@size_t got = 0;@NL@while (got < strlen(m)) {@NL@ssize_t r = recv(cf, b + got, sizeof b - got - 1, 0);@NL@if (r <= 0) break;@NL@got += (size_t)r;@NL@}@NL@shutdown(cf, SHUT_WR);@NL@pthread_join(t, NULL);@NL@CHECK(got == strlen(m));@NL@CHECK(strstr(b, @T2@) != NULL);@NL@close(cf);@NL@close(lf);", "Every sent byte comes back: echo semantics over one loopback connection."),
            ("empty stream tolerated", "int lf2 = make_loopback_listener();@NL@pthread_t t2;@NL@struct serve_arg sa2 = { lf2 };@NL@CHECK_EQ(pthread_create(&t2, NULL, serve_thread, &sa2), 0);@NL@int cf2 = connect_to_listener(lf2);@NL@shutdown(cf2, SHUT_WR);@NL@pthread_join(t2, NULL);@NL@close(cf2);@NL@close(lf2);", "A client that says nothing and closes: the server sees EOF immediately and finishes cleanly."),
            ("bad fd refused", "CHECK_EQ(echo_serve(-1), -1);", "accept on an invalid descriptor fails: -1, no crash."),
        ],
        level="capstone",
    ),
    {
        "ca20-checkpoint-echo": vi_challenge(
            "Kiểm tra: Lõi echo server",
            "POSIX. Cài `int echo_serve(int lfd)` — accept MỘT kết nối trên socket đã bind/listen lfd, echo mọi byte nhận được về client cho đến khi client half-close (recv trả 0), đóng kết nối, và trả 0 (-1 khi accept thất bại).",
            [
                ("vòng lặp echo", "Mọi byte gửi đi đều quay về: ngữ nghĩa echo trên một kết nối loopback."),
                ("stream rỗng được chấp nhận", "Client không nói gì và đóng: server thấy EOF ngay và kết thúc sạch."),
                ("fd xấu bị từ chối", "accept trên descriptor không hợp lệ thất bại: -1, không crash."),
            ],
        ),
    },
    solution=
    C_PRELUDE + POSIX + THREADS
    + "struct serve_arg {@NL@"
    + "    int lfd;@NL@"
    + "};@NL@"
    + "static int make_loopback_listener(void) {@NL@"
    + "    int fd = socket(AF_INET, SOCK_STREAM, 0);@NL@"
    + "    if (fd < 0) return -1;@NL@"
    + "    struct sockaddr_in sa;@NL@"
    + "    memset(&sa, 0, sizeof sa);@NL@"
    + "    sa.sin_family = AF_INET;@NL@"
    + "    sa.sin_addr.s_addr = htonl(INADDR_LOOPBACK);@NL@"
    + "    sa.sin_port = 0;@NL@"
    + "    if (bind(fd, (struct sockaddr *)&sa, sizeof sa) != 0) { close(fd); return -1; }@NL@"
    + "    if (listen(fd, 16) != 0) { close(fd); return -1; }@NL@"
    + "    return fd;@NL@"
    + "};@NL@"
    + "static int connect_to_listener(int lfd) {@NL@"
    + "    struct sockaddr_in sa;@NL@"
    + "    socklen_t sl = sizeof sa;@NL@"
    + "    if (getsockname(lfd, (struct sockaddr *)&sa, &sl) != 0) return -1;@NL@"
    + "    int cfd = socket(AF_INET, SOCK_STREAM, 0);@NL@"
    + "    if (cfd < 0) return -1;@NL@"
    + "    if (connect(cfd, (struct sockaddr *)&sa, sizeof sa) != 0) { close(cfd); return -1; }@NL@"
    + "    return cfd;@NL@"
    + "};@NL@"
    + "int echo_serve(int lfd) {@NL@"
    + "    if (lfd < 0) return -1;@NL@"
    + "    int cfd = accept(lfd, NULL, NULL);@NL@"
    + "    if (cfd < 0) return -1;@NL@"
    + "    char buf[256];@NL@"
    + "    ssize_t n;@NL@"
    + "    while ((n = recv(cfd, buf, sizeof buf, 0)) > 0) {@NL@"
    + "        ssize_t off = 0;@NL@"
    + "        while (off < n) {@NL@"
    + "            ssize_t w = send(cfd, buf + off, (size_t)(n - off), 0);@NL@"
    + "            if (w <= 0) break;@NL@"
    + "            off += w;@NL@"
    + "        }@NL@"
    + "    }@NL@"
    + "    close(cfd);@NL@"
    + "    return 0;@NL@"
    + "};@NL@"
    + "static void *serve_thread(void *arg) {@NL@"
    + "    struct serve_arg *a = (struct serve_arg *)arg;@NL@"
    + "    echo_serve(a->lfd);@NL@"
    + "    return NULL;@NL@"
    + "};@NL@"
    + "int main(void) { return 0; }@NL@",
    wrong=
    C_PRELUDE + POSIX + THREADS
    + "struct serve_arg {@NL@"
    + "    int lfd;@NL@"
    + "};@NL@"
    + "static int make_loopback_listener(void) {@NL@"
    + "    int fd = socket(AF_INET, SOCK_STREAM, 0);@NL@"
    + "    if (fd < 0) return -1;@NL@"
    + "    struct sockaddr_in sa;@NL@"
    + "    memset(&sa, 0, sizeof sa);@NL@"
    + "    sa.sin_family = AF_INET;@NL@"
    + "    sa.sin_addr.s_addr = htonl(INADDR_LOOPBACK);@NL@"
    + "    sa.sin_port = 0;@NL@"
    + "    if (bind(fd, (struct sockaddr *)&sa, sizeof sa) != 0) { close(fd); return -1; }@NL@"
    + "    if (listen(fd, 16) != 0) { close(fd); return -1; }@NL@"
    + "    return fd;@NL@"
    + "};@NL@"
    + "static int connect_to_listener(int lfd) {@NL@"
    + "    struct sockaddr_in sa;@NL@"
    + "    socklen_t sl = sizeof sa;@NL@"
    + "    if (getsockname(lfd, (struct sockaddr *)&sa, &sl) != 0) return -1;@NL@"
    + "    int cfd = socket(AF_INET, SOCK_STREAM, 0);@NL@"
    + "    if (cfd < 0) return -1;@NL@"
    + "    if (connect(cfd, (struct sockaddr *)&sa, sizeof sa) != 0) { close(cfd); return -1; }@NL@"
    + "    return cfd;@NL@"
    + "};@NL@"
    + "int echo_serve(int lfd) {@NL@"
    + "    if (lfd < 0) return -1;@NL@"
    + "    int cfd = accept(lfd, NULL, NULL);@NL@"
    + "    if (cfd < 0) return -1;@NL@"
    + "    char buf[256];@NL@"
    + "    ssize_t n = recv(cfd, buf, sizeof buf, 0);@NL@"
    + "    if (n > 0) {@NL@"
    + "        memset(buf, 88, (size_t)n);@NL@"
    + "        send(cfd, buf, (size_t)n, 0);@NL@"
    + "    }@NL@"
    + "    close(cfd);@NL@"
    + "    return 0;@NL@"
    + "};@NL@"
    + "static void *serve_thread(void *arg) {@NL@"
    + "    struct serve_arg *a = (struct serve_arg *)arg;@NL@"
    + "    echo_serve(a->lfd);@NL@"
    + "    return NULL;@NL@"
    + "};@NL@"
    + "int main(void) { return 0; }@NL@",
)
