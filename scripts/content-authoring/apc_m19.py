#!/usr/bin/env python3
"""AP CSA M19 — Integrated AP CSA problems: mixed units, exam-shape synthesis."""
from apc import *

M = "apc-integration"

L1 = r"""
Integrated problems combine units the way the exam does. A single
question may demand: an ArrayList of objects, a traversal, a String
method, and a boolean contract. The strategy:

1. **Inventory** — list the types in play (`ArrayList<Song>`, `int`,
   `boolean`). Each type names a toolbox from an earlier module.
2. **Decompose** — one method per sub-task. "Find the best" and "print
   the report" are two methods, not one tangled loop.
3. **Contract per method** — one sentence: what goes in, what comes
   out, what's guaranteed.
4. **Assemble** — the driver method calls the pieces in order.

```java
// Pieces: findBest(list), countBelow(list, cut)
public static ArrayList<String> topNames(ArrayList<Song> list, int cut) {
    ArrayList<String> names = new ArrayList<String>();
    for (Song s : list) {
        if (s.getPlays() >= cut) {
            names.add(s.getTitle());
        }
    }
    return names;
}
```

Notice the pattern: **select** (filter by plays) + **transform**
(extract title). Most integrated FRQs are two or three patterns
glued together — recognizing the glue is the skill.
"""

L2 = r"""
**State machines over objects** — the second integrated pattern: an
object's methods change its state, and later calls *read* that state.

```java
public static class Register {
    private int cents;

    public Register() { cents = 0; }

    public void add(int c) { cents += c; }

    public boolean spend(int c) {
        if (c > cents) { return false; }
        cents -= c;
        return true;
    }

    public int balance() { return cents; }
}
```

Trace questions ask: after this SEQUENCE of calls, what is the state?
The discipline is literal — a two-column trace table, one row per
call, updating every field. Sequence matters: `spend(500)` before any
`add` fails; after enough adds it succeeds. Method order is content.

The exam's object-tracing items ("What is the value of...") are all
this pattern with different nouns. Trace, don't guess.
"""

L3 = r"""
**Mixed collections and arrays** — the exam loves asking for both in
one method:

```java
// array in, list out
public static ArrayList<Integer> positives(int[] a) {
    ArrayList<Integer> out = new ArrayList<Integer>();
    for (int x : a) {
        if (x > 0) {
            out.add(x);
        }
    }
    return out;
}
```

Four conversion facts that decide correctness:

- `int[]` and `ArrayList<Integer>` are different types; neither
  auto-converts. Box manually (`out.add(x)` boxes the int).
- `list.remove(Integer.valueOf(5))` removes the VALUE 5;
  `list.remove(5)` removes INDEX 5. The exam tests this distinction.
- Removing while iterating forward **skips** the element after the
  removed one — iterate backwards or use an index-corrected loop.
- `a.length` vs `list.size()` — one is a field, one is a method.

When a spec says "return a new list", never mutate the input.
"""

write_module(
    M,
    "Integrated Problems",
    "Mixed-unit synthesis: select-transform pipelines, object state machines, and array-list conversion traps.",
    "Bài toán tích hợp",
    "Tổng hợp đa chủ đề: chuỗi chọn-biến đổi, máy trạng thái đối tượng, và bẫy chuyển đổi mảng-danh sách.",
    lessons=["apc-m19-pipeline", "apc-m19-statemachine", "apc-m19-mixed", "apc-cp-m19"],
    practices=["apc-p19-integration"],
)

write_lesson(
    M, "apc-m19-pipeline", "Select-transform pipelines",
    "Inventory, decompose, contract, assemble — patterns glued together.",
    12, L1,
    "Chuỗi chọn-biến đổi",
    "Kiểm kê, tách nhỏ, hợp đồng, lắp ráp — các mẫu hình ghép lại với nhau.",
    r"""
Bài tích hợp kết hợp các chủ đề đúng như kỳ thi. Một câu hỏi có thể
đòi: một `ArrayList` chứa đối tượng, một phép duyệt, một phương thức
String, và một hợp đồng boolean. Chiến lược:

1. **Kiểm kê** — liệt kê các kiểu đang có mặt (`ArrayList<Song>`,
   `int`, `boolean`). Mỗi kiểu gọi tên một bộ công cụ từ module trước.
2. **Tách nhỏ** — mỗi việc con một phương thức. "Tìm cái tốt nhất" và
   "in báo cáo" là hai phương thức, không phải một vòng lặp rối.
3. **Hợp đồng cho mỗi phương thức** — một câu: đầu vào gì, đầu ra gì,
   bảo đảm gì.
4. **Lắp ráp** — phương thức điều phối gọi các mảnh theo thứ tự.

```java
// Các mảnh: findBest(list), countBelow(list, cut)
public static ArrayList<String> topNames(ArrayList<Song> list, int cut) {
    ArrayList<String> names = new ArrayList<String>();
    for (Song s : list) {
        if (s.getPlays() >= cut) {
            names.add(s.getTitle());
        }
    }
    return names;
}
```

Chú ý mẫu hình: **chọn** (lọc theo plays) + **biến đổi** (rút ra
title). Đa số FRQ tích hợp là hai hoặc ba mẫu hình dán với nhau —
nhận ra lớp keo là kỹ năng then chốt.
""",
)

