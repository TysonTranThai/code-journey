#!/usr/bin/env python3
"""AP CSA Advanced M14 — FRQ class mastery (verified class-design tasks)."""
from apx import *

M = "apx-frq-class"

write_module(
    M,
    "FRQ Class Mastery",
    "Full FRQ2-style class designs: state machines, object interaction, and lifecycle rules read from prose. Difficulty E4–E5.",
    "Làm chủ lớp FRQ",
    "Thiết kế lớp kiểu FRQ2 trọn vẹn: máy trạng thái, tương tác đối tượng, và luật vòng đời đọc từ văn xuôi. Độ khó E4–E5.",
    lessons=["apx-m14-lifecycle", "apx-m14-interaction", "apx-m14-rubric", "apx-cp-m14"],
    practices=["apx-p14-class"],
)

L1 = r"""
Class FRQs are won in the **lifecycle rules** — the sentences that
say when state may change:

- "coins reset to zero when the machine is emptied" → a getter with
  a side effect (`emptyCoins`).
- "a song becomes liked on its FIFTH play" → `== 5`, not `>= 5`
  (the sixth play must do nothing).
- "a player at 0 HP cannot be damaged or healed" → BOTH mutators
  guard on the same condition.
- "restock happens even when empty" → a transition with no guard.

Underline every rule sentence; each one is one `if` (or one
deliberate absence of an `if`). Then implement the class in spec
order — constructor first, transitions next, accessors last — and
re-read the rules against your ifs. A missing guard is invisible in
the happy path; that is why the graders wrote hidden tests for it.
"""

L2 = r"""
**Object interaction** is the FRQ2 finale: a class that HOLDS other
objects and drives them. The two patterns:

- **Delegation loop**: `Library.playAll()` calls `play()` on every
  held Song. The Library stores no play counts itself — the truth
  lives in the held objects, and the Library only *asks*.
- **Aggregation query**: `likedCount()` asks each held object a
  boolean and counts. One accumulator over a for-each.

The design smell to avoid: duplicating a held object's state in the
holder (a Library that also tracks play counts will drift). When
the story says the holder "knows about" the songs, it means it
holds references — not that it copies their fields.

Constructors of holders start empty (`new ArrayList<>()`), and
nothing else happens there — a constructor that *creates* data the
caller should pass in is answering the wrong FRQ.
"""

L3 = r"""
**Reading the rubric into your code.** Every class FRQ rubric has
the same five rows; aim your code at them:

1. **Fields**: correct types, `private`. One field per state
   variable the story names — no more, no less.
2. **Constructor**: every field assigned (parameters via `this.`),
   derived fields computed, nothing invented.
3. **Transitions**: each mutator implements exactly its rule
   sentence, guards included.
4. **Accessors**: computed from state on demand, no caching
   duplicates.
5. **No extra public API**: methods the story never named cannot
   earn points and can leak state.

Time plan for a 9-point class FRQ: 3 minutes reading/marking rules,
4 minutes writing fields+constructor, 8 minutes transitions,
3 minutes accessors, 2 minutes rule audit. The audit finds the
missing guard — the single most common lost point.
"""

VI_L1 = r"""
Bài FRQ lớp được giành trong các **luật vòng đời** — những câu nói
khi nào trạng thái được phép đổi:

- "xu được về 0 khi máy được rút trống" → một getter có tác dụng phụ
  (`emptyCoins`).
- "một bài hát được thích ở lượt chơi THỨ NĂM" → `== 5`, không phải
  `>= 5` (lượt chơi thứ sáu không được làm gì).
- "người chơi ở 0 HP không thể bị sát thương hay hồi máu" → CẢ HAI
  bộ biến đổi chặn trên cùng một điều kiện.
- "nạp thêm hàng diễn ra cả khi trống" → một bước chuyển không có
  biến chặn.

Gạch chân mọi câu luật; mỗi câu là một `if` (hoặc một sự vắng mặt
chủ ý của `if`). Rồi cài lớp theo thứ tự đặc tả — constructor trước,
các bước chuyển kế, accessor sau — và đọc lại các luật đối chiếu với
các if của bạn. Một biến chặn bị thiếu là vô hình trên đường hạnh
phúc; vì vậy người chấm viết test ẩn cho nó.
"""

