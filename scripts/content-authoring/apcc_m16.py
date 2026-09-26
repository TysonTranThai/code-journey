#!/usr/bin/env python3
"""AP CSA Core M16 — FRQ ArrayList Analysis (Q3)."""
from apcc import *

M = "cx-frq-list"

L1 = r"""
Q3 hands you a provided class and asks you to write ONE method — the
whole question is that method. The list usually holds objects:

```java
// provided:
public class Order {
    private String customer;
    private int cents;
    public Order(String c, int cents) { customer = c; this.cents = cents; }
    public String getCustomer() { return customer; }
    public int getCents() { return cents; }
}
// to write: total for one customer
public int customerTotal(ArrayList<Order> orders, String name) { ... }
```

The Q3 playbook is three verbs:

- **count** — how many orders belong to "Ana"? (filter + counter)
- **match** — find the first/last order matching a condition (filter +
  sentinel)
- **process** — aggregate or transform (filter + accumulator)

Every Q3 answer is a for-each (reading) or indexed loop (mutating)
plus one machine. The wrapper class changes; the machines never do.
The exam's twist is usually in the **specification prose**: "adjacent
duplicates count once", "orders before the first rejection only",
"ties broken by earliest" — underline those phrases; they are the
obligations that separate 6 from 9.
"""

L2 = r"""
**String tokens inside Q3** — the exam loves lists of words:

*"Count words that start and end with the same letter"*

```java
public int sameEnds(ArrayList<String> words) {
    int count = 0;
    for (String w : words) {
        if (w.length() > 0 && w.charAt(0) == w.charAt(w.length() - 1)) {
            count++;
        }
    }
    return count;
}
```

Two obligations hide in one line: the guard `w.length() > 0` (empty
strings are legal elements!) and the first/last comparison. Swap
charAt order and nothing changes; forget the guard and a single
empty-string element throws — the test that separates 8 from 9.

**Autoboxing in Q3 answers:** `ArrayList<Integer>` totals need no
special handling (`int sum += list.get(i)` unboxes), but `equals`
still beats `==` when the spec says "the Integer equal to" — for
small values they agree; for exam values, write `.equals` or unbox
explicitly.

**Mutating Q3** — when the question says "remove", the answer is the
backward loop (Module 7) wearing a Q3 wrapper class. The provided
class never changes the rules of mutation.
"""

L3 = r"""
Multi-part Q3: part (a) computes, part (b) consumes part (a).

*"You may write a private helper."*

```java
// (a) private int maxGap(ArrayList<Integer> temps):
//     largest difference between ADJACENT entries; 0 for size < 2.
private int maxGap(ArrayList<Integer> temps) {
    if (temps.size() < 2) { return 0; }
    int best = 0;
    for (int i = 1; i < temps.size(); i++) {
        int gap = Math.abs(temps.get(i) - temps.get(i - 1));
        if (gap > best) { best = gap; }
    }
    return best;
}

// (b) public boolean unstable(ArrayList<Integer> temps):
//     true when maxGap is 10 or more.
public boolean unstable(ArrayList<Integer> temps) {
    return maxGap(temps) >= 10;
}
```

Part (a) is adjacency + accumulator; part (b) is one comparison. The
exam's part (b) often flips a perspective: "for how many positions is
the gap ≥ 10?" — then (b) counts gaps qualifying instead of returning
a boolean, reusing the same helper.

Grade-hunting insight: if (b) is stuck, shipping a correct (a) with a
correct helper still banks most of the question's points. Never
sacrifice (a)'s correctness to gamble on (b).
"""

write_module(
    M,
    "FRQ ArrayList Analysis",
    "Q3's one-method answers: count/match/process over object lists, token analysis, and multi-part helpers.",
    "Phân tích ArrayList kiểu FRQ",
    "Các lời giải một-phương-thức của Q3: đếm/khớp/xử lý trên danh sách đối tượng, phân tích token, và hàm trợ giúp đa phần.",
    lessons=["cx-m16-q3-shape", "cx-m16-tokens", "cx-m16-multipart", "cx-cp-m16"],
    practices=["cx-p16-frqlist"],
)

