#!/usr/bin/env python3
"""Java - Beginner - Module 13: java-testing-debug.

Testing as a beginner superpower: why the compiler can't catch logic bugs,
JUnit's shape and philosophy (AAA), what makes a good assertion message,
edge-case discipline, and a debugging method that survives contact with
real bugs. House contract: declarative write_*, CjTestBase tests.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-testing-debug"

# ── lesson 13.1 — why tests ─────────────────────────────────────────────────
L_WHY_EN = r"""
You already test - every time you run a program and squint at the output,
you're testing. The problem: **you** have to rerun everything after every
change, and you eventually get lazy. Automated tests are programs whose
only job is to run your other code and complain loudly when it's wrong.

## What the compiler cannot catch

```java
static double average(int[] scores) {
    int sum = 0;
    for (int s : scores) sum += s;
    return sum / scores.length;        // compiles. runs. wrong.
}
```

Integer division silently truncates: `average({1, 2})` is `1.0`, not
`1.5`. The compiler saw valid types and valid syntax - the *logic* is your
problem. Tests are how logic bugs get caught, ideally before your users
find them.

## JUnit: the shape

JUnit 5 is the standard Java test framework. In real Maven projects the
tests live in `src/test/java`, one test class per production class:

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ScoreAverageTest {

    @Test
    void averagesTwoScores() {
        assertEquals(1.5, ScoreAverage.average(new int[]{1, 2}));
    }

    @Test
    void emptyScoresThrow() {
        assertThrows(IllegalArgumentException.class,
            () -> ScoreAverage.average(new int[0]));
    }
}
```

The vocabulary:

- `@Test` - marks a method the runner executes. Each test is independent
  and runs in a fresh instance.
- `assertEquals(expected, actual)` - the workhorse. Note the order:
  **expected first**. The failure message prints both, so order makes
  failures readable.
- `assertTrue` / `assertFalse`, `assertNull` / `assertNotNull`,
  `assertThrows` - the rest of the everyday set.
- `@BeforeEach` - a method run before *each* test: build fresh fixtures
  there instead of copy-pasting setup.

## Arrange, Act, Assert

Read every test as three beats:

```java
@Test
void withdrawReducesBalance() {
    // Arrange
    Account a = new Account(100);
    // Act
    a.withdraw(30);
    // Assert
    assertEquals(70, a.balance());
}
```

One behavior per test. If you can't name the test's single behavior in a
sentence, it's two tests.
"""

L_WHY_VI = r"""
Bạn vốn đã test - mỗi lần chạy chương trình và nheo mắt nhìn output là
bạn đang test. Vấn đề: **bạn** phải chạy lại mọi thứ sau mỗi lần sửa, và
rồi bạn sẽ lười. Test tự động là những chương trình mà công việc duy nhất
là chạy code khác của bạn và la lên to khi nó sai.

## Những gì compiler không bắt được

```java
static double average(int[] scores) {
    int sum = 0;
    for (int s : scores) sum += s;
    return sum / scores.length;        // biên dịch được. chạy được. sai.
}
```

Chia số nguyên âm thầm cắt cụt: `average({1, 2})` là `1.0`, không phải
`1.5`. Compiler thấy kiểu hợp lệ, cú pháp hợp lệ - còn *logic* là vấn đề
của bạn. Test là cách bắt bug logic, tốt nhất là trước khi người dùng tìm
ra chúng.

## JUnit: hình dạng

JUnit 5 là framework test chuẩn của Java. Trong dự án Maven thật, test
nằm ở `src/test/java`, một lớp test cho mỗi lớp thật:

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ScoreAverageTest {

    @Test
    void averagesTwoScores() {
        assertEquals(1.5, ScoreAverage.average(new int[]{1, 2}));
    }

    @Test
    void emptyScoresThrow() {
        assertThrows(IllegalArgumentException.class,
            () -> ScoreAverage.average(new int[0]));
    }
}
```

Từ vựng:

