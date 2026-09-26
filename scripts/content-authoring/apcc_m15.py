#!/usr/bin/env python3
"""AP CSA Core M15 — FRQ Class Design (Q2)."""
from apcc import *

M = "cx-frq-class"

L1 = r"""
The Q2 spec table is a fill-in-the-blanks contract. A representative
table — this module's checkpoint — reads:

```text
Class: Signaler
Fields:
  - private int level        (current signal level, starts at 1)
  - private int streak       (consecutive strengthens, starts at 0)
Constructor: Signaler() — both fields at start values.
Methods:
  void boost()      — level += streak; then streak++
  void reset()      — level back to 1; streak back to 0
  int getLevel()    — reader
```

The workflow is mechanical: translate each row, in order. Two rows
deserve special respect:

**"starts at 0/1"** — set it in the CONSTRUCTOR, not lazily. Graders
check the initial state with a getter call before any mutation.

**Order inside a method matters.** `boost()` adds the CURRENT streak
to level, THEN increments streak. Swapping the two lines changes every
subsequent value — trace `boost; boost; boost`: levels 1+0=1, 1+1=2,
2+2=4 vs (if swapped) 1+1=2, 2+2=4, 4+3=7. Both are "implementations";
only one matches the table. When the table gives an order, the order
is the specification.
"""

L2 = r"""
Q2 rewards **helper decomposition** — often explicitly ("a private
helper may earn full credit if used correctly"). Two patterns:

**The normalize helper.** A class storing minutes could store raw
seconds internally and normalize on write:

```java
private int totalSeconds;
private void normalize() {
    minutes += seconds / 60;   // ...via fields
    seconds = seconds % 60;
}
```

The helper converts "carry" logic into one named place; mutators call
it after every change. The exam rewards this when the spec says
"invariant: seconds < 60 always".

**The classify helper.** Part (b) usually needs part (a)'s decision:

```java
private boolean isPrime(int n) { ... }
public int countPrimes() {
    int c = 0;
    for (int v : values) { if (isPrime(v)) c++; }
    return c;
}
```

Writing the classifier as a helper makes (b) a two-liner and makes
YOUR trace easier (test the helper on small inputs first).

**Object interaction in Q2** — "the method takes another object of
the same class": `public void merge(Counter other)` reads other's
getters and mutates this. The trap: mutating `other` instead of `this`
(aliased-parameter confusion), or reading `this` where `other` was
meant. Name the target of every assignment out loud while writing.
"""

L3 = r"""
A repair-flavored Q2 variant: given a *class that almost works*, the
bugs live in the seams between rows of the spec table:

- **The un-initialized field.** Constructor sets two of three fields;
  the third rides Java's default (0/null). If the spec says it starts
  at 1, every computation touching it is off — and the getter-only
  test passes while behavior tests fail.
- **The copied-not-called method.** A mutator recomputes a derived
  value that another method ALSO recomputes differently — two sources
  of truth. The spec's invariant ("count always equals list.size()")
  is the referee: whichever method breaks it is the bug.
- **The wrong-this mutation.** `void adopt(Other o) { o.x = x; }`
  updates the parameter instead of the receiver. State flows the wrong
  way; the rubric's "mutates this object" behavior silently fails.

Repair discipline: write the spec table as a checklist, tick each row
against the code, and fix only unticked rows. On the exam (typed) this
takes ninety seconds and catches every seam bug above.
"""

write_module(
    M,
    "FRQ Class Design",
    "Q2 spec-table translation: ordered mutators, helper decomposition, object-interaction discipline, and seam-bug repair.",
    "Thiết kế lớp kiểu FRQ",
    "Dịch bảng đặc tả của Q2: mutator có thứ tự, phân rã hàm trợ giúp, kỷ luật tương-tác-đối-tượng, và sửa lỗi-khe-hở.",
    lessons=["cx-m15-spec-table", "cx-m15-helpers", "cx-m15-seams", "cx-cp-m15"],
    practices=["cx-p15-frqclass"],
)

