#!/usr/bin/env python3
"""AP CSA Core M7 — ArrayList Mastery (removal discipline + object lists)."""
from apcc import *

M = "cx-arraylist"

L1 = r"""
ArrayList is where the exam harvests points. Two API facts separate
calm students from panicked ones:

**remove(int) vs remove(Integer).** `list.remove(2)` removes the element
AT INDEX 2. To remove the *value* 2 from an `ArrayList<Integer>`, write
`list.remove(Integer.valueOf(2))`. When a list holds {10, 20, 30},
`remove(1)` leaves {10, 30} — it did not remove the value 1 (which was
never there).

**Index invalidation.** Every removal shifts all later elements left by
one. `size()` changes the moment remove fires. The classic broken loop:

```java
for (int i = 0; i < list.size(); i++) {
    if (list.get(i).equals(target)) {
        list.remove(i);     // shifts left; next element is now at i
    }
}
```

With {\"a\", \"a\", \"b\"} and target \"a\": i=0 removes, list is {\"a\",
\"b\"}; i=1 checks \"b\" — the SECOND \"a\" at index 1 was skipped
entirely. Consecutive matches are the case that exposes this.

**Forward-with-fix** (re-decrement i): correct but subtle.
**Backward removal** — the exam's preferred clean solution:

```java
for (int i = list.size() - 1; i >= 0; i--) {
    if (list.get(i).equals(target)) {
        list.remove(i);
    }
}
```

Removing at i only shifts elements *after* i — and you have already
visited all of them. Safe, no index gymnastics.
"""

L2 = r"""
ArrayLists hold objects, so `ArrayList<Integer>` stores Integer boxes —
and arithmetic quietly unboxes them:

```java
ArrayList<Integer> nums = new ArrayList<Integer>();
nums.add(7);
int x = nums.get(0) + 1;          // unboxes to int, x = 8
Integer boxed = nums.get(0);
if (boxed == 7) { ... }           // true: unboxing comparison
if (nums.get(0) == new Integer(7)) { ... }  // int comparison, true
```

But between two Integers, `==` compares references:

```java
Integer a = 200, b = 200;
if (a == b) { }          // false outside the small-value cache!
if (a.equals(b)) { }     // true — always compare objects with equals
```

(The small-value cache makes `-128..127` sometimes compare equal with
`==` — a trap that only *looks* reliable in tests.)

The exam's ArrayList FRQ always wraps a real class:

```java
ArrayList<Member> roster = new ArrayList<Member>();
for (Member m : roster) {
    if (m.getPoints() >= threshold) { count++; }
}
```

For-each is perfect for reading; the moment you must **remove**,
switch to an indexed loop. And the length-vs-size discipline:
arrays use `.length` (no parens), Strings use `.length()`,
ArrayLists use `.size()`.
"""

L3 = r"""
The merge pattern — ArrayList's most exam-typical synthesis task:

*"Merge two sorted lists into one sorted result (duplicates allowed)."*

```java
public static ArrayList<Integer> merge(ArrayList<Integer> a, ArrayList<Integer> b) {
    ArrayList<Integer> out = new ArrayList<Integer>();
    int i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        if (a.get(i) <= b.get(j)) { out.add(a.get(i)); i++; }
        else { out.add(b.get(j)); j++; }
    }
    while (i < a.size()) { out.add(a.get(i)); i++; }
    while (j < b.size()) { out.add(b.get(j)); j++; }
    return out;
}
```

Reading it as machines: a two-pointer comparison while both lists have
material, then two "drain the remainder" sentinel loops. The `<=`
matters for stability — with `<=`, ties take from `a` first; a student
writing `<` is still correct here, but in exam variants asking for
stable merge of records, that one character is the difference.

Second synthesis: **positional operations**. *"Swap the halves of list
in place"* or *"insert value after every even element"* (backward insert
loop! insertion shifts right just like removal shifts left). Whenever
an ArrayList problem mutates, ask: forward or backward? Removal from
the front region, insertion, and anything touching consecutive
elements → backward. Pure reading or end-appending → forward is fine.
"""

