#!/usr/bin/env python3
"""HSG Intermediate — Module 18: hsgi-contests (mock contest series).

Six graded contest problems across three 120-minute mock competitions
(two problems each), mixing the intermediate toolkit: two-pass arrays,
stacks, monotonic deques, exchange-argument scheduling, DP, and DSU.
Every W is the classic wrong-near-miss for its problem (one-sided wall,
pair counting instead of contiguous, start-sorted scheduling, greedy
steps, parent overwrite without find).

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

M = "hsgi-contests"

write_module(
    M,
    "Intermediate Contest Series",
    "Three mock contests (two problems each) mixing every intermediate tool — time management and problem selection are graded skills too.",
    "Chuỗi kỳ thi trình độ trung cấp",
    "Ba kỳ thi giả lập (mỗi kỳ hai bài) trộn mọi công cụ trung cấp — quản lý thời gian và chọn bài cũng là kỹ năng bị chấm.",
    ["hsgi-m18-strategy", "hsgi-m18-manage", "hsgi-cp-m18a", "hsgi-cp-m18b",
     "hsgi-cp-m18c", "hsgi-cp-m18d"],
    ["hsgi-p18-mixed"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m18-strategy",
    "Contest Strategy — Scan, Rank, Secure",
    "The first 15 minutes decide the contest: read everything, rank by expected solving time, secure the easiest first.",
    20,
    """## 15 phút đầu

**Đọc TOÀN BỘ đề trước khi code bài nào.** Ghi lại cho mỗi bài: kỹ
thuật đoán được, ràng buộc lớn nhất, ước lượng thời gian. Điểm HSG
đến từ TỔNG điểm, không phải số bài giải đẹp.

**Thứ tự gợi ý:** bài dễ nhất theo ƯỚC LƯỢNG RIÊNG CỦA BẠN (không
phải số thứ tự). Bài dễ = kỹ thuật bạn cài đúng ngay + test biên rõ.

## Phân bổ thời gian (kỳ 120 phút, 2–3 bài)

- 15': đọc + xếp hạng.
- Xếp hạng 1: giải trong 20–25'. Nếu vượt 40' → dừng, ghi subtask
  brute force (điểm một phần), chuyển bài.
- Xếp hạng 2: 40'. Giữa kỳ: quay lại bài 1 nếu có ý mới.
- 20' cuối: kiểm tra Overflow, biên, định dạng in — KHÔNG bắt đầu
  bài mới lúc này trừ khi chắc chắn.

## Điểm một phần (subtask)

Trước khi code: kiểm tra giới hạn con. n ≤ 1000 giải được bằng
O(n^2)? Viết luôn bản O(n^2) chắc chắn trước, tối ưu sau nếu còn
thời gian — điểm con là điểm THẬT.

**Điểm mấu chốt:** tổng điểm tối đa hóa bằng thứ tự giải + điểm con,
không bằng độ khó bài giải đẹp nhất.""",
    "Chiến lược thi — Đọc, xếp hạng, chốt",
    "15 phút đầu quyết định kỳ thi: đọc hết, xếp theo thời gian dự kiến, chốt bài dễ nhất trước.",
    """## 15 phút đầu

Đọc TOÀN BỘ đề trước khi code. Ghi cho mỗi bài: kỹ thuật đoán được,
ràng buộc lớn nhất, ước lượng thời gian. Điểm HSG là TỔNG điểm.

Thứ tự theo ước lượng của chính bạn. Bài dễ = cài đúng ngay + test
biên rõ.

## Phân bổ (120 phút)

15' đọc + xếp hạng → 20–25' bài 1 (quá 40' thì ghi subtask brute
force và chuyển) → 40' bài 2 → 20' cuối rà soát overflow/biên/định
dạng, không mở bài mới.

## Điểm một phần

Kiểm tra subtask trước khi code: n nhỏ giải được O(n^2) → chốt bản
đó trước, tối ưu sau. Điểm con là điểm thật.

