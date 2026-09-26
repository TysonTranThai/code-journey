#!/usr/bin/env python3
"""AP CSA Advanced M1 — Advanced AP problem solving (strategy, not teaching)."""
from apx import *

M = "apx-problem-solving"

write_module(
    M,
    "Advanced Problem Solving",
    "Exam-shaped specs, multi-concept decomposition, and when to trace versus when to reason — the working method for the whole course. Difficulty E2–E4.",
    "Giải quyết vấn đề nâng cao",
    "Đặc tả dạng đề thi, phân rã đa khái niệm, và khi nào truy vết hay suy luận — phương pháp làm việc cho toàn khóa. Độ khó E2–E4.",
    lessons=["apx-m1-method", "apx-m1-decompose", "apx-m1-selective", "apx-cp-m1"],
    practices=["apx-p1-spec"],
)

L1 = r"""
This course assumes the full AP CSA toolkit. Nothing is labeled anymore.
Problems arrive the way the exam delivers them — a **specification plus
some code** — and your job is to decide *what matters* before writing a
single line. That is a skill, and skills are trained by reps.

The method used all course long:

1. **Restate** the spec in one sentence: inputs → outputs, what changes.
2. **Type the data**: what is `int`, what is `String`, what is a reference?
   References alias — two variables can name one object.
3. **Find the boundaries**: empty, size 1, first/last index, zero, cap.
4. **Pick the smallest correct algorithm** and only optimize if the spec
   demands it.
5. **Trace your own code once** before submitting — always.

Overthinking is the classic advanced failure: a spec that says *one pass,
no removals* does not want nested loops. Under-thinking is worse: a spec
that says *each item may affect the next* demands a state you must carry
between iterations.
"""

L2 = r"""
**Multi-concept decomposition.** The exam hides a simple computation
inside an unfamiliar story. Example — "loyalty program":

```java
// A Gold member earns 3 points per dollar; Silver earns 2; everyone
// earns double on Fridays. Given the member's tier and the weekday
// number (1=Mon..7=Sun), return the multiplier.
public static int multiplier(String tier, int day) {
    int base = tier.equals("Gold") ? 3 : 2;
    return day == 5 ? base * 2 : base;
}
```

The story is noise; the computation is a table plus one special case.
Practice extracting:

- **What is actually stored or returned?** (a number? an object? a list?)
- **Which words map to conditions?** ("double on Fridays" → `day == 5`)
- **Which words are decoration?** (tier names, the loyalty backstory)

Write the mapping on paper *before* coding. On the exam, thirty seconds
of mapping saves five minutes of rewriting.
"""

L3 = r"""
**When to trace, when to reason.** Full tracing is expensive; the
advanced move is selective execution:

- **State-heavy code** (objects mutated across many calls): trace it —
  build a table, one row per call.
- **Loop-plus-accumulator code**: name the invariant instead. What is
  true after k iterations? If you can state it, you can answer without
  simulating every index.
- **Reference-heavy code**: draw the boxes and arrows once. Aliasing
  questions are cheap *if you draw*, expensive if you re-derive.

And the two cheap wins on every exam:

- **Eliminate impossible answers** before computing: negative lengths,
  indexes that cannot exist, a `String` result from an `int` method.
- **Sanity-check extremes**: does your reading still hold when the list
  is empty or has one element? If not, your reading is wrong.
"""

