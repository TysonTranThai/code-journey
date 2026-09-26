#!/usr/bin/env python3
"""AP CSA Core M12 — Integrated Java Problems (topics removed)."""
from apcc import *

M = "cx-mixed"

L1 = r"""
No module label this time. Each problem below mixes several machines;
**your first job is diagnosis, not coding.** The two-minute ritual:

1. **Read the contract; name the return type.** A count → counter
   machine. A String → builder machine. A boolean → flag/existence. A
   position → sentinel. A new collection → accumulator.
2. **Name the data.** Array vs ArrayList decides the loop family and
   the size API. String decides charAt/substring.
3. **Name the composition.** Does the answer need a pass over data AND
   a pass over positions (columns)? A filter inside a scan? A max over
   computed per-row values?
4. **Only now write code** — the machines assemble themselves once
   named.

Example diagnosis: *"Return the number of distinct values in the
strictly-positive half of the grid's first row."* →
return type: count (counter). Data: array row. Composition: filter
(positive) + dedup (backward-looking pairwise). The code is three
machines you already own — the reading is the work.
"""

L2 = r"""
Exam questions present **plausible near-misses**. The skill is
elimination by contract, not by vibes. The four elimination probes:

1. **The empty probe.** What happens with length 0 / "" / empty list?
   A solution that reads element 0 unguarded dies here.
2. **The single probe.** One element: does a seeded-max or adjacency
   scan handle it? Adjacency loops from 1 or to length − 1 do nothing —
   correct or not, depending on the contract.
3. **The all-equal probe.** Every value identical: tie-breaking (strict
   vs non-strict) decides.
4. **The order probe.** Run the trace on a *sorted* and a *reverse*
   input: order-dependent bugs (first vs last, min vs max) expose
   themselves in one of the two.

Apply to this candidate solution for *"index of the smallest value,
earliest on ties"*:

```java
int best = 0;
for (int i = 1; i < arr.length; i++) {
    if (arr[i] <= arr[best]) { best = i; }   // probe 3: fails
}
```

The all-equal probe `{7, 7}`: i=1, `7 <= 7` true, best becomes 1 — the
LAST tie. Contract says earliest. The `<=` must be `<`. One probe, one
character, one eliminated answer.
"""

L3 = r"""
Synthesis reading — trace a multi-machine program without running it:

```java
public static int process(int[] nums) {
    int marked = 0;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] % 2 == 0) {
            nums[i] = nums[i] / 2;
            marked++;
        } else {
            nums[i] = nums[i] * 2 + 1;
        }
    }
    int total = 0;
    for (int v : nums) {
        total += v;
    }
    return total - marked;
}

// call: process({3, 4, 5})
```

The trace table (two passes, one table):

| i | in | even? | out | marked |
| - | -- | ----- | --- | ------ |
| 0 | 3  | no    | 7   | 0      |
| 1 | 4  | yes   | 2   | 1      |
| 2 | 5  | no    | 11  | 0      |

Pass two: total = 7 + 2 + 11 = 20. Return 20 − 1 = **19**.

Two habits to keep: (1) the mutation pass CHANGES the array — a second
pass reads the mutated values, not the originals; (2) for-each in pass
two is fine (read-only). Programs like this are 3–4 MCQs on every exam,
and the table finishes them all.
"""

write_module(
    M,
    "Integrated Java Problems",
    "Unlabeled problems: diagnose the machines first, eliminate near-misses with the four probes, and trace multi-pass programs.",
    "Bài toán Java tổng hợp",
    "Bài toán không nhãn: chẩn đoán các cỗ máy trước, loạinear-miss bằng bốn phép dò, và truy vết chương trình đa-lượt.",
    lessons=["cx-m12-diagnose", "cx-m12-eliminate", "cx-m12-syntrace", "cx-cp-m12"],
    practices=["cx-p12-mixed"],
)

