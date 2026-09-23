#!/usr/bin/env python3
"""AP CSA M10 — ArrayList (generics, autoboxing, mutation-while-iterating)."""
from apc import *

M = "apc-arraylist"

L1 = r"""
An `ArrayList` is a **resizable** list of objects. Unlike arrays, it grows
and shrinks:

```java
import java.util.ArrayList;

ArrayList<String> names = new ArrayList<String>();
names.add("An");
names.add("Binh");
names.add("Chi");
```

The `<String>` in angle brackets is the **generic type**: it declares what
the list holds, and the compiler then enforces it — `names.add(42)` is a
compile error. (The shorthand `new ArrayList<>()` is legal Java but the AP
reference uses the explicit form; know both.)

**The exam's method set:**

```java
names.size()               // 3  — method, not a field!
names.get(0)               // "An"
names.set(1, "Bao")        // replaces index 1; returns the old value
names.add("Duong")         // appends at the end
names.add(1, "Binh")       // INSERTS at 1, shifting the rest right
names.remove(0)            // removes index 0, shifting left; returns it
names.contains("Chi")      // true
names.indexOf("Chi")       // 1
```

**Autoboxing**: a list of numbers is `ArrayList<Integer>` (the wrapper
class) — never `ArrayList<int>`. Java converts `int ↔ Integer`
automatically when you add or get:

```java
ArrayList<Integer> nums = new ArrayList<Integer>();
nums.add(5);                    // int boxed to Integer
int first = nums.get(0);        // unboxed back to int
```
"""

L2 = r"""
The three-way mnemonic the exam loves to test:

| | arrays | String | ArrayList |
| --- | --- | --- | --- |
| size | `arr.length` | `s.length()` | `list.size()` |
| read | `arr[i]` | `s.charAt(i)` | `list.get(i)` |
| write | `arr[i] = v` | (immutable) | `list.set(i, v)` |

**Traversing** an ArrayList — two safe forms:

```java
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}

for (String s : list) {          // enhanced for: read-only visits
    System.out.println(s);
}
```

**The trap**: `remove` *shifts* everything after the removed index left.
Remove while walking forward and you skip the element right after each
removal:

```java
// remove all "x" from ["x", "x", "a"] — WRONG
for (int i = 0; i < list.size(); i++) {
    if (list.get(i).equals("x")) {
        list.remove(i);      // i++ now skips the shifted-in element
    }
}
// result: ["x", "a"] — an x survives!
```

Three correct fixes: walk **backwards** (`for (int i = list.size() - 1; i
>= 0; i--)`), re-check the same index after removing (`i--`), or use the
enhanced for only when you remove nothing. Consecutive-duplicate questions
are built exactly on this trap.
"""

L3 = r"""
FRQ **Question 3 (Data Analysis with ArrayList)** provides a class and asks
you to write one method. The recurring algorithm shapes:

**Filter into a new list** (no mutation of the source):

```java
public static ArrayList<String> longWords(ArrayList<String> words) {
    ArrayList<String> out = new ArrayList<String>();
    for (String w : words) {
        if (w.length() >= 5) {
            out.add(w);
        }
    }
    return out;
}
```

**Aggregate:**

```java
public static int totalLetters(ArrayList<String> words) {
    int total = 0;
    for (String w : words) {
        total += w.length();
    }
    return total;
}
```

**Conditional removal** — the backwards walk:

```java
public static void removeShort(ArrayList<String> words) {
    for (int i = words.size() - 1; i >= 0; i--) {
        if (words.get(i).length() < 3) {
            words.remove(i);
        }
    }
}
```

**Find max/count by property** mixes M9's patterns with `.get(i)` syntax.
One more spec-reading note: FRQ specs say things like "the list contains at
least one element" — that is your license to seed `best = list.get(0)`
without an empty-list branch.
"""

