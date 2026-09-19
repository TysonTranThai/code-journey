#!/usr/bin/env python3
"""HSG Intermediate — Module 12: hsgi-knap (Knapsack & Coin Problems).

0/1 knapsack with the 1D reverse loop, unbounded coin problems with the
forward loop, subset counting, exact-fill variants. The teaching spine:
the direction of the weight loop IS the item-reuse policy.

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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-knap"
write_module(
    M,
    "Knapsack — 0/1, Unbounded, Counting",
    "One array, two loop directions: reverse weight loop for 0/1 (each item once), forward for unbounded (reuse allowed). The direction is the policy.",
    "Balo — 0/1, không giới hạn, đếm",
    "Một mảng, hai chiều duyệt: ngược cho 0/1 (mỗi món một lần), xuôi cho không giới hạn (được dùng lại). Chiều duyệt là chính sách.",
    ["hsgi-m12-knapsack", "hsgi-m12-counting", "hsgi-cp-m12"],
    ["hsgi-p12-knap"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m12-knapsack",
    "The Reverse Loop Is the Policy",
    "2D knapsack compressed to 1D by iterating weights DOWNWARD for 0/1 and UPWARD for unbounded reuse.",
    20,
    """## 0/1 knapsack — bảng đầy đủ

n món, món i (w_i, v_i), balo sức chứa W. dp[j] = giá trị lớn nhất với
sức chứa j. Bảng 2D: dp[i][j] = max(dp[i-1][j], dp[i-1][j-w_i] + v_i) —
hàng i chỉ đọc hàng i−1 → cuộn một mảng, nhưng PHẢI duyệt j TỪ LỚN VỀ
NHỎ:

```cpp
vector<long long> dp(W + 1, 0);
for (int i = 0; i < n; ++i)
    for (int j = W; j >= w[i]; --j)          // NGƯỢC
        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
```

### Vì sao ngược

Duyệt ngược: khi tính dp[j], dp[j − w_i] vẫn là giá trị HÀNG TRƯỚC
(chưa đụng tới món i) → món i dùng MỘT lần. Duyệt xuôi: dp[j − w_i]
có thể vừa được cập nhật bằng món i → món i được dùng LẠI — chính là
bài không giới hạn!

### Không giới hạn — xuôi

Đổi tiền: đồng xu kiểu k (w_k), cần tổng S. Xuôi duyệt:

```cpp
vector<int> dp(S + 1, INF); dp[0] = 0;
for (int k = 0; k < K; ++k)
    for (int s = w[k]; s <= S; ++s)          // XUÔI — dùng lại được
        if (dp[s - w[k]] + 1 < dp[s]) dp[s] = dp[s - w[k]] + 1;
```

### Một mảng, hai chính sách

- 0/1: NGƯỢC — mỗi món một lần.
- Unbounded: XUÔI — dùng vô hạn.
Đây là lỗi sinh viên lặp lại nhiều nhất trong contest: chép khung balo
0/1 rồi để vòng xuôi → kết quả phình to âm thầm trên test lớn.

### Bộ nhớ và thời gian

O(n·W) thời gian; O(W) bộ nhớ. n = 3000, W = 8000 → 24 triệu phép
tính: thoải mái. W tới 10^9 → KHÔNG dùng balo thường (đổi hướng: balo
trên GIÁ TRỊ, hoặc greedy có chứng minh).

**Điểm mấu chốt:** chiều duyệt là chính sách tái sử dụng; nhớ bằng
câu "ngược một lần, xuôi vô hạn".""",
    "Vòng ngược là chính sách",
    "Balo 2D nén thành 1D: duyệt trọng số XUỐNG cho 0/1, XUÔI cho dùng lại.",
    """## Balo 0/1 — bảng đầy đủ

n món (w_i, v_i), sức chứa W. Bảng 2D nén một mảng, duyệt j TỪ LỚN
XUỐNG:

```cpp
vector<long long> dp(W + 1, 0);
for (int i = 0; i < n; ++i)
    for (int j = W; j >= w[i]; --j)          // NGƯỢC
        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
```

