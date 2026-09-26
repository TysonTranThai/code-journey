#!/usr/bin/env python3
"""AP CSA Core M3 — Control Flow & Algorithmic Reasoning (patterns + traps)."""
from apcc import *

M = "cx-flow"

L1 = r"""
Almost every AP loop is one of four machines. Name the machine, and the
code writes itself.

**Accumulator — collapse a collection to one number.**

```java
int total = 0;
for (int i = 0; i < arr.length; i++) {
    total += arr[i];
}
```

Initialize to the identity of the operation: 0 for sums, 1 for products,
`arr[0]` for max/min, `""` for building a String.

**Counter — count events, return the count.**

```java
int hits = 0;
for (int v : arr) {
    if (meets(v)) {
        hits++;
    }
}
```

A counter *is* an accumulator whose addition is `+ 1`. Same identity rule
(0), same shape.

**Flag — did anything ever fire?**

```java
boolean found = false;
for (int v : arr) {
    if (v == target) {
        found = true;
    }
}
return found;
```

The default comes from the vacuous case (nothing fired → false). The
early-exit form — `return true;` inside, `return false;` after — is the
same machine with the exit moved.

**Sentinel scan — find *where*, not *whether*.**

```java
int at = -1;
for (int i = 0; i < arr.length && at == -1; i++) {
    if (arr[i] == target) {
        at = i;
    }
}
return at;
```

-1 means "absent" by exam convention. The `&& at == -1` stops scanning at
the first hit — without it you return the *last* occurrence (Module 1's
bug, promoted to a pattern).
"""

L2 = r"""
Traps are just patterns wearing a disguise. Each of these fails a
plausible-looking test:

**Trap 1 — the runaway initializer.**

```java
int max = 0;                    // wrong when all values are negative
for (int v : arr) { if (v > max) { max = v; } }
```

Fix: seed with `arr[0]` (requires `arr.length >= 1`, which the spec will
state as a precondition).

**Trap 2 — the fencepost loop.** Print `1 2 3` with dashes *between*:
`-` must be printed before every element except the first.

```java
for (int i = 0; i < arr.length; i++) {
    if (i > 0) { System.out.print("-"); }
    System.out.print(arr[i]);
}
```

The general rule: N items need N−1 separators. Count the posts, count the
fences.

**Trap 3 — the off-by-one range.** "Elements at odd *positions*"
(positions 1, 3, 5...) means indexes 0, 2, 4 in 0-based Java. "Every
second element starting at the first" is indexes 0, 2, 4 too. Draw
index numbers over the elements before writing the loop bounds.

**Trap 4 — the boundary comparison.** `<=` vs `<` in `i < arr.length`
decides whether the last element participates. When a loop *should*
touch every element, `<` with `arr.length` is right; adding `<=` walks
off the end with `ArrayIndexOutOfBoundsException`.

**Trap 5 — early exit forgotten.** Scanning for one match without
`break`/`return` overwrites the result (Module 1's `findFirst`). Ask of
every search loop: "can the answer change after it is already decided?"
If yes, you needed an exit.
"""

L3 = r"""
Combining machines is where exam questions live. The recipe: **decompose
the prompt into named machines, then wire them in one pass.**

*"Return the longest String in `words`; if several tie for longest,
return the earliest. Empty array returns null."*

```java
public static String longest(String[] words) {
    if (words.length == 0) { return null; }
    String best = words[0];
    for (int i = 1; i < words.length; i++) {
        if (words[i].length() > best.length()) {
            best = words[i];
        }
    }
    return best;
}
```

Decomposition: guard the vacuous case → seed from element 0 → scan with
**strict** `>` so ties keep the earlier winner (Trap 1 + tie-breaking in
one). Compare with `>=` and the answer silently becomes the *last* tie —
a one-character difference the exam adores.

Second combination — *"count how many elements are strictly between the
first and last occurrence of `key`"*:

```java
public static int between(int[] arr, int key) {
    int first = -1, last = -1;
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == key) {
            if (first == -1) { first = i; }
            last = i;
        }
    }
    if (first == -1) { return 0; }
    return last - first - 1;
}
```

Two sentinel scans in one loop (first stays, last overwrites), then a
guard that also rejects a single occurrence (`last == first` means
"nothing in between"), then index algebra. No nested loops, no second
pass. When you can
name the machines, "hard" problems assemble from parts you already own.
"""

