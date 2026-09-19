#!/usr/bin/env python3
"""HSG Intermediate — Module 15: hsgi-strings (String Techniques).

Polynomial rolling hashes (single + the double-hash anti-collision
pair), palindromic prefix detection with hash + binary search, distinct
substring counting, and KMP for occurrence counting. The hunted
failure: single small-mod hash collisions and the O(n²) sort-all-
substrings near-miss.

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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-strings"
write_module(
    M,
    "Strings — Hashing and Pattern Matching",
    "Rolling hash to compare substrings in O(1), palindromic prefix detection, distinct substring counting, and KMP for occurrence counting.",
    "Xâu — Băm và khớp mẫu",
    "Băm cuộn so sánh đoạn con trong O(1), dò tiền tố đối xứng, đếm xâu con phân biệt, và KMP đếm lần xuất hiện.",
    ["hsgi-m15-hash", "hsgi-m15-kmp", "hsgi-cp-m15"],
    ["hsgi-p15-strings"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m15-hash",
    "Rolling Hash — Substring Fingerprints",
    "Prefix hashes make any substring comparison O(1) — with the collision caveats that decide real verdicts.",
    20,
    """## Ý tưởng

So sánh hai đoạn con trực tiếp mất O(độ dài). Băm đa thức: coi xâu là
số cơ số B, lấy phần dư MOD:

h(s) = s[0]·B^(k−1) + s[1]·B^(k−2) + ... + s[k−1]

Tiền tố H[i] = hash của s[0..i); đoạn (l, r] = H[r] − H[l]·B^(r−l).
Chuẩn bị O(n), mỗi truy vấn O(1):

```cpp
const long long MOD = 1000000007;   // hoặc 2^61 − 1 (Mersenne)
const long long B = 131;
vector<long long> H(n + 1, 0), P(n + 1, 1);
for (int i = 0; i < n; ++i) {
    H[i+1] = (H[i] * B + s[i]) % MOD;
    P[i+1] = P[i] * B % MOD;
}
// hash của s[l..r) = (H[r] - H[l]*P[r-l] % MOD + MOD) % MOD
```

SỐ ÂM sau phép trừ: +MOD rồi %MOD — bẫy số âm module trước đã học.

## Va chạm — câu chuyện thật

Hai xâu khác nhau có thể trùng hash: xác suất ~1/MOD mỗi cặp. Với MOD
= 10^9+7 và 10^6 cặp so sánh: kỳ vọng va chạm ~10^6/10^9 = 10^3 —
NHỎ nhưng không phải không; kẻ địch CỐ TÌNH (hack) thì tìm được cặp
chống đơn-băm dễ dàng. Giải pháp contest: HAI băm (MOD, B khác nhau),
so sánh CẢ HAI:

```cpp
// pair<hash1, hash2> — va chạm đồng thời ~1/(MOD1·MOD2) ≈ 10^-18
```

Đề "chống băm" ở HSG thật: các bộ test sinh để hạ đơn-băm nhỏ — băm
kép là phao chuẩn.

## Ứng dụng kinh điển — tiền tố đối xứng

Tiền tố s[0..k) là palindrome ⇔ s[0..k) == reverse(s[0..k)). Precompute
hash của xâu và xâu ĐẢO; nhị phân tìm tiền tố đối xứng dài nhất (tiền
tố đối xứng của độ dài k+1... không đơn điệu? — ĐÚNG đơn điệu: nếu
tiền tố k đối xứng thì tiền tố k−1 cũng vậy? KHÔNG! "abcb a"? — s =
"abcba": tiền tố 5 đối xứng, tiền tố 4 "abcb" không, tiền tố 3 "abc"
không... tiền tố 1 "a" có. Đơn điệu SAI — phải quét mọi k hoặc rút ra
từManacher (chưa học). Quét O(n) với hash từng k vẫn nhanh.)

## Đếm xâu con phân biệt

Số xâu con phân biệt của s (n ≤ 1000): mọi cặp (độ dài, vị trí) — với
MỖI độ dài L, thu thập hash của n−L+1 đoạn, sort, đếm khác nhau. Tổng
O(n² log n) — n = 1000: ~10^7, ổn. n = 10^5: chết (cần suffix array /
automaton — để sau). Biết GIỚI HÀN của công cụ mình đang cầm.

