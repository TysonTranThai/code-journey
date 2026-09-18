#!/usr/bin/env python3
"""Java — Advanced — Module 9: javaa-perf-measure.

Measurement before optimization: nanoTime (monotonic, not a clock), JIT
warmup and why first runs lie, the interpreter-vs-C3 threshold, bounded
inversion counts for honest javap-free bytecode claims, JMH philosophy
(why @Benchmark exists), and the checkpoint — a micro-harness with warmup,
median-of-runs, and epsilon comparison. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-perf-measure"

L_NANO_EN = """
`System.nanoTime()` is *monotonic*: it never goes backward, is unaffected by
NTP or user clock changes, and is only meaningful as a DIFFERENCE between two
reads. `System.currentTimeMillis()` is a wall clock — it can jump. Timing
arithmetic uses nanoTime; date/time display uses the wall clock. Confusing
them is how you time a test during a DST changeover.

```java
long t0 = System.nanoTime();
work();
long nanos = System.nanoTime() - t0;   // duration; divide for ms
```

JIT compilation is *asynchronous* and happens per-method, on thresholds: the
interpreter counts invocations/back-edges, and at roughly 10k the method is
queued for C1 (fast compile) and later C2 (full optimization). Timing an
unwarmed method measures the interpreter plus the compiler's attention, not
your code. Hence the golden rule: **measure warm code** — run the workload
some thousands of times first, discard that data, then measure. `fork()`
between benchmark JVMs and the absence of dead-code elimination are why JMH
(@Benchmark) exists at all: an ad-hoc timer is a benchmarking *toy*.
"""
L_NANO_VI = """
`System.nanoTime()` là *đơn điệu*: không bao giờ đi lùi, không bị NTP hay người
dùng đổi giờ ảnh hưởng, và chỉ có ý nghĩa như một HIỆU giữa hai lần đọc.
`System.currentTimeMillis()` là đồng hồ tường — nó có thể nhảy. Phép tính thời
gian dùng nanoTime; hiển thị ngày giờ mới dùng đồng hồ tường. Nhầm hai cái là
cách bạn "đo" test đúng lúc hệ thống đổi giờ.

```java
long t0 = System.nanoTime();
work();
long nanos = System.nanoTime() - t0;   // thời lượng; chia để ra ms
```

JIT biên dịch *bất đồng bộ* và theo từng method, dựa trên ngưỡng: trình thông
dịch đếm số lần gọi/số lần quay lùi, và ở khoảng 10k method được xếp hàng cho
C1 (biên dịch nhanh) rồi C2 (tối ưu đầy đủ). Đo một method chưa warm là đo
trình thông dịch cộng cả sự chú ý của compiler, không phải đo code của bạn.
Vì thế có quy tắc vàng: **đo code đã warm** — chạy workload vài nghìn lần
trước, vứt số liệu đó, rồi mới đo. `fork()` giữa các JVM benchmark và việc
tránh dead-code elimination là lý do JMH (@Benchmark) tồn tại: đồng hồ tự chế
là đồ chơi đo hiệu năng.
"""

L_INV_EN = """
You cannot run `javap` in this sandbox — but you can still make *bounded,
honest* claims about compiled code. Bubble sort's inversions (out-of-order
pairs) are exactly the count of swaps it performs:

```java
static long inversionCount(int[] a) {   // O(n^2) — honest brute force
    long inv = 0;
    for (int i = 0; i < a.length; i++)
        for (int j = i + 1; j < a.length; j++)
            if (a[i] > a[j]) inv++;
    return inv;
}
```

`inversionCount` is a *fact about the data*; the number of swaps a correct
bubble sort performs equals it exactly; and a linear scan of the final array
proves the sort actually sorted (all-zero inversions). Three mutually
reinforcing measurements — none of which trusts the optimizer to be honest,
all of which the optimizer cannot cheat. This is the pattern for testing
performance-adjacent behavior: assert on *countable* effects, not on vibes.
"""
L_INV_VI = """
Bạn không thể chạy `javap` trong sandbox này — nhưng vẫn có thể đưa ra những
tuyên bố *có chặn trên, trung thực* về code đã biên dịch. Số nghịch đảo (cặp
lệch thứ tự) của bubble sort chính là số lần swap nó thực hiện:

```java
static long inversionCount(int[] a) {   // O(n^2) — vét cạn trung thực
    long inv = 0;
    for (int i = 0; i < a.length; i++)
        for (int j = i + 1; j < a.length; j++)
            if (a[i] > a[j]) inv++;
    return inv;
}
```