write_lesson(
    M, "cx-m12-diagnose", "Diagnose before code",
    "Return type → data → composition: naming the machines from the contract.",
    12, L1,
    "Chẩn đoán trước khi viết",
    "Kiểu trả về → dữ liệu → tổ hợp: gọi tên các cỗ máy từ hợp đồng.",
    r"""
Không còn nhãn module. Mỗi bài dưới đây trộn vài cỗ máy; **việc đầu tiên
của bạn là chẩn đoán, không phải gõ mã.** Nghi thức hai phút:

1. **Đọc hợp đồng; gọi tên kiểu trả về.** Một số đếm → cỗ máy đếm. Một
   String → cỗ máy dựng. Một boolean → cờ/tồn-tại. Một vị trí → lính
   canh. Một bộ sưu tập mới → bộ cộng dồn.
2. **Gọi tên dữ liệu.** Mảng với ArrayList quyết định họ vòng lặp và API
   kích thước. String quyết định charAt/substring.
3. **Gọi tên tổ hợp.** Đáp án có cần một lượt qua dữ liệu VÀ một lượt
   qua vị trí (cột) không? Một bộ lọc bên trong quét? Một max trên các
   giá trị tính theo hàng?
4. **Giờ mới viết mã** — khi đã gọi tên, các cỗ máy tự lắp ráp.

Ví dụ chẩn đoán: *"Trả về số giá trị phân biệt trong phần dương-nghiêm-
ngặt của hàng đầu tiên của lưới."* → kiểu trả về: số đếm (bộ đếm). Dữ
liệu: hàng mảng. Tổ hợp: lọc (dương) + khử trùng lặp (từng cặp nhìn về
sau). Mã là ba cỗ máy bạn đã sở hữu — việc đọc mới là công việc.
""",
)

write_lesson(
    M, "cx-m12-eliminate", "The four elimination probes",
    "Empty, single, all-equal, order: killing near-miss answers by contract.",
    12, L2,
    "Bốn phép dò loại answer",
    "Rỗng, đơn, toàn-bằng, thứ tự: giết các đáp án gần-đúng bằng hợp đồng.",
    r"""
Đề thi đưa ra các **near-miss đáng tin**. Kỹ năng là loại trừ theo hợp
đồng, không theo cảm tính. Bốn phép dò:

1. **Phép dò rỗng.** Chuyện gì xảy ra với độ dài 0 / "" / danh sách
   rỗng? Lời giải đọc phần tử 0 không chặn sẽ chết ở đây.
2. **Phép dò đơn.** Một phần tử: lời giải seed-max hay quét liền kề xử
   lý được không? Vòng liền kề chạy từ 1 hoặc đến length − 1 sẽ không
   làm gì — đúng hay sai tùy hợp đồng.
3. **Phép dò toàn-bằng.** Mọi giá trị giống hệt: phá-đồng-giá (nghiêm
   ngặt hay không) quyết định.
4. **Phép dò thứ tự.** Chạy truy vết trên đầu vào *đã sắp xếp* và *đảo
   ngược*: các lỗi phụ-thuộc-thứ-tự (đầu vs cuối, min vs max) tự phơi ra
   trong một trong hai.

Áp dụng cho ứng viên sau cho *"chỉ số của giá trị nhỏ nhất, sớm nhất khi
đồng giá"*:

```java
int best = 0;
for (int i = 1; i < arr.length; i++) {
    if (arr[i] <= arr[best]) { best = i; }   // phép dò 3: hỏng
}
```

Phép dò toàn-bằng `{7, 7}`: i=1, `7 <= 7` đúng, best thành 1 — đồng giá
CUỐI. Hợp đồng nói sớm nhất. Dấu `<=` phải là `<`. Một phép dò, một ký
tự, một đáp án bị loại.
""",
)

write_lesson(
    M, "cx-m12-syntrace", "Synthesis tracing",
    "Two passes, one table: mutation passes poison later reads.",
    12, L3,
    "Truy vết tổng hợp",
    "Hai lượt, một bảng: lượt biến đổi đầu độc các lượt đọc sau.",
    r"""
Đọc tổng hợp — truy vết một chương trình đa-cỗ-máy mà không chạy:

```java
public static int process(int[] nums) {
    int marked = 0;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] % 2 == 0) {
            nums[i] = nums[i] / 2;
            marked++;
        } else {
            nums[i] = nums[i] * 2 + 1;
        }
    }
    int total = 0;
    for (int v : nums) {
        total += v;
    }
    return total - marked;
}

// lời gọi: process({3, 4, 5})
```

Bảng truy vết (hai lượt, một bảng):

| i | in | chẵn? | out | marked |
| - | -- | ----- | --- | ------ |
| 0 | 3  | không | 7   | 0      |
| 1 | 4  | có    | 2   | 1      |
| 2 | 5  | không | 11  | 0      |

Lượt hai: total = 7 + 2 + 11 = 20. Trả về 20 − 1 = **19**.

Hai thói quen cần giữ: (1) lượt biến đổi LÀM ĐỔI mảng — lượt thứ hai
đọc các giá trị đã đổi, không phải gốc; (2) for-each ở lượt hai là ổn
(chỉ đọc). Các chương trình dạng này là 3–4 câu MCQ trong mọi đề thi,
và bảng xử lý hết tất cả.
""",
)