write_module(
    M,
    "ArrayList Mastery",
    "Removal discipline (backward loops, index invalidation), Integer boxing traps, and object collections — plus merge synthesis.",
    "Làm chủ ArrayList",
    "Kỷ luật xóa (vòng lặp ngược, vô hiệu hóa chỉ số), bẫy boxing Integer, và bộ sưu tập đối tượng — kèm bài tổng hợp merge.",
    lessons=["cx-m7-removal", "cx-m7-boxing", "cx-m7-synthesis", "cx-cp-m7"],
    practices=["cx-p7-arraylist"],
)

write_lesson(
    M, "cx-m7-removal", "Removal discipline",
    "remove(int) vs remove(Integer), index invalidation, backward removal.",
    12, L1,
    "Kỷ luật xóa phần tử",
    "remove(int) với remove(Integer), vô hiệu hóa chỉ số, xóa bằng vòng ngược.",
    r"""
ArrayList là nơi đề thi gặt điểm. Hai sự thật API tách học sinh bình tĩnh
khỏi học sinh hoảng loạn:

**remove(int) với remove(Integer).** `list.remove(2)` xóa phần tử TẠI
CHỈ SỐ 2. Để xóa *giá trị* 2 khỏi một `ArrayList<Integer>`, hãy viết
`list.remove(Integer.valueOf(2))`. Khi danh sách chứa {10, 20, 30},
`remove(1)` còn lại {10, 30} — nó không hề xóa giá trị 1 (mà chưa từng có
trong danh sách).

**Vô hiệu hóa chỉ số.** Mỗi lần xóa dịch toàn bộ phần tử phía sau sang
trái một bước. `size()` đổi ngay khi remove nổ ra. Vòng lặp gãy kinh
điển:

```java
for (int i = 0; i < list.size(); i++) {
    if (list.get(i).equals(target)) {
        list.remove(i);     // dịch trái; phần tử kế giờ nằm ở i
    }
}
```

Với {\"a\", \"a\", \"b\"} và target \"a\": i=0 xóa, danh sách còn {\"a\",
\"b\"}; i=1 kiểm tra \"b\" — chữ \"a\" THỨ HAI tại chỉ số 1 bị bỏ qua hoàn
toàn. Các lần khớp liền kề chính là trường hợp phơi bày lỗi này.

**Sửa-xuôi** (hạ i xuống lại): đúng nhưng tinh vi. **Xóa bằng vòng
ngược** — lời giải sạch được đề thi ưa chuộng:

```java
for (int i = list.size() - 1; i >= 0; i--) {
    if (list.get(i).equals(target)) {
        list.remove(i);
    }
}
```

Xóa tại i chỉ dịch các phần tử *sau* i — và bạn đã ghé thăm hết chúng rồi.
An toàn, không cần nhào lộn chỉ số.
""",
)

write_lesson(
    M, "cx-m7-boxing", "Integers in lists",
    "Autoboxing, == vs equals between Integers, and object collections.",
    12, L2,
    "Integer trong danh sách",
    "Autoboxing, == với equals giữa các Integer, và bộ sưu tập đối tượng.",
    r"""
ArrayList chứa đối tượng, nên `ArrayList<Integer>` cất các hộp Integer —
và phép toán số học lặng lẽ mở hộp:

```java
ArrayList<Integer> nums = new ArrayList<Integer>();
nums.add(7);
int x = nums.get(0) + 1;          // mở hộp thành int, x = 8
Integer boxed = nums.get(0);
if (boxed == 7) { ... }           // true: so sánh sau khi mở hộp
if (nums.get(0) == new Integer(7)) { ... }  // so sánh int, true
```

Nhưng giữa hai Integer với nhau, `==` so tham chiếu:

```java
Integer a = 200, b = 200;
if (a == b) { }          // false ngoài vùng đệm giá trị nhỏ!
if (a.equals(b)) { }     // true — luôn so đối tượng bằng equals
```

(Vùng đệm giá trị nhỏ khiến `-128..127` đôi khi so bằng được với `==` —
một cái bẫy chỉ *trông* đáng tin trong bài kiểm tra.)

FRQ ArrayList của đề thi luôn bọc một lớp thật:

```java
ArrayList<Member> roster = new ArrayList<Member>();
for (Member m : roster) {
    if (m.getPoints() >= threshold) { count++; }
}
```

For-each hoàn hảo để đọc; khoảnh khắc bạn phải **xóa**, hãy chuyển sang
vòng lặp có chỉ số. Và kỷ luật length-vs-size: mảng dùng `.length`
(không ngoặc), String dùng `.length()`, ArrayList dùng `.size()`.
""",
)

