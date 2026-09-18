#!/usr/bin/env python3
"""C Beginner — batch 5: modules 9 (arrays) and 10 (strings)."""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ============================ MODULE 9: arrays ============================
M9 = "arrays"

L9A = "array-basics"
L9B = "arrays-loops"
L9C = "2d-arrays"
L9D = "cb-checkpoint-m9"

write_module(
    M9,
    "Arrays",
    "Fixed-size collections: declaration, indexing, iteration, and the out-of-bounds trap.",
    "Mảng",
    "Bộ sưu tập kích thước cố định: khai báo, đánh chỉ số, duyệt và cái bẫy vượt biên.",
    [L9A, L9B, L9C, L9D],
    ["cb-p9-arrays", "cb-p9-grid"],
)

write_lesson(
    M9,
    L9A,
    "Array Basics",
    "A contiguous block of same-typed elements, indexed from 0.",
    12,
    r"""
## Declaration and indexing

```c
int scores[5];              // 5 ints, UNINITIALIZED (indeterminate values)
int primes[4] = {2, 3, 5, 7};
int first = primes[0];      // 2 — indexing starts at 0
int last  = primes[3];      // 7 — index size-1
```

- Elements live **contiguously** in memory: `primes[i]` sits at
  "start + i * sizeof(int)".
- The size is part of the type — fixed at compile time (dynamic sizing is
  module 13).
- The compiler will not stop you from reading `primes[9]` — that is
  **undefined behavior**. Out-of-bounds access is THE classic C bug.

## Initialization rules

```c
int a[4] = {1, 2};          // {1, 2, 0, 0} — rest zero-filled
int b[]  = {1, 2, 3};       // size deduced: 3
int c[4] = {0};             // all zeros
```

Any initializer list (even `{0}`) gives defined values; no list at all leaves
the contents indeterminate — reading them is a bug.

## No length operator

C arrays do not know their own length. Passing them to functions loses the
size — you pass it separately (module 12). For now: keep a constant.

```c
#define N 5
int a[N];
for (int i = 0; i < N; i++) { /* ... */ }
```
""",
    "Cơ bản về mảng",
    "Một khối liền kề các phần tử cùng kiểu, đánh chỉ số từ 0.",

    r"""
## Khai báo và đánh chỉ số

```c
int scores[5];              // 5 int, CHƯA KHỞI TẠO (giá trị không xác định)
int primes[4] = {2, 3, 5, 7};
int first = primes[0];      // 2 — chỉ số bắt đầu từ 0
int last  = primes[3];      // 7 — chỉ số size-1
```

- Các phần tử nằm **liên tiếp** trong bộ nhớ: `primes[i]` ở vị trí
  "đầu + i * sizeof(int)".
- Kích thước là một phần của kiểu — cố định khi biên dịch (kích thước động ở
  module 13).
- Trình biên dịch sẽ không chặn bạn đọc `primes[9]` — đó là **hành vi không
  xác định**. Truy cập vượt biên là cái bẫy kinh điển của C.

## Quy tắc khởi tạo

```c
int a[4] = {1, 2};          // {1, 2, 0, 0} — phần còn lại bù 0
int b[]  = {1, 2, 3};       // suy ra kích thước: 3
int c[4] = {0};             // toàn 0
```

Có danh sách khởi tạo (kể cả `{0}`) thì giá trị xác định; không có danh sách
thì nội dung không xác định — đọc chúng là lỗi.

## Không có toán tử độ dài

Mảng C không tự biết độ dài. Truyền cho hàm sẽ mất kích thước — phải truyền
riêng (module 12). Tạm thời: giữ một hằng số.

```c
#define N 5
int a[N];
for (int i = 0; i < N; i++) { /* ... */ }
```
""",
)

write_lesson(
    M9,
    L9B,
    "Arrays and Loops",
    "The for-loop is the array's natural partner: visit every index, in order.",
    11,
    r"""
## The visit pattern

```c
int a[5] = {4, 8, 15, 16, 23};
int sum = 0;
for (int i = 0; i < 5; i++) {
    sum += a[i];
}
```

Three canonical walks: compute a value from all elements (sum/max), transform
in place (`a[i] = a[i] * 2`), and build a new array from an old one.

## The identity: last index is size-1

```c
int a[5];
for (int i = 0; i <= 5; i++) {   // BUG: i == 5 is out of bounds
    a[i] = i;
}
```

`i < size` is the loop condition for arrays. `i <= size` writes one element
past the end — sometimes it "works", sometimes it corrupts a neighbor,
always it is undefined behavior.

## Counting and finding

```c
int count = 0, found = -1;
for (int i = 0; i < 5; i++) {
    if (a[i] > 10) count++;          // count matches
    if (a[i] == 15) found = i;       // remember the index
}
```

`found = -1` as "not present" is a C idiom you will use everywhere.
""",
    "Mảng và vòng lặp",
    "Vòng for là cặp đôi tự nhiên của mảng: ghé thăm từng chỉ số, đúng thứ tự.",

    r"""
## Mẫu duyệt

```c
int a[5] = {4, 8, 15, 16, 23};
int sum = 0;
for (int i = 0; i < 5; i++) {
    sum += a[i];
}
```

Ba lượt đi kinh điển: tính một giá trị từ mọi phần tử (tổng/max), biến đổi
tại chỗ (`a[i] = a[i] * 2`), và dựng mảng mới từ mảng cũ.

## Đẳng thức: chỉ số cuối là size-1

```c
int a[5];
for (int i = 0; i <= 5; i++) {   // LỖI: i == 5 vượt biên
    a[i] = i;
}
```

`i < size` là điều kiện vòng lặp cho mảng. `i <= size` ghi một phần tử sau
cuối — đôi khi "chạy được", đôi khi hỏng biến bên cạnh, và luôn luôn là hành
vi không xác định.

## Đếm và tìm

```c
int count = 0, found = -1;
for (int i = 0; i < 5; i++) {
    if (a[i] > 10) count++;          // đếm phần tử khớp
    if (a[i] == 15) found = i;       // nhớ lại chỉ số
}
```

`found = -1` nghĩa là "không có" — một thành ngữ C bạn sẽ dùng khắp nơi.
""",
)