**Điểm mấu chốt:** tối đa hóa tổng điểm bằng thứ tự giải + subtask.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m18-manage",
    "Time Management — When to Abandon a Problem",
    "Sunk cost is the contest killer: the schedule, not pride, decides when to switch.",
    20,
    """## Quy tắc chuyển bài

Đặt ngân sách thời gian TRƯỚC khi bắt đầu code. Hết ngân sách mà
chưa có bản chắc chắn pass ví dụ → viết bản brute force cho phần
nhỏ nhất, nộp để chốt điểm con, chuyển bài. Trở lại sau nếu còn
thời gian.

## Dấu hiệu bạn đang sa lầy

- Debug cùng một mẫu > 15 phút mà không có giả thuyết mới → code
  sai cấu trúc, viết lại nhanh hơn sửa.
- Chưa đọc đề các bài khác trong 45 phút → điểm bỏ lỡ lớn hơn lợi
  ích của bài hiện tại.
- "Sắp xong rồi" ba lần liên tiếp — đo bằng test đã pass, không
  phải cảm giác.

## Sức mạnh của bản chắc chắn

Một bản O(n^2) chắc chắn đúng ăn subtask 1–2 luôn nhanh hơn bản
O(n log n) chưa chạy được lần nào. Nộp sớm bản chắc chắn, rồi mới
tối ưu — chấm lấy kết quả nộp CUỐI (nếu judge chấm bài cuối) hoặc
điểm cao nhất (kiểm tra luật thi cụ thể — đọc THẬT kỹ quy định).

## Sau kỳ thi

Đọc lời giải mọi bài không giải được — kỹ thuật trong đề sẽ quay
lại ở kỳ sau. Ghi lại loại lỗi của chính mình (đọc đề? biên?
phức tạp?) để sửa quy trình, không chỉ sửa bài.

**Điểm mấu chốt:** ngân sách trước, nộp chắc chắn sớm, đọc lại đề
các bài bỏ lỡ.""",
    "Quản lý thời gian — Khi nào bỏ bài",
    "Chi phí chìm là sát thủ kỳ thi: lịch trình chứ không tự ái quyết định lúc chuyển bài.",
    """## Quy tắc chuyển bài

Hết ngân sách (đặt trước khi code) mà chưa có bản chắc chắn pass ví
dụ → viết brute force chốt điểm con, chuyển bài, quay lại sau.

## Dấu hiệu sa lầy

Cùng một lỗi debug > 15 phút không có giả thuyết mới → viết lại.
45 phút không đọc đề bài khác → mất điểm nhiều hơn lợi ích bài này.
Đo bằng TEST đã pass, không phải cảm giác "sắp xong".

## Sức mạnh của bản chắc chắn

Bản O(n^2) đúng ăn subtask 1–2 nhanh hơn bản O(n log n) chưa chạy
được. Đọc kỹ luật chấm của kỳ thi thật (bài cuối hay điểm cao nhất).

## Sau kỳ thi

Đọc lời giải mọi bài bỏ lỡ — kỹ thuật sẽ quay lại. Ghi loại lỗi của
chính mình để sửa quy trình.

**Điểm mấu chốt:** ngân sách trước, nộp chắc chắn sớm, học từ bài
bỏ lỡ.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
C1A = challenge(
    "hsgi-p18-rain",
    "Mưa giữ nước",
    """**Bài toán.** Trục x có n cột, cột i cao a[i] (phần tử 0 là cột thấp,
có thể bằng 0). Sau cơn mưa, nước đọng giữa các cột. In TỔNG LƯỢNG
NƯỚC (đơn vị ô 1×1).

Tại mỗi vị trí: mức nước = min(max bên trái, max bên phải) − a[i]
(không âm). Hai mảng max tiền tố/hậu tố, một lượt cộng.

**Ràng buộc:** 1 ≤ n ≤ 2·10^5; 0 ≤ a[i] ≤ 10^9. Tổng tới ~10^14 —
long long.

