#!/usr/bin/env python3
"""AP CSA Core M8 — 2D Array Mastery (orientation + neighbors + paths)."""
from apcc import *

M = "cx-2d"

L1 = r"""
A 2D array is an array of rows. `int[][] g = new int[3][4]` is 3 rows of
4 columns; `g.length` is 3 (rows), `g[0].length` is 4 (columns). The
single most reliable exam fact: **`g[r][c]` — row first, always.**

**Row-major traversal** (the natural order):
```java
for (int r = 0; r < g.length; r++) {
    for (int c = 0; c < g[r].length; c++) {
        // g[r][c]
    }
}
```
Inner bound `g[r].length` (not `g[0].length`) is the exam-safe form —
it works even if rows had different lengths, and it is what the
reference solutions accept.

**Column traversal** — outer loop over columns, inner over rows:
```java
for (int c = 0; c < g[0].length; c++) {
    for (int r = 0; r < g.length; r++) {
        // g[r][c] — walks DOWN one column
    }
}
```

Position vocabulary for {1,2,3},{4,5,6}: g[0] is the FIRST row
(1,2,3); g[2][0] is row index 2, column 0 → value 6... no — check:
`{ {1,2,3}, {4,5,6} }` has 2 rows; `g[1][0]` is 4. Draw the grid with
indexes labeled before answering anything. Every wrong "which element"
MCQ comes from row/column transposition.
"""

L2 = r"""
Two scanning shapes beyond the basics:

**Find a position, return coordinates.** When the answer is a place,
return the row (or a coded r/c pair) — and decide what happens when
absent (−1 is conventional):

```java
public static int findRow(int[][] g, int target) {
    for (int r = 0; r < g.length; r++) {
        for (int c = 0; c < g[r].length; c++) {
            if (g[r][c] == target) {
                return r;
            }
        }
    }
    return -1;
}
```

Note the **double early-exit**: the inner return leaves both loops at
once. A `break` would only leave the inner loop — a classic MCQ
distinction.

**Neighbors of g[r][c]** — up to four orthogonal friends, but edges
have fewer. Guard each direction independently:

```java
if (r > 0) { ... g[r - 1][c] ... }
if (r < g.length - 1) { ... g[r + 1][c] ... }
if (c > 0) { ... g[r][c - 1] ... }
if (c < g[r].length - 1) { ... g[r][c + 1] ... }
```

Or count matching neighbors:

```java
int count = 0;
if (r > 0 && g[r - 1][c] == v) { count++; }
if (r < g.length - 1 && g[r + 1][c] == v) { count++; }
if (c > 0 && g[r][c - 1] == v) { count++; }
if (c < g[r].length - 1 && g[r][c + 1] == v) { count++; }
```

Never index `g[r-1]` before checking `r > 0` — the negative index
throws before the value is even read.
"""

L3 = r"""
**Column aggregation** — the classic "compute per-column totals" task:

```java
public static int[] colSums(int[][] g) {
    int[] sums = new int[g[0].length];
    for (int c = 0; c < g[0].length; c++) {
        for (int r = 0; r < g.length; r++) {
            sums[c] += g[r][c];
        }
    }
    return sums;
}
```

The output array is sized by COLUMNS; the loops read column-major. Two
orientations in one method — draw which loop walks which direction
until it is automatic.

**Transformations** that read and write the same array need care:
swapping rows uses a temporary one-row array:

```java
int[] tmp = g[a];
g[a] = g[b];
g[b] = tmp;
```

That is O(1) — row references swap, no element copying. Compare with
transposing (rows become columns), which needs element-by-element copy
into a NEW array of swapped dimensions:

```java
int[][] t = new int[g[0].length][g.length];
for (int r = 0; r < g.length; r++) {
    for (int c = 0; c < g[r].length; c++) {
        t[c][r] = g[r][c];
    }
}
```

Both directions appear on exams; the swap copies nothing, the transpose
copies everything. Know which question you are answering.
"""