write_module(
    M,
    "Control Flow & Algorithmic Reasoning",
    "The four loop machines (accumulator, counter, flag, sentinel), the five boundary traps, and composing them into combined algorithms.",
    "Luồng điều khiển & suy luận thuật toán",
    "Bốn cỗ máy vòng lặp (cộng dồn, đếm, cờ, lính canh), năm cái bẫy biên, và ghép chúng thành thuật toán kết hợp.",
    lessons=["cx-m3-machines", "cx-m3-traps", "cx-m3-compose", "cx-cp-m3"],
    practices=["cx-p3-flow"],
)

write_lesson(
    M, "cx-m3-machines", "The four loop machines",
    "Accumulator, counter, flag, and sentinel scan — with correct initializations.",
    12, L1,
    "Bốn cỗ máy vòng lặp",
    "Cộng dồn, đếm, cờ, và quét lính canh — với cách khởi tạo đúng.",
    r"""
Gần như mọi vòng lặp AP đều là một trong bốn cỗ máy. Gọi đúng tên cỗ máy,
mã sẽ tự viết ra.

**Cộng dồn (accumulator) — gộp cả bộ sưu tập thành một con số.**

```java
int total = 0;
for (int i = 0; i < arr.length; i++) {
    total += arr[i];
}
```

Khởi tạo bằng phần tử trung hòa của phép toán: 0 cho tổng, 1 cho tích,
`arr[0]` cho max/min, `""` khi dựng chuỗi.

**Bộ đếm (counter) — đếm sự kiện, trả về số đếm.**

```java
int hits = 0;
for (int v : arr) {
    if (meets(v)) {
        hits++;
    }
}
```

Bộ đếm *chính là* bộ cộng dồn với phép cộng `+ 1`. Cùng luật khởi tạo (0),
cùng hình dạng.

**Cờ (flag) — có bao giờ kích hoạt chưa?**

```java
boolean found = false;
for (int v : arr) {
    if (v == target) {
        found = true;
    }
}
return found;
```

Giá trị mặc định đến từ trường hợp chân không (không kích hoạt lần nào →
false). Dạng thoát sớm — `return true;` bên trong, `return false;` sau —
chỉ là cỗ máy đó với lối thoát dời chỗ.

**Quét lính canh (sentinel) — tìm *ở đâu*, không chỉ *có hay không*.**

```java
int at = -1;
for (int i = 0; i < arr.length && at == -1; i++) {
    if (arr[i] == target) {
        at = i;
    }
}
return at;
```

-1 nghĩa là "vắng mặt" theo quy ước đề thi. Điều kiện `&& at == -1` dừng
quét ngay lần trúng đầu — thiếu nó bạn trả về lần xuất hiện *cuối* (bug
của Module 1, nay nâng cấp thành mẫu nhận diện).
""",
)