write_lesson(
    M, "cx-m7-synthesis", "Synthesis: merge and mutate",
    "Two-pointer merge with remainder drains; when to traverse backward.",
    12, L3,
    "Tổng hợp: merge và biến đổi",
    "Merge hai con trỏ với các vòng rút phần còn lại; khi nào phải duyệt ngược.",
    r"""
Mẫu merge — nhiệm vụ tổng hợp điển hình nhất của ArrayList:

*"Gộp hai danh sách đã sắp xếp thành một kết quả đã sắp xếp (cho phép
trùng)."*

```java
public static ArrayList<Integer> merge(ArrayList<Integer> a, ArrayList<Integer> b) {
    ArrayList<Integer> out = new ArrayList<Integer>();
    int i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        if (a.get(i) <= b.get(j)) { out.add(a.get(i)); i++; }
        else { out.add(b.get(j)); j++; }
    }
    while (i < a.size()) { out.add(a.get(i)); i++; }
    while (j < b.size()) { out.add(b.get(j)); j++; }
    return out;
}
```

Đọc theo cỗ máy: so sánh hai con trỏ khi cả hai danh sách còn nguyên liệu,
rồi hai vòng lính canh \"rút phần còn lại\". Dấu `<=` quan trọng cho tính
ổn định — với `<=`, đồng giá lấy từ `a` trước; người viết `<` vẫn đúng ở
đây, nhưng trong biến thể đề thi yêu cầu merge ổn định cho bản ghi, một
ký tự đó là ranh giới.

Tổng hợp thứ hai: **thao tác theo vị trí**. *\"Đổi chỗ hai nửa của danh
sách tại chỗ\"* hoặc *\"chèn giá trị sau mỗi phần tử chẵn\"* (vòng chèn
ngược!). Chèn dịch phải y như xóa dịch trái. Mỗi khi bài ArrayList biến
đổi danh sách, hãy hỏi: xuôi hay ngược? Xóa vùng đầu, chèn, và bất cứ
thứ gì chạm vào phần tử liền kề → ngược. Thuần đọc hoặc nối vào đuôi →
xuôi là đủ.
""",
)

BOILER_EVEN_REM = r"""import java.util.ArrayList;

public class Solution {
    // CONTRACT: remove every EVEN number from nums, in place.
    // [3, 4, 6, 7, 6] -> [3, 7]
    public static void removeEvens(ArrayList<Integer> nums) {
        // replace (backward loop)
    }
}
"""

BOILER_VALUE_REM = r"""import java.util.ArrayList;

public class Solution {
    // CONTRACT: remove the first element EQUAL TO value (by content).
    // Return true when something was removed.
    public static boolean removeFirst(ArrayList<String> list, String value) {
        return false; // replace
    }
}
"""

BOILER_INSERT_AFTERS = r"""import java.util.ArrayList;

public class Solution {
    // CONTRACT: insert 0 immediately after every even element.
    // [2, 3, 4] -> [2, 0, 3, 4, 0]
    public static void insertAfterEvens(ArrayList<Integer> nums) {
        // replace
    }
}
"""

BOILER_SWAPHALVES = r"""import java.util.ArrayList;

public class Solution {
    // CONTRACT: swap the two halves of list IN PLACE. Odd lengths:
    // the middle element belongs to the SECOND half.
    // [1, 2, 3, 4, 5] -> [3, 4, 5, 1, 2]
    public static void swapHalves(ArrayList<Integer> list) {
        // replace
    }
}
"""

BOILER_TOTALPT = r"""import java.util.ArrayList;

public class Solution {
    public static class Member {
        private String name;
        private int points;
        public Member(String n, int p) { name = n; points = p; }
        public String getName() { return name; }
        public int getPoints() { return points; }
    }

    // CONTRACT: total points of members whose name starts with letter;
    // 0 when nobody matches.
    public static int rosterPoints(ArrayList<Member> roster, char letter) {
        return 0; // replace
    }
}
"""

