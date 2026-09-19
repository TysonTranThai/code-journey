#!/usr/bin/env python3
"""HSG Intermediate — Module 14: hsgi-numth (Number Theory).

Sieve to 10^7, prime check via trial division to sqrt, gcd/lcm identity
with the overflow-safe order, modular exponentiation, factorization,
divisor counting. Modulo traps (negative mod, modding intermediates) are
the hunted failure modes.

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

M = "hsgi-numth"
write_module(
    M,
    "Number Theory — Sieve, GCD, Modular Power",
    "Prime tables in O(n log log n), the gcd identity with safe ordering, binary exponentiation, and the modulo hygiene that decides verdicts.",
    "Lý thuyết số — Sàng, GCD, lũy thừa mô-đun",
    "Bảng nguyên tố O(n log log n), đồng nhất thức gcd với thứ tự an toàn, luỹ thừa nhị phân, và vệ sinh mô-đun quyết định verdict.",
    ["hsgi-m14-sieve", "hsgi-m14-modpow", "hsgi-cp-m14"],
    ["hsgi-p14-numth"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m14-sieve",
    "The Sieve and Its Siblings",
    "Eratosthenes in O(n log log n), trial division for one-off checks, and factorization by smallest prime factor.",
    20,
    """## Sàng Eratosthenes

Bảng nguyên tố tới N:

```cpp
const int N = 10000000;
vector<char> is_composite(N + 1, 0);
vector<int> primes;
for (int i = 2; i <= N; ++i) {
    if (!is_composite[i]) {
        primes.push_back(i);
        if ((long long)i * i <= N)
            for (long long j = (long long)i * i; j <= N; j += i)
                is_composite[j] = 1;
    }
}
```

Độ phức tạp O(n log log n) ≈ tuyến tính; 10^7 bool ≈ 10 MB. Chi tiết
quan trọng: bắt đầu từ i*i (bội nhỏ hơn đã bị sàng bởi số nhỏ hơn);
vòng trong dùng long long tránh tràn i*i.

## Kiểm tra một số — không cần sàng

Một số x: thử chia các i = 2, 3, 5, 7... tới sqrt(x). Nếu x ≤ 10^12,
sqrt = 10^6 phép — nhanh:

```cpp
bool isPrime(long long x) {
    if (x < 2) return false;
    for (long long i = 2; i * i <= x; ++i)
        if (x % i == 0) return false;
    return true;
}
```

i*i ≤ x với i kiểu long long: x tới ~9·10^18 mới tràn (2^63).

## Phân tích thừa số

SPF (smallest prime factor) từ sàng, hoặc chia thử:

```cpp
vector<pair<long long,int>> factorize(long long x) {
    vector<pair<long long,int>> f;
    for (long long d = 2; d * d <= x; ++d) {
        if (x % d == 0) {
            int k = 0;
            while (x % d == 0) { x /= d; ++k; }
            f.push_back({d, k});
        }
    }
    if (x > 1) f.push_back({x, 1});
    return f;
}
```

Sau vòng lặp x là thừa số nguyên tố còn lại > sqrt(x gốc).

## Số ước

Từ phân tích: d(n) = ∏ (k_i + 1). n ≤ 10^12 → tối đa ~6720 ước — liệt
kê bằng chia thử tới sqrt cũng nhanh.

**Điểm mấu chốt:** sàng cho NHIỀU truy vấn; chia thử sqrt cho MỘT số
lớn; i*i dùng long long; bắt đầu sàng từ i*i.""",
    "Sàng và họ hàng",
    "Eratosthenes O(n log log n), chia thử sqrt cho một số lớn, phân tích thừa số bằng SPF hoặc chia thử.",
    """## Sàng Eratosthenes

```cpp
const int N = 10000000;
vector<char> is_composite(N + 1, 0);
vector<int> primes;
for (int i = 2; i <= N; ++i) {
    if (!is_composite[i]) {
        primes.push_back(i);
        if ((long long)i * i <= N)
            for (long long j = (long long)i * i; j <= N; j += i)
                is_composite[j] = 1;
    }
}
```