### Vì sao ngược

Khi tính dp[j], dp[j − w_i] còn là giá trị HÀNG TRƯỚC (chưa đụng món
i) → mỗi món MỘT lần. Duyệt xuôi: dp[j − w_i] vừa cập nhật bằng món i
→ món dùng LẠI — bài không giới hạn!

### Không giới hạn — xuôi

Đổi tiền kiểu k, tổng S:

```cpp
vector<int> dp(S + 1, INF); dp[0] = 0;
for (int k = 0; k < K; ++k)
    for (int s = w[k]; s <= S; ++s)          // XUÔI
        if (dp[s - w[k]] + 1 < dp[s]) dp[s] = dp[s - w[k]] + 1;
```

### Một mảng, hai chính sách

- 0/1: NGƯỢC — mỗi món một lần.
- Unbounded: XUÔI — vô hạn.
Lỗi contest kinh điển: khung 0/1 nhưng vòng xuôi → kết quả phình âm
thầm trên test lớn.

### Bộ nhớ và thời gian

O(n·W) thời gian, O(W) bộ nhớ. n = 3000, W = 8000 → 24 triệu phép:
thoải mái. W tới 10^9 → KHÔNG dùng balo thường.

**Điểm mấu chốt:** "ngược một lần, xuôi vô hạn".""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m12-counting",
    "Counting Variants — Subsets and Exact Fill",
    "Same tables, counts instead of maxima: add instead of max, and watch the modulus; exact fill means the rest of the table stays at zero/INF.",
    18,
    """## Đếm tập con có tổng T

dp[s] = số tập con có tổng s. Mỗi món một lần → NGƯỢC, và phép hợp
thay max là CỘNG:

```cpp
vector<long long> dp(T + 1, 0);
dp[0] = 1;
for (int i = 0; i < n; ++i)
    for (int s = T; s >= a[i]; --s)
        dp[s] = (dp[s] + dp[s - a[i]]) % MOD;
```

dp[0] = 1 là "tập rỗng" — quên nó làm mọi kết quả lệch đúng một lớp.
Xuôi vòng → đếm "dùng lại" — kết quả phình: test phân biệt phải có
phần tử lặp lại nhỏ.

## Chia đôi mảng

Tổng S; hỏi tách thành hai nửa BẰNG NHAU ⇔ tồn tại tập con tổng S/2.
S lẻ → NO ngay (không cần DP). Sẵn sàng boolean dp[0..S/2]:

```cpp
vector<char> dp(half + 1, 0);
dp[0] = 1;
for (int i = 0; i < n; ++i)
    for (int s = half; s >= a[i]; --s)
        if (dp[s - a[i]]) dp[s] = 1;
```

## Lấp ĐÚNG sức chứa

Variant khó hơn max-thường: chọn món sao cho TỔNG TRỌNG LƯỢNG ĐÚNG
BẰNG W (không thừa không thiếu), tối đa giá trị; không được → in −1.
dp[j] = giá trị tốt nhất đạt TỔNG ĐÚNG j; khởi tạo −INF, dp[0] = 0:

```cpp
const long long NEG = -(1LL << 60);
vector<long long> dp(W + 1, NEG);
dp[0] = 0;
for (int i = 0; i < n; ++i)
    for (int j = W; j >= w[i]; --j)
        if (dp[j - w[i]] != NEG)
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
if (dp[W] < 0) out << -1;
```

Khác biệt so với balo thường: những j không đạt ĐÚNG giữ −INF, không
bao giờ góp vào kết quả. W "bal ≤ thường" sẽ in giá trị balo bình
thường — sai khi lấp không đầy.

## Nhận diện

- "số cách" → cộng, mô-đun, cẩn thận dp[0] = 1.
- "tách hai nửa" → subset-sum về S/2.
- "đúng sức chứa / đúng tổng" → nền −INF thay vì 0.

**Điểm mấu chốt:** đếm = max đổi thành cộng (mô-đun!); exact = −INF
nền; mọi variant vẫn còn chiềuu duyệt quyết định tái sử dụng.""",
    "Các biến thể đếm — tập con và lấp đúng",
    "Đếm tập con tổng T (cộng, mô-đun), chia đôi mảng, và lấp ĐÚNG sức chứa bằng nền −INF.",
    """## Đếm tập con có tổng T

dp[s] = số tập con tổng s. NGƯỢC, max đổi CỘNG:

```cpp
vector<long long> dp(T + 1, 0);
dp[0] = 1;
for (int i = 0; i < n; ++i)
    for (int s = T; s >= a[i]; --s)
        dp[s] = (dp[s] + dp[s - a[i]]) % MOD;
```

dp[0] = 1 là tập rỗng — quên nó lệch cả bảng. Xuôi vòng → đếm "dùng
lại" — kết quả phình.

## Chia đôi mảng

Tổng S; tách hai nửa bằng nhau ⇔ tập con tổng S/2. S lẻ → NO ngay.
Boolean dp[0..S/2] như trên.

## Lấp ĐÚNG sức chứa

Tổng trọng lượng ĐÚNG BẰNG W, tối đa giá trị; không được → −1. Nền
−INF thay vì 0:

```cpp
const long long NEG = -(1LL << 60);
vector<long long> dp(W + 1, NEG);
dp[0] = 0;
for (int i = 0; i < n; ++i)
    for (int j = W; j >= w[i]; --j)
        if (dp[j - w[i]] != NEG)
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
if (dp[W] < 0) out << -1;
```

j không đạt ĐÚNG giữ −INF, không góp kết quả. Balo thường (nền 0) sẽ
in giá trị balo bình thường — sai khi lấp không đầy.

## Nhận diện

- "số cách" → cộng + mô-đun + dp[0] = 1.
- "tách hai nửa" → subset-sum S/2.
- "đúng sức" → nền −INF.

**Điểm mấu chốt:** đếm = cộng; exact = −INF; chiều duyệt vẫn là
chính sách.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p12-knapsack",
    "Balo phá kho",
    """**Bài toán.** n món (w_i, v_i), balo sức chứa W. Chọn mỗi món NHIỀU