write_module(
    M,
    "2D Array Mastery",
    "Row-major orientation, column scans with per-column aggregation, neighbor guards, and position-finding with double early exits.",
    "Làm chủ mảng 2 chiều",
    "Định hướng hàng-chính, quét cột với tổng hợp theo cột, lớp chặn hàng xóm, và tìm vị trí với thoát-sớm kép.",
    lessons=["cx-m8-orientation", "cx-m8-neighbors", "cx-m8-columns", "cx-cp-m8"],
    practices=["cx-p8-2d"],
)

write_lesson(
    M, "cx-m8-orientation", "Orientation: rows first",
    "g[r][c], length vs g[0].length, row-major vs column traversal.",
    12, L1,
    "Định hướng: hàng trước",
    "g[r][c], length với g[0].length, duyệt hàng-chính với duyệt theo cột.",
    r"""
Mảng 2 chiều là mảng của các hàng. `int[][] g = new int[3][4]` là 3 hàng,
mỗi hàng 4 cột; `g.length` là 3 (số hàng), `g[0].length` là 4 (số cột).
Sựfact đáng tin nhất của đề thi: **`g[r][c]` — hàng trước, luôn luôn.**

**Duyệt hàng-chính** (thứ tự tự nhiên):
```java
for (int r = 0; r < g.length; r++) {
    for (int c = 0; c < g[r].length; c++) {
        // g[r][c]
    }
}
```
Biên trong `g[r].length` (không phải `g[0].length`) là dạng an toàn đề
thi — hoạt động kể cả khi các hàng dài khác nhau.

**Duyệt theo cột** — vòng ngoài qua các cột, vòng trong qua các hàng:
```java
for (int c = 0; c < g[0].length; c++) {
    for (int r = 0; r < g.length; r++) {
        // g[r][c] — đi XUỐNG một cột
    }
}
```

Từ vựng vị trí cho {1,2,3},{4,5,6}: g[0] là hàng ĐẦU (1,2,3);
`g[1][0]` là hàng chỉ số 1, cột chỉ số 0 → giá trị 4. Hãy vẽ lưới kèm
chỉ số trước khi trả lời bất cứ điều gì. Mọi câu MCQ "phần tử nào" sai
đều đến từ việc tráo hàng/cột.
""",
)

write_lesson(
    M, "cx-m8-neighbors", "Positions and neighbors",
    "Double early exit vs break, and orthogonal neighbor guards.",
    12, L2,
    "Vị trí và hàng xóm",
    "Thoát-sớm kép với break, và lớp chặn hàng xóm trực giao.",
    r"""
Hai hình quét vượt lên ngoài cơ bản:

**Tìm một vị trí, trả về tọa độ.** Khi đáp án là một địa điểm, trả về
hàng (hoặc cặp r/c mã hóa) — và quyết định chuyện gì xảy ra khi vắng mặt
(−1 là quy ước):

```java
public static int findRow(int[][] g, int target) {
    for (int r = 0; r < g.length; r++) {
        for (int c = 0; c < g[r].length; c++) {
            if (g[r][c] == target) {
                return r;
            }
        }
    }
    return -1;
}
```

Chú ý **thoát-sớm kép**: return bên trong rời cả hai vòng lặp cùng lúc.
Một `break` chỉ rời vòng trong — phân biệt MCQ kinh điển.

**Hàng xóm của g[r][c]** — tối đa bốn người bạn trực giao, nhưng mép
lưới có ít hơn. Chặn từng hướng độc lập:

```java
if (r > 0) { ... g[r - 1][c] ... }
if (r < g.length - 1) { ... g[r + 1][c] ... }
if (c > 0) { ... g[r][c - 1] ... }
if (c < g[r].length - 1) { ... g[r][c + 1] ... }
```

Hoặc đếm hàng xóm khớp:

```java
int count = 0;
if (r > 0 && g[r - 1][c] == v) { count++; }
if (r < g.length - 1 && g[r + 1][c] == v) { count++; }
if (c > 0 && g[r][c - 1] == v) { count++; }
if (c < g[r].length - 1 && g[r][c + 1] == v) { count++; }
```

Đừng bao giờ truy cập `g[r-1]` trước khi kiểm tra `r > 0` — chỉ số âm
ném ngoại lệ trước khi giá trị kịp được đọc.
""",
)