write_lesson(
    M, "cx-m15-spec-table", "The spec table contract",
    "Translating rows exactly; why field order inside methods is specification.",
    12, L1,
    "Hợp đồng bảng đặc tả",
    "Dịch từng dòng một cách chính xác; vì sao thứ tự phép toán trong phương thức là đặc tả.",
    r"""
Bảng đặc tả của Q2 là một hợp đồng điền-khuyết. Một bảng tiêu biểu —
điểm kiểm tra của module này — đọc:

```text
Lớp: Signaler
Trường:
  - private int level        (bậc tín hiệu hiện tại, bắt đầu ở 1)
  - private int streak       (số lần strengthen liên tiếp, bắt đầu ở 0)
Constructor: Signaler() — cả hai trường ở giá trị khởi đầu.
Phương thức:
  void boost()      — level += streak; sau đó streak++
  void reset()      — level về 1; streak về 0
  int getLevel()    — reader
```

Quy trình là cơ học: dịch từng dòng, theo thứ tự. Hai dòng xứng đáng
được tôn trọng đặc biệt:

**"bắt đầu ở 0/1"** — đặt nó trong CONSTRUCTOR, không lười biếng. Người
chấm kiểm tra trạng thái ban đầu bằng một lời gọi getter trước mọi
phép biến đổi.

**Thứ tự bên trong một phương thức quan trọng.** `boost()` cộng streak
HIỆN TẠI vào level, SAU ĐÓ mới tăng streak. Hoán đổi hai dòng đó đổi
mọi giá trị sau này — truy vết `boost; boost; boost`: các mức 1+0=1,
1+1=2, 2+2=4 so với (nếu hoán đổi) 1+1=2, 2+2=4, 4+3=7. Cả hai đều là
"bản hiện thực"; chỉ một khớp với bảng. Khi bảng cho một thứ tự, thứ tự
đó chính là đặc tả.
""",
)

write_lesson(
    M, "cx-m15-helpers", "Helper decomposition",
    "Normalize invariants, classify-then-count, and same-class parameters.",
    12, L2,
    "Phân rã hàm trợ giúp",
    "Chuẩn hóa bất biến, phân-loại-rồi-đếm, và tham số cùng-lớp.",
    r"""
Q2 thưởng cho **phân rã hàm trợ giúp** — thường là tường minh ("một hàm
trợ giúp private có thể được điểm đầy đủ nếu dùng đúng"). Hai mẫu:

**Hàm chuẩn hóa.** Một lớp cất phút có thể cất giây thô bên trong và
chuẩn hóa khi ghi:

```java
private int totalSeconds;
private void normalize() {
    minutes += seconds / 60;   // ...qua các trường
    seconds = seconds % 60;
}
```

Hàm trợ giúp biến logic "nhớ-t tentang" thành một nơi được đặt tên;
các mutator gọi nó sau mỗi thay đổi. Đề thi thưởng cho điều này khi đặc
tả nói "bất biến: seconds < 60 luôn luôn".

**Hàm phân loại.** Phần (b) thường cần quyết định của phần (a):

```java
private boolean isPrime(int n) { ... }
public int countPrimes() {
    int c = 0;
    for (int v : values) { if (isPrime(v)) c++; }
    return c;
}
```

Viết bộ phân loại thành hàm trợ giúp khiến (b) thành hai dòng và khiến
phép truy vết của bạn dễ hơn (kiểm tra hàm trợ giúp với đầu vào nhỏ
trước).

**Tương tác đối tượng trong Q2** — "phương thức nhận một đối tượng khác
cùng lớp": `public void merge(Counter other)` đọc getter của other và
biến đổi this. Cái bẫy: biến đổi `other` thay vì `this` (nhầm lẫn
tham-số-bí-danh), hoặc đọc `this` ở chỗ đáng lẽ là `other`. Gọi to tên
đích của mọi phép gán khi viết.
""",
)