VI_L1 = r"""
Khóa học này giả định bạn đã có trọn bộ công cụ AP CSA. Không còn gì
được dán nhãn. Bài toán xuất hiện như đề thi trao chúng — một **đặc tả
kèm vài dòng mã** — và việc của bạn là quyết định *điều gì quan trọng*
trước khi viết một dòng nào. Đó là kỹ năng, và kỹ năng được rèn bằng
số lần luyện.

Phương pháp dùng xuyên suốt khóa học:

1. **Diễn đạt lại** đặc tả trong một câu: đầu vào → đầu ra, cái gì thay đổi.
2. **Xác định kiểu dữ liệu**: cái nào là `int`, cái nào là `String`, cái nào
   là tham chiếu? Tham chiếu tạo bí danh — hai biến có thể cùng chỉ một
   đối tượng.
3. **Tìm biên**: rỗng, kích thước 1, chỉ số đầu/cuối, số 0, giới hạn.
4. **Chọn thuật toán nhỏ nhất đúng** và chỉ tối ưu khi đặc tả đòi hỏi.
5. **Truy vết lại mã của chính mình một lần** trước khi nộp — luôn luôn.

Suy nghĩ quá mức là lỗi kinh điển của trình độ nâng cao: đặc tả nói
*một lượt duyệt, không xóa phần tử* thì không cần vòng lặp lồng. Suy
nghĩ thiếu còn tệ hơn: đặc tả nói *mỗi phần tử có thể ảnh hưởng phần tử
kế tiếp* thì đòi hỏi một trạng thái phải mang theo giữa các vòng lặp.
"""

VI_L2 = r"""
**Phân rã đa khái niệm.** Đề thi giấu một phép tính đơn giản trong một
câu chuyện lạ. Ví dụ — "chương trình khách hàng thân thiết":

```java
// Hạng Gold được 3 điểm mỗi đô; Silver được 2; mọi hạng nhân đôi vào
// thứ Sáu. Cho hạng thành viên và số thứ tự ngày trong tuần (1=Hai..
// 7=Chủ nhật), trả về hệ số nhân.
public static int multiplier(String tier, int day) {
    int base = tier.equals("Gold") ? 3 : 2;
    return day == 5 ? base * 2 : base;
}
```

Câu chuyện là nhiễu; phép tính là một bảng cộng một trường hợp đặc biệt.
Luyện việc trích xuất:

- **Thực sự lưu hoặc trả về cái gì?** (một số? một đối tượng? một danh sách?)
- **Từ nào ánh xạ thành điều kiện?** ("nhân đôi thứ Sáu" → `day == 5`)
- **Từ nào chỉ là trang trí?** (tên hạng, câu chuyện thân thiết)

Vẽ bảng ánh xạ trên giấy *trước* khi lập trình. Trong phòng thi, ba mươi
giây vẽ bảng cứu bạn khỏi năm phút viết lại.
"""

VI_L3 = r"""
**Khi nào truy vết, khi nào suy luận.** Truy vết đầy đủ tốn kém; nước đi
nâng cao là thực thi chọn lọc:

- **Mã nặng trạng thái** (đối tượng bị biến đổi qua nhiều lời gọi): truy
  vết — dựng bảng, mỗi lời gọi một dòng.
- **Mã vòng lặp cộng bộ tích lũy**: nêu bất biến thay vì mô phỏng. Sau k
  vòng lặp điều gì đúng? Nếu nói được, bạn trả lời được mà không cần chạy
  từng chỉ số.
- **Mã nặng tham chiếu**: vẽ hộp và mũi tên một lần. Câu hỏi bí danh rẻ
  *nếu bạn vẽ*, đắt nếu bạn suy luận lại trong đầu.

Và hai nước đi rẻ có mặt trong mọi đề thi:

- **Loại các đáp án bất khả** trước khi tính: độ dài âm, chỉ số không thể
  tồn tại, kết quả `String` từ phương thức trả `int`.
- **Kiểm tra nhanh các trường hợp cực trị**: cách hiểu của bạn còn đúng
  khi danh sách rỗng hoặc một phần tử không? Nếu không, cách hiểu sai.
"""

BOILER_TIER = r"""public class Solution {
    public static int multiplier(String tier, int day) {
        return 0; // replace: 3 per $ for Gold, 2 for Silver; x2 on Friday (day 5)
    }
}
"""

BOILER_ID = r"""public class Solution {
    public static String process(String s) {
        return ""; // replace
    }
}
"""

BOILER_ALIAS = r"""public class Solution {
    public static class Bag {
        public int value;
        public Bag(int v) { value = v; }
    }

    public static int after() {
        return 0; // replace: final value of a.value after the sequence
    }
}
"""