O(n log log n) ≈ tuyến tính; 10^7 bool ≈ 10 MB. Bắt đầu từ i*i (bội
nhỏ hơn đã sàng); vòng trong long long tránh tràn i*i.

## Kiểm một số — không cần sàng

x ≤ 10^12 → sqrt = 10^6 phép:

```cpp
bool isPrime(long long x) {
    if (x < 2) return false;
    for (long long i = 2; i * i <= x; ++i)
        if (x % i == 0) return false;
    return true;
}
```

i*i ≤ x với long long: an toàn tới ~9·10^18.

## Phân tích thừa số

```cpp
vector<pair<long long,int>> factorize(long long x) {
    vector<pair<long long,int>> f;
    for (long long d = 2; d * d <= x; ++d) {
        if (x % d == 0) {
            int k = 0;
            while (x % d == 0) { x /= d; ++k; }
            f.push_back({d, k});
        }
    }
    if (x > 1) f.push_back({x, 1});
    return f;
}
```

Sau vòng, x là thừa số nguyên tố > sqrt(x gốc).

## Số ước

d(n) = ∏ (k_i + 1). n ≤ 10^12 → ≤ ~6720 ước: chia thử tới sqrt đủ.

**Điểm mấu chốt:** sàng cho nhiều truy vấn; sqrt chia thử cho một số
lớn; i*i long long; bắt đầu từ i*i.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m14-modpow",
    "GCD, Modular Exponentiation, and Mod Hygiene",
    "The gcd identity with lcm computed by division-first, binary exponentiation in O(log b), and the three modulo traps that cost contest verdicts.",
    20,
    """## gcd — và thứ tự tính lcm

std::gcd có sẵn (C++17). lcm là nơi gãy: a / gcd(a,b) * b — CHIA
TRƯỚC, NHÂN SAU. Nhân trước (a * b / gcd) tràn với a, b ~ 10^9 (tích
10^18 vẫn long long... nhưng a, b ~ 10^18 thì chết); thói quen chia
trước là phao cứu sinh:

```cpp
long long lcm_ll(long long a, long long b) {
    return a / std::gcd(a, b) * b;
}
```

## Luỹ thừa mô-đun — nhị phân

a^b mod m với b tới 10^18: nhân dần mất O(b) — chết. Bình phương:

```cpp
long long power(long long a, long long b, long long m) {
    long long r = 1 % m;
    a %= m;
    while (b > 0) {
        if (b & 1) r = r * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return r;
}
```

O(log b) ≈ 60 phép. a * a % m: tích trước mô-đun phải < m² < 2^63 → m
< ~3·10^9 an toàn; m tới 10^18 cần nhân 128-bit (__int128).

## Ba bẫy mô-đun

1. SỐ ÂM: (−3) % 10^9+7 = −3 trong C++ (cắt về 0). Sau phép trừ luôn
   `x = ((x % MOD) + MOD) % MOD`.
2. QUÊN MÔ-ĐUN GIỮA CHỪNG: cộng 10^9 vài lần trong long long là ổn,
   nhưng NHÂN hai số chưa mod là chết. Quy tắc: mod sau mỗi phép nhân.
3. MOD LỖI CHỖ: mod TỔNG trước khi in nhưng quên trong vòng — kết quả
   lệch âm hoặc tràn âm thầm.

## Kết hợp

power là nền của nghịch đảo mô-đun (Fermat: a^(p−2) mod p khi p nguyên
tố) — dùng lại mọi nơi cần "chia" trong mô-đun (tổ hợp, hệ số).

**Điểm mấu chốt:** lcm = a/gcd*b; power O(log b) mod từng bước; âm
hàng → cộng MOD; m ≤ ~3·10^9 cho nhân 64-bit.""",
    "GCD, luỹ thừa mô-đun, vệ sinh mod",
    "gcd + lcm chia-trước-nhân-sau, luỹ thừa nhị phân O(log b), ba bẫy mô-đun quyết định verdict.",
    """## gcd — và thứ tự tính lcm

std::gcd có sẵn. lcm: a / gcd(a,b) * b — CHIA TRƯỚC, NHÂN SAU:

```cpp
long long lcm_ll(long long a, long long b) {
    return a / std::gcd(a, b) * b;
}
```

Nhân trước tràn khi a, b ~ 10^18; chia trước là phao cứu sinh.

## Luỹ thừa mô-đun — nhị phân

a^b mod m, b tới 10^18:

```cpp
long long power(long long a, long long b, long long m) {
    long long r = 1 % m;
    a %= m;
    while (b > 0) {
        if (b & 1) r = r * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return r;
}
```

O(log b) ≈ 60 phép. a * a % m an toàn khi m < ~3·10^9; m tới 10^18
cần __int128.

## Ba bẫy mô-đun

1. SỐ ÂM: (−3) % p = −3 — sau trừ: `x = ((x % p) + p) % p`.
2. QUÊN MOD GIỮA CHỪNG: nhân hai số chưa mod là chết; mod sau mỗi
   phép nhân.
3. MOD LỖI CHỖ: mod khi in nhưng quên trong vòng — lệch âm thầm.

## Kết hợp

power là nền nghịch đảo mô-đun (a^(p−2) mod p) — "chia" trong mô-đun.

**Điểm mấu chốt:** lcm = a/gcd*b; power mod từng bước; âm → cộng p;
m ≤ 3·10^9 cho nhân 64-bit.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p14-sievecount",
    "Đếm số nguyên tố",
    """**Bài toán.** Q truy vấn; truy vấn i là số N_i. In số nguyên tố ≤