write_lesson(
    M, "apc-m19-statemachine", "Object state machines",
    "Methods mutate state; later calls read it. Trace tables, one row per call.",
    12, L2,
    "Máy trạng thái đối tượng",
    "Phương thức thay đổi trạng thái; lời gọi sau đọc trạng thái đó. Bảng truy vết, mỗi lời gọi một hàng.",
    r"""
**Máy trạng thái trên đối tượng** — mẫu hình tích hợp thứ hai: các
phương thức của đối tượng thay đổi trạng thái, và các lời gọi sau
*đọc* trạng thái đó.

```java
public static class Register {
    private int cents;

    public Register() { cents = 0; }

    public void add(int c) { cents += c; }

    public boolean spend(int c) {
        if (c > cents) { return false; }
        cents -= c;
        return true;
    }

    public int balance() { return cents; }
}
```

Câu truy vết hỏi: sau CHUỖI lời gọi này, trạng thái là gì? Kỷ luật
là nghĩa chữ — bảng truy vết hai cột, mỗi lời gọi một hàng, cập nhật
mọi trường. Thứ tự có ý nghĩa: `spend(500)` trước bất kỳ `add` nào
sẽ thất bại; sau đủ lần add thì thành công. Thứ tự phương thức là
nội dung.

Các câu truy vết đối tượng của đề ("Giá trị của... là gì") đều là
mẫu hình này với danh từ khác nhau. Truy vết, đừng đoán.
""",
)

write_lesson(
    M, "apc-m19-mixed", "Mixed arrays and lists",
    "Conversions, boxing, remove-by-value vs remove-by-index, mutation discipline.",
    12, L3,
    "Mảng và danh sách trộn lẫn",
    "Chuyển đổi, boxing, remove-theo-giá-trị so với remove-theo-chỉ-số, kỷ luật biến đổi.",
    r"""
**Bộ sưu tập và mảng trộn lẫn** — đề rất thích yêu cầu cả hai trong
một phương thức:

```java
// mảng vào, danh sách ra
public static ArrayList<Integer> positives(int[] a) {
    ArrayList<Integer> out = new ArrayList<Integer>();
    for (int x : a) {
        if (x > 0) {
            out.add(x);
        }
    }
    return out;
}
```

Bốn sự thật chuyển đổi quyết định tính đúng:

- `int[]` và `ArrayList<Integer>` là hai kiểu khác nhau; không kiểu
  nào tự chuyển thành kiểu kia. Box thủ công (`out.add(x)` box int).
- `list.remove(Integer.valueOf(5))` xóa GIÁ TRỊ 5;
  `list.remove(5)` xóa CHỈ SỐ 5. Đề kiểm tra đúng sự phân biệt này.
- Xóa trong khi duyệt tới sẽ **bỏ sót** phần tử ngay sau phần tử bị
  xóa — duyệt ngược hoặc dùng vòng có chỉnh chỉ số.
- `a.length` so với `list.size()` — một cái là trường, một cái là
  phương thức.

Khi đặc tả nói "trả về danh sách mới", đừng bao giờ biến đổi đầu vào.
""",
)

BOILER_TOP = r"""import java.util.*;

public class Solution {
    public static class Song {
        private String title;
        private int plays;

        public Song(String title, int plays) {
            this.title = title;
            this.plays = plays;
        }

        public String getTitle() {
            return title;
        }

        public int getPlays() {
            return plays;
        }
    }

    // Postcondition: returns the titles of all songs with plays
    // >= cut, in the same order as the input list
    public static ArrayList<String> topNames(ArrayList<Song> list, int cut) {
        // complete
        return new java.util.ArrayList<String>();
    }
}
"""

BOILER_REG = r"""import java.util.*;

public class Solution {
    public static class Register {
        private int cents;

        public Register() {
            cents = 0;
        }

        public void add(int c) {
            cents += c;
        }

        // Postcondition: subtracts c if affordable and returns true;
        // otherwise leaves state unchanged and returns false
        public boolean spend(int c) {
            // complete
            return false;
        }

        public int balance() {
            return cents;
        }
    }
}
"""

