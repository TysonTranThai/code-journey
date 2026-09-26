#!/usr/bin/env python3
"""AP CSA Advanced M8 — Advanced OOP: object state across calls (verified)."""
from apx import *

M = "apx-oop"

write_module(
    M,
    "Advanced Object-Oriented Problems",
    "State machines as classes: capacity rules, helper methods, encapsulated mutation, and multi-step interactions. Difficulty E3–E5.",
    "Bài toán hướng đối tượng nâng cao",
    "Máy trạng thái dưới dạng lớp: luật dung tích, phương thức trợ giúp, biến đổi đóng gói, và tương tác nhiều bước. Độ khó E3–E5.",
    lessons=["apx-m8-state", "apx-m8-helpers", "apx-m8-interaction", "apx-cp-m8"],
    practices=["apx-p8-oop"],
)

L1 = r"""
An object is a **state machine**: fields are the state, methods are
transitions, constructors set the start state. Exam FRQs hide a
state machine behind a story (parking garage, scoreboard, vending
machine), and the rubric cares about exactly three things:

1. **The transition rule is the whole problem.** `arrive` returns
   false when full — one comparison decides three test cases.
2. **Order of checks** matters: is a duplicate plate rejected before
   or after the capacity check? The spec's sentence order is the
   check order.
3. **Derived state** (`count()`, `isFull()`) must be computed from
   the real state, never stored twice — a second copy of the truth
   will drift.

The classic FRQ2 shape: constructor stores parameters (with `this.`),
one boolean-returning transition with a guard, one mutator that
reaches a boundary (`depart` on empty → false), and one accessor.
Every graded behavior is one of those four.
"""

L2 = r"""
**Helpers are the rubric's favorite.** A private helper that
normalizes, validates, or classifies turns a sprawling method into
three clean calls — and the FRQ rubric *names* helper usage as a
point. Design rule: if a piece of logic would be repeated in two
methods, it becomes a helper.

```java
private boolean isValid(String code) {
    return code.length() == 4 && code.charAt(0) == 'X';
}
```

Watch the **constructor traps**: shadowing (`price = price`), a
field initialized twice, or a constructor that forgets one field —
leaving it at a silent default that poisons every later method call.
Trace constructors like any other code: list every field and its
value after the constructor returns.

**Object interaction**: when one object holds another (a Register
holding a Drawer), the outer object's method calls the inner one's —
and null is always a state. "Nothing registered yet" usually means
"a null inner object," and the first transition must guard it.
"""

L3 = r"""
**Designing from a spec.** The exam hands you a class diagram or a
prose spec; your implementation is graded behavior-by-behavior. The
workflow:

1. **List the fields** with types (from "the register tracks..." —
   a count? a list? a total?).
2. **One method per bullet** in the spec; do not invent extras the
   spec did not name (the rubric cannot award them).
3. **State the guard** for each transition in one sentence before
   coding ("arrive fails when full OR plate already present").
4. **Order of events**: a scoreboard that processes a foul then a
   goal is a different state than goal-then-foul only if the spec
   says order matters — decide, then code.

And the testing discipline: after implementing, drive every
transition to every boundary — full, empty, duplicate, missing —
because the hidden tests were written by someone who thought of
them first.
"""

VI_L1 = r"""
Một đối tượng là một **máy trạng thái**: trường là trạng thái,
phương thức là bước chuyển, constructor đặt trạng thái khởi đầu.
FRQ đề thi giấu một máy trạng thái sau một câu chuyện (bãi đỗ xe,
bảng điểm, máy bán hàng), và bảng điểm quan tâm đúng ba điều:

1. **Luật chuyển trạng thái là toàn bộ bài toán.** `arrive` trả false
   khi đầy — một phép so sánh quyết định ba test case.
2. **Thứ tự kiểm tra** quan trọng: vé trùng bị chặn trước hay sau phép
   kiểm tra dung tích? Thứ tự câu trong đặc tả là thứ tự kiểm tra.
3. **Trạng thái suy ra** (`count()`, `isFull()`) phải được tính từ
   trạng thái thật, không bao giờ lưu bản sao — bản sao thứ hai của
   sự thật sẽ lệch.

Hình dạng FRQ2 kinh điển: constructor lưu tham số (với `this.`), một
bước chuyển trả boolean có biến chặn, một bộ biến đổi chạm biên
(`depart` khi rỗng → false), và một accessor. Mọi hành vi được chấm
đều là một trong bốn cái đó.
"""

