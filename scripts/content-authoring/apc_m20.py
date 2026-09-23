#!/usr/bin/env python3
"""AP CSA M20 — AP CSA Readiness Checkpoint: capstone synthesis across all units."""
from apc import *

M = "apc-readiness"

L1 = r"""
You are ready for dedicated AP CSA exam preparation when you can do
all of the following WITHOUT looking anything up:

- **Read**: given unfamiliar code, say what each variable holds at
  each line, which method runs, and what is returned or printed.
- **Write**: given a prose spec, produce a compiling method that
  matches the signature and honors pre/postconditions.
- **Debug**: classify an error (compile/runtime/logical) and repair it
  at the cause.
- **Design**: decompose a small problem into classes with private
  fields, constructors, accessors, and behavior methods.
- **Reason**: state the iteration count and complexity class of a
  loop structure, and choose the right traversal.

The capstone challenge below touches all four units of the revised
framework: objects and methods, selection and iteration, class
creation, and data collections. Work it on paper first — the exam
gives you a pencil, and the habit starts now.
"""

L2 = r"""
**Reading unfamiliar code** — the exam's Unit-weighted core skill.
The methodical pass:

1. Inventory the members: fields, constructors, methods. Private?
   Static? One line each.
2. For each method: precondition → postcondition in your own words.
3. Trace the call sequence the question names, one row per call,
   every field updated per row.
4. Answer from the table, never from vibes.

```java
public static class Meter {
    private int units;
    private int cap;

    public Meter(int cap) { this.cap = cap; this.units = 0; }

    public void tick() {
        if (units < cap) { units++; }
    }

    public boolean overflowed() { return units == cap; }
}
```

What does this print?

```java
Meter m = new Meter(2);
m.tick(); m.tick(); m.tick();
System.out.println(m.overflowed());
```

Trace: tick→1, tick→2, tick→no-op (cap). `overflowed()` → true. If
you got that by tracing instead of pattern-matching "ticks past cap",
the course did its job — the cap is a boundary, and boundaries are
where the exam lives.
"""

L3 = r"""
**The readiness gap** — what this course deliberately did NOT cover,
and what the next course will:

- Full FRQ strategy: time allocation, partial-credit harvesting,
  the four question types in exam format.
- Inheritance/polymorphism at exam depth (this course kept it light,
  matching the revised framework's reduced weight).
- 2D-array FRQ patterns beyond the foundations of Module 15.
- Formal algorithm analysis beyond O(n)/O(n²) intuition.

Self-assessment before moving on: redo any checkpoint where your
first attempt needed hints; rebuild any challenge from scratch on a
blank page; and teach one pattern (accumulator, state machine, or
select-transform) out loud to a classmate. If you can teach it, the
next course can build on it.
"""

write_module(
    M,
    "AP CSA Readiness",
    "The capstone: a synthesis checkpoint across all four units, plus a reading exam and a readiness self-assessment.",
    "Sẵn sàng AP CSA",
    "Chốt chặn tổng hợp: một bài kiểm tra xuyên bốn chủ đề, kèm bài đọc mã thi và tự đánh giá mức sẵn sàng.",
    lessons=["apc-m20-ready", "apc-m20-reading", "apc-m20-gap", "apc-cp-m20"],
    practices=["apc-p20-readiness"],
)

write_lesson(
    M, "apc-m20-ready", "The readiness bar",
    "Five abilities that define exam-readiness — read, write, debug, design, reason.",
    10, L1,
    "Chuẩn sẵn sàng",
    "Năm năng lực định nghĩa sự sẵn sàng thi — đọc, viết, gỡ, thiết kế, lý giải.",
    r"""
Bạn sẵn sàng cho khóa luyện thi AP CSA chuyên sâu khi làm được TẤT
CẢ những điều dưới đây mà không cần tra cứu:

- **Đọc**: cho mã lạ, nói được từng biến giữ gì ở từng dòng, phương
  thức nào chạy, và cái gì được trả về hoặc in ra.
- **Viết**: cho đặc tả bằng văn bản, viết được phương thức biên dịch
  được, khớp chữ ký, tôn trọng điều kiện tiền/hậu.
- **Gỡ lỗi**: phân loại lỗi (biên dịch/runtime/logic) và sửa tại gốc.
- **Thiết kế**: tách bài nhỏ thành các lớp có trường private, hàm
  dựng, accessor, và phương thức hành vi.
- **Lý giải**: nêu số vòng lặp và lớp độ phức tạp của một cấu trúc
  lặp, và chọn đúng kiểu duyệt.

Bài chốt chặn bên dưới chạm cả bốn chủ đề của khung sửa đổi: đối
tượng và phương thức, rẽ nhánh và lặp, tạo lớp, và bộ sưu tập dữ
liệu. Làm trên giấy trước — đề thi đưa cho bạn bút chì, và thói quen
bắt đầu từ bây giờ.
""",
)