NHẤT MỘT LẦN, tổng trọng ≤ W, giá trị lớn nhất. In giá trị.

**Ràng buộc:** 1 ≤ n ≤ 3000; 1 ≤ W ≤ 8000; 1 ≤ w_i ≤ W; 1 ≤ v_i ≤ 10^9.""",
    [
        contest_test(
            "ví dụ",
            T("4 10", "7 49", "6 48", "5 35", "5 35"),
            T("70"),
            "Hai món 5: 35+35 = 70 — tham lam theo tỉ lệ chọn món 6 đứng im.",
        ),
        contest_test(
            "một món",
            T("1 5", "4 9"),
            T("9"),
            "Vừa sức: chọn luôn.",
        ),
        contest_test(
            "không vừa món nào",
            T("2 3", "4 9", "5 10"),
            T("0"),
            "Chọn rỗng: 0 — không âm.",
        ),
        contest_test(
            "n lớn — W lớn",
            T("3000 8000") + T(*[(str(3 + (i % 40)) + " " + str(10 + i)) for i in range(3000)]),
            T("1640274"),
            "O(n·W) 24 triệu phép — 1D ngược; W tham-lam-tỉ-lệ sẽ gom sai hỗn hợp.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p12-coinmin",
    "Đổi tiền ít xu nhất",
    """**Bài toán.** K loại xu mệnh giá c_k (DÙNG VÔ HẠN LẦN). Tổng đúng S,
ít xu nhất; không đổi được → in −1.