`inversionCount` là *sự thật về dữ liệu*; số swap mà một bubble sort đúng thực
hiện bằng đúng con số đó; và một lần quét tuyến tính trên mảng cuối chứng minh
mảng đã được sắp (nghịch đảo = 0). Ba phép đo củng cố lẫn nhau — không phép đo
nào tin tưởng optimizer là trung thực, và optimizer không thể gian lận phép đo
nào. Đây là mẫu để kiểm thử hành vi lân cận hiệu năng: khẳng định trên *hiệu
ứng đếm được*, không phải trên cảm giác.
"""

L_HARNESS_EN = """
A defensible micro-benchmark in 30 lines:

1. **Warmup**: run the workload W times; discard everything.
2. **Measure**: run R rounds, each timing N operations with nanoTime.
3. **Reduce**: take the MEDIAN of the per-round averages — the median resists
   outliers (a GC pause in one round) far better than the mean.
4. **Compare with epsilon**: declare A faster than B only if
   `medianB - medianA > epsilon` where epsilon is a meaningful fraction (say
   10%) of the slower median. Anything inside epsilon is "no measured
   difference".

The benchmark is itself code and can be gamed: if the JIT proves the measured
result is unused, it deletes the work (dead-code elimination) and you measure
nothing. Consume the result — sum it into a variable, print it in verbose
mode, check it. A benchmark that returns void and ignores its output is a
benchmark of the optimizer, not of your code.
"""
L_HARNESS_VI = """
Một micro-benchmark defendable trong 30 dòng:

1. **Warmup**: chạy workload W lần; vứt toàn bộ số liệu.
2. **Đo**: chạy R vòng, mỗi vòng đo N phép toán bằng nanoTime.
3. **Giảm dữ liệu**: lấy MEDIAN của trung bình các vòng — median chịu nhiễu
   (một đợt tạm dừng GC) tốt hơn mean nhiều.
4. **So sánh với epsilon**: chỉ tuyên bố A nhanh hơn B khi
   `medianB - medianA > epsilon`, với epsilon là một phần đáng kể (ví dụ 10%)
   của median chậm hơn. Mọi thứ trong epsilon là "không khác biệt đo được".

Bản thân benchmark cũng là code và có thể bị lừa: nếu JIT chứng minh kết quả
đo không được dùng, nó xóa luôn công việc (dead-code elimination) và bạn đo
một khoảng không. Hãy tiêu thụ kết quả — cộng vào biến, in ra ở chế độ verbose,
kiểm tra nó. Benchmark trả về void và bỏ qua output là benchmark của optimizer,
không phải của code bạn.
"""

write_module(
    M, "Performance Measurement",
    "nanoTime and warmup discipline, bounded bytecode claims, and an honest micro-benchmark harness.",
    "Đo lường hiệu năng",
    "nanoTime và kỷ luật warmup, tuyên bố bytecode có chặn trên, và harness micro-benchmark trung thực.",
    ["javaa-nanotime-warmup", "javaa-bounded-bytecode", "javaa-micro-harness"],
    ["javaa-p9-perf"],
)

write_lesson(M, "javaa-nanotime-warmup",
    "nanoTime, warmup, and the JIT threshold",
    "Monotonic timing, asynchronous JIT, why first runs lie, and the measure-warm-code rule.",
    16, L_NANO_EN,
    "nanoTime, warmup, và ngưỡng JIT",
    "Đo thời gian đơn điệu, JIT bất đồng bộ, vì sao lần chạy đầu nói dối, và quy tắc đo code đã warm.",
    L_NANO_VI)

write_lesson(M, "javaa-bounded-bytecode",
    "Bounded claims about compiled code",
    "Inversion counting as an optimizer-proof measurement of sorting work.",
    14, L_INV_EN,
    "Tuyên bố có chặn trên về code đã biên dịch",
    "Đếm nghịch đảo là phép đo chống-gian-lận cho công việc sắp xếp.",
    L_INV_VI)

write_lesson(M, "javaa-micro-harness",
    "The micro-benchmark harness",
    "Warmup, median reduction, epsilon comparison, and defeating dead-code elimination.",
    16, L_HARNESS_EN,
    "Harness micro-benchmark",
    "Warmup, giảm dữ liệu bằng median, so sánh epsilon, và đánh bại dead-code elimination.",
    L_HARNESS_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_NANO = challenge(
    "javaa-p9-nano",
    "Timing that cannot lie",
    "1. `static long timedSum(int n)` — time a loop summing 1..n with nanoTime; return\n"
    "the elapsed NANOS. Verify the sum equals (long) n * (n + 1) / 2 and throw\n"
    "IllegalStateException if it does not (defeat dead-code elimination by consuming\n"
    "the result).\n"
    "2. `static long warmMedianSum(int n, int rounds)` — for each of `rounds` rounds:\n"
    "time the same sum, convert to microseconds, collect; return the MEDIAN of the\n"
    "rounds (sort, take the middle). Warmup is inside: run the sum 2_000 times\n"
    "untimed before measuring.\n"
    "3. `static boolean nanoIsMonotonic()` — read nanoTime 1_000 times; return true iff\n"
    "no read was less than its predecessor (strictly: never a NEGATIVE step).",
    P_BOILER,
    [
        ("timed, consumed, honest", r"""
