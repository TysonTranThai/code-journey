#!/usr/bin/env python3
"""One-shot fixer for hsgi_m18.py: restore C2A/C2B definitions (with the
fixed winmax discriminator test), merge VI entries into VI_P18, and point
the write_practice call at VI_P18. Idempotent: aborts if anchors missing."""
import io

P = "scripts/content-authoring/hsgi_m18.py"
src = io.open(P, encoding="utf-8").read()

C2_DEFS = """C2A = challenge(
    "hsgi-p18-winmax",
    "Cửa sổ lớn nhất",
    \"\"\"**Bài toán.** Mảng n phần tử và cửa sổ k. In GIÁ TRỊ LỚN NHẤT của
mỗi cửa sổ kích thước k trượt từ trái sang phải — mỗi cửa sổ một số,
cách nhau bởi dấu cách, tất cả trên MỘT dòng.

**Ràng buộc:** 1 ≤ k ≤ n ≤ 2·10^5; |a[i]| ≤ 10^9.

Deque đơn điệu giảm: đầu deque là chỉ số lớn nhất hiện hành; phần tử
ra khỏi cửa sổ bị pop đầu, phần tử mới pop đuổi mọi phần tử ≤ nó.
Mỗi phần tử vào/ra deque đúng một lần — O(n). Quét max lại mỗi cửa
sổ là O(n·k) — quá hạn với n = 2·10^5, k lớn.\"\"\",
    [
        contest_test(
            "kinh điển",
            T("8 3", "1 3 -1 -3 5 3 6 7"),
            T("3 3 5 5 6 7"),
            "Sáu cửa sổ: [1 3 -1]→3, [3 -1 -3]→3, [-1 -3 5]→5, [-3 5 3]→5, [5 3 6]→6, [3 6 7]→7.",
        ),
        contest_test(
            "k = 1 — chính mảng",
            T("7 1", "4 2 12 11 -5 6 7"),
            T("4 2 12 11 -5 6 7"),
            "Cửa sổ đơn phần tử.",
        ),
        contest_test(
            "k = n — một cửa sổ",
            T("3 3", "2 9 4"),
            T("9"),
            "Max toàn mảng.",
        ),
        contest_test(
            "max cũ phải rời cửa sổ",
            T("3 2", "3 1 2"),
            T("3 2"),
            "Cửa sổ hai: max(1, 2) = 2 — max cũ 3 đã rời; quên pop hết hạn trả 3.",
        ),
        contest_test(
            "n lớn — cửa sổ gần trọn mảng",
            T("200000 199996") + T(" ".join(str((i * 13) % 201 - 100) for i in range(200000))),
            T("100 100 100 100 100"),
            "Năm cửa sổ, mỗi cửa đều chứa đỉnh 100; deque một lượt O(n).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

C2B = challenge(
    "hsgi-p18-movies",
    "Xem phim tối đa",
    \"\"\"**Bài toán.** n suất chiếu, suất i bắt đầu s[i] và kết thúc e[i]
(s[i] < e[i]). Chọn số suất lớn nhất để xem sao cho không hai suất
nào chồng nhau (suất bắt đầu đúng lúc suất trước kết thúc vẫn hợp
lệ: s ≥ e_trước). In số suất tối đa.

Luận điểm đổi chỗ: chọn suất KẾT THÚC SỚM NHẤT còn khả dĩ — bất kỳ
nghiệm tối ưu nào đều đổi được sang lựa chọn này không xấu đi. Sort
theo e, quét một lượt.

Cái bẫy kinh điển: sort theo THỜI ĐIỂM BẮT ĐẦU — một suất dài sớm
chiếm slot chặn mọi suất ngắn phía sau.\"\"\",
    [
        contest_test(
            "ví dụ",
            T("6", "1 3", "2 5", "4 7", "1 8", "5 9", "8 10"),
            T("3"),
            "Chọn (1,3), (4,7), (8,10).",
        ),
        contest_test(
            "một suất",
            T("1", "3 7"),
            T("1"),
            "Luôn xem được một suất.",
        ),
        contest_test(
            "daisy chain",
            T("3", "1 2", "2 3", "3 4"),
            T("3"),
            "Tiếp giáp đúng biên được tính (s ≥ e_trước).",
        ),
        contest_test(
            "trùng giờ toàn phần",
            T("6") + T(" ".join("5 7" for _ in range(6))),
            T("1"),
            "Sáu suất trùng — chỉ chọn một.",
        ),
        contest_test(
            "n lớn",
            T("200000") + T(" ".join(str((i * 7) % 100) + " " + str((i * 7) % 100 + 1 + (i % 10)) for i in range(200000))),
            T("31"),
            "Sort theo kết thúc; quét một lượt O(n log n).",
        ),
        contest_test(
            "phản ví dụ sort-bắt-đầu",
            T("3", "1 10", "2 3", "4 5"),
            T("2"),
            "Sort theo bắt đầu chọn (1,10) trước → chỉ 1 suất; EDF chọn 2.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_P18.update({"""

if "C2A = challenge(" in src:
    print("already fixed")
    raise SystemExit(0)

old = "VI_P18B = {"
assert src.count(old) == 1, "anchor VI_P18B not found"
src = src.replace(old, C2_DEFS)

old_call = "    [C1A, C1B, C2A, C2B],\n    VI_P18B,"
assert src.count(old_call) == 1, "anchor practice VI map not found"
src = src.replace(old_call, "    [C1A, C1B, C2A, C2B],\n    VI_P18,")

io.open(P, "w", encoding="utf-8").write(src)
print("C2A/C2B restored; VI merged; practice passes VI_P18")