N_i cho mỗi truy vấn (mỗi kết quả một dòng).

**Ràng buộc:** 1 ≤ Q ≤ 10^4; 1 ≤ N_i ≤ 10^7.

Nhiều truy vấn → sàng MỘT lần, trả O(1).""",
    [
        contest_test(
            "ví dụ",
            T("4", "1", "2", "10", "100"),
            T("0", "1", "4", "25"),
            "π(1)=0, π(2)=1, π(10)=4, π(100)=25 — bảng π sẵn sàng.",
        ),
        contest_test(
            "N = 10^7",
            T("1", "10000000"),
            T("664579"),
            "π(10^7) = 664579 — sàng 10^7 bool ≈ 10 MB, một lượt.",
        ),
        contest_test(
            "Q lớn — truy vấn 10^7 lặp",
            T("40") + T(*["10000000"] * 40),
            T(*["664579"] * 40),
            "Bốn mươi truy vấn N = 10^7: bảng π trả ngay; chia-thử mỗi truy vấn ~10^9 phép × 40 → quá hạn chắc chắn.",
        ),
        contest_test(
            "biên N nhỏ",
            T("3", "0", "3", "4"),
            T("0", "2", "2"),
            "π(0)=0, π(3)=2, π(4)=2 — biên 0/1/2 phải đúng.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p14-primecheck",
    "Kiểm tra số lớn",
    """**Bài toán.** Q truy vấn số x_i (tới 10^12); in PRIME hoặc
COMPOSITE (mỗi dòng một kết quả). x_i = 1 → COMPOSITE.

**Ràng buộc:** 1 ≤ Q ≤ 100; 1 ≤ x_i ≤ 10^12.

Một số lớn một lần → chia thử tới sqrt (10^6 phép) — không cần sàng.""",
    [
        contest_test(
            "ví dụ",
            T("4", "2", "999999999989", "1000000000000", "1"),
            T("PRIME", "PRIME", "COMPOSITE", "COMPOSITE"),
            "999999999989 là nguyên tố lớn (kiểm biết); 10^12 = (10^6)² hợp số; 1 → COMPOSITE.",
        ),
        contest_test(
            "bình phương nguyên tố",
            T("2", "104729", "10968163441"),
            T("PRIME", "COMPOSITE"),
            "104729 nguyên tố; 10968163441 = 104729² — hợp số có ước duy nhất lớn (chia thử tới 10^5 mới tìm ra).",
        ),
        contest_test(
            "số chẵn lớn",
            T("2", "999999999998", "999999999989"),
            T("COMPOSITE", "PRIME"),
            "Chẵn > 2 luôn hợp số — thoát sớm; 999999999989 nguyên tố (ước nhỏ nhất > 10^6).",
        ),
        contest_test(
            "Q trùng",
            T("3", "998244353", "998244353", "998244353"),
            T("PRIME", "PRIME", "PRIME"),
            "998244353 — hằng số NTT kinh điển, nguyên tố.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p14-lcmrange",
    "BCNN đoạn",
    """**Bài toán.** Cho L, R (1 ≤ L ≤ R ≤ 10^6). In BCNN của TẤT CẢ số