VI_L2 = r"""
**Tương tác đối tượng** là màn cuối của FRQ2: một lớp GIỮ các đối
tượng khác và điều khiển chúng. Hai mẫu:

- **Vòng ủy quyền**: `Library.playAll()` gọi `play()` trên mỗi Bài
  hát đang giữ. Thư viện không lưu số lượt chơi của chính nó — sự
  thật nằm trong các đối tượng được giữ, và Thư viện chỉ *hỏi*.
- **Truy vấn tổng hợp**: `likedCount()` hỏi mỗi đối tượng được giữ
  một boolean và đếm. Một bộ tích lũy trên vòng for-each.

Mùi thiết kế cần tránh: nhân bản trạng thái của đối tượng được giữ
trong vật chứa (một Thư viện cũng theo dõi lượt chơi sẽ lệch). Khi
câu chuyện nói vật chứa "biết về" các bài hát, nghĩa là nó giữ tham
chiếu — không phải sao chép trường của chúng.

Constructor của vật chứa khởi đầu rỗng (`new ArrayList<>()`), và
không gì khác xảy ra ở đó — một constructor *tự tạo* dữ liệu mà
caller lẽ ra truyền vào là đang trả lời sai đề.
"""

VI_L3 = r"""
**Đọc bảng điểm vào mã của bạn.** Mọi bảng điểm FRQ lớp có cùng năm
hàng; hướng mã của bạn vào chúng:

1. **Các trường**: đúng kiểu, `private`. Mỗi biến trạng thái mà câu
   chuyện nêu tên một trường — không hơn, không kém.
2. **Constructor**: mọi trường được gán (tham số qua `this.`), các
   trường suy ra được tính, không chế thêm.
3. **Các bước chuyển**: mỗi bộ biến đổi hiện thực đúng câu luật của
   nó, kể cả biến chặn.
4. **Các accessor**: tính từ trạng thái theo nhu cầu, không cache
   bản sao.
5. **Không API public thừa**: phương thức mà câu chuyện không hề nêu
   tên không thể giành điểm và có thể lộ trạng thái.

Kế hoạch thời gian cho FRQ lớp 9 điểm: 3 phút đọc/đánh dấu luật,
4 phút viết trường+constructor, 8 phút bước chuyển, 3 phút accessor,
2 phút kiểm toán luật. Phép kiểm toán tìm ra biến chặn bị thiếu —
điểm mất phổ biến nhất.
"""

BOILER_CANDY = r"""public class Solution {
    public static class CandyMachine {
        public CandyMachine(int candies) {
        }

        public boolean buy() {
            return false;
        }

        public void restock(int n) {
        }

        public int emptyCoins() {
            return 0;
        }
    }
}
"""

BOILER_SONG = r"""public class Solution {
    public static class Song {
        public Song(String title) {
        }

        public void play() {
        }

        public void unlike() {
        }

        public boolean isLiked() {
            return false;
        }
    }
}
"""

BOILER_LIBRARY = r"""public class Solution {
    public static class Library {
        public void add(Song s) {
        }

        public void playAll() {
        }

        public int likedCount() {
            return 0;
        }
    }
}
"""

BOILER_PLAYER = r"""public class Solution {
    public static class Player {
        public Player(int hp) {
        }

        public void move(int steps) {
        }

        public void hit(int dmg) {
        }

        public void heal(int amount) {
        }

        public int getHp() {
            return 0;
        }

        public int getX() {
            return 0;
        }
    }
}
"""

P_CANDY = challenge(
    "apx-m14-candy",
    "The candy machine lifecycle",
    "Implement `CandyMachine`: constructor takes the starting candy "
    "count (coins start at 0). `buy()` dispenses one candy and takes "
    "one coin — returns false (changing nothing) when out of candy. "
    "`restock(n)` adds n candies, allowed at any time. "
    "`emptyCoins()` returns the collected coins and **resets the "
    "coin count to zero**.",
    BOILER_CANDY,
    [(
        "machine lifecycle",
        r"""
Solution.CandyMachine m = new Solution.CandyMachine(2);
CjTestBase.checkTrue(m.buy(), "first sale");
CjTestBase.checkTrue(m.buy(), "second sale");
CjTestBase.checkTrue(!m.buy(), "sold out");
CjTestBase.checkEq(m.emptyCoins(), 2, "two coins collected");
CjTestBase.checkEq(m.emptyCoins(), 0, "reset happened");
m.restock(1);
CjTestBase.checkTrue(m.buy(), "restock revives sales");
""",
        "buy guards on candy count; emptyCoins reads-and-resets; restock has no guard.",
    )],
    level="independent",
    difficulty="advanced",
)

