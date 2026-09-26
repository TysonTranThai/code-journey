#!/usr/bin/env python3
"""AP CSA Core M17 — FRQ 2D Arrays (Q4)."""
from apcc import *

M = "cx-frq-2d"

L1 = r"""
Q4: one method, one grid, nine points. The recurring shapes:

**Find-and-report-position** — "return {row, col} of the largest
value" as an int[]:

```java
public int[] findMax(int[][] grid) {
    int[] at = new int[2];
    for (int r = 0; r < grid.length; r++) {
        for (int c = 0; c < grid[r].length; c++) {
            if (grid[r][c] > grid[at[0]][at[1]]) {
                at[0] = r;
                at[1] = c;
            }
        }
    }
    return at;
}
```

Seed from (0,0) — the precondition `grid.length >= 1` makes it legal —
and keep a strict `>` for the earliest tie.

**Conditional transform** — mutate cells matching a rule:

```java
for (int r = 0; r < grid.length; r++) {
    for (int c = 0; c < grid[r].length; c++) {
        if (grid[r][c] < 0) {
            grid[r][c] = 0;
        }
    }
}
```

**Count by neighborhood** — the guarded-neighbor pattern (Module 8)
inside a full-grid loop.

The Q4-specific discipline: when the answer is a POSITION, decide
immediately how to encode it (int[2]? an int code like 10*r+c?
a row-only?) — the prompt's return type forces one; misreading it is
the classic zero.
"""

L2 = r"""
**Positional transforms** — Q4's most intricate family: cells whose
new value depends on a NEIGHBORHOOD, not just themselves.

*"Replace each cell with the count of orthogonal neighbors holding
the same value"* — the read/write hazard: writes must not poison
reads. Compute the counts into a NEW grid, then (if required in
place) copy back:

```java
int[][] counts = new int[grid.length][grid[0].length];
for (int r = 0; r < grid.length; r++) {
    for (int c = 0; c < grid[r].length; c++) {
        int same = 0;
        if (r > 0 && grid[r - 1][c] == grid[r][c]) { same++; }
        if (r < grid.length - 1 && grid[r + 1][c] == grid[r][c]) { same++; }
        if (c > 0 && grid[r][c - 1] == grid[r][c]) { same++; }
        if (c < grid[r].length - 1 && grid[r][c + 1] == grid[r][c]) { same++; }
        counts[r][c] = same;
    }
}
// counts is the answer (or copy into grid if the spec says in place)
```

The two-grid pattern costs one allocation and saves the entire class
of read-after-write bugs. When the spec says "in place", the safe
compromise is compute-then-copy — still no aliasing bugs.

**The transposed-index trap:** `grid[c][r]` compiles fine whenever
`c` happens to be within row bounds... and reads the wrong cell. The
only defense is the orientation ritual: name the loop variables
`r` and `c`, index `grid[r][c]`, and never "save typing" by reusing
one variable for both.
"""

L3 = r"""
**Navigation Q4s** — the hardest variant: walk from a cell according
to a rule.

*"From (row, col), repeatedly move to the adjacent cell with the
smallest value (ties: up, left, right, down); stop when no neighbor is
smaller; return the number of moves."*

```java
public int descent(int[][] grid, int row, int col) {
    int moves = 0;
    int[][] dirs = { {-1, 0}, {0, -1}, {0, 1}, {1, 0} };
    while (true) {
        int best = grid[row][col];
        int br = -1, bc = -1;
        for (int[] d : dirs) {
            int nr = row + d[0], nc = col + d[1];
            if (nr >= 0 && nr < grid.length && nc >= 0 && nc < grid[0].length) {
                if (grid[nr][nc] < best) {
                    best = grid[nr][nc];
                    br = nr;
                    bc = nc;
                }
            }
        }
        if (br == -1) { return moves; }
        row = br; col = bc; moves++;
    }
}
```

Reading it: candidate-collection (four guarded reads), a seeded min,
and a sentinel stop. Note the tie rule encoded by the DIRECTION
ORDER: scanning up→left→right→down with strict `<` keeps the FIRST
preferred direction on ties — the ordering is part of the
specification.

Grid walks also test termination: a move rule that can revisit cells
needs a visited guard or a step cap (the CP8 path pattern) — check the
prompt for which it wants.
"""