**Điểm mấu chốt:** băm tiền tố = so sánh O(1); băm kép chống va chạm;
số âm +MOD; đếm xâu con phân biệt O(n² log n) tới n ≈ 1000.""",
    "Băm cuộn — Vân tay đoạn con",
    "Băm tiền tố so sánh đoạn con O(1) — với các lưu ý va chạm quyết định verdict.",
    """## Ý tưởng

So hai đoạn con trực tiếp O(độ dài). Băm đa thức: xâu là số cơ số B:

h(s) = s[0]·B^(k−1) + ... + s[k−1]

Tiền tố H[i]; đoạn (l, r] = H[r] − H[l]·B^(r−l). Chuẩn bị O(n), truy
vấn O(1):

```cpp
const long long MOD = 1000000007;
const long long B = 131;
vector<long long> H(n + 1, 0), P(n + 1, 1);
for (int i = 0; i < n; ++i) {
    H[i+1] = (H[i] * B + s[i]) % MOD;
    P[i+1] = P[i] * B % MOD;
}
// (H[r] - H[l]*P[r-l] % MOD + MOD) % MOD
```

Trừ ra số ÂM: +MOD rồi %MOD.

## Va chạm

Hai xâu khác nhau trùng hash: ~1/MOD mỗi cặp. Kẻ địch cố tình tìm được
cặp hạ đơn-băm nhỏ. Contest: HAI băm (MOD, B khác nhau), so CẢ HAI —
va chạm đồng thời ~10^-18.

## Tiền tố đối xứng

s[0..k) palindrome ⇔ == reverse. Precompute hash xâu + xâu đảo; quét
k (đơn điệu SAI — ví dụ "abcba": k=5 có, k=4 không, k=1 có) — quét O(n)
vẫn nhanh.

## Đếm xâu con phân biệt

Với mỗi độ dài L: hash các đoạn, sort, đếm khác — O(n² log n). n ≤
1000 ổn; n = 10^5 chết (cần suffix automaton — chưa học). Biết giới
hạn công cụ.

