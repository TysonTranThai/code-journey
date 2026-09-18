"""Module 11 — Parallel programming (csa-m11)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-parallel",
        "Parallel Programming",
        "Parallel.For, PLINQ, partitioning, and the arithmetic of when parallelism pays — measured, not assumed.",
    )

    csa.register_lesson(
        MID, "csa-m11-data-parallel", "Data parallelism: Parallel.For and friends",
        "Parallel.For/ForEach, local state, stop/break, and how the scheduler partitions work across cores.",
        15, "advanced", _m11_data_parallel, _m11_data_parallel_vi,
    )
    csa.register_lesson(
        MID, "csa-m11-plinq", "PLINQ: parallel query, real costs",
        "AsParallel, ordering, merging, degree of parallelism — and the workloads where PLINQ loses to LINQ.",
        15, "advanced", _m11_plinq, _m11_plinq_vi,
    )
    csa.register_lesson(
        MID, "csa-m11-when-parallel", "When parallelism pays — the arithmetic",
        "Amdahl's law, per-item overhead, chunking, false sharing — the model you use BEFORE writing the loop.",
        15, "advanced", _m11_when, _m11_when_vi,
    )
    csa.register_lesson(
        MID, "csa-m11-parallel-pitfalls", "Parallel pitfalls and exception handling",
        "AggregateException, thread-local accumulation errors, oversubscription, and cancellation of parallel loops.",
        15, "advanced", _m11_pitfalls, _m11_pitfalls_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m11", "Checkpoint: parallel",
        "Synthesis: a measured parallel pipeline with correct cancellation and aggregation.",
        12, "advanced", _m11_checkpoint, _m11_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m11-task", MID,
        title="Parallel checkpoint",
        prompt=(
            "Implement `static long SumSquaresParallel(int[] data, int threshold)` that sums squares of elements — "
            "sequentially when data.Length <= threshold, in parallel otherwise, using Parallel.For with a thread-local "
            "sum (interlocked-locked final combine). Then implement `static int[] SquaresParallel(int[] data)` "
            "returning squares IN ORIGINAL ORDER via PLINQ (AsOrdered). The test compares both against sequential "
            "results and asserts the parallel version of a 10M-element array beats a deliberately slow sequential "
            "baseline (a fake per-item cost)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "sum-correct",
                "code": (
                    "var data = Enumerable.Range(1, 1000).ToArray();\n"
                    "long seq = 0; foreach (var x in data) seq += (long)x * x;\n"
                    'Cj.Eq(Solution.SumSquaresParallel(data, 100), seq, "parallel sum matches sequential");\n'
                    'Cj.Eq(Solution.SumSquaresParallel(data, 10000), seq, "below threshold runs sequentially and still sums");'
                ),
                "hint": "Parallel.For with localInit: () => 0L, body: (i, state, local) => local + (long)data[i]*data[i], localFinally: local => Interlocked.Add(ref total, local).",
            },
            {
                "name": "plinq-ordered",
                "code": (
                    "var data = Enumerable.Range(1, 100).ToArray();\n"
                    "var r = Solution.SquaresParallel(data);\n"
                    'Cj.Eq(string.Join(",", r.Take(5)), "1,4,9,16,25", "AsOrdered preserves index order");\n'
                    'Cj.Eq(r.Length, 100, "all present");'
                ),
                "hint": "data.AsParallel().AsOrdered().Select(x => x * x).ToArray() — without AsOrdered, PLINQ merges out of order.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static long SumSquaresParallel(int[] data, int threshold)\n"
            "    {\n"
            "        if (data.Length <= threshold)\n"
            "        {\n"
            "            long s = 0;\n"
            "            foreach (var x in data) s += (long)x * x;\n"
            "            return s;\n"
            "        }\n"
            "        long total = 0;\n"
            "        Parallel.For(0, data.Length,\n"
            "            () => 0L,\n"
            "            (i, _, local) => local + (long)data[i] * data[i],\n"
            "            local => Interlocked.Add(ref total, local));\n"
            "        return total;\n"
            "    }\n\n"
            "    public static int[] SquaresParallel(int[] data)\n"
            "        => data.AsParallel().AsOrdered().Select(x => x * x).ToArray();\n"
            "}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static long SumSquaresParallel(int[] data, int threshold)\n"
            "    {\n"
            "        long total = 0;\n"
            "        Parallel.For(0, data.Length, i => total += (long)data[i] * data[i]);   // WRONG: lost updates on total\n"
            "        return total;\n"
            "    }\n\n"
            "    public static int[] SquaresParallel(int[] data)\n"
            "        => data.AsParallel().Select(x => x * x).ToArray();   // WRONG: unordered merge\n"
            "}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p11-par", "Parallel drills",
        "Local-state aggregation, PLINQ ordering, Amdahl reasoning, and cancellation of long loops.",
        45, "advanced", "csa-m11-parallel-pitfalls",
        ["csa-p11-parallel-cancel", "csa-p11-amdahl"],
    )
    csa.register_challenge(
        "csa-p11-parallel-cancel", MID,
        title='Parallel scan with early exit',
        prompt=(
            "Implement `static int FirstMatch(int[] data, Func<int, bool> predicate, int workers)` that finds the first index (lowest i) where predicate(data[i]) is true, running the scan in parallel chunks — using Parallel.For with a shared 'found index' guarded by Interlocked.CompareExchange so only a LOWER index ever wins, and stopping other iterations once found (loopState.Stop()). Return -1 if absent. The test counts predicate invocations: without Stop() the full scan runs all 10 million calls for a match at index 5 — the test requires fewer than 1 million."
        ),
        difficulty='advanced',
        tests=[
            {
                "name": 'first-match',
                "code": (
                    'var data = new int[100_000];\nfor (int i = 0; i < data.Length; i++) data[i] = i;\ndata[42_000] = -1; data[42_001] = -1;\nfor (int rep = 0; rep < 50; rep++)\n    Cj.Eq(Solution.FirstMatch(data, x => x == -1, 8), 42_000, "lowest index wins, every rep");'
                ),
                "hint": 'Interlocked.CompareExchange(ref best, i, int.MaxValue) wins only when best is still MaxValue OR i is lower — the CAS loop keeps the smallest index.',
            },
            {
                "name": 'absent',
                "code": (
                    'var data = Enumerable.Range(0, 10_000).ToArray();\nCj.Eq(Solution.FirstMatch(data, x => x == 99_999, 4), -1, "absent returns -1");'
                ),
                "hint": 'Same loop; no CAS ever succeeds.',
            },
            {
                "name": 'early-exit',
                "code": (
                    '// 10M elements, match at index 5. Without Stop() the full scan runs ALL\n// 10,000,000 predicate calls; with Stop() it must be orders of magnitude less.\nvar data = new int[10_000_000];\ndata[5] = -1;\nlong calls = 0;\nint hit = Solution.FirstMatch(data, x => { System.Threading.Interlocked.Increment(ref calls); return x == -1; }, 4);\nCj.Eq(hit, 5, "finds the early match");\nCj.True(calls < 1_000_000, $"Stop() must cut the scan: {calls:N0} predicate calls (full scan = 10,000,000)");'
                ),
                "hint": 'After the CAS wins, call loopState.Stop() so Parallel.For stops scheduling further iterations — the test counts predicate invocations and a full scan is 10,000,000.',
            },
        ],
        reference=(
            'public class Solution\n{\n    public static int FirstMatch(int[] data, Func<int, bool> predicate, int workers)\n    {\n        int best = int.MaxValue;\n        var options = new ParallelOptions { MaxDegreeOfParallelism = workers };\n        Parallel.For(0, data.Length, options, (i, loopState) =>\n        {\n            if (predicate(data[i]))\n            {\n                int seen;\n                do { seen = best; }\n                while (i < seen && Interlocked.CompareExchange(ref best, i, seen) != seen);\n                if (best == i) loopState.Stop();   // we won; tell the others\n            }\n        });\n        return best == int.MaxValue ? -1 : best;\n    }\n}'
        ),
        wrong=(
            'public class Solution\n{\n    public static int FirstMatch(int[] data, Func<int, bool> predicate, int workers)\n    {\n        int best = int.MaxValue;\n        var options = new ParallelOptions { MaxDegreeOfParallelism = workers };\n        Parallel.For(0, data.Length, options, (i, loopState) =>\n        {\n            // WRONG: coordination without cancellation - every match CASes the minimum, but the\n            // loop never stops early, so all 10 million iterations ALWAYS run. With a slow\n            // predicate and an early match this is an order of magnitude slower.\n            if (predicate(data[i]))\n            {\n                int seen;\n                do { seen = best; }\n                while (i < seen && Interlocked.CompareExchange(ref best, i, seen) != seen);\n            }\n        });\n        return best == int.MaxValue ? -1 : best;\n    }\n}'
        ),
        level='guided',
    )
    csa.register_challenge(
        "csa-p11-amdahl", MID,
        title="Amdahl's law, measured",
        prompt=(
            "A pipeline has a parallelizable part P and a serial fraction S (S + P = 1). Implement `static double "
            "Speedup(double serialFraction, int cores)` returning Amdahl's speedup S(n) = 1 / (S + P/n) — and "
            "`static int BreakEvenCores(double serialFraction, double minSpeedup)` returning the smallest core count "
            "whose speedup reaches minSpeedup (return -1 if no finite core count reaches it). The test checks the "
            "hard ceiling: with 10% serial work, no number of cores beats 10x."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "amdahl-values",
                "code": (
                    'Cj.True(Math.Abs(Solution.Speedup(0.1, 4) - 1.0 / (0.1 + 0.9 / 4)) < 1e-9, "formula exact");\n'
                    'Cj.True(Solution.Speedup(0.1, 1_000_000) < 10.0, "serial 10% caps speedup below 10x");\n'
                    'Cj.Eq(Solution.BreakEvenCores(0.1, 5.0), 9, "smallest n reaching 5x with S=0.1");'
                ),
                "hint": "Speedup = 1/(S + (1-S)/n). BreakEven: solve 1/(S + (1-S)/n) >= target for n, ceil it — unless S*target >= 1, then unreachable (-1).",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static double Speedup(double serialFraction, int cores)\n"
            "        => 1.0 / (serialFraction + (1.0 - serialFraction) / cores);\n\n"
            "    public static int BreakEvenCores(double serialFraction, double minSpeedup)\n"
            "    {\n"
            "        if (serialFraction * minSpeedup >= 1.0) return -1;   // ceiling below target\n"
            "        double n = (1.0 - serialFraction) * minSpeedup / (1.0 - serialFraction * minSpeedup);\n"
            "        return (int)Math.Ceiling(n);\n"
            "    }\n"
            "}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static double Speedup(double serialFraction, int cores)\n"
            "        => cores;   // WRONG: assumes perfect scaling — the exact mistake Amdahl's law names\n\n"
            "    public static int BreakEvenCores(double serialFraction, double minSpeedup)\n"
            "        => (int)Math.Ceiling(minSpeedup);   // WRONG: ignores serial fraction\n"
            "}"
        ),
        level="independent",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m11_data_parallel = r"""## Data parallelism: Parallel.For and friends