Cái bẫy kinh điển: tính nước chỉ theo BƯỨC TƯỜNG TRÁI (bỏ tường phải)
— sai mọi thung lũng lệch phải.""",
    [
        contest_test(
            "kinh điển",
            T("12", "0 1 0 2 1 0 1 3 2 1 2 1"),
            T("6"),
            "Thung lũng giữa hai tường cao 2 và 3 giữ 5 + vùng 1 ô bên phải.",
        ),
        contest_test(
            "thung lũng lệch",
            T("3", "3 0 2"),
            T("2"),
            "Mức nước min(3, 2) − 0 = 2. Chỉ tường trái sẽ tính 3 — SAI.",
        ),
        contest_test(
            "dốc lên — không giữ nước",
            T("5", "1 2 3 4 5"),
            T("0"),
            "Mọi ô có tường phải bằng chính nó → không nước.",
        ),
        contest_test(
            "hình răng cưa",
            T("5", "2 1 3 0 4"),
            T("4"),
            "Ô 1 giữ 1, ô 3 giữ 3: tổng 4.",
        ),
        contest_test(
            "n lớn — chữ V",
            T("200000") + T(" ".join(str(abs(i - 99999)) for i in range(200000))),
            T("9999800001"),
            "Hai mảng max + tổng long long; naive mỗi ô quét hai phía O(n^2) chết.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

C1B = challenge(
    "hsgi-p18-paren",
    "Dãy ngoặc dài nhất",
    """**Bài toán.** Xâu chỉ gồm '(' và ')' (độ dài ≤ 10^6). In độ dài dãy
ngoặc hợp lệ LIÊN TIẾP dài nhất.

Stack chỉ số: đẩy chỉ số '('; gặp ')' pop — nếu stack rỗng, đẩy chỉ
số này làm "hàng rào"; ngược lại độ dài = i − chỉ số đỉnh stack.
Khởi tạo stack với −1 làm hàng rào gốc.

Cái bẫy kinh điển: đếm SỐ CẶP khớp ở bất kỳ đâu — bỏ điều kiện liên
tiếp (vd "()((" có 2 cặp nhưng dãy liên tiếp dài nhất là 2).""",
    [
        contest_test(
            "ví dụ",
            T("()(()"),
            T("2"),
            "Dãy liên tiếp dài nhất là '()' đầu.",
        ),
        contest_test(
            "kinh điển",
            T(")()())"),
            T("4"),
            "'()()' giữa xâu.",
        ),
        contest_test(
            "lồng sâu",
            T("((()))"),
            T("6"),
            "Cả xâu.",
        ),
        contest_test(
            "hai khối rời",
            T("())(()"),
            T("2"),
            "Hai khối '()' không nối được — liên tiếp bị đứt tại ')('.",
        ),
        contest_test(
            "n lớn",
            T("()" * 100000),
            T("200000"),
            "Cả xâu hợp lệ.",
        ),
        contest_test(
            "n lớn lồng",
            T("(" * 100000 + ")" * 100000),
            T("200000"),
            "Lồng trọn vẹn; stack chỉ số O(n), không đệ quy.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_P18 = {
    "hsgi-p18-rain": vi_challenge(
        "Mưa giữ nước",
        """**Bài toán.** n cột cao a[i]: tổng nước đọng = Σ max(0,
min(maxL, maxR) − a[i]).""",
        [("3 0 2", "2 — min(3, 2) − 0; chỉ tường trái sẽ sai (3)."),
         ("kỹ thuật", "Hai mảng max tiền tố/hậu tố, O(n); long long.")],
    ),
    "hsgi-p18-paren": vi_challenge(
        "Dãy ngoặc dài nhất",
        """**Bài toán.** Độ dài dãy ngoặc hợp lệ LIÊN TIẾP dài nhất.""",
        [(")()())", "4."),
         ("kỹ thuật", "Stack chỉ số với hàng rào −1; đếm cặp bất kỳ là SAI.")],
    ),
}


C2A = challenge(
    "hsgi-p18-winmax",
    "Cửa sổ lớn nhất",
    """**Bài toán.** Mảng n phần tử và cửa sổ k. In GIÁ TRỊ LỚN NHẤT của
mỗi cửa sổ kích thước k trượt từ trái sang phải — mỗi cửa sổ một số,
cách nhau bởi dấu cách, tất cả trên MỘT dòng.

**Ràng buộc:** 1 ≤ k ≤ n ≤ 2·10^5; |a[i]| ≤ 10^9.