nguyên trong [L, R], theo mô-đun 10^9 + 7. Nếu BCNN thật ≥ 10^9+7,
kết quả vẫn là phần dư (in phần dư).

**Ràng buộc:** 1 ≤ L ≤ R ≤ 10^6.

BCNN thật có thể khổng lồ (nhiều chữ số) — chỉ in phần dư. Ghép bằng
đồng nhất thức lcm với chia-trước; mô-đun từng bước. LƯU Ý: với
mod, a/gcd không đơn giản — hãy giữ số nguyên tố mũ cao nhất: với mỗi
số nguyên tố p ≤ R, lấy mũ lớn nhất e sao cho p^e ≤ R... trong [L, R]
chọn p^e ≥ L lớn nhất.""",
    [
        contest_test(
            "ví dụ — đoạn nhỏ",
            T("1 4"),
            T("12"),
            "lcm(1,2,3,4) = 12.",
        ),
        contest_test(
            "một số",
            T("7 7"),
            T("7"),
            "lcm của một số là chính nó.",
        ),
        contest_test(
            "đoạn lũy thừa",
            T("8 10"),
            T("360"),
            "lcm(8,9,10) = 2^3·3^2·5 = 360.",
        ),
        contest_test(
            "R lớn — phần dư",
            T("999983 1000000"),
            T("982831551"),
            "BCNN thật khổng lồ; kỳ vọng theo R sau probe Python (tính bằng tích mũ nguyên tố + mod).",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p14-divisors",
    "Số ước nhiều nhất",
    """**Bài toán.** Với n (1 ≤ n ≤ 10^12), in SỐ LƯỢNG ước dương của n.

**Ràng buộc:** 1 ≤ Q ≤ 100 truy vấn; 1 ≤ n ≤ 10^12.

Phân tích thừa số bằng chia thử tới sqrt; d(n) = ∏(k_i+1).""",
    [
        contest_test(
            "ví dụ",
            T("3", "12", "1", "999999999989"),
            T("6", "1", "2"),
            "12 = 2²·3 → 6 ước; 1 có đúng 1 ước; nguyên tố lớn → 2 ước.",
        ),
        contest_test(
            "bậc hai nguyên tố",
            T("1", "10968163441"),
            T("3"),
            "104729² có 3 ước: 1, p, p².",
        ),
        contest_test(
            "số ước phong phú",
            T("1", "963761198400"),
            T("6720"),
            "963761198400 = 2^6·3^4·5²·7·11·13·17·19·23·29 — 6720 ước, champion cổ điển dưới 10^12.",
        ),
        contest_test(
            "Q trùng",
            T("2", "720", "720"),
            T("30", "30"),
            "720 = 2^4·3^2·5 → (4+1)(2+1)(1+1) = 30.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p14-modpowsum",
    "Tổng luỹ thừa mô-đun",
    """**Bài toán.** Cho a, b, m (1 ≤ a, b ≤ 10^18; 1 ≤ m ≤ 10^9). In
(a^b) mod m. LƯU Ý: a có thể ≥ m, b khổng lồ — luỹ thừa nhị phân với
mod từng bước là bắt buộc.