BOILER_CP_AL = r"""import java.util.ArrayList;

public class Solution {
    // CONTRACT: merge two sorted lists into a new sorted list
    // (duplicates allowed, ties take from a first).
    public static ArrayList<Integer> merge(ArrayList<Integer> a, ArrayList<Integer> b) {
        return new ArrayList<Integer>(); // replace
    }
}
"""

P_EVENS = challenge(
    "cx-m7-remove-evens",
    "Backward removal",
    "Implement `void removeEvens(ArrayList<Integer> nums)`: remove every even number in place. The backward loop is the intended discipline — a forward loop will fail on consecutive evens like [4, 6].",
    BOILER_EVEN_REM,
    [(
        "evens removed",
        r"""
ArrayList<Integer> a = new ArrayList<Integer>();
a.add(3); a.add(4); a.add(6); a.add(7); a.add(6);
Solution.removeEvens(a);
CjTestBase.checkEq(a, List.of(3, 7), "consecutive evens all removed");
ArrayList<Integer> b = new ArrayList<Integer>();
b.add(1); b.add(2);
Solution.removeEvens(b);
CjTestBase.checkEq(b, List.of(1), "pair case");
ArrayList<Integer> c = new ArrayList<Integer>();
Solution.removeEvens(c);
CjTestBase.checkEq(c, List.of(), "empty list");
""",
        "for (int i = nums.size() - 1; i >= 0; i--) if (nums.get(i) % 2 == 0) nums.remove(i);",
    )],
    level="guided",
)

P_VALUEREM = challenge(
    "cx-m7-remove-first-value",
    "Value removal with report",
    "Implement `boolean removeFirst(ArrayList<String> list, String value)`: remove the FIRST element equal (by content) to value; return whether anything was removed. Missing value → false, list untouched.",
    BOILER_VALUE_REM,
    [(
        "first match removed",
        r"""
ArrayList<String> a = new ArrayList<String>();
a.add("x"); a.add("y"); a.add("x");
CjTestBase.checkEq(Solution.removeFirst(a, "x"), true, "found");
CjTestBase.checkEq(a, List.of("y", "x"), "only the FIRST x is gone");
ArrayList<String> b = new ArrayList<String>();
b.add("q");
CjTestBase.checkEq(Solution.removeFirst(b, "z"), false, "absent value");
CjTestBase.checkEq(b, List.of("q"), "untouched");
""",
        "indexOf gives the first match; -1 means absent. remove(index) or remove(Object).",
    )],
    level="independent",
)

P_INSERT = challenge(
    "cx-m7-insert-after-evens",
    "Backward insertion",
    "Implement `void insertAfterEvens(ArrayList<Integer> nums)`: insert 0 immediately after every even element. Insertions shift right — a forward loop re-processes its own insertions forever. [2, 3, 4] → [2, 0, 3, 4, 0].",
    BOILER_INSERT_AFTERS,
    [(
        "zeros inserted",
        r"""
ArrayList<Integer> a = new ArrayList<Integer>();
a.add(2); a.add(3); a.add(4);
Solution.insertAfterEvens(a);
CjTestBase.checkEq(a, List.of(2, 0, 3, 4, 0), "after 2 and after 4");
ArrayList<Integer> b = new ArrayList<Integer>();
b.add(1);
Solution.insertAfterEvens(b);
CjTestBase.checkEq(b, List.of(1), "no evens, no inserts");
""",
        "Backward: for i from size-1 down to 0, if get(i) even, add(i + 1, 0).",
    )],
    level="combination",
)

