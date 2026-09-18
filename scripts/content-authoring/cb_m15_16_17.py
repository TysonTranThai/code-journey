#!/usr/bin/env python3
"""C Beginner — batch 8: modules 15 (enums-typedef), 16 (file-io), 17 (preprocessor)."""
from cb import (
    C_PRELUDE,
    challenge,
    vi_challenge,
    write_checkpoint,
    write_lesson,
    write_module,
    write_practice,
)

# ========================= MODULE 15: enums-typedef =========================
M15 = "enums-typedef"

L15A = "enums-basics"
L15B = "typedef-aliases"
L15C = "modeling-state"
L15D = "cb-checkpoint-m15"

write_module(
    M15,
    "Enums, Typedef & Data Modeling",
    "Named constants, type aliases, and modeling real-world state readably.",
    "Enum, Typedef & Mô hình dữ liệu",
    "Hằng số có tên, bí danh kiểu, và mô hình hóa trạng thái thực tế một cách dễ đọc.",
    [L15A, L15B, L15C, L15D],
    ["cb-p15-enum", "cb-p15-model"],
)

write_lesson(
    M15,
    L15A,
    "Enum Basics",
    "An enum is a type whose values are named integer constants.",
    12,
    r"""
## Declaring and using

```c
enum Color { RED, GREEN, BLUE };

enum Color c = GREEN;
```

The compiler assigns values starting at 0: RED=0, GREEN=1, BLUE=2. You can
pin or offset values:

```c
enum Level { LOW = 1, MEDIUM, HIGH };   // 1, 2, 3
enum Mask  { BIT0 = 1, BIT2 = 4 };      // explicit
```

## Why not just ints?

Magic numbers (`if (s == 2)`) hide meaning; enum names carry it
(`if (s == STATE_PAUSED)`). The compiler also type-checks the intent, and
switch coverage warnings catch missing cases.

## Enums and switch

```c
enum Color invert(enum Color c) {
    switch (c) {
        case RED:   return BLUE;
        case BLUE:  return RED;
        case GREEN: return GREEN;
    }
    return c;   // defensive: reachable only on invalid input
}
```

Each `case` names a constant — no more guessing what 1 meant.
""",
    "Cơ bản về enum",
    "Enum là một kiểu mà các giá trị của nó là hằng số nguyên có tên.",
    r"""
## Khai báo và dùng

```c
enum Color { RED, GREEN, BLUE };

enum Color c = GREEN;
```

Trình biên dịch gán giá trị bắt đầu từ 0: RED=0, GREEN=1, BLUE=2. Bạn có thể
định hoặc dịch giá trị:

```c
enum Level { LOW = 1, MEDIUM, HIGH };   // 1, 2, 3
enum Mask  { BIT0 = 1, BIT2 = 4 };      // chỉ định rõ
```

## Tại sao không dùng int cho nhanh?

Số ma thuật (`if (s == 2)`) che giấu ý nghĩa; tên enum mang nó
(`if (s == STATE_PAUSED)`). Trình biên dịch còn kiểm tra kiểu theo ý định,
và cảnh báo bao phủ switch bắt được các case bị thiếu.

## Enum và switch

```c
enum Color invert(enum Color c) {
    switch (c) {
        case RED:   return BLUE;
        case BLUE:  return RED;
        case GREEN: return GREEN;
    }
    return c;   // phòng thủ: chỉ đến được khi đầu vào không hợp lệ
}
```

Mỗi `case` là một hằng số có tên — không còn phải đoán số 1 nghĩa là gì.
""",
)

write_lesson(
    M15,
    L15B,
    "Typedef Aliases",
    "typedef gives a type a shorter, intention-revealing name.",
    11,
    r"""
## The basic form

```c
typedef unsigned long ulong;    // 'ulong' now names unsigned long
typedef int Score;              // Score is int, with intent
```

`typedef` does not create a new type — it creates a new NAME for an existing
type. `Score` and `int` are interchangeable.

## The classic: typedef struct

```c
typedef struct {
    int x;
    int y;
} Point;                 // now 'Point', not 'struct Point'

Point p = {1, 2};        // no struct keyword needed
```

Or naming a tagged struct so it can self-reference:

```c
typedef struct Node Node;
struct Node {
    int value;
    Node *next;          // self-reference needs the tag
};
```

You will build this Node in module 20.

## When to alias

- burying `unsigned long long` behind `u64`
- `typedef struct {...} Config;` — the dominant C idiom
- naming semantic roles: `typedef int UserId;`
""",
    "Bí danh Typedef",
    "typedef đặt cho một kiểu cái tên ngắn hơn, thể hiện đúng ý đồ.",
    r"""
## Dạng cơ bản

```c
typedef unsigned long ulong;    // 'ulong' giờ là tên của unsigned long
typedef int Score;              // Score là int, nhưng có ý đồ
```

`typedef` không tạo kiểu mới — nó tạo TÊN MỚI cho kiểu có sẵn. `Score` và
`int` thay thế cho nhau được.

## Kinh điển: typedef struct

```c
typedef struct {
    int x;
    int y;
} Point;                 // giờ là 'Point', không phải 'struct Point'

Point p = {1, 2};        // không cần từ khóa struct
```

Hoặc đặt tên cho struct có tag để nó tự tham chiếu:

```c
typedef struct Node Node;
struct Node {
    int value;
    Node *next;          // tự tham chiếu cần tag
};
```

Bạn sẽ dựng Node này ở module 20.

## Khi nào nên tạo bí danh

- che `unsigned long long` đằng sau `u64`
- `typedef struct {...} Config;` — thành ngữ C phổ biến nhất
- đặt tên cho vai trò ngữ nghĩa: `typedef int UserId;`
""",
)

write_lesson(
    M15,
    L15C,
    "Modeling State",
    "Enums + structs + functions = small, readable state machines.",
    14,
    r"""
## A tiny state machine

```c
typedef enum { IDLE, RUNNING, PAUSED } State;

State step(State s, int event) {
    switch (s) {
        case IDLE:    return event == 1 ? RUNNING : IDLE;
        case RUNNING: return event == 0 ? PAUSED  : RUNNING;
        case PAUSED:  return event == 1 ? RUNNING : PAUSED;
    }
    return s;
}
```

The enum names the states, the function names the transition rules, and the
types make illegal states obvious.

## Modeling records

```c
typedef enum { DOC, VIDEO, QUIZ } Kind;

typedef struct {
    int id;
    Kind kind;
    int minutes;
} Material;

int total_minutes(const Material *ms, int n, Kind k) {
    int t = 0;
    for (int i = 0; i < n; i++)
        if (ms[i].kind == k) t += ms[i].minutes;
    return t;
}
```

This is the data-modeling layer of every C program: an enum for categories, a
struct for records, functions that query and update them.

## Design hint

When you catch yourself writing `status == 3`, stop and invent the enum.
The rename costs two minutes and pays off for the life of the code.
""",
    "Mô hình hóa trạng thái",
    "Enum + struct + hàm = máy trạng thái nhỏ, dễ đọc.",
    r"""
## Một máy trạng thái tí hon

```c
typedef enum { IDLE, RUNNING, PAUSED } State;

State step(State s, int event) {
    switch (s) {
        case IDLE:    return event == 1 ? RUNNING : IDLE;
        case RUNNING: return event == 0 ? PAUSED  : RUNNING;
        case PAUSED:  return event == 1 ? RUNNING : PAUSED;
    }
    return s;
}
```

Enum đặt tên cho các trạng thái, hàm đặt tên cho luật chuyển, và hệ thống kiểu
khiến các trạng thái bất hợp lệ trở nên rõ ràng.

## Mô hình hóa bản ghi

```c
typedef enum { DOC, VIDEO, QUIZ } Kind;

typedef struct {
    int id;
    Kind kind;
    int minutes;
} Material;

int total_minutes(const Material *ms, int n, Kind k) {
    int t = 0;
    for (int i = 0; i < n; i++)
        if (ms[i].kind == k) t += ms[i].minutes;
    return t;
}
```

Đây chính là tầng mô hình dữ liệu của mọi chương trình C: một enum cho danh
mục, một struct cho bản ghi, và các hàm truy vấn/cập nhật chúng.

## Gợi ý thiết kế

Khi bắt gặp chính mình viết `status == 3`, hãy dừng lại và đặt tên enum cho nó.
Việc đổi tên tốn hai phút và trả lãi suốt vòng đời của mã nguồn.
""",
)