P_SONG = challenge(
    "apx-m14-song",
    "The five-play like rule",
    "Implement `Song`: constructor takes the title (plays 0, not "
    "liked). `play()` increments the play count; on the **fifth** "
    "play the song becomes liked (plays 6, 7, … do nothing further). "
    "`unlike()` clears the liked flag (plays are NOT reset — and "
    "reaching five again after unlike does nothing). `isLiked()` "
    "reports the flag.",
    BOILER_SONG,
    [(
        "like lifecycle",
        r"""
Solution.Song s = new Solution.Song("Hi");
s.play();
s.play();
s.play();
s.play();
CjTestBase.checkTrue(!s.isLiked(), "four plays not enough");
s.play();
CjTestBase.checkTrue(s.isLiked(), "fifth play likes");
s.unlike();
s.play();
s.play();
CjTestBase.checkTrue(!s.isLiked(), "re-crossing five does nothing");
""",
        "A plays counter and a separate liked flag; the like happens only when plays becomes exactly 5 AND the flag is still false... actually simplest: exactly-on-5.",
    )],
    level="combination",
    difficulty="advanced",
)

P_LIBRARY = challenge(
    "apx-m14-library",
    "The library that drives its songs",
    "Implement `Song` (as before: five-play like rule with "
    "`isLiked()`) and `Library`: starts empty, `add(Song)` appends, "
    "`playAll()` plays every held song once, `likedCount()` returns "
    "how many held songs are currently liked. The Library must NOT "
    "duplicate play counts — it asks its songs.",
    BOILER_LIBRARY + "\n\n" + BOILER_SONG.replace("public static class Song", "    public static class Song").replace("\n    ", "\n        ").replace("        public", "        public"),
    [(
        "library aggregation",
        r"""
Solution.Library lib = new Solution.Library();
lib.add(new Solution.Song("A"));
lib.add(new Solution.Song("B"));
lib.add(new Solution.Song("C"));
lib.playAll();
lib.playAll();
lib.playAll();
CjTestBase.checkEq(lib.likedCount(), 0, "three plays each is not five");
lib.playAll();
lib.playAll();
CjTestBase.checkEq(lib.likedCount(), 3, "every song hit five plays");
""",
        "playAll is a delegation loop; likedCount is an aggregation query over isLiked().",
    )],
    level="real-world",
    difficulty="advanced",
)

CP14 = challenge(
    "apx-cp-m14-player",
    "Checkpoint: the player lifecycle",
    "Implement `Player`: constructor takes starting HP (position "
    "starts at 0). `move(steps)` advances position (works at any "
    "HP). `hit(dmg)` reduces HP but **never below 0**, and does "
    "nothing when HP is already 0. `heal(amount)` raises HP but "
    "does nothing when HP is 0 (the player is out). `getHp()` and "
    "`getX()` report state.",
    BOILER_PLAYER,
    [(
        "player lifecycle",
        r"""
Solution.Player p = new Solution.Player(10);
p.hit(4);
p.move(3);
CjTestBase.checkEq(p.getX(), 3, "moving works while alive");
p.hit(6);
CjTestBase.checkEq(p.getHp(), 0, "floored at zero, not negative");
p.heal(5);
CjTestBase.checkEq(p.getHp(), 0, "the fallen cannot heal");
p.hit(3);
CjTestBase.checkEq(p.getHp(), 0, "the fallen cannot be hit");
""",
        "hit clamps at 0 and guards on hp > 0; heal guards on hp > 0; move has no guard.",
    )],
    level="mini-build",
    difficulty="advanced",
)