write_module(
    M,
    "ArrayList",
    "Generics and autoboxing, the exam method set, safe removal patterns, and FRQ-style list analysis.",
    "ArrayList",
    "Generic và autoboxing, bộ phương thức của đề thi, các mẫu xóa an toàn, và phân tích danh sách kiểu FRQ.",
    lessons=["apc-m10-api", "apc-m10-remove", "apc-m10-frq", "apc-cp-m10"],
    practices=["apc-p10-arraylist"],
)

write_lesson(
    M, "apc-m10-api", "The ArrayList API",
    "Generic types, autoboxing with Integer, the exam method set.",
    14, L1,
    "Bộ API ArrayList",
    "Kiểu generic, autoboxing với Integer, bộ phương thức của đề thi.",
    r"""
`ArrayList` là danh sách **co giãn được** các đối tượng. Khác mảng, nó lớn
lên và nhỏ lại:

```java
import java.util.ArrayList;

ArrayList<String> names = new ArrayList<String>();
names.add("An");
names.add("Binh");
names.add("Chi");
```

`<String>` trong ngoặc nhọn là **kiểu generic**: nó khai báo danh sách chứa
gì, và trình biên dịch sẽ kiểm soát — `names.add(42)` là lỗi biên dịch.
(Dạng tắt `new ArrayList<>()` là Java hợp lệ nhưng tài liệu AP dùng dạng
viết tường minh; biết cả hai.)

**Bộ phương thức của đề thi:**

```java
names.size()               // 3  — là phương thức, không phải trường!
names.get(0)               // "An"
names.set(1, "Bao")        // thay chỉ số 1; trả về giá trị cũ
names.add("Duong")         // thêm vào cuối
names.add(1, "Binh")       // CHÈN vào 1, dịch phần còn lại sang phải
names.remove(0)            // xóa chỉ số 0, dịch sang trái; trả về nó
names.contains("Chi")      // true
names.indexOf("Chi")       // 1
```

**Autoboxing**: danh sách số là `ArrayList<Integer>` (lớp bao bọc) — không
bao giờ `ArrayList<int>`. Java chuyển `int ↔ Integer` tự động khi thêm hoặc
lấy:

```java
ArrayList<Integer> nums = new ArrayList<Integer>();
nums.add(5);                    // int được box thành Integer
int first = nums.get(0);        // unbox về int
```
""",
)

write_lesson(
    M, "apc-m10-remove", "Removing safely",
    "The length/size/charAt/get table, and the remove-while-iterating trap.",
    14, L2,
    "Xóa một cách an toàn",
    "Bảng length/size/charAt/get, và cái bẫy xóa-đang-duyệt.",
    r"""
Bụt ngữ ba-way đề thi thích kiểm tra:

| | mảng | String | ArrayList |
| --- | --- | --- | --- |
| kích thước | `arr.length` | `s.length()` | `list.size()` |
| đọc | `arr[i]` | `s.charAt(i)` | `list.get(i)` |
| ghi | `arr[i] = v` | (bất biến) | `list.set(i, v)` |

**Duyệt** ArrayList — hai dạng an toàn:

```java
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}

for (String s : list) {          // enhanced for: chỉ đọc
    System.out.println(s);
}
```

**Cái bẫy**: `remove` *dịch* mọi phần tử sau chỉ số bị xóa sang trái. Xóa
trong khi đi tới và bạn bỏ sót phần tử ngay sau mỗi lần xóa:

```java
// xóa hết "x" khỏi ["x", "x", "a"] — SAI
for (int i = 0; i < list.size(); i++) {
    if (list.get(i).equals("x")) {
        list.remove(i);      // i++ giờ bỏ qua phần tử vừa dịch vào
    }
}
// kết quả: ["x", "a"] — còn sót một x!
```

Ba cách sửa đúng: đi **ngược** (`for (int i = list.size() - 1; i >= 0;
i--)`), kiểm tra lại cùng chỉ số sau khi xóa (`i--`), hoặc dùng enhanced for
chỉ khi bạn không xóa gì. Các bài "xóa phần tử trùng liền kề" được xây đúng
trên cái bẫy này.
""",
)