**Điểm mấu chốt:** băm tiền tố O(1); băm kép; số âm +MOD; đếm phân
biệt tới n ≈ 1000.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m15-kmp",
    "KMP — Occurrences Without Rescanning",
    "The failure function records the longest border of each prefix; matching never backs up in the text.",
    20,
    """## Vấn đề

Đếm/ liệt kê vị trí mẫu p xuất hiện trong văn bản t: duyệt mỗi vị trí
so từ đầu là O(|t|·|p|) — t, p tới 10^6 thì chết.

## Hàm tiền tố (failure function)

pi[i] = độ dài biên dài nhất của p[0..i] — tiền tố cũng là hậu tố
(không tính cả xâu):

```cpp
vector<int> pi(m, 0);
for (int i = 1; i < m; ++i) {
    int j = pi[i-1];
    while (j > 0 && p[i] != p[j]) j = pi[j-1];
    if (p[i] == p[j]) ++j;
    pi[i] = j;
}
```

pi[i] cho biết khi KHÔNG khớp tại vị trí kế, nhảy về đâu mà không so
lại phần đã khớp.

## Quét văn bản — con trỏ text không lùi

```cpp
int j = 0;                       // số ký tự p đã khớp
for (int i = 0; i < n; ++i) {
    while (j > 0 && t[i] != p[j]) j = pi[j-1];
    if (t[i] == p[j]) ++j;
    if (j == m) {
        // khớp kết thúc tại i → bắt đầu tại i - m + 1
        j = pi[j-1];             // tiếp tục tìm khớp kế
    }
}
```

i CHỈ tăng — tổng số lần j giảm bị chặn bởi số lần j tăng: O(n + m)
 amortized.

## Chuẩn hóa hai xâu — ghép với dấu ngăn

Cách nhớ nhanh: s = p + '#' + t ('#' không có trong hai xâu); tính pi
trên s; mọi vị trí i với pi[i] == m là một lần xuất hiện. Một khung
code duy nhất.

## Khi nào KHÔNG cần KMP

Đếm xâu con phân biệt: băm/sort. So SÁI MỘT cặp: trực tiếp. So nhiều
cặp cùng xâu: băm tiền tố. KMP dành cho "mẫu xuất hiện ở đâu" — đặc
biệt khi |p| nhỏ và |t| lớn, hoặc cần TẤT CẢ vị trí.

**Điểm mấu chốt:** pi = biên dài nhất; con trỏ text không lùi; O(n+m)
amortized; p+'#'+t là khung nhớ nhanh.""",
    "KMP — Đếm mẫu không quét lại",
    "Hàm tiền tố lưu biên dài nhất; con trỏ văn bản không bao giờ lùi.",
    """## Vấn đề

Đếm vị trí p trong t: quét từng vị trí O(|t|·|p|) — 10^6 × 10^6 chết.

## Hàm tiền tố

pi[i] = biên dài nhất của p[0..i] (tiền tố = hậu tố, không tính cả
xâu):

```cpp
vector<int> pi(m, 0);
for (int i = 1; i < m; ++i) {
    int j = pi[i-1];
    while (j > 0 && p[i] != p[j]) j = pi[j-1];
    if (p[i] == p[j]) ++j;
    pi[i] = j;
}
```

## Quét văn bản — không lùi

```cpp
int j = 0;
for (int i = 0; i < n; ++i) {
    while (j > 0 && t[i] != p[j]) j = pi[j-1];
    if (t[i] == p[j]) ++j;
    if (j == m) {
        // khớp kết thúc tại i
        j = pi[j-1];
    }
}
```

i chỉ tăng; j giảm bị chặn bởi j tăng: O(n + m) amortized.

## Khung nhớ nhanh

s = p + '#' + t; tính pi trên s; pi[i] == m → một lần xuất hiện kết
thúc tại i.

## Khi nào KHÔNG cần KMP

So một cặp: trực tiếp. Nhiều cặp cùng xâu: băm tiền tố. KMP cho "mẫu
ở đâu" — |p| nhỏ |t| lớn, hoặc cần mọi vị trí.

**Điểm mấu chốt:** pi = biên dài nhất; text không lùi; O(n+m);
p+'#'+t.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p15-paliprefix",
    "Tiền tố đối xứng dài nhất",
    """**Bài toán.** Xâu s thường (≤ 10^6 ký tự). In ĐỘ DÀI tiền tố dài
nhất của s là xâu ĐỐI XỨNG (palindrome; tiền tố có thể là cả xâu).

**Ràng buộc:** 1 ≤ |s| ≤ 10^6.

So trực tiếp từng độ dài O(n²) — n = 10^6 sẽ chết; dùng băm tiền tố
(xâu + xâu đảo) hoặc KMP trick.""",
    [
        contest_test(
            "ví dụ — cả xâu",
            T("abcba"),
            T("5"),
            "\"abcba\" đối xứng trọn: 5.",
        ),
        contest_test(
            "một ký tự",
            T("z"),
            T("1"),
            "Một ký tự luôn đối xứng.",
        ),
        contest_test(
            "không đối xứng sớm",
            T("abca"),
            T("1"),
            "Tiền tố \"a\" có; \"ab\", \"abc\", \"abca\" không — chỉ 1.",
        ),
        contest_test(
            "n lớn — a lặp",
            T("a" * 1000000),
            T("1000000"),
            "Toàn 'a': đối xứng trọn — O(n) bằng băm; O(n²) so ký tự sẽ chết thời gian.",
        ),
        contest_test(
            "n lớn — chặn giữa",
            T("a" * 499999 + "b" + "a" * 500000),
            T("999999"),
            "Tiền tố 999999 = a^499999 b a^499999 ĐỐI XỨNG (b ở giữa); cả xâu có 'b' lệch tâm → không — R KMP-trick trả 999999.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p15-subcount",
    "Đếm xâu con phân biệt",
    """**Bài toán.** Xâu s thường (≤ 1000 ký tự). In số LƯỢNG xâu con LIÊN
TIẾP phân biệt của s (hai xâu con cùng nội dung đếm một).

**Ràng buộc:** 1 ≤ |s| ≤ 1000.