write_module(
    M,
    "FRQ 2D Arrays",
    "Q4's one-method answers: position reports, neighborhood transforms with the two-grid pattern, and navigational walks.",
    "Mảng 2 chiều kiểu FRQ",
    "Các lời giải một-phương-thức của Q4: báo-cáo-vị-trí, biến đổi hàng-xóm với mẫu hai-lưới, và các bước đi định hướng.",
    lessons=["cx-m17-q4-shapes", "cx-m17-transform", "cx-m17-navigation", "cx-cp-m17"],
    practices=["cx-p17-frq2d"],
)

write_lesson(
    M, "cx-m17-q4-shapes", "The Q4 shapes",
    "Position reports, conditional transforms, neighborhood counts.",
    12, L1,
    "Các hình Q4",
    "Báo cáo vị trí, biến đổi có điều kiện, đếm theo hàng xóm.",
    r"""
Q4: một phương thức, một lưới, chín điểm. Các hình tái diễn:

**Tìm-và-báo-cáo-vị-trí** — "trả về {hàng, cột} của giá trị lớn nhất"
dưới dạng int[]:

```java
public int[] findMax(int[][] grid) {
    int[] at = new int[2];
    for (int r = 0; r < grid.length; r++) {
        for (int c = 0; c < grid[r].length; c++) {
            if (grid[r][c] > grid[at[0]][at[1]]) {
                at[0] = r;
                at[1] = c;
            }
        }
    }
    return at;
}
```

Seed từ (0,0) — điều kiện tiên quyết `grid.length >= 1` hợp pháp hóa
điều đó — và giữ dấu `>` nghiêm ngặt cho đồng giá sớm nhất.

**Biến đổi có điều kiện** — biến đổi các ô khớp luật:

```java
for (int r = 0; r < grid.length; r++) {
    for (int c = 0; c < grid[r].length; c++) {
        if (grid[r][c] < 0) {
            grid[r][c] = 0;
        }
    }
}
```

**Đếm theo hàng xóm** — mẫu hàng-xóm-có-chặn (Module 8) bên trong một
vòng lặp toàn-lưới.

Kỷ luật riêng của Q4: khi đáp án là một VỊ TRÍ, quyết định ngay cách
mã hóa (int[2]? một mã int kiểu 10*r+c? chỉ-hàng?) — kiểu trả về của
đề ép một lựa chọn; đọc sai nó là lỗi-số-không kinh điển.
""",
)

write_lesson(
    M, "cx-m17-transform", "Neighborhood transforms",
    "The two-grid pattern against read-after-write poisoning; orientation ritual.",
    12, L2,
    "Biến đổi hàng xóm",
    "Mẫu hai-lưới chống đầu-độc-sau-khi-ghi; nghi thức định hướng.",
    r"""
**Biến đổi theo vị trí** — họ phức-tạp-nhất của Q4: ô mới phụ thuộc
HÀNG XÓM, không chỉ chính nó.

*"Thay mỗi ô bằng số hàng xóm trực giao mang cùng giá trị"* — mối nguy
đọc/ghi: phép ghi không được đầu độc phép đọc. Tính các số đếm vào một
lưới MỚI, rồi (nếu đặc tả yêu cầu tại chỗ) sao chép lại:

```java
int[][] counts = new int[grid.length][grid[0].length];
for (int r = 0; r < grid.length; r++) {
    for (int c = 0; c < grid[r].length; c++) {
        int same = 0;
        if (r > 0 && grid[r - 1][c] == grid[r][c]) { same++; }
        if (r < grid.length - 1 && grid[r + 1][c] == grid[r][c]) { same++; }
        if (c > 0 && grid[r][c - 1] == grid[r][c]) { same++; }
        if (c < grid[r].length - 1 && grid[r][c + 1] == grid[r][c]) { same++; }
        counts[r][c] = same;
    }
}
// counts là đáp án (hoặc sao chép vào grid nếu đề nói tại chỗ)
```

Mẫu hai-lưới tốn một phép cấp phát và cứu cả một họ lỗi ghi-xong-đọc.
Khi đặc tả nói "tại chỗ", thỏa hiệp an toàn là tính-xong-rồi-sao-chép
— vẫn không có lỗi bí danh.

**Cái bẫy chỉ-số-chuyển-vị:** `grid[c][r]` biên dịch ngon lành cứ mỗi
lần `c` tình cờ nằm trong biên hàng... và đọc nhầm ô. Vũ khí duy nhất
là nghi thức định hướng: đặt tên biến lặp là `r` và `c`, đánh chỉ số
`grid[r][c]`, và không bao giờ "tiết kiệm gõ phím" bằng cách dùng lại
một biến cho cả hai.
""",
)