write_lesson(
    M, "cx-m3-traps", "The five boundary traps",
    "Negative-max seeds, fenceposts, off-by-one ranges, <= vs <, forgotten exits.",
    12, L2,
    "Năm cái bẫy biên",
    "Seed cho max khi toàn số âm, hàng rào, lệch một, <= với <, và lối thoát bị quên.",
    r"""
Cái bẫy chỉ là cỗ máy đội lốt. Mỗi cái dưới đây đều trượt một bài kiểm tra
trông rất hợp lý:

**Bẫy 1 — seed chạy trốn.**

```java
int max = 0;                    // sai khi mọi giá trị đều âm
for (int v : arr) { if (v > max) { max = v; } }
```

Sửa: seed bằng `arr[0]` (cần `arr.length >= 1` — đề bài sẽ nêu là điều
kiện tiên quyết).

**Bẫy 2 — vòng lặp hàng rào (fencepost).** In `1 2 3` với gạch ngang
*ở giữa*: dấu `-` phải in trước mọi phần tử trừ phần tử đầu.

```java
for (int i = 0; i < arr.length; i++) {
    if (i > 0) { System.out.print("-"); }
    System.out.print(arr[i]);
}
```

Luật tổng quát: N phần tử cần N−1 dấu ngăn. Đếm cột, đếm rào.

**Bẫy 3 — khoảng lệch một.** "Các phần tử ở *vị trí* lẻ" (vị trí 1, 3,
5...) nghĩa là chỉ số 0, 2, 4 trong Java 0-based. "Mỗi phần tử thứ hai
bắt đầu từ phần tử đầu" cũng là chỉ số 0, 2, 4. Hãy vẽ số chỉ số lên trên
các phần tử trước khi viết biên vòng lặp.

**Bẫy 4 — phép so sánh biên.** `<=` hay `<` trong `i < arr.length` quyết
định phần tử cuối có tham gia không. Vòng lặp cần chạm mọi phần tử thì
dùng `<` với `arr.length`; thêm `<=` là bước ra ngoài mảng với
`ArrayIndexOutOfBoundsException`.

**Bẫy 5 — quên thoát sớm.** Quét tìm một kết quả khớp mà không có
`break`/`return` sẽ ghi đè kết quả (`findFirst` của Module 1). Hỏi mỗi
vòng lặp tìm kiếm: "kết quả có thể đổi sau khi đã quyết định?" Nếu có,
bạn cần một lối thoát.
""",
)

write_lesson(
    M, "cx-m3-compose", "Composing the machines",
    "Longest-with-tie and two-sentinels-one-loop worked examples.",
    12, L3,
    "Ghép các cỗ máy",
    "Ví dụ mẫu: dài nhất có đồng giá và hai lính canh trong một vòng lặp.",
    r"""
Kết hợp các cỗ máy chính là nơi câu hỏi thi sinh ra. Công thức: **tách đề
bài thành các cỗ máy có tên, rồi nối chúng trong một lượt duy nhất.**

*"Trả về String dài nhất trong `words`; nếu nhiều chuỗi cùng dài nhất,
trả về chuỗi sớm nhất. Mảng rỗng trả về null."*

```java
public static String longest(String[] words) {
    if (words.length == 0) { return null; }
    String best = words[0];
    for (int i = 1; i < words.length; i++) {
        if (words[i].length() > best.length()) {
            best = words[i];
        }
    }
    return best;
}
```

Phân rã: chặn trường hợp chân không → seed từ phần tử 0 → quét với dấu
**>` nghiêm ngặt** để đồng giá giữ người thắng sớm hơn (Bẫy 1 + phá đồng
giá trong một). Đổi thành `>=` và đáp án lặng lẽ trở thành đồng giá
*cuối* — khác nhau một ký tự mà đề thi mê mệt.

Ví dụ kết hợp thứ hai — *"đếm xem bao nhiêu phần tử nằm giữa lần xuất
hiện đầu và cuối của `key`"*:

```java
public static int between(int[] arr, int key) {
    int first = -1, last = -1;
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == key) {
            if (first == -1) { first = i; }
            last = i;
        }
    }
    if (first == -1) { return 0; }
    return last - first - 1;
}
```

Hai phép quét lính canh trong một vòng lặp (first giữ nguyên, last ghi
đè), rồi một lớp chặn đồng thời loại trường hợp chỉ xuất hiện một lần
(`last == first` nghĩa là "không có gì ở giữa"), rồi đại số chỉ số. Không
vòng lặp lồng, không lượt
chạy thứ hai. Khi gọi được tên các cỗ máy, bài "khó" lắp ráp từ những bộ
phận bạn đã có sẵn.
""",
)

