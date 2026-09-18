#!/usr/bin/env python3
"""C Beginner — batch 3: modules 5 (conditionals) and 6 (loops)."""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ============================ MODULE 5: conditionals ============================
M5 = "conditionals"

L5A = "if-else-else-if"
L5B = "switch-cases"
L5C = "cb-checkpoint-m5"

write_module(
    M5,
    "Conditional Logic",
    "if/else chains, nested decisions, and switch — teaching programs to choose.",
    "Logic Điều Kiện",
    "Chuỗi if/else, điều kiện lồng nhau và switch — dạy chương trình biết lựa chọn.",
    [L5A, L5B, L5C],
    ["cb-p5-decisions", "cb-p5-menu"],
)

write_lesson(
    M5,
    L5A,
    "if, else, and else if",
    "The decision ladder: exact syntax, common shapes, and the dangling-else pitfall.",
    11,
    r"""
## The ladder

```c
if (score >= 90) {
    grade = 'A';
} else if (score >= 80) {
    grade = 'B';
} else {
    grade = 'F';
}
```

Conditions test top to bottom; the FIRST true branch runs and the rest are
skipped. The final `else` catches everything remaining — put the most specific
test first.

## Brace discipline

Braces are optional for a single statement — and a standing trap:

```c
if (x > 0)
    printf("positive\n");
    printf("always prints!\n");   // NOT part of the if
```

Rule for this course: **always brace**.

## Ternary: a tiny if as an expression

```c
const char* sign = (x >= 0) ? "non-negative" : "negative";
```

Use it for choosing a value; keep real logic in `if`.
""",
    "if, else và else if",
    "Thang quyết định: cú pháp chính xác, các dạng thường gặp và bẫy else lơ lửng.",

    r"""
## Thang điều kiện

```c
if (score >= 90) {
    grade = 'A';
} else if (score >= 80) {
    grade = 'B';
} else {
    grade = 'F';
}
```

Điều kiện được xét từ trên xuống; nhánh ĐẦU TIÊN đúng chạy và phần còn lại bị
bỏ qua. `else` cuối cùng hứng tất cả phần còn lại — đặt điều kiện cụ thể nhất
lên đầu.

## Kỷ luật ngoặc

Ngoặc là tùy chọn cho một câu lệnh — và là cái bẫy kinh điển:

```c
if (x > 0)
    printf("positive\n");
    printf("always prints!\n");   // KHÔNG thuộc if
```

Quy tắc của khóa này: **luôn dùng ngoặc**.

## Toán tử điều kiện: một if nhỏ dưới dạng biểu thức

```c
const char* sign = (x >= 0) ? "không âm" : "âm";
```

Dùng nó để CHỌN một giá trị; logic thật hãy để trong `if`.
""",
)

write_lesson(
    M5,
    L5B,
    "switch, case, and fall-through",
    "Multi-way branching on one value: case labels, break, default, and when switch beats if.",
    10,
    r"""
## The shape

```c
switch (choice) {
    case 1:
        printf("deposit\n");
        break;
    case 2:
        printf("withdraw\n");
        break;
    default:
        printf("unknown\n");
        break;
}
```

- The controlling value must be an integer type (int, char, enum — module 15).
- `case` labels are entry points, not sections: **without `break`, execution
  falls through into the next case.** Occasionally useful (grouping cases),
  usually a bug.
- `default` runs when nothing matched — handle it explicitly.

## switch vs if

Use `switch` when one integral value selects among fixed options (menus,
state codes). Use `if` for ranges (`x > 100`) and mixed conditions.
""",
    "switch, case và fall-through",
    "Rẽ nhánh nhiều hướng trên một giá trị: nhãn case, break, default, và khi nào switch hơn if.",

    r"""
## Dạng chuẩn

```c
switch (choice) {
    case 1:
        printf("gui tien\n");
        break;
    case 2:
        printf("rut tien\n");
        break;
    default:
        printf("khong ro\n");
        break;
}
```

- Giá trị điều khiển phải là kiểu nguyên (int, char, enum — mô-đun 15).
- Nhãn `case` là điểm vào, không phải mục: **không có `break`, việc chạy sẽ
  rơi xuống case kế tiếp.** Đôi khi hữu ích (gom nhóm case), thường là lỗi.
- `default` chạy khi không khớp gì — hãy xử lý tường minh.

## switch hay if

Dùng `switch` khi một giá trị nguyên chọn giữa các lựa chọn cố định (menu, mã
trạng thái). Dùng `if` cho khoảng (`x > 100`) và điều kiện hỗn hợp.
""",
)