- `@Test` - đánh dấu phương thức mà runner thực thi. Mỗi test độc lập,
  chạy trên một đối tượng mới.
- `assertEquals(expected, actual)` - chú diễn viên chính. Chú ý thứ tự:
  **expected đứng trước**. Message lỗi in cả hai, nên đúng thứ tự thì lỗi
  mới dễ đọc.
- `assertTrue` / `assertFalse`, `assertNull` / `assertNotNull`,
  `assertThrows` - phần còn lại của bộ hằng ngày.
- `@BeforeEach` - chạy trước *mỗi* test: dựng fixture mới ở đó thay vì
  copy-paste phần chuẩn bị.

## Arrange, Act, Assert

Đọc mỗi test như ba nhịp:

```java
@Test
void withdrawReducesBalance() {
    // Arrange
    Account a = new Account(100);
    // Act
    a.withdraw(30);
    // Assert
    assertEquals(70, a.balance());
}
```

Một hành vi cho mỗi test. Nếu bạn không gọi tên được hành vi duy nhất đó
trong một câu, thì đó là hai test.
"""

# ── lesson 13.2 — edge cases ────────────────────────────────────────────────
L_EDGE_EN = r"""
Beginners test the happy path. Engineers test the **boundaries** - because
that's where the bugs actually live.

## The four families to check every time

For a function `parseAge(String)` returning `Integer`:

1. **Empty and missing** - `""`, `"   "`, `null`.
2. **Wrong shape** - `"abc"`, `"12x"`, `"1.5"` (a double where an int
   belongs), `"+5"`.
3. **Edges of the valid range** - exactly `0`, exactly `150`, then the
   first invalid on each side: `-1`, `151`.
4. **In the middle** - one boring valid value, so you know the machinery
   works when the edges do.

```java
assertEquals(0,  Score.parseAge("0"));      // inclusive edge
assertEquals(150, Score.parseAge("150"));   // other inclusive edge
assertEquals(null, Score.parseAge("-1"));   // one past
assertEquals(null, Score.parseAge("151"));  // other past
```

Off-by-one bugs *only* show at the exact edges: `<` vs `<=` is invisible
in the middle of the range and glaring at `150`.

## Numeric landmines

- **Zero** - the input that divides, averages, and indexes by surprise.
- **Negative values** - legal for temperatures, illegal for ages; decide
  and enforce.
- **Very large** - `Integer.MAX_VALUE + 1` wraps to negative; sums can
  overflow even when every input is small (`int` holds ~2.1 billion).
- **Doubles are approximations** - `0.1 + 0.2 != 0.3`. Compare with a
  tolerance (`assertEquals(0.3, x, 1e-9)` in JUnit terms) or use exact
  types for money.

## Collections and strings

- **Empty collection** - `List.of()`, not just a full one.
- **Single element** - the smallest non-empty case; loops and streams
  often misbehave exactly here.
- **Duplicates** - "count the unique words" must survive `"the the"`.
- **Whitespace and case** - `"  Ada "`, `"ada"` vs `"Ada"`: decide whether
  they're equal and test the decision.

A test suite with only happy paths verifies the demo, not the program.
"""

L_EDGE_VI = r"""
Người mới test đường vui. Kỹ sư test **biên giới** - vì bug thực sự sống
ở đó.

## Bốn họ cần kiểm tra mỗi lần

Với hàm `parseAge(String)` trả về `Integer`:

1. **Rỗng và thiếu** - `""`, `"   "`, `null`.
2. **Sai hình dạng** - `"abc"`, `"12x"`, `"1.5"` (double ở chỗ cần int),
   `"+5"`.
3. **Hai mép của khoảng hợp lệ** - đúng `0`, đúng `150`, rồi giá trị bất
   hợp lệ đầu tiên mỗi phía: `-1`, `151`.
4. **Ở giữa** - một giá trị hợp lệ bình thường, để biết cỗ máy vẫn chạy
   khi các mép đều đúng.

