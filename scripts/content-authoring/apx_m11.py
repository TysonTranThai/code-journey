#!/usr/bin/env python3
"""AP CSA Advanced M11 — Integrated coding challenges (no topic labels)."""
from apx import *

M = "apx-integrated"

write_module(
    M,
    "Integrated Coding Challenges",
    "Unlabeled problems that fuse loops, strings, arrays, lists, and objects — the concept is yours to identify. Difficulty E3–E5.",
    "Bài toán tích hợp",
    "Bài không nhãn trộn vòng lặp, chuỗi, mảng, danh sách, và đối tượng — khái niệm là việc của bạn để nhận diện. Độ khó E3–E5.",
    lessons=["apx-m11-identify", "apx-m11-fusion", "apx-m11-plan", "apx-cp-m11"],
    practices=["apx-p11-integrated"],
)

L1 = r"""
Nothing on this module's problems tells you the topic. That is the
point: on the exam, "ArrayList" never appears in the stem — a story
about a **waitlist** does. The identification step:

1. **Underline the nouns** in the spec. "Passengers," "positions,"
   "cap" — each maps to a variable, a list, or a field.
2. **Underline the verbs**: "adds," "removes," "counts," "shifts."
   Verbs over collections → list mutation; verbs over letters →
   string traversal; verbs over "each row" → nested loops.
3. **Name the shape** before writing code: this is a remove-scan,
   this is an accumulator, this is a two-pass. Shapes transfer;
   stories don't.

The wrong move is diving into code from the story. The right move
is a one-line restatement with data types: "given a list of int
arrays, count rows whose max exceeds the sum of the rest" — the
code writes itself from there.
"""

L2 = r"""
**Fusion problems** stack two mechanisms where each alone is easy:

- **String scan + char arithmetic**: shift vowels only — classify
  (`"aeiou".indexOf(ch) >= 0`) then transform (`ch + 1`). Both halves
  are intro-level; the fusion is where care lives.
- **List of arrays + per-row analysis**: `ArrayList<int[]>` where
  each row needs its own max/sum scan — nested loops with a *reset*
  between rows. Forgetting the reset is the classic bug.
- **Log processing + running state**: walk characters, maintain an
  altitude/count, answer from the final state. The state variable
  must survive the whole loop — declaring it inside is the classic
  bug.

When two mechanisms fuse, write each as a helper if the spec allows,
or as clearly separated passes if it doesn't. Fusion is a reading
skill; the code stays ordinary.
"""

L3 = r"""
**Planning under exam conditions.** For a 15-point FRQ, five minutes
of planning is the highest-yield investment:

1. Write the method signature with real types — no `var`-style
   vagueness.
2. List the states: what does the loop carry between iterations?
3. Mark the boundaries: first element, last element, empty, none
   match, all match.
4. Write the control skeleton in comments first:

```java
// for each row:
//     compute row max and row total
//     if max > total - max: count++
```

5. Then fill the code. The skeleton catches structural mistakes
   (wrong loop order, missing reset) while they are still free to
   fix.

After coding, re-read the spec sentence by sentence and check each
claim against your code. Most lost FRQ points are spec sentences
that were true in the reader's head and absent from the code.
"""

VI_L1 = r"""
Không bài nào trong module này cho bạn biết chủ đề. Đó chính là điểm:
trong đề thi, "ArrayList" không bao giờ xuất hiện trong đề — một câu
chuyện về **danh sách chờ** thì có. Bước nhận diện:

1. **Gạch chân các danh từ** trong đặc tả. "Hành khách," "vị trí,"
   "giới hạn" — mỗi cái ánh xạ tới một biến, một danh sách, hoặc một
   trường.
2. **Gạch chân các động từ**: "thêm," "xóa," "đếm," "dịch." Động từ
   trên bộ sưu tập → biến đổi danh sách; động từ trên chữ cái → duyệt
   chuỗi; động từ trên "mỗi hàng" → vòng lặp lồng.
3. **Gọi tên hình dạng** trước khi viết mã: đây là quét-xóa, đây là
   bộ tích lũy, đây là hai lượt. Hình dạng chuyển giao được; câu chuyện
   thì không.

Nước đi sai là lao vào viết mã từ câu chuyện. Nước đi đúng là diễn đạt
lại một dòng với kiểu dữ liệu: "cho danh sách các mảng int, đếm các
hàng có max vượt tổng phần còn lại" — từ đó mã tự viết ra.
"""