**Ràng buộc:** 1 ≤ Q ≤ 100; 1 ≤ a ≤ 10^18; 1 ≤ b ≤ 10^18; 1 ≤ m ≤ 10^9.""",
    [
        contest_test(
            "ví dụ",
            T("3", "2 10 1000", "1 999999999999999999 998244353", "998244353 2 1000000007"),
            T("24", "1", "320946142"),
            "2^10 = 1024 mod 1000 = 24; 1^anything = 1; 998244353² mod (10^9+7) = 320946142 (pow xác nhận).",
        ),
        contest_test(
            "a > m",
            T("2", "1000000007 5 7", "123456789123456789 3 1000000007"),
            T("6", "275772668"),
            "10^9+7 ≡ 6 (−1) mod 7: (−1)^5 = 6 — mod a TRƯỚC rồi bình phương; giá trị thứ hai xác nhận bằng pow Python.",
        ),
        contest_test(
            "b = 0 ẩn",
            T("1", "5 1 13"),
            T("5"),
            "b ≥ 1 theo đề; b=1 → a mod m.",
        ),
        contest_test(
            "m = 1",
            T("2", "999 999999999999999999 1", "7 3 1"),
            T("0", "0"),
            "Mọi số mod 1 = 0 — r % m với r khởi tạo 1 % m = 0 đúng.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI14 = {
    "hsgi-p14-sievecount": vi_challenge(
        "Đếm số nguyên tố",
        """**Bài toán.** Q truy vấn N_i ≤ 10^7: in π(N_i) — số nguyên tố ≤