P_SWAP = challenge(
    "cx-m7-swap-halves",
    "Halves swap",
    "Implement `void swapHalves(ArrayList<Integer> list)`: swap the halves in place. For odd sizes the middle element belongs to the SECOND half: [1, 2, 3, 4, 5] → [3, 4, 5, 1, 2]. Work the index mapping on paper for sizes 4 and 5 before coding.",
    BOILER_SWAPHALVES,
    [(
        "halves swapped",
        r"""
ArrayList<Integer> a = new ArrayList<Integer>();
a.add(1); a.add(2); a.add(3); a.add(4); a.add(5);
Solution.swapHalves(a);
CjTestBase.checkEq(a, List.of(3, 4, 5, 1, 2), "odd size mapping");
ArrayList<Integer> b = new ArrayList<Integer>();
b.add(1); b.add(2); b.add(3); b.add(4);
Solution.swapHalves(b);
CjTestBase.checkEq(b, List.of(3, 4, 1, 2), "even size mapping");
ArrayList<Integer> c = new ArrayList<Integer>();
c.add(9);
Solution.swapHalves(c);
CjTestBase.checkEq(c, List.of(9), "single element");
""",
        "half = size / 2; new position of index i is (i + half) % size.",
    )],
    level="real-world",
)

P_ROSTER = challenge(
    "cx-m7-roster-points",
    "Object collection",
    "Implement `int rosterPoints(ArrayList<Member> roster, char letter)`: total points of members whose name starts with `letter` (case-sensitive), 0 when nobody matches. For-each over objects; guard the empty-name case.",
    BOILER_TOTALPT,
    [(
        "filtered total",
        r"""
ArrayList<Solution.Member> roster = new ArrayList<Solution.Member>();
roster.add(new Solution.Member("An", 10));
roster.add(new Solution.Member("Binh", 5));
roster.add(new Solution.Member("Anh", 2));
CjTestBase.checkEq(Solution.rosterPoints(roster, 'A'), 12, "An + Anh");
CjTestBase.checkEq(Solution.rosterPoints(roster, 'Z'), 0, "nobody matches");
CjTestBase.checkEq(Solution.rosterPoints(new ArrayList<Solution.Member>(), 'A'), 0, "empty roster");
""",
        "char c = m.getName().charAt(0); needs getName().length() > 0 first.",
    )],
    level="combination",
)