VI_L2 = r"""
**Phương thức trợ giúp là mục ưa thích của bảng điểm.** Một helper
private chuẩn hóa, kiểm tra, hoặc phân loại biến một phương thức dài
thành ba lời gọi sạch — và bảng điểm FRQ *nêu tên* việc dùng helper
là một điểm. Luật thiết kế: nếu một đoạn logic sẽ lặp lại trong hai
phương thức, nó trở thành helper.

```java
private boolean isValid(String code) {
    return code.length() == 4 && code.charAt(0) == 'X';
}
```

Chú ý các **bẫy constructor**: bóng che (`price = price`), một trường
được khởi tạo hai lần, hoặc constructor quên một trường — để nó ở giá
trị mặc định âm thầm đầu độc mọi lời gọi sau. Hãy truy vết constructor
như bất kỳ mã nào khác: liệt kê từng trường và giá trị của nó sau khi
constructor trả về.

**Tương tác đối tượng**: khi một đối tượng giữ đối tượng khác (một
Register giữ một Drawer), phương thức của đối tượng ngoài gọi đối
tượng trong — và null luôn là một trạng thái. "Chưa đăng ký gì" thường
nghĩa là "đối tượng trong là null", và bước chuyển đầu tiên phải chặn
nó.
"""

VI_L3 = r"""
**Thiết kế từ đặc tả.** Đề thi đưa bạn sơ đồ lớp hoặc đặc tả văn
xuất; bản cài đặt được chấm theo từng hành vi. Quy trình:

1. **Liệt kê các trường** với kiểu (từ "máy thu ngân ghi nhận..." —
   một con đếm? một danh sách? một tổng?).
2. **Mỗi gạch đầu dòng một phương thức**; không chế phương thức ngoài
   đặc tả (bảng điểm không thể chấm điểm cho chúng).
3. **Nêu biến chặn** cho mỗi bước chuyển trong một câu trước khi viết
   ("arrive thất bại khi đầy HOẶC biển số đã có").
4. **Thứ tự sự kiện**: bảng điểm xử lý lỗi rồi ghi điểm khác với
   ghi-điểm-rồi-lỗi chỉ khi đặc tả nói thứ tự quan trọng — quyết định,
   rồi viết mã.

Và kỷ luật kiểm thử: sau khi cài đặt, đưa mọi bước chuyển tới mọi
biên — đầy, rỗng, trùng, thiếu — vì những test ẩn được viết bởi người
đã nghĩ đến chúng trước bạn.
"""

BOILER_PARK = r"""public class Solution {
    public static class Parking {
        public Parking(int capacity) {
        }

        public boolean arrive(String plate) {
            return false;
        }

        public boolean depart(String plate) {
            return false;
        }

        public int count() {
            return 0;
        }
    }
}
"""

BOILER_REG = r"""public class Solution {
    public static class Register {
        public Register() {
        }

        public void scan(int price) {
        }

        public void pay(int cash) {
        }

        public int changeDue() {
            return 0;
        }
    }
}
"""

BOILER_SCORE = r"""public class Solution {
    public static class Scoreboard {
        public Scoreboard(String home, String away) {
        }

        public void score(String team, int points) {
        }

        public void foul(String team) {
        }

        public String leader() {
            return "";
        }
    }
}
"""

P_PARK = challenge(
    "apx-m8-parking",
    "The parking gate state machine",
    "Implement the `Parking` class: constructor takes the **capacity**. "
    "`arrive(plate)` adds the plate and returns true, unless the lot is "
    "**full** — then return false and change nothing. `depart(plate)` "
    "removes the plate and returns true, or returns false if the plate "
    "is not parked. `count()` returns the number of parked cars. Use an "
    "ArrayList<String>.",
    BOILER_PARK,
    [(
        "gate transitions",
        r"""
Solution.Parking p = new Solution.Parking(2);
CjTestBase.checkTrue(p.arrive("AA"), "first car fits");
CjTestBase.checkTrue(p.arrive("BB"), "second car fits");
CjTestBase.checkTrue(!p.arrive("CC"), "full lot rejects");
CjTestBase.checkEq(p.count(), 2, "count unchanged after reject");
CjTestBase.checkTrue(p.depart("BB"), "parked car leaves");
CjTestBase.checkTrue(!p.depart("BB"), "departing again fails");
CjTestBase.checkEq(p.count(), 1, "one car remains");
""",
        "arrive guards on size >= capacity; depart uses remove(plate) which already returns the boolean.",
    )],
    level="independent",
    difficulty="advanced",
)