write_practice(
    M15,
    "cb-p15-enum",
    "Enum Practice",
    "State transitions and category queries built on enums.",
    "Luyện tập enum",
    "Chuyển đổi trạng thái và truy vấn danh mục dựa trên enum.",
    L15A,
    14,
    "beginner",
    [
        challenge(
            "cb15-next-light",
            "Traffic Light Cycle",
            "Given `typedef enum { RED, YELLOW, GREEN } Light;` in scope, implement `Light next_light(Light l)` cycling RED -> GREEN -> YELLOW -> RED.",
            C_PRELUDE + "typedef enum { RED, YELLOW, GREEN } Light;\n",
            [
                ("red to green", "CHECK_EQ(next_light(RED), GREEN);", "Follow the cycle order."),
                ("green to yellow", "CHECK_EQ(next_light(GREEN), YELLOW);", "Green gives way to yellow."),
                ("yellow to red", "CHECK_EQ(next_light(YELLOW), RED);", "And back to red."),
            ],
            level="imitation",
        ),
        challenge(
            "cb15-weekend",
            "Weekend Check",
            "Given `typedef enum { MON, TUE, WED, THU, FRI, SAT, SUN } Day;` in scope, implement `int is_weekend(Day d)` returning 1 for SAT or SUN, else 0.",
            C_PRELUDE + "typedef enum { MON, TUE, WED, THU, FRI, SAT, SUN } Day;\n",
            [
                ("saturday", "CHECK_EQ(is_weekend(SAT), 1);", "SAT counts."),
                ("sunday", "CHECK_EQ(is_weekend(SUN), 1);", "SUN counts."),
                ("weekday", "CHECK_EQ(is_weekend(WED), 0);", "Midweek does not."),
                ("friday", "CHECK_EQ(is_weekend(FRI), 0);", "Friday is still a workday."),
            ],
            level="imitation",
        ),
        challenge(
            "cb15-step-machine",
            "State Machine Step",
            "Given `typedef enum { IDLE, RUNNING, PAUSED } State;` in scope, implement `State step(State s, int event)`: from IDLE event 1 goes RUNNING; from RUNNING event 0 goes PAUSED; from PAUSED event 1 goes RUNNING; anything else stays.",
            C_PRELUDE + "typedef enum { IDLE, RUNNING, PAUSED } State;\n",
            [
                ("start", "CHECK_EQ(step(IDLE, 1), RUNNING);", "Event 1 starts the machine."),
                ("pause", "CHECK_EQ(step(RUNNING, 0), PAUSED);", "Event 0 pauses."),
                ("resume", "CHECK_EQ(step(PAUSED, 1), RUNNING);", "Event 1 resumes."),
                ("stay idle", "CHECK_EQ(step(IDLE, 0), IDLE);", "No start event: stay."),
                ("stay paused", "CHECK_EQ(step(PAUSED, 0), PAUSED);", "Pause again changes nothing."),
            ],
            level="guided",
        ),
        challenge(
            "cb15-count-kind",
            "Count by Kind",
            "Given the Material model in scope, implement `int count_kind(const Material *ms, int n, Kind k)` returning how many records have kind k.",
            C_PRELUDE + "typedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\n",
            [
                ("mixed", "Material ms[] = {{1, DOC, 5}, {2, VIDEO, 7}, {3, DOC, 2}};\nCHECK_EQ(count_kind(ms, 3, DOC), 2);", "Compare ms[i].kind."),
                ("none", "Material ms[] = {{1, QUIZ, 4}};\nCHECK_EQ(count_kind(ms, 1, VIDEO), 0);", "Absent kind counts 0."),
                ("empty", "Material ms[1];\nCHECK_EQ(count_kind(ms, 0, DOC), 0);", "n=0 gives 0."),
            ],
            level="independent",
        ),
    ],
    {
        "cb15-next-light": vi_challenge(
            "Vòng đèn giao thông",
            "Với `typedef enum { RED, YELLOW, GREEN } Light;` có sẵn, cài `Light next_light(Light l)` theo chu kỳ RED -> GREEN -> YELLOW -> RED.",
            [("đỏ sang xanh", "Theo đúng thứ tự vòng."), ("xanh sang vàng", "Xanh nhường vàng."), ("vàng sang đỏ", "Rồi quay về đỏ.")],
        ),
        "cb15-weekend": vi_challenge(
            "Kiểm tra cuối tuần",
            "Với `typedef enum { MON, TUE, WED, THU, FRI, SAT, SUN } Day;` có sẵn, cài `int is_weekend(Day d)` trả 1 cho SAT hoặc SUN, ngược lại 0.",
            [("thứ bảy", "SAT được tính."), ("chủ nhật", "SUN được tính."), ("ngày thường", "Giữa tuần không tính."), ("thứ sáu", "Thứ sáu vẫn là ngày làm việc.")],
        ),
        "cb15-step-machine": vi_challenge(
            "Bước máy trạng thái",
            "Với `typedef enum { IDLE, RUNNING, PAUSED } State;` có sẵn, cài `State step(State s, int event)`: từ IDLE sự kiện 1 sang RUNNING; từ RUNNING sự kiện 0 sang PAUSED; từ PAUSED sự kiện 1 sang RUNNING; còn lại giữ nguyên.",
            [("khởi động", "Sự kiện 1 khởi động máy."), ("tạm dừng", "Sự kiện 0 tạm dừng."), ("chạy tiếp", "Sự kiện 1 chạy tiếp."), ("vẫn IDLE", "Không có sự kiện khởi động: giữ nguyên."), ("vẫn PAUSED", "Tạm dừng thêm lần nữa chẳng đổi gì.")],
        ),
        "cb15-count-kind": vi_challenge(
            "Đếm theo loại",
            "Với mô hình Material có sẵn, cài `int count_kind(const Material *ms, int n, Kind k)` trả về số bản ghi có loại k.",
            [("hỗn hợp", "So sánh ms[i].kind."), ("không có", "Loại vắng mặt đếm là 0."), ("rỗng", "n=0 cho ra 0.")],
        ),
    },
    solutions=[
        (
            "cb15-next-light",
            '#include <stdio.h>\ntypedef enum { RED, YELLOW, GREEN } Light;\nLight next_light(Light l) {\n    switch (l) {\n        case RED: return GREEN;\n        case GREEN: return YELLOW;\n        case YELLOW: return RED;\n    }\n    return l;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef enum { RED, YELLOW, GREEN } Light;\nLight next_light(Light l) {\n    switch (l) {\n        case RED: return YELLOW;\n        case GREEN: return YELLOW;\n        case YELLOW: return RED;\n    }\n    return l;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb15-weekend",
            '#include <stdio.h>\ntypedef enum { MON, TUE, WED, THU, FRI, SAT, SUN } Day;\nint is_weekend(Day d) {\n    return d == SAT || d == SUN;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef enum { MON, TUE, WED, THU, FRI, SAT, SUN } Day;\nint is_weekend(Day d) {\n    return d == SAT || d == FRI;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb15-step-machine",
            '#include <stdio.h>\ntypedef enum { IDLE, RUNNING, PAUSED } State;\nState step(State s, int event) {\n    switch (s) {\n        case IDLE:    return event == 1 ? RUNNING : IDLE;\n        case RUNNING: return event == 0 ? PAUSED : RUNNING;\n        case PAUSED:  return event == 1 ? RUNNING : PAUSED;\n    }\n    return s;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef enum { IDLE, RUNNING, PAUSED } State;\nState step(State s, int event) {\n    switch (s) {\n        case IDLE:    return event == 1 ? RUNNING : IDLE;\n        case RUNNING: return event == 0 ? PAUSED : RUNNING;\n        case PAUSED:  return event == 1 ? PAUSED : PAUSED;\n    }\n    return s;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb15-count-kind",
            '#include <stdio.h>\ntypedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\nint count_kind(const Material *ms, int n, Kind k) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (ms[i].kind == k) c++;\n    return c;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\nint count_kind(const Material *ms, int n, Kind k) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (ms[i].kind == k) c += ms[i].minutes;\n    return c;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M15,
    "cb-p15-model",
    "Model Building",
    "typedef struct records with queries that mix enums and arithmetic.",
    "Dựng mô hình",
    "Bản ghi typedef struct với các truy vấn trộn enum và số học.",
    L15C,
    15,
    "beginner",
    [
        challenge(
            "cb15-total-minutes",
            "Minutes by Kind",
            "Given the Material model in scope, implement `int total_minutes(const Material *ms, int n, Kind k)` summing minutes of records with kind k.",
            C_PRELUDE + "typedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\n",
            [
                ("mixed", "Material ms[] = {{1, DOC, 5}, {2, VIDEO, 7}, {3, DOC, 2}};\nCHECK_EQ(total_minutes(ms, 3, DOC), 7);", "Filter first, then sum."),
                ("video only", "Material ms[] = {{1, VIDEO, 4}, {2, VIDEO, 6}};\nCHECK_EQ(total_minutes(ms, 2, VIDEO), 10);", "All match."),
                ("none match", "Material ms[] = {{1, QUIZ, 9}};\nCHECK_EQ(total_minutes(ms, 1, DOC), 0);", "No match: 0."),
            ],
            level="guided",
        ),
        challenge(
            "cb15-score-tier",
            "Score Tier",
            "Given `typedef enum { BRONZE, SILVER, GOLD } Tier;` in scope, implement `Tier tier_for(int score)`: >= 90 GOLD, >= 70 SILVER, else BRONZE.",
            C_PRELUDE + "typedef enum { BRONZE, SILVER, GOLD } Tier;\n",
            [
                ("gold", "CHECK_EQ(tier_for(95), GOLD);", "High scores are gold."),
                ("exact ninety", "CHECK_EQ(tier_for(90), GOLD);", "90 is gold: the cut is >="),
                ("silver boundary", "CHECK_EQ(tier_for(70), SILVER);", "Exactly 70 is silver."),
                ("bronze", "CHECK_EQ(tier_for(69), BRONZE);", "Below 70 is bronze."),
                ("zero", "CHECK_EQ(tier_for(0), BRONZE);", "Zero is bronze."),
            ],
            level="imitation",
        ),
        challenge(
            "cb15-longest-video",
            "Longest Video",
            "Given the Material model in scope, implement `const Material* longest_video(const Material *ms, int n)` returning the VIDEO record with the most minutes, or NULL when there are none.",
            C_PRELUDE + "typedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\n",
            [
                ("winner", "Material ms[] = {{1, VIDEO, 4}, {2, DOC, 9}, {3, VIDEO, 8}};\nCHECK_EQ(longest_video(ms, 3), &ms[2]);", "Skip non-videos; track the max."),
                ("no videos", "Material ms[] = {{1, DOC, 9}};\nCHECK_EQ(longest_video(ms, 1), NULL);", "No candidates: NULL."),
                ("single", "Material ms[] = {{5, VIDEO, 2}};\nCHECK_EQ(longest_video(ms, 1), &ms[0]);", "One video wins by default."),
            ],
            level="independent",
        ),
    ],
    {
        "cb15-total-minutes": vi_challenge(
            "Số phút theo loại",
            "Với mô hình Material có sẵn, cài `int total_minutes(const Material *ms, int n, Kind k)` cộng phút của các bản ghi có loại k.",
            [("hỗn hợp", "Lọc trước, rồi cộng."), ("chỉ video", "Tất cả khớp."), ("không khớp", "Không khớp: 0.")],
        ),
        "cb15-score-tier": vi_challenge(
            "Bậc điểm số",
            "Với `typedef enum { BRONZE, SILVER, GOLD } Tier;` có sẵn, cài `Tier tier_for(int score)`: >= 90 GOLD, >= 70 SILVER, còn lại BRONZE.",
            [("gold", "Điểm cao là gold."), ("đúng chín mươi", "90 là gold: mốc là >="), ("biên silver", "Đúng 70 là silver."), ("bronze", "Dưới 70 là bronze."), ("số 0", "0 là bronze.")],
        ),
        "cb15-longest-video": vi_challenge(
            "Video dài nhất",
            "Với mô hình Material có sẵn, cài `const Material* longest_video(const Material *ms, int n)` trả bản ghi VIDEO có nhiều phút nhất, hoặc NULL khi không có.",
            [("người thắng", "Bỏ qua loại khác; theo dõi max."), ("không có video", "Không ứng viên: NULL."), ("một bản", "Một video mặc định thắng.")],
        ),
    },
    solutions=[
        (
            "cb15-total-minutes",
            '#include <stdio.h>\ntypedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\nint total_minutes(const Material *ms, int n, Kind k) {\n    int t = 0;\n    for (int i = 0; i < n; i++)\n        if (ms[i].kind == k) t += ms[i].minutes;\n    return t;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\nint total_minutes(const Material *ms, int n, Kind k) {\n    int t = 0;\n    for (int i = 0; i < n; i++)\n        if (ms[i].kind == k) t += ms[i].id;\n    return t;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb15-score-tier",
            '#include <stdio.h>\ntypedef enum { BRONZE, SILVER, GOLD } Tier;\nTier tier_for(int score) {\n    if (score >= 90) return GOLD;\n    if (score >= 70) return SILVER;\n    return BRONZE;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef enum { BRONZE, SILVER, GOLD } Tier;\nTier tier_for(int score) {\n    if (score > 90) return GOLD;\n    if (score >= 70) return SILVER;\n    return BRONZE;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb15-longest-video",
            '#include <stdio.h>\ntypedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\nconst Material* longest_video(const Material *ms, int n) {\n    const Material *best = NULL;\n    for (int i = 0; i < n; i++)\n        if (ms[i].kind == VIDEO && (best == NULL || ms[i].minutes > best->minutes))\n            best = &ms[i];\n    return best;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\ntypedef enum { DOC, VIDEO, QUIZ } Kind;\ntypedef struct { int id; Kind kind; int minutes; } Material;\nconst Material* longest_video(const Material *ms, int n) {\n    const Material *best = NULL;\n    for (int i = 0; i < n; i++)\n        if (ms[i].kind == DOC && (best == NULL || ms[i].minutes > best->minutes))\n            best = &ms[i];\n    return best;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M15,
    L15D,
    "Checkpoint: Enums & Models",
    "An order-status model with transitions and aggregate queries.",
    15,
    r"""
## Checkpoint

Enums for categories, structs for records, functions for rules — the modeling
trinity.
""",
    "Điểm kiểm tra: Enum & mô hình",
    "Enum cho danh mục, struct cho bản ghi, hàm cho luật — bộ ba mô hình hóa.",
    r"""
## Điểm kiểm tra

Enum cho danh mục, struct cho bản ghi, hàm cho luật — bộ ba mô hình hóa.
""",
    challenge(
        "cb15-checkpoint-orders",
        "Order Pipeline",
        "Given the Order model in scope, implement `Order next_status(Order o)` advancing PENDING -> SHIPPED -> DELIVERED (DELIVERED stays), `int count_status(const Order *os, int n, Order s)` counting matches, and `int shipped_revenue(const Order *os, int n)` summing total_cents of SHIPPED orders.",
        C_PRELUDE + "typedef enum { PENDING, SHIPPED, DELIVERED } Order;\ntypedef struct { int id; Order status; int total_cents; } OrderRec;\n",
        [
            ("advance", "CHECK_EQ(next_status(PENDING), SHIPPED);\nCHECK_EQ(next_status(SHIPPED), DELIVERED);", "One step per call."),
            ("delivered stays", "CHECK_EQ(next_status(DELIVERED), DELIVERED);", "Terminal state is stable."),
            ("count", "OrderRec os[] = {{1, PENDING, 100}, {2, SHIPPED, 200}, {3, PENDING, 300}};\nCHECK_EQ(count_status(os, 3, PENDING), 2);", "Compare os[i].status."),
            ("revenue", "OrderRec os[] = {{1, SHIPPED, 100}, {2, DELIVERED, 400}, {3, SHIPPED, 50}};\nCHECK_EQ(shipped_revenue(os, 3), 150);", "Only SHIPPED counts."),
        ],
    ),
    vi_challenge(
        "Đường ống đơn hàng",
        "Với mô hình Order có sẵn, cài `Order next_status(Order o)` chuyển PENDING -> SHIPPED -> DELIVERED (DELIVERED giữ nguyên), `int count_status(const Order *os, int n, Order s)` đếm số khớp, và `int shipped_revenue(const Order *os, int n)` cộng total_cents của các đơn SHIPPED.",
        [("chuyển trạng thái", "Mỗi lần gọi đi một bước."), ("delivered ổn định", "Trạng thái kết thúc là ổn định."), ("đếm", "So sánh os[i].status."), ("doanh thu", "Chỉ SHIPPED được tính.")],
    ),
    solution='#include <stdio.h>\ntypedef enum { PENDING, SHIPPED, DELIVERED } Order;\ntypedef struct { int id; Order status; int total_cents; } OrderRec;\nOrder next_status(Order o) {\n    switch (o) {\n        case PENDING: return SHIPPED;\n        case SHIPPED: return DELIVERED;\n        default: return DELIVERED;\n    }\n}\nint count_status(const OrderRec *os, int n, Order s) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (os[i].status == s) c++;\n    return c;\n}\nint shipped_revenue(const OrderRec *os, int n) {\n    int t = 0;\n    for (int i = 0; i < n; i++)\n        if (os[i].status == SHIPPED) t += os[i].total_cents;\n    return t;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\ntypedef enum { PENDING, SHIPPED, DELIVERED } Order;\ntypedef struct { int id; Order status; int total_cents; } OrderRec;\nOrder next_status(Order o) {\n    switch (o) {\n        case PENDING: return SHIPPED;\n        case SHIPPED: return DELIVERED;\n        default: return DELIVERED;\n    }\n}\nint count_status(const OrderRec *os, int n, Order s) {\n    int c = 0;\n    for (int i = 0; i < n; i++)\n        if (os[i].status == s) c++;\n    return c;\n}\nint shipped_revenue(const OrderRec *os, int n) {\n    int t = 0;\n    for (int i = 0; i < n; i++)\n        t += os[i].total_cents;\n    return t;\n}\nint main(void) { return 0; }',
)

# ============================ MODULE 16: file-io ============================
M16 = "file-io"

L16A = "files-and-streams"
L16B = "read-write-files"
L16C = "cb-checkpoint-m16"

write_module(
    M16,
    "File I/O",
    "FILE*, open modes, reading and writing text, and handling the failure cases.",
    "Nhập xuất tệp",
    "FILE*, các chế độ mở, đọc ghi văn bản, và xử lý các trường hợp thất bại.",
    [L16A, L16B, L16C],
    ["cb-p16-fileio", "cb-p16-persist"],
)

write_lesson(
    M16,
    L16A,
    "Files and Streams",
    "A FILE* is a handle to an open stream; modes decide read, write, or append.",
    13,
    r"""
## Opening and closing

```c
#include <stdio.h>

FILE *f = fopen("notes.txt", "r");   // mode: how you intend to use it
if (f == NULL) {
    perror("notes.txt");             // WHY it failed, on stderr
    return 1;
}
// ... use f ...
fclose(f);                           // every open gets a close
```

`fopen` returns NULL on failure — missing file, no permission, bad path.
Unconditionally assuming success is a beginner signature move; check it.

## The modes that matter now

| mode | meaning | if file exists | if missing |
|------|---------|----------------|------------|
| "r"  | read    | reads from start | NULL |
| "w"  | write   | TRUNCATED to empty | created |
| "a"  | append  | writes at end | created |

"w" destroys existing content the moment you open it. "a" preserves it.

## Streams you already use

`stdout` and `stderr` are FILE* too. `printf(...)` is `fprintf(stdout, ...)`.
That is why the same fprintf/fgets family works everywhere.
""",
    "Tệp và luồng",
    "FILE* là tay cầm của một luồng đang mở; chế độ quyết định đọc, ghi, hay nối thêm.",
    r"""
## Mở và đóng

```c
#include <stdio.h>

FILE *f = fopen("notes.txt", "r");   // chế độ: bạn định dùng thế nào
if (f == NULL) {
    perror("notes.txt");             // TẠI SAO thất bại, ra stderr
    return 1;
}
// ... dùng f ...
fclose(f);                           // mỗi lần mở ứng một lần đóng
```

`fopen` trả NULL khi thất bại — thiếu tệp, không quyền, đường dẫn sai. Giả
định thành công vô điều kiện là dấu hiệu của người mới; hãy kiểm tra.

## Các chế độ quan trọng lúc này

| chế độ | nghĩa | nếu tệp đã có | nếu thiếu |
|--------|-------|----------------|------------|
| "r"  | đọc    | đọc từ đầu | NULL |
| "w"  | ghi    | BỊ CẮT RỖNG | tạo mới |
| "a"  | nối    | ghi vào cuối | tạo mới |

"w" phá hủy nội dung cũ ngay khi mở. "a" giữ nguyên nó.

## Những luồng bạn đã dùng

`stdout` và `stderr` cũng là FILE*. `printf(...)` là
`fprintf(stdout, ...)`. Vì thế họ fprintf/ffgets dùng được ở khắp nơi.
""",
)

write_lesson(
    M16,
    L16B,
    "Reading and Writing Files",
    "fgets/fputs for lines, fprintf/fscanf for formatted data, feof/EOF for the end.",
    14,
    r"""
## Writing text

```c
FILE *f = fopen("log.txt", "w");
if (f == NULL) return 1;
fprintf(f, "score=%d\n", 42);
fputs("plain line\n", f);
fclose(f);
```

## Reading line by line

```c
char line[128];
FILE *f = fopen("log.txt", "r");
if (f == NULL) return 1;
while (fgets(line, sizeof line, f) != NULL) {
    // line includes the trailing '\n' (when it fits)
    fputs(line, stdout);
}
fclose(f);
```

`fgets` returns NULL at end-of-file or error — that is the loop condition.
The buffer size is respected: no overflow.

## Parsing what you read

```c
int score;
if (sscanf(line, "score=%d", &score) == 1) {
    // matched exactly one conversion
}
```

Check sscanf's return value — it counts successful conversions.

## The EOF family

- `fgets` returning NULL: the line loop's end signal
- `feof(f)`: true AFTER a read hit end-of-file — never loop on feof alone
- `ferror(f)`: true if an I/O error occurred

## The pattern for persistence

write → fclose → fopen("r") → read → fclose. Closing on write flushes the
data; reopening for read sees it. You will use exactly this in the practice:
write a small log, then read it back and count.
""",
    "Đọc ghi tệp",
    "fgets/fputs cho từng dòng, fprintf/fscanf cho dữ liệu định dạng, feof/EOF cho điểm kết thúc.",
    r"""
## Ghi văn bản

```c
FILE *f = fopen("log.txt", "w");
if (f == NULL) return 1;
fprintf(f, "score=%d\n", 42);
fputs("plain line\n", f);
fclose(f);
```

## Đọc từng dòng

```c
char line[128];
FILE *f = fopen("log.txt", "r");
if (f == NULL) return 1;
while (fgets(line, sizeof line, f) != NULL) {
    // line có cả '\n' ở cuối (khi vừa đủ chỗ)
    fputs(line, stdout);
}
fclose(f);
```

`fgets` trả NULL khi hết tệp hoặc lỗi — đó là điều kiện của vòng lặp. Kích
thước bộ đệm được tôn trọng: không tràn.

## Phân tích cái bạn đọc

```c
int score;
if (sscanf(line, "score=%d", &score) == 1) {
    // khớp đúng một phép chuyển đổi
}
```

Hãy kiểm tra giá trị trả về của sscanf — nó đếm số chuyển đổi thành công.

## Gia đình EOF

- `fgets` trả NULL: tín hiệu kết thúc của vòng lặp dòng
- `feof(f)`: đúng SAU KHI một lần đọc chạm cuối tệp — đừng bao giờ lặp chỉ
  dựa trên feof
- `ferror(f)`: đúng nếu có lỗi I/O

## Mẫu cho việc lưu trữ

ghi → fclose → fopen("r") → đọc → fclose. Đóng lúc ghi đẩy dữ liệu xuống đĩa;
mở lại để đọc sẽ thấy nó. Bạn sẽ dùng đúng mẫu này trong phần luyện tập: ghi
một tệp nhỏ, rồi đọc lại và đếm.
""",
)

write_practice(
    M16,
    "cb-p16-fileio",
    "File Workbench",
    "Write, read back, append, and count — real files under /tmp.",
    "Bàn làm việc tệp",
    "Ghi, đọc lại, nối thêm, và đếm — tệp thật trong /tmp.",
    L16B,
    18,
    "beginner",
    [
        challenge(
            "cb16-count-lines",
            "Count Lines",
            "Implement `int count_lines(const char *path)` opening path for reading and returning the number of lines (a line ends at '\\n'; a trailing final line without '\\n' still counts; missing file returns -1).",
            C_PRELUDE,
            [
                ("three lines", "FILE *f = fopen(\"/tmp/cj16-a.txt\", \"w\");\nfputs(\"x\\ny\\nz\\n\", f);\nfclose(f);\nCHECK_EQ(count_lines(\"/tmp/cj16-a.txt\"), 3);\nremove(\"/tmp/cj16-a.txt\");", "One '\\n' per line."),
                ("no trailing newline", "FILE *f = fopen(\"/tmp/cj16-b.txt\", \"w\");\nfputs(\"x\\ny\", f);\nfclose(f);\nCHECK_EQ(count_lines(\"/tmp/cj16-b.txt\"), 2);\nremove(\"/tmp/cj16-b.txt\");", "The last partial line counts."),
                ("empty file", "FILE *f = fopen(\"/tmp/cj16-c.txt\", \"w\");\nfclose(f);\nCHECK_EQ(count_lines(\"/tmp/cj16-c.txt\"), 0);\nremove(\"/tmp/cj16-c.txt\");", "Zero bytes: zero lines."),
                ("missing file", "CHECK_EQ(count_lines(\"/tmp/cj16-nope.txt\"), -1);", "fopen NULL means -1."),
            ],
            level="guided",
        ),
        challenge(
            "cb16-write-read-back",
            "Write Then Read",
            "Implement `int echo_file(const char *path, const char *text)`: write text to path (mode \"w\"), then read the WHOLE file back and return the number of characters stored. Any open failure returns -1.",
            C_PRELUDE,
            [
                ("round trip", "CHECK_EQ(echo_file(\"/tmp/cj16-d.txt\", \"hello\"), 5);\nremove(\"/tmp/cj16-d.txt\");", "5 characters written and read."),
                ("with newline", "CHECK_EQ(echo_file(\"/tmp/cj16-e.txt\", \"a\\nb\\n\"), 4);\nremove(\"/tmp/cj16-e.txt\");", "Newlines are characters too."),
                ("empty text", "CHECK_EQ(echo_file(\"/tmp/cj16-f.txt\", \"\"), 0);\nremove(\"/tmp/cj16-f.txt\");", "Zero-length writes are legal."),
                ("content really written", "CHECK_EQ(echo_file(\"/tmp/cj16-g.txt\", \"hello\"), 5);\nFILE *f = fopen(\"/tmp/cj16-g.txt\", \"r\");\nchar buf[16] = {0};\nfgets(buf, 16, f);\nfclose(f);\nCHECK_STR_EQ(buf, \"hello\");\nremove(\"/tmp/cj16-g.txt\");", "The bytes must actually reach the disk."),
            ],
            level="independent",
        ),
        challenge(
            "cb16-append-log",
            "Append Log",
            "Implement `int append_line(const char *path, const char *line)`: append line + '\\n' to path (mode \"a\", creating it if needed) and return 0; return -1 on open failure. Two consecutive appends must BOTH survive.",
            C_PRELUDE,
            [
                ("two appends", "remove(\"/tmp/cj16-g.txt\");\nappend_line(\"/tmp/cj16-g.txt\", \"one\");\nappend_line(\"/tmp/cj16-g.txt\", \"two\");\nFILE *f = fopen(\"/tmp/cj16-g.txt\", \"r\");\nchar buf[64] = {0};\nfgets(buf, 64, f);\nCHECK_STR_EQ(buf, \"one\\n\");\nfgets(buf, 64, f);\nCHECK_STR_EQ(buf, \"two\\n\");\nfclose(f);\nremove(\"/tmp/cj16-g.txt\");", "\"a\" never truncates."),
                ("creates file", "remove(\"/tmp/cj16-h.txt\");\nCHECK_EQ(append_line(\"/tmp/cj16-h.txt\", \"seed\"), 0);\nremove(\"/tmp/cj16-h.txt\");", "Missing file is created."),
            ],
            level="independent",
        ),
    ],
    {
        "cb16-count-lines": vi_challenge(
            "Đếm dòng",
            "Cài `int count_lines(const char *path)` mở path để đọc và trả về số dòng (một dòng kết thúc tại '\\n'; dòng cuối không có '\\n' vẫn được tính; tệp thiếu trả -1).",
            [("ba dòng", "Mỗi '\\n' là một dòng."), ("không có xuống dòng cuối", "Dòng cụt cuối cùng vẫn được tính."), ("tệp rỗng", "Không byte nào: không dòng nào."), ("tệp thiếu", "fopen NULL nghĩa là -1.")],
        ),
        "cb16-write-read-back": vi_challenge(
            "Ghi rồi đọc",
            "Cài `int echo_file(const char *path, const char *text)`: ghi text vào path (chế độ \"w\"), rồi đọc lại TOÀN BỘ tệp và trả về số ký tự đã lưu. Mở thất bại trả -1.",
            [("vòng lặp trọn vẹn", "5 ký tự được ghi và đọc."), ("có xuống dòng", "Ký tự xuống dòng cũng là ký tự."), ("văn bản rỗng", "Ghi độ dài 0 là hợp lệ."), ("nội dung được ghi thật", "Các byte phải thực sự tới đĩa.")],
        ),
        "cb16-append-log": vi_challenge(
            "Nối vào nhật ký",
            "Cài `int append_line(const char *path, const char *line)`: nối line + '\\n' vào path (chế độ \"a\", tạo tệp nếu chưa có) và trả 0; mở thất bại trả -1. Hai lần nối liên tiếp phải CÙNG tồn tại.",
            [("hai lần nối", "\"a\" không bao giờ cắt nội dung cũ."), ("tự tạo tệp", "Tệp thiếu sẽ được tạo.")],
        ),
    },
    solutions=[
        (
            "cb16-count-lines",
            '#include <stdio.h>\nint count_lines(const char *path) {\n    FILE *f = fopen(path, "r");\n    if (f == NULL) return -1;\n    int n = 0, c, last = -1;\n    while ((c = fgetc(f)) != EOF) {\n        if (c == \'\\n\') n++;\n        last = c;\n    }\n    if (last != -1 && last != \'\\n\') n++;\n    fclose(f);\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint count_lines(const char *path) {\n    FILE *f = fopen(path, "r");\n    if (f == NULL) return -1;\n    int n = 0, c;\n    while ((c = fgetc(f)) != EOF)\n        if (c == \'\\n\') n++;\n    fclose(f);\n    return n;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb16-write-read-back",
            '#include <stdio.h>\n#include <string.h>\nint echo_file(const char *path, const char *text) {\n    FILE *f = fopen(path, "w");\n    if (f == NULL) return -1;\n    fputs(text, f);\n    fclose(f);\n    f = fopen(path, "r");\n    if (f == NULL) return -1;\n    int n = 0, c;\n    while ((c = fgetc(f)) != EOF) n++;\n    fclose(f);\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nint echo_file(const char *path, const char *text) {\n    FILE *f = fopen(path, "w");\n    if (f == NULL) return -1;\n    fclose(f);\n    return (int)strlen(text);\n}\nint main(void) { return 0; }',
        ),
        (
            "cb16-append-log",
            '#include <stdio.h>\nint append_line(const char *path, const char *line) {\n    FILE *f = fopen(path, "a");\n    if (f == NULL) return -1;\n    fputs(line, f);\n    fputc(\'\\n\', f);\n    fclose(f);\n    return 0;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint append_line(const char *path, const char *line) {\n    FILE *f = fopen(path, "w");\n    if (f == NULL) return -1;\n    fputs(line, f);\n    fputc(\'\\n\', f);\n    fclose(f);\n    return 0;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M16,
    "cb-p16-persist",
    "Persistence Layer",
    "Save records to a file and load them back — the seed of every stored-data app.",
    "Tầng lưu trữ",
    "Lưu bản ghi vào tệp rồi nạp lại — hạt mầm của mọi ứng dụng có dữ liệu lưu.",
    L16B,
    18,
    "beginner",
    [
        challenge(
            "cb16-save-scores",
            "Save Scores",
            "Implement `int save_scores(const char *path, const int *scores, int n)`: write one integer per line (fprintf \"%d\\n\") and return n. Open failure returns -1.",
            C_PRELUDE,
            [
                ("round trip", "int sc[] = {10, 20, 30};\nCHECK_EQ(save_scores(\"/tmp/cj16-s.txt\", sc, 3), 3);\nFILE *f = fopen(\"/tmp/cj16-s.txt\", \"r\");\nint a, b, c;\nfscanf(f, \"%d %d %d\", &a, &b, &c);\nfclose(f);\nCHECK_EQ(a, 10);\nCHECK_EQ(c, 30);\nremove(\"/tmp/cj16-s.txt\");", "One number per line."),
                ("empty", "CHECK_EQ(save_scores(\"/tmp/cj16-t.txt\", NULL, 0), 0);\nremove(\"/tmp/cj16-t.txt\");", "n=0 writes nothing."),
            ],
            level="guided",
        ),
        challenge(
            "cb16-load-sum",
            "Load and Sum",
            "Implement `int load_sum(const char *path)`: read integers (one per line, fscanf \"%d\") until reading fails, returning their sum; missing file returns -1.",
            C_PRELUDE,
            [
                ("sums file", "FILE *f = fopen(\"/tmp/cj16-u.txt\", \"w\");\nfprintf(f, \"5\\n10\\n15\\n\");\nfclose(f);\nCHECK_EQ(load_sum(\"/tmp/cj16-u.txt\"), 30);\nremove(\"/tmp/cj16-u.txt\");", "fscanf in a while loop."),
                ("empty file", "FILE *f = fopen(\"/tmp/cj16-v.txt\", \"w\");\nfclose(f);\nCHECK_EQ(load_sum(\"/tmp/cj16-v.txt\"), 0);\nremove(\"/tmp/cj16-v.txt\");", "No numbers: sum 0."),
                ("missing", "CHECK_EQ(load_sum(\"/tmp/cj16-nope2.txt\"), -1);", "No file: -1."),
            ],
            level="independent",
        ),
        challenge(
            "cb16-waiting-scan",
            "Bad Line Scanner",
            "Implement `int count_bad(const char *path)` counting lines that do NOT start with 'ok' (a line starting with \"ok\" is fine). Missing file returns -1.",
            C_PRELUDE,
            [
                ("mixed", "FILE *f = fopen(\"/tmp/cj16-w.txt\", \"w\");\nfputs(\"ok one\\nok two\\nBAD\\nok three\\n\", f);\nfclose(f);\nCHECK_EQ(count_bad(\"/tmp/cj16-w.txt\"), 1);\nremove(\"/tmp/cj16-w.txt\");", "fgets + strncmp(line, \"ok\", 2)."),
                ("all ok", "FILE *f = fopen(\"/tmp/cj16-x.txt\", \"w\");\nfputs(\"ok\\nok\\n\", f);\nfclose(f);\nCHECK_EQ(count_bad(\"/tmp/cj16-x.txt\"), 0);\nremove(\"/tmp/cj16-x.txt\");", "Zero bad lines."),
                ("missing", "CHECK_EQ(count_bad(\"/tmp/cj16-nope3.txt\"), -1);", "Same -1 contract."),
            ],
            level="independent",
        ),
    ],
    {
        "cb16-save-scores": vi_challenge(
            "Lưu điểm số",
            "Cài `int save_scores(const char *path, const int *scores, int n)`: ghi mỗi số một dòng (fprintf \"%d\\n\") và trả n. Mở thất bại trả -1.",
            [("vòng lặp trọn vẹn", "Mỗi dòng một số."), ("rỗng", "n=0 không ghi gì.")],
        ),
        "cb16-load-sum": vi_challenge(
            "Nạp và cộng",
            "Cài `int load_sum(const char *path)`: đọc các số nguyên (một số mỗi dòng, fscanf \"%d\") cho đến khi đọc thất bại, trả tổng; tệp thiếu trả -1.",
            [("cộng tệp", "fscanf trong vòng while."), ("tệp rỗng", "Không số nào: tổng 0."), ("tệp thiếu", "Không tệp: -1.")],
        ),
        "cb16-waiting-scan": vi_challenge(
            "Quét dòng xấu",
            "Cài `int count_bad(const char *path)` đếm các dòng KHÔNG bắt đầu bằng 'ok' (dòng bắt đầu bằng \"ok\" là ổn). Tệp thiếu trả -1.",
            [("hỗn hợp", "fgets + strncmp(line, \"ok\", 2)."), ("toàn ok", "Không dòng xấu nào."), ("tệp thiếu", "Cùng giao ước -1.")],
        ),
    },
    solutions=[
        (
            "cb16-save-scores",
            '#include <stdio.h>\nint save_scores(const char *path, const int *scores, int n) {\n    FILE *f = fopen(path, "w");\n    if (f == NULL) return -1;\n    for (int i = 0; i < n; i++) fprintf(f, "%d\\n", scores[i]);\n    fclose(f);\n    return n;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint save_scores(const char *path, const int *scores, int n) {\n    FILE *f = fopen(path, "w");\n    if (f == NULL) return -1;\n    for (int i = 1; i < n; i++) fprintf(f, "%d\\n", scores[i]);\n    fclose(f);\n    return n;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb16-load-sum",
            '#include <stdio.h>\nint load_sum(const char *path) {\n    FILE *f = fopen(path, "r");\n    if (f == NULL) return -1;\n    int v, sum = 0;\n    while (fscanf(f, "%d", &v) == 1) sum += v;\n    fclose(f);\n    return sum;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nint load_sum(const char *path) {\n    FILE *f = fopen(path, "r");\n    if (f == NULL) return -1;\n    int v, sum = 0;\n    while (fscanf(f, "%d", &v) == 1) sum = v;\n    fclose(f);\n    return sum;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb16-waiting-scan",
            '#include <stdio.h>\n#include <string.h>\nint count_bad(const char *path) {\n    FILE *f = fopen(path, "r");\n    if (f == NULL) return -1;\n    char line[256];\n    int bad = 0;\n    while (fgets(line, sizeof line, f) != NULL)\n        if (strncmp(line, "ok", 2) != 0) bad++;\n    fclose(f);\n    return bad;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#include <string.h>\nint count_bad(const char *path) {\n    FILE *f = fopen(path, "r");\n    if (f == NULL) return -1;\n    char line[256];\n    int bad = 0;\n    while (fgets(line, sizeof line, f) != NULL)\n        if (strncmp(line, "ok", 2) == 0) bad++;\n    fclose(f);\n    return bad;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M16,
    L16C,
    "Checkpoint: File I/O",
    "A deposit log: append entries, then audit the file.",
    16,
    r"""
## Checkpoint

Open, check, read/write, close — the four moves of every C file program.
""",
    "Điểm kiểm tra: Nhập xuất tệp",
    "Mở, kiểm tra, đọc/ghi, đóng — bốn động tác của mọi chương trình C có tệp.",
    r"""
## Điểm kiểm tra

Mở, kiểm tra, đọc/ghi, đóng — bốn động tác của mọi chương trình C có tệp.
""",
    challenge(
        "cb16-checkpoint-audit",
        "Deposit Log Audit",
        "Implement `int log_deposit(const char *path, int cents)` appending a line \"D <cents>\\n\" (mode \"a\"), and `int audit_total(const char *path)` reading all \"D <int>\" lines and returning the sum (other lines are ignored; missing file returns -1).",
        C_PRELUDE,
        [
            ("log then audit", "remove(\"/tmp/cj16-cap.txt\");\nlog_deposit(\"/tmp/cj16-cap.txt\", 100);\nlog_deposit(\"/tmp/cj16-cap.txt\", 250);\nCHECK_EQ(audit_total(\"/tmp/cj16-cap.txt\"), 350);\nremove(\"/tmp/cj16-cap.txt\");", "Append twice, sum once."),
            ("skips junk", "FILE *f = fopen(\"/tmp/cj16-cap2.txt\", \"w\");\nfputs(\"D 10\\nJUNK\\nD 5\\n\", f);\nfclose(f);\nCHECK_EQ(audit_total(\"/tmp/cj16-cap2.txt\"), 15);\nremove(\"/tmp/cj16-cap2.txt\");", "Only D lines count."),
            ("missing", "CHECK_EQ(audit_total(\"/tmp/cj16-nope4.txt\"), -1);", "The -1 contract again."),
        ],
    ),
    vi_challenge(
        "Kiểm toán sổ nạp tiền",
        "Cài `int log_deposit(const char *path, int cents)` nối một dòng \"D <cents>\\n\" (chế độ \"a\"), và `int audit_total(const char *path)` đọc mọi dòng \"D <int>\" rồi trả tổng (các dòng khác bị bỏ qua; tệp thiếu trả -1).",
        [("ghi rồi kiểm", "Nối hai lần, cộng một lần."), ("bỏ dòng rác", "Chỉ dòng D được tính."), ("tệp thiếu", "Giao ước -1 một lần nữa.")],
    ),
    solution='#include <stdio.h>\nint log_deposit(const char *path, int cents) {\n    FILE *f = fopen(path, "a");\n    if (f == NULL) return -1;\n    fprintf(f, "D %d\\n", cents);\n    fclose(f);\n    return 0;\n}\nint audit_total(const char *path) {\n    FILE *f = fopen(path, "r");\n    if (f == NULL) return -1;\n    char line[128];\n    int total = 0, v;\n    while (fgets(line, sizeof line, f) != NULL)\n        if (sscanf(line, "D %d", &v) == 1) total += v;\n    fclose(f);\n    return total;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\nint log_deposit(const char *path, int cents) {\n    FILE *f = fopen(path, "a");\n    if (f == NULL) return -1;\n    fprintf(f, "D %d\\n", cents);\n    fclose(f);\n    return 0;\n}\nint audit_total(const char *path) {\n    FILE *f = fopen(path, "r");\n    if (f == NULL) return -1;\n    char line[128];\n    int total = 0, v;\n    while (fgets(line, sizeof line, f) != NULL)\n        if (sscanf(line, "D %d", &v) == 1) total = v;\n    fclose(f);\n    return total;\n}\nint main(void) { return 0; }',
)

# ========================= MODULE 17: preprocessor =========================
M17 = "preprocessor"

L17A = "macros-basics"
L17B = "conditional-compilation"
L17C = "headers-why"
L17D = "cb-checkpoint-m17"

write_module(
    M17,
    "Preprocessor & Headers",
    "What happens before compilation: #include, #define, guards, and the .h/.c split.",
    "Bộ tiền xử lý & Header",
    "Điều gì xảy ra trước khi biên dịch: #include, #define, include guard, và tách .h/.c.",
    [L17A, L17B, L17C, L17D],
    ["cb-p17-macros", "cb-p17-organize"],
)

write_lesson(
    M17,
    L17A,
    "Macros and #define",
    "Text substitution with rules: object macros, function-like macros, and the parenthesis trap.",
    14,
    r"""
## Two kinds of macros

```c
#define MAX_SCORE 100                  // object macro: a named constant
#define SQUARE(x) ((x) * (x))          // function-like macro
```

The preprocessor replaces text BEFORE compilation. `SQUARE(a+b)` becomes
`((a+b) * (a+b))` — the compiler never sees the name SQUARE.

## The parenthesis trap

```c
#define BAD_SQUARE(x) (x * x)
BAD_SQUARE(2 + 3)     // becomes (2 + 3 * 2 + 3) = 11 — not 25!
```

Every parameter AND the whole expansion get parentheses. This is not style;
it is correctness.

## The double-evaluation trap

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
int i = 5;
MAX(i++, 3);    // i++ may be evaluated TWICE — side effects multiply
```

Macros paste text; arguments with side effects are dangerous. A do-while
wrapper gives statement-like macros sane semantics:

```c
#define LOG(msg) do { fprintf(stderr, "%s\n", msg); } while (0)
```

## #undef and scope

Macros live from their #define to the end of the file (or #undef). They do
not respect C scopes — a macro named SIZE will clobber any SIZE in every
header included after it. Name them deliberately (or not at all: a `const`
or `static const` is often the better tool).
""",
    "Macro và #define",
    "Thay thế văn bản với những quy tắc: macro đối tượng, macro kiểu hàm, và cái bẫy dấu ngoặc.",
    r"""
## Hai loại macro

```c
#define MAX_SCORE 100                  // macro đối tượng: hằng số có tên
#define SQUARE(x) ((x) * (x))          // macro kiểu hàm
```

Bộ tiền xử lý thay thế văn bản TRƯỚC khi biên dịch. `SQUARE(a+b)` trở thành
`((a+b) * (a+b))` — trình biên dịch không bao giờ thấy tên SQUARE.

## Cái bẫy dấu ngoặc

```c
#define BAD_SQUARE(x) (x * x)
BAD_SQUARE(2 + 3)     // trở thành (2 + 3 * 2 + 3) = 11 — chứ không phải 25!
```

Mỗi tham số VÀ toàn bộ biểu thức mở rộng đều cần ngoặc. Đây không phải chuyện
phong cách; đó là tính đúng đắn.

## Cái bẫy đánh giá hai lần

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
int i = 5;
MAX(i++, 3);    // i++ có thể bị đánh giá HAI LẦN — tác dụng phụ nhân đôi
```

Macro dán văn bản; đối số có tác dụng side-effect rất nguy hiểm. Bao bọc
do-while cho macro kiểu câu lệnh một ngữ nghĩa lành lành:

```c
#define LOG(msg) do { fprintf(stderr, "%s\n", msg); } while (0)
```

## #undef và phạm vi

Macro sống từ #define đến cuối tệp (hoặc #undef). Chúng không tôn trọng phạm
vi của C — một macro tên SIZE sẽ đè mọi SIZE trong mọi header được include
sau nó. Hãy đặt tên có chủ đích (hoặc đừng dùng macro: `const` hoặc
`static const` thường là công cụ tốt hơn).
""",
)

write_lesson(
    M17,
    L17B,
    "Conditional Compilation",
    "#if, #ifdef, and the include guard that stops double definitions.",
    12,
    r"""
## The include guard

Every header wears this armor:

```c
#ifndef GEOM_H
#define GEOM_H

/* declarations live here */

#endif
```

If the header is included twice, the second pass finds GEOM_H already
defined and skips the body — no duplicate definitions. Without guards,
two #includes of one header that defines anything = compile error.

## #ifdef / #ifndef for platform or debug switches

```c
#define DEBUG 1

#ifdef DEBUG
    fprintf(stderr, "x=%d\n", x);
#endif
```

The debug line exists in the compiled program ONLY when DEBUG is defined.
This is how C code bases support many platforms and configurations from one
source tree.

## #if with constant expressions

```c
#if MAX_SCORE > 50
#   define GRADE_SCALE "percent"
#else
#   define GRADE_SCALE "raw"
#endif
```

## What the preprocessor is NOT

It knows nothing of C types, variables, or scopes. It is a text machine.
Everything it produces must still be legal C — the errors you see after
expansion point at the result, not the macro call.
""",
    "Biên dịch có điều kiện",
    "#if, #ifdef, và include guard ngăn chặn định nghĩa trùng.",
    r"""
## Include guard

Mọi header đều mặc bộ giáp này:

```c
#ifndef GEOM_H
#define GEOM_H

/* khai báo nằm ở đây */

#endif
```

Nếu header bị include hai lần, lượt thứ hai thấy GEOM_H đã định nghĩa và bỏ
qua phần thân — không có định nghĩa trùng. Không có guard, hai lần #include
cùng một header định nghĩa gì đó = lỗi biên dịch.

## #ifdef / #ifndef cho các công tắc nền tảng hoặc debug

```c
#define DEBUG 1

#ifdef DEBUG
    fprintf(stderr, "x=%d\n", x);
#endif
```

Dòng debug chỉ tồn tại trong chương trình đã biên dịch KHI DEBUG được định
nghĩa. Đây là cách các code base C hỗ trợ nhiều nền tảng và cấu hình từ một
cây mã nguồn.

## #if với biểu thức hằng

```c
#if MAX_SCORE > 50
#   define GRADE_SCALE "percent"
#else
#   define GRADE_SCALE "raw"
#endif
```

## Những gì bộ tiền xử lý KHÔNG làm

Nó không biết gì về kiểu, biến, hay phạm vi của C. Nó là một cỗ máy văn bản.
Mọi thứ nó tạo ra vẫn phải là C hợp lệ — lỗi bạn thấy sau khi mở rộng chỉ vào
kết quả, không chỉ vào lời gọi macro.
""",
)

write_lesson(
    M17,
    L17C,
    "Why .h and .c Files Exist",
    "Declarations shared, definitions private — the split that scales.",
    13,
    r"""
## The problem it solves

Two .c files both need `int add(int, int);`. Without headers, each writes its
own copy — and when the signature changes, one copy silently rots.

## The split

```c
/* geom.h — the CONTRACT: what exists */
#ifndef GEOM_H
#define GEOM_H
int add(int a, int b);
double circle_area(double r);
#endif

/* geom.c — the IMPLEMENTATION */
#include "geom.h"
int add(int a, int b) { return a + b; }
double circle_area(double r) { return 3.14159265358979 * r * r; }
```

Any file that #includes "geom.h" may call add and circle_area; the compiler
checks calls against the declarations, and the linker finds the definitions
in geom.o.

## Declaration vs definition

A declaration announces a name and type (`...;`). A definition provides the
body/storage. Declarations may repeat; definitions of a function or global
must not (that is what guards protect).

## Translation units

Each .c file compiles alone — a translation unit. It sees only its own text
plus everything its #includes pull in. `static` on a function keeps it
private to the unit: the C tool for "this is not part of the public API".

## The build line grows

```sh
gcc -std=c23 main.c geom.c -o app
```

Two sources, compiled and linked in one command. Make (module 22) automates
exactly this.
""",
    "Vì sao tồn tại .h và .c",
    "Khai báo dùng chung, định nghĩa giữ riêng — sự tách biệt giúp mã nguồn lớn lên.",
    r"""
## Vấn đề nó giải quyết

Hai tệp .c cùng cần `int add(int, int);`. Không có header, mỗi bên tự viết
một bản — và khi chữ ký thay đổi, một bản âm thầm mục rữa.

## Sự tách biệt

```c
/* geom.h — HỢP ĐỒNG: cái gì tồn tại */
#ifndef GEOM_H
#define GEOM_H
int add(int a, int b);
double circle_area(double r);
#endif

/* geom.c — CÀI ĐẶT */
#include "geom.h"
int add(int a, int b) { return a + b; }
double circle_area(double r) { return 3.14159265358979 * r * r; }
```

Tệp nào #include "geom.h" đều gọi được add và circle_area; trình biên dịch
kiểm tra lời gọi theo khai báo, và linker tìm định nghĩa trong geom.o.

## Khai báo vs định nghĩa

Khai báo công bố tên và kiểu (`...;`). Định nghĩa cung cấp thân/bộ nhớ. Khai
báo có thể lặp lại; định nghĩa của một hàm hoặc biến toàn cục thì không (đó
là điều guard bảo vệ).

## Đơn vị dịch

Mỗi tệp .c được biên dịch một mình — một translation unit. Nó chỉ thấy văn
bản của mình cộng với mọi thứ #include kéo vào. `static` trên một hàm giữ nó
riêng tư trong đơn vị: công cụ C của "cái này không thuộc API công khai".

## Dòng lệnh build dài ra

```sh
gcc -std=c23 main.c geom.c -o app
```

Hai tệp nguồn, biên dịch và liên kết trong một lệnh. Make (module 22) sẽ tự
động hóa đúng việc này.
""",
)

write_practice(
    M17,
    "cb-p17-macros",
    "Macro Mechanics",
    "Function-like macros that must survive compound arguments.",
    "Cơ chế macro",
    "Macro kiểu hàm phải sống sót trước đối số phức hợp.",
    L17A,
    14,
    "beginner",
    [
        challenge(
            "cb17-sq-macro",
            "PARENTHESIZED SQUARE",
            "Define `#define SQ(x)` so that SQ of ANY integer expression computes its square. The tests compile SQ against compound arguments.",
            "#include <stdio.h>\n",
            [
                ("plain", "CHECK_EQ(SQ(4), 16);", "4*4."),
                ("compound arg", "CHECK_EQ(SQ(2 + 3), 25);", "Without inner parens this is 2+3*2+3 = 11."),
                ("in expression", "CHECK_EQ(SQ(3) + 1, 10);", "Outer parens keep +1 outside."),
            ],
            level="imitation",
        ),
        challenge(
            "cb17-max-macro",
            "Ternary MAX",
            "Define `#define MAX(a, b)` yielding the larger value. It must work inside larger expressions.",
            "#include <stdio.h>\n",
            [
                ("basic", "CHECK_EQ(MAX(3, 7), 7);", "Bigger wins."),
                ("negative", "CHECK_EQ(MAX(-9, -2), -2);", "Negatives compare fine."),
                ("expression args", "int i = 5;\nCHECK_EQ(MAX(i * 2, 9), 10);", "Each arg used exactly once here — safe."),
                ("nested", "CHECK_EQ(MAX(MAX(1, 5), 3), 5);", "Macros nest."),
            ],
            level="guided",
        ),
        challenge(
            "cb17-const-vs-define",
            "Constant Contract",
            "Define an object macro `SCALE` with value 100 and implement `int apply_scale(int v)` returning v * SCALE. Changing SCALE must change the function — the tests recompile with a different value through your macro.",
            "#include <stdio.h>\n",
            [
                ("uses macro", "CHECK_EQ(apply_scale(3), 300);", "Reference SCALE, not a literal 100."),
                ("bigger v", "CHECK_EQ(apply_scale(12), 1200);", "Same relationship for all inputs."),
            ],
            level="imitation",
        ),
    ],
    {
        "cb17-sq-macro": vi_challenge(
            "BÌNH PHƯƠNG CÓ NGOẶC",
            "Định nghĩa `#define SQ(x)` sao cho SQ của BẤT KỲ biểu thức nguyên nào cũng tính bình phương đúng. Các test biên dịch SQ với đối số phức hợp.",
            [("trơn", "4*4."), ("đối số phức hợp", "Không có ngoặc trong thì ra 2+3*2+3 = 11."), ("trong biểu thức", "Ngoặc ngoài giữ +1 ở bên ngoài.")],
        ),
        "cb17-max-macro": vi_challenge(
            "MAX tam nguyên",
            "Định nghĩa `#define MAX(a, b)` cho giá trị lớn hơn. Nó phải hoạt động trong các biểu thức lớn hơn.",
            [("cơ bản", "Số lớn thắng."), ("số âm", "Số âm so sánh bình thường."), ("đối số là biểu thức", "Mỗi đối số dùng đúng một lần ở đây — an toàn."), ("lồng nhau", "Macro lồng được.")],
        ),
        "cb17-const-vs-define": vi_challenge(
            "Hợp đồng hằng số",
            "Định nghĩa macro đối tượng `SCALE` bằng 100 và cài `int apply_scale(int v)` trả v * SCALE. Đổi SCALE phải đổi theo hàm — test biên dịch lại với giá trị khác qua macro của bạn.",
            [("dùng macro", "Tham chiếu SCALE, đừng viết số 100 cố định."), ("v lớn hơn", "Cùng quan hệ cho mọi đầu vào.")],
        ),
    },
    solutions=[
        (
            "cb17-sq-macro",
            '#include <stdio.h>\n#define SQ(x) ((x) * (x))\nint main(void) { return 0; }',
            '#include <stdio.h>\n#define SQ(x) (x * x)\nint main(void) { return 0; }',
        ),
        (
            "cb17-max-macro",
            '#include <stdio.h>\n#define MAX(a, b) ((a) > (b) ? (a) : (b))\nint main(void) { return 0; }',
            '#include <stdio.h>\n#define MAX(a, b) ((a) > (b) ? (b) : (b))\nint main(void) { return 0; }',
        ),
        (
            "cb17-const-vs-define",
            '#include <stdio.h>\n#define SCALE 100\nint apply_scale(int v) {\n    return v * SCALE;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#define SCALE 100\nint apply_scale(int v) {\n    return v + SCALE;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_practice(
    M17,
    "cb-p17-organize",
    "Organization Practice",
    "static helpers, do-while macro wrappers, and guarded declarations.",
    "Luyện tổ chức mã",
    "Hàm static, macro bao do-while, và khai báo có guard.",
    L17B,
    15,
    "beginner",
    [
        challenge(
            "cb17-static-helper",
            "Private Helper",
            "Implement `int digit_sum(int n)` using a static helper `int digit_sum_nonneg(int n)` for n >= 0; digit_sum itself handles negatives by summing the digits of the absolute value.",
            C_PRELUDE,
            [
                ("positive", "CHECK_EQ(digit_sum(123), 6);", "1+2+3."),
                ("negative", "CHECK_EQ(digit_sum(-45), 9);", "Absolute value first."),
                ("zero", "CHECK_EQ(digit_sum(0), 0);", "Zero has digit sum 0."),
            ],
            level="guided",
        ),
        challenge(
            "cb17-dowhile-macro",
            "Statement Macro",
            "Define `#define INCREMENT_IF(var, cond)` as a do-while(0) statement macro that increments var only when cond is true. It must be usable as a single statement (with a trailing semicolon) even inside if/else.",
            "#include <stdio.h>\n",
            [
                ("increments", "int x = 5;\nINCREMENT_IF(x, x > 0);\nCHECK_EQ(x, 6);", "Condition true: +1."),
                ("no increment", "int x = 5;\nINCREMENT_IF(x, x < 0);\nCHECK_EQ(x, 5);", "Condition false: unchanged."),
                ("dangling else safe", "int x = 0;\nint y = 0;\nif (1)\n    INCREMENT_IF(x, 1);\nelse\n    INCREMENT_IF(y, 1);\nCHECK_EQ(x, 1);\nCHECK_EQ(y, 0);", "do-while(0) makes the macro one statement."),
            ],
            level="independent",
        ),
        challenge(
            "cb17-triple-guard",
            "Guarded Values",
            "Define macros LOW_CUT 10 and HIGH_CUT 90 and implement `int band(int v)` returning -1 if v < LOW_CUT, 1 if v > HIGH_CUT, else 0.",
            C_PRELUDE,
            [
                ("below", "CHECK_EQ(band(5), -1);", "Under the floor."),
                ("inside", "CHECK_EQ(band(50), 0);", "Between cuts."),
                ("above", "CHECK_EQ(band(95), 1);", "Over the ceiling."),
                ("boundaries", "CHECK_EQ(band(10), 0);\nCHECK_EQ(band(90), 0);", "The cuts themselves are inside."),
            ],
            level="imitation",
        ),
    ],
    {
        "cb17-static-helper": vi_challenge(
            "Trợ giúp riêng tư",
            "Cài `int digit_sum(int n)` dùng một helper static `int digit_sum_nonneg(int n)` cho n >= 0; còn digit_sum xử lý số âm bằng cách cộng chữ số của giá trị tuyệt đối.",
            [("dương", "1+2+3."), ("âm", "Lấy giá trị tuyệt đối trước."), ("số 0", "Tổng chữ số của 0 là 0.")],
        ),
        "cb17-dowhile-macro": vi_challenge(
            "Macro câu lệnh",
            "Định nghĩa `#define INCREMENT_IF(var, cond)` là macro câu lệnh do-while(0) chỉ tăng var khi cond đúng. Nó phải dùng được như một câu lệnh đơn (kèm dấu chấm phẩy) ngay cả trong if/else.",
            [("tăng", "Điều kiện đúng: +1."), ("không tăng", "Điều kiện sai: giữ nguyên."), ("an toàn với else treo", "do-while(0) biến macro thành một câu lệnh.")],
        ),
        "cb17-triple-guard": vi_challenge(
            "Giá trị có hàng rào",
            "Định nghĩa macro LOW_CUT 10 và HIGH_CUT 90 rồi cài `int band(int v)` trả -1 nếu v < LOW_CUT, 1 nếu v > HIGH_CUT, còn lại 0.",
            [("dưới", "Dưới sàn."), ("trong", "Giữa hai hàng rào."), ("trên", "Vượt trần."), ("biên", "Chính các mốc nằm trong khoảng.")],
        ),
    },
    solutions=[
        (
            "cb17-static-helper",
            '#include <stdio.h>\nstatic int digit_sum_nonneg(int n) {\n    int s = 0;\n    while (n > 0) { s += n % 10; n /= 10; }\n    return s;\n}\nint digit_sum(int n) {\n    if (n < 0) n = -n;\n    return digit_sum_nonneg(n);\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\nstatic int digit_sum_nonneg(int n) {\n    int s = 0;\n    while (n > 0) { s += n % 10; n /= 10; }\n    return s;\n}\nint digit_sum(int n) {\n    if (n < 0) n = -n;\n    return digit_sum_nonneg(n) + 1;\n}\nint main(void) { return 0; }',
        ),
        (
            "cb17-dowhile-macro",
            '#include <stdio.h>\n#define INCREMENT_IF(var, cond) do { if (cond) (var)++; } while (0)\nint main(void) { return 0; }',
            '#include <stdio.h>\n#define INCREMENT_IF(var, cond) do { if (cond) (var)++; else (var)--; } while (0)\nint main(void) { return 0; }',
        ),
        (
            "cb17-triple-guard",
            '#include <stdio.h>\n#define LOW_CUT 10\n#define HIGH_CUT 90\nint band(int v) {\n    if (v < LOW_CUT) return -1;\n    if (v > HIGH_CUT) return 1;\n    return 0;\n}\nint main(void) { return 0; }',
            '#include <stdio.h>\n#define LOW_CUT 10\n#define HIGH_CUT 90\nint band(int v) {\n    if (v <= LOW_CUT) return -1;\n    if (v > HIGH_CUT) return 1;\n    return 0;\n}\nint main(void) { return 0; }',
        ),
    ],
)

write_checkpoint(
    M17,
    L17D,
    "Checkpoint: Preprocessor",
    "Macro-driven clamp logic with a statement macro.",
    15,
    r"""
## Checkpoint

Macros as named constants and guarded statements — before reaching for them
in real headers.
""",
    "Điểm kiểm tra: Bộ tiền xử lý",
    "Logic kẹp giá trị bằng macro cùng một macro câu lệnh.",
    r"""
## Điểm kiểm tra

Macro làm hằng số có tên và câu lệnh có bảo vệ — trước khi dùng chúng trong
header thật.
""",
    challenge(
        "cb17-checkpoint-clamp",
        "Macro Clamp",
        "Define `#define CLAMP(v, lo, hi)` as a do-while(0) statement macro that modifies v IN PLACE to lie within [lo, hi], and implement `int percent_band(int v)` returning 0 when v <= 0, 100 when v >= 100, and v otherwise.",
        "#include <stdio.h>\n",
        [
            ("clamp mid", "int v = 42;\nCLAMP(v, 0, 100);\nCHECK_EQ(v, 42);", "Inside stays."),
            ("clamp low", "int v = -5;\nCLAMP(v, 0, 100);\nCHECK_EQ(v, 0);", "Floor applies."),
            ("clamp high", "int v = 150;\nCLAMP(v, 0, 100);\nCHECK_EQ(v, 100);", "Ceiling applies."),
            ("percent band", "CHECK_EQ(percent_band(-5), 0);\nCHECK_EQ(percent_band(150), 100);\nCHECK_EQ(percent_band(42), 42);", "Compose CLAMP with the band logic."),
        ],
    ),
    vi_challenge(
        "Kẹp giá trị bằng macro",
        "Định nghĩa `#define CLAMP(v, lo, hi)` là macro câu lệnh do-while(0) sửa v TẠI CHỖ nằm trong [lo, hi], và cài `int percent_band(int v)` trả 0 khi v <= 0, 100 khi v >= 100, còn lại trả v.",
        [("kẹp giữa", "Trong khoảng thì giữ."), ("kẹp dưới", "Sàn áp dụng."), ("kẹp trên", "Trần áp dụng."), ("percent band", "Kết hợp CLAMP với logic băng giá trị.")],
    ),
    solution='#include <stdio.h>\n#define CLAMP(v, lo, hi) do { (v) = ((v) < (lo) ? (lo) : ((v) > (hi) ? (hi) : (v))); } while (0)\nint percent_band(int v) {\n    int c = v;\n    CLAMP(c, 0, 100);\n    return c;\n}\nint main(void) { return 0; }',
    wrong='#include <stdio.h>\n#define CLAMP(v, lo, hi) do { (v) = ((v) < (lo) ? (lo) : ((v) > (hi) ? (hi) : (v))); } while (0)\nint percent_band(int v) {\n    int c = v;\n    CLAMP(c, 10, 100);\n    return c;\n}\nint main(void) { return 0; }',
)

print("batch 8 done: modules 15-17")