write_lesson(
    M, "cx-m16-q3-shape", "The Q3 shape",
    "Provided class + one method; count, match, process; prose obligations.",
    12, L1,
    "Hình dạng Q3",
    "Lớp cho sẵn + một phương thức; đếm, khớp, xử lý; các nghĩa vụ trong lời văn.",
    r"""
Q3 đưa cho bạn một lớp cho sẵn và yêu cầu viết MỘT phương thức — toàn
bộ câu hỏi nằm ở phương thức đó. Danh sách thường chứa đối tượng:

```java
// cho sẵn:
public class Order {
    private String customer;
    private int cents;
    public Order(String c, int cents) { customer = c; this.cents = cents; }
    public String getCustomer() { return customer; }
    public int getCents() { return cents; }
}
// cần viết: tổng cho một khách hàng
public int customerTotal(ArrayList<Order> orders, String name) { ... }
```

Sách lược Q3 là ba động từ:

- **đếm** — bao nhiêu đơn thuộc về "Ana"? (lọc + bộ đếm)
- **khớp** — tìm đơn đầu/cuối khớp điều kiện (lọc + lính canh)
- **xử lý** — cộng dồn hoặc biến đổi (lọc + bộ cộng dồn)

Mọi lời giải Q3 là một for-each (đọc) hoặc vòng có chỉ số (biến đổi)
cộng đúng một cỗ máy. Lớp bọc thay đổi; các cỗ máy không bao giờ đổi.
Cú twist của đề thi thường nằm trong **lời văn đặc tả**: "phần tử trùng
liền kề chỉ đếm một lần", "chỉ các đơn trước lần từ-chối đầu tiên",
"đồng giá ưu tiên cái sớm nhất" — gạch dưới những cụm đó; chúng là các
nghĩa vụ phân cách 6 điểm và 9 điểm.
""",
)

write_lesson(
    M, "cx-m16-tokens", "Tokens and boxing",
    "Word lists with per-string obligations; autoboxing in totals.",
    12, L2,
    "Token và boxing",
    "Danh sách từ với các nghĩa vụ theo-chuỗi; autoboxing trong phép cộng dồn.",
    r"""
**Token chuỗi bên trong Q3** — đề thi mê danh sách các từ:

*"Đếm từ bắt đầu và kết thúc bằng cùng một chữ cái"*

```java
public int sameEnds(ArrayList<String> words) {
    int count = 0;
    for (String w : words) {
        if (w.length() > 0 && w.charAt(0) == w.charAt(w.length() - 1)) {
            count++;
        }
    }
    return count;
}
```

Hai nghĩa vụ nấp trong một dòng: lớp chặn `w.length() > 0` (chuỗi rỗng
là phần tử hợp lệ!) và phép so sánh đầu/cuối. Đổi thứ tự charAt chẳng
đổi gì; quên lớp chặn và một phần tử chuỗi-rỗng-duy-nhất sẽ ném ngoại
lệ — chính là bài kiểm tra phân cách 8 điểm và 9 điểm.

**Autoboxing trong lời giải Q3:** tổng trên `ArrayList<Integer>` không
cần xử lý gì đặc biệt (`int sum += list.get(i)` tự mở hộp), nhưng
`.equals` vẫn thắng `==` khi đặc tả nói "the Integer bằng với" — với
giá trị nhỏ chúng đồng ý; với giá trị trong đề, hãy viết `.equals` hoặc
mở hộp tường minh.

**Q3 biến đổi** — khi câu hỏi nói "xóa", đáp án là vòng ngược (Module 7)
khoác lớp wrapper Q3. Lớp cho sẵn không bao giờ đổi luật của phép biến
đổi.
""",
)

