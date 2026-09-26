#!/usr/bin/env python3
"""AP CSA Advanced M7 — Advanced 2D array problems (verified ground truths)."""
from apx import *

M = "apx-grids"

write_module(
    M,
    "Advanced 2D Array Problems",
    "Rotations, neighborhood scans, column ledgers, and spiral traversal — row/column discipline under edge pressure. Difficulty E3–E5.",
    "Bài toán mảng 2 chiều nâng cao",
    "Xoay ma trận, quét vùng lân cận, sổ cái theo cột, và duyệt xoắn ốc — kỷ luật hàng/cột dưới áp lực biên. Độ khó E3–E5.",
    lessons=["apx-m7-axes", "apx-m7-neighborhood", "apx-m7-bounds", "apx-cp-m7"],
    practices=["apx-p7-grids"],
)

L1 = r"""
**Rows and columns are different axes.** The exam's 2D traps are all
axis confusions:

- `g[r][c]` — row first, always. `g[0]` is the first ROW, not the
  first column.
- `g.length` is the row count; `g[0].length` is the column count.
  Rectangular grids can have `g.length != g[0].length` — a rotation
  changes which one is which.
- **Row-major traversal** (for r, then for c) visits in storage
  order; **column-major** (for c, then for r) is the one FRQs ask
  for when they say "process column by column".

The 90° clockwise rotation is the canonical axis exercise:
`out[c][rows - 1 - r] = g[r][c]`. Derive it once slowly: the old row
r becomes the new column (rows-1-r) counted from the right; the old
column c becomes the new row c. Verify on a 2×3 before you trust it.
"""

L2 = r"""
**Neighborhood processing** needs an offset table and a bounds
guard — the pattern behind Game-of-Life, image blurs, and hotspot
problems:

```java
int[] dr = {-1, -1, -1, 0, 0, 1, 1, 1};
int[] dc = {-1,  0,  1, -1, 1, -1, 0, 1};
for (int d = 0; d < 8; d++) {
    int nr = r + dr[d], nc = c + dc[d];
    if (nr >= 0 && nr < g.length && nc >= 0 && nc < g[0].length) {
        sum += g[nr][nc];
        count++;
    }
}
```

Two decisions hide the difficulty: **does a cell count itself?**
(usually no — read the spec twice), and **do you average over 8 or
over the actual in-bounds neighbor count?** Corners have 3 neighbors;
dividing by 8 everywhere is the subtle wrong answer the hidden tests
catch.

**Aggregation with signs**: when a ledger holds debits and credits,
summing columns then taking absolute values is NOT the same as
summing absolute values. The spec's phrase "per-column balance"
tells you which.
"""

L3 = r"""
**Complex traversals** (spirals, diagonals, borders) are boundary
management problems. The spiral keeps four walls (top, bottom, left,
right) and shrinks them after each side — with two re-checks
(`if (top <= bottom)`, `if (left <= right)`) that exist only for
single-row and single-column remainders. Drop a re-check and a 3×1
grid double-counts.

Rules for writing any complex traversal:

1. Write the loop invariants in the margin: "top row fully filled",
   "right column fully filled", etc.
2. After each side, move the corresponding wall and *say why* the
   next side's bounds are still valid.
3. Test 1×n, n×1, and 1×1 before anything else. Rectangular
   (non-square) inputs break symmetric-looking code.

That last rule is the advanced habit: the bug is never in the middle
of the grid. It is on the last column, the single row, or the
already-shrunk wall.
"""

VI_L1 = r"""
**Hàng và cột là hai trục khác nhau.** Các bẫy 2D của đề thi đều là
nhầm trục:

- `g[r][c]` — hàng trước, luôn luôn. `g[0]` là hàng ĐẦU TIÊN, không
  phải cột đầu tiên.
- `g.length` là số hàng; `g[0].length` là số cột. Mảng chữ nhật có
  thể `g.length != g[0].length` — một phép xoay đổi chỗ hai giá trị
  này cho nhau.
- **Duyệt theo hàng** (for r, rồi for c) đi theo thứ tự lưu trữ;
  **duyệt theo cột** (for c, rồi for r) là thứ FRQ yêu cầu khi nói
  "xử lý theo từng cột".

Xoay 90° theo chiều kim đồng hồ là bài tập trục kinh điển:
`out[c][rows - 1 - r] = g[r][c]`. Dẫn ra một lần từ từ: hàng cũ r
thành cột mới (rows-1-r) đếm từ bên phải; cột cũ c thành hàng mới c.
Kiểm chứng trên 2×3 trước khi tin nó.
"""

