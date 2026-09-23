#!/usr/bin/env python3
"""AP CSA M15 — 2D Arrays: rows/columns, nested traversal, aggregation, grid search."""
from apc import *

M = "apc-2d"

L1 = r"""
A **2D array** is an array of arrays — rows first, then columns:

```java
int[][] grid = new int[3][4];      // 3 rows, 4 columns, all zeros
int[][] g2 = { {1, 2, 3}, {4, 5, 6} };   // 2 rows, 3 columns
```

Indexing is `grid[row][col]`, both zero-based. `grid[0]` is the whole
first **row** (it is itself an `int[]`), `grid[0][2]` is one element.

The lengths trick: `grid.length` is the number of rows,
`grid[0].length` is the number of columns. They are NOT the same
variable, and mixing them up is the classic bounds bug:

```java
for (int r = 0; r < grid.length; r++) {          // rows
    for (int c = 0; c < grid[0].length; c++) {   // columns of that row
        System.out.print(grid[r][c] + " ");
    }
    System.out.println();
}
```

**Row-major order** — this outer-rows / inner-columns pattern — is how
almost every AP 2D problem starts. Say the loop bounds out loud: "r goes
over rows, c goes over the columns of row r."
"""

L2 = r"""
Aggregation over a grid is the same accumulator pattern from 1D arrays,
applied per-row, per-column, or over everything:

```java
// row sums: one answer per row
public static int[] rowSums(int[][] g) {
    int[] sums = new int[g.length];
    for (int r = 0; r < g.length; r++) {
        int s = 0;                       // reset PER ROW — inside loop 1
        for (int c = 0; c < g[0].length; c++) {
            s += g[r][c];
        }
        sums[r] = s;
    }
    return sums;
}
```

Two placement bugs that cause half the wrong answers:

- Accumulator declared **outside** the row loop: sums accumulate down
  the whole grid (running total instead of per-row totals).
- Reset placed inside the **column** loop: every accumulator dies after
  one column.

Column traversal just swaps which loop is outside:

```java
for (int c = 0; c < g[0].length; c++) {      // columns outside
    for (int r = 0; r < g.length; r++) {
        // g[r][c] walks DOWN column c
    }
}
```

Both loops stay; only their bounds and index order swap.
"""

L3 = r"""
**Searching a grid** — find a value and report where it lives:

```java
// returns {row, col} or null if absent
public static int[] find(int[][] g, int target) {
    for (int r = 0; r < g.length; r++) {
        for (int c = 0; c < g[0].length; c++) {
            if (g[r][c] == target) {
                return new int[] {r, c};
            }
        }
    }
    return null;
}
```

Three habits from this snippet that recur on FRQ 4:

- **Early return** the moment the target is found — no flag needed.
- **Return null** (or a sentinel like -1) when not found; the contract
  must say which. `null` means "no object here" — calling a method on
  it throws `NullPointerException`.
- Test the **not-found** path on purpose. Un-tested contracts rot.

Grid size conventions: many AP grids are **square-ish** or have
different row/column counts on purpose — `{{1,2,3},{4,5}}` is legal
(a "ragged" shape, though the exam's grids are usually rectangular).
Never assume rows and columns are interchangeable: `g[r][c]` and
`g[c][r]` are different cells, and one of them may not exist.
"""

write_module(
    M,
    "2D Arrays",
    "Grids of rows and columns: nested traversal, per-row aggregation, and coordinate search.",
    "Mảng hai chiều",
    "Lưới hàng và cột: duyệt lồng nhau, tổng hợp theo hàng, và tìm kiếm theo tọa độ.",
    lessons=["apc-m15-grid", "apc-m15-agg", "apc-m15-find", "apc-cp-m15"],
    practices=["apc-p15-2d"],
)