long ns = Solution.timedSum(1_000_000);
checkTrue(ns > 0, "elapsed is positive: " + ns);
checkTrue(Solution.nanoIsMonotonic(), "nanoTime never steps backward");
""", "Consumed results survive DCE; monotonic holds."),
        ("median after warmup", r"""
long us = Solution.warmMedianSum(1_000_000, 5);
checkTrue(us > 0, "median micros is positive: " + us);
""", "Warm first, median second."),
    ],
    level="guided",
)
CH_NANO_VI = vi_challenge(
    "Đo thời gian không thể nói dối",
    "timedSum/warmMedianSum/nanoIsMonotonic: tiêu thụ kết quả để chống DCE, median sau warmup, nanoTime không lùi.",
    [("Đo xong phải tiêu thụ", "Kết quả được kiểm để sống sót qua DCE."),
     ("Warm trước, median sau", "Vứt giai đoạn thông dịch.")],
)

CH_SORTPROOF = challenge(
    "javaa-p9-sortproof",
    "Prove the sort with arithmetic",
    "1. `static long inversionCount(int[] a)` — count out-of-order pairs (i < j, a[i] > a[j])\n"
    "with the honest O(n^2) double loop, as a long.\n"
    "2. `static void bubbleSort(int[] a)` — classic bubble sort, no early exit.\n"
    "3. `static long swapsFor(int[] a)` — return the number of swaps bubbleSort performs\n"
    "on a defensive copy of a WITHOUT re-counting inversions (count inside the sort or\n"
    "wrap it — your choice) — it must equal inversionCount(a) for every input.\n"
    "4. `static boolean isSorted(int[] a)` — linear scan, true iff non-decreasing.",
    P_BOILER,
    [
        ("swap count equals inversions", r"""
int[] xs = {5, 1, 4, 2, 8};
checkEq(Solution.inversionCount(xs), 4L, "4 inversions: 5>1, 5>4, 5>2, 4>2");
checkEq(Solution.swapsFor(xs), 4L, "bubble performs exactly that many swaps");
Solution.bubbleSort(xs);
checkTrue(Solution.isSorted(xs), "array actually sorted");
""", "Data fact, algorithm work, final state — all agree."),
        ("empty and single", r"""
checkEq(Solution.inversionCount(new int[]{}), 0L, "empty: zero inversions");
checkEq(Solution.swapsFor(new int[]{7}), 0L, "single element: zero swaps");
""", "Edge cases hold."),
    ],
    level="independent",
)
CH_SORTPROOF_VI = vi_challenge(
    "Chứng minh phép sắp bằng số học",
    "inversionCount/bubbleSort/swapsFor/isSorted: số swap bằng đúng số nghịch đảo, mảng cuối thực sự đã sắp.",
    [("Swap bằng nghịch đảo", "Sự thật dữ liệu, công việc thuật toán, trạng thái cuối — khớp nhau."),
     ("Rỗng và một phần tử", "Trường hợp biên vẫn giữ."),],
)

write_practice(M, "javaa-p9-perf",
    "Measurement drills",
    "Time like an engineer: consume results, warm up, take medians, and prove work with counters.",
    "Bài tập đo lường",
    "Đo như kỹ sư: tiêu thụ kết quả, warm up, lấy median, và chứng minh công việc bằng bộ đếm.",
    "javaa-micro-harness", 50, "advanced",
    [CH_NANO, CH_SORTPROOF],
    {"javaa-p9-nano": CH_NANO_VI, "javaa-p9-sortproof": CH_SORTPROOF_VI},
    solutions=[
        ("javaa-p9-nano", r"""
import java.util.*;

public class Solution {
    public static long timedSum(int n) {
        long t0 = System.nanoTime();
        long sum = 0;
        for (int i = 1; i <= n; i++) sum += i;
        long elapsed = System.nanoTime() - t0;
        if (sum != (long) n * (n + 1) / 2) {
            throw new IllegalStateException("sum corrupted: " + sum);
        }
        return elapsed;
    }