write_lesson(
    M, "cx-m8-columns", "Columns, swaps, transposes",
    "Per-column aggregation and the two meanings of 'rearranging a grid'.",
    12, L3,
    "Cột, hoán đổi, chuyển vị",
    "Tổng hợp theo cột và hai nghĩa của 'sắp xếp lại lưới'.",
    r"""
**Tổng hợp theo cột** — nhiệm vụ kinh điển "tính tổng từng cột":

```java
public static int[] colSums(int[][] g) {
    int[] sums = new int[g[0].length];
    for (int c = 0; c < g[0].length; c++) {
        for (int r = 0; r < g.length; r++) {
            sums[c] += g[r][c];
        }
    }
    return sums;
}
```

Mảng đầu ra có kích thước theo CỘT; các vòng lặp đọc theo cột. Hai hướng
trong một phương thức — vẽ ra vòng nào đi hướng nào cho đến khi thành
phản xạ.

**Biến đổi** đọc và ghi cùng một mảng thì cần cẩn trọng: hoán đổi hàng
dùng một mảng tạm một-hàng:

```java
int[] tmp = g[a];
g[a] = g[b];
g[b] = tmp;
```

Đó là O(1) — các tham chiếu hàng hoán đổi cho nhau, không sao chép phần
tử. So với chuyển vị (hàng thành cột), cần sao chép từng phần tử vào
mảng MỚI với kích thước hoán đổi:

```java
int[][] t = new int[g[0].length][g.length];
for (int r = 0; r < g.length; r++) {
    for (int c = 0; c < g[r].length; c++) {
        t[c][r] = g[r][c];
    }
}
```

Cả hai hướng đều xuất hiện trong đề thi; hoán đổi không sao chép gì,
chuyển vị sao chép tất cả. Hãy biết mình đang trả lời câu nào.
""",
)

GRID2x3 = r"""int[][] g = { {1, 2, 3}, {4, 5, 6} };"""

BOILER_RAVG = r"""public class Solution {
    // CONTRACT: average of ONE row as a double. Precondition:
    // grid.length >= 1 and 0 <= row < grid.length.
    public static double rowAverage(int[][] grid, int row) {
        return 0; // replace
    }
}
"""

BOILER_COUNTVAL = r"""public class Solution {
    // CONTRACT: how many cells of grid equal value.
    public static int countValue(int[][] grid, int value) {
        return 0; // replace
    }
}
"""

BOILER_MAXCOL = r"""public class Solution {
    // CONTRACT: index of the column with the LARGEST sum; ties -> the
    // EARLIEST such column. Precondition: grid.length >= 1 and
    // grid[0].length >= 1 (rectangular).
    public static int maxColumn(int[][] grid) {
        return 0; // replace
    }
}
"""

BOILER_NEIGHBORS = r"""public class Solution {
    // CONTRACT: count orthogonal neighbors of (row, col) that equal
    // value. Edges and corners legitimately have fewer neighbors.
    public static int countNeighbors(int[][] grid, int row, int col, int value) {
        return 0; // replace
    }
}
"""

BOILER_ROWSWAPBAD = r"""public class Solution {
    // CONTRACT: swap rows a and b of grid, in place.
    // Precondition: 0 <= a, b < grid.length.
    public static void swapRows(int[][] grid, int a, int b) {
        for (int c = 0; c < grid[0].length; c++) {
            grid[a][c] = grid[b][c];
        }
    }
}
"""