write_lesson(
    M, "apc-m20-reading", "Reading unfamiliar code",
    "The four-pass method: inventory, contracts, trace table, answer.",
    12, L2,
    "Đọc mã chưa từng thấy",
    "Phương pháp bốn lượt: kiểm kê, hợp đồng, bảng truy vết, trả lời.",
    r"""
**Đọc mã chưa từng thấy** — kỹ năng lõi được tính điểm theo chủ đề
của đề. Lượt đi có phương pháp:

1. Kiểm kê thành viên: trường, hàm dựng, phương thức. Private?
   Static? Mỗi thứ một dòng.
2. Với mỗi phương thức: điều kiện tiền → điều kiện hậu bằng lời của
   bạn.
3. Truy vết chuỗi lời gọi mà câu hỏi nêu, mỗi lời gọi một hàng, cập
   nhật mọi trường mỗi hàng.
4. Trả lời từ bảng, không bao giờ dựa vào cảm tính.

```java
public static class Meter {
    private int units;
    private int cap;

    public Meter(int cap) { this.cap = cap; this.units = 0; }

    public void tick() {
        if (units < cap) { units++; }
    }

    public boolean overflowed() { return units == cap; }
}
```

Đoạn này in gì?

```java
Meter m = new Meter(2);
m.tick(); m.tick(); m.tick();
System.out.println(m.overflowed());
```

Truy vết: tick→1, tick→2, tick→không-làm-gì (chạm cap).
`overflowed()` → true. Nếu bạn có đáp án bằng truy vết thay vì bắt
mẫu hình "tick quá cap", khóa học đã xong việc của nó — cap là một
biên, và biên là nơi đề thi sống.
""",
)

write_lesson(
    M, "apc-m20-gap", "The readiness gap",
    "What comes next: full FRQ strategy, deeper inheritance, 2D FRQ patterns.",
    8, L3,
    "Khoảng cách còn lại",
    "Điều gì tiếp theo: chiến lược FRQ đầy đủ, kế thừa sâu hơn, các mẫu FRQ 2D.",
    r"""
**Khoảng cách sẵn sàng** — những gì khóa này CỐ Ý chưa dạy, và khóa
sau sẽ dạy:

- Chiến lược FRQ đầy đủ: phân bổ thời gian, gom điểm từng phần, bốn
  dạng câu hỏi đúng định dạng đề.
- Kế thừa/đa hình ở độ sâu đề thi (khóa này giữ nhẹ, khớp trọng số
  giảm của khung sửa đổi).
- Các mẫu FRQ mảng hai chiều vượt nền tảng của Module 15.
- Phân tích thuật toán chính thức vượt trực giác O(n)/O(n²).

Tự đánh giá trước khi tiến: làm lại mọi checkpoint mà lần đầu cần
gợi ý; dựng lại bất kỳ challenge nào trên trang giấy trắng; và dạy
một mẫu hình (bộ tích lũy, máy trạng thái, hoặc
chọn-biến-đổi) thành tiếng cho một bạn cùng lớp. Dạy được nghĩa là
khóa sau có thể xây trên đó.
""",
)

BOILER_LIB =    r"""
import java.util.*;

public class Solution {
    public static class Book {
        private String title;
        private int pages;

        public Book(String title, int pages) {
            this.title = title;
            this.pages = pages;
        }

        public String getTitle() {
            return title;
        }

        public int getPages() {
            return pages;
        }
    }

    // Postcondition: returns the total pages across all books with
    // pages <= limit, in any order of iteration
    public static int shelfPages(ArrayList<Book> shelf, int limit) {
        // complete
        return 0;
    }
}
"""