VI_L2 = r"""
**Xử lý vùng lân cận** cần bảng độ dịch và biến chặn biên — mẫu nền
của Game-of-Life, làm mờ ảnh, và bài điểm nóng:

```java
int[] dr = {-1, -1, -1, 0, 0, 1, 1, 1};
int[] dc = {-1,  0,  1, -1, 1, -1, 0, 1};
for (int d = 0; d < 8; d++) {
    int nr = r + dr[d], nc = c + dc[d];
    if (nr >= 0 && nr < g.length && nc >= 0 && nc < g[0].length) {
        sum += g[nr][nc];
        count++;
    }
}
```

Hai quyết định giấu độ khó: **ô đó có tự đếm mình không?** (thường
không — đọc đặc tả hai lần), và **lấy trung bình chia cho 8 hay chia
cho số láng giềng thực tế trong biên?** Ô góc có 3 láng giềng; chia
cho 8 ở mọi nơi là đáp án sai tinh vi mà test ẩn bắt được.

**Tổng hợp có dấu**: khi sổ cái có cả ghi nợ và ghi có, cộng từng
cột rồi lấy trị tuyệt đối KHÁC với cộng trị tuyệt đối từng ô. Cụm từ
"số dư từng cột" trong đặc tả cho biết cái nào.
"""

VI_L3 = r"""
**Các lượt duyệt phức tạp** (xoắn ốc, đường chéo, viền) là bài toán
quản lý biên. Xoắn ốc giữ bốn bức tường (trên, dưới, trái, phải) và
thu nhỏ sau mỗi cạnh — với hai lần kiểm tra lại (`if (top <= bottom)`,
`if (left <= right)`) tồn tại chỉ cho phần dư một hàng hoặc một cột.
Bỏ một lần kiểm tra, lưới 3×1 bị đếm trùng.

Luật viết bất kỳ lượt duyệt phức tạp nào:

1. Viết bất biến của vòng lặp ra lề: "hàng trên đã đầy", "cột phải
   đã đầy", v.v.
2. Sau mỗi cạnh, dịch bức tường tương ứng và *nói vì sao* biên của
   cạnh kế vẫn hợp lệ.
3. Thử 1×n, n×1, và 1×1 trước mọi thứ khác. Đầu vào chữ nhật (không
   vuông) phá vỡ mã trông đối xứng.

Quy tắc cuối là thói quen nâng cao: lỗi không bao giờ nằm giữa lưới.
Nó nằm ở cột cuối, hàng đơn, hoặc bức tường đã thu.
"""

BOILER_2D = r"""public class Solution {
    public static int[][] process(int[][] g) {
        return new int[0][0]; // replace
    }
}
"""

BOILER_PT = r"""public class Solution {
    public static int process(int[][] g, int r, int c) {
        return 0; // replace
    }
}
"""

BOILER_2D_INT = r"""public class Solution {
    public static int process(int[][] g) {
        return 0; // replace
    }
}
"""

P_ROT = challenge(
    "apx-m7-rotate",
    "Rotate 90 degrees clockwise",
    "Return a **new** grid rotated 90° clockwise (the original must be "
    "untouched; the result may be non-square). Implement "
    "`process(int[][] g)`.\n\nExample: `{{1,2,3},{4,5,6}}` → "
    "`{{4,1},{5,2},{6,3}}`.",
    BOILER_2D,
    [(
        "clockwise rotation",
        r"""
int[][] out = Solution.process(new int[][]{{1, 2, 3}, {4, 5, 6}});
CjTestBase.checkEq(out, new int[][]{{4, 1}, {5, 2}, {6, 3}}, "2x3 becomes 3x2");
int[][] sq = Solution.process(new int[][]{{1, 2}, {3, 4}});
CjTestBase.checkEq(sq, new int[][]{{3, 1}, {4, 2}}, "square rotation");
""",
        "out[c][rows - 1 - r] = g[r][c]; dimensions swap (cols x rows).",
    )],
    level="independent",
    difficulty="advanced",
)