CP7 = challenge(
    "cx-cp-m7-merge",
    "Checkpoint: sorted merge",
    "Implement `ArrayList<Integer> merge(ArrayList<Integer> a, ArrayList<Integer> b)`: merge two sorted lists into a new sorted list, duplicates allowed, ties taking from `a` first. The lesson's three-loop structure maps directly — write it from the machines, not from memory.",
    BOILER_CP_AL,
    [(
        "merged in order",
        r"""
ArrayList<Integer> a = new ArrayList<Integer>();
a.add(1); a.add(3); a.add(5);
ArrayList<Integer> b = new ArrayList<Integer>();
b.add(2); b.add(3); b.add(6);
CjTestBase.checkEq(Solution.merge(a, b), List.of(1, 2, 3, 3, 5, 6), "interleaved with tie");
CjTestBase.checkEq(Solution.merge(new ArrayList<Integer>(), b), List.of(2, 3, 6), "a empty");
CjTestBase.checkEq(Solution.merge(a, new ArrayList<Integer>()), List.of(1, 3, 5), "b empty");
""",
        "Two-pointer while + two drain loops; ties take a first with <=.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p7-arraylist", "ArrayList lab",
    "Backward removal and insertion, value semantics, halves swap, object totals.",
    "Phòng ArrayList",
    "Xóa và chèn bằng vòng ngược, ngữ nghĩa giá trị, đổi nửa, tổng trên đối tượng.",
    after_lesson="cx-m7-boxing", minutes=60, difficulty="advanced",
    challenges=[P_EVENS, P_VALUEREM, P_INSERT, P_SWAP, P_ROSTER],
    vi_challenges={
        "cx-m7-remove-evens": vi_challenge("Xóa bằng vòng ngược",
            "Hiện thực `void removeEvens(ArrayList<Integer> nums)`: xóa mọi số chẵn tại chỗ. Vòng ngược là kỷ luật chủ đích — vòng xuôi sẽ gãy với các số chẵn liền kề như [4, 6].",
            [("evens removed", "for (int i = nums.size() - 1; i >= 0; i--) if (nums.get(i) % 2 == 0) nums.remove(i);")]),
        "cx-m7-remove-first-value": vi_challenge("Xóa theo giá trị có báo cáo",
            "Hiện thực `boolean removeFirst(ArrayList<String> list, String value)`: xóa phần tử ĐẦU TIÊN bằng giá trị (theo nội dung); trả về có xóa được gì không. Giá trị vắng mặt → false, danh sách nguyên vẹn.",
            [("first match removed", "indexOf trả về lần khớp đầu; -1 nghĩa là vắng mặt. remove(index) hoặc remove(Object).")]),
        "cx-m7-insert-after-evens": vi_challenge("Chèn bằng vòng ngược",
            "Hiện thực `void insertAfterEvens(ArrayList<Integer> nums)`: chèn 0 ngay sau mỗi phần tử chẵn. Phép chèn dịch phải — vòng xuôi sẽ tự xử lý chính phần nó vừa chèn mãi mãi. [2, 3, 4] → [2, 0, 3, 4, 0].",
            [("zeros inserted", "Ngược: cho i chạy từ size-1 về 0, nếu get(i) chẵn thì add(i + 1, 0).")]),
        "cx-m7-swap-halves": vi_challenge("Đổi hai nửa",
            "Hiện thực `void swapHalves(ArrayList<Integer> list)`: đổi chỗ hai nửa tại chỗ. Kích thước lẻ: phần tử giữa thuộc về NỬA SAU: [1, 2, 3, 4, 5] → [3, 4, 5, 1, 2]. Làm ánh xạ chỉ số trên giấy cho kích thước 4 và 5 trước khi viết mã.",
            [("halves swapped", "half = size / 2; `half` phần tử đầu chuyển xuống cuối; kích thước lẻ: phần tử giữa thuộc nửa sau.")]),
        "cx-m7-roster-points": vi_challenge("Bộ sưu tập đối tượng",
            "Hiện thực `int rosterPoints(ArrayList<Member> roster, char letter)`: tổng điểm của các thành viên có tên bắt đầu bằng `letter` (phân biệt hoa thường), 0 khi không ai khớp. For-each trên đối tượng; chặn trường hợp tên rỗng.",
            [("filtered total", "char c = m.getName().charAt(0); cần getName().length() > 0 trước.")]),
    },
    solutions=[
        ("cx-m7-remove-evens",
         r"""import java.util.ArrayList;

public class Solution {
    public static void removeEvens(ArrayList<Integer> nums) {
        for (int i = nums.size() - 1; i >= 0; i--) {
            if (nums.get(i) % 2 == 0) {
                nums.remove(i);
            }
        }
    }
}
""",
         r"""import java.util.ArrayList;

public class Solution {
    public static void removeEvens(ArrayList<Integer> nums) {
        for (int i = 0; i < nums.size(); i++) {
            if (nums.get(i) % 2 == 0) {
                nums.remove(i);
            }
        }
    }
}
"""),
        ("cx-m7-remove-first-value", BOILER_VALUE_REM.replace("return false; // replace",
            "int at = list.indexOf(value);\n        if (at < 0) { return false; }\n        list.remove(at);\n        return true;"),
         BOILER_VALUE_REM.replace("return false; // replace",
            "int at = list.indexOf(value);\n        if (at > 0) {\n            list.remove(at);\n            return true;\n        }\n        return false;")),
        ("cx-m7-insert-after-evens",
         r"""import java.util.ArrayList;

public class Solution {
    public static void insertAfterEvens(ArrayList<Integer> nums) {
        for (int i = nums.size() - 1; i >= 0; i--) {
            if (nums.get(i) % 2 == 0) {
                nums.add(i + 1, 0);
            }
        }
    }
}
""",
         r"""import java.util.ArrayList;

public class Solution {
    public static void insertAfterEvens(ArrayList<Integer> nums) {
        for (int i = 0; i < nums.size(); i++) {
            if (nums.get(i) % 2 == 0) {
                nums.add(i + 1, 0);
            }
        }
    }
}
"""),
        ("cx-m7-swap-halves",
         r"""import java.util.ArrayList;

public class Solution {
    public static void swapHalves(ArrayList<Integer> list) {
        int half = list.size() / 2;
        int size = list.size();
        ArrayList<Integer> first = new ArrayList<Integer>();
        for (int i = 0; i < half; i++) { first.add(list.get(i)); }
        int k = 0;
        for (int i = half; i < size; i++) { list.set(k, list.get(i)); k++; }
        for (int i = 0; i < half; i++) { list.set(k, first.get(i)); k++; }
    }
}
""",
         r"""import java.util.ArrayList;

public class Solution {
    public static void swapHalves(ArrayList<Integer> list) {
        int half = list.size() / 2 + 1;
        int size = list.size();
        ArrayList<Integer> first = new ArrayList<Integer>();
        for (int i = 0; i < half; i++) { first.add(list.get(i)); }
        int k = 0;
        for (int i = half; i < size; i++) { list.set(k, list.get(i)); k++; }
        for (int i = 0; i < half; i++) { list.set(k, first.get(i)); k++; }
    }
}
"""),
        ("cx-m7-roster-points", BOILER_TOTALPT.replace("return 0; // replace",
            "int total = 0;\n        for (Member m : roster) {\n            String name = m.getName();\n            if (name.length() > 0 && name.charAt(0) == letter) {\n                total += m.getPoints();\n            }\n        }\n        return total;"),
         BOILER_TOTALPT.replace("return 0; // replace",
            "int total = 0;\n        for (Member m : roster) {\n            String name = m.getName();\n            if (name.length() > 0 && name.charAt(0) != letter) {\n                total += m.getPoints();\n            }\n        }\n        return total;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m7", "Checkpoint: the sorted merge",
    "Two-pointer merge with remainder drains — ArrayList's signature synthesis.",
    25,
    r"""
The merge is three machines in a trench coat: a two-pointer comparison,
and two sentinel drains. Get the tie direction right (`<=` takes from
`a` first) and the empty cases are free — the drain loops handle them
without extra code. This shape returns in the exam's ArrayList FRQ
almost every year in disguise.
""",
    "Điểm kiểm tra: merge có thứ tự",
    "Merge hai con trỏ với các vòng rút phần còn lại — tổng hợp đặc trưng của ArrayList.",
    r"""
Merge là ba cỗ máy khoác áo choàng nhau: một phép so sánh hai con trỏ,
và hai vòng rút lính canh. Đi đúng hướng đồng giá (`<=` lấy từ `a`
trước) và các trường hợp rỗng là miễn phí — các vòng rút xử lý chúng
mà không cần mã thêm. Hình dạng này tái xuất trong FRQ ArrayList của đề
thi gần như mỗi năm, chỉ thay lớp nguỵ trang.
""",
    CP7,
    vi_challenge("Điểm kiểm tra: merge có thứ tự",
        "Hiện thực `ArrayList<Integer> merge(ArrayList<Integer> a, ArrayList<Integer> b)`: gộp hai danh sách đã sắp xếp thành danh sách mới vẫn sắp xếp, cho phép trùng, đồng giá lấy từ `a` trước. Cấu trúc ba-vòng-lặp trong bài học ánh xạ trực tiếp — viết từ các cỗ máy, đừng viết từ trí nhớ.",
        [("merged in order", "While hai con trỏ + hai vòng rút; đồng giá lấy a trước bằng <=.")]),
    solution=r"""import java.util.ArrayList;

public class Solution {
    public static ArrayList<Integer> merge(ArrayList<Integer> a, ArrayList<Integer> b) {
        ArrayList<Integer> out = new ArrayList<Integer>();
        int i = 0, j = 0;
        while (i < a.size() && j < b.size()) {
            if (a.get(i) <= b.get(j)) { out.add(a.get(i)); i++; }
            else { out.add(b.get(j)); j++; }
        }
        while (i < a.size()) { out.add(a.get(i)); i++; }
        while (j < b.size()) { out.add(b.get(j)); j++; }
        return out;
    }
}
""",
    wrong=r"""import java.util.ArrayList;

public class Solution {
    public static ArrayList<Integer> merge(ArrayList<Integer> a, ArrayList<Integer> b) {
        ArrayList<Integer> out = new ArrayList<Integer>();
        int i = 0, j = 0;
        while (i < a.size() && j < b.size()) {
            if (a.get(i) <= b.get(j)) { out.add(a.get(i)); i++; }
            else { out.add(b.get(j)); j++; }
        }
        return out;
    }
}
""",
)