BOILER_FIXCAP = r"""public class Solution {
    public static class Meter {
        private int units;
        private int cap;

        public Meter(int cap) {
            this.cap = cap;
            this.units = 0;
        }

        public void tick() {
            // BUG: original flaw kept — ticks past the cap, so
            // overflowed() (units == cap) can never become true
            units++;
        }

        public boolean overflowed() {
            return units == cap;
        }
    }
}
"""

BOILER_BANK = r"""public class Solution {
    public static class Account {
        private int balance;

        public Account(int opening) {
            balance = opening;
        }

        public int getBalance() {
            return balance;
        }

        // Postcondition: adds amount if positive; returns new balance
        public int deposit(int amount) {
            // complete
            return balance;
        }

        // Postcondition: subtracts amount if the balance covers it;
        // returns true and updates state, otherwise returns false and
        // leaves state unchanged
        public boolean withdraw(int amount) {
            // complete
            return false;
        }
    }
}
"""

CP20 = r"""
import java.util.*;

public class Solution {
    public static class Playlist {
        private ArrayList<String> tracks;

        public Playlist() {
            tracks = new ArrayList<String>();
        }

        // Postcondition: appends the title (duplicates allowed)
        public void add(String title) {
            // complete
        }

        // Postcondition: removes the FIRST occurrence of title and
        // returns true; if absent, returns false with no change
        public boolean remove(String title) {
            // complete
        }

        // Postcondition: returns the number of tracks
        public int size() {
            // complete
            return 0;
        }
    }
}
"""

P_LIB = challenge(
    "apc-m20-shelf",
    "Capstone: the shelf",
    "Implement `shelfPages(ArrayList<Book> shelf, int limit)`: total pages across books with pages <= limit. Uses selection + accumulation over an object collection.",
    BOILER_LIB,
    [(
        "filter and sum",
        r"""
ArrayList<Solution.Book> shelf = new ArrayList<Solution.Book>();
shelf.add(new Solution.Book("thin", 80));
shelf.add(new Solution.Book("fat", 900));
shelf.add(new Solution.Book("edge", 400));
CjTestBase.checkEq(Solution.shelfPages(shelf, 400), 480, "limit-inclusive: 80 + 400");
CjTestBase.checkEq(Solution.shelfPages(shelf, 0), 0, "nothing qualifies");
""",
        "if (b.getPages() <= limit) total += b.getPages();",
    )],
    level="independent",
)

P_FIXCAP = challenge(
    "apc-m20-fix-meter",
    "Capstone: debug the meter",
    "`Meter.tick()` increments unconditionally, so `overflowed()` (units == cap) never becomes true. Fix tick() to respect the cap. All signatures stay.",
    BOILER_FIXCAP,
    [(
        "cap respected",
        r"""
Solution.Meter m = new Solution.Meter(2);
m.tick(); m.tick(); m.tick();
CjTestBase.checkTrue(m.overflowed(), "capped at 2");
Solution.Meter n = new Solution.Meter(1);
n.tick();
CjTestBase.checkTrue(n.overflowed(), "capped at 1");
""",
        "if (units < cap) { units++; }",
    )],
    level="debugging",
)

P_BANK = challenge(
    "apc-m20-bank",
    "Capstone: the account",
    "Implement both mutators to spec: `deposit` adds only positive amounts and returns the new balance; `withdraw` succeeds only if the balance covers it, returning true/false and leaving state unchanged on failure.",
    BOILER_BANK,
    [(
        "both contracts",
        r"""
Solution.Account a = new Solution.Account(100);
CjTestBase.checkEq(a.deposit(50), 150, "deposit returns new balance");
CjTestBase.checkEq(a.deposit(-5), 150, "negative deposit ignored");
CjTestBase.checkEq(a.withdraw(200), false, "overdraw refused");
CjTestBase.checkEq(a.getBalance(), 150, "state unchanged");
CjTestBase.checkEq(a.withdraw(150), true, "exact withdrawal");
CjTestBase.checkEq(a.getBalance(), 0, "drained");
""",
        "two guards: amount > 0 for deposit, amount <= balance for withdraw.",
    )],
    level="independent",
)