**Ràng buộc:** 1 ≤ K ≤ 100; 1 ≤ S ≤ 100000; 1 ≤ c_k ≤ S.""",
    [
        contest_test(
            "ví dụ — tham lam gãy",
            T("2 6", "3 4"),
            T("2"),
            "3+3 = 2 xu; tham-lam-lớn-nhất chọn 4 trước, phần dư 2 không đổi được → trả −1 sai.",
        ),
        contest_test(
            "một xu khớp",
            T("2 5", "5 3"),
            T("1"),
            "Mệnh giá 5 cho S = 5.",
        ),
        contest_test(
            "không đổi được",
            T("2 3", "5 7"),
            T("-1"),
            "Mọi tổng từ 5,7 > 3: vô nghiệm.",
        ),
        contest_test(
            "S lớn — xu 1",
            T("1 100000", "1"),
            T("100000"),
            "Chỉ xu 1: 100000 xu — O(K·S) một lượt; không được đệ quy mỏi.",
        ),
        contest_test(
            "lẻ — xu 6 và 5",
            T("2 11", "6 5"),
            T("2"),
            "6+5 = 11.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p12-subsetcount",
    "Đếm tập con bằng tổng",
    """**Bài toán.** n số a_i; in số tập con (mỗi phần tử chọn/ không) có
tổng ĐÚNG T, theo mô-đun 10^9 + 7.

**Ràng buộc:** 1 ≤ n ≤ 100; 1 ≤ a_i ≤ 100; 1 ≤ T ≤ 10000.""",
    [
        contest_test(
            "ví dụ — phần tử lặp",
            T("3 3", "1 1 2"),
            T("2"),
            "{1a,2}, {1b,2} = 2 cách ({1a,1b} tổng 2, không tính) — vòng XUÔI sẽ đếm phình dùng lại.",
        ),
        contest_test(
            "một phần tử khớp",
            T("1 4", "4"),
            T("1"),
            "Chọn nó.",
        ),
        contest_test(
            "không đạt",
            T("2 9", "3 4"),
            T("0"),
            "Tổng max 7 < 9.",
        ),
        contest_test(
            "T = 0 ẩn",
            T("3 2", "1 1 1"),
            T("3"),
            "Tổng 2 từ ba số 1: chọn 2 trong 3 — 3 cách.",
        ),
        contest_test(
            "n lớn — toàn 1",
            T("100 50") + T(*["1"] * 100),
            T("538992043"),
            "C(100,50) mô-đun 10^9+7 — kỳ vọng tính bằng comb chính xác.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p12-equal",
    "Chia hai nửa bằng nhau",
    """**Bài toán.** n số; tách thành hai nhóm có tổng BẰNG NHAU? In YES
hoặc NO. (Số 0 nhóm nào cũng được; nhóm có thể rỗng nếu tổng = 0 —
nhưng với a_i ≥ 1 hai nhóm đều khác rỗng.)

**Ràng buộc:** 1 ≤ n ≤ 100; 1 ≤ a_i ≤ 500.""",
    [
        contest_test(
            "ví dụ — tổng lẻ",
            T("3", "1 2 4"),
            T("NO"),
            "Tổng 7 lẻ: NO ngay không cần DP.",
        ),
        contest_test(
            "được",
            T("4", "2 4 3 1"),
            T("YES"),
            "Tổng 10: {4,1} và {2,3}.",
        ),
        contest_test(
            "không được dù chẵn",
            T("3", "1 2 5"),
            T("NO"),
            "Tổng 8, nửa 4: không tập con nào = 4 — vòng XUÔI (dùng lại) sẽ YES do 2+2!",
        ),
        contest_test(
            "một phần tử",
            T("1", "0"),
            T("YES"),
            "Tổng 0: hai nửa rỗng 0 = 0.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p12-exact",
    "Đóng thùng đúng sức",
    """**Bài toán.** n món (w_i, v_i); chọn mỗi món nhiều nhất một lần sao
cho TỔNG TRỌNG LƯỢNG ĐÚNG BẰNG W, giá trị lớn nhất. Không thể → −1.