BOILER_LONGEST = r"""public class Solution {
    public static String longest(String[] words) {
        // CONTRACT: earliest of the longest strings; null for empty input.
        return null; // replace
    }
}
"""

BOILER_BETWEEN = r"""public class Solution {
    public static int between(int[] arr, int key) {
        // CONTRACT: count of elements strictly between the FIRST and LAST
        // occurrence of key; 0 when key is absent or occurs once.
        return 0; // replace
    }
}
"""

BOILER_ALTBAD = r"""public class Solution {
    public static int sumAlt(int[] arr) {
        // CONTRACT: arr[0] - arr[1] + arr[2] - arr[3] + ...
        int total = 0;
        for (int i = 0; i < arr.length; i++) {
            if (i % 2 == 0) {
                total += arr[i];
            } else {
                total += arr[i];
            }
        }
        return total;
    }
}
"""

BOILER_FENCE = r"""public class Solution {
    public static String dashed(int[] arr) {
        // CONTRACT: elements joined by "-", e.g. {1,2,3} -> "1-2-3";
        // empty array -> "".
        String out = "";
        for (int i = 0; i < arr.length; i++) {
            out += "-";
        }
        return out;
    }
}
"""

BOILER_MINPOS = r"""public class Solution {
    public static int minPositive(int[] arr) {
        // CONTRACT: smallest value > 0; returns -1 when the array
        // contains no positive number. arr may be empty.
        int min = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] > 0) {
                min = arr[i];
            }
        }
        return min;
    }
}
"""

BOILER_CP_FLOW = r"""public class Solution {
    public static int compress(int[] arr) {
        // CONTRACT: sum of elements, but each run of equal adjacent
        // elements counts ONCE. {2,2,5,5,5,1} -> 2 + 5 + 1 = 8.
        int total = 0;
        for (int i = 0; i < arr.length; i++) {
            total += arr[i];
        }
        return total;
    }
}
"""

P_LONGEST = challenge(
    "cx-m3-longest-tie",
    "Longest with earliest tie",
    "Implement `String longest(String[] words)`: the earliest of the longest strings, null for empty input. One pass, strict comparison — think about which comparison operator keeps the earlier winner.",
    BOILER_LONGEST,
    [(
        "earliest longest",
        r"""
CjTestBase.checkEq(Solution.longest(new String[]{"ab", "cde", "fg"}), "cde", "unique longest");
CjTestBase.checkEq(Solution.longest(new String[]{"aa", "bb", "c"}), "aa", "tie keeps the EARLIEST");
CjTestBase.checkEq(Solution.longest(new String[]{"x"}), "x", "single element");
CjTestBase.checkEq(Solution.longest(new String[]{}), null, "empty input");
""",
        "Seed with words[0]; scan from 1 with strict > (>= would steal ties).",
    )],
    level="guided",
)

P_BETWEEN = challenge(
    "cx-m3-between-count",
    "Between first and last",
    "Implement `int between(int[] arr, int key)`: how many elements lie strictly between the first and last occurrence of key. Absent or single occurrence → 0. Work a three-element example by hand before coding the index algebra.",
    BOILER_BETWEEN,
    [(
        "between count",
        r"""
CjTestBase.checkEq(Solution.between(new int[]{1, 9, 2, 9, 3}, 9), 1, "index 2 lies between");
CjTestBase.checkEq(Solution.between(new int[]{5, 1, 2}, 5), 0, "single occurrence");
CjTestBase.checkEq(Solution.between(new int[]{1, 2}, 7), 0, "absent key");
CjTestBase.checkEq(Solution.between(new int[]{4, 4}, 4), 0, "adjacent occurrences");
CjTestBase.checkEq(Solution.between(new int[]{9, 1, 2, 3, 9}, 9), 3, "three in between");
""",
        "Record first once, overwrite last always; guard single occurrence too; answer = last - first - 1.",
    )],
    level="independent",
)