write_lesson(
    M, "apc-m15-grid", "Grid layout and nested traversal",
    "2D indexing, lengths trick, row-major pattern, common bounds bugs.",
    12, L1,
    "Bố cục lưới và duyệt lồng nhau",
    "Chỉ số 2D, mẹo lấy kích thước, mẫu duyệt theo hàng, các lỗi cận điển hình.",
    r"""
Mảng **hai chiều** là mảng của các mảng — hàng trước, cột sau:

```java
int[][] grid = new int[3][4];      // 3 hàng, 4 cột, toàn số 0
int[][] g2 = { {1, 2, 3}, {4, 5, 6} };   // 2 hàng, 3 cột
```

Chỉ số là `grid[row][col]`, đều bắt đầu từ 0. `grid[0]` là cả **hàng**
đầu tiên (bản thân nó là một `int[]`), `grid[0][2]` là một phần tử.

Mẹo lấy kích thước: `grid.length` là số hàng, `grid[0].length` là số
cột. Đây KHÔNG phải cùng một biến, và nhầm lẫn chúng là lỗi cận kinh điển:

```java
for (int r = 0; r < grid.length; r++) {          // các hàng
    for (int c = 0; c < grid[0].length; c++) {   // cột của hàng đó
        System.out.print(grid[r][c] + " ");
    }
    System.out.println();
}
```

**Duyệt theo hàng-chính** — mẫu ngoài-hàng / trong-cột — là khởi đầu
của gần mọi bài 2D trong đề. Đọc to cận của vòng lặp: "r chạy trên các
hàng, c chạy trên các cột của hàng r."
""",
)

write_lesson(
    M, "apc-m15-agg", "Row and column aggregation",
    "Accumulators per row, per column, or whole-grid; where the reset goes.",
    12, L2,
    "Tổng hợp theo hàng và cột",
    "Bộ tích lũy theo hàng, theo cột, hay toàn lưới; vị trí đặt lệnh reset.",
    r"""
Tổng hợp trên lưới chính là mẫu bộ tích lũy từ mảng 1D, áp dụng theo
hàng, theo cột, hoặc trên toàn bộ:

```java
// tổng từng hàng: một kết quả mỗi hàng
public static int[] rowSums(int[][] g) {
    int[] sums = new int[g.length];
    for (int r = 0; r < g.length; r++) {
        int s = 0;                       // reset CHO TỪNG HÀNG — trong vòng 1
        for (int c = 0; c < g[0].length; c++) {
            s += g[r][c];
        }
        sums[r] = s;
    }
    return sums;
}
```

Hai lỗi đặt chỗ gây ra một nửa đáp án sai:

- Bộ tích lũy khai báo **ngoài** vòng hàng: tổng cộng dồn xuống cả lưới
  (tổng chạy thay vì tổng từng hàng).
- Lệnh reset đặt trong vòng **cột**: bộ tích lũy chết sau một cột.

Duyệt theo cột chỉ là đổi vòng nào ở ngoài:

```java
for (int c = 0; c < g[0].length; c++) {      // cột ở ngoài
    for (int r = 0; r < g.length; r++) {
        // g[r][c] đi XUỐNG cột c
    }
}
```

Cả hai vòng vẫn còn; chỉ đổi cận và thứ tự chỉ số.
""",
)

write_lesson(
    M, "apc-m15-find", "Grid search and the null contract",
    "Coordinate search with early return, null contracts, not-found testing.",
    12, L3,
    "Tìm trên lưới và hợp đồng null",
    "Tìm theo tọa độ với early return, hợp đồng null, kiểm thử trường hợp không thấy.",
    r"""
**Tìm kiếm trên lưới** — tìm một giá trị và báo nó ở đâu:

```java
// trả {row, col} hoặc null nếu không có
public static int[] find(int[][] g, int target) {
    for (int r = 0; r < g.length; r++) {
        for (int c = 0; c < g[0].length; c++) {
            if (g[r][c] == target) {
                return new int[] {r, c};
            }
        }
    }
    return null;
}
```

Ba thói quen từ đoạn mã này lặp lại trên FRQ 4:

- **Early return** ngay khi thấy mục tiêu — không cần cờ.
- **Trả null** (hoặc giá trị đặc biệt như -1) khi không thấy; hợp đồng
  phải nói rõ chọn cái nào. `null` nghĩa là "không có đối tượng ở đây"
  — gọi phương thức trên nó sẽ ném `NullPointerException`.
- Cố tình kiểm tra đường **không-thấy**. Hợp đồng không được kiểm thử
  sẽ mục ruỗng.

Quy ước kích thước: nhiều lưới trong đề là **vuông** hoặc cố ý có số
hàng/cột khác nhau — `{{1,2,3},{4,5}}` là hợp lệ (dạng "răng lược",
dù lưới trong đề thường là hình chữ nhật). Đừng bao giờ giả định hàng
và cột hoán đổi được cho nhau: `g[r][c]` và `g[c][r]` là hai ô khác
nhau, và một trong hai có thể không tồn tại.
""",
)