write_practice(
    M5,
    "cb-p5-decisions",
    "Decision Bench",
    "Grade ladders, eligibility, and branch coverage — every path verified.",
    "Bàn quyết định",
    "Thang điểm, điều kiện đủ điều kiện và bao phủ nhánh — mọi đường đi đều được xác minh.",
    L5A,
    14,
    "beginner",
    [
        challenge(
            "cb5-grade-ladder",
            "Grade Ladder",
            "Implement `char grade_for(int score)`: >=90 'A', >=80 'B', >=70 'C', >=60 'D', else 'F'.",
            C_PRELUDE,
            [
                ("top band", "CHECK_EQ(grade_for(95), 'A');", "First true branch wins."),
                ("middle band", "CHECK_EQ(grade_for(74), 'C');", "Order the ladder from high to low."),
                ("bottom band", "CHECK_EQ(grade_for(12), 'F');", "The final else catches these."),
                ("boundaries", "CHECK_EQ(grade_for(90), 'A');\nCHECK_EQ(grade_for(89), 'B');\nCHECK_EQ(grade_for(70), 'C');\nCHECK_EQ(grade_for(69), 'D');\nCHECK_EQ(grade_for(60), 'D');\nCHECK_EQ(grade_for(59), 'F');", "Each boundary belongs to the higher band (>=)."),
            ],
            level="imitation",
        ),
        challenge(
            "cb5-eligibility",
            "Eligibility Rules",
            "Implement `int can_rent_car(int age, int license_years)`: eligible when age >= 21 AND license_years >= 1; a driver under 21 is never eligible, no matter the years. Return 1/0.",
            C_PRELUDE,
            [
                ("young no license", "CHECK_EQ(can_rent_car(22, 0), 0);", "Under 25 needs at least 1 license year."),
                ("young with license", "CHECK_EQ(can_rent_car(22, 1), 1);\nCHECK_EQ(can_rent_car(22, 2), 1);", "age >= 21 && license_years >= 1 — one year is enough."),
                ("too young entirely", "CHECK_EQ(can_rent_car(19, 5), 0);", "age < 21 is never eligible."),
                ("senior shortcut", "CHECK_EQ(can_rent_car(25, 1), 1);\nCHECK_EQ(can_rent_car(30, 1), 1);", "25+ with >= 1 year is eligible."),
            ],
            level="independent",
        ),
        challenge(
            "cb5-bmi-band",
            "BMI Band",
            "Implement `const char* bmi_band(double bmi)`: below 18.5 -> \"under\", below 25 -> \"normal\", below 30 -> \"over\", else \"obese\". Return the exact strings.",
            C_PRELUDE,
            [
                ("under", 'CHECK_STR_EQ(bmi_band(17.0), "under");', "First threshold."),
                ("normal boundary", 'CHECK_STR_EQ(bmi_band(18.5), "normal");\nCHECK_STR_EQ(bmi_band(24.9), "normal");', "18.5 is INCLUDED in normal."),
                ("over", 'CHECK_STR_EQ(bmi_band(25.0), "over");', "25 starts the over band."),
                ("obese", 'CHECK_STR_EQ(bmi_band(31.0), "obese");', "The final else."),
            ],
            level="guided",
        ),
    ],
    {
        "cb5-grade-ladder": vi_challenge(
            "Thang điểm",
            "Cài `char grade_for(int score)`: >=90 'A', >=80 'B', >=70 'C', >=60 'D', còn lại 'F'.",
            [("dải trên", "Nhánh đúng đầu tiên thắng."), ("dải giữa", "Sắp thang từ cao xuống thấp."), ("dải dưới", "else cuối hứng các trường hợp này."), ("biên", "Mỗi biên thuộc dải cao hơn (>=).")],
        ),
        "cb5-eligibility": vi_challenge(
            "Điều kiện thuê xe",
            "Cài `int can_rent_car(int age, int license_years)`: đủ điều kiện khi age >= 21 VÀ license_years >= 1; nhưng tài xế từ 25 tuổi chỉ cần giấy phép hợp lệ (>= 1 năm). Trả 1/0.",
            [("trẻ không giấy phép", "Dưới 25 cần ít nhất 1 năm giấy phép."), ("trẻ có giấy phép", "age >= 21 && license_years >= 1."), ("quá trẻ", "age < 21 không bao giờ đủ."), ("đường tắt 25+", "Từ 25 với >= 1 năm là đủ.")],
        ),
        "cb5-bmi-band": vi_challenge(
            "Dải BMI",
            "Cài `const char* bmi_band(double bmi)`: dưới 18.5 -> \"under\", dưới 25 -> \"normal\", dưới 30 -> \"over\", còn lại \"obese\". Trả về đúng chuỗi.",
            [("under", "Ngưỡng đầu tiên."), ("biên normal", "18.5 NẰM TRONG normal."), ("over", "25 bắt đầu dải over."), ("obese", "else cuối cùng.")],
        ),
    },
    solutions=[
        (
            "cb5-grade-ladder",
            "#include <stdio.h>\nchar grade_for(int score) {\n    if (score >= 90) return 'A';\n    if (score >= 80) return 'B';\n    if (score >= 70) return 'C';\n    if (score >= 60) return 'D';\n    return 'F';\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nchar grade_for(int score) {\n    if (score >= 90) return 'A';\n    if (score >= 80) return 'B';\n    if (score > 70) return 'C';\n    if (score >= 60) return 'D';\n    return 'F';\n}\nint main(void) { return 0; }",
        ),
        (
            "cb5-eligibility",
            "#include <stdio.h>\nint can_rent_car(int age, int license_years) {\n    if (age < 21) return 0;\n    if (age >= 25) return license_years >= 1;\n    return license_years >= 1;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nint can_rent_car(int age, int license_years) {\n    if (age < 21) return 0;\n    if (age >= 25) return license_years >= 1;\n    return license_years >= 2;\n}\nint main(void) { return 0; }",
        ),
        (
            "cb5-bmi-band",
            '#include <stdio.h>\nconst char* bmi_band(double bmi) {\n    if (bmi < 18.5) return "under";\n    if (bmi < 25.0) return "normal";\n    if (bmi < 30.0) return "over";\n    return "obese";\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nconst char* bmi_band(double bmi) {\n    if (bmi <= 18.5) return "under";\n    if (bmi < 25.0) return "normal";\n    if (bmi < 30.0) return "over";\n    return "obese";\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M5,
    "cb-p5-menu",
    "Menu Machine",
    "switch dispatch with default handling — the graded skeleton of every console menu.",
    "Cỗ máy menu",
    "Điều phối switch với xử lý default — bộ khung được chấm của mọi menu console.",
    L5B,
    12,
    "beginner",
    [
        challenge(
            "cb5-menu-dispatch",
            "Menu Dispatch",
            "Implement `const char* menu_action(int choice)` using switch: 1 -> \"deposit\", 2 -> \"withdraw\", 3 -> \"balance\", any other value -> \"unknown\".",
            C_PRELUDE,
            [
                ("known choices", 'CHECK_STR_EQ(menu_action(1), "deposit");\nCHECK_STR_EQ(menu_action(2), "withdraw");\nCHECK_STR_EQ(menu_action(3), "balance");', "One case per choice, each with break."),
                ("default catches rest", 'CHECK_STR_EQ(menu_action(9), "unknown");\nCHECK_STR_EQ(menu_action(-1), "unknown");', "The default label."),
            ],
            level="imitation",
        ),
        challenge(
            "cb5-fallthrough-fix",
            "Stop the Fall-Through",
            "This `dispatch` is missing its breaks, so choosing 1 reports the wrong thing. Fix it so each choice reports ONLY its own label (1 -> \"one\", 2 -> \"two\", else \"many\").",
            '#include <stdio.h>\n\nconst char* dispatch(int n) {\n    /* BROKEN: falls through */\n    switch (n) {\n        case 1:\n        case 2:\n            return "many";\n        default:\n            return "many";\n    }\n}\n\nint main(void) { return 0; }',
            [
                ("one is isolated", 'CHECK_STR_EQ(dispatch(1), "one");', "case 1 needs its own return/break."),
                ("two stays", 'CHECK_STR_EQ(dispatch(2), "two");', "case 2 reports two."),
                ("rest is many", 'CHECK_STR_EQ(dispatch(5), "many");', "default unchanged."),
            ],
            level="debugging",
        ),
    ],
    {
        "cb5-menu-dispatch": vi_challenge(
            "Điều phối menu",
            "Cài `const char* menu_action(int choice)` dùng switch: 1 -> \"deposit\", 2 -> \"withdraw\", 3 -> \"balance\", giá trị khác -> \"unknown\".",
            [("lựa chọn đã biết", "Mỗi case một lựa chọn, đều có break."), ("default hứng phần còn lại", "Nhãn default.")],
        ),
        "cb5-fallthrough-fix": vi_challenge(
            "Chặn fall-through",
            "`dispatch` thiếu break nên chọn 1 báo sai. Sửa để mỗi lựa chọn chỉ báo nhãn của mình (1 -> \"one\", 2 -> \"two\", còn lại \"many\").",
            [("one tách riêng", "case 1 cần return/break riêng."), ("two giữ nguyên", "case 2 báo two."), ("còn lại là many", "default không đổi.")],
        ),
    },
    solutions=[
        (
            "cb5-menu-dispatch",
            '#include <stdio.h>\nconst char* menu_action(int choice) {\n    switch (choice) {\n        case 1: return "deposit";\n        case 2: return "withdraw";\n        case 3: return "balance";\n        default: return "unknown";\n    }\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nconst char* menu_action(int choice) {\n    switch (choice) {\n        case 1: return "deposit";\n        case 2: return "withdraw";\n        default: return "unknown";\n    }\n}\nint main(void) { return 0; }',
        ),
        (
            "cb5-fallthrough-fix",
            '#include <stdio.h>\nconst char* dispatch(int n) {\n    switch (n) {\n        case 1: return "one";\n        case 2: return "two";\n        default: return "many";\n    }\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nconst char* dispatch(int n) {\n    switch (n) {\n        case 1:\n        case 2: return "many";\n        default: return "many";\n    }\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M5,
    L5C,
    "Checkpoint: Conditional Logic",
    "A shipping-rate calculator: tiers, edge cases, and one switch.",
    15,
    r"""
## Checkpoint

Conditions feed real decisions: a tiered pricing function with exact edge
behavior plus a switch-driven category label.
""",
    "Điểm kiểm tra: Logic Điều Kiện",
    "Điều kiện nuôi quyết định thật: hàm giá theo bậc với hành vi biên chính xác cùng một nhãn danh mục theo switch.",

    r"""
## Điểm kiểm tra

Điều kiện nuôi quyết định thật: hàm giá theo bậc với hành vi biên chính xác
cùng một nhãn danh mục theo switch.
""",
    challenge(
        "cb5-checkpoint-shipping",
        "Shipping Calculator",
        "Implement two functions.\n\n1. `double shipping_cost(double weight)`: up to and including 1.0 kg -> 5.00; over 1.0 up to and including 5.0 -> 10.00; above 5.0 -> 10.00 + 1.50 per full kg above 5 (so 6.2 kg -> 11.50).\n2. `const char* shipping_label(int speed)` using switch: 1 -> \"standard\", 2 -> \"express\", default -> \"standard\".",
        C_PRELUDE,
        [
            ("tier boundaries", "CHECK_NEAR(shipping_cost(1.0), 5.00, 1e-9);\nCHECK_NEAR(shipping_cost(1.01), 10.00, 1e-9);\nCHECK_NEAR(shipping_cost(5.0), 10.00, 1e-9);", "Both 'up to and including' edges are inclusive."),
            ("overage math", "CHECK_NEAR(shipping_cost(6.2), 11.50, 1e-9);\nCHECK_NEAR(shipping_cost(7.0), 13.00, 1e-9);", "Full kg above 5: (int)(weight - 5) when weight > 5. 6.2 -> 1 extra -> 11.50; 7.0 -> 2 extra -> 13.00."),
            ("label switch", 'CHECK_STR_EQ(shipping_label(1), "standard");\nCHECK_STR_EQ(shipping_label(2), "express");\nCHECK_STR_EQ(shipping_label(99), "standard");', "default maps to standard."),
        ],
    ),
    vi_challenge(
        "Máy tính phí vận chuyển",
        "Cài hai hàm: `shipping_cost` theo ba bậc (<=1.0kg -> 5.00; <=5.0 -> 10.00; trên 5.0 cộng 1.50 cho mỗi kg ĐỦ trên 5) và `shipping_label` theo switch (1 -> \"standard\", 2 -> \"express\", mặc định -> \"standard\").",
        [("biên bậc", "Cả hai cạnh 'tính đến' là bao hàm."), ("phí vượt", "Số kg ĐỦ trên 5: 6.2 -> 1 -> 11.50; 7.0 -> 2 -> 13.00."), ("nhãn switch", "default trả standard.")],
    ),
    solution='#include <stdio.h>\ndouble shipping_cost(double weight) {\n    if (weight <= 1.0) return 5.00;\n    if (weight <= 5.0) return 10.00;\n    return 10.00 + 1.50 * (int)(weight - 5.0);\n}\nconst char* shipping_label(int speed) {\n    switch (speed) {\n        case 2: return "express";\n        default: return "standard";\n    }\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\ndouble shipping_cost(double weight) {\n    if (weight < 1.0) return 5.00;\n    if (weight <= 5.0) return 10.00;\n    return 10.00 + 1.50 * (int)(weight - 5.0);\n}\nconst char* shipping_label(int speed) {\n    switch (speed) {\n        case 2: return "express";\n        default: return "standard";\n    }\n}\nint main(void) { return 0; }',
)

# ============================ MODULE 6: loops ============================
M6 = "loops"

L6A = "for-while-do"
L6B = "nested-loops-patterns"
L6C = "break-continue-guard"
L6D = "cb-checkpoint-m6"

write_module(
    M6,
    "Loops",
    "for, while, do-while; nested patterns; break/continue; and loop design that terminates.",
    "Vòng Lặp",
    "for, while, do-while; mẫu lồng nhau; break/continue; và thiết kế vòng lặp có điểm dừng.",
    [L6A, L6B, L6C, L6D],
    ["cb-p6-loops", "cb-p6-patterns"],
)

write_lesson(
    M6,
    L6A,
    "for, while, and do-while",
    "The three loop forms, when each fits, and the anatomy of termination.",
    11,
    r"""
## for: counted repetition

```c
for (int i = 0; i < 5; i++) {
    printf("%d ", i);        // 0 1 2 3 4
}
```

init; condition; step — run init once, test before every pass, step after.
Loop variable visible only inside the loop (declare it there).

## while: condition first

```c
int n = 40;
while (n > 0) {
    n = n / 2;
}
```

Use when the count is unknown in advance. The condition is tested BEFORE the
first pass — a false condition skips the body entirely.

## do-while: body first

```c
int choice;
do {
    choice = read_menu();     // runs at least once
} while (!valid(choice));
```

Tested AFTER each pass. Rare but right for "ask, then check" flows.

## Termination is your job

Every loop needs something inside the body to move the condition toward false.
`while (1)` with no exit is an infinite loop — the sandbox will kill it at the
timeout and the challenge fails.
""",
    "for, while và do-while",
    "Ba dạng vòng lặp, khi nào dùng dạng nào, và giải phẫu của việc kết thúc.",

    r"""
## for: lặp theo biến đếm

```c
for (int i = 0; i < 5; i++) {
    printf("%d ", i);        // 0 1 2 3 4
}
```

khởi_tạo; điều_kiện; bước — chạy khởi tạo một lần, xét điều kiện trước mỗi
lượt, thực hiện bước sau đó. Biến lệnh chỉ tồn tại bên trong vòng (hãy khai
báo tại đó).

## while: điều kiện trước

```c
int n = 40;
while (n > 0) {
    n = n / 2;
}
```

Dùng khi số lượt chưa biết trước. Điều kiện được xét TRƯỚC lượt đầu — điều
kiện sai là bỏ qua toàn bộ thân.

## do-while: thân trước

```c
int choice;
do {
    choice = read_menu();     // chạy ít nhất một lần
} while (!valid(choice));
```

Xét SAU mỗi lượt. Hiếm nhưng đúng cho dạng "hỏi rồi kiểm tra".

## Kết thúc là trách nhiệm của bạn

Mọi vòng lặp cần thứ gì đó trong thân đưa điều kiện tiến về sai. `while (1)`
không lối thoát là vòng vô hạn — sandbox sẽ giết ở timeout và thử thách trượt.
""",
)

write_lesson(
    M6,
    L6B,
    "Nested Loops and Patterns",
    "Rows and columns: loops inside loops, the grid mental model, and printing shapes.",
    11,
    r"""
## The grid model

A loop inside a loop is a grid: the outer loop is ROWS, the inner is COLUMNS.
The inner loop runs completely for each single step of the outer loop.

```c
for (int row = 1; row <= 3; row++) {
    for (int col = 1; col <= row; col++) {
        printf("*");
    }
    printf("\n");
}
```

Output:

```text
*
**
***
```

## Trace before you run

Say it out loud: row 1 prints 1 star; row 2 prints 2; row 3 prints 3. The
inner bound depends on the OUTER variable — that is what makes a triangle, not
a rectangle.

## Cost intuition

3 rows x 3 columns = 9 inner steps. Doubling the side quadruples the work —
loops multiply, and this intuition becomes Big-O thinking later.
""",
    "Vòng lặp lồng và các mẫu hình",
    "Hàng và cột: vòng trong vòng, mô hình lưới, và in các hình.",

    r"""
## Mô hình lưới

Vòng lặp trong vòng lặp là một lưới: vòng ngoài là HÀNG, vòng trong là CỘT.
Vòng trong chạy trọn vẹn cho mỗi một bước của vòng ngoài.

```c
for (int row = 1; row <= 3; row++) {
    for (int col = 1; col <= row; col++) {
        printf("*");
    }
    printf("\n");
}
```

Đầu ra:

```text
*
**
***
```

## Vết trước khi chạy

Nói to: hàng 1 in 1 sao; hàng 2 in 2; hàng 3 in 3. Biên của vòng trong phụ
thuộc biến NGOÀI — điều đó tạo hình tam giác chứ không phải hình chữ nhật.

## Trực giác chi phí

3 hàng x 3 cột = 9 bước trong. Nhân đôi cạnh là nhân tư công việc — vòng lặp
nhân nhau, và trực giác này sau này thành tư duy Big-O.
""",
)

write_lesson(
    M6,
    L6C,
    "break, continue, and Loop Guards",
    "Early exits, skipped iterations, and the two classic loop bugs: off-by-one and the runaway condition.",
    10,
    r"""
## break and continue

- `break` — leave the loop NOW (innermost one only).
- `continue` — skip to the next iteration.

```c
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) continue;   // skip evens
    if (i > 7) break;           // stop after 7
    printf("%d ", i);           // 1 3 5 7
}
```

## Off-by-one

The classic: `<=` vs `<` with a 0-based index.

```c
int a[5] = {1, 2, 3, 4, 5};
for (int i = 0; i <= 5; i++) printf("%d ", a[i]);   // BUG: a[5] is out of bounds
for (int i = 0; i < 5; i++)  printf("%d ", a[i]);   // correct
```

Out-of-bounds access is undefined behavior — the module 9 rule is born here:
**the last valid index is size - 1.**

## The runaway condition

If the update step moves AWAY from the exit condition (`for (int i = 0; i < 5; i--)`),
or nothing in the body changes the tested variable, the loop never ends.
When a loop misbehaves, print the loop variable each pass and watch.
""",
    "break, continue và bảo vệ vòng lặp",
    "Lối thoát sớm, bỏ qua lượt, và hai lỗi vòng lặp kinh điển: lệch một và điều kiện chạy trốn.",

    r"""
## break và continue

- `break` — rời vòng lặp NGAY (chỉ vòng trong cùng).
- `continue` — bỏ qua phần còn lại, sang lượt kế tiếp.

```c
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) continue;   // bỏ qua số chẵn
    if (i > 7) break;           // dừng sau 7
    printf("%d ", i);           // 1 3 5 7
}
```

## Lệch một

Kinh điển: `<=` hay `<` với chỉ số bắt đầu từ 0.

```c
int a[5] = {1, 2, 3, 4, 5};
for (int i = 0; i <= 5; i++) printf("%d ", a[i]);   // LỖI: a[5] ngoài biên
for (int i = 0; i < 5; i++)  printf("%d ", a[i]);   // đúng
```

Truy cập ngoài biên là hành vi không xác định — quy tắc của mô-đun 9 sinh ra
tại đây: **chỉ số hợp lệ cuối cùng là kích thước - 1.**

## Điều kiện chạy trốn

Nếu bước cập nhật đi XA điều kiện thoát (`for (int i = 0; i < 5; i--)`), hoặc
không gì trong thân thay đổi biến được xét, vòng lặp không bao giờ kết thúc.
Khi vòng lặp hành xử lạ, in biến lặp mỗi lượt và quan sát.
""",
)

write_practice(
    M6,
    "cb-p6-loops",
    "Loop Gym",
    "Counters, accumulations, digit tricks, and exact termination.",
    "Phòng gym vòng lặp",
    "Bộ đếm, tích lũy, thủ thuật chữ số và kết thúc chính xác.",
    L6A,
    14,
    "beginner",
    [
        challenge(
            "cb6-sum-to-n",
            "Sum to N",
            "Implement `int sum_to(int n)` returning 1+2+...+n using a loop (not the closed formula).",
            C_PRELUDE,
            [
                ("small n", "CHECK_EQ(sum_to(5), 15);", "Accumulate in a result variable."),
                ("n = 1", "CHECK_EQ(sum_to(1), 1);", "Single iteration."),
                ("n = 0", "CHECK_EQ(sum_to(0), 0);", "A loop that never runs returns the initial 0."),
            ],
            level="imitation",
        ),
        challenge(
            "cb6-factorial",
            "Factorial",
            "Implement `long long factorial(int n)` computing n! iteratively. 0! is 1.",
            C_PRELUDE,
            [
                ("base", "CHECK_EQ(factorial(0), 1);", "Start the accumulator at 1."),
                ("small", "CHECK_EQ(factorial(5), 120);", "Multiply 1*2*3*4*5."),
                ("bigger", "CHECK_EQ(factorial(12), 479001600);", "long long survives 12!."),
            ],
            level="guided",
        ),
        challenge(
            "cb6-digit-sum",
            "Digit Sum",
            "Implement `int digit_sum(int n)` summing the decimal digits of n (n >= 0). Use % 10 and / 10 in a loop.",
            C_PRELUDE,
            [
                ("multi-digit", "CHECK_EQ(digit_sum(1729), 19);", "9 + 2 + 7 + 1."),
                ("single digit", "CHECK_EQ(digit_sum(7), 7);", "One pass."),
                ("zero", "CHECK_EQ(digit_sum(0), 0);", "The loop must not run."),
            ],
            level="independent",
        ),
        challenge(
            "cb6-power-while",
            "Power by While",
            "Implement `int pow_while(int base, int exp)` (exp >= 0) using a while loop, not any library function.",
            C_PRELUDE,
            [
                ("zeroth power", "CHECK_EQ(pow_while(3, 0), 1);", "Result starts at 1; the while may not run."),
                ("cubes", "CHECK_EQ(pow_while(2, 10), 1024);", "Multiply exp times."),
            ],
            level="independent",
        ),
    ],
    {
        "cb6-sum-to-n": vi_challenge(
            "Tổng tới N",
            "Cài `int sum_to(int n)` trả về 1+2+...+n bằng vòng lặp (không dùng công thức kín).",
            [("n nhỏ", "Tích lũy vào biến kết quả."), ("n = 1", "Một lượt duy nhất."), ("n = 0", "Vòng không chạy trả về 0 ban đầu.")],
        ),
        "cb6-factorial": vi_challenge(
            "Giai thừa",
            "Cài `long long factorial(int n)` tính n! bằng vòng lặp. 0! là 1.",
            [("cơ sở", "Khởi tạo biến tích lũy bằng 1."), ("nhỏ", "Nhân 1*2*3*4*5."), ("lớn hơn", "long long chịu nổi 12!.")],
        ),
        "cb6-digit-sum": vi_challenge(
            "Tổng chữ số",
            "Cài `int digit_sum(int n)` tính tổng các chữ số thập phân của n (n >= 0). Dùng % 10 và / 10.",
            [("nhiều chữ số", "9 + 2 + 7 + 1."), ("một chữ số", "Một lượt."), ("không", "Vòng không được chạy.")],
        ),
        "cb6-power-while": vi_challenge(
            "Lũy thừa bằng while",
            "Cài `int pow_while(int base, int exp)` (exp >= 0) dùng while, không dùng hàm thư viện.",
            [("mũ 0", "Kết quả bắt đầu bằng 1; while có thể không chạy."), ("lập phương", "Nhân exp lần.")],
        ),
    },
    solutions=[
        (
            "cb6-sum-to-n",
            "#include <stdio.h>\nint sum_to(int n) {\n    int s = 0;\n    for (int i = 1; i <= n; i++) s += i;\n    return s;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nint sum_to(int n) {\n    int s = 0;\n    for (int i = 1; i < n; i++) s += i;\n    return s;\n}\nint main(void) { return 0; }",
        ),
        (
            "cb6-factorial",
            "#include <stdio.h>\nlong long factorial(int n) {\n    long long r = 1;\n    for (int i = 2; i <= n; i++) r *= i;\n    return r;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nlong long factorial(int n) {\n    long long r = 0;\n    for (int i = 2; i <= n; i++) r *= i;\n    return r;\n}\nint main(void) { return 0; }",
        ),
        (
            "cb6-digit-sum",
            "#include <stdio.h>\nint digit_sum(int n) {\n    int s = 0;\n    while (n > 0) {\n        s += n % 10;\n        n /= 10;\n    }\n    return s;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nint digit_sum(int n) {\n    int s = 0;\n    while (n > 0) {\n        s += n % 10;\n        n /= 100;\n    }\n    return s;\n}\nint main(void) { return 0; }",
        ),
        (
            "cb6-power-while",
            "#include <stdio.h>\nint pow_while(int base, int exp) {\n    int result = 1;\n    while (exp > 0) {\n        result *= base;\n        exp--;\n    }\n    return result;\n}\nint main(void) { return 0; }",
            "#include <stdio.h>\nint pow_while(int base, int exp) {\n    int result = 1;\n    while (exp > 0) {\n        result += base;\n        exp--;\n    }\n    return result;\n}\nint main(void) { return 0; }",
        ),
    ],
)

write_practice(
    M6,
    "cb-p6-patterns",
    "Pattern Factory",
    "Nested loops producing exact shapes and tables.",
    "Xưởng mẫu hình",
    "Vòng lặp lồng tạo hình và bảng chính xác.",
    L6B,
    14,
    "beginner",
    [
        challenge(
            "cb6-star-triangle",
            "Star Triangle",
            "Implement `void program(void)` printing a left-aligned triangle of `*` with 4 rows:\n\n```\n*\n**\n***\n****\n```\n\nRows and inner counts computed by nested loops — no literal strings of stars.",
            C_PRELUDE,
            [
                ("exact triangle", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "*\\n**\\n***\\n****\\n");', "Inner loop bound depends on the row."),
            ],
            level="imitation",
        ),
        challenge(
            "cb6-times-table",
            "Times Table",
            "Implement `void program(void)` printing the 1..3 x 1..3 multiplication grid, one row per line, numbers separated by single spaces (no trailing space):\n\n```\n1 2 3\n2 4 6\n3 6 9\n```\n\nCompute every cell; print the separator logic explicitly.",
            C_PRELUDE,
            [
                ("exact grid", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "1 2 3\\n2 4 6\\n3 6 9\\n");', "Print `col == 3 ? \"%d\" : \"%d \"` or guard the space."),
            ],
            level="guided",
        ),
        challenge(
            "cb6-fizzbuzz-limited",
            "FizzBuzz (7..15)",
            "Implement `void program(void)` printing numbers 7..15 one per line, but `fizz` for multiples of 3, `buzz` for multiples of 5, `fizzbuzz` for both.",
            C_PRELUDE,
            [
                ("exact fizzbuzz window", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "7\\n8\\nfizz\\nbuzz\\n11\\nfizz\\n13\\n14\\nfizzbuzz\\n");', "Check the BOTH case first."),
            ],
            level="independent",
        ),
    ],
    {
        "cb6-star-triangle": vi_challenge(
            "Tam giác sao",
            "Cài `void program(void)` in tam giác căn trái 4 hàng bằng vòng lặp lồng — không dùng chuỗi sao cố định.",
            [("tam giác chính xác", "Biên vòng trong phụ thuộc hàng.")],
        ),
        "cb6-times-table": vi_challenge(
            "Bảng cửu chương",
            "Cài `void program(void)` in lưới nhân 1..3 x 1..3, mỗi hàng một dòng, các số cách nhau một dấu cách (không dấu cách thừa).",
            [("lưới chính xác", "In `%d` với điều kiện thêm dấu cách, hoặc chặn dấu cách cuối.")],
        ),
        "cb6-fizzbuzz-limited": vi_challenge(
            "FizzBuzz (7..15)",
            "Cài `void program(void)` in các số 7..15 mỗi số một dòng, nhưng `fizz` cho bội của 3, `buzz` cho bội của 5, `fizzbuzz` cho cả hai.",
            [("cửa sổ fizzbuzz chính xác", "Kiểm tra trường CẢ HAI trước.")],
        ),
    },
    solutions=[
        (
            "cb6-star-triangle",
            '#include <stdio.h>\nvoid program(void) {\n    for (int row = 1; row <= 4; row++) {\n        for (int col = 0; col < row; col++) printf("*");\n        printf("\\n");\n    }\n}\nint main(void) { program(); return 0; }',
            '#include <stdio.h>\nvoid program(void) {\n    for (int row = 1; row <= 4; row++) {\n        for (int col = 0; col <= row; col++) printf("*");\n        printf("\\n");\n    }\n}\nint main(void) { program(); return 0; }',
        ),
        (
            "cb6-times-table",
            '#include <stdio.h>\nvoid program(void) {\n    for (int row = 1; row <= 3; row++) {\n        for (int col = 1; col <= 3; col++) {\n            printf("%d", row * col);\n            if (col < 3) printf(" ");\n        }\n        printf("\\n");\n    }\n}\nint main(void) { program(); return 0; }',
            '#include <stdio.h>\nvoid program(void) {\n    for (int row = 1; row <= 3; row++) {\n        for (int col = 1; col <= 3; col++) {\n            printf("%d ", row * col);\n        }\n        printf("\\n");\n    }\n}\nint main(void) { program(); return 0; }',
        ),
        (
            "cb6-fizzbuzz-limited",
            '#include <stdio.h>\nvoid program(void) {\n    for (int n = 7; n <= 15; n++) {\n        if (n % 15 == 0) printf("fizzbuzz\\n");\n        else if (n % 3 == 0) printf("fizz\\n");\n        else if (n % 5 == 0) printf("buzz\\n");\n        else printf("%d\\n", n);\n    }\n}\nint main(void) { program(); return 0; }',
            '#include <stdio.h>\nvoid program(void) {\n    for (int n = 7; n <= 15; n++) {\n        if (n % 3 == 0) printf("fizz\\n");\n        else if (n % 5 == 0) printf("buzz\\n");\n        else printf("%d\\n", n);\n    }\n}\nint main(void) { program(); return 0; }',
        ),
    ],
)

write_checkpoint(
    M6,
    L6D,
    "Checkpoint: Loops",
    "A digit machine: exact output computed by loops, with break/continue semantics.",
    16,
    r"""
## Checkpoint

Loops under integration pressure: exact multi-line output, a counting loop
with skip rules, and a digit-machine fold.
""",
    "Điểm kiểm tra: Vòng Lặp",
    "Vòng lặp dưới áp lực tích hợp: đầu ra nhiều dòng chính xác, vòng đếm có luật bỏ qua, và gập máy chữ số.",

    r"""
## Điểm kiểm tra

Vòng lặp dưới áp lực tích hợp: đầu ra nhiều dòng chính xác, vòng đếm có luật
bỏ qua, và gập máy chữ số.
""",
    challenge(
        "cb6-checkpoint-primes",
        "Prime Counter",
        "Implement `int count_primes(int limit)` counting primes in [2, limit] (inclusive) using loops only. Also implement `void program(void)` printing exactly:\n\n```\nprimes under 10: 4\n2 3 5 7\n```\n\nLine 2 lists the primes 2..7 space-separated (single spaces, no trailing space).",
        C_PRELUDE,
        [
            ("count is right", "CHECK_EQ(count_primes(10), 4);\nCHECK_EQ(count_primes(2), 1);\nCHECK_EQ(count_primes(1), 0);", "Trial division by every d from 2 while d*d <= n."),
            ("exact program output", 'const char* out = cj_capture(program);\nCHECK_STR_EQ(out, "primes under 10: 4\\n2 3 5 7\\n");', "Reuse count_primes and a listing loop; guard the separator."),
        ],
    ),
    vi_challenge(
        "Bộ đếm số nguyên tố",
        "Cài `int count_primes(int limit)` đếm số nguyên tố trong [2, limit] (bao hàm) chỉ dùng vòng lặp. Cài `void program(void)` in đúng hai dòng như đề bài.",
        [("đếm đúng", "Thử chia cho mọi d từ 2 trong khi d*d <= n."), ("đầu ra chính xác", "Tái dùng count_primes và một vòng liệt kê; chặn dấu cách cuối.")],
    ),
    solution='#include <stdio.h>\nstatic int is_prime(int n) {\n    if (n < 2) return 0;\n    for (int d = 2; d * d <= n; d++) {\n        if (n % d == 0) return 0;\n    }\n    return 1;\n}\nint count_primes(int limit) {\n    int c = 0;\n    for (int n = 2; n <= limit; n++) {\n        if (is_prime(n)) c++;\n    }\n    return c;\n}\nvoid program(void) {\n    printf("primes under 10: %d\\n", count_primes(10));\n    for (int n = 2; n <= 10; n++) {\n        if (is_prime(n)) {\n            printf("%d", n);\n            if (n < 7) printf(" ");\n        }\n    }\n    printf("\\n");\n}\nint main(void) { program(); return 0; }',
    wrong='#include <stdio.h>\nstatic int is_prime(int n) {\n    if (n < 2) return 0;\n    for (int d = 2; d * d <= n; d++) {\n        if (n % d == 0) return 0;\n    }\n    return 1;\n}\nint count_primes(int limit) {\n    int c = 0;\n    for (int n = 2; n < limit; n++) {\n        if (is_prime(n)) c++;\n    }\n    return c;\n}\nvoid program(void) {\n    printf("primes under 10: %d\\n", count_primes(10));\n    for (int n = 2; n <= 10; n++) {\n        if (is_prime(n)) {\n            printf("%d", n);\n            if (n < 7) printf(" ");\n        }\n    }\n    printf("\\n");\n}\nint main(void) { program(); return 0; }',
)

print("batch 3 complete: modules 5-6")