**Ràng buộc:** 1 ≤ n ≤ 2000; 1 ≤ W ≤ 5000; 1 ≤ w_i ≤ W; 1 ≤ v_i ≤ 10^6.""",
    [
        contest_test(
            "lấp không đầy — balo thường sai",
            T("2 10", "4 5", "7 9"),
            T("-1"),
            "4+7=11 quá, 4, 7 < 10: không lấp đúng — balo thường in 9.",
        ),
        contest_test(
            "được",
            T("3 10", "4 5", "7 9", "6 6"),
            T("11"),
            "4+6 = 10 đúng sức: 5+6 = 11 > 9 (món 7 một mình).",
        ),
        contest_test(
            "một món đúng",
            T("1 5", "5 12"),
            T("12"),
            "Chính nó lấp đầy.",
        ),
        contest_test(
            "W = 0",
            T("2 0", "1 5", "2 7"),
            T("0"),
            "Chọn rỗng: tổng 0 đúng bằng W = 0, giá trị 0.",
        ),
        contest_test(
            "n lớn",
            T("2000 5000") + T(*[(str(2 + (i % 30)) + " " + str(100 + i)) for i in range(2000)]),
            T("912214"),
            "O(n·W) 10 triệu phép — một lượt ngược; lấp đúng sức có thể vô nghiệm trên bộ khác.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI12 = {
    "hsgi-p12-knapsack": vi_challenge(
        "Balo phá kho",
        """**Bài toán.** Balo 0/1: tổng trọng ≤ W, giá trị max. In giá trị.""",
        [("ví dụ", "Hai món 5: 70; tham lam tỉ lệ gãy."),
         ("n lớn", "1D ngược O(n·W) = 24 triệu.")],
    ),
    "hsgi-p12-coinmin": vi_challenge(
        "Đổi tiền ít xu nhất",
        """**Bài toán.** Xu dùng vô hạn; tổng đúng S, ít xu nhất; không được
in −1.""",
        [("ví dụ", "6,5,1 và S=7 → 2; tham lam → 3."),
         ("S lớn", "O(K·S) một lượt.")],
    ),
    "hsgi-p12-subsetcount": vi_challenge(
        "Đếm tập con bằng tổng",
        """**Bài toán.** Số tập con tổng đúng T, mô-đun 10^9 + 7.""",
        [("ví dụ", "1,1,2 và T=3 → 2 cách."),
         ("lặp", "Vòng xuôi đếm phình dùng lại.")],
    ),
    "hsgi-p12-equal": vi_challenge(
        "Chia hai nửa bằng nhau",
        """**Bài toán.** Tách hai nhóm tổng bằng nhau? In YES/NO.""",
        [("lẻ", "Tổng lẻ → NO ngay."),
         ("1,2,5", "Nửa 4 không đạt: NO; vòng xuôi YES sai.")],
    ),
    "hsgi-p12-exact": vi_challenge(
        "Đóng thùng đúng sức",
        """**Bài toán.** Tổng trọng ĐÚNG BẰNG W, giá trị max; không được −1.