CP20C = challenge(
    "apc-cp-m20-playlist",
    "Checkpoint: the playlist",
    "Complete the Playlist class to spec: `add` appends; `remove` deletes the FIRST occurrence of the title and returns true (false + no change if absent); `size` returns the count.",
    CP20,
    [(
        "first occurrence",
        r"""
Solution.Playlist p = new Solution.Playlist();
p.add("a"); p.add("b"); p.add("a");
CjTestBase.checkEq(p.size(), 3, "three tracks");
CjTestBase.checkEq(p.remove("a"), true, "first a removed");
CjTestBase.checkEq(p.size(), 2, "shrunk");
CjTestBase.checkEq(p.remove("zzz"), false, "absent refused");
CjTestBase.checkEq(p.size(), 2, "no change on refusal");
""",
        "remove(java.util.List.of-check): indexOf(title), then remove(index) if >= 0.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p20-readiness", "Readiness reps", "Shelf totals, meter caps, account contracts, playlist state.",
    "Luyện sẵn sàng", "Tổng kệ sách, chặn đồng hồ, hợp đồng tài khoản, trạng thái danh sách phát.",
    after_lesson="apc-m20-gap", minutes=50, difficulty="beginner",
    challenges=[P_LIB, P_FIXCAP, P_BANK],
    vi_challenges={
        "apc-m20-shelf": vi_challenge("Chốt chặn: kệ sách", "Cài đặt `shelfPages(ArrayList<Book> shelf, int limit)`: tổng số trang của các sách có pages <= limit. Dùng chọn + cộng dồn trên bộ sưu tập đối tượng.",
            [("filter and sum", "if (b.getPages() <= limit) total += b.getPages();")]),
        "apc-m20-fix-meter": vi_challenge("Chốt chặn: gỡ đồng hồ", "`Meter.tick()` tăng vô điều kiện, nên `overflowed()` (units == cap) không bao giờ thành true. Sửa tick() để tôn trọng cap. Giữ nguyên mọi chữ ký.",
            [("cap respected", "if (units < cap) { units++; }")]),
        "apc-m20-bank": vi_challenge("Chốt chặn: tài khoản", "Cài đặt cả hai mutator theo đặc tả: `deposit` chỉ cộng số dương và trả số dư mới; `withdraw` chỉ thành công khi số dư đủ, trả true/false và giữ nguyên trạng thái khi thất bại.",
            [("both contracts", "hai lớp chặn: amount > 0 cho deposit, amount <= balance cho withdraw.")]),
    },
    solutions=[
        ("apc-m20-shelf",    r"""
import java.util.*;

public class Solution {
    public static class Book {
        private String title;
        private int pages;

        public Book(String title, int pages) {
            this.title = title;
            this.pages = pages;
        }

        public String getTitle() {
            return title;
        }

        public int getPages() {
            return pages;
        }
    }

    public static int shelfPages(ArrayList<Book> shelf, int limit) {
        int total = 0;
        for (Book b : shelf) {
            if (b.getPages() <= limit) {
                total += b.getPages();
            }
        }
        return total;
    }
}
""",    r"""
import java.util.*;

public class Solution {
    public static class Book {
        private String title;
        private int pages;

        public Book(String title, int pages) {
            this.title = title;
            this.pages = pages;
        }

        public String getTitle() {
            return title;
        }

        public int getPages() {
            return pages;
        }
    }

    public static int shelfPages(ArrayList<Book> shelf, int limit) {
        // BUG: compares against the wrong bound — strictly-less
        // excludes exactly-at-limit books the spec includes
        int total = 0;
        for (Book b : shelf) {
            if (b.getPages() < limit) {
                total += b.getPages();
            }
        }
        return total;
    }
}
"""),
        ("apc-m20-fix-meter", r"""public class Solution {
    public static class Meter {
        private int units;
        private int cap;

        public Meter(int cap) {
            this.cap = cap;
            this.units = 0;
        }

        public void tick() {
            if (units < cap) {
                units++;
            }
        }

        public boolean overflowed() {
            return units == cap;
        }
    }
}
""", r"""public class Solution {
    public static class Meter {
        private int units;
        private int cap;

        public Meter(int cap) {
            this.cap = cap;
            this.units = 0;
        }

        public void tick() {
            // BUG: original flaw kept — ticks past the cap, so
            // overflowed() (units == cap) can never become true
            units++;
        }

        public boolean overflowed() {
            return units == cap;
        }
    }
}
"""),
        ("apc-m20-bank", r"""public class Solution {
    public static class Account {
        private int balance;

        public Account(int opening) {
            balance = opening;
        }

        public int getBalance() {
            return balance;
        }

        public int deposit(int amount) {
            if (amount > 0) {
                balance += amount;
            }
            return balance;
        }

        public boolean withdraw(int amount) {
            if (amount <= balance) {
                balance -= amount;
                return true;
            }
            return false;
        }
    }
}
""", r"""public class Solution {
    public static class Account {
        private int balance;

        public Account(int opening) {
            balance = opening;
        }

        public int getBalance() {
            return balance;
        }

        public int deposit(int amount) {
            // BUG: accepts negative amounts — a "deposit" drains the
            // account
            if (amount != 0) {
                balance += amount;
            }
            return balance;
        }

        public boolean withdraw(int amount) {
            if (amount <= balance) {
                balance -= amount;
                return true;
            }
            return false;
        }
    }
}
"""),
        ("apc-cp-m20-playlist", r"""
import java.util.*;

public class Solution {
    public static class Playlist {
        private ArrayList<String> tracks;

        public Playlist() {
            tracks = new ArrayList<String>();
        }

        public void add(String title) {
            tracks.add(title);
        }

        public boolean remove(String title) {
            int idx = tracks.indexOf(title);
            if (idx >= 0) {
                tracks.remove(idx);
                return true;
            }
            return false;
        }

        public int size() {
            return tracks.size();
        }
    }
}
""", r"""public class Solution {
    public static class Playlist {
        private ArrayList<String> tracks;

        public Playlist() {
            tracks = new ArrayList<String>();
        }

        public void add(String title) {
            tracks.add(title);
        }

        public boolean remove(String title) {
            // BUG: removes by INDEX argument even when indexOf returned
            // -1 — drops the LAST track on an absent title
            int idx = tracks.indexOf(title);
            if (idx >= 0) {
                tracks.remove(idx);
                return true;
            }
            tracks.remove(tracks.size() - 1);
            return false;
        }

        public int size() {
            return tracks.size();
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m20", "Checkpoint: the playlist",
    "The full readiness loop: state, first-occurrence search, refusal contract.",
    25,
    r"""
The pattern: the playlist is every skill at once — an ArrayList
field, a mutator, an indexOf-based first-occurrence remover with a
boolean contract, and a derived size. The refusal path must touch
NOTHING. If you traced the state table before coding, you were ready
before you wrote a line — which is the entire point of this course.
""",
    "Điểm kiểm tra: danh sách phát",
    "Vòng sẵn sàng trọn vẹn: trạng thái, tìm lần-đầu-tiên, hợp đồng từ chối.",
    r"""
Mẫu hình: playlist là mọi kỹ năng cùng lúc — một trường ArrayList,
một mutator, một bộ xóa lần-xuất-hiện-đầu-tiên dựa trên indexOf với
hợp đồng boolean, và một size suy ra. Đường từ chối không được đụng
VÀO BẤT CỨ GÌ. Nếu bạn dựng bảng truy vết trạng thái trước khi code,
bạn đã sẵn sàng trước khi viết một dòng — đó chính là mục đích của
cả khóa học.
""",
    CP20C,
    vi_challenge("Điểm kiểm tra: danh sách phát", "Hoàn thiện lớp Playlist theo đặc tả: `add` nối vào; `remove` xóa lần xuất hiện ĐẦU TIÊN của title và trả true (trả false và không đổi gì nếu vắng mặt); `size` trả số bài.",
        [("first occurrence", "indexOf(title), rồi remove(index) nếu >= 0.")]),
    solution=r"""
import java.util.*;

public class Solution {
    public static class Playlist {
        private ArrayList<String> tracks;

        public Playlist() {
            tracks = new ArrayList<String>();
        }

        public void add(String title) {
            tracks.add(title);
        }

        public boolean remove(String title) {
            int idx = tracks.indexOf(title);
            if (idx >= 0) {
                tracks.remove(idx);
                return true;
            }
            return false;
        }

        public int size() {
            return tracks.size();
        }
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public static class Playlist {
        private ArrayList<String> tracks;

        public Playlist() {
            tracks = new ArrayList<String>();
        }

        public void add(String title) {
            tracks.add(title);
        }

        public boolean remove(String title) {
            // BUG: removes by INDEX argument even when indexOf returned
            // -1 — drops the LAST track on an absent title
            int idx = tracks.indexOf(title);
            if (idx >= 0) {
                tracks.remove(idx);
                return true;
            }
            tracks.remove(tracks.size() - 1);
            return false;
        }

        public int size() {
            return tracks.size();
        }
    }
}
""",
)