write_lesson(
    M, "apc-m10-frq", "FRQ list analysis",
    "Filter-copy, aggregate, conditional removal, spec-reading notes.",
    12, L3,
    "Phân tích danh sách kiểu FRQ",
    "Lọc-sang-list-mới, tổng hợp, xóa có điều kiện, ghi chú đọc đề.",
    r"""
FRQ **Câu 3 (Phân tích dữ liệu với ArrayList)** cung cấp một lớp và yêu cầu
viết một phương thức. Các dạng thuật toán lặp lại:

**Lọc sang danh sách mới** (không đổi nguồn):

```java
public static ArrayList<String> longWords(ArrayList<String> words) {
    ArrayList<String> out = new ArrayList<String>();
    for (String w : words) {
        if (w.length() >= 5) {
            out.add(w);
        }
    }
    return out;
}
```

**Tổng hợp:**

```java
public static int totalLetters(ArrayList<String> words) {
    int total = 0;
    for (String w : words) {
        total += w.length();
    }
    return total;
}
```

**Xóa có điều kiện** — đi ngược:

```java
public static void removeShort(ArrayList<String> words) {
    for (int i = words.size() - 1; i >= 0; i--) {
        if (words.get(i).length() < 3) {
            words.remove(i);
        }
    }
}
```

**Tìm max/đếm theo thuộc tính** trộn các mẫu của M9 với cú pháp `.get(i)`.
Một ghi chú đọc đề: đặc tả FRQ nói những câu như "danh sách chứa ít nhất một
phần tử" — đó là giấy phép để khởi tạo `best = list.get(0)` mà không cần
nhánh xử lý danh sách rỗng.
""",
)

BOILER_TOTAL = r"""public class Solution {
    public static int totalLetters(java.util.ArrayList<String> words) {
        return 0; // replace
    }
}
"""

BOILER_ODDS = r"""public class Solution {
    public static java.util.ArrayList<Integer> odds(java.util.ArrayList<Integer> nums) {
        return new java.util.ArrayList<Integer>(); // replace: NEW list of the odd values
    }
}
"""

BOILER_REMOVEDUP = r"""public class Solution {
    public static void removeAdjacentDuplicates(java.util.ArrayList<String> list) {
        // replace: remove every element equal to the one before it
    }
}
"""

BOILER_LASTOCC = r"""public class Solution {
    public static int lastIndexOf(java.util.ArrayList<String> list, String target) {
        return -1; // replace
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static void removeAll(java.util.ArrayList<String> list, String target) {
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).equals(target)) {
                list.remove(i);
            }
        }
    }
}
"""

CP10 = r"""public class Solution {
    public static java.util.ArrayList<String> topScorers(java.util.ArrayList<String> names, java.util.ArrayList<Integer> scores, int cutoff) {
        return new java.util.ArrayList<String>(); // replace
    }
}
"""

P_TOTAL = challenge(
    "apc-m10-totalletters",
    "Total letters",
    "Implement `int totalLetters(ArrayList<String> words)`: the sum of every word's length. Empty list → 0.",
    BOILER_TOTAL,
    [(
        "letters summed",
        r"""
java.util.ArrayList<String> ws = new java.util.ArrayList<String>();
java.util.Collections.addAll(ws, "hi", "there");
CjTestBase.checkEq(Solution.totalLetters(ws), 7, "2 + 5");
CjTestBase.checkEq(Solution.totalLetters(new java.util.ArrayList<String>()), 0, "empty");
""",
        "Accumulate w.length() over an enhanced-for.",
    )],
    level="imitation",
)