P_REG = challenge(
    "apx-m8-register",
    "The register with a running balance",
    "Implement the `Register` class (a checkout register). `scan(price)` "
    "adds to the amount owed. `pay(cash)` records cash received — the "
    "register accepts payment **larger than owed** (change is owed "
    "back). `changeDue()` returns how much change the customer must "
    "receive (cash received minus amount owed, never negative; 0 "
    "while still owing). The register starts empty.",
    BOILER_REG,
    [(
        "balance transitions",
        r"""
Solution.Register r = new Solution.Register();
r.scan(300);
r.scan(120);
CjTestBase.checkEq(r.changeDue(), 0, "still owing");
r.pay(250);
CjTestBase.checkEq(r.changeDue(), 0, "partially paid");
r.pay(400);
CjTestBase.checkEq(r.changeDue(), 230, "overpaid: change due");
r.pay(50);
CjTestBase.checkEq(r.changeDue(), 280, "extra payment adds to change");
""",
        "Track owed and paid separately; changeDue = max(0, paid - owed).",
    )],
    level="combination",
    difficulty="advanced",
)

P_SCORE = challenge(
    "apx-m8-scoreboard",
    "The scoreboard with fouls",
    "Implement the `Scoreboard` class: constructor stores both team "
    "names. `score(team, points)` adds points to that team (ignore "
    "unknown team names). `foul(team)` records a foul for that team; "
    "when a team reaches **5 fouls**, the opponent immediately gains 2 "
    "bonus points (the 6th foul does nothing extra). `leader()` returns "
    "the leading team's name, or the **home** team's name on a tie.",
    BOILER_SCORE,
    [(
        "score and foul transitions",
        r"""
Solution.Scoreboard s = new Solution.Scoreboard("Hawks", "Owls");
s.score("Owls", 3);
for (int i = 0; i < 5; i++) {
    s.foul("Owls");
}
s.score("Hawks", 2);
CjTestBase.checkTrue(s.leader().equals("Hawks"), "Hawks 4 vs Owls 3 (bonus went to the opponent)");
s.score("Referee", 99);
CjTestBase.checkTrue(s.leader().equals("Hawks"), "unknown team ignored");
""",
        "Owls foul 5 times → HAWKS gain exactly one +2 bonus (Hawks 2), then score 2 more (4) to lead 4-3. A bonus paid to the fouling team leaves Hawks at 2 and Owls ahead.",
    )],
    level="real-world",
    difficulty="advanced",
)

CP8 = challenge(
    "apx-cp-m8-locker",
    "Checkpoint: the locker room",
    "Implement the `Locker` class: constructor takes the number of "
    "lockers. `claim(name)` assigns the **lowest-numbered free locker** "
    "to name and returns the locker number (1-based), or -1 when full. "
    "`release(num)` frees that locker (silently ignoring invalid or "
    "already-free numbers). `owner(num)` returns the current owner's "
    "name or null. Use an array of String.",
    r"""public class Solution {
    public static class Locker {
        public Locker(int size) {
        }

        public int claim(String name) {
            return -1;
        }

        public void release(int num) {
        }

        public String owner(int num) {
            return null;
        }
    }
}
""",
    [(
        "locker lifecycle",
        r"""
Solution.Locker l = new Solution.Locker(3);
CjTestBase.checkEq(l.claim("Ann"), 1, "first claim gets 1");
CjTestBase.checkEq(l.claim("Bob"), 2, "second claim gets 2");
l.release(1);
CjTestBase.checkEq(l.claim("Cat"), 1, "lowest free is reused");
CjTestBase.checkTrue(l.owner(3) == null, "locker 3 still free");
CjTestBase.checkEq(l.owner(2), "Bob", "Bob still holds 2");
""",
        "Scan 0..size-1 for the first free slot; null marks free; validate num bounds in release/owner.",
    )],
    level="real-world",
    difficulty="advanced",
)

VI_CP8 = vi_challenge(
    "Điểm kiểm tra: phòng tủ đồ",
    "Cài đặt lớp `Locker`: constructor nhận số lượng tủ. `claim(name)` "
    "gán **tủ trống số nhỏ nhất** cho name và trả về số tủ (đánh số từ "
    "1), hoặc -1 khi đầy. `release(num)` giải phóng tủ đó (bỏ qua im "
    "lặng số không hợp lệ hoặc đã trống). `owner(num)` trả về tên người "
    "đang giữ hoặc null. Dùng mảng String.",
    [("locker lifecycle", "Quét 0..size-1 tìm ô trống đầu tiên; null đánh dấu trống; kiểm tra biên num trong release/owner.")],
)