VI_L2 = r"""
**Bài hợp nhất** chồng hai cơ chế mà riêng từng cái đều dễ:

- **Quét chuỗi + phép toán ký tự**: dịch chỉ nguyên âm — phân loại
  (`"aeiou".indexOf(ch) >= 0`) rồi biến đổi (`ch + 1`). Cả hai nửa ở
  trình nhập môn; phần hợp nhất là nơi sự cẩn thận sống.
- **Danh sách mảng + phân tích từng hàng**: `ArrayList<int[]>` mà mỗi
  hàng cần lượt quét max/tổng riêng — vòng lặp lồng với phép *reset*
  giữa các hàng. Quên reset là lỗi kinh điển.
- **Xử lý log + trạng thái chạy**: đi qua ký tự, giữ một độ cao/bộ
  đếm, trả lời từ trạng thái cuối. Biến trạng thái phải sống xuyên suốt
  vòng lặp — khai báo nó bên trong là lỗi kinh điển.

Khi hai cơ chế hợp nhất, viết mỗi cái thành helper nếu đặc tả cho
phép, hoặc thành các lượt tách bạch nếu không. Hợp nhất là kỹ năng
đọc; mã vẫn bình thường.
"""

VI_L3 = r"""
**Lập kế hoạch trong điều kiện phòng thi.** Với một FRQ 15 điểm, năm
phút lập kế hoạch là khoản đầu tư hiệu quả nhất:

1. Viết chữ ký phương thức với kiểu thật — không mơ hồ kiểu var.
2. Liệt kê các trạng thái: vòng lặp mang gì giữa các lần lặp?
3. Đánh dấu các biên: phần tử đầu, phần tử cuối, rỗng, không khớp
   cái nào, khớp tất cả.
4. Viết khung điều khiển dạng chú thích trước:

```java
// với mỗi hàng:
//     tính max hàng và tổng hàng
//     nếu max > tổng - max: count++
```

5. Rồi điền mã. Khung bắt lỗi cấu trúc (sai thứ tự vòng lặp, thiếu
   reset) khi chúng vẫn còn miễn phí để sửa.

Sau khi viết xong, đọc lại đặc tả từng câu và đối chiếu mỗi tuyên bố
với mã của bạn. Đa số điểm FRQ mất là những câu đặc tả đúng trong đầu
người đọc nhưng vắng mặt trong mã.
"""

BOILER_VOWEL = r"""public class Solution {
    public static String encode(String word) {
        return ""; // replace
    }
}
"""

BOILER_ROWS = r"""public class Solution {
    public static int process(java.util.ArrayList<int[]> rows) {
        return 0; // replace
    }
}
"""

BOILER_LOG = r"""public class Solution {
    public static int process(java.util.ArrayList<String> log) {
        return 0; // replace
    }
}
"""

P_VOWEL = challenge(
    "apx-m11-vowelstep",
    "The word encoder",
    "A cipher replaces each **vowel** (a, e, i, o, u — lowercase only) "
    "with the NEXT letter of the alphabet; every other character is "
    "unchanged. Implement `encode(String word)`.\n\nExample: "
    "`\"banana\"` → `\"bbnbnb\"` (a→b twice, a→b again).",
    BOILER_VOWEL,
    [(
        "vowel-shifted output",
        r"""
CjTestBase.checkEq(Solution.encode("banana"), "bbnbnb", "three vowels");
CjTestBase.checkEq(Solution.encode("xyz"), "xyz", "no vowels");
CjTestBase.checkEq(Solution.encode(""), "", "empty");
CjTestBase.checkEq(Solution.encode("aE"), "bE", "uppercase untouched");
""",
        "Classify with \"aeiou\".indexOf(ch) >= 0, then append (char)(ch + 1).",
    )],
    level="guided",
    difficulty="intermediate",
)

P_ROWS = challenge(
    "apx-m11-dominant",
    "The row auditor",
    "Given a list of number rows, count the rows whose **largest "
    "value is strictly greater than the sum of all its other "
    "values**. Implement `process(java.util.ArrayList<int[]> rows)` "
    "(0 for an empty list).\n\nExample: rows `{9,1,2}` (9 > 3 ✓), "
    "`{3,3,3}` (3 > 6 ✗), `{1,1,5}` (5 > 2 ✓) → `2`.",
    BOILER_ROWS,
    [(
        "dominant row count",
        r"""
java.util.ArrayList<int[]> rows = new java.util.ArrayList<>();
rows.add(new int[]{9, 1, 2});
rows.add(new int[]{3, 3, 3});
rows.add(new int[]{1, 1, 5});
CjTestBase.checkEq(Solution.process(rows), 2, "two dominant rows");
CjTestBase.checkEq(Solution.process(new java.util.ArrayList<>()), 0, "empty list");
""",
        "Per row: one pass for max and total, then compare max > total - max. Reset both between rows.",
    )],
    level="independent",
    difficulty="advanced",
)