write_lesson(
    M, "cx-m17-navigation", "Navigational Q4s",
    "Grid walks with candidate collection, seeded min, and sentinel stops.",
    12, L3,
    "Q4 định hướng",
    "Bước đi trên lưới với thu-thập-ứng-viên, min có seed, và điểm dừng lính canh.",
    r"""
**Q4 dẫn đường** — biến thể khó nhất: đi từ một ô theo một luật.

*"Từ (row, col), liên tục chuyển sang ô kề có giá trị nhỏ nhất (đồng
giá: lên, trái, phải, xuống); dừng khi không còn hàng xóm nhỏ hơn; trả
về số bước đi."*

```java
public int descent(int[][] grid, int row, int col) {
    int moves = 0;
    int[][] dirs = { {-1, 0}, {0, -1}, {0, 1}, {1, 0} };
    while (true) {
        int best = grid[row][col];
        int br = -1, bc = -1;
        for (int[] d : dirs) {
            int nr = row + d[0], nc = col + d[1];
            if (nr >= 0 && nr < grid.length && nc >= 0 && nc < grid[0].length) {
                if (grid[nr][nc] < best) {
                    best = grid[nr][nc];
                    br = nr;
                    bc = nc;
                }
            }
        }
        if (br == -1) { return moves; }
        row = br; col = bc; moves++;
    }
}
```

Đọc nó: thu-thập-ứng-viên (bốn lần đọc có chặn), một min có seed, và
điểm dừng lính canh. Chú ý luật đồng-giá được mã hóa bởi THỨ TỰ
HƯỚNG: quét lên→trái→phải→xuống với dấu `<` nghiêm ngặt giữ hướng
được-ưu-tiên-đầu-tiên khi đồng giá — thứ tự quét là một phần của đặc tả.

Các bước đi trên lưới cũng kiểm tra tính dừng: một luật di-chuyển có
thể ghé lại ô cũ cần lớp chặn đã-thăm hoặc trần bước (mẫu đường-dẫn của
CP8) — đọc đề xem nó muốn cái nào.
""",
)

BOILER_FINDMAX = r"""public class Solution {
    // CONTRACT: {row, col} of the LARGEST value (earliest tie, row-major
    // order). Precondition: grid.length >= 1, rectangular.
    public static int[] findMax(int[][] grid) {
        return null; // replace
    }
}
"""

BOILER_ZEROOUT = r"""public class Solution {
    // CONTRACT: in place, replace every negative cell with 0.
    public static void zeroOut(int[][] grid) {
        // replace
    }
}
"""

BOILER_SAMECOUNT = r"""public class Solution {
    // CONTRACT: NEW grid where each cell holds the count of its
    // orthogonal neighbors holding the SAME value as it.
    // Precondition: grid.length >= 1 and rectangular.
    public static int[][] sameCount(int[][] grid) {
        return null; // replace
    }
}
"""

BOILER_DESCENT = r"""public class Solution {
    // CONTRACT: from (row, col), repeatedly move to the adjacent cell
    // with the SMALLEST value; ties prefer up, then left, then right,
    // then down. Stop when no neighbor is strictly smaller. Return the
    // number of moves.
    public static int descent(int[][] grid, int row, int col) {
        return 0; // replace
    }
}
"""

BOILER_RIMSUM = r"""public class Solution {
    // CONTRACT: sum of the border cells (first/last row and first/last
    // column of a rectangular grid; a 1xN or Nx1 grid is all border).
    public static int rimSum(int[][] grid) {
        return 0; // replace
    }
}
"""

BOILER_CP17 = r"""public class Solution {
    // FULL Q4 — relocation:
    // From (row, col), walk through adjacent cells (up/left/right/down)
    // to reach the cell whose value equals `target`, using the FEWEST
    // moves. Return that minimum move count, or -1 when target is
    // unreachable. (BFS or repeated-scan is fine; small grids.)
    public static int relocate(int[][] grid, int row, int col, int target) {
        return -1; // replace
    }
}
"""