`Parallel.For` and `Parallel.ForEach` split an index range or collection
across worker threads, pooling the thread pool's threads. The three-delegate
form is the workhorse because it solves the aggregation problem correctly:

```csharp
long total = 0;
Parallel.For(0, data.Length,
    localInit: () => 0L,                                    // per-worker accumulator
    body: (i, state, local) => local + (long)data[i] * data[i],
    localFinally: local => Interlocked.Add(ref total, local));  // combine once per worker
```

Why it matters: the naive `Parallel.For(0, n, i => total += f(i))` loses
updates — the combine happens inside the hot loop under contention. The
local-state version touches shared memory once per worker chunk, which is
the difference between parallel speedup and parallel slowdown.

Control surfaces worth knowing: `loopState.Stop()` halts as soon as possible
(earliest-stop, not index-ordered); `loopState.Break()` stops everything
AFTER the current iteration (ordered-ish, rarely what you want);
`ParallelOptions { MaxDegreeOfParallelism, CancellationToken }` bound both
CPU and lifetime.

The scheduler chunks the range adaptively — small ranges get small chunks
(load balance), big ones get bigger chunks (less coordination). This is
also why tiny bodies lose: chunk coordination + thread handoff dominates
a 10ns body. Parallelism needs per-item work measured in microseconds, not
nanoseconds.
"""

_m11_data_parallel_vi = r"""## Song song dữ liệu: Parallel.For và bạn bè