P_ALTBAD = challenge(
    "cx-m3-fix-alternating",
    "Fix the alternating sum",
    "`sumAlt` must compute arr[0] - arr[1] + arr[2] - ... but both branches add. Trace {5, 2, 7} against the contract, then repair the minimal line.",
    BOILER_ALTBAD,
    [(
        "alternating sum",
        r"""
CjTestBase.checkEq(Solution.sumAlt(new int[]{5, 2, 7}), 10, "5 - 2 + 7");
CjTestBase.checkEq(Solution.sumAlt(new int[]{1}), 1, "single element stays positive");
CjTestBase.checkEq(Solution.sumAlt(new int[]{}), 0, "empty sum");
CjTestBase.checkEq(Solution.sumAlt(new int[]{2, 2, 2, 2}), 0, "2-2+2-2");
""",
        "The even-index branch adds; the odd-index branch must SUBTRACT.",
    )],
    level="debugging",
)

P_FENCE = challenge(
    "cx-m3-fix-fencepost",
    "Fix the fencepost",
    "`dashed` must join elements with \"-\" ({1,2,3} → \"1-2-3\") but currently prints only dashes. Apply the N elements / N-1 separators rule.",
    BOILER_FENCE,
    [(
        "joined with dashes",
        r"""
CjTestBase.checkEq(Solution.dashed(new int[]{1, 2, 3}), "1-2-3", "three elements, two dashes");
CjTestBase.checkEq(Solution.dashed(new int[]{7}), "7", "no dash for one element");
CjTestBase.checkEq(Solution.dashed(new int[]{}), "", "empty in, empty out");
""",
        "Print the separator BEFORE every element except the first.",
    )],
    level="debugging",
)

P_MINPOS = challenge(
    "cx-m3-min-positive",
    "Min positive with absence",
    "Implement `int minPositive(int[] arr)`: the smallest value strictly greater than 0, or -1 when no positive value exists (empty arrays included). Two machines cooperate here: a sentinel for \"found yet?\" and an accumulator for the minimum.",
    BOILER_MINPOS,
    [(
        "smallest positive",
        r"""
CjTestBase.checkEq(Solution.minPositive(new int[]{-3, 8, 2, 5}), 2, "2 is the smallest positive");
CjTestBase.checkEq(Solution.minPositive(new int[]{-1, -9}), -1, "no positives");
CjTestBase.checkEq(Solution.minPositive(new int[]{}), -1, "empty array");
CjTestBase.checkEq(Solution.minPositive(new int[]{6}), 6, "single positive");
""",
        "Track found with -1 sentinel; update min only for values > 0 (and first positive wins the seed).",
    )],
    level="combination",
)

CP3 = challenge(
    "cx-cp-m3-compress",
    "Checkpoint: runs count once",
    "Upgrade the broken `compress`: sum elements, but each RUN of equal adjacent elements counts once ({2,2,5,5,5,1} → 8). The broken version sums every element (15). Compare each element with its predecessor — one extra condition in the loop body is enough.",
    BOILER_CP_FLOW,
    [(
        "runs counted once",
        r"""
CjTestBase.checkEq(Solution.compress(new int[]{2, 2, 5, 5, 5, 1}), 8, "2 + 5 + 1");
CjTestBase.checkEq(Solution.compress(new int[]{}), 0, "empty");
CjTestBase.checkEq(Solution.compress(new int[]{4}), 4, "single element run");
CjTestBase.checkEq(Solution.compress(new int[]{7, 7, 7}), 7, "one run");
CjTestBase.checkEq(Solution.compress(new int[]{1, 2, 3}), 6, "no repeats, plain sum");
""",
        "Add arr[i] only when i == 0 or arr[i] != arr[i-1] — the run's first element represents it.",
    )],
    level="independent",
)