BOILER_CP_2D = r"""public class Solution {
    // CONTRACT: a path walk: starting at (row, col), repeatedly move to
    // the position recorded in the current cell. Cells hold 2-digit
    // codes: 10*row + col. Return the code of the FIRST cell visited
    // TWICE (including the start), or -1 if the walk leaves the grid.
    // Step limit: grid cells count * 2 steps.
    public static int firstRepeat(int[][] grid, int row, int col) {
        return -1; // replace
    }
}
"""

P_RAVG = challenge(
    "cx-m8-row-average",
    "Row average",
    "Implement `double rowAverage(int[][] grid, int row)`: the average of one row. One pass over `grid[row]`, divide by its length as a double.",
    BOILER_RAVG,
    [(
        "row average",
        r"""
int[][] g = { {1, 2, 3}, {4, 5, 6}, {1, 2} };
CjTestBase.checkNear(Solution.rowAverage(g, 0), 2.0, 1e-9, "first row");
CjTestBase.checkNear(Solution.rowAverage(g, 1), 5.0, 1e-9, "second row");
CjTestBase.checkNear(Solution.rowAverage(g, 2), 1.5, 1e-9, "non-integer average");
CjTestBase.checkNear(Solution.rowAverage(new int[][]{{7}}, 0), 7.0, 1e-9, "single cell");
""",
        "Sum grid[row], divide by grid[row].length (as a double).",
    )],
    level="imitation",
)

P_COUNTVAL = challenge(
    "cx-m8-count-value",
    "Count cells",
    "Implement `int countValue(int[][] grid, int value)`: how many cells equal value. Row-major double loop; the for-each form over rows also works.",
    BOILER_COUNTVAL,
    [(
        "cells counted",
        r"""
int[][] g = { {1, 2}, {2, 2} };
CjTestBase.checkEq(Solution.countValue(g, 2), 3, "three 2s");
CjTestBase.checkEq(Solution.countValue(new int[][]{}, 1), 0, "no rows");
CjTestBase.checkEq(Solution.countValue(g, 9), 0, "absent value");
""",
        "Row-major scan, one counter.",
    )],
    level="guided",
)

P_MAXCOL = challenge(
    "cx-m8-max-column",
    "Column with the largest sum",
    "Implement `int maxColumn(int[][] grid)`: the index of the column with the largest sum (ties → earliest). Combine column-major aggregation with the seeded max-index machine from Module 6.",
    BOILER_MAXCOL,
    [(
        "winning column",
        r"""
int[][] g = { {1, 6, 2}, {0, 1, 9} };
CjTestBase.checkEq(Solution.maxColumn(g), 2, "col sums 1, 7, 11");
CjTestBase.checkEq(Solution.maxColumn(new int[][]{{5}}), 0, "single cell");
int[][] t = { {2, 2}, {2, 2} };
CjTestBase.checkEq(Solution.maxColumn(t), 0, "tie keeps earliest");
""",
        "Track bestSum and bestCol seeded from column 0; strict > keeps the earliest tie.",
    )],
    level="combination",
)

P_NEIGHBORS = challenge(
    "cx-m8-count-neighbors",
    "Neighbor counting",
    "Implement `int countNeighbors(int[][] grid, int row, int col, int value)`: how many orthogonal neighbors (up/down/left/right) equal value. Guard each direction independently — corners have 2, edges 3, interior 4.",
    BOILER_NEIGHBORS,
    [(
        "neighbors counted",
        r"""
int[][] g = { {7, 1, 7}, {1, 7, 1}, {7, 1, 7} };
CjTestBase.checkEq(Solution.countNeighbors(g, 1, 1, 7), 0, "checkerboard interior: neighbors are all 1s");
CjTestBase.checkEq(Solution.countNeighbors(g, 0, 0, 7), 0, "corner, neighbors are 1s");
CjTestBase.checkEq(Solution.countNeighbors(g, 0, 0, 1), 2, "corner has two neighbors");
CjTestBase.checkEq(Solution.countNeighbors(g, 0, 1, 7), 3, "edge has three neighbors, all 7s");
""",
        "Four independent if-guards: up, down, left, right.",
    )],
    level="combination",
)