P_ODDS = challenge(
    "apc-m10-odds",
    "Filter into a new list",
    "Implement `ArrayList<Integer> odds(ArrayList<Integer> nums)`: a NEW list holding only the odd values, in order. The source list must be unchanged, and `nums` may be empty.",
    BOILER_ODDS,
    [(
        "odd filter",
        r"""
java.util.ArrayList<Integer> src = new java.util.ArrayList<Integer>();
java.util.Collections.addAll(src, 1, 2, 3, 4, 5);
java.util.ArrayList<Integer> out = Solution.odds(src);
CjTestBase.checkEq(out.size(), 3, "three odds");
CjTestBase.checkEq(out.get(0), 1, "first");
CjTestBase.checkEq(out.get(2), 5, "last");
CjTestBase.checkEq(src.size(), 5, "source untouched");
""",
        "x % 2 != 0 tests odd for negatives too; build a fresh ArrayList.",
    )],
    level="guided",
)

P_DUP = challenge(
    "apc-m10-adjdup",
    "Remove adjacent duplicates",
    "Implement `void removeAdjacentDuplicates(ArrayList<String> list)`: mutate the list so any run of equal neighboring elements collapses to one — [\"a\",\"a\",\"b\",\"b\",\"b\",\"c\"] becomes [\"a\",\"b\",\"c\"]. Mind the shifting trap: walk BACKWARDS.",
    BOILER_REMOVEDUP,
    [(
        "runs collapsed",
        r"""
java.util.ArrayList<String> l = new java.util.ArrayList<String>();
java.util.Collections.addAll(l, "a", "a", "b", "b", "b", "c");
Solution.removeAdjacentDuplicates(l);
CjTestBase.checkEq(l.size(), 3, "three left");
CjTestBase.checkEq(l.get(0), "a", "a");
CjTestBase.checkEq(l.get(2), "c", "c");
""",
        "Backwards loop: remove i when list.get(i).equals(list.get(i - 1)).",
    )],
    level="combination",
)

P_LAST = challenge(
    "apc-m10-lastocc",
    "Last occurrence",
    "Implement `int lastIndexOf(ArrayList<String> list, String target)`: the highest index holding target, or -1 when absent. Walk backwards and return early.",
    BOILER_LASTOCC,
    [(
        "last positions",
        r"""
java.util.ArrayList<String> l = new java.util.ArrayList<String>();
java.util.Collections.addAll(l, "a", "b", "a", "c", "a");
CjTestBase.checkEq(Solution.lastIndexOf(l, "a"), 4, "last a");
CjTestBase.checkEq(Solution.lastIndexOf(l, "b"), 1, "single b");
CjTestBase.checkEq(Solution.lastIndexOf(l, "z"), -1, "absent");
""",
        "Backwards loop returns the first match it sees — that is the last.",
    )],
    level="guided",
)

P_FIX = challenge(
    "apc-m10-fix-removeall",
    "Debug the removal",
    "`removeAll` should delete every occurrence of target, but some targets survive. Explain-why-then-fix: the forward loop skips shifted elements. Rewrite with a correct pattern.",
    BOILER_FIX,
    [(
        "all gone",
        r"""
java.util.ArrayList<String> l = new java.util.ArrayList<String>();
java.util.Collections.addAll(l, "x", "x", "a", "x");
Solution.removeAll(l, "x");
CjTestBase.checkEq(l.size(), 1, "one survivor");
CjTestBase.checkEq(l.get(0), "a", "it is a");
""",
        "Backwards loop, or i-- after each remove.",
    )],
    level="debugging",
)

