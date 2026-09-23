#!/usr/bin/env python3
"""AP CSA M12 — Object-Oriented Design (multiple classes, composition, FRQ 2 shape)."""
from apc import *

M = "apc-oop-design"

L1 = r"""
Real AP FRQ 2 (Class Design) gives you a class with a *comment spec* and a
"complete the constructor/methods" task. Two design ideas carry most of it:

**Composition** — an object holding other objects. A `Club` has a `roster`
of `String`s (or, later, `Member`s):

```java
public class Club {
    private String name;
    private String[] roster;   // an object owns this array
    private int size;          // how many slots are used

    public Club(String clubName, int capacity) {
        name = clubName;
        roster = new String[capacity];
        size = 0;
    }

    public boolean add(String member) {
        if (size >= roster.length) {
            return false;              // full — refuse politely
        }
        roster[size] = member;
        size++;
        return true;
    }
}
```

Note the division of labor: the array is `private`, the outside world only
calls `add`/`size()`/`isFull()`. That is **encapsulation working at design
scale** — invariants ("size never exceeds capacity") are enforced in one
place, the class.

**Object parameters**: methods take object references. `public boolean
contains(String member)` walks `roster[0..size-1]` comparing with
`equals` — remember, only the *used* slots matter, not capacity.
"""

L2 = r"""
A class can own *objects of classes you wrote*. A tiny `Timer` inside a
`Stopwatch`:

```java
public class Stopwatch {
    private int minutes;
    private int seconds;

    public Stopwatch() {
        minutes = 0;
        seconds = 0;
    }

    public void tick() {              // one second passes
        seconds++;
        if (seconds >= 60) {
            seconds = 0;
            minutes++;
        }
    }

    public String toString() {        // AP-style format: M:SS
        return minutes + ":" + String.format("%02d", seconds);
    }
}
```

Two conventions the exam relies on:

- **`toString()`** — every class can define it; concatenation
  (`"" + stopwatch`) calls it automatically. AP FRQ answers frequently end
  with building a `String` and returning it.
- **Constructors calling constructors** — `this(...)` as the first
  statement delegates; overloads stay DRY:

```java
public Point(int x, int y) {
    this.x = x;
    this.y = y;
}

public Point() {
    this(0, 0);       // reuse the main constructor
}
```

**State transitions** are the heart of trace questions: after
`t.tick(); t.tick(); t.tick();` from 0:59, the state is 1:02 — the carry
(`seconds >= 60`) is where students lose points by ticking only one field.
"""

L3 = r"""
Reading a spec is a skill of its own. FRQ wording translates mechanically:

| Spec sentence | Code |
| --- | --- |
| "returns true if..." | `return <condition>;` — no `if` needed |
| "the number of..." | accumulator loop over the data |
| "if it is not possible, return..." | guard clause *first* |
| "helper methods may be called" | use them — the grid of provided helpers is a gift |
| "prepends"/"appends" | order of concatenation: `s + rest` vs `rest + s` |
| "in no particular order" | any order accepted → keep yours simple |

A complete FRQ 2 answer is usually 5–15 lines: the constructor copies
parameters into fields (watch for `this.x = x`), and each method guards,
loops, accumulates, returns. Nothing else.

**Write tests from the spec**, not from your code: every "returns -1 if
absent" sentence is one test case; every boundary in the spec ("between 0
and 100 inclusive") is two more.
"""

write_module(
    M,
    "Object-Oriented Design",
    "Composition, multi-class programs, toString/constructor conventions, spec-to-code translation.",
    "Thiết kế hướng đối tượng",
    "Composition, chương trình nhiều lớp, quy ước toString/hàm dựng, dịch đặc tả thành mã.",
    lessons=["apc-m12-composition", "apc-m12-objects", "apc-m12-specs", "apc-cp-m12"],
    practices=["apc-p12-oop"],
)