Nền −INF.""",
        [("4,5 + 7,9", "Không lấp đủ 10 → −1."),
         ("được", "4+6 → 11."),
         ("W=0", "Chọn rỗng → 0.")],
    ),
}

write_practice(
    M,
    "hsgi-p12-knap",
    "Knapsack Problem Set",
    "Five problems: 0/1 knapsack, min coins unbounded, subset counting, equal partition, exact fill.",
    "Bài tập balo",
    "Năm bài: balo 0/1, đổi tiền ít xu, đếm tập con, chia đôi, lấp đúng sức.",
    "hsgi-m12-counting",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI12,
    solutions=[
        (
            "hsgi-p12-knapsack",
            CPP_STD + cpp("""    int n, W; in >> n >> W;
    vector<int> w(n), v(n);
    for (int i = 0; i < n; ++i) in >> w[i] >> v[i];
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < n; ++i)
        for (int j = W; j >= w[i]; --j)
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    out << dp[W] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, W; in >> n >> W;
    vector<int> w(n), v(n);
    for (int i = 0; i < n; ++i) in >> w[i] >> v[i];
    // near-miss: THAM LAM theo tỉ lệ giá/trọng — chỉ đúng với món "chia
    // được"; ví dụ 6/48 vs 5+5/70 chọn 6 và bị kẹt 4 sức còn lại
    vector<pair<double,int>> order(n);
    for (int i = 0; i < n; ++i)
        order[i] = { (double)v[i] / w[i], i };
    sort(order.rbegin(), order.rend());
    long long val = 0; int cap = W;
    for (auto& [r, i] : order)
        if (w[i] <= cap) { val += v[i]; cap -= w[i]; }
    out << val << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p12-coinmin",
            CPP_STD + cpp("""    int K, S; in >> K >> S;
    vector<int> c(K);
    for (auto& x : c) in >> x;
    const int INF = 1e9;
    vector<int> dp(S + 1, INF);
    dp[0] = 0;
    for (int k = 0; k < K; ++k)
        for (int s = c[k]; s <= S; ++s)          // XUÔI — vô hạn
            if (dp[s - c[k]] + 1 < dp[s]) dp[s] = dp[s - c[k]] + 1;
    out << (dp[S] >= INF ? -1 : dp[S]) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int K, S; in >> K >> S;
    vector<int> c(K);
    for (auto& x : c) in >> x;
    sort(c.rbegin(), c.rend());
    // near-miss: THAM LAM lớn-nhất-trước — 6,5,1 và S=7: 5+1+1 = 3 xu
    // thay vì 6+1 = 2
    int cnt = 0;
    for (int k = 0; k < K; ++k) {
        cnt += S / c[k];
        S %= c[k];
    }
    out << (S > 0 ? -1 : cnt) << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p12-subsetcount",
            CPP_STD + cpp("""    int n, T; in >> n >> T;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    const long long MOD = 1000000007;
    vector<long long> dp(T + 1, 0);
    dp[0] = 1;
    for (int i = 0; i < n; ++i)
        for (int s = T; s >= a[i]; --s)          // NGƯỢC — 0/1
            dp[s] = (dp[s] + dp[s - a[i]]) % MOD;
    out << dp[T] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, T; in >> n >> T;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    const long long MOD = 1000000007;
    vector<long long> dp(T + 1, 0);
    dp[0] = 1;
    // near-miss: vòng XUÔI — mỗi phần tử dùng lại được; 1,1,2 và T=3
    // đếm phình các tổ hợp tái sử dụng
    for (int i = 0; i < n; ++i)
        for (int s = a[i]; s <= T; ++s)
            dp[s] = (dp[s] + dp[s - a[i]]) % MOD;
    out << dp[T] << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p12-equal",
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> a(n);
    int S = 0;
    for (auto& x : a) { in >> x; S += x; }
    if (S % 2 != 0) { out << "NO" << "{{NL}}"; return; }
    int half = S / 2;
    vector<char> dp(half + 1, 0);
    dp[0] = 1;
    for (int i = 0; i < n; ++i)
        for (int s = half; s >= a[i]; --s)
            if (dp[s - a[i]]) dp[s] = 1;
    out << (dp[half] ? "YES" : "NO") << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> a(n);
    int S = 0;
    for (auto& x : a) { in >> x; S += x; }
    if (S % 2 != 0) { out << "NO" << "{{NL}}"; return; }
    int half = S / 2;
    vector<char> dp(half + 1, 0);
    dp[0] = 1;
    // near-miss: vòng XUÔI — phần tử dùng lại; 1,2,5 nửa 4 "đạt" bằng
    // 2+2 (món 2 dùng hai lần) → YES sai
    for (int i = 0; i < n; ++i)
        for (int s = a[i]; s <= half; ++s)
            if (dp[s - a[i]]) dp[s] = 1;
    out << (dp[half] ? "YES" : "NO") << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p12-exact",
            CPP_STD + cpp("""    int n, W; in >> n >> W;
    vector<int> w(n), v(n);
    for (int i = 0; i < n; ++i) in >> w[i] >> v[i];
    const long long NEG = -(1LL << 60);
    vector<long long> dp(W + 1, NEG);
    dp[0] = 0;
    for (int i = 0; i < n; ++i)
        for (int j = W; j >= w[i]; --j)
            if (dp[j - w[i]] != NEG)
                dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    out << (dp[W] < 0 ? -1 : dp[W]) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, W; in >> n >> W;
    vector<int> w(n), v(n);
    for (int i = 0; i < n; ++i) in >> w[i] >> v[i];
    // near-miss: balo THƯỜNG (nền 0, điều kiện ≤) — không cần lấp đúng;
    // 4,5 + 7,9 và W=10 in 9 thay vì −1
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < n; ++i)
        for (int j = W; j >= w[i]; --j)
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    out << dp[W] << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH12 = challenge(
    "hsgi-cp-m12-vault",
    "Checkpoint — Két sắt đúng mã",
    """**Bài toán.** K loại "chìa khóa số" mệnh giá c_k (dùng vô hạn). Mã
két là tổng ĐÚNG S. Hãy mở két với ÍT CHÌA KHÓA NHẤT; không mở được
in −1.

**Ràng buộc:** 1 ≤ K ≤ 100; 1 ≤ S ≤ 100000; 1 ≤ c_k ≤ 100000.""",
    [
        contest_test(
            "tham lam gãy",
            T("2 6", "3 4"),
            T("2"),
            "3+3 = 2; tham-lam-lớn-nhất chọn 4 trước rồi kẹt: 6−4 = 2 không đổi được → −1.",
        ),
        contest_test(
            "vô nghiệm",
            T("2 3", "5 7"),
            T("-1"),
            "Không tổ hợp nào ra 3.",
        ),
        contest_test(
            "S lớn — xu đơn",
            T("1 100000", "77777"),
            T("-1"),
            "77777×1 < 100000, ×2 = 155554 ≠ 100000 — một mệnh giá không chia hết: vô nghiệm.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP12 = vi_challenge(
    "Checkpoint — Két sắt đúng mã",
    """**Bài toán.** Chìa mệnh giá c_k vô hạn; tổng ĐÚNG S với ít chìa nhất;
không được −1.""",
    [("tham lam", "3,4 và S=6 → 2; tham lam chọn 4 → −1 sai."),
     ("vô nghiệm", "5,7 và S=3 → −1."),
     ("S lớn", "Một mệnh giá 77777, S=100000 → −1.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m12",
    "Checkpoint — Knapsack",
    "Pass the graded problem to finish the knapsack module.",
    25,
    """**Checkpoint — Knapsack.** Pass the graded challenge: unbounded
exact-sum minimum count with a −1 verdict — the forward-loop DP with
an INF sentinel. Greedy largest-first is the trap this checkpoint
explicitly hunts.

**Điểm kiểm tra — Balo.** Pass bài chấm: đổi tiền không giới hạn, tổng
ĐÚNG, ít xu nhất, −1 khi vô nghiệm — DP vòng xuôi với mốc INF. Tham
lam lớn-nhất-trước là bẫy mà checkpoint này săn.""",
    "Checkpoint — Knapsack",
    "Pass bài chấm để hoàn thành module balo.",
    """**Điểm kiểm tra — Balo.** Pass bài chấm bên dưới: đổi tiền vô hạn
tổng đúng S ít xu nhất (−1 vô nghiệm).""",
    CH12,
    VI_CP12,
    solution=CPP_STD + cpp("""    int K, S; in >> K >> S;
    vector<int> c(K);
    for (auto& x : c) in >> x;
    const int INF = 1e9;
    vector<int> dp(S + 1, INF);
    dp[0] = 0;
    for (int k = 0; k < K; ++k)
        for (int s = c[k]; s <= S; ++s)
            if (dp[s - c[k]] + 1 < dp[s]) dp[s] = dp[s - c[k]] + 1;
    out << (dp[S] >= INF ? -1 : dp[S]) << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int K, S; in >> K >> S;
    vector<int> c(K);
    for (auto& x : c) in >> x;
    sort(c.rbegin(), c.rend());
    // near-miss: THAM LAM lớn-nhất-trước — 6,5,1 và S=7 ra 3 xu thay vì 2
    int cnt = 0;
    for (int k = 0; k < K; ++k) {
        cnt += S / c[k];
        S %= c[k];
    }
    out << (S > 0 ? -1 : cnt) << "{{NL}}";
""") + END,
)