write_lesson(
    M, "cx-m15-seams", "Seam bugs",
    "Un-initialized fields, dual sources of truth, wrong-this mutations.",
    12, L3,
    "Lỗi khe hở",
    "Trường chưa khởi tạo, hai nguồn sự thật, biến đổi wrong-this.",
    r"""
Một biến thể Q2 hướng-sửa-chữa: cho một lớp *gần đúng*, các lỗi nằm ở
khe hở giữa các dòng của bảng đặc tả:

- **Trường chưa khởi tạo.** Constructor đặt hai trong ba trường; cái
  thứ ba trôi theo giá trị mặc định của Java (0/null). Nếu đặc tả nói
  nó bắt đầu ở 1, mọi phép tính chạm vào nó đều lệch — và test chỉ-getter
  vẫn pass trong khi test hành vi trượt.
- **Phương thức sao-chép-mà-không-gọi.** Một mutator tự tính lại một
  giá trị dẫn xuất mà phương thức khác CŨNG tính lại theo cách khác —
  hai nguồn sự thật. Bất biến của đặc tả ("count luôn bằng
  list.size()") là trọng tài: phương thức nào phá nó là phương thức có
  lỗi.
- **Biến đổi wrong-this.** `void adopt(Other o) { o.x = x; }` cập nhật
  tham số thay vì đối tượng nhận lời gọi. Trạng thái chảy ngược chiều;
  hành vi "biến đổi đối tượng này" trong bảng chấm lặng lẽ thất bại.

Kỷ luật sửa chữa: viết bảng đặc tả thành một checklist, tick từng dòng
đối chiếu mã, và chỉ sửa các dòng chưa tick. Trong phòng thi (gõ phím)
nó mất chín mươi giây và bắt được mọi lỗi khe hở ở trên.
""",
)

BOILER_SIGNALER = r"""public class Solution {
    // SPEC TABLE (complete the class):
    // private int level  — starts at 1
    // private int streak — starts at 0
    // Signaler()         — both at start values
    // void boost()  — level += streak; THEN streak++
    // void reset()  — level = 1; streak = 0
    // int getLevel()
    // int getStreak()
    public static class Signaler {
        // replace: fields, constructor, methods
    }
}
"""

BOILER_REGISTER = r"""public class Solution {
    // SPEC: a cash register.
    // private int itemCount — starts 0
    // private int totalCents — starts 0
    // void ring(int cents) — item count +1, total += cents
    // void clear() — both to start values
    // int getItemCount() / int getTotalCents()
    // int average() — totalCents / itemCount as int division;
    //   returns 0 when empty. (Precondition-safe: guard the empty case.)
    public static class Register {
        // replace
    }
}
"""

BOILER_MERGE = r"""public class Solution {
    // SPEC: a word accumulator.
    // private String joined — starts ""
    // private int wordCount — starts 0
    // void absorb(WordBag other) — append other's joined (in order)
    //   to THIS joined and add other's wordCount to THIS count;
    //   other is NOT modified.
    // void add(String w) — append w (space-separated) and count it
    // String getJoined() / int getCount()
    public static class WordBag {
        // replace
    }
}
"""

BOILER_SWAPPED = r"""public class Solution {
    // Repair: this DownCounter almost matches its spec.
    // SPEC: private int remaining (starts 5);
    // boolean tick() — when remaining > 0: decrement and return true;
    //   when remaining == 0: return false, NO change.
    // int getRemaining().
    // BUGS (find via the checklist): field never initialized to 5, and
    // tick() counts below zero.
    public static class DownCounter {
        private int remaining;

        public DownCounter() {
        }

        public boolean tick() {
            remaining--;
            return true;
        }

        public int getRemaining() { return remaining; }
    }
}
"""

BOILER_GRIDCOL = r"""public class Solution {
    // SPEC: a tiny grid summary class (Q2 with a helper):
    // private int[][] grid; private int rows; private int cols;
    // GridSummary(int[][] g) — store g, rows = g.length, cols = g[0].length
    // private int colSum(int c) — sum of column c (helper)
    // public int maxColSum() — the largest colSum (uses the helper)
    public static class GridSummary {
        // replace
    }
}
"""

BOILER_CP15 = r"""public class Solution {
    // FULL Q2 SPEC — Signaler, extended:
    // fields: int level (starts 1); int streak (starts 0); int boosts (starts 0)
    // void boost()    — level += streak; THEN streak++; THEN boosts++
    // void reset()    — level = 1; streak = 0  (boosts KEEPS counting)
    // int getLevel() / int getStreak() / int getBoosts()
    public static class Signaler2 {
        // replace
    }
}
"""