write_practice(
    M, "cx-p3-flow", "Flow lab",
    "Ties, sentinels, alternating sums, fenceposts, and absence handling.",
    "Phòng luồng điều khiển",
    "Đồng giá, lính canh, tổng đan dấu, hàng rào, và xử lý vắng mặt.",
    after_lesson="cx-m3-traps", minutes=55, difficulty="intermediate",
    challenges=[P_LONGEST, P_BETWEEN, P_ALTBAD, P_FENCE, P_MINPOS],
    vi_challenges={
        "cx-m3-longest-tie": vi_challenge("Dài nhất, đồng giá giữ người sớm",
            "Hiện thực `String longest(String[] words)`: chuỗi dài nhất, nếu đồng giá thì lấy chuỗi xuất hiện sớm nhất; mảng rỗng trả về null. Một lượt quét, so sánh nghiêm ngặt — nghĩ xem toán tử nào giữ người thắng sớm.",
            [("earliest longest", "Seed bằng words[0]; quét từ 1 với dấu > nghiêm ngặt (dấu >= sẽ cướp đồng giá).")]),
        "cx-m3-between-count": vi_challenge("Đếm ở giữa",
            "Hiện thực `int between(int[] arr, int key)`: bao nhiêu phần tử nằm giữa lần xuất hiện đầu và cuối của key. Vắng mặt hoặc chỉ xuất hiện một lần → 0. Làm thử ví dụ ba phần tử bằng tay trước khi viết đại số chỉ số.",
            [("between count", "Ghi first đúng một lần, last cứ ghi đè; chặn thêm trường hợp chỉ một lần xuất hiện; đáp án = last - first - 1.")]),
        "cx-m3-fix-alternating": vi_challenge("Sửa tổng đan dấu",
            "`sumAlt` phải tính arr[0] - arr[1] + arr[2] - ... nhưng cả hai nhánh đều cộng. Truy vết {5, 2, 7} theo hợp đồng, rồi sửa đúng một dòng tối thiểu.",
            [("alternating sum", "Nhánh chỉ số chẵn cộng; nhánh chỉ số lẻ phải TRỪ.")]),
        "cx-m3-fix-fencepost": vi_challenge("Sửa hàng rào",
            "`dashed` phải nối các phần tử bằng \"-\" ({1,2,3} → \"1-2-3\") nhưng hiện chỉ in toàn dấu gạch. Áp dụng luật N phần tử / N−1 dấu ngăn.",
            [("joined with dashes", "In dấu ngăn TRƯỚC mọi phần tử trừ phần tử đầu.")]),
        "cx-m3-min-positive": vi_challenge("Dương nhỏ nhất",
            "Hiện thực `int minPositive(int[] arr)`: giá trị dương nhỏ nhất, hoặc -1 khi không có giá trị dương nào (kể cả mảng rỗng). Hai cỗ máy hợp tác: một lính canh cho \"đã thấy chưa?\" và một bộ cộng dồn cho giá trị nhỏ nhất.",
            [("smallest positive", "Theo dõi 'đã thấy' bằng sentinel -1; chỉ cập nhật min với giá trị > 0 (số dương đầu tiên làm seed).")]),
    },
    solutions=[
        ("cx-m3-longest-tie", BOILER_LONGEST.replace("return null; // replace",
            "if (words.length == 0) { return null; }\n        String best = words[0];\n        for (int i = 1; i < words.length; i++) {\n            if (words[i].length() > best.length()) {\n                best = words[i];\n            }\n        }\n        return best;"),
         BOILER_LONGEST.replace("return null; // replace",
            "if (words.length == 0) { return null; }\n        String best = words[0];\n        for (int i = 1; i < words.length; i++) {\n            if (words[i].length() >= best.length()) {\n                best = words[i];\n            }\n        }\n        return best;")),
        ("cx-m3-between-count", BOILER_BETWEEN.replace("return 0; // replace",
            "int first = -1;\n        int last = -1;\n        for (int i = 0; i < arr.length; i++) {\n            if (arr[i] == key) {\n                if (first == -1) { first = i; }\n                last = i;\n            }\n        }\n        if (first == -1 || last == first) { return 0; }\n        return last - first - 1;"),
         BOILER_BETWEEN.replace("return 0; // replace",
            "int first = -1;\n        int last = -1;\n        for (int i = 0; i < arr.length; i++) {\n            if (arr[i] == key) {\n                if (first == -1) { first = i; }\n                last = i;\n            }\n        }\n        if (first == -1) { return 0; }\n        return last - first;")),
        ("cx-m3-fix-alternating", BOILER_ALTBAD.replace("} else {\n                total += arr[i];\n            }",
            "} else {\n                total -= arr[i];\n            }"),
         BOILER_ALTBAD.replace("if (i % 2 == 0) {\n                total += arr[i];\n            } else {\n                total += arr[i];\n            }",
            "if (i % 2 == 1) {\n                total += arr[i];\n            } else {\n                total += arr[i];\n            }")),
        ("cx-m3-fix-fencepost",
         r"""public class Solution {
    public static String dashed(int[] arr) {
        String out = "";
        for (int i = 0; i < arr.length; i++) {
            if (i > 0) {
                out += "-";
            }
            out += arr[i];
        }
        return out;
    }
}
""",
         r"""public class Solution {
    public static String dashed(int[] arr) {
        String out = "";
        for (int i = 0; i < arr.length; i++) {
            out += "-";
            out += arr[i];
        }
        return out;
    }
}
"""),
        ("cx-m3-min-positive", BOILER_MINPOS.replace("int min = 0;", "int min = -1;").replace(
            "if (arr[i] > 0) {\n                min = arr[i];\n            }",
            "if (arr[i] > 0 && (min == -1 || arr[i] < min)) {\n                min = arr[i];\n            }"),
         BOILER_MINPOS),
    ],
)