write_lesson(
    M, "cx-m16-multipart", "Multi-part Q3",
    "Helper in (a), consumer in (b); how part (b) flips perspective.",
    12, L3,
    "Q3 đa phần",
    "Hàm trợ giúp ở (a), bộ tiêu thụ ở (b); cách phần (b) đảo góc nhìn.",
    r"""
Q3 đa phần: phần (a) tính, phần (b) tiêu thụ phần (a).

*"Bạn được viết một hàm trợ giúp private."*

```java
// (a) private int maxGap(ArrayList<Integer> temps):
//     hiệu lớn nhất giữa hai phần tử LIỀN KỀ; 0 cho size < 2.
private int maxGap(ArrayList<Integer> temps) {
    if (temps.size() < 2) { return 0; }
    int best = 0;
    for (int i = 1; i < temps.size(); i++) {
        int gap = Math.abs(temps.get(i) - temps.get(i - 1));
        if (gap > best) { best = gap; }
    }
    return best;
}

// (b) public boolean unstable(ArrayList<Integer> temps):
//     true khi maxGap từ 10 trở lên.
public boolean unstable(ArrayList<Integer> temps) {
    return maxGap(temps) >= 10;
}
```

Phần (a) là quét-liền-kề + bộ cộng dồn; phần (b) là một phép so sánh.
Phần (b) của đề thi thường đảo một góc nhìn: "có bao nhiêu vị trí có
khoảng cách ≥ 10?" — khi đó (b) đếm các khoảng-cách-đạt-chuẩn thay vì
trả về boolean, tái dùng cùng hàm trợ giúp.

Trực giác săn-điểm: nếu (b) bí, nộp một (a) đúng với hàm trợ giúp đúng
vẫn mang về đa số điểm của câu. Đừng bao giờ hy sinh tính đúng của (a)
để đánh bạc với (b).
""",
)

ORDERS = r"""import java.util.ArrayList;

public class Solution {
    public static class Order {
        private String customer;
        private int cents;
        public Order(String customer, int cents) {
            this.customer = customer;
            this.cents = cents;
        }
        public String getCustomer() { return customer; }
        public int getCents() { return cents; }
    }

    // CONTRACT: total cents across all orders of `name`.
    public static int customerTotal(ArrayList<Order> orders, String name) {
        return 0; // replace
    }
}
"""

BOILER_SAMEENDS = r"""import java.util.ArrayList;

public class Solution {
    // CONTRACT: count words that start AND end with the same letter
    // (length >= 1 only; empty strings count 0).
    public static int sameEnds(ArrayList<String> words) {
        return 0; // replace
    }
}
"""

BOILER_REMOVECOLD = r"""import java.util.ArrayList;

public class Solution {
    public static class Reading {
        private int celsius;
        public Reading(int celsius) { this.celsius = celsius; }
        public int getCelsius() { return celsius; }
    }

    // CONTRACT: remove every reading with celsius below `limit`,
    // in place. Backward loop expected.
    public static void removeCold(ArrayList<Reading> readings, int limit) {
        // replace
    }
}
"""

BOILER_GAP = r"""import java.util.ArrayList;

public class Solution {
    // (a) CONTRACT: largest absolute difference between ADJACENT
    //     entries; 0 when size < 2.
    // (b) CONTRACT: true when the largest gap is 10 or more.
    public static int maxGap(ArrayList<Integer> temps) {
        return 0; // replace
    }

    public static boolean unstable(ArrayList<Integer> temps) {
        return false; // replace
    }
}
"""

BOILER_FIRSTGAP = r"""import java.util.ArrayList;

public class Solution {
    // CONTRACT: index of the FIRST Integer strictly greater than
    // `threshold`, or -1 when none. Use indexOf-style logic.
    public static int firstAbove(ArrayList<Integer> nums, int threshold) {
        return -1; // replace
    }
}
"""