    public static long warmMedianSum(int n, int rounds) {
        for (int w = 0; w < 2_000; w++) {
            long s = 0;
            for (int i = 1; i <= n; i++) s += i;
            if (s == Long.MIN_VALUE) throw new IllegalStateException();
        }
        long[] samples = new long[rounds];
        for (int r = 0; r < rounds; r++) {
            samples[r] = timedSum(n) / 1_000;   // micros
        }
        Arrays.sort(samples);
        return samples[rounds / 2];
    }

    public static boolean nanoIsMonotonic() {
        long prev = System.nanoTime();
        for (int i = 0; i < 1_000; i++) {
            long now = System.nanoTime();
            if (now < prev) return false;
            prev = now;
        }
        return true;
    }
}
""", r"""
import java.util.*;

public class Solution {
    public static long timedSum(int n) {
        long t0 = System.nanoTime();
        long sum = 0;
        for (int i = 1; i <= n; i++) sum += i;   // result never checked:
        return System.nanoTime() - t0;           // WRONG — the JIT may delete the whole loop
    }

    public static long warmMedianSum(int n, int rounds) {
        long[] samples = new long[rounds];
        for (int r = 0; r < rounds; r++) {
            samples[r] = 0;                      // WRONG: never times — all zeros
        }
        Arrays.sort(samples);
        return samples[rounds / 2];              // WRONG: median of nothing = 0
    }

    public static boolean nanoIsMonotonic() {
        long prev = System.currentTimeMillis();  // WRONG: wall clock, not nanoTime
        for (int i = 0; i < 1_000; i++) {
            long now = System.nanoTime();
            if (now < prev) return false;
            prev = now;
        }
        return true;
    }
}
"""),
        ("javaa-p9-sortproof", r"""
public class Solution {
    public static long inversionCount(int[] a) {
        long inv = 0;
        for (int i = 0; i < a.length; i++) {
            for (int j = i + 1; j < a.length; j++) {
                if (a[i] > a[j]) inv++;
            }
        }
        return inv;
    }

    public static void bubbleSort(int[] a) {
        for (int i = 0; i < a.length - 1; i++) {
            for (int j = 0; j < a.length - 1 - i; j++) {
                if (a[j] > a[j + 1]) {
                    int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                }
            }
        }
    }

    public static long swapsFor(int[] a) {
        int[] copy = a.clone();
        long swaps = 0;
        for (int i = 0; i < copy.length - 1; i++) {
            for (int j = 0; j < copy.length - 1 - i; j++) {
                if (copy[j] > copy[j + 1]) {
                    int t = copy[j]; copy[j] = copy[j + 1]; copy[j + 1] = t;
                    swaps++;
                }
            }
        }
        return swaps;
    }

    public static boolean isSorted(int[] a) {
        for (int i = 1; i < a.length; i++) {
            if (a[i - 1] > a[i]) return false;
        }
        return true;
    }
}
""", r"""
public class Solution {
    public static long inversionCount(int[] a) {
        long inv = 0;
        for (int i = 0; i < a.length; i++) {
            for (int j = i + 1; j < a.length; j++) {
                if (a[i] > a[j]) inv++;
            }
        }
        return inv;
    }

    public static void bubbleSort(int[] a) {
        for (int i = 0; i < a.length - 1; i++) {
            for (int j = 0; j < a.length - 1 - i; j++) {
                if (a[j] > a[j + 1]) {
                    int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                }
            }
        }
    }

    public static long swapsFor(int[] a) {
        return inversionCount(a) + 1;   // WRONG: +1 — swaps must EQUAL inversions
    }