P_CLIMB = challenge(
    "apx-m11-altitude",
    "The climb log",
    "A hike log is a list of strings made of 'U' (up) and 'D' (down) "
    "characters. Compute the **net altitude change** over the whole "
    "log (U counts +1, D counts -1, other characters ignored). "
    "Implement `process(java.util.ArrayList<String> log)` (0 for "
    "empty).\n\nExample: `[\"UUD\", \"DUU\"]` → 4 ups, 2 downs → `2`.",
    BOILER_LOG,
    [(
        "net altitude",
        r"""
java.util.ArrayList<String> log = new java.util.ArrayList<>();
log.add("UUD");
log.add("DUU");
CjTestBase.checkEq(Solution.process(log), 2, "4 ups, 2 downs");
CjTestBase.checkEq(Solution.process(new java.util.ArrayList<>()), 0, "empty log");
""",
        "Outer loop over strings, inner over characters, one altitude accumulator outside both.",
    )],
    level="imitation",
    difficulty="intermediate",
)

CP11 = challenge(
    "apx-cp-m11-blend",
    "Checkpoint: the blend machine",
    "A smoothie menu is a list of ingredient codes like `\"ab2x\"` — "
    "digits mark add-in counts. Compute the **total add-in count**: "
    "the sum of every digit character's numeric value across the whole "
    "menu. Implement `process(java.util.ArrayList<String> menu)` (0 "
    "for empty menu or no digits).\n\nExample: `[\"ab2x\", \"3\"]` → "
    "2 + 3 = `5`.",
    BOILER_LOG,
    [(
        "total add-ins",
        r"""
java.util.ArrayList<String> menu = new java.util.ArrayList<>();
menu.add("ab2x");
menu.add("3");
CjTestBase.checkEq(Solution.process(menu), 5, "2 + 3");
CjTestBase.checkEq(Solution.process(new java.util.ArrayList<>()), 0, "empty menu");
""",
        "Character classification (digit) plus the ch - '0' conversion, nested loops, one accumulator.",
    )],
    level="combination",
    difficulty="advanced",
)

VI_CP11 = vi_challenge(
    "Điểm kiểm tra: máy pha trộn",
    "Thực đơn sinh tố là danh sách mã nguyên liệu như `\"ab2x\"` — chữ "
    "số đánh dấu số phần thêm. Tính **tổng số phần thêm**: tổng giá trị "
    "số của mọi ký tự chữ số trên toàn thực đơn. Cài đặt "
    "`process(java.util.ArrayList<String> menu)` (0 cho thực đơn rỗng "
    "hoặc không có chữ số).\n\nVí dụ: `[\"ab2x\", \"3\"]` → 2 + 3 = `5`.",
    [("total add-ins", "Phân loại ký tự (chữ số) cộng phép đổi ch - '0', vòng lặp lồng, một bộ tích lũy.")],
)