BOILER_CP16 = r"""import java.util.ArrayList;

public class Solution {
    public static class Ticket {
        private String zone;
        private int minutes;
        public Ticket(String zone, int minutes) {
            this.zone = zone;
            this.minutes = minutes;
        }
        public String getZone() { return zone; }
        public int getMinutes() { return minutes; }
    }

    // TWO-PART Q3:
    // (a) int zoneTotal(ArrayList<Ticket> tickets, String zone):
    //     total minutes of tickets in `zone`.
    // (b) boolean overtime(ArrayList<Ticket> tickets, String zone,
    //     int limit): true when zoneTotal(...) for that zone is
    //     strictly greater than limit. Use part (a).
    public static int zoneTotal(ArrayList<Ticket> tickets, String zone) {
        return 0; // replace
    }

    public static boolean overtime(ArrayList<Ticket> tickets, String zone, int limit) {
        return false; // replace
    }
}
"""

P_ORDERS = challenge(
    "cx-m16-customer-total",
    "Q3: filter and aggregate",
    "Implement `customerTotal`: total cents across the named customer's orders. One for-each, one filter, one accumulator — the Q3 playbook, page one.",
    ORDERS,
    [(
        "customer total",
        r"""
ArrayList<Solution.Order> orders = new ArrayList<Solution.Order>();
orders.add(new Solution.Order("Ana", 500));
orders.add(new Solution.Order("Bao", 200));
orders.add(new Solution.Order("Ana", 300));
CjTestBase.checkEq(Solution.customerTotal(orders, "Ana"), 800, "500 + 300");
CjTestBase.checkEq(Solution.customerTotal(orders, "Bao"), 200, "single order");
CjTestBase.checkEq(Solution.customerTotal(orders, "Chi"), 0, "no orders");
CjTestBase.checkEq(Solution.customerTotal(new ArrayList<Solution.Order>(), "Ana"), 0, "empty list");
""",
        "for (Order o : orders) if (o.getCustomer().equals(name)) total += o.getCents();",
    )],
    level="guided",
)

P_SAMEENDS = challenge(
    "cx-m16-same-ends",
    "Q3: token obligations",
    "Implement `sameEnds`. The empty-string element is legal and counts 0 — forgetting its guard is the planted trap the rubric pays for.",
    BOILER_SAMEENDS,
    [(
        "ends matched",
        r"""
ArrayList<String> words = new ArrayList<String>();
words.add("eve");
words.add("ann");
words.add("");
words.add("bob");
words.add("cat");
CjTestBase.checkEq(Solution.sameEnds(words), 2, "eve and bob (ann: a vs n)");
CjTestBase.checkEq(Solution.sameEnds(new ArrayList<String>()), 0, "empty list");
ArrayList<String> single = new ArrayList<String>();
single.add("");
CjTestBase.checkEq(Solution.sameEnds(single), 0, "empty string element");
""",
        "Guard w.length() > 0 before charAt(0).",
    )],
    level="combination",
)

P_REMOVECOLD = challenge(
    "cx-m16-remove-cold",
    "Q3: object removal",
    "Implement `removeCold`: drop every Reading below `limit`, in place — the backward removal loop behind a wrapper class.",
    BOILER_REMOVECOLD,
    [(
        "cold readings removed",
        r"""
ArrayList<Solution.Reading> rs = new ArrayList<Solution.Reading>();
rs.add(new Solution.Reading(5));
rs.add(new Solution.Reading(3));
rs.add(new Solution.Reading(12));
rs.add(new Solution.Reading(11));
Solution.removeCold(rs, 10);
CjTestBase.checkEq(rs.size(), 2, "12 and 11 survive");
CjTestBase.checkEq(rs.get(0).getCelsius(), 12, "order preserved");
""",
        "for (int i = rs.size() - 1; i >= 0; i--) if (rs.get(i).getCelsius() < limit) rs.remove(i);",
    )],
    level="combination",
)