write_practice(
    M, "apx-p8-oop", "State machine lab",
    "Three class designs driven to every boundary; state transitions are the whole exam.",
    "Phòng thí nghiệm máy trạng thái",
    "Ba thiết kế lớp được đưa tới mọi biên; bước chuyển trạng thái là toàn bộ đề thi.",
    after_lesson="apx-m8-interaction", minutes=65, difficulty="advanced",
    challenges=[P_PARK, P_REG, P_SCORE],
    vi_challenges={
        "apx-m8-parking": vi_challenge(
            "Máy trạng thái cổng bãi đỗ xe",
            "Cài đặt lớp `Parking`: constructor nhận **dung tích**. "
            "`arrive(plate)` thêm biển số và trả true, trừ khi bãi **đầy** — "
            "khi đó trả false và không đổi gì. `depart(plate)` xóa biển số và "
            "trả true, hoặc trả false nếu biển số không có trong bãi. "
            "`count()` trả số xe đang đỗ. Dùng ArrayList<String>.",
            [("gate transitions", "arrive chặn khi size >= capacity; depart dùng remove(plate) vốn đã trả boolean.")],
        ),
        "apx-m8-register": vi_challenge(
            "Máy thu ngân với số dư chạy",
            "Cài đặt lớp `Register` (máy thu ngân). `scan(price)` cộng vào số "
            "tiền khách nợ. `pay(cash)` ghi nhận tiền khách trả — máy chấp "
            "nhận khoản trả **lớn hơn số nợ** (phải trả lại tiền thừa). "
            "`changeDue()` trả số tiền thừa phải trả lại khách (tiền đã nhận "
            "trừ số nợ, không bao giờ âm; 0 khi còn nợ). Máy khởi đầu trống.",
            [("balance transitions", "Theo dõi nợ và đã-trả riêng biệt; changeDue = max(0, đãTrả - nợ).")],
        ),
        "apx-m8-scoreboard": vi_challenge(
            "Bảng điểm với lỗi phá luật",
            "Cài đặt lớp `Scoreboard`: constructor lưu tên hai đội. "
            "`score(team, points)` cộng điểm cho đội đó (bỏ qua tên đội lạ). "
            "`foul(team)` ghi một lỗi cho đội; khi đội chạm **5 lỗi**, đội "
            "bên kia ngay lập tức được cộng 2 điểm thưởng (lỗi thứ 6 không "
            "thêm gì). `leader()` trả tên đội đang dẫn trước, hoặc tên đội "
            "**home** khi hòa.",
            [("score and foul transitions", "Bộ đếm lỗi theo từng đội; ở lỗi thứ 5 thưởng cho đối thủ 2 điểm. leader() phân xử hòa về home.")],
        ),
    },
    solutions=[
        ("apx-m8-parking", r"""public class Solution {
    public static class Parking {
        private int capacity;
        private java.util.ArrayList<String> plates = new java.util.ArrayList<String>();

        public Parking(int capacity) {
            this.capacity = capacity;
        }

        public boolean arrive(String plate) {
            if (plates.size() >= capacity) {
                return false;
            }
            plates.add(plate);
            return true;
        }

        public boolean depart(String plate) {
            return plates.remove(plate);
        }

        public int count() {
            return plates.size();
        }
    }
}
""", r"""public class Solution {
    public static class Parking {
        private int capacity;
        private java.util.ArrayList<String> plates = new java.util.ArrayList<String>();

        public Parking(int capacity) {
            this.capacity = capacity;
        }

        public boolean arrive(String plate) {
            if (plates.size() >= capacity) {
                return false;
            }
            plates.add(plate);
            return true;
        }

        public boolean depart(String plate) {
            // BUG: removes by INDEX semantics confusion — removes first element instead
            if (plates.size() > 0) {
                plates.remove(0);
                return true;
            }
            return false;
        }

        public int count() {
            return plates.size();
        }
    }
}
"""),
        ("apx-m8-register", r"""public class Solution {
    public static class Register {
        private int owed;
        private int paid;

        public Register() {
            owed = 0;
            paid = 0;
        }

        public void scan(int price) {
            owed += price;
        }

        public void pay(int cash) {
            paid += cash;
        }

        public int changeDue() {
            return Math.max(0, paid - owed);
        }
    }
}
""", r"""public class Solution {
    public static class Register {
        private int owed;
        private int paid;

        public Register() {
            owed = 0;
            paid = 0;
        }

        public void scan(int price) {
            owed += price;
        }

        public void pay(int cash) {
            paid += cash;
        }

        public int changeDue() {
            // BUG: forgets the clamp — returns negative while owing
            return paid - owed;
        }
    }
}
"""),
        ("apx-m8-scoreboard", r"""public class Solution {
    public static class Scoreboard {
        private String home;
        private String away;
        private int homeScore;
        private int awayScore;
        private int homeFouls;
        private int awayFouls;

        public Scoreboard(String home, String away) {
            this.home = home;
            this.away = away;
        }

        public void score(String team, int points) {
            if (team.equals(home)) {
                homeScore += points;
            } else if (team.equals(away)) {
                awayScore += points;
            }
        }

        public void foul(String team) {
            if (team.equals(home)) {
                homeFouls++;
                if (homeFouls == 5) {
                    awayScore += 2;
                }
            } else if (team.equals(away)) {
                awayFouls++;
                if (awayFouls == 5) {
                    homeScore += 2;
                }
            }
        }

        public String leader() {
            if (awayScore > homeScore) {
                return away;
            }
            return home;
        }
    }
}
""", r"""public class Solution {
    public static class Scoreboard {
        private String home;
        private String away;
        private int homeScore;
        private int awayScore;
        private int homeFouls;
        private int awayFouls;

        public Scoreboard(String home, String away) {
            this.home = home;
            this.away = away;
        }

        public void score(String team, int points) {
            if (team.equals(home)) {
                homeScore += points;
            } else if (team.equals(away)) {
                awayScore += points;
            }
        }

        public void foul(String team) {
            // BUG: awards the bonus to the FOULING team instead of the opponent
            if (team.equals(home)) {
                homeFouls++;
                if (homeFouls == 5) {
                    homeScore += 2;
                }
            } else if (team.equals(away)) {
                awayFouls++;
                if (awayFouls == 5) {
                    awayScore += 2;
                }
            }
        }

        public String leader() {
            if (awayScore > homeScore) {
                return away;
            }
            return home;
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m8", "Checkpoint: lowest-free allocation",
    "Full class checkpoint: scan for the first free slot, guard the boundaries.",
    25,
    r"""
Allocation problems are state machines plus a search: the state is
"which slots are free," and each transition scans from the start.
The rubric-visible parts are the guard (full → -1), the silent
invalid release, and the null owner.
""",
    "Điểm kiểm tra: cấp phát ô trống thấp nhất",
    "Bài kiểm tra lớp hoàn chỉnh: quét ô trống đầu tiên, chặn các biên.",
    r"""
Bài cấp phát là máy trạng thái cộng một phép tìm kiếm: trạng thái là
"ô nào còn trống", và mỗi bước chuyển quét từ đầu. Các phần nhìn thấy
trên bảng điểm là biến chặn (đầy → -1), release không hợp lệ được bỏ
qua im lặng, và owner trả null.
""",
    CP8,
    VI_CP8,
    solution=r"""public class Solution {
    public static class Locker {
        private String[] slots;

        public Locker(int size) {
            slots = new String[size];
        }

        public int claim(String name) {
            for (int i = 0; i < slots.length; i++) {
                if (slots[i] == null) {
                    slots[i] = name;
                    return i + 1;
                }
            }
            return -1;
        }

        public void release(int num) {
            if (num >= 1 && num <= slots.length) {
                slots[num - 1] = null;
            }
        }

        public String owner(int num) {
            if (num >= 1 && num <= slots.length) {
                return slots[num - 1];
            }
            return null;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Locker {
        private String[] slots;
        private int next;

        public Locker(int size) {
            slots = new String[size];
            next = 0;
        }

        public int claim(String name) {
            // BUG: never reuses freed slots — always bumps next
            if (next >= slots.length) {
                return -1;
            }
            slots[next] = name;
            next++;
            return next;
        }

        public void release(int num) {
            if (num >= 1 && num <= slots.length) {
                slots[num - 1] = null;
            }
        }

        public String owner(int num) {
            if (num >= 1 && num <= slots.length) {
                return slots[num - 1];
            }
            return null;
        }
    }
}
""",
)

print("M8 done")