write_practice(
    M, "apx-p11-integrated", "Integration gauntlet",
    "Three unlabeled fusion problems; identify the shape, then implement.",
    "Võ đài tích hợp",
    "Ba bài hợp nhất không nhãn; nhận diện hình dạng, rồi cài đặt.",
    after_lesson="apx-m11-plan", minutes=50, difficulty="advanced",
    challenges=[P_VOWEL, P_CLIMB, P_ROWS],
    vi_challenges={
        "apx-m11-vowelstep": vi_challenge(
            "Máy mã hóa từ",
            "Một phép mật mã thay mỗi **nguyên âm** (a, e, i, o, u — chỉ chữ "
            "thường) bằng chữ cái KẾ TIẾP trong bảng chữ cái; mọi ký tự khác "
            "giữ nguyên. Cài đặt `encode(String word)`.\n\nVí dụ: "
            "`\"banana\"` → `\"bbnbnb\"` (a→b hai lần, a→b lần nữa).",
            [("vowel-shifted output", "Phân loại bằng \"aeiou\".indexOf(ch) >= 0, rồi nối (char)(ch + 1).")],
        ),
        "apx-m11-altitude": vi_challenge(
            "Nhật ký leo núi",
            "Nhật ký leo là danh sách chuỗi gồm ký tự 'U' (lên) và 'D' "
            "(xuống). Tính **độ thay đổi độ cao ròng** trên toàn nhật ký "
            "(U tính +1, D tính -1, ký tự khác bỏ qua). Cài đặt "
            "`process(java.util.ArrayList<String> log)` (0 cho rỗng).\n\n"
            "Ví dụ: `[\"UUD\", \"DUU\"]` → 4 lần lên, 2 lần xuống → `2`.",
            [("net altitude", "Vòng ngoài qua chuỗi, vòng trong qua ký tự, một bộ tích lũy độ cao ngoài cả hai.")],
        ),
        "apx-m11-dominant": vi_challenge(
            "Thanh tra hàng",
            "Cho danh sách các hàng số, đếm các hàng có **giá trị lớn nhất "
            "lớn hơn hoàn toàn tổng tất cả giá trị khác của hàng đó**. Cài "
            "đặt `process(java.util.ArrayList<int[]> rows)` (0 cho danh sách "
            "rỗng).\n\nVí dụ: các hàng `{9,1,2}` (9 > 3 ✓), `{3,3,3}` "
            "(3 > 6 ✗), `{1,1,5}` (5 > 2 ✓) → `2`.",
            [("dominant row count", "Mỗi hàng: một lượt lấy max và tổng, rồi so sánh max > tổng - max. Reset cả hai giữa các hàng.")],
        ),
    },
    solutions=[
        ("apx-m11-vowelstep", r"""public class Solution {
    public static String encode(String word) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < word.length(); i++) {
            char ch = word.charAt(i);
            if ("aeiou".indexOf(ch) >= 0) {
                ch = (char) (ch + 1);
            }
            out.append(ch);
        }
        return out.toString();
    }
}
""", r"""public class Solution {
    // BUG: shifts vowels by two — misread "next" as "after next"
    public static String encode(String word) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < word.length(); i++) {
            char ch = word.charAt(i);
            if ("aeiou".indexOf(ch) >= 0) {
                ch = (char) (ch + 2);
            }
            out.append(ch);
        }
        return out.toString();
    }
}
"""),
        ("apx-m11-altitude", r"""public class Solution {
    public static int process(java.util.ArrayList<String> log) {
        int altitude = 0;
        for (String s : log) {
            for (int i = 0; i < s.length(); i++) {
                char ch = s.charAt(i);
                if (ch == 'U') {
                    altitude++;
                } else if (ch == 'D') {
                    altitude--;
                }
            }
        }
        return altitude;
    }
}
""", r"""public class Solution {
    // BUG: resets the accumulator for every string — loses earlier entries
    public static int process(java.util.ArrayList<String> log) {
        int total = 0;
        for (String s : log) {
            int altitude = 0;
            for (int i = 0; i < s.length(); i++) {
                char ch = s.charAt(i);
                if (ch == 'U') {
                    altitude++;
                } else if (ch == 'D') {
                    altitude--;
                }
            }
            total = altitude;
        }
        return total;
    }
}
"""),
        ("apx-m11-dominant", r"""public class Solution {
    public static int process(java.util.ArrayList<int[]> rows) {
        int count = 0;
        for (int[] row : rows) {
            int max = Integer.MIN_VALUE;
            int total = 0;
            for (int v : row) {
                total += v;
                if (v > max) {
                    max = v;
                }
            }
            if (max > total - max) {
                count++;
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // BUG: compares max against the FULL total including itself
    public static int process(java.util.ArrayList<int[]> rows) {
        int count = 0;
        for (int[] row : rows) {
            int max = Integer.MIN_VALUE;
            int total = 0;
            for (int v : row) {
                total += v;
                if (v > max) {
                    max = v;
                }
            }
            if (max > total) {
                count++;
            }
        }
        return count;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m11", "Checkpoint: the blend machine",
    "Digit extraction fused with nested scanning — three mechanisms, one method.",
    22,
    r"""
The checkpoint fuses classification, conversion, and accumulation.
Identify the three mechanisms in the spec before writing — that
sentence you produce IS the solution plan.
""",
    "Điểm kiểm tra: máy pha trộn",
    "Trích chữ số hợp nhất với quét lồng — ba cơ chế, một phương thức.",
    r"""
Bài kiểm tra hợp nhất phân loại, đổi kiểu, và tích lũy. Nhận diện ba
cơ chế trong đặc tả trước khi viết — câu bạn tạo ra CHÍNH LÀ kế hoạch
lời giải.
""",
    CP11,
    VI_CP11,
    solution=r"""public class Solution {
    public static int process(java.util.ArrayList<String> menu) {
        int total = 0;
        for (String s : menu) {
            for (int i = 0; i < s.length(); i++) {
                char ch = s.charAt(i);
                if (ch >= '0' && ch <= '9') {
                    total += ch - '0';
                }
            }
        }
        return total;
    }
}
""",
    wrong=r"""public class Solution {
    public static int process(java.util.ArrayList<String> menu) {
        int total = 0;
        for (String s : menu) {
            for (int i = 0; i < s.length(); i++) {
                char ch = s.charAt(i);
                if (ch >= '0' && ch <= '9') {
                    // BUG: adds the raw char code instead of the digit value
                    total += ch;
                }
            }
        }
        return total;
    }
}
""",
)

print("M11 done")