P_GAP = challenge(
    "cx-m16-max-gap",
    "Q3: helper + consumer",
    "Implement both parts: `maxGap` (adjacency accumulator with the size<2 guard) and `unstable` (one comparison reusing it). Part (b) consuming part (a) is the graded shape.",
    BOILER_GAP,
    [(
        "gap and verdict",
        r"""
ArrayList<Integer> a = new ArrayList<Integer>();
a.add(3); a.add(5); a.add(18); a.add(20);
CjTestBase.checkEq(Solution.maxGap(a), 13, "5 -> 18");
CjTestBase.checkEq(Solution.unstable(a), true, "13 >= 10");
ArrayList<Integer> b = new ArrayList<Integer>();
b.add(1); b.add(4);
CjTestBase.checkEq(Solution.maxGap(b), 3, "small gap");
CjTestBase.checkEq(Solution.unstable(b), false, "3 < 10");
ArrayList<Integer> c = new ArrayList<Integer>();
c.add(0); c.add(10);
CjTestBase.checkEq(Solution.unstable(c), true, "gap exactly 10 counts");
CjTestBase.checkEq(Solution.maxGap(new ArrayList<Integer>()), 0, "empty guard");
CjTestBase.checkEq(Solution.unstable(new ArrayList<Integer>()), false, "empty is stable");
""",
        "maxGap guards size < 2, then adjacency-scan with Math.abs; unstable is maxGap >= 10.",
    )],
    level="real-world",
)

P_FIRSTABOVE = challenge(
    "cx-m16-first-above",
    "Q3: first match index",
    "Implement `firstAbove`: the index of the first Integer strictly greater than threshold, or -1. A filter + sentinel — with the fix of Module 1's findFirst already built in (return immediately).",
    BOILER_FIRSTGAP,
    [(
        "first above found",
        r"""
ArrayList<Integer> nums = new ArrayList<Integer>();
nums.add(1); nums.add(9); nums.add(9); nums.add(2);
CjTestBase.checkEq(Solution.firstAbove(nums, 5), 1, "first 9, not the second");
CjTestBase.checkEq(Solution.firstAbove(nums, 100), -1, "none above");
CjTestBase.checkEq(Solution.firstAbove(new ArrayList<Integer>(), 0), -1, "empty list");
""",
        "Loop with index; return i immediately on the first hit; -1 after the loop.",
    )],
    level="independent",
)