P_NB = challenge(
    "apx-m7-neighborsum",
    "Sum the neighbors",
    "Return the **sum of all in-bounds neighbors** of cell (r, c) — "
    "the 8 surrounding cells, excluding the cell itself. Implement "
    "`process(int[][] g, int r, int c)`.\n\nExample: in "
    "`{{1,2},{3,4}}`, cell (0,0) has neighbors 2, 3, 4 → `9`.",
    BOILER_PT,
    [(
        "neighbor sum",
        r"""
CjTestBase.checkEq(Solution.process(new int[][]{{1, 2}, {3, 4}}, 0, 0), 9, "corner has 3 neighbors");
CjTestBase.checkEq(Solution.process(new int[][]{{1, 2}, {3, 4}}, 1, 1), 6, "opposite corner");
CjTestBase.checkEq(Solution.process(new int[][]{{5}}, 0, 0), 0, "no neighbors");
""",
        "Offset table of 8 directions + bounds guard; the cell itself is never included.",
    )],
    level="guided",
    difficulty="intermediate",
)

P_PEAK = challenge(
    "apx-m7-peaks",
    "Count the peaks",
    "A cell is a **peak** if its value is strictly greater than the "
    "**average of its existing neighbors** (the in-bounds 8 "
    "neighbors — corners have 3, edges have 5; the cell itself never "
    "counts). Count the peaks. Implement `process(int[][] g)`.\n\n"
    "Example: `{{9,1},{1,1}}` → `1`.",
    BOILER_2D_INT,
    [(
        "peak count",
        r"""
CjTestBase.checkEq(Solution.process(new int[][]{{9, 1}, {1, 1}}), 1, "single sharp peak");
CjTestBase.checkEq(Solution.process(new int[][]{{5, 2, 5}, {2, 1, 2}, {5, 2, 5}}), 4, "four corners");
CjTestBase.checkEq(Solution.process(new int[][]{{2, 2}, {2, 2}}), 0, "no peaks");
""",
        "Reuse the neighbor pattern but ALSO count the in-bounds neighbors; divide the sum by that count (as a double).",
    )],
    level="combination",
    difficulty="advanced",
)

P_LEDGER = challenge(
    "apx-m7-ledger",
    "Per-column balances",
    "A ledger grid holds debits (negative) and credits (positive). "
    "Return the sum of the **absolute per-column balances** (sum each "
    "column, then add the absolute values of the column sums). "
    "Implement `process(int[][] g)`.\n\nExample: "
    "`{{5,-3,2},{-4,1,0}}` → column sums 1, -2, 2 → `1+2+2` = `5`.",
    BOILER_2D_INT,
    [(
        "column ledger",
        r"""
CjTestBase.checkEq(Solution.process(new int[][]{{5, -3, 2}, {-4, 1, 0}}), 5, "columns then abs");
CjTestBase.checkEq(Solution.process(new int[][]{{-1, -1}, {-1, -1}}), 4, "all negative columns");
CjTestBase.checkEq(Solution.process(new int[][]{{3}}), 3, "single cell");
""",
        "Column-major loop: for c outside, for r inside; abs applied to each finished column sum, not each cell.",
    )],
    level="independent",
    difficulty="advanced",
)

P_SPIRAL = challenge(
    "apx-m7-spiral",
    "Spiral fill",
    "Fill a `rows x cols` grid counting from 1 in **spiral order**: "
    "top row left→right, right column top→bottom, bottom row "
    "right→left, left column bottom→top, then shrink inward. Implement "
    "`fill(int rows, int cols)` returning the grid.\n\nExample: 3×4 → "
    "`{{1,2,3,4},{10,11,12,5},{9,8,7,6}}`.",
    r"""public class Solution {
    public static int[][] fill(int rows, int cols) {
        return new int[0][0]; // replace
    }
}
""",
    [(
        "spiral order",
        r"""
CjTestBase.checkEq(Solution.fill(3, 4), new int[][]{{1, 2, 3, 4}, {10, 11, 12, 5}, {9, 8, 7, 6}}, "3x4 spiral");
CjTestBase.checkEq(Solution.fill(1, 5), new int[][]{{1, 2, 3, 4, 5}}, "single row");
CjTestBase.checkEq(Solution.fill(3, 1), new int[][]{{1}, {2}, {3}}, "single column");
""",
        "Four shrinking walls (top/bottom/left/right) with re-checks before the bottom row and left column passes.",
    )],
    level="real-world",
    difficulty="advanced",
)