BOILER_DIAG = r"""public class Solution {
    // CONTRACT (yours to diagnose): return the number of DISTINCT
    // strictly-positive values in row 0 of grid. grid.length >= 1.
    // {{3, -1, 3, 5}} -> 2 ; {{2, 2, 2}} -> 1 ; {{-4}} -> 0
    public static int distinctPositive(int[][] grid) {
        return 0; // replace
    }
}
"""

BOILER_CANDID = r"""public class Solution {
    // CONTRACT: index of the SMALLEST value, earliest on ties.
    // The implementation is fixed and correct; make the tests express
    // the contract (this grades your probes).
    public static int minIndex(int[] arr) {
        int best = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < arr[best]) {
                best = i;
            }
        }
        return best;
    }
}
"""

BOILER_TWOPASS = r"""public class Solution {
    // CONTRACT: from the lesson trace — reproduce process():
    // pass 1: evens -> value / 2 (count them), odds -> value * 2 + 1
    // pass 2: sum all; return sum - countOfEvens.
    public static int process(int[] nums) {
        return 0; // replace
    }
}
"""

BOILER_FILTERSCAN = r"""public class Solution {
    // CONTRACT: the longest INCREASING RUN's length in arr.
    // {3, 1, 2, 3, 0, 5} -> 3 (the 1,2,3 stretch).
    // Empty -> 0, single element -> 1.
    public static int longestRisingRun(int[] arr) {
        return 0; // replace
    }
}
"""

BOILER_COMBO = r"""import java.util.ArrayList;

public class Solution {
    public static class Sale {
        private String item;
        private int cents;
        public Sale(String item, int cents) { this.item = item; this.cents = cents; }
        public String getItem() { return item; }
        public int getCents() { return cents; }
    }

    // CONTRACT: among sales of item, return the SMALLEST cents as a
    // double; -1.0 when the item never appears.
    public static double bestPrice(ArrayList<Sale> sales, String item) {
        return 0; // replace
    }
}
"""

BOILER_CP12 = r"""public class Solution {
    // CONTRACT: "grade book" synthesis.
    // names[i] scored scores[i] (parallel arrays; scores.length >= 1).
    // Return the name of the student with the HIGHEST score, earliest
    // on ties; append their score as "#n" — e.g. "Lan#92".
    public static String topStudent(String[] names, int[] scores) {
        return ""; // replace
    }
}
"""

P_DIAG = challenge(
    "cx-m12-distinct-positive",
    "Diagnose and implement",
    "No topic label. Implement `int distinctPositive(int[][] grid)` from its contract comment. Diagnose first: which machines compose here? Write your diagnosis in a comment above the code (ungraded, but the habit is the point).",
    BOILER_DIAG,
    [(
        "machines composed",
        r"""
CjTestBase.checkEq(Solution.distinctPositive(new int[][]{{3, -1, 3, 5}}), 2, "3 and 5");
CjTestBase.checkEq(Solution.distinctPositive(new int[][]{{2, 2, 2}}), 1, "all same");
CjTestBase.checkEq(Solution.distinctPositive(new int[][]{{-4}}), 0, "no positives");
CjTestBase.checkEq(Solution.distinctPositive(new int[][]{{}}), 0, "empty row");
""",
        "Counter + positive filter + backward-looking dedup, over grid[0] only.",
    )],
    level="combination",
)

P_CANDID = challenge(
    "cx-m12-probe-tests",
    "Write the probes",
    "`minIndex` is correct. Your job: the tests must PROVE the contract — including the all-equal tie probe and the single-element probe. The provided test is the happy path; add the missing probe tests (the checker verifies that your test set still passes with the reference and that you did not delete tests).",
    BOILER_CANDID,
    [(
        "happy path",
        r"""
CjTestBase.checkEq(Solution.minIndex(new int[]{5, 2, 8}), 1, "unique minimum");
""",
        "Add: all-equal {7,7,7} -> 0 (earliest tie); single {4} -> 0; negative {-3,-9} -> 1.",
    )],
    level="independent",
)