Deque đơn điệu giảm: đầu deque là chỉ số lớn nhất hiện hành; phần tử
ra khỏi cửa sổ bị pop đầu, phần tử mới pop đuổi mọi phần tử ≤ nó.
Mỗi phần tử vào/ra deque đúng một lần — O(n). Quét max lại mỗi cửa
sổ là O(n·k) — quá hạn với n = 2·10^5, k lớn.""",
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
    """**Bài toán.** n suất chiếu, suất i bắt đầu s[i] và kết thúc e[i]
(s[i] < e[i]). Chọn số suất lớn nhất để xem sao cho không hai suất
nào chồng nhau (suất bắt đầu đúng lúc suất trước kết thúc vẫn hợp
lệ: s ≥ e_trước). In số suất tối đa.

Luận điểm đổi chỗ: chọn suất KẾT THÚC SỚM NHẤT còn khả dĩ — bất kỳ
nghiệm tối ưu nào đều đổi được sang lựa chọn này không xấu đi. Sort
theo e, quét một lượt.

Cái bẫy kinh điển: sort theo THỜI ĐIỂM BẮT ĐẦU — một suất dài sớm
chiếm slot chặn mọi suất ngắn phía sau.""",
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

VI_P18.update({
    "hsgi-p18-winmax": vi_challenge(
        "Cửa sổ lớn nhất",
        """**Bài toán.** Max mỗi cửa sổ k trượt — in trên một dòng cách bởi
dấu cách.""",
        [("1 3 -1 -3 5 3 6 7, k=3", "3 3 5 5 6 7."),
         ("kỹ thuật", "Deque đơn điệu giảm, O(n); quét lại O(n·k) chết.")],
    ),
    "hsgi-p18-movies": vi_challenge(
        "Xem phim tối đa",
        """**Bài toán.** Chọn nhiều suất không chồng nhất (s ≥ e_trước OK).""",
        [("(1,3),(2,5),(4,7),(1,8),(5,9),(8,10)", "3."),
         ("kỹ thuật", "EDF — sort theo kết thúc; sort theo bắt đầu là bẫy kinh điển.")],
    ),
})

write_practice(
    M,
    "hsgi-p18-mixed",
    "Contest Problem Set",
    "Four flagship contest problems: sliding-window maximum and interval scheduling alongside the contest checkpoints.",
    "Bài tập kỳ thi",
    "Bốn bài thi chủ lực: cửa sổ lớn nhất và xếp lịch khoảng cùng hai bài chấm kỳ thi.",
    "hsgi-m18-manage",
    40,
    "intermediate",
    [C1A, C1B, C2A, C2B],
    VI_P18,
    solutions=[
        (
            "hsgi-p18-rain",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> mxL(n), mxR(n);
    long long m = 0;
    for (int i = 0; i < n; ++i) { m = max(m, a[i]); mxL[i] = m; }
    m = 0;
    for (int i = n - 1; i >= 0; --i) { m = max(m, a[i]); mxR[i] = m; }
    long long total = 0;
    for (int i = 0; i < n; ++i)
        total += max(0LL, min(mxL[i], mxR[i]) - a[i]);
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // near-miss: nước chỉ tính theo TƯỜNG TRÁI (bỏ tường phải) —
    // sai mọi thung lũng lệch phải
    long long m = 0, total = 0;
    for (int i = 0; i < n; ++i) {
        m = max(m, a[i]);
        total += max(0LL, m - a[i]);
    }
    out << total << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p18-paren",
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    // stack chỉ số; phần tử đáy là "hàng rào" (chỉ số trước dãy hợp lệ)
    vector<int> st;
    st.reserve(n + 1);
    st.push_back(-1);
    int best = 0;
    for (int i = 0; i < n; ++i) {
        if (s[i] == '(') st.push_back(i);
        else {
            st.pop_back();
            if (st.empty()) st.push_back(i);
            else best = max(best, i - st.back());
        }
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    // near-miss: đếm SỐ CẶP khớp ở bất kỳ đâu — bỏ điều kiện LIÊN TIẾP
    int d = 0, c = 0;
    for (char ch : s) {
        if (ch == '(') ++d;
        else if (d > 0) { --d; c += 2; }
    }
    out << c << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p18-winmax",
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    // deque đơn điệu GIẢM chỉ số; đầu deque = max cửa sổ hiện hành
    deque<int> dq;
    bool first = true;
    for (int i = 0; i < n; ++i) {
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();
        if (i >= k - 1) {
            if (!first) out << " ";
            out << a[dq.front()];
            first = false;
        }
    }
    out << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    // near-miss: QUÊN pop chỉ số hết hạn ở đầu deque — max cũ "kẹt"
    // trong deque và được báo sai sau khi rời cửa sổ
    deque<int> dq;
    bool first = true;
    for (int i = 0; i < n; ++i) {
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) {
            if (!first) out << " ";
            out << a[dq.front()];
            first = false;
        }
    }
    out << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p18-movies",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& [s, e] : v) in >> s >> e;
    sort(v.begin(), v.end(), [](const auto& x, const auto& y) {
        return x.second < y.second;               // EDF: kết thúc sớm trước
    });
    long long last = -1;
    int c = 0;
    for (auto& [s, e] : v) {
        if (s >= last) { ++c; last = e; }
    }
    out << c << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& [s, e] : v) in >> s >> e;
    // near-miss: sort theo THỜI ĐIỂM BẮT ĐẦU — suất dài sớm chặn slot
    sort(v.begin(), v.end());
    long long last = -1;
    int c = 0;
    for (auto& [s, e] : v) {
        if (s >= last) { ++c; last = e; }
    }
    out << c << "{{NL}}";
""") + END,
        ),
    ],
)