VI_CP14 = vi_challenge(
    "Điểm kiểm tra: vòng đời người chơi",
    "Cài đặt `Player`: constructor nhận HP ban đầu (vị trí bắt đầu ở "
    "0). `move(steps)` tiến vị trí (hoạt động ở mọi HP). `hit(dmg)` "
    "giảm HP nhưng **không bao giờ dưới 0**, và không làm gì khi HP "
    "đã là 0. `heal(amount)` tăng HP nhưng không làm gì khi HP là 0 "
    "(người chơi đã bị hạ). `getHp()` và `getX()` báo trạng thái.",
    [("player lifecycle", "hit chặn tại 0 và chặn khi hp > 0; heal chặn khi hp > 0; move không có biến chặn.")],
)

write_practice(
    M, "apx-p14-class", "Class design gauntlet",
    "Two full lifecycle classes plus the interaction finale.",
    "Võ đài thiết kế lớp",
    "Hai lớp vòng đời trọn vẹn cộng màn cuối tương tác đối tượng.",
    after_lesson="apx-m14-rubric", minutes=65, difficulty="advanced",
    challenges=[P_CANDY, P_SONG, P_LIBRARY],
    vi_challenges={
        "apx-m14-candy": vi_challenge(
            "Vòng đời máy bán kẹo",
            "Cài đặt `CandyMachine`: constructor nhận số kẹo ban đầu (xu "
            "bắt đầu 0). `buy()` dispensing một kẹo và nhận một xu — trả "
            "false (không đổi gì) khi hết kẹo. `restock(n)` thêm n kẹo, "
            "cho phép mọi lúc. `emptyCoins()` trả số xu đã thu và **đặt "
            "số xu về 0**.",
            [("machine lifecycle", "buy chặn theo số kẹo; emptyCoins đọc-và-reset; restock không có biến chặn.")],
        ),
        "apx-m14-song": vi_challenge(
            "Luật thích ở lượt chơi thứ năm",
            "Cài đặt `Song`: constructor nhận tiêu đề (0 lượt chơi, chưa "
            "được thích). `play()` tăng số lượt chơi; ở lượt chơi **thứ "
            "năm** bài hát được thích (lượt 6, 7, … không làm gì thêm). "
            "`unlike()` xóa cờ thích (số lượt chơi KHÔNG được reset — và "
            "chạm lại năm sau khi unlike không làm gì). `isLiked()` báo "
            "cờ.",
            [("like lifecycle", "Một bộ đếm lượt chơi và một cờ thích riêng biệt; việc thích chỉ xảy ra đúng khi lượt chơi thành 5.")],
        ),
        "apx-m14-library": vi_challenge(
            "Thư viện điều khiển các bài hát",
            "Cài đặt `Song` (như trước: luật thích ở lượt thứ năm với "
            "`isLiked()`) và `Library`: khởi đầu rỗng, `add(Song)` nối "
            "vào, `playAll()` chơi mỗi bài một lần, `likedCount()` trả số "
            "bài đang được thích. Thư viện KHÔNG được nhân bản số lượt "
            "chơi — nó hỏi các bài hát của mình.",
            [("library aggregation", "playAll là vòng ủy quyền; likedCount là truy vấn tổng hợp trên isLiked().")],
        ),
    },
    solutions=[
        ("apx-m14-candy", r"""public class Solution {
    public static class CandyMachine {
        private int coins;
        private int candies;

        public CandyMachine(int candies) {
            this.candies = candies;
            coins = 0;
        }

        public boolean buy() {
            if (candies == 0) {
                return false;
            }
            candies--;
            coins++;
            return true;
        }

        public void restock(int n) {
            candies += n;
        }

        public int emptyCoins() {
            int collected = coins;
            coins = 0;
            return collected;
        }
    }
}
""", r"""public class Solution {
    public static class CandyMachine {
        private int coins;
        private int candies;

        public CandyMachine(int candies) {
            this.candies = candies;
            coins = 0;
        }

        public boolean buy() {
            if (candies == 0) {
                return false;
            }
            candies--;
            coins++;
            return true;
        }

        public void restock(int n) {
            candies += n;
        }

        public int emptyCoins() {
            // BUG: reads without resetting — coins repeat forever
            return coins;
        }
    }
}
"""),
        ("apx-m14-song", r"""public class Solution {
    public static class Song {
        private String title;
        private int plays;
        private boolean liked;

        public Song(String title) {
            this.title = title;
            plays = 0;
            liked = false;
        }

        public void play() {
            plays++;
            if (plays == 5 && !liked) {
                liked = true;
            }
        }

        public void unlike() {
            liked = false;
        }

        public boolean isLiked() {
            return liked;
        }
    }
}
""", r"""public class Solution {
    public static class Song {
        private String title;
        private int plays;
        private boolean liked;

        public Song(String title) {
            this.title = title;
            plays = 0;
            liked = false;
        }

        public void play() {
            plays++;
            // BUG: likes at five AND at every later play — unlike is undone
            if (plays >= 5) {
                liked = true;
            }
        }

        public void unlike() {
            liked = false;
        }

        public boolean isLiked() {
            return liked;
        }
    }
}
"""),
        ("apx-m14-library", r"""public class Solution {
    public static class Library {
        private java.util.ArrayList<Song> songs = new java.util.ArrayList<Song>();

        public void add(Song s) {
            songs.add(s);
        }

        public void playAll() {
            for (Song s : songs) {
                s.play();
            }
        }

        public int likedCount() {
            int count = 0;
            for (Song s : songs) {
                if (s.isLiked()) {
                    count++;
                }
            }
            return count;
        }
    }

    public static class Song {
        private String title;
        private int plays;
        private boolean liked;

        public Song(String title) {
            this.title = title;
            plays = 0;
            liked = false;
        }

        public void play() {
            plays++;
            if (plays == 5) {
                liked = true;
            }
        }

        public void unlike() {
            liked = false;
        }

        public boolean isLiked() {
            return liked;
        }
    }
}
""", r"""public class Solution {
    public static class Library {
        private java.util.ArrayList<Song> songs = new java.util.ArrayList<Song>();
        private int playTotal = 0;

        public void add(Song s) {
            songs.add(s);
        }

        public void playAll() {
            for (Song s : songs) {
                s.play();
                playTotal++;
            }
        }

        public int likedCount() {
            // BUG: derives likes from the holder's own play counter
            return playTotal / 5;
        }
    }

    public static class Song {
        private String title;
        private int plays;
        private boolean liked;

        public Song(String title) {
            this.title = title;
            plays = 0;
            liked = false;
        }

        public void play() {
            plays++;
            if (plays == 5) {
                liked = true;
            }
        }

        public void unlike() {
            liked = false;
        }

        public boolean isLiked() {
            return liked;
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m14", "Checkpoint: the player lifecycle",
    "Guarded mutators, an unguarded mover, and clamping — all three rules in one class.",
    25,
    r"""
Two rules interact here: the floor at zero and the cannot-act-when-
out guard. Implement them in the order the spec states them, then
audit: every mutator either guards or deliberately does not.
""",
    "Điểm kiểm tra: vòng đời người chơi",
    "Các bộ biến đổi có biến chặn, một bộ di chuyển không chặn, và việc chặn sàn — cả ba luật trong một lớp.",
    r"""
Hai luật tương tác ở đây: sàn tại 0 và biến chặn không-hành-động-khi-
hạ. Cài chúng theo thứ tự đặc tả nêu, rồi kiểm toán: mỗi bộ biến đổi
hoặc chặn hoặc chủ ý không chặn.
""",
    CP14,
    VI_CP14,
    solution=r"""public class Solution {
    public static class Player {
        private int hp;
        private int x;

        public Player(int hp) {
            this.hp = hp;
            x = 0;
        }

        public void move(int steps) {
            x += steps;
        }

        public void hit(int dmg) {
            if (hp > 0) {
                hp -= dmg;
                if (hp < 0) {
                    hp = 0;
                }
            }
        }

        public void heal(int amount) {
            if (hp > 0) {
                hp += amount;
            }
        }

        public int getHp() {
            return hp;
        }

        public int getX() {
            return x;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Player {
        private int hp;
        private int x;

        public Player(int hp) {
            this.hp = hp;
            x = 0;
        }

        public void move(int steps) {
            x += steps;
        }

        public void hit(int dmg) {
            // BUG: no floor — HP goes negative
            hp -= dmg;
        }

        public void heal(int amount) {
            if (hp > 0) {
                hp += amount;
            }
        }

        public int getHp() {
            return hp;
        }

        public int getX() {
            return x;
        }
    }
}
""",
)

print("M14 done")