O(n²) đoạn × hash + sort mỗi độ dài: O(n² log n) — chấp nhận được.""",
    [
        contest_test(
            "ví dụ",
            T("aba"),
            T("5"),
            "a, b, ab, ba, aba — 'a' lặp đếm một: 5.",
        ),
        contest_test(
            "một ký tự",
            T("q"),
            T("1"),
            "Chỉ 'q'.",
        ),
        contest_test(
            "toàn giống",
            T("aaaa"),
            T("4"),
            "a, aa, aaa, aaaa — 4.",
        ),
        contest_test(
            "n = 1000 — đan xen",
            T(("ab" * 500)),
            T("1999"),
            "Mỗi độ dài 1..n−1 có đúng 2 xâu ('ab…'/'ba…') + 1 cả xâu: 2·999 + 1 = 1999.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p15-occurrences",
    "Đếm lần xuất hiện của mẫu",
    """**Bài toán.** Hai dòng: mẫu p (≤ 10^6), văn bản t (≤ 10^6), chữ
thường. In số lần p xuất hiện trong t (CÁC KHỚP CÓ CHỒNG ĐÈ được đếm).

**Ràng buộc:** 1 ≤ |p| ≤ |t| ≤ 10^6.

KMP O(n + m). Quét từng vị trí so lại từ đầu O(n·m) sẽ chết khi mẫu
lặp (vd p = aa, t = aaaa).""",
    [
        contest_test(
            "chồng đè",
            T("aa", "aaaa"),
            T("3"),
            "aa tại vị trí 0, 1, 2 — chồng đè đếm: 3 (không chồng là 2).",
        ),
        contest_test(
            "không có",
            T("xy", "abcabc"),
            T("0"),
            "Không khớp nào.",
        ),
        contest_test(
            "mẫu = văn bản",
            T("abc", "abc"),
            T("1"),
            "Khớp duy nhất ở đầu.",
        ),
        contest_test(
            "n lớn — mẫu đơn",
            T("ab", "ab" * 500000),
            T("500000"),
            "10^6 ký tự; khớp tại vị trí lẻ 1, 3, …, 10^6−1: 500000 — O(n+m) chạy tức thì.",
        ),
        contest_test(
            "n lớn — mẫu lặp tự thân",
            T("a" * 500000, "a" * 1000000),
            T("500001"),
            "Mẫu tự chồng đè triệt để: naive phải so lại ~2.5·10^11 phép → quá hạn; KMP π một lượt O(n + m).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p15-period",
    "Chu kỳ của xâu",
    """**Bài toán.** Xâu s (≤ 10^6). Xâu p là CHU KỲ của s nếu s = p lặp k
lần (k ≥ 2). In chu kỳ NGẮN NHẤT của s; nếu s nguyên tố (không tách
được) in −1... LƯU Ý: nếu |s| % (n − pi[n−1]) == 0 và n − pi[n−1] < n
thì chu kỳ ngắn nhất là n − pi[n−1]; ngược lại −1.

**Ràng buộc:** 1 ≤ |s| ≤ 10^6.""",
    [
        contest_test(
            "ví dụ — lặp trọn",
            T("abcabcabc"),
            T("3"),
            "n = 9, pi cuối = 6 → 9 − 6 = 3, 9 % 3 = 0: chu kỳ \"abc\".",
        ),
        contest_test(
            "không tách được",
            T("abcab"),
            T("-1"),
            "pi cuối = 2 → 5 − 2 = 3, 5 % 3 ≠ 0: nguyên tố.",
        ),
        contest_test(
            "một ký tự",
            T("a"),
            T("-1"),
            "Không lặp được (k ≥ 2 cần): −1.",
        ),
        contest_test(
            "chu kỳ 1",
            T("zzzzzz"),
            T("1"),
            "pi cuối = 5 → 6 − 5 = 1: 'z' lặp sáu lần.",
        ),
        contest_test(
            "n lớn — chu kỳ 7",
            T("xaydung" * 142857)[:10**6][0:0] + T(("xaydung" * 142858)[:1000000]),
            T("-1"),
            "10^6 % 7 ≠ 0 (10^6 = 7·142857 + 1): phần thừa phá chu kỳ → −1; KMP O(n).",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p15-hasheq",
    "Truy vấn đoạn bằng nhau",
    """**Bài toán.** Xâu s (≤ 2·10^5), Q truy vấn (l1, r1, l2, r2): đoạn