P_FINDMAX = challenge(
    "cx-m17-find-max-pos",
    "Q4: position report",
    "Implement `findMax` returning `int[]{row, col}` of the largest value, earliest in row-major order. Seed from (0,0); strict comparison.",
    BOILER_FINDMAX,
    [(
        "position reported",
        r"""
int[] at = Solution.findMax(new int[][]{ {1, 9}, {7, 2} });
CjTestBase.checkEq(at[0], 0, "row of 9");
CjTestBase.checkEq(at[1], 1, "col of 9");
int[] b = Solution.findMax(new int[][]{ {5, 5}, {5, 5} });
CjTestBase.checkEq(b[0], 0, "all equal -> first cell");
CjTestBase.checkEq(b[1], 0, "first cell");
""",
        "int[] at = {0, 0}; strict > against grid[at[0]][at[1]].",
    )],
    level="guided",
)

P_ZEROOUT = challenge(
    "cx-m17-zero-out",
    "Q4: conditional transform",
    "Implement `zeroOut`: negatives become 0, in place. The simplest transform — do it cleanly and verify with an all-negative grid.",
    BOILER_ZEROOUT,
    [(
        "negatives zeroed",
        r"""
int[][] g = { {1, -2}, {-3, 4} };
Solution.zeroOut(g);
CjTestBase.checkEq(g[0], new int[]{1, 0}, "row 0");
CjTestBase.checkEq(g[1], new int[]{0, 4}, "row 1");
int[][] all = { {-1, -1} };
Solution.zeroOut(all);
CjTestBase.checkEq(all[0], new int[]{0, 0}, "all negative");
""",
        "Plain double loop; if (grid[r][c] < 0) grid[r][c] = 0;",
    )],
    level="imitation",
)

P_SAMECOUNT = challenge(
    "cx-m17-same-count",
    "Q4: neighborhood transform",
    "Implement `sameCount` with the two-grid pattern: each output cell counts orthogonal neighbors equal to it. Corners count at most 2, edges 3, interior 4.",
    BOILER_SAMECOUNT,
    [(
        "neighborhood counted",
        r"""
int[][] out = Solution.sameCount(new int[][]{ {7, 1, 7}, {7, 7, 1}, {2, 2, 2} });
CjTestBase.checkEq(out[0][0], 1, "down neighbor 7");
CjTestBase.checkEq(out[1][1], 1, "only the left neighbor is 7");
CjTestBase.checkEq(out[0][1], 0, "1 surrounded by 7s");
CjTestBase.checkEq(out[2][1], 2, "left and right neighbors are 2");
""",
        "Compute into counts[][], return it — do NOT write into grid while reading.",
    )],
    level="real-world",
)

P_DESCENT = challenge(
    "cx-m17-descent",
    "Q4: navigational walk",
    "Implement `descent` exactly per its contract, including the tie order (up, left, right, down). Trace a 2x2 grid by hand for each starting corner before coding.",
    BOILER_DESCENT,
    [(
        "walk counted",
        r"""
int[][] g = { {5, 3}, {4, 1} };
CjTestBase.checkEq(Solution.descent(g, 0, 0), 2, "5 -> 3 -> 1");
CjTestBase.checkEq(Solution.descent(g, 1, 1), 0, "already the minimum");
CjTestBase.checkEq(Solution.descent(g, 0, 1), 1, "3 -> 1");
""",
        "Scan directions in tie order with strict <; stop when no candidate.",
    )],
    level="real-world",
)

P_RIMSUM = challenge(
    "cx-m17-rim-sum",
    "Q4: rim aggregation",
    "Implement `rimSum`: the sum of border cells. Handle the degenerate shapes (1xN, Nx1 — every cell is border; 1x1 — the single cell) explicitly. This is a fencepost-style boundary test in grid form.",
    BOILER_RIMSUM,
    [(
        "rim totaled",
        r"""
CjTestBase.checkEq(Solution.rimSum(new int[][]{ {1, 2}, {3, 4} }), 10, "all four are rim");
CjTestBase.checkEq(Solution.rimSum(new int[][]{ {1, 2, 3}, {4, 5, 6}, {7, 8, 9} }), 40, "rim excludes 5");
CjTestBase.checkEq(Solution.rimSum(new int[][]{ {9} }), 9, "single cell is rim");
CjTestBase.checkEq(Solution.rimSum(new int[][]{ {1, 2, 3} }), 6, "1xN: everything");
""",
        "Two options: sum everything minus interior, or iterate with r==0/last || c==0/last.",
    )],
    level="combination",
)