write_checkpoint(
    M, "cx-cp-m3", "Checkpoint: compose under contract",
    "Adjacent-run compression from a named-machine decomposition.",
    20,
    r"""
The compress fix is a one-condition insight: an element is its run's
representative exactly when it differs from its predecessor (or starts
the array). You combined adjacency reasoning with accumulation — the
same shape as exam questions that ask you to merge, deduplicate, or
summarize. Next module: the same discipline applied to method
specifications with helpers.
""",
    "Điểm kiểm tra: ghép máy dưới hợp đồng",
    "Nén các đoạn liền kề bằng phân rã theo cỗ máy có tên.",
    r"""
Bản sửa compress là một trực giác một-điều-kiện: một phần tử là đại diện
cho đoạn của nó đúng khi nó khác phần tử đứng trước (hoặc mở đầu mảng).
Bạn đã kết hợp suy luận liền kề với cộng dồn — cùng hình dạng với những
câu thi yêu cầu gộp, khử trùng lặp, hay tóm tắt. Module sau: cùng kỷ luật
áp dụng cho đặc tả phương thức với hàm trợ giúp.
""",
    CP3,
    vi_challenge("Điểm kiểm tra: ghép máy dưới hợp đồng",
        "Nâng cấp `compress` đang sai: cộng các phần tử nhưng mỗi ĐOẠN các phần tử liền kề bằng nhau chỉ tính một lần ({2,2,5,5,5,1} → 8). Bản sai cộng mọi phần tử (15). So sánh mỗi phần tử với phần tử đứng trước — thêm một điều kiện trong thân vòng lặp là đủ.",
        [("runs counted once", "Chỉ cộng arr[i] khi i == 0 hoặc arr[i] != arr[i-1] — phần tử đầu đoạn là đại diện của đoạn.")]),
    solution=r"""public class Solution {
    public static int compress(int[] arr) {
        int total = 0;
        for (int i = 0; i < arr.length; i++) {
            if (i == 0 || arr[i] != arr[i - 1]) {
                total += arr[i];
            }
        }
        return total;
    }
}
""",
    wrong=r"""public class Solution {
    public static int compress(int[] arr) {
        int total = 0;
        for (int i = 0; i < arr.length; i++) {
            if (i == 0 || arr[i] != arr[i - 1]) {
                total += 1;
            }
        }
        return total;
    }
}
""",
)