write_lesson(
    M9,
    L9C,
    "2D Arrays",
    "Rows and columns: an array of arrays, stored row by row.",
    11,
    r"""
## Declaration and indexing

```c
int grid[3][4];                    // 3 rows, 4 columns
grid[1][2] = 7;                    // row 1, column 2
int diag[2][2] = {{1, 0}, {0, 1}};
```

A 2D array is one contiguous block, stored **row-major**: row 0's four ints,
then row 1's, then row 2's. `[r][c]` is the element at row r, column c.

## The nested-loop walk

```c
int grid[3][4] = {0};
for (int r = 0; r < 3; r++) {
    for (int c = 0; c < 4; c++) {
        grid[r][c] = r * 10 + c;
    }
}
```

Outer loop = rows, inner loop = columns. Total elements = 3 × 4 = 12.

## Row totals

```c
int row_sum(const int g[][4], int rows) {   // column count is part of the type
    int total = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < 4; c++)
            total += g[r][c];
    return total;
}
```

Note the parameter shape: the first bracket may be empty, the second may not.
""",
    "Mảng 2 chiều",
    "Hàng và cột: mảng của mảng, lưu theo hàng.",

    r"""
## Khai báo và đánh chỉ số

```c
int grid[3][4];                    // 3 hàng, 4 cột
grid[1][2] = 7;                    // hàng 1, cột 2
int diag[2][2] = {{1, 0}, {0, 1}};
```

Mảng 2 chiều là một khối liền, lưu theo **hàng-trước**: bốn int của hàng 0,
rồi hàng 1, rồi hàng 2. `[r][c]` là phần tử ở hàng r, cột c.

## Lượt đi bằng vòng lặp lồng

```c
int grid[3][4] = {0};
for (int r = 0; r < 3; r++) {
    for (int c = 0; c < 4; c++) {
        grid[r][c] = r * 10 + c;
    }
}
```

Vòng ngoài = hàng, vòng trong = cột. Tổng phần tử = 3 × 4 = 12.

## Tổng theo hàng

```c
int row_sum(const int g[][4], int rows) {   // số cột là một phần của kiểu
    int total = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < 4; c++)
            total += g[r][c];
    return total;
}
```

Chú ý dạng tham số: ngoặc đầu có thể trống, ngoặc thứ hai thì không.
""",
)