CP17 = challenge(
    "cx-cp-m17-relocate",
    "Checkpoint: relocation walk",
    "The hardest Q4 variant: minimum moves from (row, col) to the cell holding `target`, moving up/left/right/down, or -1 if unreachable. A BFS or a repeated-scan distance fill both work — small grids. This fuses navigation, guards, and a sentinel.",
    BOILER_CP17,
    [(
        "moves minimized",
        r"""
int[][] g = { {5, 3}, {4, 1} };
CjTestBase.checkEq(Solution.relocate(g, 0, 0, 1), 2, "5 -> 3 -> 1");
CjTestBase.checkEq(Solution.relocate(g, 0, 0, 5), 0, "already there");
CjTestBase.checkEq(Solution.relocate(g, 0, 0, 9), -1, "absent target");
int[][] h = { {5, 3}, {4, 5} };
CjTestBase.checkEq(Solution.relocate(h, 0, 0, 5), 0, "target is the start");
""",
        "BFS with a distance grid, or relax repeatedly: dist[r][c] = min neighbor dist + 1.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p17-frq2d", "FRQ 2D array lab",
    "Position reports, transforms, neighborhood counts, navigation, rim sums.",
    "Phòng mảng 2 chiều kiểu FRQ",
    "Báo cáo vị trí, biến đổi, đếm hàng xóm, định hướng, tổng vành ngoài.",
    after_lesson="cx-m17-transform", minutes=65, difficulty="advanced",
    challenges=[P_FINDMAX, P_ZEROOUT, P_SAMECOUNT, P_DESCENT, P_RIMSUM],
    vi_challenges={
        "cx-m17-find-max-pos": vi_challenge("Q4: báo cáo vị trí",
            "Hiện thực `findMax` trả về `int[]{row, col}` của giá trị lớn nhất, sớm nhất theo thứ tự hàng-chính. Seed từ (0,0); so sánh nghiêm ngặt.",
            [("position reported", "int[] at = {0, 0}; dấu > nghiêm ngặt đối chiếu grid[at[0]][at[1]].")]),
        "cx-m17-zero-out": vi_challenge("Q4: biến đổi có điều kiện",
            "Hiện thực `zeroOut`: các ô âm thành 0, tại chỗ. Biến đổi đơn giản nhất — làm sạch sẽ và kiểm chứng bằng một lưới toàn số âm.",
            [("negatives zeroed", "Vòng kép thuần; if (grid[r][c] < 0) grid[r][c] = 0;")]),
        "cx-m17-same-count": vi_challenge("Q4: biến đổi hàng xóm",
            "Hiện thực `sameCount` bằng mẫu hai-lưới: mỗi ô đầu ra đếm số hàng xóm trực giao bằng giá trị của nó. Góc đếm tối đa 2, mép 3, giữa 4.",
            [("neighborhood counted", "Tính vào counts[][], trả về nó — ĐỪNG ghi vào grid trong khi đang đọc.")]),
        "cx-m17-descent": vi_challenge("Q4: bước đi định hướng",
            "Hiện thực `descent` đúng theo hợp đồng, kể cả thứ tự đồng giá (lên, trái, phải, xuống). Truy vết tay một lưới 2x2 cho từng góc xuất phát trước khi viết mã.",
            [("walk counted", "Quét các hướng theo thứ tự ưu tiên với dấu < nghiêm ngặt; dừng khi không có ứng viên.")]),
        "cx-m17-rim-sum": vi_challenge("Q4: tổng vành ngoài",
            "Hiện thực `rimSum`: tổng các ô biên. Xử lý tường minh các hình thoái hóa (1xN, Nx1 — mọi ô đều là biên; 1x1 — ô duy nhất). Đây là bài kiểm-trả-biên kiểu hàng-rào dưới dạng lưới.",
            [("rim totaled", "Hai lựa chọn: cộng hết trừ phần trong, hoặc duyệt với r==0/cuối || c==0/cuối.")]),
    },
    solutions=[
        ("cx-m17-find-max-pos", BOILER_FINDMAX.replace("return null; // replace",
            "int[] at = new int[2];\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                if (grid[r][c] > grid[at[0]][at[1]]) {\n                    at[0] = r;\n                    at[1] = c;\n                }\n            }\n        }\n        return at;"),
         BOILER_FINDMAX.replace("return null; // replace",
            "int[] at = new int[2];\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                if (grid[r][c] >= grid[at[0]][at[1]]) {\n                    at[0] = r;\n                    at[1] = c;\n                }\n            }\n        }\n        return at;")),
        ("cx-m17-zero-out",
         r"""public class Solution {
    public static void zeroOut(int[][] grid) {
        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[r].length; c++) {
                if (grid[r][c] < 0) {
                    grid[r][c] = 0;
                }
            }
        }
    }
}
""",
         r"""public class Solution {
    public static void zeroOut(int[][] grid) {
        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[r].length; c++) {
                if (grid[r][c] > 0) {
                    grid[r][c] = 0;
                }
            }
        }
    }
}
"""),
        ("cx-m17-same-count", BOILER_SAMECOUNT.replace("return null; // replace",
            "int[][] counts = new int[grid.length][grid[0].length];\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                int same = 0;\n                if (r > 0 && grid[r - 1][c] == grid[r][c]) { same++; }\n                if (r < grid.length - 1 && grid[r + 1][c] == grid[r][c]) { same++; }\n                if (c > 0 && grid[r][c - 1] == grid[r][c]) { same++; }\n                if (c < grid[r].length - 1 && grid[r][c + 1] == grid[r][c]) { same++; }\n                counts[r][c] = same;\n            }\n        }\n        return counts;"),
         BOILER_SAMECOUNT.replace("return null; // replace",
            "int[][] counts = new int[grid.length][grid[0].length];\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                int same = 0;\n                if (r > 0 && grid[r - 1][c] != grid[r][c]) { same++; }\n                if (r < grid.length - 1 && grid[r + 1][c] != grid[r][c]) { same++; }\n                if (c > 0 && grid[r][c - 1] != grid[r][c]) { same++; }\n                if (c < grid[r].length - 1 && grid[r][c + 1] != grid[r][c]) { same++; }\n                counts[r][c] = same;\n            }\n        }\n        return counts;")),
        ("cx-m17-descent", BOILER_DESCENT.replace("return 0; // replace",
            "int moves = 0;\n        int[][] dirs = { {-1, 0}, {0, -1}, {0, 1}, {1, 0} };\n        while (true) {\n            int best = grid[row][col];\n            int br = -1, bc = -1;\n            for (int[] d : dirs) {\n                int nr = row + d[0], nc = col + d[1];\n                if (nr >= 0 && nr < grid.length && nc >= 0 && nc < grid[0].length) {\n                    if (grid[nr][nc] < best) {\n                        best = grid[nr][nc];\n                        br = nr;\n                        bc = nc;\n                    }\n                }\n            }\n            if (br == -1) { return moves; }\n            row = br;\n            col = bc;\n            moves++;\n        }"),
         BOILER_DESCENT.replace("return 0; // replace",
            "int moves = 1;\n        int[][] dirs = { {-1, 0}, {0, -1}, {0, 1}, {1, 0} };\n        while (true) {\n            int best = grid[row][col];\n            int br = -1, bc = -1;\n            for (int[] d : dirs) {\n                int nr = row + d[0], nc = col + d[1];\n                if (nr >= 0 && nr < grid.length && nc >= 0 && nc < grid[0].length) {\n                    if (grid[nr][nc] < best) {\n                        best = grid[nr][nc];\n                        br = nr;\n                        bc = nc;\n                    }\n                }\n            }\n            if (br == -1) { return moves; }\n            row = br;\n            col = bc;\n            moves++;\n        }")),
        ("cx-m17-rim-sum", BOILER_RIMSUM.replace("return 0; // replace",
            "int total = 0;\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                if (r == 0 || r == grid.length - 1 || c == 0 || c == grid[r].length - 1) {\n                    total += grid[r][c];\n                }\n            }\n        }\n        return total;"),
         BOILER_RIMSUM.replace("return 0; // replace",
            "int total = 0;\n        for (int r = 1; r < grid.length - 1; r++) {\n            for (int c = 1; c < grid[r].length - 1; c++) {\n                if (r == 0 || r == grid.length - 1 || c == 0 || c == grid[r].length - 1) {\n                    total += grid[r][c];\n                }\n            }\n        }\n        return total;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m17", "Checkpoint: relocation",
    "Minimum-move navigation with distance relaxation — Q4's ceiling.",
    35,
    r"""
relocate is BFS-lite: seed the start with distance 0, relax neighbors
in passes until nothing changes, read the target's distance — or -1
when the fill never reaches it. It fuses navigation, guards, and the
sentinel into one method, which is why Q4 sometimes asks for exactly
this. If your first version moved into already-shorter cells forever,
the relaxation condition was missing `dist[nr][nc] > dist[r][c] + 1`.
""",
    "Điểm kiểm tra: di dời",
    "Định hướng với số bước tối thiểu bằng nới-lỏng-khoảng-cách — trần của Q4.",
    r"""
relocate là BFS-rút-gọn: seed điểm xuất phát bằng khoảng cách 0, nới
lỏng hàng xóm theo các lượt cho tới khi không gì đổi nữa, đọc khoảng
cách của đích — hoặc -1 khi phép-lấp không bao giờ chạm tới. Nó hợp
nhất định hướng, lớp chặn, và lính canh vào một phương thức, vì vậy Q4
đôi khi hỏi đúng thứ này. Nếu bản đầu của bạn đi-lang-thang vào các ô
đã-ngắn-hơn-mãi-mãi, điều kiện nới lỏng còn thiếu
`dist[nr][nc] > dist[r][c] + 1`.
""",
    CP17,
    vi_challenge("Điểm kiểm tra: di dời",
        "Biến thể Q4 khó nhất: số bước tối thiểu từ (row, col) tới ô chứa `target`, đi lên/trái/phải/xuống, hoặc -1 nếu không tới được. BFS hoặc điền-khoảng-cách-quét-lặp đều được — lưới nhỏ. Bài này hợp nhất định hướng, lớp chặn, và lính canh.",
        [("moves minimized", "BFS với lưới khoảng cách, hoặc nới lỏng lặp lại: dist[nr][nc] = min dist hàng xóm + 1.")]),
    solution=r"""public class Solution {
    public static int relocate(int[][] grid, int row, int col, int target) {
        int rows = grid.length;
        int cols = grid[0].length;
        int[][] dist = new int[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                dist[r][c] = -1;
            }
        }
        dist[row][col] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < rows; r++) {
                for (int c = 0; c < cols; c++) {
                    if (dist[r][c] < 0) {
                        int best = Integer.MAX_VALUE / 4;
                        if (r > 0 && dist[r - 1][c] >= 0) { best = Math.min(best, dist[r - 1][c] + 1); }
                        if (r < rows - 1 && dist[r + 1][c] >= 0) { best = Math.min(best, dist[r + 1][c] + 1); }
                        if (c > 0 && dist[r][c - 1] >= 0) { best = Math.min(best, dist[r][c - 1] + 1); }
                        if (c < cols - 1 && dist[r][c + 1] >= 0) { best = Math.min(best, dist[r][c + 1] + 1); }
                        if (best < Integer.MAX_VALUE / 4) {
                            dist[r][c] = best;
                            changed = true;
                        }
                    }
                }
            }
        }
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == target) {
                    return dist[r][c];
                }
            }
        }
        return -1;
    }
}
""",
    wrong=r"""public class Solution {
    public static int relocate(int[][] grid, int row, int col, int target) {
        int rows = grid.length;
        int cols = grid[0].length;
        int[][] dist = new int[rows][cols];
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < rows; r++) {
                for (int c = 0; c < cols; c++) {
                    if (r == row && c == col) {
                        dist[r][c] = 0;
                    }
                    int best = (r == row && c == col) ? 0 : dist[r][c];
                    if (best == -1) {
                        best = Integer.MAX_VALUE / 4;
                        if (r > 0 && dist[r - 1][c] >= 0) { best = Math.min(best, dist[r - 1][c] + 1); }
                        if (r < rows - 1 && dist[r + 1][c] >= 0) { best = Math.min(best, dist[r + 1][c] + 1); }
                        if (c > 0 && dist[r][c - 1] >= 0) { best = Math.min(best, dist[r][c - 1] + 1); }
                        if (c < cols - 1 && dist[r][c + 1] >= 0) { best = Math.min(best, dist[r][c + 1] + 1); }
                        if (best < Integer.MAX_VALUE / 4 && best != dist[r][c]) {
                            if (dist[r][c] != best) { changed = true; }
                            dist[r][c] = best;
                        }
                    }
                }
            }
        }
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == target && dist[r][c] >= 0) {
                    return dist[r][c];
                }
            }
        }
        return -1;
    }
}
""",
)