BOILER_SUMS = r"""public class Solution {
    public static int[] rowSums(int[][] g) {
        // complete: one sum per row
        return new int[g.length];
    }
}
"""

BOILER_TRANSPOSE = r"""public class Solution {
    public static int[][] transpose(int[][] g) {
        // complete: result has g[0].length rows and g.length columns;
        // result[c][r] == g[r][c]
        return new int[g[0].length][g.length];
    }
}
"""

BOILER_COUNT = r"""public class Solution {
    public static int countOnPath(int[][] g) {
        // complete: count cells with value 1 that lie in row 0, the last
        // column, or on the main diagonal
        return 0;
    }
}
"""

BOILER_FIND = r"""public class Solution {
    public static int[] find(int[][] g, int target) {
        // complete: return {row, col} of the first match in row-major
        // order, or null if absent
        return null;
    }
}
"""

BOILER_FIXSUM = r"""public class Solution {
    public static int[] rowSums(int[][] g) {
        // BUG: original flaw kept — the accumulator is declared OUTSIDE
        // the row loop, so each row's "sum" is a running total of the
        // whole grid so far
        int s = 0;
        int[] sums = new int[g.length];
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            sums[r] = s;
        }
        return sums;
    }
}
"""

CP15 = r"""public class Solution {
    public static int largestRow(int[][] g) {
        // complete: return the INDEX of the row with the largest sum;
        // if several rows tie, return the smallest index
        return 0;
    }
}
"""

P_SUMS = challenge(
    "apc-m15-rowsums",
    "Row sums",
    "Implement `rowSums(int[][] g)`: return a new array where `sums[r]` is the sum of row `r`. The accumulator must reset for every row.",
    BOILER_SUMS,
    [(
        "mixed shape",
        r"""
CjTestBase.checkEq(Solution.rowSums(new int[][] { {1, 2, 3}, {4, 5, 6} }), new int[] {6, 15}, "two rows");
CjTestBase.checkEq(Solution.rowSums(new int[][] { {10, 0, 0}, {-5, 5, 20} }), new int[] {10, 20}, "uneven totals, same shape");
CjTestBase.checkEq(Solution.rowSums(new int[][] { {} }), new int[] {0}, "empty row sums to 0");
""",
        "declare the accumulator inside the outer (row) loop, before the column loop.",
    )],
    level="imitation",
)

P_TRANS = challenge(
    "apc-m15-transpose",
    "Transpose",
    "Implement `transpose(int[][] g)`: return a new grid where `result[c][r] == g[r][c]` — rows become columns. Build the result with `new int[g[0].length][g.length]`.",
    BOILER_TRANSPOSE,
    [(
        "asymmetric shape",
        r"""
int[][] g = { {1, 2, 3}, {4, 5, 6} };
CjTestBase.checkEq(Solution.transpose(g), new int[][] { {1, 4}, {2, 5}, {3, 6} }, "2x3 becomes 3x2");
CjTestBase.checkEq(Solution.transpose(new int[][] { {7} }), new int[][] { {7} }, "1x1 fixed point");
""",
        "result[c][r] = g[r][c]; get the result dimensions in the right order.",
    )],
    level="guided",
)