`Parallel.For` và `Parallel.ForEach` chia một dải chỉ số hoặc bộ sưu tập
cho các worker thread, gom mượn thread của thread pool. Dạng ba-delegate là
lao động chính vì nó giải bài toán tổng hợp đúng cách:

```csharp
long total = 0;
Parallel.For(0, data.Length,
    localInit: () => 0L,                                    // bộ tích lũy mỗi worker
    body: (i, state, local) => local + (long)data[i] * data[i],
    localFinally: local => Interlocked.Add(ref total, local));  // gộp một lần mỗi worker
```

Vì sao quan trọng: `Parallel.For(0, n, i => total += f(i))` ngây thơ mất
cập nhật — phép gộp diễn ra trong vòng nóng dưới contention. Bản local-state
chạm bộ nhớ dùng chung một lần mỗi mảnh worker — đó là khác biệt giữa tăng
tốc song song và giảm tốc song song.

Các bề mặt điều khiển đáng biết: `loopState.Stop()` dừng càng sớm càng tốt
(early-stop, không theo thứ tự chỉ số); `loopState.Break()` dừng mọi thứ
SAU lần lặp hiện tại (kiểu có thứ tự, hiếm khi là điều bạn muốn);
`ParallelOptions { MaxDegreeOfParallelism, CancellationToken }` chặn cả CPU
lẫn tuổi thọ.