P_TWOPASS = challenge(
    "cx-m12-reproduce-process",
    "Reproduce the trace",
    "Implement `process` exactly as the lesson's trace describes: pass 1 transforms in place (evens halved and counted, odds doubled-plus-one), pass 2 sums, return sum − count. Verify your trace table predicts process({3, 4, 5}) == 19 before submitting.",
    BOILER_TWOPASS,
    [(
        "two passes composed",
        r"""
CjTestBase.checkEq(Solution.process(new int[]{3, 4, 5}), 19, "lesson trace");
CjTestBase.checkEq(Solution.process(new int[]{}), 0, "empty: 0 - 0");
CjTestBase.checkEq(Solution.process(new int[]{2}), 0, "2 -> 1, sum 1, minus 1");
""",
        "Mutate in place in pass 1; remember the second pass reads MUTATED values.",
    )],
    level="independent",
)

P_RUN = challenge(
    "cx-m12-rising-run",
    "Longest rising run",
    "Implement `int longestRisingRun(int[] arr)`: the length of the longest stretch of strictly increasing adjacent values. {3, 1, 2, 3, 0, 5} → 3. This is adjacency scanning + an accumulator + a seeded best — compose them; run the empty and single probes first.",
    BOILER_FILTERSCAN,
    [(
        "longest run found",
        r"""
CjTestBase.checkEq(Solution.longestRisingRun(new int[]{3, 1, 2, 3, 0, 5}), 3, "1,2,3");
CjTestBase.checkEq(Solution.longestRisingRun(new int[]{}), 0, "empty probe");
CjTestBase.checkEq(Solution.longestRisingRun(new int[]{9}), 1, "single probe");
CjTestBase.checkEq(Solution.longestRisingRun(new int[]{5, 4, 3}), 1, "all falling: runs of one");
CjTestBase.checkEq(Solution.longestRisingRun(new int[]{1, 1, 1}), 1, "equal is not rising");
""",
        "current run starts at 1; extend while arr[i] > arr[i-1]; reset to 1 otherwise; track best.",
    )],
    level="real-world",
)

P_COMBO = challenge(
    "cx-m12-best-price",
    "Object list + sentinel + min",
    "Implement `double bestPrice(ArrayList<Sale> sales, String item)`: smallest cents among that item's sales as a double, −1.0 when absent. Three machines: object for-each with a filter, a seeded min, and a sentinel for absence.",
    BOILER_COMBO,
    [(
        "best price found",
        r"""
ArrayList<Solution.Sale> sales = new ArrayList<Solution.Sale>();
sales.add(new Solution.Sale("pen", 300));
sales.add(new Solution.Sale("ink", 1200));
sales.add(new Solution.Sale("pen", 250));
CjTestBase.checkNear(Solution.bestPrice(sales, "pen"), 250.0, 1e-9, "min of pen");
CjTestBase.checkNear(Solution.bestPrice(sales, "ink"), 1200.0, 1e-9, "single match");
CjTestBase.checkNear(Solution.bestPrice(sales, "glue"), -1.0, 1e-9, "absent sentinel");
""",
        "Seed best = -1; when found, seed from the first match, keep strict <.",
    )],
    level="real-world",
)