CP10C = challenge(
    "apc-cp-m10-top",
    "Checkpoint: parallel lists",
    "Implement `ArrayList<String> topScorers(ArrayList<String> names, ArrayList<Integer> scores, int cutoff)`: return a new list of every name whose matching score (same index) is strictly greater than cutoff, in order. The two lists have equal length.",
    CP10,
    [(
        "parallel scan",
        r"""
java.util.ArrayList<String> ns = new java.util.ArrayList<String>();
java.util.ArrayList<Integer> ss = new java.util.ArrayList<Integer>();
java.util.Collections.addAll(ns, "An", "Binh", "Chi");
java.util.Collections.addAll(ss, 5, 9, 8);
java.util.ArrayList<String> top = Solution.topScorers(ns, ss, 6);
CjTestBase.checkEq(top.size(), 2, "two pass cutoff");
CjTestBase.checkEq(top.get(0), "Binh", "Binh first");
CjTestBase.checkEq(top.get(1), "Chi", "Chi second");
""",
        "One indexed loop over both lists; score.get(i) > cutoff decides.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p10-arraylist", "List practice", "Filter, aggregate, mutate safely, scan in parallel.",
    "Luyện danh sách", "Lọc, tổng hợp, thay đổi an toàn, quét song song.",
    after_lesson="apc-m10-remove", minutes=55, difficulty="beginner",
    challenges=[P_TOTAL, P_ODDS, P_DUP, P_LAST, P_FIX],
    vi_challenges={
        "apc-m10-totalletters": vi_challenge("Tổng số chữ cái", "Cài đặt `int totalLetters(ArrayList<String> words)`: tổng độ dài của mọi từ. Danh sách rỗng → 0.",
            [("letters summed", "Tích lũy w.length() qua enhanced-for.")]),
        "apc-m10-odds": vi_challenge("Lọc sang danh sách mới", "Cài đặt `ArrayList<Integer> odds(ArrayList<Integer> nums)`: một danh sách MỚI chỉ giữ các giá trị lẻ, theo thứ tự. Danh sách nguồn không được đổi, và `nums` có thể rỗng.",
            [("odd filter", "x % 2 != 0 kiểm tra lẻ cả với số âm; dựng ArrayList mới.")]),
        "apc-m10-adjdup": vi_challenge("Xóa trùng liền kề", "Cài đặt `void removeAdjacentDuplicates(ArrayList<String> list)`: biến đổi danh sách để mỗi chuỗi phần tử giống nhau liền kề còn một — [\"a\",\"a\",\"b\",\"b\",\"b\",\"c\"] thành [\"a\",\"b\",\"c\"]. Co chừng bẫy dịch chuyển: đi NGƯỢC.",
            [("runs collapsed", "Vòng ngược: xóa i khi list.get(i).equals(list.get(i - 1)).")]),
        "apc-m10-lastocc": vi_challenge("Lần xuất hiện cuối", "Cài đặt `int lastIndexOf(ArrayList<String> list, String target)`: chỉ số cao nhất chứa target, hoặc -1 khi vắng. Đi ngược và return sớm.",
            [("last positions", "Vòng ngược trả vềmatch đầu tiên nó thấy — đó chính là cái cuối.")]),
        "apc-m10-fix-removeall": vi_challenge("Sửa phép xóa", "`removeAll` phải xóa mọi lần xuất hiện của target, nhưng một số target còn sống. Giải thích rồi sửa: vòng đi tới bỏ sót phần tử bị dịch. Viết lại với mẫu đúng.",
            [("all gone", "Vòng ngược, hoặc i-- sau mỗi lần xóa.")]),
    },
    solutions=[
        ("apc-m10-totalletters", r"""public class Solution {
    public static int totalLetters(java.util.ArrayList<String> words) {
        int total = 0;
        for (String w : words) {
            total += w.length();
        }
        return total;
    }
}
""",
         r"""public class Solution {
    public static int totalLetters(java.util.ArrayList<String> words) {
        // BUG: counts words, not letters
        int total = 0;
        for (String w : words) {
            total += 1;
        }
        return total;
    }
}
"""),
        ("apc-m10-odds", r"""public class Solution {
    public static java.util.ArrayList<Integer> odds(java.util.ArrayList<Integer> nums) {
        java.util.ArrayList<Integer> out = new java.util.ArrayList<Integer>();
        for (int x : nums) {
            if (x % 2 != 0) {
                out.add(x);
            }
        }
        return out;
    }
}
""",
         r"""public class Solution {
    public static java.util.ArrayList<Integer> odds(java.util.ArrayList<Integer> nums) {
        // BUG: mutates the source instead of building a new list
        for (int i = nums.size() - 1; i >= 0; i--) {
            if (nums.get(i) % 2 == 0) {
                nums.remove(i);
            }
        }
        return nums;
    }
}
"""),
        ("apc-m10-adjdup", r"""public class Solution {
    public static void removeAdjacentDuplicates(java.util.ArrayList<String> list) {
        for (int i = list.size() - 1; i >= 1; i--) {
            if (list.get(i).equals(list.get(i - 1))) {
                list.remove(i);
            }
        }
    }
}
""",
         r"""public class Solution {
    public static void removeAdjacentDuplicates(java.util.ArrayList<String> list) {
        // BUG: forward walk skips shifted-in elements — some duplicates survive
        for (int i = 1; i < list.size(); i++) {
            if (list.get(i).equals(list.get(i - 1))) {
                list.remove(i);
            }
        }
    }
}
"""),
        ("apc-m10-lastocc", r"""public class Solution {
    public static int lastIndexOf(java.util.ArrayList<String> list, String target) {
        for (int i = list.size() - 1; i >= 0; i--) {
            if (list.get(i).equals(target)) {
                return i;
            }
        }
        return -1;
    }
}
""",
         r"""public class Solution {
    public static int lastIndexOf(java.util.ArrayList<String> list, String target) {
        // BUG: returns the FIRST occurrence
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).equals(target)) {
                return i;
            }
        }
        return -1;
    }
}
"""),
        ("apc-m10-fix-removeall", r"""public class Solution {
    public static void removeAll(java.util.ArrayList<String> list, String target) {
        for (int i = list.size() - 1; i >= 0; i--) {
            if (list.get(i).equals(target)) {
                list.remove(i);
            }
        }
    }
}
""",
         r"""public class Solution {
    public static void removeAll(java.util.ArrayList<String> list, String target) {
        // BUG: original flaw kept — forward walk skips shifted elements
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).equals(target)) {
                list.remove(i);
            }
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m10", "Checkpoint: parallel lists",
    "Scan two lists in lockstep and build a filtered result.",
    22,
    r"""
Parallel-list analysis is a genuine FRQ Q3 shape: one indexed loop, two
gets, one condition, one new list. Build it exactly that way.
""",
    "Điểm kiểm tra: danh sách song song",
    "Quét hai danh sách đồng bộ và dựng kết quả đã lọc.",
    r"""
Phân tích danh sách song song là một dạng FRQ Câu 3 thật: một vòng có chỉ
số, hai get, một điều kiện, một danh sách mới. Dựng đúng như vậy.
""",
    CP10C,
    vi_challenge("Điểm kiểm tra: danh sách song song", "Cài đặt `ArrayList<String> topScorers(ArrayList<String> names, ArrayList<Integer> scores, int cutoff)`: trả về danh sách mới gồm mọi tên có điểm tương ứng (cùng chỉ số) lớn hơn cutoff một cách nghiêm ngặt, theo thứ tự. Hai danh sách có độ dài bằng nhau.",
        [("parallel scan", "Một vòng có chỉ số qua cả hai danh sách; score.get(i) > cutoff quyết định.")]),
    solution=r"""public class Solution {
    public static java.util.ArrayList<String> topScorers(java.util.ArrayList<String> names, java.util.ArrayList<Integer> scores, int cutoff) {
        java.util.ArrayList<String> out = new java.util.ArrayList<String>();
        for (int i = 0; i < names.size(); i++) {
            if (scores.get(i) > cutoff) {
                out.add(names.get(i));
            }
        }
        return out;
    }
}
""",
    wrong=r"""public class Solution {
    public static java.util.ArrayList<String> topScorers(java.util.ArrayList<String> names, java.util.ArrayList<Integer> scores, int cutoff) {
        // BUG: pairs the wrong indexes — names.get(i) vs scores.get(size-1-i)
        java.util.ArrayList<String> out = new java.util.ArrayList<String>();
        for (int i = 0; i < names.size(); i++) {
            if (scores.get(scores.size() - 1 - i) > cutoff) {
                out.add(names.get(i));
            }
        }
        return out;
    }
}
""",
)