BOILER_POS = r"""import java.util.*;

public class Solution {
    // Postcondition: returns a NEW list of the positive values of a,
    // in order; a must not be modified
    public static ArrayList<Integer> positives(int[] a) {
        // complete
        return new ArrayList<Integer>();
    }
}
"""

BOILER_FIXDROP = r"""import java.util.*;

public class Solution {
    // Postcondition: removes every occurrence of value from list
    public static void removeAll(ArrayList<Integer> list, int value) {
        // BUG: original flaw kept — forward removal skips the element
        // after each removed one
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).intValue() == value) {
                list.remove(i);
            }
        }
    }
}
"""

CP19 = r"""import java.util.*;

public class Solution {
    public static class Log {
        private int total;
        private int count;

        public Log() {
            total = 0;
            count = 0;
        }

        // Postcondition: records one reading
        public void record(int reading) {
            // complete
        }

        // Postcondition: average of recorded readings, or 0 if none
        public int average() {
            // complete
            return 0;
        }

        public int getCount() {
            return count;
        }
    }
}
"""

P_TOP = challenge(
    "apc-m19-topnames",
    "Select and transform",
    "Implement `topNames` to spec: titles of all songs with plays >= cut, input order preserved. Use the Song accessors.",
    BOILER_TOP,
    [(
        "order preserved",
        r"""
java.util.ArrayList<Solution.Song> list = new java.util.ArrayList<Solution.Song>();
list.add(new Solution.Song("b", 50));
list.add(new Solution.Song("a", 150));
list.add(new Solution.Song("c", 100));
CjTestBase.checkEq(Solution.topNames(list, 100), java.util.List.of("a", "c"), "two pass the cut");
CjTestBase.checkEq(Solution.topNames(list, 500), java.util.List.of(), "none pass");
""",
        "loop the list, test s.getPlays() >= cut, add s.getTitle().",
    )],
    level="guided",
)

P_REG = challenge(
    "apc-m19-register",
    "State machine: the register",
    "Implement `Register.spend(int c)` to spec: if c fits in the balance, subtract it and return true; otherwise change nothing and return false.",
    BOILER_REG,
    [(
        "sequence trace",
        r"""
Solution.Register r = new Solution.Register();
CjTestBase.checkEq(r.spend(100), false, "empty register refuses");
r.add(250);
CjTestBase.checkEq(r.spend(100), true, "affordable now");
CjTestBase.checkEq(r.balance(), 150, "balance updated");
CjTestBase.checkEq(r.spend(200), false, "overdraw refused");
CjTestBase.checkEq(r.balance(), 150, "state unchanged on refusal");
""",
        "guard first: if (c > cents) return false; then subtract.",
    )],
    level="independent",
)

P_POS = challenge(
    "apc-m19-positives",
    "Array to list",
    "Implement `positives(int[] a)`: return a NEW `ArrayList<Integer>` holding the positive values of a, in order. The input array must not be modified.",
    BOILER_POS,
    [(
        "new list, no mutation",
        r"""
int[] a = {1, -2, 3, 0, 5};
CjTestBase.checkEq(Solution.positives(a), java.util.List.of(1, 3, 5), "positives only, in order");
CjTestBase.checkEq(a.length, 5, "input untouched");
CjTestBase.checkEq(Solution.positives(new int[] {-1, -2}), java.util.List.of(), "none positive");
""",
        "the enhanced-for over int[] boxes each x automatically on add.",
    )],
    level="imitation",
)

P_FIXDROP = challenge(
    "apc-m19-fix-removeall",
    "Debug: the skipping remover",
    "`removeAll(list, value)` should remove EVERY occurrence of value, but the forward loop skips the element right after each removal (\"aab\" removing 'a' leaves one 'a'). Fix it — the signature stays.",
    BOILER_FIXDROP,
    [(
        "no skips",
        r"""
java.util.ArrayList<Integer> list = new java.util.ArrayList<Integer>();
list.add(3); list.add(3); list.add(7); list.add(3); list.add(3);
Solution.removeAll(list, 3);
CjTestBase.checkEq(list, java.util.List.of(7), "all 3s gone, 7 stays");
java.util.ArrayList<Integer> none = new java.util.ArrayList<Integer>();
none.add(1);
Solution.removeAll(none, 9);
CjTestBase.checkEq(none, java.util.List.of(1), "no-op keeps list");
""",
        "iterate BACKWARDS (from size()-1 down to 0), or don't advance i after a removal.",
    )],
    level="debugging",
)