CP12 = challenge(
    "cx-cp-m12-top-student",
    "Checkpoint: gradebook synthesis",
    "Implement `String topStudent(String[] names, int[] scores)`: name of the highest score (earliest tie) plus \"#\" and the score — \"Lan#92\". Diagnose: max-index machine + parallel-array discipline + String builder. Run all four probes on your own solution before submitting.",
    BOILER_CP12,
    [(
        "winner announced",
        r"""
CjTestBase.checkEq(Solution.topStudent(new String[]{"An", "Lan", "Binh"}, new int[]{88, 92, 71}), "Lan#92", "clear winner");
CjTestBase.checkEq(Solution.topStudent(new String[]{"An", "Lan"}, new int[]{92, 92}), "An#92", "earliest tie");
CjTestBase.checkEq(Solution.topStudent(new String[]{"Solo"}, new int[]{50}), "Solo#50", "single probe");
""",
        "Track bestI with strict >; return names[bestI] + \"#\" + scores[bestI].",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p12-mixed", "Mixed clinic",
    "Diagnosis drills, probe writing, two-pass reproduction, three-machine composition.",
    "Ph phòng tổng hợp",
    "Luyện chẩn đoán, viết phép dò, tái hiện đa-lượt, tổ hợp ba cỗ máy.",
    after_lesson="cx-m12-eliminate", minutes=65, difficulty="advanced",
    challenges=[P_DIAG, P_CANDID, P_TWOPASS, P_RUN, P_COMBO],
    vi_challenges={
        "cx-m12-distinct-positive": vi_challenge("Chẩn đoán rồi hiện thực",
            "Không nhãn chủ đề. Hiện thực `int distinctPositive(int[][] grid)` từ chú thích hợp đồng. Chẩn đoán trước: những cỗ máy nào ghép lại đây? Viết chẩn đoán thành chú thích trên mã (không chấm, nhưng thói quen mới là điểm).",
            [("machines composed", "Bộ đếm + lọc dương + khử trùng lặp nhìn-về-sau, chỉ trên grid[0].")]),
        "cx-m12-probe-tests": vi_challenge("Viết các phép dò",
            "`minIndex` đã đúng. Việc của bạn: các test phải CHỨNG MINH hợp đồng — kể cả phép dò đồng-giá-toàn-bằng và phép dò một-phần-tử. Test đã có là đường vui; thêm các test còn thiếu (bộ kiểm tra xác minh tập test của bạn vẫn pass với lời giải tham chiếu).",
            [("happy path", "Thêm: toàn-bằng {7,7,7} -> 0 (đồng giá sớm nhất); đơn {4} -> 0; âm {-3,-9} -> 1.")]),
        "cx-m12-reproduce-process": vi_challenge("Tái hiện phép truy vết",
            "Hiện thực `process` đúng như bảng truy vết trong bài học: lượt 1 biến đổi tại chỗ (chẵn chia đôi và đếm, lẻ nhân đôi cộng một), lượt 2 cộng dồn, trả về tổng − số-đếm. Xác minh bảng của bạn dự đoán process({3, 4, 5}) == 19 trước khi nộp.",
            [("two passes composed", "Biến đổi tại chỗ ở lượt 1; nhớ rằng lượt hai đọc các giá trị ĐÃ ĐỔI.")]),
        "cx-m12-rising-run": vi_challenge("Đoạn tăng dài nhất",
            "Hiện thực `int longestRisingRun(int[] arr)`: độ dài đoạn dài nhất các giá trị liền kề tăng nghiêm ngặt. {3, 1, 2, 3, 0, 5} → 3. Đây là quét-liền-kề + bộ cộng dồn + best có seed — ghép chúng; chạy phép dò rỗng và đơn trước.",
            [("longest run found", "Đoạn hiện tại bắt đầu ở 1; kéo dài khi arr[i] > arr[i-1]; đặt lại 1 nếu không; theo dõi best.")]),
        "cx-m12-best-price": vi_challenge("Danh sách đối tượng + lính canh + min",
            "Hiện thực `double bestPrice(ArrayList<Sale> sales, String item)`: cents nhỏ nhất trong các bản ghi của món hàng đó dưới dạng double, −1.0 khi vắng mặt. Ba cỗ máy: for-each đối tượng có lọc, min có seed, và lính canh cho vắng mặt.",
            [("best price found", "Seed best = -1; khi tìm thấy, seed từ lần khớp đầu, giữ dấu < nghiêm ngặt.")]),
    },
    solutions=[
        ("cx-m12-distinct-positive", BOILER_DIAG.replace("return 0; // replace",
            "int[] row = grid[0];\n        int distinct = 0;\n        for (int i = 0; i < row.length; i++) {\n            if (row[i] > 0) {\n                boolean seen = false;\n                for (int j = 0; j < i; j++) {\n                    if (row[j] == row[i]) { seen = true; break; }\n                }\n                if (!seen) { distinct++; }\n            }\n        }\n        return distinct;"),
         BOILER_DIAG.replace("return 0; // replace",
            "int[] row = grid[0];\n        int distinct = 0;\n        for (int i = 0; i < row.length; i++) {\n            if (row[i] > 0) {\n                boolean seen = false;\n                for (int j = 0; j < i; j++) {\n                    if (row[j] == row[i]) { seen = true; break; }\n                }\n                if (!seen) { distinct += 2; }\n            }\n        }\n        return distinct;")),
        ("cx-m12-probe-tests", BOILER_CANDID,
         BOILER_CANDID.replace("if (arr[i] < arr[best]) {", "if (arr[i] > arr[best]) {")),
        ("cx-m12-reproduce-process", BOILER_TWOPASS.replace("return 0; // replace",
            "int marked = 0;\n        for (int i = 0; i < nums.length; i++) {\n            if (nums[i] % 2 == 0) {\n                nums[i] = nums[i] / 2;\n                marked++;\n            } else {\n                nums[i] = nums[i] * 2 + 1;\n            }\n        }\n        int total = 0;\n        for (int v : nums) {\n            total += v;\n        }\n        return total - marked;"),
         BOILER_TWOPASS.replace("return 0; // replace",
            "int marked = 0;\n        for (int i = 0; i < nums.length; i++) {\n            if (nums[i] % 2 == 0) {\n                nums[i] = nums[i] / 2;\n                marked++;\n            } else {\n                nums[i] = nums[i] * 2 + 1;\n            }\n        }\n        int total = 0;\n        for (int v : nums) {\n            total += v;\n        }\n        return total + marked;")),
        ("cx-m12-rising-run", BOILER_FILTERSCAN.replace("return 0; // replace",
            "if (arr.length == 0) { return 0; }\n        int best = 1;\n        int current = 1;\n        for (int i = 1; i < arr.length; i++) {\n            if (arr[i] > arr[i - 1]) {\n                current++;\n                if (current > best) { best = current; }\n            } else {\n                current = 1;\n            }\n        }\n        return best;"),
         BOILER_FILTERSCAN.replace("return 0; // replace",
            "if (arr.length == 0) { return 0; }\n        int best = 1;\n        int current = 1;\n        for (int i = 1; i < arr.length; i++) {\n            if (arr[i] >= arr[i - 1]) {\n                current++;\n                if (current > best) { best = current; }\n            } else {\n                current = 1;\n            }\n        }\n        return best;")),
        ("cx-m12-best-price", BOILER_COMBO.replace("return 0; // replace",
            "double best = -1.0;\n        for (Sale s : sales) {\n            if (s.getItem().equals(item)) {\n                if (best < 0 || s.getCents() < best) {\n                    best = s.getCents();\n                }\n            }\n        }\n        return best;"),
         BOILER_COMBO.replace("return 0; // replace",
            "double best = -1.0;\n        for (Sale s : sales) {\n            if (s.getItem().equals(item)) {\n                if (best < 0 || s.getCents() > best) {\n                    best = s.getCents();\n                }\n            }\n        }\n        return best;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m12", "Checkpoint: gradebook synthesis",
    "Parallel arrays + max-index + String building, no topic label.",
    30,
    r"""
topStudent compresses the whole course so far into one method: the
max-index machine from Module 6, parallel-array discipline (two indexes
move together), strict > for earliest tie, and a String result assembled
from two arrays. If you diagnosed return-type → data → composition
before typing, this took five minutes. If you typed first and debugged
after, compare the time — the diagnosis IS the exam skill.
""",
    "Điểm kiểm tra: tổng hợp sổ điểm",
    "Hai mảng song song + max-index + dựng chuỗi, không nhãn chủ đề.",
    r"""
topStudent nén toàn bộ khóa học tới thời điểm này vào một phương thức:
cỗ máy max-index từ Module 6, kỷ luật mảng-song-song (hai chỉ số di
chuyển cùng nhau), dấu > nghiêm ngặt cho đồng giá sớm nhất, và kết quả
String lắp từ hai mảng. Nếu bạn chẩn đoán kiểu-trả-về → dữ liệu → tổ hợp
trước khi gõ, việc này mất năm phút. Nếu gõ trước và gỡ lỗi sau, hãy so
thời gian — chẩn đoán CHÍNH LÀ kỹ năng thi.
""",
    CP12,
    vi_challenge("Điểm kiểm tra: tổng hợp sổ điểm",
        "Hiện thực `String topStudent(String[] names, int[] scores)`: tên của điểm cao nhất (đồng giá sớm nhất) cộng \"#\" và điểm — \"Lan#92\". Chẩn đoán: cỗ máy max-index + kỷ luật mảng-song-song + bộ dựng chuỗi. Tự chạy cả bốn phép dò trên lời giải của mình trước khi nộp.",
        [("winner announced", "Theo dõi bestI bằng dấu > nghiêm ngặt; trả về names[bestI] + \"#\" + scores[bestI].")]),
    solution=r"""public class Solution {
    public static String topStudent(String[] names, int[] scores) {
        int bestI = 0;
        for (int i = 1; i < scores.length; i++) {
            if (scores[i] > scores[bestI]) {
                bestI = i;
            }
        }
        return names[bestI] + "#" + scores[bestI];
    }
}
""",
    wrong=r"""public class Solution {
    public static String topStudent(String[] names, int[] scores) {
        int bestI = 0;
        for (int i = 1; i < scores.length; i++) {
            if (scores[i] >= scores[bestI]) {
                bestI = i;
            }
        }
        return names[scores[bestI]] + "#" + scores[bestI];
    }
}
""",
)