```java
assertEquals(0,  Score.parseAge("0"));      // mép chứa trong
assertEquals(150, Score.parseAge("150"));   // mép kia chứa trong
assertEquals(null, Score.parseAge("-1"));   // lệch một đơn vị
assertEquals(null, Score.parseAge("151"));  // phía kia
```

Bug lệch-một-đơn vị *chỉ* xuất hiện đúng tại mép: `<` với `<=` vô hình ở
giữa khoảng nhưng lóe sáng tại `150`.

## Mỏ đất nổ bằng số

- **Số 0** - input chia, lấy trung bình, đánh chỉ số bất ngờ.
- **Số âm** - hợp lệ cho nhiệt độ, bất hợp lệ cho tuổi; hãy quyết định và
  thực thi.
- **Số rất lớn** - `Integer.MAX_VALUE + 1` tràn thành số âm; tổng có thể
  tràn dù mọi input nhỏ (`int` chỉ giữ ~2,1 tỷ).
- **Double là xấp xỉ** - `0.1 + 0.2 != 0.3`. So sánh với dung sai, hoặc
  dùng kiểu chính xác cho tiền tệ.

## Collection và chuỗi

- **Collection rỗng** - `List.of()`, đừng chỉ test danh sách đầy.
- **Một phần tử** - trường hợp không-rỗng nhỏ nhất; vòng lặp và stream
  thường hỏng đúng ở đây.
- **Trùng lặp** - "đếm từ duy nhất" phải sống sót qua `"the the"`.
- **Khoảng trắng và hoa thường** - `"  Ada "`, `"ada"` với `"Ada"`: hãy
  quyết định chúng có bằng nhau không và test đúng quyết định đó.

Bộ test chỉ có đường vui chỉ xác minh được phần demo, không phải chương
trình.
"""

# ── lesson 13.3 — debugging method ──────────────────────────────────────────
L_DEBUG_EN = r"""
A bug report says "the total is wrong." Where do you even start? With a
method, not a mood.

## The loop that works

1. **Reproduce** - find the smallest input that triggers the bug. A bug
   you can trigger on demand is already half-dead.
2. **Read the evidence** - the stack trace, the wrong value itself. "Total
   is 0" says more than "total is wrong": zero usually means a loop never
   ran, an accumulate-variable was never assigned, or a lookup missed.
3. **Form one hypothesis** - a specific, falsifiable sentence: "the sum is
   0 because `items` is empty when `filter` rejects everything."
4. **Test it cheaply** - print the intermediate value once (`System.out.println`),
   or step in a debugger. Did `items.size()` equal 0? Hypothesis confirmed
   or killed - either way you've learned.
5. **Fix the cause, not the symptom** - re-initializing the variable at
   the call site might hide this crash while the empty-collection bug
   lives on elsewhere.
6. **Prove it dead** - add a test that fails with the bug and passes
   without it. This is the regression test, and it's how the same bug
   never wastes your time twice.

## The debugger you already own

Real projects use IDE debuggers (breakpoints, step-over, variable
inspection). In this course the sandbox gives you two tools:

- `System.out.println("items=" + items + " size=" + items.size())` -
  one-line, throwaway, gone before you commit.
- A failing **test** with a precise message - the `CjTestBase.checkEq`
  failures you've seen all course are exactly this: `expected X but got Y`
  at the exact statement.

## Reading someone else's stack trace

Bottom-up: your classes first, then libraries. The top *exception line*
names the crime (`NumberFormatException: For input string: "12x"`); the
bottom frames name the crime scene (`Main.parseCount(Main.java:8)`). When
a *cause* chain appears (`Caused by: ...`), read the deepest `Caused by`
first - that's usually the true origin.
"""

L_DEBUG_VI = r"""
Một báo lỗi nói "tổng bị sai." Bắt đầu từ đâu? Từ một phương pháp, không
phải từ một tâm trạng.

## Vòng lặp có hiệu quả

1. **Tái hiện** - tìm input nhỏ nhất gây ra bug. Bug mà bạn gọi là tới
   đã chết một nửa.