P_COUNT = challenge(
    "apc-m15-countpath",
    "Count the path cells",
    "Implement `countOnPath(int[][] g)`: count cells whose value is 1 that lie in **row 0**, in the **last column**, or on the **main diagonal** (cells where row == col). A cell satisfying several conditions still counts once.",
    BOILER_COUNT,
    [(
        "overlap counted once",
        r"""
CjTestBase.checkEq(Solution.countOnPath(new int[][] { {1, 1}, {0, 1} }), 3, "all three 1-cells are on the path");
CjTestBase.checkEq(Solution.countOnPath(new int[][] { {0, 1}, {1, 0} }), 1, "only the row-0 cell is on the path");
CjTestBase.checkEq(Solution.countOnPath(new int[][] { {0, 0}, {0, 0} }), 0, "none");
""",
        "check each cell once in one pass; a condition chain with else avoids double counting.",
    )],
    level="independent",
)

P_FIND = challenge(
    "apc-m15-findcell",
    "Find with a null contract",
    "Implement `find(int[][] g, int target)`: return `{row, col}` of the FIRST match in row-major order, or `null` when absent.",
    BOILER_FIND,
    [(
        "first match + not found",
        r"""
int[][] g = { {9, 4}, {4, 4} };
CjTestBase.checkEq(Solution.find(g, 4), new int[] {0, 1}, "first match wins");
CjTestBase.checkTrue(Solution.find(g, 7) == null, "absent returns null");
CjTestBase.checkTrue(Solution.find(new int[][] {}, 1) == null, "empty grid, still null");
""",
        "return inside the loops the moment you see the target; return null after both loops.",
    )],
    level="independent",
)

P_FIX = challenge(
    "apc-m15-fix-rowsums",
    "Debug: running totals instead of row sums",
    "`rowSums` compiles and returns the right *shape*, but each entry is a running total of the grid so far instead of that row's sum. Fix the accumulator placement (signature stays the same).",
    BOILER_FIXSUM,
    [(
        "row sums repaired",
        r"""
CjTestBase.checkEq(Solution.rowSums(new int[][] { {1, 2}, {10, 20} }), new int[] {3, 30}, "per-row, not cumulative");
CjTestBase.checkEq(Solution.rowSums(new int[][] { {5}, {5}, {5} }), new int[] {5, 5, 5}, "three equal rows");
""",
        "move the accumulator declaration INSIDE the outer loop so each row starts from 0.",
    )],
    level="debugging",
)