N_i.""",
        [("ví dụ", "π(100) = 25."),          ("N = 10^7", "664579 — sàng một lượt."),
         ("kỹ thuật", "Bảng π, truy vấn O(1).")],
    ),
    "hsgi-p14-primecheck": vi_challenge(
        "Kiểm tra số lớn",
        """**Bài toán.** x ≤ 10^12: PRIME hay COMPOSITE? 1 → COMPOSITE.""",
        [("ví dụ", "999999999989 PRIME; 10^12 COMPOSITE."),
         ("kỹ thuật", "Chia thử tới sqrt(10^6).")],
    ),
    "hsgi-p14-lcmrange": vi_challenge(
        "BCNN đoạn",
        """**Bài toán.** lcm của mọi số trong [L, R], mod 10^9 + 7.""",
        [("1..4", "12."),
         ("8..10", "360."),
         ("kỹ thuật", "Mỗi nguyên tố p ≤ R: chọn p^e lớn nhất trong [L, R].")],
    ),
    "hsgi-p14-divisors": vi_challenge(
        "Số ước nhiều nhất",
        """**Bài toán.** d(n) cho n ≤ 10^12.""",
        [("12", "6 ước."),
         ("963761198400", "6720 ước."),
         ("kỹ thuật", "Phân tích + ∏(k+1).")],
    ),
    "hsgi-p14-modpowsum": vi_challenge(
        "Tổng luỹ thừa mô-đun",
        """**Bài toán.** a^b mod m với a, b tới 10^18, m ≤ 10^9.""",
        [("ví dụ", "2^10 mod 1000 = 24."),
         ("a > m", "Mod a trước."),
         ("m = 1", "0.")],
    ),
}

write_practice(
    M,
    "hsgi-p14-numth",
    "Number Theory Problem Set",
    "Five problems: π-counting sieve, big prime check, lcm of a range, divisor count, modular exponentiation.",
    "Bài tập lý thuyết số",
    "Năm bài: đếm nguyên tố bằng sàng, kiểm số lớn, BCNN đoạn, số ước, luỹ thừa mô-đun.",
    "hsgi-m14-modpow",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI14,
    solutions=[
        (
            "hsgi-p14-sievecount",
            CPP_STD + cpp("""    int Q; in >> Q;
    const int N = 10000000;
    vector<char> comp(N + 1, 0);
    vector<int> pi(N + 1, 0);
    for (int i = 2; i <= N; ++i) {
        if (!comp[i])
            for (long long j = (long long)i * i; j <= N; j += i) comp[j] = 1;
    }
    for (int i = 2; i <= N; ++i) pi[i] = pi[i-1] + (comp[i] ? 0 : 1);
    while (Q--) {
        int x; in >> x;
        out << pi[x] << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int Q; in >> Q;
    // near-miss: kiểm nguyên tố CHIA THỬ từng truy vấn — Q = 10^4 ×
    // N/ln N phép chia mỗi truy vấn → quá hạn tổng thể
    while (Q--) {
        int x; in >> x;
        int cnt = 0;
        for (int p = 2; p <= x; ++p) {
            bool ip = true;
            for (int d = 2; d * d <= p; ++d)
                if (p % d == 0) { ip = false; break; }
            cnt += ip;
        }
        out << cnt << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p14-primecheck",
            CPP_STD + cpp("""    int Q; in >> Q;
    while (Q--) {
        long long x; in >> x;
        bool ip = x >= 2;
        for (long long d = 2; d * d <= x && ip; d += (d == 2 ? 1 : 2))
            if (x % d == 0) ip = false;
        out << (ip ? "PRIME" : "COMPOSITE") << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int Q; in >> Q;
    while (Q--) {
        long long x; in >> x;
        // near-miss: d * d là NHÂN INT — d*d tràn khi d > ~46341, vòng
        // dừng sớm; hợp số có ước nhỏ nhất > 46341 (vd 104729²) bị
        // gọi nhầm PRIME
        int d = 2;
        bool ip = x >= 2;
        while (d * d <= x) {
            if (x % d == 0) { ip = false; break; }
            ++d;
        }
        out << (ip ? "PRIME" : "COMPOSITE") << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p14-lcmrange",
            CPP_STD + cpp("""    long long L, R; in >> L >> R;
    const long long MOD = 1000000007;
    const int N = 1000000;
    vector<char> comp(N + 1, 0);
    for (int i = 2; i <= N; ++i)
        if (!comp[i])
            for (long long j = (long long)i * i; j <= N; j += i) comp[j] = 1;
    long long ans = 1;
    for (long long p = 2; p <= R; ++p) {
        if (comp[p]) continue;
        // luỹ thừa p^e LỚN NHẤT có bội trong [L, R]:
        // bội của pw trong đoạn tồn tại ⇔ floor(R/pw) ≥ ceil(L/pw)
        long long best = 1, pw = 1;
        while (pw * p <= R) {
            pw *= p;
            if (R / pw >= (L + pw - 1) / pw) best = pw;
        }
        if (best > 1) ans = ans % MOD * (best % MOD) % MOD;
    }
    out << ans << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long L, R; in >> L >> R;
    const long long MOD = 1000000007;
    // near-miss: NHÂN TỪNG SỐ trong đoạn với mod — lcm KHÔNG phải tích
    // mod: 8,9,10 → tích mod = 720/2? — kết quả sai mọi đoạn dài
    long long ans = 1;
    for (long long x = L; x <= R; ++x)
        ans = ans % MOD * (x % MOD) % MOD;
    out << ans << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p14-divisors",
            CPP_STD + cpp("""    int Q; in >> Q;
    while (Q--) {
        long long n; in >> n;
        long long total = 1;
        for (long long d = 2; d * d <= n; ++d) {
            if (n % d == 0) {
                int k = 0;
                while (n % d == 0) { n /= d; ++k; }
                total *= (k + 1);
            }
        }
        if (n > 1) total *= 2;
        out << total << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int Q; in >> Q;
    while (Q--) {
        long long n; in >> n;
        // near-miss: LIỆT KÊ ước tới sqrt rồi ×2 — số CHÍNH PHƯƠNG bị
        // đếm thừa 1 (ước căn được tính hai lần)
        long long cnt = 0;
        for (long long d = 1; d * d <= n; ++d)
            if (n % d == 0) cnt += 2;
        out << cnt << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p14-modpowsum",
            CPP_STD + cpp("""    int Q; in >> Q;
    while (Q--) {
        long long a, b, m; in >> a >> b >> m;
        long long r = 1 % m;
        a %= m;
        while (b > 0) {
            if (b & 1) r = r * a % m;
            a = a * a % m;
            b >>= 1;
        }
        out << r << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int Q; in >> Q;
    while (Q--) {
        long long a, b, m; in >> a >> b >> m;
        // near-miss: nhân dần O(b) — b tới 10^18 → quá hạn tức thì
        long long r = 1 % m;
        for (long long i = 0; i < b; ++i) r = r * (a % m) % m;
        out << r << "{{NL}}";
    }
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH14 = challenge(
    "hsgi-cp-m14-fence",
    "Checkpoint — Hàng rào nguyên tố",
    """**Bài toán.** Khu vườn có dãy hàng rào đánh số 1..N. Ông chủ muốn
biết với mỗi truy vấn (L, R): trong đoạn hàng [L, R] có bao nhiêu cột
NGUYÊN TỐ mang số chính xác p với p nguyên tố và L ≤ p ≤ R. In tổng
số cột (mỗi truy vấn một dòng).

**Ràng buộc:** 1 ≤ Q ≤ 10^4; 1 ≤ L ≤ R ≤ 10^7.""",
    [
        contest_test(
            "ví dụ",
            T("3", "1 10", "10 20", "2 3"),
            T("4", "4", "2"),
            "π ≤ 10: 2,3,5,7 → 4; trong 10..20: 11,13,17,19 → 4; 2,3 → 2.",
        ),
        contest_test(
            "R = 10^7",
            T("10") + T(*["1 10000000"] * 10),
            T(*["664579"] * 10),
            "Mười truy vấn toàn dải: π(10^7) = 664579 — sàng + tiền tố trả ngay; quét-từng-đoạn 10 lần → quá hạn chắc chắn.",
        ),
        contest_test(
            "truy vấn điểm",
            T("2", "7 7", "9 9"),
            T("1", "0"),
            "7 nguyên tố; 9 không.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP14 = vi_challenge(
    "Checkpoint — Hàng rào nguyên tố",
    """**Bài toán.** Q truy vấn (L, R) ≤ 10^7: số nguyên tố trong
đoạn.""",
        [("ví dụ", "1..10 → 4."),
         ("R = 10^7", "664579."),
         ("kỹ thuật", "Sàng + tiền tố π.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m14",
    "Checkpoint — Number Theory",
    "Pass the graded problem to finish the number theory module.",
    25,
    """**Checkpoint — Number Theory.** Pass the graded challenge: prime
counts over ranges — sieve once, prefix-sum π, answer each query in
O(1). Per-query trial division is the hunted timeout.

**Điểm kiểm tra — Lý thuyết số.** Pass bài chấm: đếm nguyên tố trong
đoạn — sàng một lần, tiền tố π, trả O(1). Chia thử từng truy vấn là
quá hạn bị săn.""",
    "Checkpoint — Number Theory",
    "Pass bài chấm để hoàn thành module lý thuyết số.",
    """**Điểm kiểm tra — Lý thuyết số.** Pass bài chấm bên dưới: đếm số
nguyên tố trong đoạn [L, R] với nhiều truy vấn.""",
    CH14,
    VI_CP14,
    solution=CPP_STD + cpp("""    int Q; in >> Q;
    const int N = 10000000;
    vector<char> comp(N + 1, 0);
    vector<int> pi(N + 1, 0);
    for (int i = 2; i <= N; ++i)
        if (!comp[i])
            for (long long j = (long long)i * i; j <= N; j += i) comp[j] = 1;
    for (int i = 2; i <= N; ++i) pi[i] = pi[i-1] + (comp[i] ? 0 : 1);
    while (Q--) {
        int L, R; in >> L >> R;
        out << pi[R] - pi[L - 1] << "{{NL}}";
    }
""") + END,
    wrong=CPP_STD + cpp("""    int Q; in >> Q;
    // near-miss: kiểm từng số trong đoạn bằng chia thử — mỗi truy vấn
    // (R − L)·sqrt(R) phép; Q = 10^4 truy vấn toàn dải → quá hạn
    while (Q--) {
        int L, R; in >> L >> R;
        int cnt = 0;
        for (int x = L; x <= R; ++x) {
            bool ip = x >= 2;
            for (long long d = 2; d * d <= x && ip; ++d)
                if (x % d == 0) ip = false;
            cnt += ip;
        }
        out << cnt << "{{NL}}";
    }
""") + END,
)