2. **Đọc bằng chứng** - stack trace, chính giá trị sai. "Tổng là 0" nói
   nhiều hơn "tổng sai": số 0 thường nghĩa là vòng lặp chưa từng chạy,
   biến tích lũy chưa từng được gán, hoặc một lần tra cứu hụt.
3. **Đặt ra một giả thuyết** - một câu cụ thể, có thể bác bỏ: "tổng là 0
   vì `items` rỗng khi `filter` chặn hết mọi thứ."
4. **Thử giả thuyết giá rẻ** - in giá trị trung gian một lần
   (`System.out.println`), hoặc step trong debugger. `items.size()` có
   bằng 0 không? Giả thuyết được xác nhận hoặc bị xử tử - cả hai đều là
   kiến thức.
5. **Sửa nguyên nhân, không phải triệu chứng** - gán lại biến tại chỗ gọi
   có thể che được lần crash này trong khi bug collection-rỗng vẫn sống
   ở nơi khác.
6. **Chứng minh nó đã chết** - thêm một test fail khi có bug và pass khi
   không có. Đó là regression test, và đó là cách cùng một bug không bao
   giờ浪费 thời gian bạn hai lần.

## Debugger bạn sẵn có

Dự án thật dùng debugger của IDE (breakpoint, step-over, soi biến). Trong
khóa này sandbox cho bạn hai công cụ:

- `System.out.println("items=" + items + " size=" + items.size())` -
  một dòng, dùng một lần, biến mất trước khi commit.
- Một **test** fail với message chính xác - những lỗi `checkEq` bạn thấy
  suốt khóa học đúng là thứ đó: `expected X but got Y` ngay tại câu lệnh.

## Đọc stack trace của người khác

Từ dưới lên: lớp của bạn trước, thư viện sau. Dòng exception trên cùng
nêu tên tội phạm (`NumberFormatException: For input string: "12x"`); các
frame dưới cùng nêu hiện trường (`Main.parseCount(Main.java:8)`). Khi có
chuỗi *cause* (`Caused by: ...`), đọc `Caused by` sâu nhất trước - đó
thường là nguồn gốc thật.
"""

# ── challenges ───────────────────────────────────────────────────────────────
BOILER_AVG = r"""public class Solution {
    public static double average(int[] scores) {
        if (scores == null || scores.length == 0) {
            throw new IllegalArgumentException("scores must be non-empty");
        }
        int sum = 0;
        for (int s : scores) sum += s;
        return sum / scores.length;
    }
}
"""

P13_WRITE = challenge(
    "javb-m13-write-tests",
    "Be the test suite",
    "The provided `average` has a real logic bug (integer division truncates). Write `main` that acts as a test suite: print one line per case, `PASS`/`FAIL name` per check, covering (1) average({1,2}) == 1.5, (2) average({5}) == 5.0, (3) average throws IllegalArgumentException for an empty array. Run it, watch case 1 FAIL, then fix `average` (cast before dividing) so all three print PASS.",
    BOILER_AVG,
    [
        (
            "the fixed average is exact",
            r"""
CjTestBase.checkEq(Solution.average(new int[]{1, 2}), 1.5, "1 and 2 average 1.5");
CjTestBase.checkEq(Solution.average(new int[]{5}), 5.0, "single score");
CjTestBase.checkEq(Solution.average(new int[]{-3, 3}), 0.0, "negatives cancel");
""",
            "Cast BEFORE dividing: sum / (double) scores.length keeps the fraction.",
        ),
        (
            "empty input still throws",
            r"""