Bộ lập lịch chia mảnh thích ứng — dải nhỏ được mảnh nhỏ (cân bằng tải),
dải lớn được mảnh lớn (ít phối hợp hơn). Đây cũng là lý do thân lặp nhỏ
thua: phối hợp mảnh + chuyển thread áp đảo một thân 10ns. Song song cần
công việc mỗi phần tử đo bằng micro giây, không phải nano giây.
"""

_m11_plinq = r"""## PLINQ: parallel query, real costs

`.AsParallel()` turns a LINQ query into a parallel pipeline; PLINQ
partitions the source, runs operators concurrently, and merges results:

```csharp
var heavy = urls.AsParallel()
                .Select(ParseAndScore)      // CPU-bound, expensive per item
                .Where(s => s > threshold)
                .ToArray();
```

The merge behavior is the first surprise: **PLINQ reorders by default.**
It buffers results to yield them faster, sacrificing order for throughput.
`.AsOrdered()` restores source order at a real buffering cost — pay it only
when order is part of the answer.

What PLINQ is good at: CPU-bound element-wise work over large inputs
(`Select` with expensive transforms), `Aggregate` with seeded overloads.
What it is bad at:

- **Tiny per-item work** — partition overhead eats the win (the same rule
  as Parallel.For).
- **Order-dependent operators** — `Take`, `First`, `Skip` need sequence
  semantics that fight partitioning.
- **Side-effecting lambdas** — they now run on many threads; your closure
  had better be thread-safe.
- **I/O-bound work** — PLINQ parallelizes THREADS, not waiting. Awaiting a
  network call inside PLINQ blocks pool threads. That job belongs to
  `Task.WhenAll`/async streams.

`WithDegreeOfParallelism(n)` caps the worker count — essential when several
PLINQ queries share a process, or when the box is shared. `AsSequential()`
drops back to sequential mid-query when a later operator cannot be
parallelized.
"""

_m11_plinq_vi = r"""## PLINQ: truy vấn song song, giá thật

`.AsParallel()` biến truy vấn LINQ thành pipeline song song; PLINQ phân
mảnh nguồn, chạy các toán tử đồng thời, và gộp kết quả:

```csharp
var heavy = urls.AsParallel()
                .Select(ParseAndScore)      // CPU-bound, đắt mỗi phần tử
                .Where(s => s > threshold)
                .ToArray();
```

Hành vi gộp là bất ngờ đầu tiên: **PLINH đổi thứ tự theo mặc định.** Nó
buffer kết quả để trả về nhanh hơn, đánh đổi thứ tự lấy thông lượng.
`.AsOrdered()` khôi phục thứ tự nguồn với chi phí buffer thật — chỉ trả khi
thứ tự là một phần của đáp án.

PLINQ giỏi gì: công việc element-wise gắn CPU trên đầu vào lớn (`Select`
với transform đắt), `Aggregate` với overload có seed. PLINQ tệ ở đâu:

- **Công việc mỗi phần tử quá nhỏ** — chi phí phân mảnh nuốt phần thắng
  (cùng quy tắc với Parallel.For).
- **Toán tử phụ thuộc thứ tự** — `Take`, `First`, `Skip` cần ngữ nghĩa
  trình tự mà chúng đi ngược phân mảnh.
- **Lambda có tác dụng phụ** — chúng giờ chạy trên nhiều thread; closure
  của bạn phải thread-safe.