# ------------------------------------------------------------------ contest 2 checkpoints
C3A = challenge(
    "hsgi-cp18-stair",
    "Cầu thang phí tối thiểu",
    """**Bài toán.** Cầu thang n bậc, bậc i có phí c[i]. Bắt đầu TẠI SÀN
(bậc 0 ảo, phí 0); mỗi bước đi lên 1 hoặc 2 bậc và TRẢ PHÍ bậc hạ
xuống. Đứng trên bậc n (trên cùng bậc n) là đích — không trả phí bậc
n. In tổng phí nhỏ nhất.

dp[i] = c[i] + min(dp[i−1], dp[i−2]); dp[−1] = dp[0] = 0 (sàn).
Đáp án = min(dp[n−1], dp[n−2]).

Cái bẫy: tham lam "bước nào rẻ hơn bước đó" — quyết định cục bộ bỏ
qua phí các bậc sau.""",
    [
        contest_test(
            "ví dụ",
            T("3", "10 15 20"),
            T("15"),
            "Bậc 1 rồi nhảy 2 bậc: 15 + 0 = 15.",
        ),
        contest_test(
            "bẫy tham lam",
            T("10", "1 100 1 1 1 100 1 1 100 1"),
            T("6"),
            "1+1+1+1+1+1 = 6 qua bậc lẻ; tham lam nhảy 2 bậc dính bậc 100.",
        ),
        contest_test(
            "hai bậc",
            T("2", "5 1"),
            T("1"),
            "Nhảy thẳng bậc 2.",
        ),
        contest_test(
            "n lớn",
            T("200000") + T(" ".join(str((i * 13) % 201 + 1) for i in range(200000))),
            T("9507280"),
            "DP một lượt O(n); đệ quy không ghi nhớ O(2^n) chết.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CP18A = vi_challenge(
    "Cầu thang phí tối thiểu",
    """**Bài toán.** Bắt đầu tại sàn; bước 1/2 bậc, trả phí bậc chạm; đứng
trên bậc n không trả phí bậc n.""",
    [("10 15 20", "15 (bậc 1 rồi nhảy qua)."),
     ("kỹ thuật", "dp[i] = c[i] + min(dp[i−1], dp[i−2]); đáp án min hai bậc cuối.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m18a",
    "Contest 2-A: Cầu thang phí",
    "Mock contest 2, problem A: min-cost climbing DP. Target: solved within 25 minutes.",
    25,
    """**Contest 2-A — Cầu thang phí.** DP một chiều. Near-miss bị chấm:
tham lam theo bước rẻ nhất cục bộ.

**Contest 2-A.** Min-cost climbing stairs: dp[i] = c[i] + min of the
two previous; answer is min of the last two states. Graded near-miss:
per-step greedy.

**Contest 2-A — Cầu thang phí.** DP một chiều: dp[i] = c[i] +
min(dp[i−1], dp[i−2]); đáp án min hai trạng thái cuối. Near-miss bị
chấm: tham lam theo bước rẻ nhất cục bộ.""",
    "Contest 2-A: Cầu thang phí",
    "Mock contest 2, problem A: min-cost climbing DP. Target: solved within 25 minutes.",
    """**Contest 2-A — Cầu thang phí.** DP một chiều: dp[i] = c[i] +
min(dp[i−1], dp[i−2]); đáp án min hai bậc cuối. Tham lam từng bước
là lỗi bị săn.""",
    C3A,
    VI_CP18A,
    solution=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> c(n);
    for (auto& x : c) in >> x;
    // dp0 = chi phí đứng trên bậc i−2, dp1 = bậc i−1; sàn = 0
    long long dp0 = 0, dp1 = 0;
    for (int i = 0; i < n; ++i) {
        long long nd = min(dp0, dp1) + c[i];
        dp0 = dp1;
        dp1 = nd;
    }
    out << min(dp0, dp1) << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> c(n);
    for (auto& x : c) in >> x;
    // near-miss: tham lam — tại mỗi vị trí bước lên bậc "rẻ hơn" kế
    // tiếp; quyết định cục bộ bỏ qua phí các bậc sau
    long long total = 0;
    int i = -1;
    while (i < n - 1) {
        long long one = (i + 1 < n) ? c[i + 1] : 0;
        long long two = (i + 2 < n) ? c[i + 2] : 0;
        if (i + 2 < n && two <= one) i += 2;
        else i += 1;
        total += c[i];
    }
    out << total << "{{NL}}";
""") + END,
)

C3B = challenge(
    "hsgi-cp18-town",
    "Phường thị — đếm khu",
    """**Bài toán.** Phố có n tòa nhà đánh số 1..n; m con phố hai chiều
nối các cặp. Hai tòa thuộc cùng MỘT KHU nếu đi được với nhau qua
các con phố (trực tiếp hoặc gián tiếp). In số khu.

DSU với find nén đường: mỗi con phố union hai đầu; số khu = số gốc
khác nhau. Lỗi kinh điển: gán trực tiếp cha (p[b] = a) không qua
find — chuỗi phố dài khiến tòa cuối không bao giờ nối vào khu của
tòa đầu.""",
    [
        contest_test(
            "ví dụ",
            T("6 3", "1 2", "3 4", "2 3"),
            T("3"),
            "Khu {1,2,3,4}, khu {5}, khu {6}.",
        ),
        contest_test(
            "một tòa, không phố",
            T("1 0"),
            T("1"),
            "Biên nhỏ nhất.",
        ),
        contest_test(
            "chuỗi dài",
            T("5 4", "1 2", "2 3", "3 4", "4 5"),
            T("1"),
            "Toàn phố nối liền — kiểm tra union qua find (p[b]=a là SAI).",
        ),
        contest_test(
            "n lớn — chuỗi 199999 phố",
            T("200000 199999") + T(" ".join(str(i) + " " + str(i + 1) for i in range(1, 200000))),
            T("1"),
            "Một khu trọn; find nén đường O(α); gán thẳng sai + chậm.",
        ),
        contest_test(
            "không phố nào — n khu",
            T("100000 0"),
            T("100000"),
            "Mỗi tòa một khu.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CP18B = vi_challenge(
    "Phường thị — đếm khu",
    """**Bài toán.** n tòa, m phố hai chiều: in số thành phần liên thông.""",
    [("6 3: (1,2),(3,4),(2,3)", "3."),
     ("kỹ thuật", "DSU find nén đường; gán p[b]=a trực tiếp là lỗi kinh điển.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m18b",
    "Contest 2-B: Phường thị",
    "Mock contest 2, problem B: connected components with DSU. Target: solved within 25 minutes.",
    25,
    """**Contest 2-B — Phường thị.** DSU đếm thành phần liên thông.
Near-miss bị chấm: gán cha trực tiếp không qua find.

**Contest 2-B.** Counting connected components via union-find with
path compression. Graded near-miss: raw parent assignment without
find.

**Contest 2-B — Phường thị.** DSU đếm thành phần liên thông với find
nén đường; union hai GỐC. Near-miss bị chấm: gán cha trực tiếp
p[b] = a không qua find.""",
    "Contest 2-B: Phường thị",
    "Mock contest 2, problem B: connected components with DSU. Target: solved within 25 minutes.",
    """**Contest 2-B — Phường thị.** DSU đếm thành phần liên thông; union
hai gốc qua find nén đường. Gán cha trực tiếp là lỗi bị săn.""",
    C3B,
    VI_CP18B,
    solution=CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<int> p(n + 1);
    for (int i = 1; i <= n; ++i) p[i] = i;
    auto find = [&](int x) {
        while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; }
        return x;
    };
    for (int i = 0; i < m; ++i) {
        int a, b; in >> a >> b;
        p[find(a)] = find(b);
    }
    int comps = 0;
    for (int i = 1; i <= n; ++i)
        if (find(i) == i) ++comps;
    out << comps << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<int> p(n + 1);
    for (int i = 1; i <= n; ++i) p[i] = i;
    // near-miss: gán cha TRỰC TIẾP p[b] = a rồi đếm số tòa BỊ GÁN CHA
    // (p[i] != i) thay vì đếm GỐC (p[i] == i) — mỗi khu bị đếm theo
    // số cạnh, không phải số khu; sai trên mọi khu có chuỗi ≥ 1
    for (int i = 0; i < m; ++i) {
        int a, b; in >> a >> b;
        p[b] = a;
    }
    int comps = 0;
    for (int i = 1; i <= n; ++i)
        if (p[i] != i) ++comps;
    out << comps << "{{NL}}";
""") + END,
)

# ------------------------------------------------------------------ contest 3 checkpoints
C4A = challenge(
    "hsgi-cp18-rain",
    "Chốt 3-A: Mưa giữ nước",
    """**Bài toán.** Như bài Mưa giữ nước đã luyện: n cột cao a[i], in tổng
nước đọng giữa các cột.

maxL[i] = max tiền tố, maxR[i] = max hậu tố; nước tại i =
max(0, min(maxL, maxR) − a[i]); tổng long long. Bản một biến chỉ
theo tường trái là lỗi bị chấm — thung lũng lệch phải bắt nó.""",
    [
        contest_test(
            "kinh điển",
            T("12", "0 1 0 2 1 0 1 3 2 1 2 1"),
            T("6"),
            "Thung lũng giữa hai tường cao 2 và 3.",
        ),
        contest_test(
            "thung lũng lệch phải",
            T("3", "3 0 2"),
            T("2"),
            "min(3, 2) − 0 = 2 — bản một tường tính 3, SAI.",
        ),
        contest_test(
            "n lớn — chữ V",
            T("200000") + T(" ".join(str(abs(i - 99999)) for i in range(200000))),
            T("9999800001"),
            "Hai mảng max + long long.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CP18C = vi_challenge(
    "Chốt 3-A: Mưa giữ nước",
    """**Bài toán.** Tổng nước đọng giữa các cột = Σ max(0, min(maxL,
maxR) − a[i]).""",
    [("3 0 2", "2."),
     ("kỹ thuật", "Hai mảng max; bản một tường trái là lỗi bị chấm.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m18c",
    "Contest 3-A: Mưa giữ nước",
    "Mock contest 3, problem A: two-pass prefix/suffix maxima. Target: solved within 25 minutes.",
    25,
    """**Contest 3-A — Mưa giữ nước.** Hai mảng max tiền tố/hậu tố.
Near-miss bị chấm: chỉ tường trái.

**Contest 3-A.** Trapping rain water via prefix/suffix maxima arrays.
Graded near-miss: left-wall-only accumulation.

**Contest 3-A — Mưa giữ nước.** Hai mảng max tiền tố/hậu tố, một lượt
cộng. Near-miss bị chấm: tích nước chỉ theo tường trái.""",
    "Contest 3-A: Mưa giữ nước",
    "Mock contest 3, problem A: two-pass prefix/suffix maxima. Target: solved within 25 minutes.",
    """**Contest 3-A — Mưa giữ nước.** Hai mảng max tiền tố/hậu tố. Near-miss
bị chấm: chỉ tường trái.""",
    C4A,
    VI_CP18C,
    solution=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> mxL(n), mxR(n);
    long long m = 0;
    for (int i = 0; i < n; ++i) { m = max(m, a[i]); mxL[i] = m; }
    m = 0;
    for (int i = n - 1; i >= 0; --i) { m = max(m, a[i]); mxR[i] = m; }
    long long total = 0;
    for (int i = 0; i < n; ++i)
        total += max(0LL, min(mxL[i], mxR[i]) - a[i]);
    out << total << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // near-miss: nước chỉ tính theo TƯỜNG TRÁI — bỏ tường phải
    long long m = 0, total = 0;
    for (int i = 0; i < n; ++i) {
        m = max(m, a[i]);
        total += max(0LL, m - a[i]);
    }
    out << total << "{{NL}}";
""") + END,
)

C4B = challenge(
    "hsgi-cp18-balanced",
    "Chốt 3-B: Ngày thi cân bằng",
    """**Bài toán.** Như bài Dãy ngoặc: xâu '(' ')' độ dài ≤ 10^6, in độ
 dài dãy hợp lệ liên tiếp dài nhất.

Stack chỉ số với hàng rào: khởi tạo −1; '(' đẩy chỉ số; ')' pop —
rỗng thì đẩy hàng rào mới, không thì độ dài i − đỉnh. Đếm cặp bất kỳ
bỏ điều kiện liên tiếp là lỗi bị chấm (vd "()((" đếm 4 nhưng đáp án 2).""",
    [
        contest_test(
            "ví dụ",
            T("()(()"),
            T("2"),
            "Dãy liên tiếp dài nhất '()' đầu.",
        ),
        contest_test(
            "kinh điển",
            T(")()())"),
            T("4"),
            "'()()' giữa xâu.",
        ),
        contest_test(
            "n lớn lồng",
            T("(" * 100000 + ")" * 100000),
            T("200000"),
            "Lồng trọn — stack chỉ số O(n).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

VI_CP18D = vi_challenge(
    "Chốt 3-B: Ngày thi cân bằng",
    """**Bài toán.** Độ dài dãy ngoặc hợp lệ liên tiếp dài nhất.""",
    [("()((", "2 — đếm cặp bất kỳ sẽ sai thành 4."),
     ("kỹ thuật", "Stack chỉ số với hàng rào −1.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m18d",
    "Contest 3-B: Ngày thi cân bằng",
    "Mock contest 3, problem B: index-stack longest valid parentheses. Target: solved within 25 minutes.",
    25,
    """**Contest 3-B — Ngày thi cân bằng.** Stack chỉ số với hàng rào.
Near-miss bị chấm: đếm cặp bất kỳ bỏ liên tiếp.

**Contest 3-B.** Longest valid parentheses via an index stack with a
sentinel. Graded near-miss: counting matched pairs anywhere.

**Contest 3-B — Ngày thi cân bằng.** Stack chỉ số, hàng rào −1; độ
dài = i − đỉnh sau pop. Near-miss bị chấm: đếm cặp khớp bất kỳ bỏ
điều kiện liên tiếp.""",
    "Contest 3-B: Ngày thi cân bằng",
    "Mock contest 3, problem B: index-stack longest valid parentheses. Target: solved within 25 minutes.",
    """**Contest 3-B — Ngày thi cân bằng.** Stack chỉ số với hàng rào −1.
Đếm cặp bỏ liên tiếp là lỗi bị săn.""",
    C4B,
    VI_CP18D,
    solution=CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    vector<int> st;
    st.reserve(n + 1);
    st.push_back(-1);
    int best = 0;
    for (int i = 0; i < n; ++i) {
        if (s[i] == '(') st.push_back(i);
        else {
            st.pop_back();
            if (st.empty()) st.push_back(i);
            else best = max(best, i - st.back());
        }
    }
    out << best << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    string s; in >> s;
    // near-miss: đếm số cặp khớp ở bất kỳ đâu — bỏ điều kiện liên tiếp
    int d = 0, c = 0;
    for (char ch : s) {
        if (ch == '(') ++d;
        else if (d > 0) { --d; c += 2; }
    }
    out << c << "{{NL}}";
""") + END,
)