try {
    Solution.average(new int[0]);
    CjTestBase.checkTrue(false, "empty must throw");
} catch (IllegalArgumentException e) {
    CjTestBase.checkTrue(true, "empty throws as documented");
}
""",
            "Keep the guard as-is - the fix is the division, not the guard.",
        ),
    ],
    level="debugging",
    difficulty="intermediate",
)

P13_WRITE_VI = vi_challenge(
    "Chính bạn là bộ test",
    "Hàm `average` được cung cấp có một bug logic thật (chia số nguyên cắt cụt). Hãy viết `main` hoạt động như một bộ test: in mỗi trường hợp một dòng `PASS`/`FAIL name`, phủ (1) average({1,2}) == 1.5, (2) average({5}) == 5.0, (3) average ném IllegalArgumentException cho mảng rỗng. Chạy, thấy case 1 FAIL, rồi sửa `average` (ép kiểu trước khi chia) để cả ba in PASS.",
    [("average sau khi sửa là chính xác", "Ép kiểu TRƯỚC khi chia: sum / (double) scores.length giữ phần lẻ."),
     ("input rỗng vẫn ném lỗi", "Giữ nguyên phần chặn - cần sửa là phép chia, không phải phần chặn.")],
)

BOILER_STATS = r"""public class Solution {
    public static int countUniqueWords(String text) {
        if (text == null || text.isBlank()) return 0;
        String[] words = text.trim().toLowerCase().split("\s+");
        java.util.Set<String> unique = new java.util.HashSet<>();
        for (String w : words) unique.add(w);
        return unique.size();
    }
}
"""

P13_EDGE = challenge(
    "javb-m13-edge-hunter",
    "Hunt the boundaries",
    "`countUniqueWords` passes every happy-path test. Write `main` printing one PASS/FAIL line per edge case you believe it must survive: empty string, only whitespace, single word, duplicated words (\"the the\"), mixed case (\"The THE\"), and words with punctuation adjacent (\"hello,world\"). Run it - at least one case should surprise you - then harden `countUniqueWords` so every one of your cases prints PASS (treat \"hello,world\" as two words by splitting on any non-letter).",
    BOILER_STATS,
    [
        (
            "core counting still works",
            r"""
CjTestBase.checkEq(Solution.countUniqueWords("the quick brown fox"), 4, "four unique words");
CjTestBase.checkEq(Solution.countUniqueWords("the the THE"), 1, "case-insensitive duplicates");
""",
            "Keep the lowercase normalization - the hardening is about splitting, not case.",
        ),
        (
            "punctuation no longer glues words",
            r"""
CjTestBase.checkEq(Solution.countUniqueWords("hello,world"), 2, "comma splits words");
CjTestBase.checkEq(Solution.countUniqueWords("it's"), 2, "apostrophe splits too");
""",
            "split(\"[^a-z]+\") after lowercasing splits on every non-letter run.",
        ),
        (
            "empty and blank survive",
            r"""
CjTestBase.checkEq(Solution.countUniqueWords(""), 0, "empty -> 0");
CjTestBase.checkEq(Solution.countUniqueWords("   "), 0, "blank -> 0");
CjTestBase.checkEq(Solution.countUniqueWords(null), 0, "null -> 0");
""",
            "Guard first; then the split never sees a blank string.",
        ),
    ],
    level="real-world",
    difficulty="advanced",
)

P13_EDGE_VI = vi_challenge(
    "Săn biên giới",
    "`countUniqueWords` pass mọi test đường vui. Hãy viết `main` in mỗi trường hợp biên giới một dòng PASS/FAIL mà bạn tin nó phải sống sót: chuỗi rỗng, chỉ khoảng trắng, một từ, từ trùng (\"the the\"), hoa thường lẫn lộn (\"The THE\"), và từ dính dấu câu (\"hello,world\"). Chạy - ít nhất một case sẽ khiến bạn bất ngờ - rồi gia cố `countUniqueWords` để mọi case của bạn đều in PASS (coi \"hello,world\" là hai từ bằng cách tách theo mọi ký tự không phải chữ cái).",
    [("việc đếm cốt lõi vẫn đúng", "Giữ lowercase hóa - phần gia cố nằm ở phép tách, không phải hoa thường."),
     ("dấu câu không còn dính các từ", "split(\"[^a-z]+\") sau khi lowercase sẽ tách theo mọi chuỗi ký tự không phải chữ cái."),
     ("rỗng và khoảng trắng sống sót", "Chặn trước; phép split sẽ không bao giờ gặp chuỗi trắng.")],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
BOILER_MONEY = r"""public class Solution {
    public static String changeFor(int cents) {
        int quarters = cents / 25;
        cents %= 25;
        int dimes = cents / 10;
        cents %= 10;
        int nickels = cents / 5;
        int pennies = cents % 5;
        return quarters + "q " + dimes + "d " + nickels + "n " + pennies + "p";
    }
}
"""

P13_CP_CH = challenge(
    "javb-m13-cp-debug-lab",
    "Checkpoint: debug & repair lab",
    "Three customers report: `changeFor(0)` prints `\"0q 0d 0n 0p\"` (good), `changeFor(97)` prints `\"3q 2d 1n 2p\"` (good), but `changeFor(-5)` prints `\"0q 0d -1n 0p\"` (nonsense) and `changeFor(41)` prints `\"1q 1d 1n 2p\"`... except one of these two reports is a lie. Reproduce with `main`, find the real defect, and fix it so: negative input throws `IllegalArgumentException` with a message containing \"negative\", and every amount 0..99 produces the exact correct breakdown (verified by your own main and by the tests).",
    BOILER_MONEY,
    [
        (
            "documented cases stay exact",
            r"""