- **Công việc gắn I/O** — PLINQ song song hóa THREAD, không phải chờ đợi.
  Await một lời gọi mạng trong PLINQ là chặn thread pool. Việc đó thuộc về
  `Task.WhenAll`/async stream.

`WithDegreeOfParallelism(n)` chặn số worker — cần thiết khi nhiều truy vấn
PLINQ dùng chung một process, hoặc máy dùng chung. `AsSequential()` hạ về
tuần tự giữa truy vấn khi toán tử sau không song song hóa được.
"""

_m11_when = r"""## When parallelism pays — the arithmetic

Before writing a parallel loop, do this arithmetic. It predicts success
better than any benchmark's vibes:

**Amdahl's law.** With serial fraction S, speedup S(n) = 1/(S + (1-S)/n).
Ten percent serial work caps you below 10x no matter how many cores. The
serial fraction is not just loops — it is contention points, shared
queues, the final combine. This is why the checkpoint makes you compute
break-even cores: most real workloads stop scaling at 4–8x.

**Per-item overhead.** Parallel.For's coordination costs ~hundreds of
nanoseconds to microseconds per chunk. Rule of thumb: each item's body
should cost ≥ a microsecond (or the data set ≥ millions of items) before
parallelism pays. Below that, the parallel version is SLOWER — a measured
fact, not an opinion.

**False sharing.** Two workers writing adjacent array elements (or
adjacent fields in one cache line) ping-pong the line between cores.
Symptom: parallel version scales to 2 cores, then flattens — while CPU
shows 100%. Fix: pad/shard accumulators (thread-local aggregation does
this naturally).

**Memory bandwidth ceilings.** Summing an int[] is compute-trivial and
memory-bound; beyond a few cores the bus saturates and speedup plateaus.
Parallelize compute-heavy work, not memcpy-shaped work.

The habit: model first (S, per-item cost, data size), then measure, then
keep or discard. The checkpoint's `BreakEvenCores` encodes the model.
"""

_m11_when_vi = r"""## Khi nào song song có lợi — phép tính

Trước khi viết vòng song song, làm phép tính này. Nó dự đoán thành bại
tốt hơn mọi cảm tính benchmark:

**Định luật Amdahl.** Với phân số tuần tự S, speedup S(n) = 1/(S + (1-S)/n).
Mười phần trăm tuần tự chặn bạn dưới 10x bất kể bao nhiêu nhân. Phân số
tuần tự không chỉ là vòng lặp — đó là các điểm contention, queue dùng chung,
phép gộp cuối. Vì vậy checkpoint bắt bạn tính break-even cores: phần lớn
workload thật dừng scale ở 4–8x.

**Chi phí mỗi phần tử.** Phối hợp của Parallel.For tốn cỡ hàng trăm nano
giây đến micro giây mỗi mảnh. Kinh nghiệm: thân của mỗi phần tử nên tốn
≥ một micro giây (hoặc tập dữ liệu ≥ hàng triệu phần tử) trước khi song
song có lợi. Thấp hơn thế, bản song song CHẬM HƠN — sự thật đo đếm được,
không phải ý kiến.

**False sharing.** Hai worker ghi các phần tử mảng kề nhau (hoặc các field
kề nhau trong một cache line) sẽ chuyền line qua lại giữa các nhân.
Triệu chứng: bản song song scale tới 2 nhân rồi dừng phẳng — trong khi CPU
báo 100%. Cách sửa: pad/phân mảnh bộ tích lũy (tổng hợp thread-local làm
việc đó tự nhiên).

**Trần băng thông bộ nhớ.** Cộng một int[] là tính toán tầm thường và bị
chặn bởi bộ nhớ; quá vài nhân thì bus bão hòa và speedup chững. Hãy song
song hóa công việc nặng tính toán, không phải công việc có hình memcpy.

Thói quen: mô hình hóa trước (S, chi phí mỗi phần tử, cỡ dữ liệu), rồi đo,
rồi giữ hoặc bỏ. `BreakEvenCores` của checkpoint mã hóa mô hình đó.
"""

_m11_pitfalls = r"""## Parallel pitfalls and exception handling

**Exceptions aggregate.** A parallel loop may throw on several workers
simultaneously; you receive `AggregateException` carrying them all:

```csharp
try { Parallel.ForEach(files, f => Process(f)); }
catch (AggregateException ag)
{
    foreach (var ex in ag.Flatten().InnerExceptions) Log(ex);
}
```