BOILER_ZONE = r"""public class Solution {
    public static int fee(int start, int end, int zone) {
        return 0; // replace: flat 400 if zones equal, else 200 per zone crossed
    }
}
"""

BOILER_STACK = r"""public class Solution {
    public static int depth(String log) {
        return 0; // replace: max nesting depth; malformed log -> -1
    }
}
"""

P_TIER = challenge(
    "apx-m1-tier",
    "Multiplier from a noisy spec",
    "A loyalty program: **Gold** members earn 3 points per dollar, **Silver** "
    "members earn 2. On **Friday** (day 5, with days numbered 1=Monday … "
    "7=Sunday) everyone earns double. Implement `multiplier(String tier, int day)`.",
    BOILER_TIER,
    [(
        "gold friday",
        r"""
CjTestBase.checkEq(Solution.multiplier("Gold", 5), 6, "Gold on Friday");
CjTestBase.checkEq(Solution.multiplier("Gold", 3), 3, "Gold midweek");
CjTestBase.checkEq(Solution.multiplier("Silver", 5), 4, "Silver on Friday");
CjTestBase.checkEq(Solution.multiplier("Silver", 7), 2, "Silver Sunday");
""",
        "Base by tier, then double only when day == 5.",
    )],
    level="guided",
    difficulty="intermediate",
)

P_INNER = challenge(
    "apx-m1-inner",
    "Spec under camouflage",
    "A 'text conditioner' applies two rules in order: (1) if the text is "
    "shorter than 3 characters (or null), return it unchanged; (2) otherwise "
    "return only its **middle two** characters (for even length, the two "
    "straddling the center; for odd length, the center character plus the "
    "one after it). Implement `process(String s)`.\n\nExamples: "
    "`\"code\"` → `\"od\"`, `\"abc\"` → `\"bc\"`, `\"ab\"` → `\"ab\"`, `\"x\"` → `\"x\"`.",
    BOILER_ID,
    [(
        "middle extraction",
        r"""
CjTestBase.checkEq(Solution.process("code"), "od", "even length");
CjTestBase.checkEq(Solution.process("abc"), "bc", "odd length");
CjTestBase.checkEq(Solution.process("ab"), "ab", "length 2 unchanged");
CjTestBase.checkEq(Solution.process("x"), "x", "length 1 unchanged");
CjTestBase.checkEq(Solution.process(null), null, "null passes through");
""",
        "Guard the short/null case first; the left index of the pair is (s.length()-1)/2 for both parities.",
    )],
    level="independent",
    difficulty="intermediate",
)

P_ALIAS = challenge(
    "apx-m1-alias",
    "Trace the alias",
    "Two `Bag` references are created, then the sequence below runs. "
    "Implement `after()` to **return the final value of the first bag's "
    "field** — but by simulating the sequence in code, not hardcoding.\n\n"
    "```java\nBag a = new Bag(10);\nBag b = a;        // alias!\nb.value = b.value + 5;\nb = new Bag(99);\nb.value = b.value + 1;\na = b;            // now a follows b\n```\n\n"
    "First trace on paper what `a.value` is at the end, then encode that "
    "final value in `after()`.",
    BOILER_ALIAS,
    [(
        "final aliased value",
        r"""
CjTestBase.checkEq(Solution.after(), 100, "final a.value");
""",
        "a.value becomes 15 while aliased; after a = b, a.value reads the NEW bag (100).",
    )],
    level="combination",
    difficulty="intermediate",
)

P_ZONE = challenge(
    "apx-m1-zone",
    "Hidden conditions in a story",
    "A train ticket costs a **flat 400** when start and end stations are in "
    "the **same zone**; otherwise **200 per zone crossed** (absolute "
    "difference between zone numbers). Implement `fee(int start, int end, "
    "int zone)` where start/end are the zones of the boarding and exit "
    "stations. Careful: the parameters are already zones — do not invent "
    "extra mapping.",
    BOILER_ZONE,
    [(
        "fare by zones",
        r"""
CjTestBase.checkEq(Solution.fee(2, 2, 1), 400, "same zone flat fee");
CjTestBase.checkEq(Solution.fee(1, 4, 9), 600, "three zones crossed");
CjTestBase.checkEq(Solution.fee(4, 1, 9), 600, "direction does not matter");
""",
        "Zones equal → 400; otherwise 200 * |start - end|.",
    )],
    level="independent",
    difficulty="intermediate",
)