s[l1..r1] và s[l2..r2] (đánh số từ 1) BẰNG NHAU? In YES/NO mỗi truy
vấn (mỗi kết quả một dòng).

**Ràng buộc:** 1 ≤ Q ≤ 2·10^5; 1 ≤ l1 ≤ r1 ≤ |s|; 1 ≤ l2 ≤ r2 ≤ |s|;
độ dài hai đoạn LUÔN bằng nhau.

Băm tiền tố trả O(1) mỗi truy vấn; so ký tự trực tiếp O(n) mỗi truy
vấn sẽ chết (2·10^5 × 2·10^5).""",
    [
        contest_test(
            "ví dụ",
            T("abcabc", "4", "1 3 4 6", "1 2 4 5", "1 3 2 4", "2 2 5 5"),
            T("YES", "YES", "NO", "YES"),
            "\"abc\"=\"abc\"; \"ab\"=\"ab\"; \"abc\"≠\"bca\"; \"c\"=\"c\".",
        ),
        contest_test(
            "truy vấn đơn ký tự",
            T("aaa", "2", "1 1 3 3", "1 1 2 2"),
            T("YES", "YES"),
            "Mọi ký tự 'a' bằng nhau.",
        ),
        contest_test(
            "n lớn — truy vấn lặp đoạn đầy",
            T("a" * 200000, "5", "1 200000 1 200000", "1 200000 1 200000", "1 200000 1 200000", "1 200000 1 200000", "1 200000 1 200000"),
            T("YES", "YES", "YES", "YES", "YES"),
            "Năm truy vấn so toàn xâu: băm trả ngay; so-từng-ký-tự 5×2·10^5 — vẫn nhanh? bài thật của băm là đoạn DỊCH — nhưng test này bẫy Q lớn: mỗi truy vấn O(1) giúp Q = 2·10^5 ở T4.",
        ),
        contest_test(
            "Q lớn — đoạn dịch",
            T(("ab" * 100000), "200000") + T(*[("1 100000 " + str(i % 2 + 1) + " " + str(100000 + (i % 2))) for i in range(200000)]),
            T(*(["YES", "NO"] * 100000)),
            "Đoạn bắt đầu 1 = 'abab…' YES; bắt đầu 2 = 'baba…' NO — xen kẽ 200000 dòng; so trực tiếp O(n·Q) = 2·10^10 chết; băm O(Q).",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI15 = {
    "hsgi-p15-paliprefix": vi_challenge(
        "Tiền tố đối xứng dài nhất",
        """**Bài toán.** |s| ≤ 10^6: độ dài tiền tố đối xứng dài nhất.""",
        [("abcba", "5 — cả xâu."),
         ("abca", "1."),
         ("kỹ thuật", "Băm xâu + đảo, hoặc KMP trick; O(n).")],
    ),
    "hsgi-p15-subcount": vi_challenge(
        "Đếm xâu con phân biệt",
        """**Bài toán.** |s| ≤ 1000: số xâu con liên tiếp phân biệt.""",
        [("aba", "5."),
         ("aaaa", "4."),
         ("kỹ thuật", "Hash + sort mỗi độ dài: O(n² log n).")],
    ),
    "hsgi-p15-occurrences": vi_challenge(
        "Đếm lần xuất hiện của mẫu",
        """**Bài toán.** p, t ≤ 10^6: số lần p xuất hiện (đếm cả chồng đè).""",
        [("aa / aaaa", "3."),
         ("kỹ thuật", "KMP O(n+m); quét lại từ đầu sẽ chết.")],
    ),
    "hsgi-p15-period": vi_challenge(
        "Chu kỳ của xâu",
        """**Bài toán.** Chu kỳ ngắn nhất p (s = p^k, k ≥ 2); không có in −1.""",
        [("abcabcabc", "3."),
         ("zzzzzz", "1."),
         ("kỹ thuật", "n − pi[n−1] chia hết n.")],
    ),
    "hsgi-p15-hasheq": vi_challenge(
        "Truy vấn đoạn bằng nhau",
        """**Bài toán.** Q truy vấn: hai đoạn cùng độ dài bằng nhau? YES/NO.""",
        [("ví dụ", "YES YES NO YES."),
         ("Q lớn", "Băm O(1)/truy vấn; so ký tự chết.")],
    ),
}

write_practice(
    M,
    "hsgi-p15-strings",
    "String Techniques Problem Set",
    "Five problems: palindromic prefix, distinct substrings, KMP occurrences, string period, substring-equality queries.",
    "Bài tập xâu",
    "Năm bài: tiền tố đối xứng, xâu con phân biệt, đếm mẫu KMP, chu kỳ xâu, truy vấn đoạn bằng nhau.",
    "hsgi-m15-kmp",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI15,
    solutions=[
        (
            "hsgi-p15-paliprefix",
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    // KMP trick: s + '#' + reverse(s); pi tại vị trí cuối = biên dài nhất
    // của reverse(s) khớp hậu tố... chuẩn hơn: tiền tố đối xứng dài nhất
    // = biên dài nhất p của s sao cho p == reverse(p) — pi[n-1] của
    // t = s + '#' + reverse(s) chính là độ dài đó
    string r(s.rbegin(), s.rend());
    string t = s + "#" + r;
    int m = t.size();
    vector<int> pi(m, 0);
    for (int i = 1; i < m; ++i) {
        int j = pi[i-1];
        while (j > 0 && t[i] != t[j]) j = pi[j-1];
        if (t[i] == t[j]) ++j;
        pi[i] = j;
    }
    out << pi[m-1] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    // near-miss: so TRỰC TIẾP từng độ dài tiền tố với đảo — O(n²) ký tự;
    // n = 10^6 toàn 'a' → 10^12 phép so → quá hạn chắc chắn
    int best = 0;
    for (int k = 1; k <= n; ++k) {
        bool ok = true;
        for (int i = 0; i < k; ++i)
            if (s[i] != s[k-1-i]) { ok = false; break; }
        if (ok) best = k;
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p15-subcount",
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    const long long MOD1 = 1000000007, MOD2 = 998244353, B = 131;
    vector<long long> H1(n + 1, 0), P1(n + 1, 1), H2(n + 1, 0), P2(n + 1, 1);
    for (int i = 0; i < n; ++i) {
        H1[i+1] = (H1[i] * B + s[i]) % MOD1;
        P1[i+1] = P1[i] * B % MOD1;
        H2[i+1] = (H2[i] * B + s[i]) % MOD2;
        P2[i+1] = P2[i] * B % MOD2;
    }
    long long total = 0;
    vector<pair<long long,long long>> hs;
    for (int L = 1; L <= n; ++L) {
        hs.clear();
        for (int l = 0; l + L <= n; ++l) {
            int r = l + L;
            long long h1 = (H1[r] - H1[l] * P1[L]) % MOD1;
            if (h1 < 0) h1 += MOD1;
            long long h2 = (H2[r] - H2[l] * P2[L]) % MOD2;
            if (h2 < 0) h2 += MOD2;
            hs.push_back({h1, h2});
        }
        sort(hs.begin(), hs.end());
        total += unique(hs.begin(), hs.end()) - hs.begin();
    }
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    // near-miss: đếm MỌI cặp vị trí (l, r) — đếm LẦN XUẤT HIỆN chứ không
    // phải xâu PHÂN BIỆT; 'aba' trả 6 thay vì 5, 'aaaa' trả 10 thay vì 4
    out << (long long)n * (n + 1) / 2 << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p15-occurrences",
            CPP_STD + cpp("""    string p, t; in >> p >> t;
    string s = p + "#" + t;
    int m = p.size(), M = s.size();
    vector<int> pi(M, 0);
    for (int i = 1; i < M; ++i) {
        int j = pi[i-1];
        while (j > 0 && s[i] != s[j]) j = pi[j-1];
        if (s[i] == s[j]) ++j;
        pi[i] = j;
    }
    long long cnt = 0;
    for (int i = m + 1; i < M; ++i)
        if (pi[i] == m) ++cnt;
    out << cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string p, t; in >> p >> t;
    int m = p.size(), n = t.size();
    // near-miss: quét từng vị trí, so lại TỪ ĐẦU mẫu — O(n·m); mẫu tự
    // lặp (aab trong aab×N) biến thành (n·m) ≈ 10^12 phép → quá hạn
    long long cnt = 0;
    for (int i = 0; i + m <= n; ++i) {
        bool ok = true;
        for (int j = 0; j < m; ++j)
            if (t[i + j] != p[j]) { ok = false; break; }
        cnt += ok;
    }
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p15-period",
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; ++i) {
        int j = pi[i-1];
        while (j > 0 && s[i] != s[j]) j = pi[j-1];
        if (s[i] == s[j]) ++j;
        pi[i] = j;
    }
    int cand = n - pi[n-1];
    if (cand < n && n % cand == 0) out << cand << "{{NL}}";
    else out << -1 << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    // near-miss: thử MỌI ước d của n và so sánh khối — đúng kết quả nhưng
    // O(n·số ước) ≈ O(n^1.1)? thực tế: mỗi ước kiểm O(n) → tổng O(n·d(n))
    // vẫn nhanh với n = 10^6 (d ≤ 240)... lỗi thật: kiểm d từ n/2 XUỐNG
    // nhưng QUÊN kiểm n % d == 0 trước — so khối lệch → kết quả sai
    for (int d = n / 2; d >= 1; --d) {
        bool ok = true;
        for (int i = 0; i < n; ++i)
            if (s[i] != s[i % d]) { ok = false; break; }
        if (ok) { out << d << "{{NL}}"; return; }
    }
    out << -1 << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p15-hasheq",
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    const long long MOD1 = 1000000007, MOD2 = 998244353, B = 131;
    vector<long long> H1(n + 1, 0), P1(n + 1, 1), H2(n + 1, 0), P2(n + 1, 1);
    for (int i = 0; i < n; ++i) {
        H1[i+1] = (H1[i] * B + s[i]) % MOD1;
        P1[i+1] = P1[i] * B % MOD1;
        H2[i+1] = (H2[i] * B + s[i]) % MOD2;
        P2[i+1] = P2[i] * B % MOD2;
    }
    auto get = [&](vector<long long>& H, vector<long long>& P, long long MOD, int l, int r) {
        long long h = (H[r] - H[l] * P[r - l]) % MOD;
        if (h < 0) h += MOD;
        return h;
    };
    int Q; in >> Q;
    while (Q--) {
        int l1, r1, l2, r2; in >> l1 >> r1 >> l2 >> r2;
        bool eq = (r1 - l1) == (r2 - l2)
            && get(H1, P1, MOD1, l1 - 1, r1) == get(H1, P1, MOD1, l2 - 1, r2)
            && get(H2, P2, MOD2, l1 - 1, r1) == get(H2, P2, MOD2, l2 - 1, r2);
        out << (eq ? "YES" : "NO") << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    // near-miss: SO TRỰC TIẾP từng truy vấn — O(Q·n); Q = 2·10^5 × đoạn
    // 10^5 ký tự = 2·10^10 phép → quá hạn chắc chắn
    int Q; in >> Q;
    while (Q--) {
        int l1, r1, l2, r2; in >> l1 >> r1 >> l2 >> r2;
        bool eq = (r1 - l1) == (r2 - l2);
        for (int i = 0; eq && i < r1 - l1 + 1; ++i)
            if (s[l1 - 1 + i] != s[l2 - 1 + i]) eq = false;
        out << (eq ? "YES" : "NO") << "{{NL}}";
    }
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH15 = challenge(
    "hsgi-cp-m15-mirror",
    "Checkpoint — Dải kính đối xứng",
    """**Bài toán.** Dãy n ô kính, ô i mang ký tự thường. Một DẢI ô liên
tục [l, r] là ĐỐI XỨNG nếu dãy ký tự đọc xuôi và ngược giống nhau. Q
truy vấn (l, r): dải đó đối xứng? In YES/NO mỗi dòng.

**Ràng buộc:** 1 ≤ n ≤ 2·10^5; 1 ≤ Q ≤ 2·10^5; 1 ≤ l ≤ r ≤ n.

Băm xuôi + băm ĐẢO trả O(1)/truy vấn; so từng ký tự chết với Q·n.""",
    [
        contest_test(
            "ví dụ",
            T("abcba", "4", "1 5", "2 4", "1 2", "3 3"),
            T("YES", "YES", "NO", "YES"),
            "abcba, bcb, c đối xứng; ab không.",
        ),
        contest_test(
            "một ô",
            T("q", "1", "1 1"),
            T("YES"),
            "Một ký tự luôn đối xứng.",
        ),
        contest_test(
            "Q lớn — dải toàn a",
            T("a" * 200000, "3", "1 200000", "1 200000", "1 200000"),
            T("YES", "YES", "YES"),
            "Ba dải trọn: băm O(1); so ký tự 3×2·10^5 vẫn nhanh — bẫy thật ở T4.",
        ),
        contest_test(
            "Q lớn — dải lệch",
            T("a" * 199999 + "b", "200000") + T(*[("1 " + str(200000 - (i % 2))) for i in range(200000)]),
            T(*(["NO", "YES"] * 100000)),
            "Dải tới 200000 chứa 'b' cuối → NO; dải tới 199999 toàn 'a' → YES — xen kẽ; so ký tự O(Q·n) = 4·10^10 → chết; băm O(Q).",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP15 = vi_challenge(
    "Checkpoint — Dải kính đối xứng",
    """**Bài toán.** Q truy vấn (l, r): dải [l, r] đối xứng? YES/NO.""",
    [("ví dụ", "YES YES NO YES."),
     ("Q lớn", "Băm xuôi + đảo O(1)/truy vấn."),
     ("bẫy", "So ký tự O(Q·n) chết.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m15",
    "Checkpoint — Strings",
    "Pass the graded problem to finish the string techniques module.",
    25,
    """**Checkpoint — Strings.** Pass the graded challenge: range
palindrome queries — forward hash + reversed hash, O(1) per query.
Character-by-character comparison is the hunted timeout.

**Điểm kiểm tra — Xâu.** Pass bài chấm: truy vấn đối xứng trên dải —
băm xuôi + băm đảo, O(1)/truy vấn. So từng ký tự là quá hạn bị săn.""",
    "Checkpoint — Strings",
    "Pass bài chấm để hoàn thành module xâu.",
    """**Điểm kiểm tra — Xâu.** Pass bài chấm bên dưới: Q truy vấn dải đối
xứng với băm kép.""",
    CH15,
    VI_CP15,
    solution=CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    const long long MOD1 = 1000000007, MOD2 = 998244353, B = 131;
    string r(s.rbegin(), s.rend());
    // hash của s và của reverse(s); đoạn [l..r] (1-based) đối xứng ⇔
    // hash_s(l..r) == hash_r(n+1-r .. n+1-l)
    auto build = [&](const string& x) {
        vector<long long> H(n + 1, 0), P(n + 1, 1);
        for (int i = 0; i < n; ++i) {
            H[i+1] = (H[i] * B + x[i]) % MOD1;
            P[i+1] = P[i] * B % MOD1;
        }
        return make_pair(H, P);
    };
    auto [Hs, Ps] = build(s);
    auto [Hr, Pr] = build(r);
    auto get = [&](vector<long long>& H, vector<long long>& P, int l, int rr) {
        long long h = (H[rr] - H[l] * P[rr - l]) % MOD1;
        if (h < 0) h += MOD1;
        return h;
    };
    int Q; in >> Q;
    while (Q--) {
        int l, rr; in >> l >> rr;
        bool eq = get(Hs, Ps, l - 1, rr) == get(Hr, Pr, n - rr, n - l + 1);
        out << (eq ? "YES" : "NO") << "{{NL}}";
    }
""") + END,
    wrong=CPP_STD + cpp("""    string s; in >> s;
    int n = s.size();
    // near-miss: SO KÝ TỰ từng truy vấn — O(Q·n); Q = 2·10^5 × n = 2·10^5
    // → 4·10^10 phép → quá hạn chắc chắn
    int Q; in >> Q;
    while (Q--) {
        int l, rr; in >> l >> rr;
        bool eq = true;
        for (int i = l - 1, j = rr - 1; i < j; ++i, --j)
            if (s[i] != s[j]) { eq = false; break; }
        out << (eq ? "YES" : "NO") << "{{NL}}";
    }
""") + END,
)