write_lesson(
    M, "apc-m12-composition", "Classes that own objects",
    "Composition, private state at design scale, object parameters.",
    14, L1,
    "Lớp sở hữu đối tượng",
    "Composition, trạng thái riêng tư ở tầm thiết kế, tham số đối tượng.",
    r"""
Bài FRQ 2 thật (Class Design) đưa cho bạn một lớp kèm *đặc tả dạng chú
thích* và yêu cầu "hoàn thiện hàm dựng/phương thức". Hai ý tưởng thiết kế
gánh phần lớn việc đó:

**Composition** — một đối tượng chứa các đối tượng khác. Một `Club` có
`roster` gồm `String`:

```java
public class Club {
    private String name;
    private String[] roster;   // đối tượng này sở hữu mảng
    private int size;          // bao nhiêu ô đang dùng

    public Club(String clubName, int capacity) {
        name = clubName;
        roster = new String[capacity];
        size = 0;
    }

    public boolean add(String member) {
        if (size >= roster.length) {
            return false;              // đầy — từ chối khéo léo
        }
        roster[size] = member;
        size++;
        return true;
    }
}
```

Chú ý sự phân công: mảng là `private`, bên ngoài chỉ gọi
`add`/`size()`/`isFull()`. Đó là **encapsulation ở tầm thiết kế** — các bất
biến ("size không vượt quá capacity") được thi hành tại đúng một chỗ, trong
lớp.

**Tham số đối tượng**: phương thức nhận tham chiếu đối tượng.
`public boolean contains(String member)` duyệt `roster[0..size-1]` so bằng
`equals` — nhớ rằng chỉ các ô *đang dùng* mới có nghĩa, không phải capacity.
""",
)

write_lesson(
    M, "apc-m12-objects", "Object state and conventions",
    "toString, constructor delegation with this(...), carry logic in traces.",
    14, L2,
    "Trạng thái đối tượng và quy ước",
    "toString, ủy quyền hàm dựng bằng this(...), logic nhớ trong truy vết.",
    r"""
Một lớp có thể chứa *đối tượng của lớp bạn tự viết*. Một `Stopwatch` nhỏ:

```java
public class Stopwatch {
    private int minutes;
    private int seconds;

    public Stopwatch() {
        minutes = 0;
        seconds = 0;
    }

    public void tick() {              // một giây trôi qua
        seconds++;
        if (seconds >= 60) {
            seconds = 0;
            minutes++;
        }
    }

    public String toString() {        // định dạng kiểu đề thi: M:SS
        return minutes + ":" + String.format("%02d", seconds);
    }
}
```

Hai quy ước đề thị dựa vào:

- **`toString()`** — mọi lớp đều có thể định nghĩa; nối chuỗi
  (`"" + stopwatch`) tự gọi nó. Đáp án FRQ thường kết thúc bằng việc dựng
  một `String` rồi trả về.
- **Hàm dựng gọi hàm dựng** — `this(...)` làm câu lệnh đầu tiên là ủy quyền;
  các overload không lặp mã:

```java
public Point(int x, int y) {
    this.x = x;
    this.y = y;
}

public Point() {
    this(0, 0);       // tái dùng hàm dựng chính
}
```

**Chuyển đổi trạng thái** là trái tim của câu truy vết: sau
`t.tick(); t.tick(); t.tick();` từ 0:59, trạng thái là 1:02 — phép nhớ
(`seconds >= 60`) chính là chỗ thí sinh mất điểm vì chỉ tích một trường.
""",
)

write_lesson(
    M, "apc-m12-specs", "From spec to code",
    "Mechanical translation of FRQ spec sentences, guard-first structure.",
    10, L3,
    "Từ đặc tả thành mã",
    "Dịch cơ học các câu đặc tả FRQ, cấu trúc chặn-trước.",
    r"""
Đọc đặc tả là một kỹ năng riêng. Cách diễn đạt FRQ dịch cơ học:

| Câu đặc tả | Mã |
| --- | --- |
| "trả về true nếu..." | `return <điều kiện>;` — không cần `if` |
| "số lượng..." | vòng lặp tích lũy trên dữ liệu |
| "nếu không thể, trả về..." | mệnh đề chặn *đầu tiên* |
| "có thể gọi phương thức trợ giúp" | hãy dùng — bảng helper được cung cấp là quà |
| "nối vào trước"/"nối vào sau" | thứ tự nối: `s + rest` so với `rest + s` |
| "theo thứ tự bất kỳ" | thứ tự nào cũng được → chọn cách đơn giản nhất của bạn |

Một đáp án FRQ 2 hoàn chỉnh thường 5–15 dòng: hàm dựng chép tham số vào
trường (chú ý `this.x = x`), mỗi phương thức chặn, lặp, tích lũy, trả về.
Không gì khác.

**Viết test từ đặc tả**, không phải từ mã của bạn: mỗi câu "trả về -1 nếu
không có" là một test; mọi biên trong đặc tả ("từ 0 đến 100 bao gồm cả hai
đầu") là thêm hai test nữa.
""",
)