P_LOG = challenge(
    "apx-m1-nesting",
    "Nesting depth from a spec",
    "A log line encodes nested calls with `<` for *call* and `>` for "
    "*return*. Compute the **maximum nesting depth** reached. If at any "
    "point a `>` occurs when nothing is open (or the log ends with calls "
    "still open), the log is malformed: return **-1**. An empty log is "
    "well-formed with depth 0. Implement `depth(String log)`.",
    BOILER_STACK,
    [(
        "depth incl. malformed",
        r"""
CjTestBase.checkEq(Solution.depth(""), 0, "empty ok");
CjTestBase.checkEq(Solution.depth("<<><>>"), 2, "two levels");
CjTestBase.checkEq(Solution.depth("<><<>>"), 2, "reopen after close");
CjTestBase.checkEq(Solution.depth(">"), -1, "close with nothing open");
CjTestBase.checkEq(Solution.depth("<<>"), -1, "left open at end");
""",
        "One pass: increment on '<', decrement on '>', track max, fail if count ever negative or final count not zero.",
    )],
    level="real-world",
    difficulty="advanced",
)

write_practice(
    M, "apx-p1-spec", "Reading specs like the exam writes them",
    "Restate, type the data, find boundaries — then implement.",
    "Đọc đặc tả như đề thi viết",
    "Diễn đạt lại, xác định kiểu dữ liệu, tìm biên — rồi mới cài đặt.",
    after_lesson="apx-m1-method", minutes=45, difficulty="intermediate",
    challenges=[P_TIER, P_INNER, P_ZONE, P_ALIAS, P_LOG],
    vi_challenges={
        "apx-m1-tier": vi_challenge(
            "Hệ số từ đặc tả nhiễu",
            "Chương trình thân thiết: thành viên **Gold** được 3 điểm mỗi đô, "
            "**Silver** được 2. Vào **thứ Sáu** (ngày 5, đánh số 1=thứ Hai … "
            "7=chủ nhật) mọi người được nhân đôi. Cài đặt `multiplier(String tier, int day)`.",
            [("gold friday", "Hệ số theo hạng, rồi chỉ nhân đôi khi day == 5.")],
        ),
        "apx-m1-inner": vi_challenge(
            "Đặc tả ngụy trang",
            "Một 'bộ điều chỉnh văn bản' áp hai luật theo thứ tự: (1) nếu văn "
            "bản ngắn hơn 3 ký tự (hoặc null), trả nguyên bản; (2) ngược lại trả "
            "**hai ký tự giữa** (độ dài chẵn: hai ký tự ôm tâm; lẻ: ký tự tâm "
            "cộng ký tự ngay sau). Cài đặt `process(String s)`.\n\nVí dụ: "
            "`\"code\"` → `\"od\"`, `\"abc\"` → `\"bc\"`, `\"ab\"` → `\"ab\"`, `\"x\"` → `\"x\"`.",
            [("middle extraction", "Chặn trường hợp ngắn/null trước; chỉ số trái của cặp là (s.length()-1)/2 cho cả hai tính chẵn lẻ.")],
        ),
        "apx-m1-alias": vi_challenge(
            "Truy vết bí danh",
            "Hai tham chiếu `Bag` được tạo, rồi chạy đoạn lệnh dưới. Cài đặt "
            "`after()` để **trả về giá trị cuối của trường túi đầu tiên** — "
            "bằng cách mô phỏng chuỗi lệnh trong mã, không ghi cứng.\n\n"
            "```java\nBag a = new Bag(10);\nBag b = a;        // bí danh!\nb.value = b.value + 5;\nb = new Bag(99);\nb.value = b.value + 1;\na = b;            // giờ a theo b\n```\n\n"
            "Truy vết trên giấy `a.value` cuối cùng, rồi mã hóa giá trị đó trong `after()`.",
            [("final aliased value", "a.value thành 15 khi còn bí danh; sau a = b, a.value đọc túi MỚI (100).")],
        ),
        "apx-m1-zone": vi_challenge(
            "Điều kiện ẩn trong câu chuyện",
            "Vé tàu giá **trọn gói 400** khi ga đi và ga đến cùng **khu vực**; "
            "ngược lại **200 mỗi khu vực vượt qua** (hiệu tuyệt đối giữa số khu "
            "vực). Cài đặt `fee(int start, int end, int zone)` với start/end là "
            "khu vực của ga lên và ga xuống. Cẩn thận: tham số đã là khu vực — "
            "đừng chế thêm phép ánh xạ.",
            [("fare by zones", "Zones bằng nhau → 400; ngược lại 200 * |start - end|.")],
        ),
        "apx-m1-nesting": vi_challenge(
            "Độ sâu lồng từ đặc tả",
            "Một dòng log mã hóa lời gọi lồng bằng `<` cho *gọi* và `>` cho "
            "*trả về*. Tính **độ sâu lồng tối đa** đạt được. Nếu gặp `>` khi "
            "không gì đang mở (hoặc log kết thúc khi còn lời gọi mở), log lỗi "
            "định dạng: trả **-1**. Log rỗng hợp lệ, độ sâu 0. Cài đặt `depth(String log)`.",
            [("depth incl. malformed", "Một lượt: tăng với '<', giảm với '>', ghi nhận max; lỗi nếu đếm âm bất kỳ lúc nào hoặc cuối cùng khác 0.")],
        ),
    },
    solutions=[
        ("apx-m1-tier", r"""public class Solution {
    public static int multiplier(String tier, int day) {
        int base = tier.equals("Gold") ? 3 : 2;
        return day == 5 ? base * 2 : base;
    }
}
""", r"""public class Solution {
    // BUG: doubles on any day >= 5 (weekend too), and reads tier after
    public static int multiplier(String tier, int day) {
        int base = tier.equals("Gold") ? 3 : 2;
        return day >= 5 ? base * 2 : base;
    }
}
"""),
        ("apx-m1-inner", r"""public class Solution {
    public static String process(String s) {
        if (s == null || s.length() < 3) {
            return s;
        }
        int mid = (s.length() - 1) / 2;
        return s.substring(mid, mid + 2);
    }
}
""", r"""public class Solution {
    // BUG: off-by-one — length/2 works for odd but grabs the right pair on even
    public static String process(String s) {
        if (s == null || s.length() < 3) {
            return s;
        }
        int mid = s.length() / 2;
        return s.substring(mid, mid + 2);
    }
}
"""),
        ("apx-m1-alias", r"""public class Solution {
    public static int after() {
        Bag a = new Bag(10);
        Bag b = a;
        b.value = b.value + 5;
        b = new Bag(99);
        b.value = b.value + 1;
        a = b;
        return a.value;
    }

    public static class Bag {
        public int value;
        public Bag(int v) { value = v; }
    }
}
""", r"""public class Solution {
    // BUG: stops before the re-aliasing — returns the mid-sequence value
    public static int after() {
        Bag a = new Bag(10);
        Bag b = a;
        b.value = b.value + 5;
        return a.value;
    }

    public static class Bag {
        public int value;
        public Bag(int v) { value = v; }
    }
}
"""),
        ("apx-m1-zone", r"""public class Solution {
    public static int fee(int start, int end, int zone) {
        if (start == end) {
            return 400;
        }
        return 200 * Math.abs(start - end);
    }
}
""", r"""public class Solution {
    // BUG: ignores direction — subtracts instead of absolute value
    public static int fee(int start, int end, int zone) {
        if (start == end) {
            return 400;
        }
        return 200 * (start - end);
    }
}
"""),
        ("apx-m1-nesting", r"""public class Solution {
    public static int depth(String log) {
        int open = 0;
        int max = 0;
        for (int i = 0; i < log.length(); i++) {
            char c = log.charAt(i);
            if (c == '<') {
                open++;
                if (open > max) {
                    max = open;
                }
            } else if (c == '>') {
                open--;
                if (open < 0) {
                    return -1;
                }
            }
        }
        if (open != 0) {
            return -1;
        }
        return max;
    }
}
""", r"""public class Solution {
    // BUG: never validates the final state — an unclosed log returns its max
    public static int depth(String log) {
        int open = 0;
        int max = 0;
        for (int i = 0; i < log.length(); i++) {
            char c = log.charAt(i);
            if (c == '<') {
                open++;
                if (open > max) {
                    max = open;
                }
            } else if (c == '>') {
                open--;
            }
        }
        return max;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m1", "Checkpoint: spec → plan → code",
    "One unfamiliar spec, full method: boundaries first, then implementation.",
    20,
    r"""
One habit carries this whole course: **boundaries before code**. Restate
the spec, list the edge cases (empty, one element, ends), and only then
write. The checkpoint below hides two of them.
""",
    "Điểm kiểm tra: đặc tả → kế hoạch → mã",
    "Một đặc tả lạ, phương thức hoàn chỉnh: biên trước, cài đặt sau.",
    r"""
Một thói quen kéo dài suốt khóa học: **biên trước khi viết mã**. Diễn đạt
lại đặc tả, liệt kê các trường hợp biên (rỗng, một phần tử, hai đầu), rồi
mới viết. Bài kiểm tra dưới đây giấu hai trường hợp như vậy.
""",
    challenge(
        "apx-cp-m1-window",
        "Checkpoint: slide the window",
        "A sensor stream is a string of digits. A reading is 'stable' if some "
        "**3-character window** has all digits equal. Implement `hasStable(String "
        "s)`: true if such a window exists, false otherwise — including when the "
        "string is **shorter than 3** (no full window can exist).",
        r"""public class Solution {
    public static boolean hasStable(String s) {
        return false; // replace
    }
}
""",
        [(
            "stable window",
            r"""
CjTestBase.checkTrue(Solution.hasStable("ab777xz"), "777 present");
CjTestBase.checkTrue(Solution.hasStable("999"), "exact window");
CjTestBase.checkTrue(!Solution.hasStable("ab77x"), "repeated pair only");
CjTestBase.checkTrue(!Solution.hasStable("99"), "too short");
CjTestBase.checkTrue(!Solution.hasStable(""), "empty");
""",
            "Loop windows i..i+2 while i+2 < s.length(); compare three chars. Short strings skip the loop and return false.",
        )],
        level="independent",
        difficulty="advanced",
    ),
    vi_challenge(
        "Điểm kiểm tra: trượt cửa sổ",
        "Luồng cảm biến là một chuỗi chữ số. Một phép đo 'ổn định' nếu tồn tại "
        "**cửa sổ 3 ký tự** có toàn chữ số giống nhau. Cài đặt `hasStable(String "
        "s)`: true nếu tồn tại, false nếu không — kể cả khi chuỗi **ngắn hơn 3** "
        "(không thể có cửa sổ đủ dài).",
        [("stable window", "Duyệt cửa sổ i..i+2 khi i+2 < s.length(); so sánh ba ký tự. Chuỗi ngắn bỏ qua vòng lặp và trả false.")],
    ),
    solution=r"""public class Solution {
    public static boolean hasStable(String s) {
        for (int i = 0; i + 2 < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i + 1) && s.charAt(i + 1) == s.charAt(i + 2)) {
                return true;
            }
        }
        return false;
    }
}
""",
    wrong=r"""public class Solution {
    // BUG: <= lets the window run off the end → StringIndexOutOfBounds
    public static boolean hasStable(String s) {
        for (int i = 0; i + 2 <= s.length(); i++) {
            if (s.charAt(i) == s.charAt(i + 1) && s.charAt(i + 1) == s.charAt(i + 2)) {
                return true;
            }
        }
        return false;
    }
}
""",
)

print("M1 done")