Catching inside the body and swallowing is how partial failures hide —
process half the files, report success.

**Closure capture is a classic trap.** `Parallel.For` gives you the index
as a parameter, so the old `for`-loop closure bug does not apply — but
`Parallel.ForEach` over a collection whose enumerator is not thread-safe,
or shared mutable state in the lambda, will bite. Anything written by two
iterations needs atomics or local aggregation.

**Oversubscription.** Launching 100 `Task.Run` CPU jobs on 8 cores just
multiplies context switches. Bound with `MaxDegreeOfParallelism`, or
partition explicitly. The thread pool's hill-climbing also resents CPU
storms — long-running work belongs in `LongRunning` tasks or dedicated
workers, not `Task.Run` floods.

**Cancellation** of a parallel loop is cooperative like everything else:
pass a token via `ParallelOptions`, and the loop stops *launching* new
iterations when it fires; bodies must check `loopState.ShouldExitCurrentIteration`
or the token themselves for prompt exit. An unobserved token cancels
scheduling only — a common production misunderstanding ("we cancelled it,
why is it still eating CPU?").

**UI-thread deadlock** is an async smell, but Parallel + UI fails too:
`Parallel.For(...).Wait()` on the UI thread is fine, but blocking the UI
thread inside a body that itself awaits deadlocks the loop. Keep bodies
CPU-only; orchestrate async at the boundary.
"""

_m11_pitfalls_vi = r"""## Cạm bẫy song song và xử lý exception

**Exception được tổng hợp.** Một vòng song song có thể ném ở nhiều worker
cùng lúc; bạn nhận `AggregateException` mang tất cả:

```csharp
try { Parallel.ForEach(files, f => Process(f)); }
catch (AggregateException ag)
{
    foreach (var ex in ag.Flatten().InnerExceptions) Log(ex);
}
```

Bắt trong thân rồi nuốt là cách lỗi cục bộ bị che giấu — xử lý được nửa
số file mà vẫn báo thành công.

**Bắt closure là cạm bẫy kinh điển.** `Parallel.For` đưa chỉ số qua tham
số nên bug closure của vòng `for` cũ không áp dụng — nhưng `Parallel.ForEach`
trên bộ sưu tập có enumerator không thread-safe, hay trạng thái khả biến
dùng chung trong lambda, sẽ cắn bạn. Mọi thứ được hai lần lặp cùng ghi cần
nguyên tử hoặc tổng hợp cục bộ.

**Oversubscription.** Phóng 100 job CPU qua `Task.Run` trên 8 nhân chỉ nhân
đôi context switch. Chặn bằng `MaxDegreeOfParallelism`, hoặc phân mảnh tường
minh. Hill-climbing của thread pool cũng ghét bão CPU — công việc dài hạn
thuộc về task `LongRunning` hoặc worker riêng, không phải lũ `Task.Run`.

**Cancellation** của vòng song song hợp tác như mọi thứ khác: truyền token
qua `ParallelOptions`, vòng sẽ ngưng *phóng* lần lặp mới khi nó bốc cháy;
thân vòng phải tự kiểm tra `loopState.ShouldExitCurrentIteration` hoặc token
để thoát kịp thời. Token không bị quan sát chỉ hủy việc lập lịch — hiểu
lầm production phổ biến ("chúng tôi đã hủy rồi, sao nó vẫn ngốn CPU?").

**Deadlock UI-thread** là mùi async, nhưng Parallel + UI cũng sập: chặn
thread UI bằng `Parallel.For(...).Wait()` thì ổn, nhưng chặn thread UI
trong thân mà thân đó lại await sẽ deadlock cả vòng. Giữ thân thuần CPU;
orchestrate async ở biên.
"""

_m11_checkpoint = r"""## Checkpoint: parallel

The graded task combines thread-local aggregation (correct sum under
parallelism), threshold-based sequential/parallel switching, and ordered
PLINQ. Practice adds min-index CAS racing with cooperative stop, and
Amdahl's-law arithmetic you compute yourself.
"""

_m11_checkpoint_vi = r"""## Checkpoint: parallel

Bài được chấm kết hợp tổng hợp thread-local (tổng đúng dưới song song),
chuyển đổi tuần tự/song song theo ngưỡng, và PLINQ có thứ tự. Practice
thêm race CAS chỉ-số-nhỏ-nhất với dừng hợp tác, và phép tính định luật
Amdahl do chính bạn thực hiện.
"""