    public static boolean isSorted(int[] a) {
        for (int i = 1; i < a.length; i++) {
            if (a[i - 1] >= a[i]) return false;   // WRONG: rejects equal neighbors — not non-decreasing
        }
        return true;
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the micro-harness

Warmup, median-of-rounds, epsilon comparison, and dead-code defense — the
four properties separating measurement from superstition. Then use your own
harness to make a *guarded* claim about two workloads.
"""

CP_CH = challenge(
    "javaa-checkpoint-m9-task",
    "Checkpoint: measure, don't guess",
    "Inside Solution, implement the harness and use it:\n"
    "1. `static long sumTo(int n)` — plain loop sum 1..n, return the sum (the workload).\n"
    "2. `static long measureSumMicros(int n, int rounds)` — warm up 2_000 untimed runs,\n"
    "then time `rounds` runs of sumTo(n) in MICROS; return the MEDIAN. Every run's result\n"
    "must be verified against n*(n+1)/2 (consume it).\n"
    "3. `static boolean fasterWithinEpsilon(long aMicros, long bMicros, double epsFrac)` —\n"
    "true iff `a < b` AND the gap `(b - a)` exceeds `epsFrac * b` (b is the slower\n"
    "baseline; a only wins beyond the epsilon).\n"
    "4. `static String claim(long aMicros, long bMicros)` — return \"faster\" if\n"
    "fasterWithinEpsilon(a, b, 0.10), \"slower\" if fasterWithinEpsilon(b, a, 0.10),\n"
    "else \"no measured difference\".",
    P_BOILER,
    [
        ("harness produces sane medians", r"""
long us = Solution.measureSumMicros(2_000_000, 5);
checkTrue(us >= 0, "median micros non-negative: " + us);
""", "Warm, timed, verified, medianed."),
        ("epsilon comparison behaves", r"""
checkTrue(Solution.fasterWithinEpsilon(80, 100, 0.10), "20 > 10% of 100");
checkTrue(!Solution.fasterWithinEpsilon(95, 100, 0.10), "5 <= 10% of 100");
checkEq(Solution.claim(80, 100), "faster", "beyond epsilon");
checkEq(Solution.claim(95, 100), "no measured difference", "within epsilon");
checkEq(Solution.claim(120, 100), "slower", "a is slower");
""", "Only gaps beyond epsilon count."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: đo, đừng đoán",
    "measureSumMicros (warm + verify + median), fasterWithinEpsilon (chỉ thắng vượt epsilon), claim (faster/slower/no measured difference).",
    [("Harness ra median hợp lý", "Warm, đo, kiểm chứng, lấy median."),
     ("So sánh epsilon đúng", "Chỉ khoảng cách vượt epsilon mới tính.")],
)

write_checkpoint(M, "javaa-checkpoint-m9",
    "Checkpoint: Measure, Don't Guess",
    "A defensible micro-harness: warmup, median, epsilon, dead-code defense.",
    25, CP_MD,
    "Checkpoint: Đo, đừng đoán",
    "Micro-harness defendable: warmup, median, epsilon, chống dead-code.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;

public class Solution {
    public static long sumTo(int n) {
        long sum = 0;
        for (int i = 1; i <= n; i++) sum += i;
        return sum;
    }

    public static long measureSumMicros(int n, int rounds) {
        long expected = (long) n * (n + 1) / 2;
        for (int w = 0; w < 2_000; w++) {
            if (sumTo(n) == Long.MIN_VALUE) throw new IllegalStateException();
        }
        long[] samples = new long[rounds];
        for (int r = 0; r < rounds; r++) {
            long t0 = System.nanoTime();
            long got = sumTo(n);
            long t1 = System.nanoTime();
            if (got != expected) throw new IllegalStateException("bad sum");
            samples[r] = (t1 - t0) / 1_000;
        }
        Arrays.sort(samples);
        return samples[rounds / 2];
    }

    public static boolean fasterWithinEpsilon(long aMicros, long bMicros, double epsFrac) {
        if (aMicros >= bMicros) return false;
        return (bMicros - aMicros) > epsFrac * bMicros;
    }

    public static String claim(long aMicros, long bMicros) {
        if (fasterWithinEpsilon(aMicros, bMicros, 0.10)) return "faster";
        if (fasterWithinEpsilon(bMicros, aMicros, 0.10)) return "slower";
        return "no measured difference";
    }
}
""", wrong=r"""
import java.util.*;

public class Solution {
    public static long sumTo(int n) {
        long sum = 0;
        for (int i = 1; i <= n; i++) sum += i;
        return sum;
    }

    public static long measureSumMicros(int n, int rounds) {
        long[] samples = new long[rounds];
        for (int r = 0; r < rounds; r++) {
            long t0 = System.nanoTime();
            sumTo(n);                       // WRONG: result ignored (DCE risk) ...
            long t1 = System.nanoTime();
            samples[r] = (t1 - t0) / 1_000; // ... and NO warmup at all
        }
        Arrays.sort(samples);
        return samples[0];                  // WRONG: min, not median
    }

    public static boolean fasterWithinEpsilon(long aMicros, long bMicros, double epsFrac) {
        return aMicros < bMicros;           // WRONG: any gap counts — no epsilon test
    }

    public static String claim(long aMicros, long bMicros) {
        if (fasterWithinEpsilon(aMicros, bMicros, 0.10)) return "faster";
        if (fasterWithinEpsilon(bMicros, aMicros, 0.10)) return "slower";
        return "no measured difference";
    }
}
""")

print("module 9 authored")