CP19C = challenge(
    "apc-cp-m19-log",
    "Checkpoint: the reading log",
    "Complete the Log class: `record(int reading)` stores one reading; `average()` returns the average of all recorded readings (integer division), or 0 when nothing was recorded. `getCount()` is provided.",
    CP19,
    [(
        "empty and average",
        r"""
Solution.Log log = new Solution.Log();
CjTestBase.checkEq(log.average(), 0, "empty log, zero average");
log.record(10); log.record(20); log.record(30);
CjTestBase.checkEq(log.average(), 20, "mean of three");
CjTestBase.checkEq(log.getCount(), 3, "count tracked");
log.record(5);
CjTestBase.checkEq(log.average(), 16, "mean truncates");
""",
        "total += reading; count++; then total / count guarded by count == 0.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p19-integration", "Integrated reps", "Pipelines, registers, conversions, skipping removals, aggregation state.",
    "Luyện tích hợp", "Chuỗi xử lý, máy tính tiền, chuyển đổi, xóa bỏ sót, trạng thái tổng hợp.",
    after_lesson="apc-m19-mixed", minutes=55, difficulty="beginner",
    challenges=[P_TOP, P_REG, P_POS, P_FIXDROP],
    vi_challenges={
        "apc-m19-topnames": vi_challenge("Chọn và biến đổi", "Cài đặt `topNames` theo đặc tả: các title của mọi bài hát có plays >= cut, giữ nguyên thứ tự đầu vào. Dùng accessor của Song.",
            [("order preserved", "duyệt list, kiểm s.getPlays() >= cut, thêm s.getTitle().")]),
        "apc-m19-register": vi_challenge("Máy trạng thái: máy tính tiền", "Cài đặt `Register.spend(int c)` theo đặc tả: nếu c vừa với số dư thì trừ và trả true; nếu không thì không đổi gì và trả false.",
            [("sequence trace", "chặn trước: if (c > cents) return false; rồi trừ.")]),
        "apc-m19-positives": vi_challenge("Mảng sang danh sách", "Cài đặt `positives(int[] a)`: trả `ArrayList<Integer>` MỚI chứa các giá trị dương của a, theo thứ tự. Mảng đầu vào không được bị thay đổi.",
            [("new list, no mutation", "enhanced-for trên int[] tự box mỗi x khi add.")]),
        "apc-m19-fix-removeall": vi_challenge("Gỡ lỗi: bộ xóa bị bỏ sót", "`removeAll(list, value)` phải xóa MỌI lần xuất hiện của value, nhưng vòng duyệt tới bỏ sót phần tử ngay sau mỗi lần xóa (\"aab\" xóa 'a' còn lại một 'a'). Sửa lại — chữ ký giữ nguyên.",
            [("no skips", "duyet NGƯỢC (từ size()-1 về 0), hoặc không tăng i sau mỗi lần xóa.")]),
    },
    solutions=[
        ("apc-m19-topnames", r"""import java.util.*;

public class Solution {
    public static class Song {
        private String title;
        private int plays;

        public Song(String title, int plays) {
            this.title = title;
            this.plays = plays;
        }

        public String getTitle() {
            return title;
        }

        public int getPlays() {
            return plays;
        }
    }

    public static ArrayList<String> topNames(ArrayList<Song> list, int cut) {
        ArrayList<String> names = new ArrayList<String>();
        for (Song s : list) {
            if (s.getPlays() >= cut) {
                names.add(s.getTitle());
            }
        }
        return names;
    }
}
""", r"""import java.util.*;

public class Solution {
    public static class Song {
        private String title;
        private int plays;

        public Song(String title, int plays) {
            this.title = title;
            this.plays = plays;
        }

        public String getTitle() {
            return title;
        }

        public int getPlays() {
            return plays;
        }
    }

    public static ArrayList<String> topNames(ArrayList<Song> list, int cut) {
        // BUG: adds the whole Song object instead of the title — type
        // mismatch with the ArrayList<String> contract
        ArrayList<String> names = new ArrayList<String>();
        for (Song s : list) {
            if (s.getPlays() >= cut) {
                names.add(s.getTitle().toUpperCase());
            }
        }
        return names;
    }
}
"""),
        ("apc-m19-register", r"""import java.util.*;

public class Solution {
    public static class Register {
        private int cents;

        public Register() {
            cents = 0;
        }

        public void add(int c) {
            cents += c;
        }

        public boolean spend(int c) {
            if (c > cents) {
                return false;
            }
            cents -= c;
            return true;
        }

        public int balance() {
            return cents;
        }
    }
}
""", r"""import java.util.*;

public class Solution {
    public static class Register {
        private int cents;

        public Register() {
            cents = 0;
        }

        public void add(int c) {
            cents += c;
        }

        public boolean spend(int c) {
            // BUG: subtracts unconditionally — the empty register
            // goes negative and wrongly reports success
            cents -= c;
            return true;
        }

        public int balance() {
            return cents;
        }
    }
}
"""),
        ("apc-m19-positives", r"""import java.util.*;

public class Solution {
    public static ArrayList<Integer> positives(int[] a) {
        ArrayList<Integer> out = new ArrayList<Integer>();
        for (int x : a) {
            if (x > 0) {
                out.add(x);
            }
        }
        return out;
    }
}
""", r"""import java.util.*;

public class Solution {
    public static ArrayList<Integer> positives(int[] a) {
        // BUG: uses >= 0 so zero sneaks into the "positives" list
        ArrayList<Integer> out = new ArrayList<Integer>();
        for (int x : a) {
            if (x >= 0) {
                out.add(x);
            }
        }
        return out;
    }
}
"""),
        ("apc-m19-fix-removeall", r"""import java.util.*;

public class Solution {
    public static void removeAll(ArrayList<Integer> list, int value) {
        for (int i = list.size() - 1; i >= 0; i--) {
            if (list.get(i).intValue() == value) {
                list.remove(i);
            }
        }
    }
}
""", r"""import java.util.*;

public class Solution {
    public static void removeAll(ArrayList<Integer> list, int value) {
        // BUG: original flaw kept — forward removal skips the element
        // after each removed one
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).intValue() == value) {
                list.remove(i);
            }
        }
    }
}
"""),
        ("apc-cp-m19-log", r"""import java.util.*;

public class Solution {
    public static class Log {
        private int total;
        private int count;

        public Log() {
            total = 0;
            count = 0;
        }

        public void record(int reading) {
            total += reading;
            count++;
        }

        public int average() {
            if (count == 0) {
                return 0;
            }
            return total / count;
        }

        public int getCount() {
            return count;
        }
    }
}
""", r"""import java.util.*;

public class Solution {
    public static class Log {
        private int total;
        private int count;

        public Log() {
            total = 0;
            count = 0;
        }

        public void record(int reading) {
            total += reading;
            count++;
        }

        public int average() {
            // BUG: no empty-log guard — divides by zero count
            return total / count;
        }

        public int getCount() {
            return count;
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m19", "Checkpoint: the reading log",
    "Object state + aggregation + the empty-input guard, in one class.",
    25,
    r"""
The pattern: a tiny class that accumulates state (`total`, `count`)
and serves a derived statistic. Two contracts tested: the empty case
MUST return 0, not crash, and the average truncates (integer
division). "What is the state after this sequence?" is answered by
your own trace table — build it, then code it.
""",
    "Điểm kiểm tra: nhật ký số đo",
    "Trạng thái đối tượng + tổng hợp + chặn đầu vào rỗng, trong một lớp.",
    r"""
Mẫu hình: một lớp nhỏ tích lũy trạng thái (`total`, `count`) và cung
cấp một thống kê suy ra. Hai hợp đồng được kiểm: trường hợp rỗng
PHẢI trả 0, không được crash, và trung bình làm tròn xuống (chia
nguyên). "Trạng thái sau chuỗi lời gọi này là gì?" được trả lời bằng
chính bảng truy vết của bạn — dựng bảng, rồi mới code.
""",
    CP19C,
    vi_challenge("Điểm kiểm tra: nhật ký số đo", "Hoàn thiện lớp Log: `record(int reading)` lưu một số đo; `average()` trả trung bình của các số đo đã lưu (chia nguyên), hoặc 0 khi chưa có gì. `getCount()` được cung cấp.",
        [("empty and average", "total += reading; count++; rồi total / count có chặn count == 0.")]),
    solution=r"""import java.util.*;

public class Solution {
    public static class Log {
        private int total;
        private int count;

        public Log() {
            total = 0;
            count = 0;
        }

        public void record(int reading) {
            total += reading;
            count++;
        }

        public int average() {
            if (count == 0) {
                return 0;
            }
            return total / count;
        }

        public int getCount() {
            return count;
        }
    }
}
""",
    wrong=r"""import java.util.*;

public class Solution {
    public static class Log {
        private int total;
        private int count;

        public Log() {
            total = 0;
            count = 0;
        }

        public void record(int reading) {
            total += reading;
            count++;
        }

        public int average() {
            // BUG: no empty-log guard — divides by zero count
            return total / count;
        }

        public int getCount() {
            return count;
        }
    }
}
""",
)
