#!/usr/bin/env python3
"""HSG Intermediate — Module 17: hsgi-debug (gỡ lỗi).

Real broken programs embedded in the statement; the learner identifies and
fixes the bug. W = the bug verbatim (a real defect, not a slow copy).
Bugs: off-by-one (binary search), wrong comparator (EDF), wrong-direction
greedy, overflow init, negative-modulo reduction.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \n escapes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test,
)

Q = chr(92)
NL = chr(10)


def cpp(s):
    return s.replace("{{NL}}", Q + "n")


def T(*lines):
    return "".join(l + NL for l in lines)


CPP_STD = cpp("""#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <deque>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-debug"

write_module(
    M,
    "Debugging — Fixing Broken Contest Code",
    "Five real defective programs: read the code like a judge reads a submission, find the bug, and fix it.",
    "Gỡ lỗi — Sửa code thi đấu bị lỗi",
    "Năm chương trình lỗi thật: đọc code như giám khảo đọc bài nộp, tìm lỗi và sửa.",
    ["hsgi-m17-method", "hsgi-m17-catalog", "hsgi-cp-m17"],
    ["hsgi-p17-debug"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m17-method",
    "The Debugging Method — Reproduce, Isolate, Verify",
    "Contest debugging is a three-step loop; the smallest failing test is the whole game.",
    20,
    """## Ba bước

**1. Tái lập nhỏ nhất.** Thu nhỏ test xuống nhỏ nhất còn sai. Test nhỏ
còn sai → logic sai; chỉ test lớn sai → khả năng cao là phức tạp/
tràn số.

**2. Cô lập giả thuyết.** Liệt kê 2–3 nghi phạm theo xác suất:
ranh giới vòng lặp, khởi tạo, so sánh sai dấu, tràn int, modulo âm.
In giá trị trung gian trên test nhỏ (debug output được phép — chấm
chỉ nhìn stdout CUỐI cùng... thận trọng: một số judge cấm; dùng biến
tạm và xóa trước khi nộp).

**3. Kiểm chứng bản vá.** Sau khi sửa, chạy lại TOÀN BỘ test ví dụ
và tự dựng thêm test biên: n = 1, giá trị lớn nhất, sắp xếp ngược.

## Nhận diện nhanh theo triệu chứng

| Triệu chứng | Nghi phạm chính |
|---|---|
| WA chỉ test lớn | tràn số, int thay long long |
| WA test nhỏ | off-by-one, sai điều kiện |
| TLE vừa phải | thuật toán đúng, phức tạp sai |
| RE | mảng ngoài biên, đệ quy quá sâu |
| WA số âm | modulo âm, init 0 cho best |

**Điểm mấu chốt:** thu nhỏ test trước; sửa rồi phải chạy lại toàn
bộ, không chỉ test vừa fail.""",
    "Phương pháp gỡ lỗi — Tái lập, cô lập, kiểm chứng",
    "Gỡ lỗi trong contest là vòng ba bước; test nhỏ nhất còn sai là tất cả.",
    """## Ba bước

Tái lập test nhỏ nhất còn sai (nhỏ mà sai → logic; chỉ lớn mà sai →
tràn số/phức tạp). Cô lập nghi phạm theo xác suất: ranh giới vòng,
khởi tạo, dấu so sánh, tràn int, modulo âm. Kiểm chứng bản vá trên
TOÀN BỘ test + test biên tự dựng.

## Nhận diện theo triệu chứng

WA chỉ test lớn → tràn số. WA test nhỏ → off-by-one. TLE → đúng thuật
toán, sai phức tạp. RE → ngoài biên. WA số âm → modulo âm/init best.

**Điểm mấu chốt:** thu nhỏ trước, vá xong chạy lại toàn bộ.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m17-catalog",
    "The Defect Catalog — The Five Classic Bugs",
    "Off-by-one binary search, EDF comparator, wrong-direction greedy, overflow init, and the negative modulo.",
    20,
    """## 1. Tìm kiếm nhị phân — off-by-one ranh giới

`lo + (hi - lo) / 2` không phóng to cho phép "nhảy qua" đáp án nằm ở
hi. Dạng chuẩn cho "thấp nhất thỏa": giữ thêm biến `ans` ghi lại vị
trí hợp lệ cuối cùng; không phụ thuộc vào việc hi kết thúc ở đâu.

## 2. Comparator EDF — sai chiều sort

deadline SỚM phải xử lý TRƯỚC → sort tăng dần theo deadline. Đảo chiều
(vì vô tình so `a.deadline > b.deadline` trong `operator<`) làm toàn bộ
lịch hỏng: test nhỏ 2 việc đã phát hiện.

## 3. Tham lam sai hướng — dấu của t

Mỗi phần tử có thời lượng riêng; sort theo TỐT NHẤT CỦA TỪNG PHẦN TỬ
(không phải theo hàng đứng của ma trận lợi nhuận). Trước khi tin một
tham lam: dựng test phản ví dụ 2–3 phần tử.

## 4. Tràn số do init

`long long best = 0` sai khi đáp án hợp lệ có thể âm. Kiểu "biến phụ
+ cờ đầu tiên" an toàn tuyệt đối.

## 5. Modulo âm

C++: `(x % p)` giữ dấu của x. Sau mọi phép trừ: `r = (r % p + p) % p`.
Tràn trước modulo — 10^18 chia dư 10^9+7 vẫn sai nếu nhân hai số
10^9 (dùng __int128 hoặc nhân Nga).

**Điểm mấu chốt:** mỗi lỗi có test phản ví dụ điển hình; học test đó
là học sửa lỗi đó.""",
    "Danh mục lỗi — Năm lỗi kinh điển",
    "Nhị phân off-by-one, comparator EDF, tham lam sai hướng, init tràn số, modulo âm.",
    """## Năm lỗi kinh điển

**Nhị phân:** giữ biến `ans` ghi vị trí hợp lệ — không tin ranh giới
hi. **Comparator EDF:** deadline sớm sort TRƯỚC — đảo chiều phá lịch
chỉ sau 2 việc. **Tham lam sai hướng:** sort theo tốt nhất của từng
phần tử; dựng phản ví dụ trước khi tin. **Init:** `best = 0` sai khi
đáp án âm — dùng biến phụ + cờ. **Modulo âm:** `(x % p)` giữ dấu x —
sau mọi phép trừ cộng lại; nhân hai số ~10^9 tràn trước modulo.

**Điểm mấu chốt:** mỗi lỗi có phản ví dụ điển hình — thuộc test đó.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p17-binoff",
    "Debug: Tìm kiếm nhị phân — off-by-one",
    T(
        "**Bài toán (đã đúng):** Mảng tăng ngặt n phần tử. Trả về chỉ số (0-based)",
        "của x nếu có, ngược lại trả về −1.",
        "",
        "**Chương trình dưới đây SAI.** Tìm lỗi và sửa: với n = 1 nó in −1 dù",
        "phần tử duy nhất có khớp x.",
        "",
        "**Code lỗi:**",
        "```cpp",
        "void solve(std::istream& in, std::ostream& out) {",
        "    int n; in >> n;",
        "    vector<long long> a(n);",
        "    for (auto& x : a) in >> x;",
        "    long long x; in >> x;",
        "    int lo = 0, hi = n - 1, ans = -1;",
        "    while (lo < hi) {                    // BUG: phải là lo <= hi",
        "        int mid = lo + (hi - lo) / 2;",
        "        if (a[mid] == x) { ans = mid; break; }",
        "        else if (a[mid] < x) lo = mid + 1;",
        "        else hi = mid - 1;",
        "    }",
        "    out << ans;",
        "}",
        "```",
        "",
        "**Yêu cầu:** nộp bản ĐÃ SỬA (đổi điều kiện vòng lặp, giữ nguyên logic",
        "còn lại) và pass mọi test.",
        "",
        "**Input:** dòng 1: n; dòng 2: mảng tăng; dòng 3: giá trị cần tìm.",
        "",
        "**Ví dụ:** `1` / `4` / `4` -> `0` (bản lỗi in −1: vòng không chạy khi",
        "lo == hi).",
    ),
    [
        contest_test(
            "dò giữa mảng",
            T("5", "1 3 5 7 9", "7"),
            T("3"),
            "Test giữa mảng: bug ranh giới không chạm — mã lỗi vẫn tìm thấy (chỉ số 3).",
        ),
        contest_test(
            "n = 1, khớp đầu",
            T("1", "4", "4"),
            T("0"),
            "Một phần tử: lo = hi = 0, mid = 0, khớp.",
        ),
        contest_test(
            "gần biên phải",
            T("3", "1 2 3", "3"),
            T("2"),
            "Phần tử cuối cùng.",
        ),
        contest_test(
            "không có — bên trái",
            T("3", "1 2 3", "0"),
            T("-1"),
            "Nhỏ hơn mọi phần tử.",
        ),
        contest_test(
            "không có — bên phải",
            T("3", "1 2 3", "4"),
            T("-1"),
            "Lớn hơn mọi phần tử.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p17-edfcmp",
    "Debug: Comparator EDF đảo chiều",
    T(
        "**Bài toán:** n việc, việc i cần t[i] giờ và có deadline d[i]. Một máy,",
        "bắt đầu tại thời điểm 0. In 'YES' nếu có thứ tự làm tất cả việc đúng",
        "deadline, ngược lại 'NO'.",
        "",
        "**Code lỗi:** deadline SỚM phải xếp TRƯỚC — comparator dưới đây sort",
        "SAI CHIỀU. Mô phỏng đúng phần còn lại của mã: cộng thời lượng tuần tự,",
        "nếu tổng vượt deadline bất kỳ thì 'NO'.",
        "",
        "```cpp",
        "// BROKEN: sort giảm dần theo deadline (ngược EDF)",
        "// sort theo d giảm dần, sau đó quét cộng dồn kiểm tra",
        "```",
        "",
        "**Yêu cầu:** Hãy VIẾT LẠI bản sửa đúng (EDF chuẩn) và pass các test.",
        "Bản nộp của bạn là bản ĐÃ SỬA — code lỗi chỉ để tham khảo.",
        "",
        "**Input:** n; n dòng t[i] d[i] (1 ≤ t[i], d[i] ≤ 10^9).",
        "**Output:** YES hoặc NO.",
        "",
        "**Ví dụ:** `2` / `3 10` / `4 5` -> `YES` (EDF: 4 (d=5) rồi 3 (d=10):",
        "4 ≤ 5 và 7 ≤ 10).",
    ),
    [
        contest_test(
            "ví dụ",
            T("2", "3 10", "4 5"),
            T("YES"),
            "EDF: 4 (d=5) rồi 3 (d=10); 4 ≤ 5 và 7 ≤ 10.",
        ),
        contest_test(
            "hai việc — đảo chiều cứu được",
            T("2", "5 3", "2 9"),
            T("NO"),
            "EDF: 5 (d=3) rồi 2: 5 > 3 → NO bất kể thứ tự.",
        ),
        contest_test(
            "thứ tự đúng duy nhất",
            T("3", "2 4", "3 7", "1 3"),
            T("YES"),
            "EDF: 1 (d=3), 2 (d=4), 3 (d=7): 1 ≤ 3, 3 ≤ 4, 6 ≤ 7.",
        ),
        contest_test(
            "việc đầu đã trễ",
            T("1", "5 4"),
            T("NO"),
            "Một việc dài hơn deadline của chính nó.",
        ),
        contest_test(
            "việc bằng deadline",
            T("3", "3 3", "2 6", "1 10"),
            T("YES"),
            "3 ≤ 3, 5 ≤ 6, 6 ≤ 10 — biên trên bằng đúng.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p17-moneysort",
    "Debug: Tham lam sai hướng",
    T(
        "**Bài toán (đã đúng):** Có n đồng xu (giá trị có thể ÂM). Chọn một TẬP",
        "CON KHÔNG RỖNG sao cho tổng lớn nhất; in tổng đó.",
        "",
        "Phân tích đúng: chọn phần tử BẤT KỲ (không cần liên tiếp) → chọn mọi",
        "phần tử dương; nếu không có phần tử dương nào, chọn đúng MỘT phần tử",
        "lớn nhất (bắt buộc khác rỗng).",
        "",
        "**Bản thảo sai:** quét LIÊN TIẾP (Kadane) với init best = 0 — liên",
        "tiếp bỏ cơ hội nhảy qua đoạn âm lớn, và init 0 sai khi mọi xu âm.",
        "",
        "**Yêu cầu:** viết bản đúng, pass mọi test.",
        "",
        "**Input:** n; n giá trị (|a[i]| ≤ 10^4, n ≤ 2·10^5).",
        "**Output:** tổng lớn nhất của tập con không rỗng.",
        "",
        "**Ví dụ:** `4` / `2 -5 3 1` -> `6` (2+3+1; bỏ −5).",
    ),
    [
        contest_test(
            "ví dụ",
            T("4", "2 -5 3 1"),
            T("6"),
            "Tổng mọi phần tử dương.",
        ),
        contest_test(
            "mọi phần tử âm",
            T("3", "-5 -2 -9"),
            T("-2"),
            "Bắt buộc chọn một xu: −2 là ít xấu nhất. Init 0 là SAI.",
        ),
        contest_test(
            "một phần tử",
            T("1", "-7"),
            T("-7"),
            "n = 1 âm.",
        ),
        contest_test(
            "xen kẽ",
            T("5", "3 -1 4 -1 5"),
            T("12"),
            "Tập con bất kỳ: chọn mọi phần tử dương 3+4+5 = 12 (bỏ hai −1).",
        ),
        contest_test(
            "toàn dương",
            T("3", "1 2 3"),
            T("6"),
            "Chọn hết.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p17-initovf",
    "Debug: Init tràn số",
    T(
        "**Bài toán (đã đúng):** n bài báo, bài i có cột d[i]. Một biên tập",
        "làm GỘP: tổng cộng dồn mọi cột rồi in (long long). Bản thảo sai dùng",
        "biến tổng kiểu int.",
        "",
        "**Yêu cầu:** viết bản đúng, dùng số học 64-bit, pass mọi test.",
        "",
        "**Input:** n (≤ 2·10^5); n giá trị d[i] (1 ≤ d[i] ≤ 10^9).",
        "**Output:** tổng dạng 64-bit.",
        "",
        "**Ví dụ:** `3` / `1000000000 1000000000 1000000000` -> `3000000000`",
        "(int 32-bit tràn).",
    ),
    [
        contest_test(
            "ví dụ",
            T("3", "1000000000 1000000000 1000000000"),
            T("3000000000"),
            "3·10^9 vượt int.",
        ),
        contest_test(
            "một phần tử",
            T("1", "1"),
            T("1"),
            "Biên dưới.",
        ),
        contest_test(
            "n lớn toàn max",
            T("200000") + T(" ".join("1000000000" for _ in range(200000))),
            T("200000000000000"),
            "2·10^14 — long long.",
        ),
        contest_test(
            "kết hợp lớn nhỏ",
            T("4", "1 999999999 3 999999999"),
            T("2000000002"),
            "Vượt 2^31−1 ≈ 2.147·10^9 ngay khi tổng chạm mốc.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p17-modneg",
    "Debug: Modulo âm",
    T(
        "**Bài toán (đã đúng):** tính (a − b) mod 10^9+7 với a, b ≤ 10^18",
        "(không âm). In kết quả trong [0, 10^9+6].",
        "",
        "**Code lỗi:** `out << (a - b) % p;` — (a − b) có thể ÂM và C++ giữ",
        "dấu của số bị chia (a, b không âm nên a − b ≥ −10^18: không tràn;",
        "lỗi duy nhất là dấu modulo).",
        "",
        "**Yêu cầu:** sửa thành `((a - b) % p + p) % p` (hoặc chuẩn hóa tương",
        "đương) và pass mọi test.",
        "",
        "**Input:** a, b (0 ≤ a, b ≤ 10^18).",
        "**Output:** (a − b) mod p.",
        "",
        "**Ví dụ:** `3 5` -> `1000000005` (không phải −2).",
    ),
    [
        contest_test(
            "ví dụ",
            T("3 5"),
            T("1000000005"),
            "−2 mod p = p − 2.",
        ),
        contest_test(
            "bằng nhau",
            T("7 7"),
            T("0"),
            "0 là biên.",
        ),
        contest_test(
            "âm vừa",
            T("0 1000000000"),
            T("7"),
            "−10^9 mod (10^9+7) = 7.",
        ),
        contest_test(
            "dương thường",
            T("10 3"),
            T("7"),
            "Không âm — chuẩn.",
        ),
        contest_test(
            "cực đại",
            T("1000000000000000000 999999999999999999"),
            T("1"),
            "Hiệu 1 — biên trên input.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

VI17 = {
    "hsgi-p17-binoff": vi_challenge(
        "Debug: Tìm kiếm nhị phân — off-by-one",
        T("**Bài toán:** tìm chỉ số x trong mảng tăng, không có trả −1.",
          "", "Chạy mã trong đề bằng tay, in đúng kết quả mã ĐÃ CHO."),
        [("1 3 5 7 9, x=7", "2."),
         ("kỹ thuật", "Đọc kỹ code: mọi vòng lặp vẽ bảng lo/hi/mid.")],
    ),
    "hsgi-p17-edfcmp": vi_challenge(
        "Debug: Comparator EDF đảo chiều",
        T("**Bài toán:** một máy, n việc (t[i], d[i]); YES nếu xếp được hết."),
        [("3 10 / 4 5", "YES (EDF: 4 rồi 3; 7 ≤ 10)."),
         ("kỹ thuật", "EDF: deadline sớm xếp trước; sort giảm dần là lỗi.")],
    ),
    "hsgi-p17-moneysort": vi_challenge(
        "Debug: Tham lam sai hướng",
        T("**Bài toán:** chọn tập con không rỗng tổng lớn nhất (xu có âm)."),
        [("2 -5 3 1", "6."),
         ("mọi âm", "-5 -2 -9 → −2 (init 0 là SAI)."),
         ("kỹ thuật", "Tập con bất kỳ: tổng mọi phần tử dương; không dương → lớn nhất.")],
    ),
    "hsgi-p17-initovf": vi_challenge(
        "Debug: Init tràn số",
        T("**Bài toán:** tổng cột 64-bit."),
        [("3 × 10^9", "3000000000 — int tràn."),
         ("n lớn", "200000 × 10^9 = 2·10^14 — long long.")],
    ),
    "hsgi-p17-modneg": vi_challenge(
        "Debug: Modulo âm",
        T("**Bài toán:** (a − b) mod 10^9+7, kết quả trong [0, p)."),
        [("3 5", "1000000005."),
         ("kỹ thuật", "((a−b) % p + p) % p — C++ giữ dấu số bị chia.")],
    ),
}

write_practice(
    M,
    "hsgi-p17-debug",
    "Debugging Problem Set",
    "Five broken-program investigations: binary-search boundary, EDF comparator, greedy direction, overflow-safe summation, negative modulo.",
    "Bài tập gỡ lỗi",
    "Năm chương trình lỗi: ranh giới nhị phân, comparator EDF, hướng tham lam, tổng 64-bit, modulo âm.",
    "hsgi-m17-catalog",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI17,
    solutions=[
        (
            "hsgi-p17-binoff",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long x; in >> x;
    int lo = 0, hi = n - 1, ans = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == x) { ans = mid; break; }
        else if (a[mid] < x) lo = mid + 1;
        else hi = mid - 1;
    }
    out << ans << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long x; in >> x;
    // near-miss: tìm chỉ số 1-based thay vì 0-based (quy ước sai)
    int lo = 0, hi = n - 1, ans = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == x) { ans = mid + 1; break; }
        else if (a[mid] < x) lo = mid + 1;
        else hi = mid - 1;
    }
    out << ans << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p17-edfcmp",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& [t, d] : v) in >> t >> d;
    sort(v.begin(), v.end(), [](const auto& x, const auto& y) {
        return x.second < y.second;               // EDF: deadline sớm trước
    });
    long long cur = 0;
    for (auto& [t, d] : v) {
        cur += t;
        if (cur > d) { out << "NO" << "{{NL}}"; return; }
    }
    out << "YES" << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& [t, d] : v) in >> t >> d;
    // near-miss: sort GIẢM dần theo deadline — ngược EDF
    sort(v.begin(), v.end(), [](const auto& x, const auto& y) {
        return x.second > y.second;
    });
    long long cur = 0;
    for (auto& [t, d] : v) {
        cur += t;
        if (cur > d) { out << "NO" << "{{NL}}"; return; }
    }
    out << "YES" << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p17-moneysort",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // tập con bất kỳ: chọn mọi phần tử dương; nếu không có phần tử
    // dương nào, chọn đúng MỘT phần tử (lớn nhất)
    long long sum = 0, mx = LLONG_MIN;
    bool any = false;
    for (long long x : a) {
        if (x > 0) { sum += x; any = true; }
        mx = max(mx, x);
    }
    out << (any ? sum : mx) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    // near-miss: init best = 0 — mảng toàn âm trả 0 thay vì xu âm lớn nhất
    long long best = 0, cur = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        cur = max(cur + x, x);
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p17-initovf",
            CPP_STD + cpp("""    int n; in >> n;
    long long s = 0;
    for (int i = 0; i < n; ++i) { long long x; in >> x; s += x; }
    out << s << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    // near-miss: int accumulator — tràn từ ~2.1·10^9
    int s = 0;
    for (int i = 0; i < n; ++i) { int x; in >> x; s += x; }
    out << s << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p17-modneg",
            CPP_STD + cpp("""    const long long p = 1000000007;
    long long a, b; in >> a >> b;
    long long r = (a - b) % p;
    if (r < 0) r += p;
    out << r << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    const long long p = 1000000007;
    long long a, b; in >> a >> b;
    // near-miss: không chuẩn hóa số âm — C++ giữ dấu của số bị chia
    out << (a - b) % p << "{{NL}}";
""") + END,
        ),
    ],
)

# ------------------------------------------------------------------ checkpoint
CH17 = challenge(
    "hsgi-cp-m17-replay",
    "Nhật ký chơi lại — dò lỗi tràn số",
    """**Bài toán.** Nhật ký gồm n sự kiện; sự kiện i có delta[i] (có thể
âm). Điểm cân bằng nhỏ nhất k sao cho tổng tiền tố S_k = delta[1] +
... + delta[k] LỚN NHẤT (in k); nếu nhiều k cùng đạt max, in k NHỎ NHẤT. Nếu
max S_k ≤ 0 (mọi tổng tiền tố không dương), in −1.

**Ràng buộc:** 1 ≤ n ≤ 2·10^5; |delta[i]| ≤ 10^9. Tổng có thể tới
2·10^14 — long long bắt buộc (đây là lỗi bị săn).

Mã lỗi kinh điển: giữ S kiểu int (tràn ở test lớn) hoặc trả k của
LẦN ĐẦU đạt giá trị lớn nhất sau khi đã cập nhật nhầm ">=" (trả k
LỚN NHẤT thay vì nhỏ nhất).""",
    [
        contest_test(
            "ví dụ",
            T("5", "2 -3 4 1 -2"),
            T("4"),
            "S = 2, −1, 3, 4, 2 — max 4 tại k = 4.",
        ),
        contest_test(
            "toàn âm",
            T("3", "-5 -2 -9"),
            T("-1"),
            "Mọi S_k âm → −1.",
        ),
        contest_test(
            "max đầu",
            T("3", "5 -1 -1"),
            T("1"),
            "S = 5, 4, 3 — max tại k = 1.",
        ),
        contest_test(
            "lặp max — k nhỏ nhất",
            T("4", "3 -1 1 0"),
            T("1"),
            "S = 3, 2, 3, 3 — max 3 lặp; dùng > (không ≥) giữ k nhỏ nhất = 1.",
        ),
        contest_test(
            "n lớn — tràn int",
            T("200000") + T(" ".join("1000000000" for _ in range(200000))),
            T("200000"),
            "Tổng tăng đơn điệu tới 2·10^14 — int tràn từ phần tử thứ 3.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CP17 = vi_challenge(
    "Nhật ký chơi lại — dò lỗi tràn số",
    """**Bài toán.** Tổng tiền tố lớn nhất đạt lần đầu tại k; nếu mọi tổng
≤ 0 in −1. long long bắt buộc.""",
    [("2 -3 4 1 -2", "4 (S = 2, −1, 3, 4, 2)."),
     ("kỹ thuật", "int tràn ở 2·10^14; dùng long long; cập nhật >, không ≥.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m17",
    "Checkpoint — Debugging",
    "Pass the graded problem to finish the debugging module.",
    25,
    """**Checkpoint — Debugging.** Pass the graded challenge: prefix-sum
argmax with the earliest index — the hunted bugs are a 32-bit
accumulator and >= instead of > on ties.

**Điểm kiểm tra — Gỡ lỗi.** Pass bài chấm: argmax tổng tiền tố với
chỉ số nhỏ nhất — lỗi bị săn: bộ cộng 32-bit và >= thay vì > khi
bằng nhau.""",
    "Checkpoint — Debugging",
    "Pass bài chấm để hoàn thành module gỡ lỗi.",
    """**Điểm kiểm tra — Gỡ lỗi.** Pass bài chấm bên dưới: argmax tổng
tiền tố, long long, đẳng thức lấy chỉ số nhỏ nhất.""",
    CH17,
    VI_CP17,
    solution=CPP_STD + cpp("""    int n; in >> n;
    long long s = 0;
    long long best = LLONG_MIN;
    int bestK = -1;
    for (int k = 1; k <= n; ++k) {
        long long x; in >> x;
        s += x;
        if (s > best) { best = s; bestK = k; }
    }
    if (best <= 0) out << -1 << "{{NL}}";
    else out << bestK << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    // near-miss: int accumulator — tràn trên test lớn (2·10^14)
    int s = 0;
    int best = INT_MIN, bestK = -1;
    for (int k = 1; k <= n; ++k) {
        int x; in >> x;
        s += x;
        if (s > best) { best = s; bestK = k; }
    }
    if (best <= 0) out << -1 << "{{NL}}";
    else out << bestK << "{{NL}}";
""") + END,
)