BOILER_TICK = r"""public class Solution {
    public static class Stopwatch {
        public Stopwatch() {
        }

        public void tick() {
        }

        public String toString() {
            return "";
        }
    }
}
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

BOILER_PAIR = r"""public class Solution {
    public static class Point {
        public Point(int x, int y) {
        }

        public Point() {
        }

        public int getX() {
            return 0;
        }

        public int getY() {
            return 0;
        }
    }
}
"""

BOILER_SPEC = r"""public class Solution {
    public static class Song {
        // Spec: constructor stores (title, seconds). duration() returns the
        // length formatted as M:SS with two digits for seconds. Longer songs
        // (more seconds) return true from isLongerThan(Song other).
        public Song(String title, int seconds) {
        }

        public String duration() {
            return "";
        }

        public boolean isLongerThan(Song other) {
            return false;
        }
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static class Register {
        private int items;
        private int total;

        public Register() {
            items = 0;
            total = 0;
        }

        public void scan(int price) {
            // BUG: price is added, but items is never incremented
            total = total + price;
        }

        public void undo(int price) {
            // BUG: removes the price even when the register is empty,
            // letting total go negative
            total = total - price;
            items--;
        }

        public int total() {
            return total;
        }

        public int items() {
            return items;
        }
    }
}
"""

CP12 = r"""public class Solution {
    public static class Locker {
        // Design a Locker with: a private int capacity, a private String[]
        // contents (created in the constructor with the given capacity),
        // a private int size. Methods: add(item) places into the first free
        // slot and returns true, or returns false when full;
        // remove(item) removes one matching item, shifts nothing, returns
        // true if found; count() returns occupied slots; isFull().
        public Locker(int capacity) {
        }

        public boolean add(String item) {
            return false;
        }

        public boolean remove(String item) {
            return false;
        }

        public int count() {
            return 0;
        }

        public boolean isFull() {
            return false;
        }
    }
}
"""

P_TICK = challenge(
    "apc-m12-stopwatch",
    "Build a Stopwatch",
    "Implement the `Stopwatch` nested class: `tick()` advances one second with correct carry into minutes; `toString()` returns `M:SS` (minutes plain, seconds zero-padded to two digits).",
    BOILER_TICK,
    [(
        "carry and format",
        r"""
Solution.Stopwatch s = new Solution.Stopwatch();
CjTestBase.checkEq(s.toString(), "0:00", "fresh");
s.tick(); s.tick(); s.tick();
CjTestBase.checkEq(s.toString(), "0:03", "three ticks");
for (int i = 0; i < 58; i++) { s.tick(); }
CjTestBase.checkEq(s.toString(), "1:01", "crossed the minute");
""",
        "The carry fires when seconds reaches 60 — reset to 0, minutes +1.",
    )],
    level="imitation",
)

P_PARK = challenge(
    "apc-m12-parking",
    "Parking lot state machine",
    "Implement the `Parking` nested class: constructor stores capacity and creates state; `arrive(plate)` adds the plate if not already present and not full (true/false); `depart(plate)` removes it if present; `count()` returns occupied spots.",
    BOILER_PARK,
    [(
        "state machine",
        r"""
Solution.Parking p = new Solution.Parking(2);
CjTestBase.checkEq(p.count(), 0, "empty");
CjTestBase.checkEq(p.arrive("29A"), true, "first car");
CjTestBase.checkEq(p.arrive("29A"), false, "duplicate refused");
CjTestBase.checkEq(p.arrive("51B"), true, "second car");
CjTestBase.checkEq(p.arrive("77C"), false, "full");
CjTestBase.checkEq(p.depart("29A"), true, "leave");
CjTestBase.checkEq(p.depart("00X"), false, "never parked");
CjTestBase.checkEq(p.count(), 1, "one remains");
CjTestBase.checkEq(p.arrive("77C"), true, "spot freed");
""",
        "Track a used-size, scan only 0..size-1, compact on depart.",
    )],
    level="guided",
)

P_PAIR = challenge(
    "apc-m12-point",
    "Constructor delegation",
    "Implement the `Point` nested class: the two-arg constructor stores x and y; the no-arg constructor must call `this(0, 0)` (delegation, not duplication); both getters return the fields.",
    BOILER_PAIR,
    [(
        "delegation",
        r"""
Solution.Point a = new Solution.Point(3, 4);
Solution.Point b = new Solution.Point();
CjTestBase.checkEq(a.getX(), 3, "stored x");
CjTestBase.checkEq(b.getX(), 0, "delegated default");
CjTestBase.checkEq(b.getY(), 0, "delegated default");
""",
        "this(0, 0); must be the FIRST statement of the no-arg constructor.",
    )],
    level="imitation",
)

P_SPEC = challenge(
    "apc-m12-song-spec",
    "Implement from a spec (FRQ 2 style)",
    "Read the comment spec in the boilerplate and implement `Song` exactly: constructor stores both fields; `duration()` formats M:SS; `isLongerThan` compares stored seconds (strictly greater). Do not add public members.",
    BOILER_SPEC,
    [(
        "spec fidelity",
        r"""
Solution.Song a = new Solution.Song("River", 63);
Solution.Song b = new Solution.Song("Echo", 59);
Solution.Song c = new Solution.Song("Dune", 61);
CjTestBase.checkEq(a.duration(), "1:03", "zero-padded");
CjTestBase.checkEq(b.duration(), "0:59", "no padding needed");
CjTestBase.checkEq(a.isLongerThan(b), true, "63 > 59");
CjTestBase.checkEq(b.isLongerThan(c), false, "59 < 61");
""",
        "String.format(\"%02d\", seconds) — and compare the stored field, not the string.",
    )],
    level="independent",
)

P_FIX = challenge(
    "apc-m12-fix-register",
    "Debug the Register class",
    "This cash-register class corrupts its state: scan() forgets to count items, and undo() drives the total negative when the register is empty. Trace two scans and one undo, fix both defects (signatures stay the same).",
    BOILER_FIX,
    [(
        "state repaired",
        r"""
Solution.Register r = new Solution.Register();
r.scan(200); r.scan(75);
CjTestBase.checkEq(r.total(), 275, "sum");
CjTestBase.checkEq(r.items(), 2, "counted");
r.undo(75);
CjTestBase.checkEq(r.total(), 200, "undone");
CjTestBase.checkEq(r.items(), 1, "count decremented");
r.undo(200);
r.undo(10);
CjTestBase.checkEq(r.total(), 0, "never negative on empty");
CjTestBase.checkEq(r.items(), 0, "never negative on empty");
""",
        "undo must guard first: if items == 0, do nothing.",
    )],
    level="debugging",
)

CP12C = challenge(
    "apc-cp-m12-locker",
    "Checkpoint: design a Locker",
    "Implement the full `Locker` nested class from its comment spec: fixed capacity, first-free-slot add, remove by value (no compaction required), count, isFull. All state private.",
    CP12,
    [(
        "full design",
        r"""
Solution.Locker l = new Solution.Locker(3);
CjTestBase.checkEq(l.count(), 0, "fresh");
CjTestBase.checkEq(l.add("jacket"), true, "add 1");
CjTestBase.checkEq(l.add("helmet"), true, "add 2");
CjTestBase.checkEq(l.add("bag"), true, "add 3");
CjTestBase.checkEq(l.add("shoes"), false, "full");
CjTestBase.checkEq(l.isFull(), true, "isFull agrees");
CjTestBase.checkEq(l.remove("helmet"), true, "middle removal");
CjTestBase.checkEq(l.remove("helmet"), false, "already gone");
CjTestBase.checkEq(l.count(), 2, "two remain");
CjTestBase.checkEq(l.add("shoes"), true, "slot freed");
CjTestBase.checkEq(l.count(), 3, "full again");
""",
        "remove scans for the first equal item and nulls that slot.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p12-oop", "Design reps", "State machines, delegation, spec fidelity, class debugging.",
    "Luyện thiết kế", "Máy trạng thái, ủy quyền, bám đặc tả, gỡ lỗi lớp.",
    after_lesson="apc-m12-specs", minutes=60, difficulty="beginner",
    challenges=[P_TICK, P_PARK, P_PAIR, P_SPEC, P_FIX],
    vi_challenges={
        "apc-m12-stopwatch": vi_challenge("Dựng đồng hồ bấm giây", "Cài đặt lớp lồng `Stopwatch`: `tick()` tăng một giây với phép nhớ đúng vào phút; `toString()` trả về `M:SS` (phút để nguyên, giây đệm không tới hai chữ số).",
            [("carry and format", "Phép nhớ kích khi giây đạt 60 — reset về 0, phút +1.")]),
        "apc-m12-parking": vi_challenge("Máy trạng thái bãi xe", "Cài đặt lớp lồng `Parking`: hàm dựng lưu capacity và tạo trạng thái; `arrive(plate)` thêm biển số nếu chưa có và chưa đầy (true/false); `depart(plate)` xóa nếu có; `count()` trả số chỗ đã chiếm.",
            [("state machine", "Theo dõi một used-size, chỉ quét 0..size-1, dồn khi depart.")]),
        "apc-m12-point": vi_challenge("Ủy quyền hàm dựng", "Cài đặt lớp lồng `Point`: hàm dựng hai tham số lưu x và y; hàm dựng không tham số phải gọi `this(0, 0)` (ủy quyền, không nhân bản mã); các getter trả về trường.",
            [("delegation", "this(0, 0); phải là câu lệnh ĐẦU TIÊN của hàm dựng không tham số.")]),
        "apc-m12-song-spec": vi_challenge("Cài từ đặc tả (kiểu FRQ 2)", "Đọc đặc tả chú thích trong boilerplate và cài `Song` chính xác: hàm dựng lưu cả hai trường; `duration()` định dạng M:SS; `isLongerThan` so giây đã lưu (lớn hơn ngặt). Không thêm thành viên public.",
            [("spec fidelity", "String.format(\"%02d\", seconds) — và so trường đã lưu, không phải chuỗi.")]),
        "apc-m12-fix-register": vi_challenge("Gỡ lỗi lớp Register", "Lớp máy thu ngân này làm hỏng trạng thái: scan() quên đếm món, còn undo() đẩy tổng âm khi máy rỗng. Truy vết hai lần quét và một lần undo, sửa cả hai khuyết tật (chữ ký giữ nguyên).",
            [("state repaired", "undo phải chặn trước: nếu items == 0, không làm gì.")]),
    },
    solutions=[
        ("apc-m12-stopwatch", r"""public class Solution {
    public static class Stopwatch {
        private int minutes;
        private int seconds;

        public Stopwatch() {
            minutes = 0;
            seconds = 0;
        }

        public void tick() {
            seconds++;
            if (seconds >= 60) {
                seconds = 0;
                minutes++;
            }
        }

        public String toString() {
            return minutes + ":" + String.format("%02d", seconds);
        }
    }
}
""",
         r"""public class Solution {
    public static class Stopwatch {
        // BUG: no carry — minutes never advance past 59 seconds
        private int minutes;
        private int seconds;

        public Stopwatch() {
            minutes = 0;
            seconds = 0;
        }

        public void tick() {
            seconds++;
            if (seconds == 100) {
                seconds = 0;
                minutes++;
            }
        }

        public String toString() {
            return minutes + ":" + String.format("%02d", seconds);
        }
    }
}
"""),
        ("apc-m12-parking", r"""public class Solution {
    public static class Parking {
        private String[] spots;
        private int size;

        public Parking(int capacity) {
            spots = new String[capacity];
            size = 0;
        }

        public boolean arrive(String plate) {
            if (size >= spots.length) {
                return false;
            }
            for (int i = 0; i < size; i++) {
                if (spots[i].equals(plate)) {
                    return false;
                }
            }
            spots[size] = plate;
            size++;
            return true;
        }

        public boolean depart(String plate) {
            for (int i = 0; i < size; i++) {
                if (spots[i].equals(plate)) {
                    spots[i] = spots[size - 1];
                    spots[size - 1] = null;
                    size--;
                    return true;
                }
            }
            return false;
        }

        public int count() {
            return size;
        }
    }
}
""",
         r"""public class Solution {
    public static class Parking {
        private String[] spots;
        private int size;

        public Parking(int capacity) {
            spots = new String[capacity];
            size = 0;
        }

        public boolean arrive(String plate) {
            // BUG: duplicates accepted — never checks presence
            if (size >= spots.length) {
                return false;
            }
            spots[size] = plate;
            size++;
            return true;
        }

        public boolean depart(String plate) {
            // BUG: leaves a null hole and never shrinks size
            for (int i = 0; i < spots.length; i++) {
                if (spots[i] != null && spots[i].equals(plate)) {
                    spots[i] = null;
                    return true;
                }
            }
            return false;
        }

        public int count() {
            return size;
        }
    }
}
"""),
        ("apc-m12-point", r"""public class Solution {
    public static class Point {
        private int x;
        private int y;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public Point() {
            this(0, 0);
        }

        public int getX() {
            return x;
        }

        public int getY() {
            return y;
        }
    }
}
""",
         r"""public class Solution {
    public static class Point {
        private int x;
        private int y;

        public Point(int x, int y) {
            // BUG: constructor parameter shadowing without this. —
            // fields never receive the arguments
            x = x;
            y = y;
        }

        public Point() {
            this(0, 0);
        }

        public int getX() {
            return x;
        }

        public int getY() {
            return y;
        }
    }
}
"""),
        ("apc-m12-song-spec", r"""public class Solution {
    public static class Song {
        private String title;
        private int seconds;

        public Song(String title, int seconds) {
            this.title = title;
            this.seconds = seconds;
        }

        public String duration() {
            return (seconds / 60) + ":" + String.format("%02d", seconds % 60);
        }

        public boolean isLongerThan(Song other) {
            return seconds > other.seconds;
        }
    }
}
""",
         r"""public class Solution {
    public static class Song {
        private String title;
        private int seconds;

        public Song(String title, int seconds) {
            this.title = title;
            this.seconds = seconds;
        }

        public String duration() {
            // BUG: seconds not zero-padded and not taken mod 60
            return (seconds / 60) + ":" + seconds;
        }

        public boolean isLongerThan(Song other) {
            return seconds > other.seconds;
        }
    }
}
"""),
        ("apc-m12-fix-register", r"""public class Solution {
    public static class Register {
        private int items;
        private int total;

        public Register() {
            items = 0;
            total = 0;
        }

        public void scan(int price) {
            total = total + price;
            items++;
        }

        public void undo(int price) {
            if (items == 0) {
                return;
            }
            total = total - price;
            items--;
        }

        public int total() {
            return total;
        }

        public int items() {
            return items;
        }
    }
}
""",
         r"""public class Solution {
    public static class Register {
        // BUG: original flaws kept — scan never counts, undo goes negative
        private int items;
        private int total;

        public Register() {
            items = 0;
            total = 0;
        }

        public void scan(int price) {
            total = total + price;
        }

        public void undo(int price) {
            total = total - price;
            items--;
        }

        public int total() {
            return total;
        }

        public int items() {
            return items;
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m12", "Checkpoint: design a class",
    "A complete multi-method class from a comment spec (FRQ 2 rehearsal).",
    25,
    r"""
This is the FRQ 2 rehearsal: one class, four methods, every invariant
enforced inside. Read the spec twice before typing; the tests are derived
from the spec sentences.
""",
    "Điểm kiểm tra: thiết kế một lớp",
    "Một lớp hoàn chỉnh nhiều phương thức từ đặc tả chú thích (diễn tập FRQ 2).",
    r"""
Đây là diễn tập FRQ 2: một lớp, bốn phương thức, mọi bất biến được thi hành
bên trong. Đọc đặc tả hai lần trước khi gõ; các test được suy ra từ các câu
đặc tả.
""",
    CP12C,
    vi_challenge("Điểm kiểm tra: thiết kế một lớp", "Cài đặt lớp lồng `Locker` đầy đủ từ đặc tả chú thích: capacity cố định, add vào ô trống đầu tiên, remove theo giá trị (không cần dồn), count, isFull. Toàn bộ trạng thái private.",
        [("full design", "remove quét phần tử bằng nhau đầu tiên và gán ô đó thành null.")]),
    solution=r"""public class Solution {
    public static class Locker {
        private String[] contents;
        private int size;

        public Locker(int capacity) {
            contents = new String[capacity];
            size = 0;
        }

        public boolean add(String item) {
            if (size >= contents.length) {
                return false;
            }
            contents[size] = item;
            size++;
            return true;
        }

        public boolean remove(String item) {
            for (int i = 0; i < size; i++) {
                if (contents[i].equals(item)) {
                    contents[i] = null;
                    for (int j = i; j < size - 1; j++) {
                        contents[j] = contents[j + 1];
                    }
                    contents[size - 1] = null;
                    size--;
                    return true;
                }
            }
            return false;
        }

        public int count() {
            return size;
        }

        public boolean isFull() {
            return size == contents.length;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Locker {
        // BUG: size tracks total adds, not occupied slots — count drifts up
        private String[] contents;
        private int size;

        public Locker(int capacity) {
            contents = new String[capacity];
            size = 0;
        }

        public boolean add(String item) {
            if (size >= contents.length) {
                return false;
            }
            for (int i = 0; i < contents.length; i++) {
                if (contents[i] == null) {
                    contents[i] = item;
                    size++;
                    return true;
                }
            }
            return false;
        }

        public boolean remove(String item) {
            for (int i = 0; i < contents.length; i++) {
                if (contents[i] != null && contents[i].equals(item)) {
                    contents[i] = null;
                    return true;
                }
            }
            return false;
        }

        public int count() {
            return size;
        }

        public boolean isFull() {
            return size == contents.length;
        }
    }
}
""",
)