P_SWAPBAD = challenge(
    "cx-m8-fix-row-swap",
    "Fix the row swap",
    "`swapRows` overwrites row a with row b and leaves row b untouched — the original row a is destroyed. Trace {1,2},{3,4} with a=0, b=1, then repair using the one-row temporary from the lesson.",
    BOILER_ROWSWAPBAD,
    [(
        "rows exchanged",
        r"""
int[][] g = { {1, 2}, {3, 4} };
Solution.swapRows(g, 0, 1);
CjTestBase.checkEq(g[0], new int[]{3, 4}, "row 0 now holds old row 1");
CjTestBase.checkEq(g[1], new int[]{1, 2}, "row 1 now holds old row 0");
""",
        "Save grid[a] in a temp reference BEFORE overwriting; swap references.",
    )],
    level="debugging",
)

CP8 = challenge(
    "cx-cp-m8-path",
    "Checkpoint: follow the path",
    "Implement `int firstRepeat(int[][] grid, int row, int col)`: each cell holds `10*row + col`. Starting at (row, col), jump to the cell it names; return the code of the first cell visited twice, or -1 if a jump leaves the grid. Cap steps at 2 × cell count. This is a traced walk: maintain the visited knowledge, one jump per iteration.",
    BOILER_CP_2D,
    [(
        "first repeated cell",
        r"""
int[][] g = { {0, 11}, {10, 3} };
CjTestBase.checkEq(Solution.firstRepeat(g, 0, 0), 0, "0 -> (0,0): immediate self-repeat");
CjTestBase.checkEq(Solution.firstRepeat(g, 0, 1), -1, "11 -> (1,1) holds 3 -> leaves grid");
int[][] h = { {0, 0}, {10, 0} };
CjTestBase.checkEq(Solution.firstRepeat(h, 1, 0), 10, "(1,0) points at itself: repeat code 10");
""",
        "Track a visited boolean grid; jump repeatedly; first revisit wins; out-of-bounds -> -1.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p8-2d", "2D array lab",
    "Row averages, cell counts, column winners, neighbors, and a swap repair.",
    "Phòng mảng 2 chiều",
    "Trung bình hàng, đếm ô, cột vô địch, hàng xóm, và sửa phép hoán đổi hàng.",
    after_lesson="cx-m8-columns", minutes=60, difficulty="advanced",
    challenges=[P_RAVG, P_COUNTVAL, P_MAXCOL, P_NEIGHBORS, P_SWAPBAD],
    vi_challenges={
        "cx-m8-row-average": vi_challenge("Trung bình hàng",
            "Hiện thực `double rowAverage(int[][] grid, int row)`: trung bình của một hàng. Một lượt qua `grid[row]`, chia cho độ dài của nó theo kiểu double.",
            [("row average", "Cộng grid[row], chia cho grid[row].length (theo double).")]),
        "cx-m8-count-value": vi_challenge("Đếm ô",
            "Hiện thực `int countValue(int[][] grid, int value)`: bao nhiêu ô bằng giá trị. Vòng kép hàng-chính; dạng for-each qua các hàng cũng được.",
            [("cells counted", "Quét hàng-chính, một bộ đếm.")]),
        "cx-m8-max-column": vi_challenge("Cột có tổng lớn nhất",
            "Hiện thực `int maxColumn(int[][] grid)`: chỉ số cột có tổng lớn nhất (đồng giá → cột sớm nhất). Kết hợp tổng hợp theo cột với cỗ máy max-theo-chỉ- số có seed từ Module 6.",
            [("winning column", "Theo dõi bestSum và bestCol seed từ cột 0; dấu > nghiêm ngặt giữ đồng giá sớm nhất.")]),
        "cx-m8-count-neighbors": vi_challenge("Đếm hàng xóm",
            "Hiện thực `int countNeighbors(int[][] grid, int row, int col, int value)`: bao nhiêu hàng xóm trực giao (lên/xuống/trái/phải) bằng giá trị. Chặn từng hướng độc lập — góc có 2, mép có 3, giữa có 4.",
            [("neighbors counted", "Bốn if-chặn độc lập: lên, xuống, trái, phải.")]),
        "cx-m8-fix-row-swap": vi_challenge("Sửa phép hoán đổi hàng",
            "`swapRows` ghi đè hàng a bằng hàng b và bỏ nguyên hàng b — hàng a gốc bị phá hủy. Truy vết {1,2},{3,4} với a=0, b=1, rồi sửa bằng mảng tạm một-hàng từ bài học.",
            [("rows exchanged", "Lưu grid[a] vào tham chiếu tạm TRƯỚC khi ghi đè; hoán đổi tham chiếu.")]),
    },
    solutions=[
        ("cx-m8-row-average", BOILER_RAVG.replace("return 0; // replace",
            "int sum = 0;\n        for (int c = 0; c < grid[row].length; c++) {\n            sum += grid[row][c];\n        }\n        return (double) sum / grid[row].length;"),
         BOILER_RAVG.replace("return 0; // replace",
            "int sum = 0;\n        for (int c = 0; c < grid[row].length; c++) {\n            sum += grid[row][c];\n        }\n        return sum / grid[row].length;")),
        ("cx-m8-count-value", BOILER_COUNTVAL.replace("return 0; // replace",
            "int count = 0;\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                if (grid[r][c] == value) {\n                    count++;\n                }\n            }\n        }\n        return count;"),
         BOILER_COUNTVAL.replace("return 0; // replace",
            "int count = 0;\n        for (int c = 0; c < grid[0].length; c++) {\n            for (int r = 0; r < grid.length; r++) {\n                if (grid[r][c] == value) {\n                    count++;\n                }\n            }\n        }\n        return count;")),
        ("cx-m8-max-column", BOILER_MAXCOL.replace("return 0; // replace",
            "int bestCol = 0;\n        int bestSum = Integer.MIN_VALUE;\n        for (int c = 0; c < grid[0].length; c++) {\n            int sum = 0;\n            for (int r = 0; r < grid.length; r++) {\n                sum += grid[r][c];\n            }\n            if (sum > bestSum) {\n                bestSum = sum;\n                bestCol = c;\n            }\n        }\n        return bestCol;"),
         BOILER_MAXCOL.replace("return 0; // replace",
            "int bestCol = 0;\n        int bestSum = Integer.MIN_VALUE;\n        for (int c = 0; c < grid[0].length; c++) {\n            int sum = 0;\n            for (int r = 0; r < grid.length; r++) {\n                sum += grid[r][c];\n            }\n            if (sum >= bestSum) {\n                bestSum = sum;\n                bestCol = c;\n            }\n        }\n        return bestCol;")),
        ("cx-m8-count-neighbors", BOILER_NEIGHBORS.replace("return 0; // replace",
            "int count = 0;\n        if (row > 0 && grid[row - 1][col] == value) { count++; }\n        if (row < grid.length - 1 && grid[row + 1][col] == value) { count++; }\n        if (col > 0 && grid[row][col - 1] == value) { count++; }\n        if (col < grid[row].length - 1 && grid[row][col + 1] == value) { count++; }\n        return count;"),
         BOILER_NEIGHBORS.replace("return 0; // replace",
            "int count = 0;\n        if (row >= 0 && grid[row - 1][col] == value) { count++; }\n        if (row < grid.length - 1 && grid[row + 1][col] == value) { count++; }\n        if (col > 0 && grid[row][col - 1] == value) { count++; }\n        if (col < grid[row].length - 1 && grid[row][col + 1] == value) { count++; }\n        return count;")),
        ("cx-m8-fix-row-swap",
         r"""public class Solution {
    public static void swapRows(int[][] grid, int a, int b) {
        int[] tmp = grid[a];
        grid[a] = grid[b];
        grid[b] = tmp;
    }
}
""",
         r"""public class Solution {
    public static void swapRows(int[][] grid, int a, int b) {
        int[] tmp = new int[grid[a].length];
        for (int c = 0; c < grid[a].length; c++) {
            tmp[c] = grid[a][c];
        }
        for (int c = 0; c < grid[a].length; c++) {
            grid[a][c] = grid[b][c];
        }
        for (int c = 0; c < grid[a].length; c++) {
            grid[b][c] = grid[a][c];
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "cx-cp-m8", "Checkpoint: follow the path",
    "A coded-cell walk with visited tracking — orientation, guards, and a loop cap.",
    30,
    r"""
The path walk fuses everything this module owns: decoding 10*row+col,
bounds guards on every jump, visited tracking, and a step cap as the
sentinel against cycles that never repeat but also never end. If your
first trace disagreed with the code, check whether you decoded the code
as column*10+row — the classic transposition.
""",
    "Điểm kiểm tra: đi theo đường dẫn",
    "Đi bộ theo mã ô với theo dõi đã-thăm — định hướng, lớp chặn, và trần vòng lặp.",
    r"""
Bài đi đường dẫn hợp nhất mọi thứ module này sở hữu: giải mã 10*row+col,
lớp chặn biên cho mỗi bước nhảy, theo dõi đã-thăm, và trần bước làm
lính canh chống các chu kỳ không lặp nhưng cũng không dứt. Nếu lần truy
vết đầu của bạn lệch với mã, hãy kiểm tra xem bạn có giải mã thành
column*10+row không — lỗi tráo vị trí kinh điển.
""",
    CP8,
    vi_challenge("Điểm kiểm tra: đi theo đường dẫn",
        "Hiện thực `int firstRepeat(int[][] grid, int row, int col)`: mỗi ô chứa mã `10*row + col`. Xuất phát từ (row, col), nhảy đến ô mà nó gọi tên; trả về mã của ô đầu tiên được thăm HAI LẦN, hoặc -1 nếu bước nhảy rời lưới. Trần: 2 × số ô.",
        [("first repeated cell", "Theo dõi một lưới boolean đã-thăm; nhảy lặp lại; lần ghé lại đầu tiên thắng; ra ngoài biên → -1.")]),
    solution=r"""public class Solution {
    public static int firstRepeat(int[][] grid, int row, int col) {
        int rows = grid.length;
        int cols = grid[0].length;
        boolean[][] seen = new boolean[rows][cols];
        int steps = 0;
        int cap = rows * cols * 2;
        while (steps <= cap) {
            if (row < 0 || row >= rows || col < 0 || col >= cols) {
                return -1;
            }
            if (seen[row][col]) {
                return 10 * row + col;
            }
            seen[row][col] = true;
            int code = grid[row][col];
            row = code / 10;
            col = code % 10;
            steps++;
        }
        return -1;
    }
}
""",
    wrong=r"""public class Solution {
    public static int firstRepeat(int[][] grid, int row, int col) {
        int rows = grid.length;
        int cols = grid[0].length;
        boolean[][] seen = new boolean[rows][cols];
        int steps = 0;
        int cap = rows * cols * 2;
        while (steps <= cap) {
            if (row < 0 || row >= rows || col < 0 || col >= cols) {
                return -1;
            }
            if (seen[row][col]) {
                return 10 * col + row;
            }
            seen[row][col] = true;
            int code = grid[row][col];
            row = code % 10;
            col = code / 10;
            steps++;
        }
        return -1;
    }
}
""",
)