P_SIGNALER = challenge(
    "cx-m15-signaler",
    "Build from the table",
    "Complete `Signaler` exactly per the spec table — especially the ORDER inside boost(). Trace three boosts by hand and predict the level sequence before implementing.",
    BOILER_SIGNALER,
    [(
        "spec table honored",
        r"""
Solution.Signaler s = new Solution.Signaler();
CjTestBase.checkEq(s.getLevel(), 1, "starts at 1");
CjTestBase.checkEq(s.getStreak(), 0, "streak starts 0");
s.boost();
CjTestBase.checkEq(s.getLevel(), 1, "1 + 0");
CjTestBase.checkEq(s.getStreak(), 1, "streak now 1");
s.boost();
CjTestBase.checkEq(s.getLevel(), 2, "1 + 1");
s.boost();
CjTestBase.checkEq(s.getLevel(), 4, "2 + 2");
s.reset();
CjTestBase.checkEq(s.getLevel(), 1, "reset level");
CjTestBase.checkEq(s.getStreak(), 0, "reset streak");
""",
        "boost(): level += streak; streak++; — order is the specification.",
    )],
    level="guided",
)

P_REGISTER = challenge(
    "cx-m15-register",
    "Guard the empty case",
    "Complete `Register`. The subtlety: `average()` must return 0 when no items — the spec's guard. Everything else is translation.",
    BOILER_REGISTER,
    [(
        "register works",
        r"""
Solution.Register r = new Solution.Register();
CjTestBase.checkEq(r.getItemCount(), 0, "starts empty");
CjTestBase.checkEq(r.average(), 0, "empty average is 0");
r.ring(250);
r.ring(100);
CjTestBase.checkEq(r.getItemCount(), 2, "two items");
CjTestBase.checkEq(r.getTotalCents(), 350, "total");
CjTestBase.checkEq(r.average(), 175, "350 / 2");
r.clear();
CjTestBase.checkEq(r.getTotalCents(), 0, "cleared");
""",
        "average(): if (itemCount == 0) return 0; return totalCents / itemCount;",
    )],
    level="guided",
)

P_MERGE = challenge(
    "cx-m15-wordbag",
    "Same-class parameter",
    "Complete `WordBag`. `absorb` reads OTHER's state but mutates THIS only — the wrong-this trap from the lesson is what's being graded.",
    BOILER_MERGE,
    [(
        "absorb direction",
        r"""
Solution.WordBag a = new Solution.WordBag();
a.add("x");
a.add("y");
Solution.WordBag b = new Solution.WordBag();
b.add("z");
a.absorb(b);
CjTestBase.checkEq(a.getCount(), 3, "this grew");
CjTestBase.checkEq(a.getJoined(), "x y z", "appended in order");
CjTestBase.checkEq(b.getCount(), 1, "other untouched");
CjTestBase.checkEq(b.getJoined(), "z", "other untouched");
""",
        "joined += (wordCount > 0 ? \" \" : \"\") + other.joined; wordCount += other.wordCount;",
    )],
    level="combination",
)

P_DOWNCOUNTER = challenge(
    "cx-m15-fix-downcounter",
    "Repair via checklist",
    "`DownCounter` violates its spec in two places. Write the spec rows as a checklist, tick them against the code, and fix only the violations.",
    BOILER_SWAPPED,
    [(
        "spec restored",
        r"""
Solution.DownCounter d = new Solution.DownCounter();
CjTestBase.checkEq(d.getRemaining(), 5, "starts at 5");
CjTestBase.checkEq(d.tick(), true, "ticks down");
CjTestBase.checkEq(d.getRemaining(), 4, "4 left");
d.tick(); d.tick(); d.tick(); d.tick();
CjTestBase.checkEq(d.tick(), false, "empty: false");
CjTestBase.checkEq(d.getRemaining(), 0, "never below zero");
""",
        "Constructor: remaining = 5. tick(): if (remaining > 0) { remaining--; return true; } return false;",
    )],
    level="debugging",
)