CP16 = challenge(
    "cx-cp-m16-zone-tickets",
    "Checkpoint: two-part Q3",
    "The complete Q3: `zoneTotal` (filter + aggregate over objects) and `overtime` (composes zoneTotal with a comparison). Run the eight-step workflow; ship (a) even if (b) fights you.",
    BOILER_CP16,
    [(
        "zones analyzed",
        r"""
ArrayList<Solution.Ticket> ts = new ArrayList<Solution.Ticket>();
ts.add(new Solution.Ticket("A", 30));
ts.add(new Solution.Ticket("B", 90));
ts.add(new Solution.Ticket("A", 45));
CjTestBase.checkEq(Solution.zoneTotal(ts, "A"), 75, "30 + 45");
CjTestBase.checkEq(Solution.zoneTotal(ts, "C"), 0, "absent zone");
CjTestBase.checkEq(Solution.overtime(ts, "A", 60), true, "75 > 60");
CjTestBase.checkEq(Solution.overtime(ts, "B", 60), true, "90 > 60");
CjTestBase.checkEq(Solution.overtime(ts, "B", 90), false, "strictly greater only");
CjTestBase.checkEq(Solution.overtime(ts, "C", 0), false, "0 > 0 is false");
""",
        "zoneTotal: for-each + zone filter + minute accumulator; overtime: zoneTotal > limit.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p16-frqlist", "FRQ ArrayList lab",
    "Object aggregation, token guards, backward removal, helper composition, first-match.",
    "Phòng ArrayList kiểu FRQ",
    "Cộng dồn đối tượng, lớp chặn token, xóa ngược, tổ hợp hàm trợ giúp, khớp đầu tiên.",
    after_lesson="cx-m16-tokens", minutes=60, difficulty="advanced",
    challenges=[P_ORDERS, P_SAMEENDS, P_REMOVECOLD, P_GAP, P_FIRSTABOVE],
    vi_challenges={
        "cx-m16-customer-total": vi_challenge("Q3: lọc và cộng dồn",
            "Hiện thực `customerTotal`: tổng cents qua các đơn của khách được nêu tên. Một for-each, một bộ lọc, một bộ cộng dồn — sách lược Q3, trang một.",
            [("customer total", "for (Order o : orders) if (o.getCustomer().equals(name)) total += o.getCents();")]),
        "cx-m16-same-ends": vi_challenge("Q3: nghĩa vụ token",
            "Hiện thực `sameEnds`. Phần tử chuỗi-rỗng là hợp lệ và đếm 0 — quên lớp chặn của nó chính là cái bẫy được cài và bảng chấm trả tiền cho nó.",
            [("ends matched", "Chặn w.length() > 0 trước charAt(0).")]),
        "cx-m16-remove-cold": vi_challenge("Q3: xóa đối tượng",
            "Hiện thực `removeCold`: bỏ mọi Reading dưới `limit`, tại chỗ — vòng xóa ngược sau một lớp bọc.",
            [("cold readings removed", "for (int i = rs.size() - 1; i >= 0; i--) if (rs.get(i).getCelsius() < limit) rs.remove(i);")]),
        "cx-m16-max-gap": vi_challenge("Q3: hàm trợ giúp + bộ tiêu thụ",
            "Hiện thực cả hai phần: `maxGap` (bộ cộng dồn liền-kề với lớp chặn size<2) và `unstable` (một phép so sánh tái dùng nó). Hình (b)-tiêu-thụ-(a) là hình được chấm.",
            [("gap and verdict", "maxGap chặn size < 2, rồi quét liền kề với Math.abs; unstable là maxGap >= 10.")]),
        "cx-m16-first-above": vi_challenge("Q3: chỉ số khớp đầu tiên",
            "Hiện thực `firstAbove`: chỉ số của Integer đầu tiên lớn hơn nghiêm ngặt threshold, hoặc -1. Một bộ lọc + lính canh — với bản sửa findFirst của Module 1 đã có sẵn (trả về ngay lập tức).",
            [("first above found", "Vòng lặp có chỉ số; trả về i ngay tại lần trúng đầu; -1 sau vòng lặp.")]),
    },
    solutions=[
        ("cx-m16-customer-total", ORDERS.replace("        return 0; // replace",
            "        int total = 0;\n        for (Order o : orders) {\n            if (o.getCustomer().equals(name)) {\n                total += o.getCents();\n            }\n        }\n        return total;"),
         ORDERS.replace("        return 0; // replace",
            "        int total = 0;\n        for (Order o : orders) {\n            if (!o.getCustomer().equals(name)) {\n                total += o.getCents();\n            }\n        }\n        return total;")),
        ("cx-m16-same-ends", BOILER_SAMEENDS.replace("        return 0; // replace",
            "        int count = 0;\n        for (String w : words) {\n            if (w.length() > 0 && w.charAt(0) == w.charAt(w.length() - 1)) {\n                count++;\n            }\n        }\n        return count;"),
         BOILER_SAMEENDS.replace("        return 0; // replace",
            "        int count = 0;\n        for (String w : words) {\n            if (w.length() >= 0 && w.charAt(0) == w.charAt(w.length() - 1)) {\n                count++;\n            }\n        }\n        return count;")),
        ("cx-m16-remove-cold",
         r"""import java.util.ArrayList;

public class Solution {
    public static class Reading {
        private int celsius;
        public Reading(int celsius) { this.celsius = celsius; }
        public int getCelsius() { return celsius; }
    }

    public static void removeCold(ArrayList<Reading> readings, int limit) {
        for (int i = readings.size() - 1; i >= 0; i--) {
            if (readings.get(i).getCelsius() < limit) {
                readings.remove(i);
            }
        }
    }
}
""",
         r"""import java.util.ArrayList;

public class Solution {
    public static class Reading {
        private int celsius;
        public Reading(int celsius) { this.celsius = celsius; }
        public int getCelsius() { return celsius; }
    }

    public static void removeCold(ArrayList<Reading> readings, int limit) {
        for (int i = 0; i < readings.size(); i++) {
            if (readings.get(i).getCelsius() < limit) {
                readings.remove(i);
            }
        }
    }
}
"""),
        ("cx-m16-max-gap",
         BOILER_GAP.replace("        return 0; // replace", "        if (temps.size() < 2) {\n            return 0;\n        }\n        int best = 0;\n        for (int i = 1; i < temps.size(); i++) {\n            int gap = Math.abs(temps.get(i) - temps.get(i - 1));\n            if (gap > best) {\n                best = gap;\n            }\n        }\n        return best;")
            .replace("        return false; // replace", "        return maxGap(temps) >= 10;"),
         BOILER_GAP.replace("        return 0; // replace", "        if (temps.size() < 2) {\n            return 0;\n        }\n        int best = 0;\n        for (int i = 1; i < temps.size(); i++) {\n            int gap = Math.abs(temps.get(i) - temps.get(i - 1));\n            if (gap > best) {\n                best = gap;\n            }\n        }\n        return best;")
            .replace("        return false; // replace", "        return maxGap(temps) > 10;")),
        ("cx-m16-first-above", BOILER_FIRSTGAP.replace("        return -1; // replace",
            "        for (int i = 0; i < nums.size(); i++) {\n            if (nums.get(i) > threshold) {\n                return i;\n            }\n        }\n        return -1;"),
         BOILER_FIRSTGAP.replace("        return -1; // replace",
            "        for (int i = 0; i < nums.size(); i++) {\n            if (nums.get(i) > threshold) {\n                return nums.size() - 1 - i;\n            }\n        }\n        return -1;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m16", "Checkpoint: zone tickets",
    "The two-part Q3: aggregate in (a), compose in (b), ship (a) no matter what.",
    30,
    r"""
zoneTotal is the Q3 playbook in one method; overtime is its consumer.
Notice what the checkpoint graded: the strict `>` in overtime (a
prose obligation), the absent-zone zero (an edge from the examples),
and the composition itself. When the real exam's part (b) stumps you,
(a)'s machines are worth their points regardless — ship them.
""",
    "Điểm kiểm tra: vé theo khu",
    "Q3 hai phần: cộng dồn ở (a), tổ hợp ở (b), nộp (a) dù thế nào.",
    r"""
zoneTotal là sách lược Q3 gọn trong một phương thức; overtime là bộ
tiêu thụ của nó. Chú ý những gì điểm kiểm tra chấm: dấu `>` nghiêm ngặt
trong overtime (một nghĩa vụ lời-văn), số 0 cho khu-vắng-mặt (một biên
từ ví dụ), và bản thân phép tổ hợp. Khi phần (b) của đề thật làm bạn bí,
các cỗ máy của (a) vẫn đáng giá điểm của chúng bất kể — hãy nộp.
""",
    CP16,
    vi_challenge("Điểm kiểm tra: vé theo khu",
        "Trọn bộ Q3: `zoneTotal` (lọc + cộng dồn trên đối tượng) và `overtime` (tổ hợp zoneTotal với một phép so sánh). Chạy quy trình tám bước; nộp (a) kể cả khi (b) khó nhằn.",
        [("zones analyzed", "zoneTotal: for-each + lọc zone + bộ cộng dồn phút; overtime: zoneTotal > limit.")]),
    solution=BOILER_CP16.replace("        return 0; // replace",
        "        int total = 0;\n        for (Ticket t : tickets) {\n            if (t.getZone().equals(zone)) {\n                total += t.getMinutes();\n            }\n        }\n        return total;")
        .replace("        return false; // replace", "        return zoneTotal(tickets, zone) > limit;"),
    wrong=BOILER_CP16.replace("        return 0; // replace",
        "        int total = 0;\n        for (Ticket t : tickets) {\n            if (t.getZone().equals(zone)) {\n                total += t.getMinutes();\n            }\n        }\n        return total;")
        .replace("        return false; // replace", "        return zoneTotal(tickets, zone) >= limit;"),
)