CjTestBase.checkEq(Solution.changeFor(0), "0q 0d 0n 0p", "zero is all zeros");
CjTestBase.checkEq(Solution.changeFor(97), "3q 2d 0n 2p", "97c = 3q 2d 0n 2p");
CjTestBase.checkEq(Solution.changeFor(41), "1q 1d 1n 1p", "41c = 1q 1d 1n 1p");
""",
            "41 cents: 1 quarter (25) leaves 16 -> 1 dime (10) leaves 6 -> 1 nickel (5) leaves 1 penny.",
        ),
        (
            "the negative report was true",
            r"""
try {
    Solution.changeFor(-5);
    CjTestBase.checkTrue(false, "negative must throw");
} catch (IllegalArgumentException e) {
    CjTestBase.checkTrue(e.getMessage().contains("negative"), "message says negative");
}
""",
            "Guard at the top: if (cents < 0) throw new IllegalArgumentException(...).",
        ),
        (
            "every amount 0..99 breaks down exactly",
            r"""
for (int c = 0; c <= 99; c++) {
    String s = Solution.changeFor(c);
    String[] parts = s.split(" ");
    int q = Integer.parseInt(parts[0].replace("q", ""));
    int d = Integer.parseInt(parts[1].replace("d", ""));
    int n = Integer.parseInt(parts[2].replace("n", ""));
    int p = Integer.parseInt(parts[3].replace("p", ""));
    if (q * 25 + d * 10 + n * 5 + p != c) {
        CjTestBase.checkTrue(false, "changeFor(" + c + ") wrong: " + s);
    }
}
CjTestBase.checkEq(Solution.changeFor(25), "1q 0d 0n 0p", "quarter boundary");
CjTestBase.checkEq(Solution.changeFor(5), "0q 0d 1n 0p", "nickel boundary");
CjTestBase.checkEq(Solution.changeFor(99), "3q 2d 0n 4p", "top of range");
""",
            "When one coin type is wrong, the exhaustive sweep finds exactly where.",
        ),
    ],
    level="debugging",
    difficulty="advanced",
)

P13_CP_VI = vi_challenge(
    "Checkpoint: phòng thí nghiệm gỡ lỗi",
    "Ba khách hàng báo cáo: `changeFor(0)` in `\"0q 0d 0n 0p\"` (đúng), `changeFor(97)` in `\"3q 2d 1n 2p\"` (đúng), nhưng `changeFor(-5)` in `\"0q 0d -1n 0p\"` (vô lý) và `changeFor(41)` in `\"1q 1d 1n 2p\"`... trừ việc một trong hai báo cáo này là bịa. Tái hiện bằng `main`, tìm defect thật, và sửa để: input âm ném `IllegalArgumentException` với message chứa \"negative\", và mọi số 0..99 cho ra phân tích chính xác (được chính main của bạn và các test xác minh).",
    [("các case có tài liệu vẫn chính xác", "41 xu: 1 quarter (25) còn 16 -> 1 dime (10) còn 6 -> 1 nickel (5) còn 1 penny."),
     ("báo cáo số âm là thật", "Chặn ở đầu hàm: if (cents < 0) throw new IllegalArgumentException(...)."),
     ("mọi số 0..99 được phân tích chính xác", "Khi một loại xu sai, quét vét toàn bộ 0..99 sẽ chỉ ra chính xác chỗ nào.")],
)

P13_CP_R = r"""public class Solution {
    public static String changeFor(int cents) {
        if (cents < 0) {
            throw new IllegalArgumentException("amount must not be negative: " + cents);
        }
        int quarters = cents / 25;
        cents %= 25;
        int dimes = cents / 10;
        cents %= 10;
        int nickels = cents / 5;
        int pennies = cents % 5;
        return quarters + "q " + dimes + "d " + nickels + "n " + pennies + "p";
    }
}
"""

P13_CP_W = r"""public class Solution {
    public static String changeFor(int cents) {
        if (cents < 0) {
            throw new IllegalArgumentException("amount must not be negative: " + cents);
        }
        int quarters = cents / 25;
        cents %= 25;
        int dimes = cents / 10;
        int nickels = cents / 5;      // BUG: forgot cents %= 10 - nickels double-count dimes
        int pennies = cents % 5;
        return quarters + "q " + dimes + "d " + nickels + "n " + pennies + "p";
    }
}
"""

CK_M13_MD = r"""
The repair lab - reproduce, hypothesize, fix, and *prove* the fix.