CP7 = challenge(
    "apx-cp-m7-symmetric",
    "Checkpoint: symmetric grid",
    "A square grid is **symmetric** if `g[r][c] == g[c][r]` for every "
    "r, c. Implement `process(int[][] g)` returning true/false "
    "(a 1×1 grid is trivially symmetric).\n\nExamples: "
    "`{{1,2},{2,1}}` → true, `{{1,2},{3,1}}` → false.",
    r"""public class Solution {
    public static boolean process(int[][] g) {
        return false; // replace
    }
}
""",
    [(
        "symmetry check",
        r"""
CjTestBase.checkTrue(Solution.process(new int[][]{{1, 2}, {2, 1}}), "2x2 symmetric");
CjTestBase.checkTrue(!Solution.process(new int[][]{{1, 2}, {3, 1}}), "2x2 asymmetric");
CjTestBase.checkTrue(Solution.process(new int[][]{{7}}), "1x1 trivially symmetric");
CjTestBase.checkTrue(Solution.process(new int[][]{{1, 2, 3}, {2, 5, 6}, {3, 6, 9}}), "3x3 symmetric");
""",
        "Compare each pair once (c starts at r + 1); any mismatch returns false immediately.",
    )],
    level="independent",
    difficulty="advanced",
)

VI_CP7 = vi_challenge(
    "Điểm kiểm tra: lưới đối xứng",
    "Lưới vuông **đối xứng** nếu `g[r][c] == g[c][r]` với mọi r, c. Cài "
    "đặt `process(int[][] g)` trả true/false (lưới 1×1 hiển nhiên đối "
    "xứng).\n\nVí dụ: `{{1,2},{2,1}}` → true, `{{1,2},{3,1}}` → false.",
    [("symmetry check", "So sánh từng cặp một lần (c bắt đầu từ r + 1); bất kỳ lệch nào trả false ngay.")],
)