CP15C = challenge(
    "apc-cp-m15-largestrow",
    "Checkpoint: largest row",
    "Implement `largestRow(int[][] g)`: return the **index** of the row with the largest sum. On ties, return the smallest index. Assume `g` has at least one row.",
    CP15,
    [(
        "tie goes to the first",
        r"""
CjTestBase.checkEq(Solution.largestRow(new int[][] { {0, 0}, {3, 0}, {0, 3} }), 1, "rows 1 and 2 tie at 3, smallest index");
CjTestBase.checkEq(Solution.largestRow(new int[][] { {0, 0}, {5, 0} }), 1, "clear winner");
CjTestBase.checkEq(Solution.largestRow(new int[][] { {9} }), 0, "single row");
""",
        "track bestIndex + bestSum; update only on strictly greater (>), not >=.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p15-2d", "2D array reps", "Row sums, transpose, path counting, coordinate search, accumulator debugging.",
    "Luyện mảng hai chiều", "Tổng hàng, hoán vị, đếm ô trên đường, tìm tọa độ, gỡ lỗi bộ tích lũy.",
    after_lesson="apc-m15-find", minutes=55, difficulty="beginner",
    challenges=[P_SUMS, P_TRANS, P_COUNT, P_FIND, P_FIX],
    vi_challenges={
        "apc-m15-rowsums": vi_challenge("Tổng từng hàng", "Cài đặt `rowSums(int[][] g)`: trả mảng mới với `sums[r]` là tổng của hàng `r`. Bộ tích lũy phải reset sau mỗi hàng.",
            [("mixed shape", "khai báo bộ tích lũy trong vòng ngoài (vòng hàng), trước vòng cột.")]),
        "apc-m15-transpose": vi_challenge("Hoán vị", "Cài đặt `transpose(int[][] g)`: trả lưới mới với `result[c][r] == g[r][c]` — hàng thành cột. Dựng kết quả bằng `new int[g[0].length][g.length]`.",
            [("asymmetric shape", "result[c][r] = g[r][c]; đặt kích thước kết quả đúng thứ tự.")]),
        "apc-m15-countpath": vi_challenge("Đếm ô trên đường", "Cài đặt `countOnPath(int[][] g)`: đếm ô có giá trị 1 nằm ở **hàng 0**, **cột cuối**, hoặc trên **đường chéo chính** (ô có hàng == cột). Ô thỏa nhiều điều kiện vẫn chỉ đếm một lần.",
            [("overlap counted once", "mỗi ô chỉ xét một lần trong một lượt; chuỗi điều kiện có else tránh đếm trùng.")]),
        "apc-m15-findcell": vi_challenge("Tìm với hợp đồng null", "Cài đặt `find(int[][] g, int target)`: trả `{row, col}` của lần khớp ĐẦU TIÊN theo thứ tự hàng-chính, hoặc `null` khi không có.",
            [("first match + not found", "return ngay trong vòng lặp khi thấy mục tiêu; trả null sau cả hai vòng.")]),
        "apc-m15-fix-rowsums": vi_challenge("Gỡ lỗi: tổng chạy thay vì tổng hàng", "`rowSums` biên dịch và trả đúng *hình dạng*, nhưng mỗi phần tử là tổng chạy của cả lưới tính đến thời điểm đó thay vì tổng của hàng đó. Sửa vị trí bộ tích lũy (chữ ký giữ nguyên).",
            [("row sums repaired", "chuyển khai báo bộ tích lũy vào TRONG vòng ngoài để mỗi hàng bắt đầu từ 0.")]),
    },
    solutions=[
        ("apc-m15-rowsums", r"""public class Solution {
    public static int[] rowSums(int[][] g) {
        int[] sums = new int[g.length];
        for (int r = 0; r < g.length; r++) {
            int s = 0;
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            sums[r] = s;
        }
        return sums;
    }
}
""", r"""public class Solution {
    public static int[] rowSums(int[][] g) {
        int[] sums = new int[g.length];
        int s = 0;
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            sums[r] = s;
        }
        return sums;
    }
}
"""),
        ("apc-m15-transpose", r"""public class Solution {
    public static int[][] transpose(int[][] g) {
        int[][] result = new int[g[0].length][g.length];
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                result[c][r] = g[r][c];
            }
        }
        return result;
    }
}
""", r"""public class Solution {
    public static int[][] transpose(int[][] g) {
        int[][] result = new int[g.length][g[0].length];
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                result[c][r] = g[r][c];
            }
        }
        return result;
    }
}
"""),
        ("apc-m15-countpath", r"""public class Solution {
    public static int countOnPath(int[][] g) {
        int count = 0;
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                if (g[r][c] != 1) {
                    continue;
                }
                boolean path = (r == 0) || (c == g[0].length - 1) || (r == c);
                if (path) {
                    count++;
                }
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    public static int countOnPath(int[][] g) {
        // BUG: counts every 1-cell anywhere in the grid — the path
        // conditions were dropped
        int count = 0;
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                if (g[r][c] == 1) {
                    count++;
                }
            }
        }
        return count;
    }
}
"""),
        ("apc-m15-findcell", r"""public class Solution {
    public static int[] find(int[][] g, int target) {
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                if (g[r][c] == target) {
                    return new int[] {r, c};
                }
            }
        }
        return null;
    }
}
""", r"""public class Solution {
    public static int[] find(int[][] g, int target) {
        // BUG: keeps scanning after a match — returns the LAST match,
        // violating the first-match contract
        int[] hit = null;
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                if (g[r][c] == target) {
                    hit = new int[] {r, c};
                }
            }
        }
        return hit;
    }
}
"""),
        ("apc-m15-fix-rowsums", r"""public class Solution {
    public static int[] rowSums(int[][] g) {
        int[] sums = new int[g.length];
        for (int r = 0; r < g.length; r++) {
            int s = 0;
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            sums[r] = s;
        }
        return sums;
    }
}
""", r"""public class Solution {
    public static int[] rowSums(int[][] g) {
        // BUG: original flaw kept — accumulator declared outside the
        // row loop, producing running totals
        int s = 0;
        int[] sums = new int[g.length];
        for (int r = 0; r < g.length; r++) {
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            sums[r] = s;
        }
        return sums;
    }
}
"""),
        ("apc-cp-m15-largestrow", r"""public class Solution {
    public static int largestRow(int[][] g) {
        int bestIndex = 0;
        int bestSum = Integer.MIN_VALUE;
        for (int r = 0; r < g.length; r++) {
            int s = 0;
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            if (s > bestSum) {
                bestSum = s;
                bestIndex = r;
            }
        }
        return bestIndex;
    }
}
""", r"""public class Solution {
    public static int largestRow(int[][] g) {
        // BUG: uses >= so ties overwrite bestIndex — the LAST tied row
        // wins instead of the first
        int bestIndex = 0;
        int bestSum = Integer.MIN_VALUE;
        for (int r = 0; r < g.length; r++) {
            int s = 0;
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            if (s >= bestSum) {
                bestSum = s;
                bestIndex = r;
            }
        }
        return bestIndex;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m15", "Checkpoint: largest row",
    "Per-row aggregation with a tie-breaking contract — the FRQ 4 core loop.",
    25,
    r"""
The pattern: aggregate per row, keep a best-so-far, and honor the tie
rule (`>` keeps the first tied index; `>=` silently hands ties to the
last). One comparison operator is the entire difference between a
correct and a subtly wrong answer.
""",
    "Điểm kiểm tra: hàng lớn nhất",
    "Tổng hợp theo từng hàng với hợp đồng phá hòa — lõi của FRQ 4.",
    r"""
Mẫu hình: tổng hợp theo từng hàng, giữ best-so-far, và tôn trọng luật
hòa (`>` giữ chỉ số hòa ĐẦU TIÊN; `>=` lặng lẽ trao hòa cho hàng CUỐI).
Một toán tử so sánh là toàn bộ khoảng cách giữa đáp án đúng và đáp án
sai tinh vi.
""",
    CP15C,
    vi_challenge("Điểm kiểm tra: hàng lớn nhất", "Cài đặt `largestRow(int[][] g)`: trả **chỉ số** của hàng có tổng lớn nhất. Khi hòa, trả chỉ số nhỏ nhất. Giả định `g` có ít nhất một hàng.",
        [("tie goes to the first", "theo dõi bestIndex + bestSum; chỉ cập nhật khi lớn hơn hẳn (>), không dùng >=.")]),
    solution=r"""public class Solution {
    public static int largestRow(int[][] g) {
        int bestIndex = 0;
        int bestSum = Integer.MIN_VALUE;
        for (int r = 0; r < g.length; r++) {
            int s = 0;
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            if (s > bestSum) {
                bestSum = s;
                bestIndex = r;
            }
        }
        return bestIndex;
    }
}
""",
    wrong=r"""public class Solution {
    public static int largestRow(int[][] g) {
        // BUG: uses >= so ties overwrite bestIndex — the LAST tied row
        // wins instead of the first
        int bestIndex = 0;
        int bestSum = Integer.MIN_VALUE;
        for (int r = 0; r < g.length; r++) {
            int s = 0;
            for (int c = 0; c < g[0].length; c++) {
                s += g[r][c];
            }
            if (s >= bestSum) {
                bestSum = s;
                bestIndex = r;
            }
        }
        return bestIndex;
    }
}
""",
)