Inside the provided `Solution` skeleton, repair `changeFor` per the
checkpoint. Two defects hide in the customer reports: one is real
(negative input flows into `%` and prints negative coin counts), one is a
lie (41 cents is actually miscounted in a sneakier way - your exhaustive
0..99 sweep in the tests is what catches arithmetic bugs a few spot
checks never will).

Method reminder: reproduce first, form one hypothesis at a time, fix the
cause, then add the test that would have caught it. The third test block
is that test - it reconstructs every amount from its coin breakdown, so
any future regression in the coinage logic fails loudly.
"""

CK_M13_MD_VI = r"""
Phòng thí nghiệm sửa chữa - tái hiện, đặt giả thuyết, sửa, và *chứng
minh* bản sửa.

Bên trong khung `Solution`, sửa `changeFor` theo checkpoint. Hai defect
nấp trong các báo cáo của khách: một cái thật (input âm chảy vào `%` và
in ra số xu âm), một cái bịa (41 xu thực ra bị đếm sai theo cách tinh vi
hơn - quét vét 0..99 trong test mới bắt được các bug số học mà vài lần
kiểm tra điểm danh không bao giờ thấy).

Nhắc lại phương pháp: tái hiện trước, mỗi lần một giả thuyết, sửa nguyên
nhân, rồi thêm test lẽ ra đã bắt được nó. Khối test thứ ba chính là test
đó - nó dựng lại mọi số tiền từ phân tích xu của nó, nên bất kỳ regression
nào trong logic đổi xu cũng fail ầm ĩ.
"""

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Testing & Debugging",
    "Why tests catch what compilers can't, JUnit's shape, boundary discipline, and a debugging loop that survives real bugs.",
    "Kiểm thử & gỡ lỗi",
    "Vì sao test bắt được thứ compiler không bắt được, hình dạng của JUnit, kỷ luật biên giới, và vòng gỡ lỗi sống sót qua bug thật.",
    ["why-tests", "edge-cases", "debugging-method", "java-checkpoint-testing"],
    ["javb-p13-testing"],
)

write_lesson(
    MOD, "why-tests",
    "Why Tests & JUnit's Shape",
    "The compiler's blind spot, @Test and the assertion family, and Arrange-Act-Assert.",
    18,
    L_WHY_EN,
    "Vì sao test & hình dạng của JUnit",
    "Điểm mù của compiler, @Test và họ assertion, và Arrange-Act-Assert.",
    L_WHY_VI,
)

write_lesson(
    MOD, "edge-cases",
    "Testing the Boundaries",
    "The four edge families, numeric landmines, and the collection/string cases beginners skip.",
    16,
    L_EDGE_EN,
    "Kiểm thử biên giới",
    "Bốn họ biên giới, mỏ đất nổ bằng số, và các case collection/chuỗi mà người mới hay bỏ qua.",
    L_EDGE_VI,
)

write_lesson(
    MOD, "java-debugging-method",
    "A Debugging Method That Works",
    "Reproduce, read evidence, hypothesize, test cheaply, fix the cause, prove it dead.",
    16,
    L_DEBUG_EN,
    "Phương pháp gỡ lỗi có hiệu quả",
    "Tái hiện, đọc bằng chứng, đặt giả thuyết, thử giá rẻ, sửa nguyên nhân, chứng minh nó đã chết.",
    L_DEBUG_VI,
)

write_practice(
    MOD, "javb-p13-testing",
    "Practice: Prove It Works",
    "Hand-write a test main that catches a truncation bug, then hunt boundaries in a word counter.",
    "Thực hành: Chứng minh nó chạy đúng",
    "Tự viết test main bắt bug cắt cụt, rồi săn biên giới trong bộ đếm từ.",
    "why-tests", 40, "beginner",
    [P13_WRITE, P13_EDGE],
    {P13_WRITE["id"]: P13_WRITE_VI, P13_EDGE["id"]: P13_EDGE_VI},
    solutions=[
        (
            P13_WRITE["id"],
            r"""public class Solution {
    public static double average(int[] scores) {
        if (scores == null || scores.length == 0) {
            throw new IllegalArgumentException("scores must be non-empty");
        }
        int sum = 0;
        for (int s : scores) sum += s;
        return sum / (double) scores.length;
    }
}
""",
            r"""public class Solution {
    public static double average(int[] scores) {
        if (scores == null || scores.length == 0) {
            throw new IllegalArgumentException("scores must be non-empty");
        }
        int sum = 0;
        for (int s : scores) sum += s;
        return sum / scores.length;   // BUG: integer division truncates 1.5 to 1.0
    }
}
""",
        ),
        (
            P13_EDGE["id"],
            r"""public class Solution {
    public static int countUniqueWords(String text) {
        if (text == null || text.isBlank()) return 0;
        String[] words = text.trim().toLowerCase().split("[^a-z]+");
        java.util.Set<String> unique = new java.util.HashSet<>();
        for (String w : words) {
            if (!w.isEmpty()) unique.add(w);
        }
        return unique.size();
    }
}
""",
            r"""public class Solution {
    public static int countUniqueWords(String text) {
        if (text == null || text.isBlank()) return 0;
        // BUG: splits on whitespace only - "hello,hello" counts as ONE word
        String[] words = text.trim().toLowerCase().split("\s+");
        java.util.Set<String> unique = new java.util.HashSet<>();
        for (String w : words) unique.add(w);
        return unique.size();
    }
}
""",
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-testing",
    "Checkpoint: Debug & Repair Lab",
    "Separate true reports from lies, fix the real defect, and leave behind an exhaustive regression net.",
    45, CK_M13_MD,
    "Checkpoint: Phòng thí nghiệm gỡ lỗi",
    "Tách báo cáo thật khỏi báo cáo bịa, sửa defect thật, và để lại một lưới regression quét vét.",
    CK_M13_MD_VI,
    P13_CP_CH, P13_CP_VI,
    solution=P13_CP_R, wrong=P13_CP_W,
)

print("module 13 complete")