write_practice(
    M, "apx-p7-grids", "Grid lab: axes, neighborhoods, walls",
    "Five traversal problems where every hidden test lives on a boundary.",
    "Phòng thí nghiệm lưới: trục, vùng lân cận, bức tường",
    "Năm bài duyệt mà mọi test ẩn đều nằm trên một biên.",
    after_lesson="apx-m7-bounds", minutes=60, difficulty="advanced",
    challenges=[P_NB, P_LEDGER, P_ROT, P_PEAK, P_SPIRAL],
    vi_challenges={
        "apx-m7-rotate": vi_challenge(
            "Xoay 90 độ theo chiều kim đồng hồ",
            "Trả về lưới **mới** đã xoay 90° theo chiều kim đồng hồ (lưới gốc "
            "phải nguyên vẹn; kết quả có thể không vuông). Cài đặt "
            "`process(int[][] g)`.\n\nVí dụ: `{{1,2,3},{4,5,6}}` → "
            "`{{4,1},{5,2},{6,3}}`.",
            [("clockwise rotation", "out[c][rows - 1 - r] = g[r][c]; hai kích thước đổi chỗ (cols x rows).")],
        ),
        "apx-m7-neighborsum": vi_challenge(
            "Cộng các láng giềng",
            "Trả về **tổng các láng giềng trong biên** của ô (r, c) — 8 ô "
            "xung quanh, không tính chính ô đó. Cài đặt "
            "`process(int[][] g, int r, int c)`.\n\nVí dụ: trong "
            "`{{1,2},{3,4}}`, ô (0,0) có láng giềng 2, 3, 4 → `9`.",
            [("neighbor sum", "Bảng 8 hướng + biến chặn biên; chính ô đó không bao giờ được tính.")],
        ),
        "apx-m7-peaks": vi_challenge(
            "Đếm các đỉnh",
            "Một ô là **đỉnh** nếu giá trị của nó lớn hơn hoàn toàn **trung "
            "bình các láng giềng thực tế** (8 hướng trong biên — góc có 3, "
            "cạnh có 5; chính ô không đếm). Đếm số đỉnh. Cài đặt "
            "`process(int[][] g)`.\n\nVí dụ: `{{9,1},{1,1}}` → `1`.",
            [("peak count", "Dùng mẫu láng giềng nhưng ĐỒNG THỜI đếm số láng giềng trong biên; chia tổng cho số đó (dạng double).")],
        ),
        "apx-m7-ledger": vi_challenge(
            "Số dư từng cột",
            "Lưới sổ cái chứa ghi nợ (âm) và ghi có (dương). Trả về tổng "
            "**trị tuyệt đối của số dư từng cột** (cộng mỗi cột, rồi cộng các "
            "giá trị tuyệt đối của tổng cột). Cài đặt `process(int[][] g)`.\n\n"
            "Ví dụ: `{{5,-3,2},{-4,1,0}}` → tổng cột 1, -2, 2 → `1+2+2` = `5`.",
            [("column ledger", "Vòng lặp theo cột: for c ngoài, for r trong; abs áp cho tổng cột hoàn thành, không áp cho từng ô.")],
        ),
        "apx-m7-spiral": vi_challenge(
            "Điền xoắn ốc",
            "Điền lưới `rows x cols` đếm từ 1 theo **thứ tự xoắn ốc**: hàng "
            "trên trái→phải, cột phải trên→dưới, hàng dưới phải→trái, cột "
            "trái dưới→trên, rồi thu vào. Cài đặt `fill(int rows, int cols)` "
            "trả về lưới.\n\nVí dụ: 3×4 → "
            "`{{1,2,3,4},{10,11,12,5},{9,8,7,6}}`.",
            [("spiral order", "Bốn bức tường thu nhỏ (trên/dưới/trái/phải) với kiểm tra lại trước các lượt hàng dưới và cột trái.")],
        ),
    },
    solutions=[
        ("apx-m7-rotate", r"""public class Solution {
    public static int[][] process(int[][] g) {
        int rows = g.length;
        int cols = g[0].length;
        int[][] out = new int[cols][rows];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                out[c][rows - 1 - r] = g[r][c];
            }
        }
        return out;
    }
}
""", r"""public class Solution {
    // BUG: counter-clockwise rotation — wrong index on the new row
    public static int[][] process(int[][] g) {
        int rows = g.length;
        int cols = g[0].length;
        int[][] out = new int[cols][rows];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                out[cols - 1 - c][r] = g[r][c];
            }
        }
        return out;
    }
}
"""),
        ("apx-m7-neighborsum", r"""public class Solution {
    public static int process(int[][] g, int r, int c) {
        int[] dr = {-1, -1, -1, 0, 0, 1, 1, 1};
        int[] dc = {-1, 0, 1, -1, 1, -1, 0, 1};
        int sum = 0;
        for (int d = 0; d < 8; d++) {
            int nr = r + dr[d];
            int nc = c + dc[d];
            if (nr >= 0 && nr < g.length && nc >= 0 && nc < g[0].length) {
                sum += g[nr][nc];
            }
        }
        return sum;
    }
}
""", r"""public class Solution {
    // BUG: includes the cell itself — self counts as a neighbor
    public static int process(int[][] g, int r, int c) {
        int[] dr = {-1, -1, -1, 0, 0, 1, 1, 1};
        int[] dc = {-1, 0, 1, -1, 1, -1, 0, 1};
        int sum = 0;
        for (int d = 0; d < 8; d++) {
            int nr = r + dr[d];
            int nc = c + dc[d];
            if (nr >= 0 && nr < g.length && nc >= 0 && nc < g[0].length) {
                sum += g[nr][nc];
            }
        }
        return sum + g[r][c];
    }
}
"""),
        ("apx-m7-peaks", r"""public class Solution {
    public static int process(int[][] g) {
        int[] dr = {-1, -1, -1, 0, 0, 1, 1, 1};
        int[] dc = {-1, 0, 1, -1, 1, -1, 0, 1};
        int count = 0;
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                int sum = 0;
                int cnt = 0;
                for (int d = 0; d < 8; d++) {
                    int nr = r + dr[d];
                    int nc = c + dc[d];
                    if (nr >= 0 && nr < g.length && nc >= 0 && nc < g[0].length) {
                        sum += g[nr][nc];
                        cnt++;
                    }
                }
                if (g[r][c] * cnt > sum) {
                    count++;
                }
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // BUG: divides by 8 always — corners and edges misjudged
    public static int process(int[][] g) {
        int[] dr = {-1, -1, -1, 0, 0, 1, 1, 1};
        int[] dc = {-1, 0, 1, -1, 1, -1, 0, 1};
        int count = 0;
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                int sum = 0;
                for (int d = 0; d < 8; d++) {
                    int nr = r + dr[d];
                    int nc = c + dc[d];
                    if (nr >= 0 && nr < g.length && nc >= 0 && nc < g[0].length) {
                        sum += g[nr][nc];
                    }
                }
                if (g[r][c] * 8 > sum) {
                    count++;
                }
            }
        }
        return count;
    }
}
"""),
        ("apx-m7-ledger", r"""public class Solution {
    public static int process(int[][] g) {
        int total = 0;
        for (int c = 0; c < g[0].length; c++) {
            int col = 0;
            for (int r = 0; r < g.length; r++) {
                col += g[r][c];
            }
            total += Math.abs(col);
        }
        return total;
    }
}
""", r"""public class Solution {
    // BUG: sums absolute VALUES per cell instead of per column balance
    public static int process(int[][] g) {
        int total = 0;
        for (int c = 0; c < g[0].length; c++) {
            for (int r = 0; r < g.length; r++) {
                total += Math.abs(g[r][c]);
            }
        }
        return total;
    }
}
"""),
        ("apx-m7-spiral", r"""public class Solution {
    public static int[][] fill(int rows, int cols) {
        int[][] g = new int[rows][cols];
        int v = 1;
        int top = 0;
        int bottom = rows - 1;
        int left = 0;
        int right = cols - 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) {
                g[top][c] = v;
                v++;
            }
            top++;
            for (int r = top; r <= bottom; r++) {
                g[r][right] = v;
                v++;
            }
            right--;
            if (top <= bottom) {
                for (int c = right; c >= left; c--) {
                    g[bottom][c] = v;
                    v++;
                }
                bottom--;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; r--) {
                    g[r][left] = v;
                    v++;
                }
                left++;
            }
        }
        return g;
    }
}
""", r"""public class Solution {
    // BUG: missing the re-check before the bottom row — single-column grids double-count
    public static int[][] fill(int rows, int cols) {
        int[][] g = new int[rows][cols];
        int v = 1;
        int top = 0;
        int bottom = rows - 1;
        int left = 0;
        int right = cols - 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) {
                g[top][c] = v;
                v++;
            }
            top++;
            for (int r = top; r <= bottom; r++) {
                g[r][right] = v;
                v++;
            }
            right--;
            for (int c = right; c >= left; c--) {
                g[bottom][c] = v;
                v++;
            }
            bottom--;
            if (left <= right) {
                for (int r = bottom; r >= top; r--) {
                    g[r][left] = v;
                    v++;
                }
                left++;
            }
        }
        return g;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m7", "Checkpoint: symmetry",
    "Pairwise comparison checkpoint: compare each pair once, fail fast.",
    15,
    r"""
Symmetry is the purest 2D-indices exercise: every element must meet
its mirror, each pair checked exactly once, and the first mismatch
ends the scan. Compare against your instinct to check every cell
twice (harmless) or only the upper triangle against the wrong index
(fatal).
""",
    "Điểm kiểm tra: đối xứng",
    "Bài kiểm tra so sánh từng cặp: mỗi cặp so đúng một lần, lệch là dừng.",
    r"""
Đối xứng là bài tập chỉ số 2D thuần khiết nhất: mọi phần tử phải gặp
ảnh gương của nó, mỗi cặp so đúng một lần, và lệch đầu tiên kết thúc
lượt quét. Đối chiếu với phản xạ kiểm tra mọi ô hai lần (vô hại) hoặc
chỉ hình tam giác trên nhưng đối chiếu sai chỉ số (chí mạng).
""",
    CP7,
    VI_CP7,
    solution=r"""public class Solution {
    public static boolean process(int[][] g) {
        for (int r = 0; r < g.length; r++) {
            for (int c = r + 1; c < g.length; c++) {
                if (g[r][c] != g[c][r]) {
                    return false;
                }
            }
        }
        return true;
    }
}
""",
    wrong=r"""public class Solution {
    // BUG: compares against the wrong mirror index (c - r instead of c, r)
    public static boolean process(int[][] g) {
        for (int r = 0; r < g.length; r++) {
            for (int c = r + 1; c < g.length; c++) {
                if (g[r][c] != g[c - r][r]) {
                    return false;
                }
            }
        }
        return true;
    }
}
""",
)

print("M7 done")