write_practice(
    M9,
    "cb-p9-arrays",
    "Array Workbench",
    "Sum, max, search, and reverse over fixed arrays.",
    "Bàn làm việc với mảng",
    "Tổng, max, tìm kiếm và đảo ngược trên mảng cố định.",
    L9B,
    15,
    "beginner",
    [
        challenge(
            "cb9-array-sum",
            "Array Sum",
            "Implement `int array_sum(const int* a, int n)` returning the sum of the first n elements.",
            C_PRELUDE,
            [
                ("basics", "int a[] = {1, 2, 3, 4};\nCHECK_EQ(array_sum(a, 4), 10);", "Accumulate in a loop."),
                ("empty", "int a[] = {5};\nCHECK_EQ(array_sum(a, 0), 0);", "n=0: no elements to add."),
                ("negatives", "int a[] = {-5, 5, -5};\nCHECK_EQ(array_sum(a, 3), -5);", "Signs combine."),
            ],
            level="imitation",
        ),
        challenge(
            "cb9-array-max",
            "Array Max",
            "Implement `int array_max(const int* a, int n)` returning the largest element (n >= 1 guaranteed).",
            C_PRELUDE,
            [
                ("basics", "int a[] = {3, 9, 4};\nCHECK_EQ(array_max(a, 3), 9);", "Start from a[0]."),
                ("first is max", "int a[] = {7, 2, 1};\nCHECK_EQ(array_max(a, 3), 7);", "Compare every element."),
                ("all equal", "int a[] = {4, 4, 4};\nCHECK_EQ(array_max(a, 3), 4);", "Max of equals is that value."),
                ("negatives", "int a[] = {-9, -2, -5};\nCHECK_EQ(array_max(a, 3), -2);", "Works below zero."),
                ("max after dip", "int a[] = {5, 3, 9};\nCHECK_EQ(array_max(a, 3), 9);", "Scan EVERY element — the max can come last."),
            ],
            level="guided",
        ),
        challenge(
            "cb9-linear-search",
            "Linear Search",
            "Implement `int find(const int* a, int n, int target)` returning the FIRST index holding target, or -1 if absent.",
            C_PRELUDE,
            [
                ("present", "int a[] = {4, 8, 15};\nCHECK_EQ(find(a, 3, 15), 2);", "Return the index."),
                ("first match wins", "int a[] = {5, 5, 5};\nCHECK_EQ(find(a, 3, 5), 0);", "Stop at the first hit."),
                ("absent", "int a[] = {1, 2};\nCHECK_EQ(find(a, 2, 9), -1);", "-1 means not found."),
            ],
            level="guided",
        ),
        challenge(
            "cb9-array-reverse",
            "In-Place Reverse",
            "Implement `void reverse(int* a, int n)` reversing the first n elements IN PLACE (no second array).",
            C_PRELUDE,
            [
                ("even length", "int a[] = {1, 2, 3, 4};\nreverse(a, 4);\nCHECK_EQ(a[0], 4);\nCHECK_EQ(a[3], 1);", "Swap ends, move inward."),
                ("odd length", "int a[] = {1, 2, 3};\nreverse(a, 3);\nCHECK_EQ(a[1], 2);", "The middle stays."),
                ("single", "int a[] = {9};\nreverse(a, 1);\nCHECK_EQ(a[0], 9);", "One element: nothing to do."),
            ],
            level="independent",
        ),
    ],
    {
        "cb9-array-sum": vi_challenge(
            "Tổng mảng",
            "Cài `int array_sum(const int* a, int n)` trả về tổng của n phần tử đầu.",
            [("cơ bản", "Cộng dồn trong vòng lặp."), ("rỗng", "n=0: không phần tử để cộng."), ("số âm", "Dấu kết hợp với nhau.")],
        ),
        "cb9-array-max": vi_challenge(
            "Max mảng",
            "Cài `int array_max(const int* a, int n)` trả về phần tử lớn nhất (n >= 1 được đảm bảo).",
            [("cơ bản", "Bắt đầu từ a[0]."), ("đầu là max", "So sánh mọi phần tử."), ("bằng nhau", "Max của các số bằng nhau là chính nó."), ("số âm", "Hoạt động dưới 0.")],
        ),
        "cb9-linear-search": vi_challenge(
            "Tìm kiếm tuyến tính",
            "Cài `int find(const int* a, int n, int target)` trả về chỉ số ĐẦU TIÊN chứa target, hoặc -1 nếu không có.",
            [("có", "Trả về chỉ số."), ("khớp đầu tiên", "Dừng tại lần trúng đầu tiên."), ("không có", "-1 nghĩa là không tìm thấy.")],
        ),
        "cb9-array-reverse": vi_challenge(
            "Đảo ngược tại chỗ",
            "Cài `void reverse(int* a, int n)` đảo ngược n phần tử đầu TẠI CHỖ (không dùng mảng thứ hai).",
            [("độ dài chẵn", "Hoán đổi hai đầu, tiến vào trong."), ("độ dài lẻ", "Phần giữa giữ nguyên."), ("một phần tử", "Không cần làm gì.")],
        ),
    },
    solutions=[
        (
            "cb9-array-sum",
            '#include <stdio.h>\nint array_sum(const int* a, int n) {\n    int s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint array_sum(const int* a, int n) {\n    int s = 0;\n    for (int i = 1; i < n; i++) s += a[i];\n    return s;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb9-array-max",
            '#include <stdio.h>\nint array_max(const int* a, int n) {\n    int m = a[0];\n    for (int i = 1; i < n; i++)\n        if (a[i] > m) m = a[i];\n    return m;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint array_max(const int* a, int n) {\n    int m = a[0];\n    for (int i = 1; i < n; i++)\n        if (a[i] > m) m = a[i];\n        else return m;\n    return m;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb9-linear-search",
            '#include <stdio.h>\nint find(const int* a, int n, int target) {\n    for (int i = 0; i < n; i++)\n        if (a[i] == target) return i;\n    return -1;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint find(const int* a, int n, int target) {\n    for (int i = 0; i < n; i++)\n        if (a[i] == target) return i;\n    return 0;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb9-array-reverse",
            '#include <stdio.h>\nvoid reverse(int* a, int n) {\n    for (int i = 0, j = n - 1; i < j; i++, j--) {\n        int t = a[i];\n        a[i] = a[j];\n        a[j] = t;\n    }\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid reverse(int* a, int n) {\n    for (int i = 0, j = n - 1; i < j; i++, j--) {\n        a[i] = a[j];\n        a[j] = a[i];\n    }\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M9,
    "cb-p9-grid",
    "Grid Exercises",
    "Two-dimensional data: fills, sums, and a diagonal.",
    "Bài tập lưới",
    "Dữ liệu hai chiều: điền, cộng và đường chéo.",
    L9C,
    14,
    "beginner",
    [
        challenge(
            "cb9-grid-fill",
            "Grid Fill",
            "Implement `void grid_fill(int g[][3], int rows)` setting g[r][c] = r * 3 + c (row-major counter).",
            C_PRELUDE,
            [
                ("row 0", "int g[2][3];\ngrid_fill(g, 2);\nCHECK_EQ(g[0][0], 0);\nCHECK_EQ(g[0][2], 2);", "First row counts 0,1,2."),
                ("row 1", "int g[2][3];\ngrid_fill(g, 2);\nCHECK_EQ(g[1][0], 3);\nCHECK_EQ(g[1][2], 5);", "Second row counts 3,4,5."),
            ],
            level="imitation",
        ),
        challenge(
            "cb9-grid-sum",
            "Grid Total",
            "Implement `int grid_sum(const int g[][3], int rows)` returning the sum of all elements.",
            C_PRELUDE,
            [
                ("basics", "int g[2][3] = {{1,2,3},{4,5,6}};\nCHECK_EQ(grid_sum(g, 2), 21);", "Nested loops over rows then columns."),
                ("with zeros", "int g[2][3] = {{0}};\ng[0][1] = 9;\nCHECK_EQ(grid_sum(g, 2), 9);", "Zeros contribute nothing."),
            ],
            level="guided",
        ),
        challenge(
            "cb9-diagonal",
            "Diagonal Sum",
            "Implement `int diag_sum(const int g[][3])` returning g[0][0] + g[1][1] + g[2][2].",
            C_PRELUDE,
            [
                ("identity", "int g[3][3] = {{1,0,0},{0,1,0},{0,0,1}};\nCHECK_EQ(diag_sum(g), 3);", "The diagonal cells only."),
                ("mixed", "int g[3][3] = {{5,9,9},{9,6,9},{9,9,7}};\nCHECK_EQ(diag_sum(g), 18);", "Skip everything off the diagonal."),
            ],
            level="guided",
        ),
    ],
    {
        "cb9-grid-fill": vi_challenge(
            "Điền lưới",
            "Cài `void grid_fill(int g[][3], int rows)` đặt g[r][c] = r * 3 + c (bộ đếm theo hàng).",
            [("hàng 0", "Hàng đầu đếm 0,1,2."), ("hàng 1", "Hàng hai đếm 3,4,5.")],
        ),
        "cb9-grid-sum": vi_challenge(
            "Tổng lưới",
            "Cài `int grid_sum(const int g[][3], int rows)` trả về tổng mọi phần tử.",
            [("cơ bản", "Vòng lặp lồng: hàng rồi cột."), ("có số 0", "Số 0 không góp gì.")],
        ),
        "cb9-diagonal": vi_challenge(
            "Tổng đường chéo",
            "Cài `int diag_sum(const int g[][3])` trả về g[0][0] + g[1][1] + g[2][2].",
            [("đơn vị", "Chỉ các ô đường chéo."), ("hỗn hợp", "Bỏ qua mọi ô ngoài đường chéo.")],
        ),
    },
    solutions=[
        (
            "cb9-grid-fill",
            '#include <stdio.h>\nvoid grid_fill(int g[][3], int rows) {\n    for (int r = 0; r < rows; r++)\n        for (int c = 0; c < 3; c++)\n            g[r][c] = r * 3 + c;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid grid_fill(int g[][3], int rows) {\n    for (int r = 0; r < rows; r++)\n        for (int c = 0; c < 3; c++)\n            g[r][c] = r + c;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb9-grid-sum",
            '#include <stdio.h>\nint grid_sum(const int g[][3], int rows) {\n    int s = 0;\n    for (int r = 0; r < rows; r++)\n        for (int c = 0; c < 3; c++)\n            s += g[r][c];\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint grid_sum(const int g[][3], int rows) {\n    int s = 0;\n    for (int r = 0; r < rows; r++)\n        s += g[r][0];\n    return s;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb9-diagonal",
            '#include <stdio.h>\nint diag_sum(const int g[][3]) {\n    int s = 0;\n    for (int i = 0; i < 3; i++) s += g[i][i];\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint diag_sum(const int g[][3]) {\n    int s = 0;\n    for (int i = 0; i < 3; i++) s += g[i][2 - i];\n    return s;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M9,
    L9D,
    "Checkpoint: Arrays",
    "A statistics toolkit: mean, variance count, and a mode scan.",
    16,
    r"""
## Checkpoint

Arrays + loops = data analysis. Build the three stat primitives.
""",
    "Điểm kiểm tra: Mảng",
    "Mảng + vòng lặp = phân tích dữ liệu. Dựng ba phép thống kê nền.",

    r"""
## Điểm kiểm tra

Mảng + vòng lặp = phân tích dữ liệu. Dựng ba phép thống kê nền.
""",
    challenge(
        "cb9-checkpoint-stats",
        "Statistics Toolkit",
        "Implement `double mean(const int* a, int n)` (sum divided by n as a double), `int count_above(const int* a, int n, int t)` (elements strictly greater than t), and `int mode(const int* a, int n)` (the value occurring most often; if several tie, return the SMALLEST such value).",
        C_PRELUDE,
        [
            ("mean", "int a[] = {2, 4, 6};\nCHECK_NEAR(mean(a, 3), 4.0, 1e-9);", "Cast inside the division: (double)sum / n."),
            ("count above", "int a[] = {5, 12, 8, 12};\nCHECK_EQ(count_above(a, 4, 7), 3);", "12, 8, 12 are > 7; 5 is not."),
            ("mode clear winner", "int a[] = {3, 1, 3, 3, 2};\nCHECK_EQ(mode(a, 5), 3);", "Count occurrences of each candidate."),
            ("mode tie", "int a[] = {4, 2, 4, 2};\nCHECK_EQ(mode(a, 4), 2);", "Tie between 4 and 2 — return the smaller."),
        ],
    ),
    vi_challenge(
        "Bộ công cụ thống kê",
        "Cài `double mean(const int* a, int n)` (tổng chia n theo kiểu double), `int count_above(const int* a, int n, int t)` (phần tử lớn hơn t NGHIÊM NGỈT), và `int mode(const int* a, int n)` (giá trị xuất hiện nhiều nhất; nếu hòa, trả giá trị NHỎ HƠN).",
        [("mean", "Ép kiểu bên trong phép chia: (double)sum / n."), ("count above", "12, 8, 12 đều > 7; 5 thì không."), ("mode thắng rõ", "Đếm số lần xuất hiện của từng ứng viên."), ("mode hòa", "Hòa giữa 4 và 2 — trả số nhỏ hơn.")],
    ),
    solution='#include <stdio.h>\ndouble mean(const int* a, int n) {\n    int s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    return (double)s / n;\n}\nint count_above(const int* a, int n, int t) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (a[i] > t) c++;\n    return c;\n}\nint mode(const int* a, int n) {\n    int best = 0, best_count = -1;\n    for (int i = 0; i < n; i++) {\n        int c = 0;\n        for (int j = 0; j < n; j++)\n            if (a[j] == a[i]) c++;\n        if (c > best_count || (c == best_count && a[i] < best)) {\n            best_count = c;\n            best = a[i];\n        }\n    }\n    return best;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\ndouble mean(const int* a, int n) {\n    int s = 0;\n    for (int i = 0; i < n; i++) s += a[i];\n    return (double)s / n;\n}\nint count_above(const int* a, int n, int t) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (a[i] > t) c++;\n    return c;\n}\nint mode(const int* a, int n) {\n    int best = 0, best_count = -1;\n    for (int i = 0; i < n; i++) {\n        int c = 0;\n        for (int j = 0; j < n; j++)\n            if (a[j] == a[i]) c++;\n        if (c > best_count || (c == best_count && a[i] > best)) {\n            best_count = c;\n            best = a[i];\n        }\n    }\n    return best;\n}\nint main(void) { return 0; }',
)

# ============================ MODULE 10: strings ============================
M10 = "strings"

L10A = "c-strings-basics"
L10B = "string-library"
L10C = "string-functions"
L10D = "cb-checkpoint-m10"

write_module(
    M10,
    "Strings & Characters",
    "C strings are memory: char arrays with a null terminator. Own the terminator or own the bug.",
    "Chuỗi & Ký tự",
    "Chuỗi C là bộ nhớ: mảng char có ký tự kết thúc null. Làm chủ terminator hoặc làm chủ cái lỗi.",
    [L10A, L10B, L10C, L10D],
    ["cb-p10-strings", "cb-p10-custom"],
)

write_lesson(
    M10,
    L10A,
    "C Strings Are Memory",
    "A string is a char array whose end is marked by '\\0' — nothing more, nothing less.",
    13,
    r"""
## The terminator is the string's length

```c
char word[6] = {'h', 'e', 'l', 'l', 'o', '\0'};
char word2[] = "hello";              // same thing; size 6, terminator included
const char* msg = "hello";           // points at a read-only literal
```

Every string function finds the end by scanning for `'\0'`. No terminator =
the scan runs off the array = undefined behavior. This is the single most
important sentence in this module.

## What's really stored

`"hi"` occupies **3 bytes**: 'h', 'i', '\0'. `strlen("hi")` is 2 (terminator
not counted); the array needs **3** slots.

## Character work

```c
char c = 'A';
if (c >= 'a' && c <= 'z') { /* lowercase letter */ }
char up = c - 'a' + 'A';             // 'b' -> 'B' — arithmetic on codes
char digit_val = '7' - '0';          // 7 — digit char to number
```

Characters are small integers. `'a'..'z'`, `'A'..'Z'`, `'0'..'9'` are each
contiguous ranges (for these sets, in every toolchain you will meet here).

## Literals vs arrays

A string **literal** ("hello") lives in read-only storage: writing through the
pointer is undefined behavior. A char **array** you declared is writable. When
you need to modify, copy into an array first.
""",
    "Chuỗi C là bộ nhớ",
    "Chuỗi là mảng char có ký tự kết thúc '\\0' — không hơn không kém.",

    r"""
## Terminator chính là độ dài của chuỗi

```c
char word[6] = {'h', 'e', 'l', 'l', 'o', '\0'};
char word2[] = "hello";              // y hệt; kích thước 6, gồm cả terminator
const char* msg = "hello";           // trỏ vào literal chỉ-đọc
```

Mọi hàm chuỗi tìm điểm kết thúc bằng cách quét `'\0'`. Thiếu terminator =
quét tràn khỏi mảng = hành vi không xác định. Đây là câu quan trọng nhất của
module này.

## Thực sự lưu những gì

`"hi"` chiếm **3 byte**: 'h', 'i', '\\0'. `strlen("hi")` là 2 (không tính
terminator); mảng cần **3** ô.

## Làm việc với ký tự

```c
char c = 'A';
if (c >= 'a' && c <= 'z') { /* chữ thường */ }
char up = c - 'a' + 'A';             // 'b' -> 'B' — số học trên mã
char digit_val = '7' - '0';          // 7 — ký tự số thành số
```

Ký tự là số nguyên nhỏ. `'a'..'z'`, `'A'..'Z'`, `'0'..'9'` là các khoảng liên
tiếp (với các bộ ký tự này, trong mọi toolchain bạn gặp ở đây).

## Literal hay mảng

String **literal** ("hello") nằm trong vùng chỉ-đọc: ghi qua con trỏ là hành
vi không xác định. Mảng **char** bạn khai báo thì ghi được. Khi cần sửa, hãy
chép vào mảng trước.
""",
)

write_lesson(
    M10,
    L10B,
    "The String Library",
    "strlen, strcpy, strcmp — and the safety rules each one imposes.",
    12,
    r"""
## strlen — the length

```c
#include <string.h>
size_t n = strlen("hello");     // 5 — scans to the terminator
```

Counts characters BEFORE '\\0'. On an unterminated array it reads out of
bounds — the terminator is your responsibility.

## strcpy — the dangerous one

```c
char dst[8];
strcpy(dst, "hello");           // copies 6 bytes (5 + terminator)
```

strcpy copies until the source's terminator and does NOT know how big `dst`
is. Source longer than dst = buffer overflow. The course rule for graded work
and for life: **know the destination size**, and prefer `snprintf` or bounded
copies when the length is not statically obvious:

```c
char dst[8];
snprintf(dst, sizeof dst, "%s", src);   // copies at most sizeof dst - 1 + '\0'
```

## strcmp — comparison is NOT ==

```c
if (a == b)          // compares POINTERS — almost always wrong
if (strcmp(a, b) == 0)  // compares CONTENTS — correct
```

strcmp returns <0, 0, or >0 (lexicographic). Equality is exactly `== 0`.

## The habit to build

Before any string operation, answer: is the destination big enough, and is
the source terminated? If either answer is "not sure", fix that first.
""",
    "Thư viện chuỗi",
    "strlen, strcpy, strcmp — và quy tắc an toàn mà mỗi hàm đặt ra.",

    r"""
## strlen — độ dài

```c
#include <string.h>
size_t n = strlen("hello");     // 5 — quét đến terminator
```

Đếm ký tự TRƯỚC '\\0'. Với mảng không có terminator, nó đọc vượt biên —
terminator là trách nhiệm của bạn.

## strcpy — cái nguy hiểm

```c
char dst[8];
strcpy(dst, "hello");           // chép 6 byte (5 + terminator)
```

strcpy chép đến terminator của nguồn và KHÔNG biết `dst` lớn bao nhiêu. Nguồn
dài hơn dst = tràn bộ đệm. Quy tắc của khóa cho bài có chấm điểm và cho đời:
**biết kích thước đích**, và ưu tiên `snprintf` hoặc chép có chặn khi độ dài
không hiển nhiên:

```c
char dst[8];
snprintf(dst, sizeof dst, "%s", src);   // chép nhiều nhất sizeof dst - 1 + '\\0'
```

## strcmp — so sánh KHÔNG phải ==

```c
if (a == b)             // so sánh CON TRỎ — hầu như luôn sai
if (strcmp(a, b) == 0)  // so sánh NỘI DUNG — đúng
```

strcmp trả về <0, 0, hoặc >0 (theo thứ tự từ điển). Bằng nhau chính xác là
`== 0`.

## Thói quen cần hình thành

Trước mọi phép toán chuỗi, hãy trả lời: đích có đủ chỗ không, và nguồn có
terminator không? Nếu câu nào "chưa chắc", xử lý cái đó trước.
""",
)

write_lesson(
    M10,
    L10C,
    "Writing String Functions",
    "Build strlen/strcmp/your-own by walking the terminator with pointers or indices.",
    12,
    r"""
## my_strlen — the canonical walk

```c
int my_strlen(const char* s) {
    int n = 0;
    while (s[n] != '\\0') n++;
    return n;
}
```

Read the loop as: "advance until the terminator". The idiom version:

```c
int my_strlen(const char* s) {
    const char* p = s;
    while (*p) p++;
    return (int)(p - s);
}
```

## my_strcmp — compare while both agree

```c
int my_strcmp(const char* a, const char* b) {
    while (*a && *a == *b) {   // stop at terminator or first difference
        a++;
        b++;
    }
    return (unsigned char)*a - (unsigned char)*b;
}
```

If the loop ended because both hit '\\0', the difference is 0. Otherwise it
is the code difference at the first mismatch.

## my_strcpy — copy WITH the terminator

```c
void my_strcpy(char* dst, const char* src) {
    while (*src) {
        *dst = *src;
        dst++;
        src++;
    }
    *dst = '\\0';              // the step beginners forget
}
```

Copy characters, then copy the terminator. Without that last line the
destination is not a string.
""",
    "Tự viết hàm chuỗi",
    "Dựng strlen/strcmp/hàm riêng bằng cách đi dọc terminator với con trỏ hoặc chỉ số.",

    r"""
## my_strlen — lượt đi kinh điển

```c
int my_strlen(const char* s) {
    int n = 0;
    while (s[n] != '\\0') n++;
    return n;
}
```

Đọc vòng lặp là: "tiến đến khi gặp terminator". Dạng thành ngữ:

```c
int my_strlen(const char* s) {
    const char* p = s;
    while (*p) p++;
    return (int)(p - s);
}
```

## my_strcmp — so sánh trong khi cả hai còn giống nhau

```c
int my_strcmp(const char* a, const char* b) {
    while (*a && *a == *b) {   // dừng ở terminator hoặc khác đầu tiên
        a++;
        b++;
    }
    return (unsigned char)*a - (unsigned char)*b;
}
```

Nếu vòng lặp kết thúc vì cả hai chạm '\\0', hiệu số là 0. Nếu không, đó là
hiệu mã tại vị trí khác nhau đầu tiên.

## my_strcpy — chép KÈM terminator

```c
void my_strcpy(char* dst, const char* src) {
    while (*src) {
        *dst = *src;
        dst++;
        src++;
    }
    *dst = '\\0';              // bước người mới hay quên
}
```

Chép từng ký tự, rồi chép terminator. Thiếu dòng cuối, đích không phải là
một chuỗi.
""",
)

write_practice(
    M10,
    "cb-p10-strings",
    "String Library Practice",
    "Use the standard string functions safely.",
    "Luyện thư viện chuỗi",
    "Dùng các hàm chuỗi chuẩn một cách an toàn.",
    L10B,
    14,
    "beginner",
    [
        challenge(
            "cb10-length-report",
            "Length Report",
            "Implement `int length_of(const char* s)` returning strlen(s) as an int. Return -1 for NULL.",
            C_PRELUDE,
            [
                ("normal", "CHECK_EQ(length_of(\"hello\"), 5);", "Delegate to strlen."),
                ("empty", "CHECK_EQ(length_of(\"\"), 0);", "The empty string still has a terminator."),
                ("null safe", "CHECK_EQ(length_of(NULL), -1);", "Check for NULL before calling strlen."),
            ],
            level="imitation",
        ),
        challenge(
            "cb10-equal-content",
            "Content Equality",
            'Implement `int same_word(const char* a, const char* b)` returning 1 when the two strings have equal content (strcmp == 0), else 0.',
            C_PRELUDE,
            [
                ("equal", "char x[] = \"cat\";\nchar y[] = \"cat\";\nCHECK_EQ(same_word(x, y), 1);", "strcmp returns 0 on equality — compare CONTENTS: two arrays are distinct objects."),
                ("different", "CHECK_EQ(same_word(\"cat\", \"car\"), 0);", "One differing character is enough."),
                ("case matters", "CHECK_EQ(same_word(\"Cat\", \"cat\"), 0);", "'C' and 'c' are different codes."),
            ],
            level="guided",
        ),
        challenge(
            "cb10-upper-count",
            "Uppercase Counter",
            "Implement `int count_upper(const char* s)` counting 'A'..'Z' characters.",
            C_PRELUDE,
            [
                ("mixed", "CHECK_EQ(count_upper(\"Hello World\"), 2);", "Walk until the terminator."),
                ("none", "CHECK_EQ(count_upper(\"quiet\"), 0);", "No matches: 0."),
                ("all", "CHECK_EQ(count_upper(\"ABC\"), 3);", "Every character matches."),
            ],
            level="guided",
        ),
        challenge(
            "cb10-censor-vowels",
            "Vowel Censor",
            "Implement `void censor(char* s)` replacing every vowel (a/e/i/o/u, both cases) IN PLACE with '*'.",
            C_PRELUDE,
            [
                ("mixed", "char s[] = \"banana\";\ncensor(s);\nCHECK_STR_EQ(s, \"b*n*n*\");", "Modify the writable copy."),
                ("no vowels", "char s[] = \"rhythm\";\ncensor(s);\nCHECK_STR_EQ(s, \"rhythm\");", "Nothing changes."),
                ("case", "char s[] = \"ApE\";\ncensor(s);\nCHECK_STR_EQ(s, \"*p*\");", "Handle uppercase too."),
            ],
            level="independent",
        ),
    ],
    {
        "cb10-length-report": vi_challenge(
            "Báo cáo độ dài",
            "Cài `int length_of(const char* s)` trả về strlen(s) dưới dạng int. Trả -1 cho NULL.",
            [("thường", "Ủy thác cho strlen."), ("rỗng", "Chuỗi rỗng vẫn có terminator."), ("an toàn NULL", "Kiểm tra NULL trước khi gọi strlen.")],
        ),
        "cb10-equal-content": vi_challenge(
            "Bằng nhau nội dung",
            "Cài `int same_word(const char* a, const char* b)` trả 1 khi hai chuỗi có nội dung bằng nhau (strcmp == 0), ngược lại 0.",
            [("bằng nhau", "strcmp trả 0 khi bằng nhau — so sánh NỘI DUNG: hai mảng là hai đối tượng riêng biệt."), ("khác nhau", "Một ký tự khác là đủ."), ("phân biệt hoa thường", "'C' và 'c' là hai mã khác nhau.")],
        ),
        "cb10-upper-count": vi_challenge(
            "Đếm chữ hoa",
            "Cài `int count_upper(const char* s)` đếm các ký tự 'A'..'Z'.",
            [("hỗn hợp", "Đi đến khi gặp terminator."), ("không có", "Không khớp: 0."), ("toàn bộ", "Mọi ký tự đều khớp.")],
        ),
        "cb10-censor-vowels": vi_challenge(
            "Kiểm duyệt nguyên âm",
            "Cài `void censor(char* s)` thay mọi nguyên âm (a/e/i/o/u, cả hai dạng chữ) THÀNH '*' TẠI CHỖ.",
            [("hỗn hợp", "Sửa trên bản ghi được."), ("không nguyên âm", "Không đổi gì."), ("chữ hoa", "Xử lý cả chữ hoa.")],
        ),
    },
    solutions=[
        (
            "cb10-length-report",
            '#include <stdio.h>\n#include <string.h>\nint length_of(const char* s) {\n    if (s == NULL) return -1;\n    return (int)strlen(s);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nint length_of(const char* s) {\n    return (int)strlen(s);\n}\nint main(void) { return 0; }',
        ),
        (
            "cb10-equal-content",
            '#include <stdio.h>\n#include <string.h>\nint same_word(const char* a, const char* b) {\n    return strcmp(a, b) == 0;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nint same_word(const char* a, const char* b) {\n    return *a == *b;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb10-upper-count",
            '#include <stdio.h>\nint count_upper(const char* s) {\n    int n = 0;\n    for (int i = 0; s[i] != 0; i++)\n        if (s[i] >= \'A\' && s[i] <= \'Z\') n++;\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint count_upper(const char* s) {\n    int n = 0;\n    for (int i = 0; s[i] != 0; i++)\n        if (s[i] >= \'a\' && s[i] <= \'z\') n++;\n    return n;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb10-censor-vowels",
            '#include <stdio.h>\nstatic int is_vowel(char c) {\n    return c==\'a\'||c==\'e\'||c==\'i\'||c==\'o\'||c==\'u\'||\n           c==\'A\'||c==\'E\'||c==\'I\'||c==\'O\'||c==\'U\';\n}\nvoid censor(char* s) {\n    for (int i = 0; s[i] != 0; i++)\n        if (is_vowel(s[i])) s[i] = \'*\';\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstatic int is_vowel(char c) {\n    return c==\'a\'||c==\'e\'||c==\'i\'||c==\'o\'||c==\'u\';\n}\nvoid censor(char* s) {\n    for (int i = 0; s[i] != 0; i++)\n        if (is_vowel(s[i])) s[i] = \'*\';\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M10,
    "cb-p10-custom",
    "Custom String Functions",
    "Rebuild the library from scratch — terminator discipline required.",
    "Hàm chuỗi tự viết",
    "Dựng lại thư viện từ đầu — bắt buộc kỷ luật terminator.",
    L10C,
    15,
    "beginner",
    [
        challenge(
            "cb10-my-strlen",
            "my_strlen",
            "Implement `int my_strlen(const char* s)` WITHOUT calling strlen — walk to the terminator yourself.",
            C_PRELUDE,
            [
                ("basics", 'CHECK_EQ(my_strlen("hello"), 5);', "while (s[n] != '\\\\0') n++;"),
                ("empty", 'CHECK_EQ(my_strlen(""), 0);', "The terminator is index 0."),
            ],
            level="imitation",
        ),
        challenge(
            "cb10-my-strcmp",
            "my_strcmp",
            "Implement `int my_strcmp(const char* a, const char* b)` returning negative/zero/positive like strcmp, without calling it.",
            C_PRELUDE,
            [
                ("equal", 'CHECK_EQ(my_strcmp("abc", "abc"), 0);', "Walk while both match."),
                ("less", 'CHECK(my_strcmp("abc", "abd") < 0);', "First differing character decides."),
                ("prefix", 'CHECK(my_strcmp("ab", "abc") < 0);', "The shorter string ends first: its terminator is 'smaller'."),
            ],
            level="guided",
        ),
        challenge(
            "cb10-my-strcpy",
            "my_strcpy",
            "Implement `void my_strcpy(char* dst, const char* src)` copying WITH the terminator, without calling strcpy.",
            C_PRELUDE,
            [
                ("copy", 'char d[16];\nmy_strcpy(d, "cat");\nCHECK_STR_EQ(d, "cat");', "Copy chars, then the terminator."),
                ("terminator copied", 'char d[16] = {\'X\',\'X\',\'X\',\'X\',\'X\',\'X\'};\nmy_strcpy(d, "hi");\nCHECK_EQ(d[2], 0);', "d[2] must be the new terminator, not old data."),
            ],
            level="guided",
        ),
        challenge(
            "cb10-my-strcat",
            "my_strcat",
            "Implement `void my_strcat(char* dst, const char* src)` APPENDING src after dst's current content (dst big enough is guaranteed), keeping one terminator.",
            C_PRELUDE,
            [
                ("append", 'char d[16];\nmemset(d, \'X\', sizeof d);\nd[0]=\'h\'; d[1]=\'i\'; d[2]=0;\nmy_strcat(d, "!");\nCHECK_STR_EQ(d, "hi!");', "Find dst's terminator, copy from there, and write the terminator."),
                ("append empty", 'char d[16] = "abc";\nmy_strcat(d, "");\nCHECK_STR_EQ(d, "abc");', "Appending the empty string changes nothing."),
            ],
            level="independent",
        ),
    ],
    {
        "cb10-my-strlen": vi_challenge(
            "my_strlen",
            "Cài `int my_strlen(const char* s)` KHÔNG gọi strlen — tự đi đến terminator.",
            [("cơ bản", "while (s[n] != '\\\\0') n++;"), ("rỗng", "Terminator nằm ở chỉ số 0.")],
        ),
        "cb10-my-strcmp": vi_challenge(
            "my_strcmp",
            "Cài `int my_strcmp(const char* a, const char* b)` trả âm/không/dương như strcmp, không gọi strcmp.",
            [("bằng nhau", "Đi trong khi cả hai còn khớp."), ("nhỏ hơn", "Ký tự khác nhau đầu tiên quyết định."), ("tiền tố", "Chuỗi ngắn kết thúc trước: terminator của nó 'nhỏ hơn'.")],
        ),
        "cb10-my-strcpy": vi_challenge(
            "my_strcpy",
            "Cài `void my_strcpy(char* dst, const char* src)` chép KÈM terminator, không gọi strcpy.",
            [("chép", "Chép ký tự, rồi chép terminator."), ("terminator được chép", "d[2] phải là terminator mới, không phải dữ liệu cũ.")],
        ),
        "cb10-my-strcat": vi_challenge(
            "my_strcat",
            "Cài `void my_strcat(char* dst, const char* src)` NỐI src sau nội dung hiện tại của dst (đảm bảo dst đủ chỗ), giữ đúng một terminator.",
            [("nối", "Tìm terminator của dst, chép bắt đầu từ đó."), ("nối rỗng", "Nối chuỗi rỗng không đổi gì.")],
        ),
    },
    solutions=[
        (
            "cb10-my-strlen",
            '#include <stdio.h>\nint my_strlen(const char* s) {\n    int n = 0;\n    while (s[n] != 0) n++;\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint my_strlen(const char* s) {\n    int n = 1;\n    while (s[n] != 0) n++;\n    return n;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb10-my-strcmp",
            '#include <stdio.h>\nint my_strcmp(const char* a, const char* b) {\n    while (*a && *a == *b) {\n        a++;\n        b++;\n    }\n    return (unsigned char)*a - (unsigned char)*b;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint my_strcmp(const char* a, const char* b) {\n    while (*a == *b) {\n        a++;\n        b++;\n    }\n    return (unsigned char)*a - (unsigned char)*b;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb10-my-strcpy",
            '#include <stdio.h>\nvoid my_strcpy(char* dst, const char* src) {\n    while (*src) {\n        *dst = *src;\n        dst++;\n        src++;\n    }\n    *dst = 0;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid my_strcpy(char* dst, const char* src) {\n    while (*src) {\n        *dst = *src;\n        dst++;\n        src++;\n    }\n}\nint main(void) { return 0; }',
        ),
        (
            "cb10-my-strcat",
            '#include <stdio.h>\nvoid my_strcat(char* dst, const char* src) {\n    while (*dst) dst++;\n    while (*src) {\n        *dst = *src;\n        dst++;\n        src++;\n    }\n    *dst = 0;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nvoid my_strcat(char* dst, const char* src) {\n    while (*dst) dst++;\n    while (*src) {\n        *dst = *src;\n        dst++;\n        src++;\n    }\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M10,
    L10D,
    "Checkpoint: Strings",
    "A word analyzer: length, digit count, and in-place title casing of a word.",
    16,
    r"""
## Checkpoint

Terminator discipline under composition: three string utilities working
together.
""",
    "Điểm kiểm tra: Chuỗi",
    "Kỷ luật terminator khi kết hợp: ba tiện ích chuỗi cùng làm việc.",

    r"""
## Điểm kiểm tra

Kỷ luật terminator khi kết hợp: ba tiện ích chuỗi cùng làm việc.
""",
    challenge(
        "cb10-checkpoint-word",
        "Word Analyzer",
        "Implement `int word_length(const char* w)` (length, -1 for NULL), `int digit_count(const char* s)` (count of '0'..'9'), and `void title_case(char* w)` (uppercase the FIRST letter a-z in place; leave everything else).",
        C_PRELUDE,
        [
            ("length", "CHECK_EQ(word_length(\"keyboard\"), 8);\nCHECK_EQ(word_length(NULL), -1);", "Delegate to strlen after the NULL check."),
            ("digits", "CHECK_EQ(digit_count(\"a1b22c\"), 3);\nCHECK_EQ(digit_count(\"no\"), 0);", "'0'..'9' is a contiguous range: 1, 2, 2 here."),
            ("title case", "char w[] = \"hello\";\ntitle_case(w);\nCHECK_STR_EQ(w, \"Hello\");", "w[0] = w[0] - 'a' + 'A' when it is lowercase."),
            ("title case guard", "char w[] = \"9lives\";\ntitle_case(w);\nCHECK_STR_EQ(w, \"9lives\");", "A non-letter first character is left alone."),
        ],
    ),
    vi_challenge(
        "Bộ phân tích từ",
        "Cài `int word_length(const char* w)` (độ dài, -1 cho NULL), `int digit_count(const char* s)` (đếm '0'..'9'), và `void title_case(char* w)` (viết hoa chữ cái ĐẦU TIÊN a-z tại chỗ; phần còn lại giữ nguyên).",
        [("độ dài", "Ủy thác cho strlen sau kiểm tra NULL."), ("chữ số", "'0'..'9' là khoảng liên tiếp."), ("viết hoa", "w[0] = w[0] - 'a' + 'A' khi nó là chữ thường."), ("viết hoa có gác", "Ký tự đầu không phải chữ cái thì giữ nguyên.")],
    ),
    solution='#include <stdio.h>\n#include <string.h>\nint word_length(const char* w) {\n    if (w == NULL) return -1;\n    return (int)strlen(w);\n}\nint digit_count(const char* s) {\n    int n = 0;\n    for (int i = 0; s[i] != 0; i++)\n        if (s[i] >= \'0\' && s[i] <= \'9\') n++;\n    return n;\n}\nvoid title_case(char* w) {\n    if (w[0] >= \'a\' && w[0] <= \'z\') w[0] = (char)(w[0] - \'a\' + \'A\');\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\n#include <string.h>\nint word_length(const char* w) {\n    if (w == NULL) return 0;\n    return (int)strlen(w);\n}\nint digit_count(const char* s) {\n    int n = 0;\n    for (int i = 0; s[i] != 0; i++)\n        if (s[i] >= \'0\' && s[i] <= \'9\') n++;\n    return n;\n}\nvoid title_case(char* w) {\n    if (w[0] >= \'a\' && w[0] <= \'z\') w[0] = (char)(w[0] - \'a\' + \'A\');\n}\nint main(void) { return 0; }',
)

print("batch 5 complete: modules 9-10")