P_GRIDSUM = challenge(
    "cx-m15-grid-summary",
    "Q2 with a helper",
    "Complete `GridSummary`: the constructor stores grid and dimensions; `colSum(c)` is the private helper; `maxColSum()` composes it. The helper pattern is the point — part (b) consuming part (a).",
    BOILER_GRIDCOL,
    [(
        "helper composed",
        r"""
int[][] g = { {1, 6}, {0, 1} };
Solution.GridSummary s = new Solution.GridSummary(g);
CjTestBase.checkEq(s.maxColSum(), 7, "columns sum 1 and 7");
Solution.GridSummary t = new Solution.GridSummary(new int[][]{{9}});
CjTestBase.checkEq(t.maxColSum(), 9, "single cell");
""",
        "maxColSum: seed from col 0, strict > to keep earliest.",
    )],
    level="real-world",
)

CP15 = challenge(
    "cx-cp-m15-signaler2",
    "Checkpoint: extended spec table",
    "Complete `Signaler2`: three fields, ordered mutator, and the subtle rule that reset() clears level/streak but NOT boosts. The table's parenthetical ('boosts KEEPS counting') is an obligation, not a remark.",
    BOILER_CP15,
    [(
        "extended spec honored",
        r"""
Solution.Signaler2 s = new Solution.Signaler2();
s.boost(); s.boost(); s.boost();
CjTestBase.checkEq(s.getLevel(), 4, "1+0, 1+1, 2+2");
CjTestBase.checkEq(s.getBoosts(), 3, "three boosts");
s.reset();
CjTestBase.checkEq(s.getLevel(), 1, "reset level");
CjTestBase.checkEq(s.getStreak(), 0, "reset streak");
CjTestBase.checkEq(s.getBoosts(), 3, "boosts SURVIVE reset");
s.boost();
CjTestBase.checkEq(s.getBoosts(), 4, "keeps counting after reset");
""",
        "reset(): level = 1; streak = 0; — do NOT touch boosts.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p15-frqclass", "FRQ class design lab",
    "Spec-table builds, a guarded average, same-class absorption, seam repair, helper composition.",
    "Phòng thiết kế lớp FRQ",
    "Dựng theo bảng đặc tả, trung bình có chặn, hấp thụ cùng-lớp, sửa khe hở, tổ hợp hàm trợ giúp.",
    after_lesson="cx-m15-helpers", minutes=60, difficulty="advanced",
    challenges=[P_SIGNALER, P_REGISTER, P_MERGE, P_DOWNCOUNTER, P_GRIDSUM],
    vi_challenges={
        "cx-m15-signaler": vi_challenge("Dựng theo bảng",
            "Hoàn thiện `Signaler` đúng theo bảng đặc tả — đặc biệt là THỨ TỰ bên trong boost(). Truy vết ba lần boost bằng tay và dự đoán dãy level trước khi hiện thực.",
            [("spec table honored", "boost(): level += streak; streak++; — thứ tự chính là đặc tả.")]),
        "cx-m15-register": vi_challenge("Chặn trường hợp rỗng",
            "Hoàn thiện `Register`. Điểm tinh tế: `average()` phải trả về 0 khi chưa có món — lớp chặn của đặc tả. Phần còn lại là dịch thuật.",
            [("register works", "average(): if (itemCount == 0) return 0; return totalCents / itemCount;")]),
        "cx-m15-wordbag": vi_challenge("Tham số cùng lớp",
            "Hoàn thiện `WordBag`. `absorb` đọc trạng thái của OTHER nhưng chỉ biến đổi THIS — cái bẫy wrong-this trong bài học là thứ được chấm.",
            [("absorb direction", "joined += (wordCount > 0 ? \" \" : \"\") + other.joined; wordCount += other.wordCount;")]),
        "cx-m15-fix-downcounter": vi_challenge("Sửa qua checklist",
            "`DownCounter` vi phạm đặc tả ở hai chỗ. Viết các dòng đặc tả thành checklist, tick đối chiếu mã, và chỉ sửa những chỗ vi phạm.",
            [("spec restored", "Constructor: remaining = 5. tick(): if (remaining > 0) { remaining--; return true; } return false;")]),
        "cx-m15-grid-summary": vi_challenge("Q2 với hàm trợ giúp",
            "Hoàn thiện `GridSummary`: constructor cất lưới và kích thước; `colSum(c)` là hàm trợ giúp private; `maxColSum()` tổ hợp nó. Mẫu hàm-trợ-giúp là điểm chính — phần (b) tiêu thụ phần (a).",
            [("helper composed", "maxColSum: seed từ cột 0, dấu > nghiêm ngặt để giữ sớm nhất.")]),
    },
    solutions=[
        ("cx-m15-signaler",
         BOILER_SIGNALER.replace("        // replace: fields, constructor, methods",
            "        private int level;\n        private int streak;\n\n        public Signaler() {\n            level = 1;\n            streak = 0;\n        }\n\n        public void boost() {\n            level += streak;\n            streak++;\n        }\n\n        public void reset() {\n            level = 1;\n            streak = 0;\n        }\n\n        public int getLevel() { return level; }\n        public int getStreak() { return streak; }"),
         BOILER_SIGNALER.replace("        // replace: fields, constructor, methods",
            "        private int level;\n        private int streak;\n\n        public Signaler() {\n            level = 1;\n            streak = 0;\n        }\n\n        public void boost() {\n            streak++;\n            level += streak;\n        }\n\n        public void reset() {\n            level = 1;\n            streak = 0;\n        }\n\n        public int getLevel() { return level; }\n        public int getStreak() { return streak; }")),
        ("cx-m15-register",
         BOILER_REGISTER.replace("        // replace",
            "        private int itemCount;\n        private int totalCents;\n\n        public Register() {\n            itemCount = 0;\n            totalCents = 0;\n        }\n\n        public void ring(int cents) {\n            itemCount++;\n            totalCents += cents;\n        }\n\n        public void clear() {\n            itemCount = 0;\n            totalCents = 0;\n        }\n\n        public int getItemCount() { return itemCount; }\n        public int getTotalCents() { return totalCents; }\n\n        public int average() {\n            if (itemCount == 0) {\n                return 0;\n            }\n            return totalCents / itemCount;\n        }"),
         BOILER_REGISTER.replace("        // replace",
            "        private int itemCount;\n        private int totalCents;\n\n        public Register() {\n            itemCount = 0;\n            totalCents = 0;\n        }\n\n        public void ring(int cents) {\n            itemCount++;\n            totalCents += cents;\n        }\n\n        public void clear() {\n            itemCount = 0;\n            totalCents = 0;\n        }\n\n        public int getItemCount() { return itemCount; }\n        public int getTotalCents() { return totalCents; }\n\n        public int average() {\n            if (itemCount == 0) {\n                return -1;\n            }\n            return totalCents / itemCount;\n        }")),
        ("cx-m15-wordbag",
         BOILER_MERGE.replace("        // replace",
            "        private String joined;\n        private int wordCount;\n\n        public WordBag() {\n            joined = \"\";\n            wordCount = 0;\n        }\n\n        public void add(String w) {\n            if (wordCount > 0) {\n                joined += \" \";\n            }\n            joined += w;\n            wordCount++;\n        }\n\n        public void absorb(WordBag other) {\n            if (other.wordCount > 0) {\n                if (wordCount > 0) {\n                    joined += \" \";\n                }\n                joined += other.joined;\n                wordCount += other.wordCount;\n            }\n        }\n\n        public String getJoined() { return joined; }\n        public int getCount() { return wordCount; }"),
         BOILER_MERGE.replace("        // replace",
            "        private String joined;\n        private int wordCount;\n\n        public WordBag() {\n            joined = \"\";\n            wordCount = 0;\n        }\n\n        public void add(String w) {\n            if (wordCount > 0) {\n                joined += \" \";\n            }\n            joined += w;\n            wordCount++;\n        }\n\n        public void absorb(WordBag other) {\n            if (other.wordCount > 0) {\n                if (other.wordCount > 0) {\n                    other.joined += \" \";\n                }\n                other.joined += joined;\n                other.wordCount += wordCount;\n            }\n        }\n\n        public String getJoined() { return joined; }\n        public int getCount() { return wordCount; }")),
        ("cx-m15-fix-downcounter",
         BOILER_SWAPPED.replace("        public DownCounter() {\n        }",
            "        public DownCounter() {\n            remaining = 5;\n        }")
            .replace("        public boolean tick() {\n            remaining--;\n            return true;\n        }",
                "        public boolean tick() {\n            if (remaining > 0) {\n                remaining--;\n                return true;\n            }\n            return false;\n        }"),
         BOILER_SWAPPED.replace("        public DownCounter() {\n        }",
            "        public DownCounter() {\n            remaining = 5;\n        }")
            .replace("        public boolean tick() {\n            remaining--;\n            return true;\n        }",
                "        public boolean tick() {\n            if (remaining >= 0) {\n                remaining--;\n                return true;\n            }\n            return false;\n        }")),
        ("cx-m15-grid-summary",
         BOILER_GRIDCOL.replace("        // replace",
            "        private int[][] grid;\n        private int rows;\n        private int cols;\n\n        public GridSummary(int[][] g) {\n            grid = g;\n            rows = g.length;\n            cols = g[0].length;\n        }\n\n        private int colSum(int c) {\n            int sum = 0;\n            for (int r = 0; r < rows; r++) {\n                sum += grid[r][c];\n            }\n            return sum;\n        }\n\n        public int maxColSum() {\n            int best = colSum(0);\n            for (int c = 1; c < cols; c++) {\n                if (colSum(c) > best) {\n                    best = colSum(c);\n                }\n            }\n            return best;\n        }"),
         BOILER_GRIDCOL.replace("        // replace",
            "        private int[][] grid;\n        private int rows;\n        private int cols;\n\n        public GridSummary(int[][] g) {\n            grid = g;\n            rows = g.length;\n            cols = g[0].length;\n        }\n\n        private int colSum(int c) {\n            int sum = 0;\n            for (int r = 0; r < rows; r++) {\n                sum += grid[r][c];\n            }\n            return sum;\n        }\n\n        public int maxColSum() {\n            int best = colSum(0);\n            for (int c = 1; c < cols; c++) {\n                if (colSum(c) < best) {\n                    best = colSum(c);\n                }\n            }\n            return best;\n        }")),
    ],
)

write_checkpoint(
    M, "cx-cp-m15", "Checkpoint: Signaler2",
    "A three-field spec table with a counter that survives reset.",
    30,
    r"""
The extended table tests one idea: which state does reset() return to
the start values? Only what the table says. Fields not mentioned keep
their continuity — boosts keeps counting. Graders grade the
parentheticals: every note in a spec table is an obligation, and the
difference between a 6 and a 9 on Q2 is usually two of them.
""",
    "Điểm kiểm tra: Signaler2",
    "Bảng đặc tả ba trường với một bộ đếm sống sót qua reset.",
    r"""
Bảng mở rộng test một ý tưởng: reset() đưa những trạng thái nào về giá
trị khởi đầu? Chỉ những gì bảng nói. Các trường không được nhắc tới giữ
nguyên tính liên tục — boosts tiếp tục đếm. Người chấm chấm cả các chú
thích: mọi ghi chú trong bảng đặc tả là một nghĩa vụ, và khoảng cách
giữa 6 và 9 điểm của Q2 thường là hai chú thích.
""",
    CP15,
    vi_challenge("Điểm kiểm tra: Signaler2",
        "Hoàn thiện `Signaler2`: ba trường, mutator có thứ tự, và luật tinh tế rằng reset() xóa level/streak nhưng KHÔNG xóa boosts. Chú thích trong ngoặc ('boosts KEEPS counting') là một nghĩa vụ, không phải một nhận xét.",
        [("extended spec honored", "reset(): level = 1; streak = 0; — ĐỪNG chạm vào boosts.")]),
    solution=r"""public class Solution {
    public static class Signaler2 {
        private int level;
        private int streak;
        private int boosts;

        public Signaler2() {
            level = 1;
            streak = 0;
            boosts = 0;
        }

        public void boost() {
            level += streak;
            streak++;
            boosts++;
        }

        public void reset() {
            level = 1;
            streak = 0;
        }

        public int getLevel() { return level; }
        public int getStreak() { return streak; }
        public int getBoosts() { return boosts; }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Signaler2 {
        private int level;
        private int streak;
        private int boosts;

        public Signaler2() {
            level = 1;
            streak = 0;
            boosts = 0;
        }

        public void boost() {
            level += streak;
            streak++;
            boosts++;
        }

        public void reset() {
            level = 1;
            streak = 0;
            boosts = 0;
        }

        public int getLevel() { return level; }
        public int getStreak() { return streak; }
        public int getBoosts() { return boosts; }
    }
}
""",
)
