#!/usr/bin/env python3
"""HSG Intensive — Module 11: hsgx-editorials (Editorial Training).

How to study an editorial the way strong competitors do: attempt → stall →
read the OBSERVATION (not the code) → re-derive → re-implement clean → solve
the variation. Each lesson-attached problem ships with a full editorial
structured as: Observation → Brute force → Why it fails → Key insight →
Optimization → Complexity → Common wrong approaches. The "variation" is a
second challenge whose statement shares the same core idea in a new skin.

Conventions (m9 style): local T()/cpp()/CPP_STD; explicit includes;
per-line outputs get per-line wants; big-test ground truths computed here.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgx import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge, contest_test

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
#include <utility>
#include <map>
#include <set>
#include <tuple>
#include <queue>
#include <functional>
#include <climits>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")
END = cpp("}")


# ------------------------------------------------------------------ module
M = "hsgx-editorials"

write_module(
    M,
    "Editorials, Re-solving, and Variations",
    "The attempt-first workflow: stall honestly, read the observation (never the code first), re-implement clean, then kill the variation.",
    "Lời giải, Giải lại, và Bài biến thể",
    "Quy trình thử-trước: bí trung thực, đọc phần nhận xét (chưa bao giờ đọc code trước), cài lại sạch, rồi hạ bài biến thể.",
    ["hsgx-m11-editorial-protocol", "hsgx-cp-m11-editorial"],
    ["hsgx-p11-editorial"],
)


# ------------------------------------------------------------------ lesson 1
L1_MDX = """
## The Editorial Protocol

Reading editorials badly is a skill leak: you nod, you move on, the next
unfamiliar problem destroys you anyway. The protocol below turns an editorial
into training.

### The stall rule

Do not open the editorial until you have a **stalled attempt**: a concrete
brute force written down, its bottleneck measured or clearly identified, and
at least 30 minutes of real attack on that bottleneck. Reading after a real
stall works; reading after five minutes teaches nothing.

### Reading order — never linear

1. **Observation section only.** Close the tab. Re-derive the algorithm from
   the observation alone.
2. **Complexity line.** Does your derivation match? If theirs is O(n log n)
   and yours is O(n log² n), find the missing trick *before* reading code.
3. **Implementation only when stuck.** The code is the *last* section. If
   you need it, you are copying an idea you have not understood yet — go
   back to step 1.
4. **Common wrong approaches.** Read these even when you solved it: the
   near-misses are where the next contest's WA lives.

### The re-solve

Close everything. Re-implement the solution from a blank editor. If you
cannot, you read a solution; you did not learn an idea. Then solve the
**variation** below — same core insight, different statement. If the
variation stalls you again, the insight did not transfer; re-derive it.

### Two worked examples ship with this module

Both follow the exact structure: Observation → Brute force → Why it fails →
Key insight → Optimization → Complexity → Common wrong approaches. Use them
as templates for post-contest editorial study — including self-written
editorials for problems you *did* solve, which is how the proof habit forms.
"""

L1_VI_MDX = """
## Quy Trình Đọc Lời Giải

Đọc lời giải sai cách là rò rỉ kỹ năng: bạn gật gù, đi tiếp, rồi bài lạ kế
tiếp vẫn hạ được bạn. Quy trình dưới đây biến lời giải thành bài tập.

### Luật bí

Không mở lời giải khi chưa có **một lần thử bị kẹt**: một brute force cụ thể
được viết ra, điểm nghẽn được đo hoặc chỉ rõ, và ít nhất 30 phút tấn công
thật vào điểm nghẽn đó. Đọc sau khi bí thật thì có tác dụng; đọc sau năm
phút thì không dạy được gì.

### Thứ tự đọc — không bao giờ đọc tuyến tính

1. **Chỉ phần nhận xét.** Đóng tab. Tự suy lại thuật toán từ nhận xét đó.
2. **Dòng độ phức tạp.** Suy diễn của bạn có khớp không? Nếu họ O(n log n)
   mà bạn O(n log² n), tìm mẹo còn thiếu *trước khi* đọc code.
3. **Cài đặt chỉ khi bí thật sự.** Code là phần cuối. Nếu bạn cần nó, bạn
   đang chép một ý chưa hiểu — quay lại bước 1.
4. **Các hướng đi sai thường gặp.** Đọc cả khi bạn đã giải được: những cú
   suýt trượt chính là nơi WA của vòng thi kế tiếp trú ngụ.

### Giải lại

Đóng hết mọi thứ. Cài lại lời giải từ trang trắng. Nếu không làm được, bạn
vừa đọc một lời giải chứ chưa học một ý tưởng. Sau đó giải **bài biến thể**
bên dưới — cùng ý lõi, đề khác. Nếu biến thể vẫn làm bạn bí, ý tưởng chưa
chuyển giao; suy lại từ đầu.

### Hai ví dụ mẫu đi kèm module

Cả hai theo đúng cấu trúc: Nhận xét → Brute force → Vì sao gãy → Ý chính →
Tối ưu → Độ phức tạp → Các hướng sai thường gặp. Dùng chúng làm khuôn để
đọc lời giải sau vòng thi — kể cả tự viết lời giải cho bài mình *đã* giải,
đó là cách hình thành thói quen chứng minh.
"""

write_lesson(
    M, "hsgx-m11-editorial-protocol", "The Editorial Protocol",
    "Attempt-first editorial study: stall rule, observation-first reading, clean re-implementation, variation transfer.",
    15, L1_MDX,
    "Quy Trình Đọc Lời Giải",
    "Đọc lời giải kiểu thử-trước: luật bí, đọc nhận xét trước, cài lại sạch, chuyển giao qua biến thể.",
    L1_VI_MDX,
)


# ================================================================ worked example 1
# Problem: max sum of a non-adjacent subset (classic; the editorial teaches
# the "drop dimension" insight). Variation: circular version.
E1_SMALL = "40"   # [3,2,5,10,7] → 3+5+7=15? no — 3+10? non-adjacent: {3,5,7}=15? {2,10}? → 3+10? indices 0,3 → 13; {0,2,4}=15; {3}=10 → 15
E1_TRAP = "103"   # adjacent-pair trap below

E1_CH = challenge(
    "hsgx-p11-e1-nonadjacent",
    "Editorial Problem 1: The Stalls",
    """**Bài toán.** A market has n stalls in a row; stall i brings a[i] revenue.
Security forbids operating two *adjacent* stalls. Choose a subset of
non-adjacent stalls with maximum total revenue; print it.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ a[i] ≤ 10^9.

**Input:** line 1: n; line 2: n values.
**Output:** one integer.
""",
    [
        contest_test("sample", T("5", "3 2 5 10 7"), T("15"),
            "Stalls 1,3,5 → 3+5+7 = 15 beats 3+10=13 and 10 alone."),
        contest_test("two", T("2", "9 4"), T("9"), "Pick the better one."),
        contest_test("zeros", T("3", "0 0 0"), T("0"), "Empty set is allowed (revenue 0)."),
        contest_test("single", T("1", "8"), T("8"), "One stall."),
    ],
    level="independent",
    difficulty="advanced",
)

E1_VI = vi_challenge(
    "Lời giải 1: Các Sạp Hàng",
    """**Bài toán.** Một khu chợ có n sạp xếp thành hàng; sạp i mang doanh thu a[i].
An ninh cấm vận hành hai sạp *kề nhau*. Chọn tập sạp không kề có tổng doanh
thu lớn nhất; in tổng đó.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ a[i] ≤ 10^9.

**Input:** dòng 1: n; dòng 2: n giá trị.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "Sạp 1,3,5 → 3+5+7 = 15 thắng 3+10=13 và 10 một mình."),
        ("hai sạp", "Chọn sạp tốt hơn."),
        ("toàn 0", "Chọn tập rũng được (doanh thu 0)."),
        ("một sạp", "Lấy sạp đó."),
    ],
)

E1_R = CPP_STD + cpp("""    long long n; in >> n;
    long long take = 0, skip = 0;   // take: best including current; skip: excluding
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        long long nt = skip + x;          // operate this stall
        long long ns = max(take, skip);   // don't
        take = nt; skip = ns;
    }
    out << max(take, skip) << "{{NL}}";
""") + END

E1_W = CPP_STD + cpp("""    long long n; in >> n;
    // WRONG: greedy by value — take the largest, ban its neighbors, repeat.
    // Fails [2, 3, 2]-style arrangements: greedy 3; optimal 2+2=4.
    vector<pair<long long,long long>> v;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        v.push_back({x, i});
    }
    sort(v.rbegin(), v.rend());
    vector<char> banned(n, 0);
    long long total = 0;
    for (auto& [val, i] : v) {
        if (banned[i]) continue;
        total += val;
        if (i > 0) banned[i - 1] = 1;
        if (i + 1 < n) banned[i + 1] = 1;
    }
    out << total << "{{NL}}";
""") + END

# the greedy trap test that discriminates: [2, 3, 2]
# (appended as a dict — contest_test returns a tuple and challenge() already
# converted the original list, so post-hoc appends must be dicts)
_t = contest_test(
    "greedy trap", T("3", "2 3 2"), T("4"),
    "Greedy takes 3 and bans both 2s → 3; optimal is 2+2 = 4.",
)
E1_CH["tests"].append({"name": _t[0], "code": _t[1], "hint": _t[2]})
E1_VI["tests"].append(("bẫy tham lam", "Tham lấy 3 và cấm cả hai sạp 2 → 3; tối ưu 2+2 = 4."))


# ================================================================ worked example 2
# Problem: count subarrays whose XOR is zero (prefix-XOR map).
E2_CH = challenge(
    "hsgx-p11-e2-xorzero",
    "Editorial Problem 2: The Gates",
    """**Bài toán.** A circuit row has n gates; gate i has state a[i] (a non-negative
integer). A *stable segment* is a contiguous segment whose XOR of states is
zero. Count stable segments.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ a[i] < 2^20.

**Input:** line 1: n; line 2: n values.
**Output:** one integer — the count (fits in 64 bits).
""",
    [
        contest_test("sample", T("5", "4 3 7 4 4"), T("4"),
            "Prefix XOR 4,7,0,4,0: equal-prefix pairs → [4,3,7], [4,3,7,4,4], [3,7,4], [4,4] → 4."),
        contest_test("zero gate", T("1", "0"), T("1"), "A single 0 gate is stable."),
        contest_test("no stable", T("3", "1 2 4"), T("0"), "Prefixes 1,3,7 all distinct."),
    ],
    level="independent",
    difficulty="advanced",
)

E2_VI = vi_challenge(
    "Lời giải 2: Cổng Logic",
    """**Bài toán.** Một hàng mạch có n cổng; cổng i có trạng thái a[i] (số nguyên
không âm). *Đoạn ổn định* là đoạn liên tiếp có XOR trạng thái bằng 0. Đếm
số đoạn ổn định.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ a[i] < 2^20.

**Input:** dòng 1: n; dòng 2: n giá trị.
**Output:** một số nguyên — số lượng (vừa 64-bit).
""",
    [
        ("ví dụ", "Prefix XOR 4,7,0,4,0: các cặp prefix bằng nhau → [4,3,7], [4,3,7,4,4], [3,7,4], [4,4] → 4."),
        ("cổng 0", "Một cổng 0 đơn lẻ là ổn định."),
        ("không ổn định", "Prefix 1,3,7 đôi một khác nhau."),
    ],
)

# Verify the sample truth with Python before shipping.
def _e2_check():
    a = [4, 3, 7, 4, 4]
    cnt = 0
    for i in range(len(a)):
        x = 0
        for j in range(i, len(a)):
            x ^= a[j]
            if x == 0:
                cnt += 1
    return cnt

E2_S = _e2_check()
assert E2_S == 4, f"E2 sample truth is {E2_S}"

E2_R = CPP_STD + cpp("""    long long n; in >> n;
    map<long long, long long> cnt;
    cnt[0] = 1;
    long long s = 0, ans = 0;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        s ^= x;
        auto it = cnt.find(s);
        if (it != cnt.end()) ans += it->second;
        ++cnt[s];
    }
    out << ans << "{{NL}}";
""") + END

E2_W = CPP_STD + cpp("""    long long n; in >> n;
    // WRONG: counts only segments of length ≤ 2 with zero XOR (a[i]=0 or
    // a[i]==a[i+1]) — the prefix-repeat structure goes unseen.
    long long ans = 0;
    long long prev = -1;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        if (x == 0) ++ans;
        if (prev == x) ++ans;
        prev = x;
    }
    out << ans << "{{NL}}";
""") + END

_t = contest_test(
    "long stable", T("6", "1 2 3 1 2 3"), T("5"),
    "Prefix XOR with pre0: 0,1,3,0,1,3,0 → 0 repeats 3× (3 pairs), 1 twice (1), 3 twice (1) → 5 stable segments.",
)
E2_CH["tests"].append({"name": _t[0], "code": _t[1], "hint": _t[2]})
E2_VI["tests"].append(("ổn định dài", "Prefix XOR gồm pre0: 0,1,3,0,1,3,0 → 0 lặp 3 lần (3 cặp), 1 hai lần (1), 3 hai lần (1) → 5 đoạn ổn định."))


# ------------------------------------------------------------------ practice
write_practice(
    M, "hsgx-p11-editorial",
    "Editorial Problems and Variations",
    "Two editorial-tier problems (non-adjacent max revenue; zero-XOR segments), each with a hidden variation in the checkpoint lesson. Solve blind first; the editorials are in the lesson pages.",
    "Bài Lời Giải và Biến Thể",
    "Hai bài tầm lời giải (doanh thu không kề lớn nhất; đoạn XOR-zero), mỗi bài có một biến thể giấu trong bài học điểm kiểm tra. Giải mù trước; lời giải nằm trong trang bài học.",
    "hsgx-m11-editorial-protocol",
    90,
    "advanced",
    [E1_CH, E2_CH],
    [E1_VI, E2_VI],
    solutions=[
        ("hsgx-p11-e1-nonadjacent", E1_R, E1_W),
        ("hsgx-p11-e2-xorzero", E2_R, E2_W),
    ],
)


# ================================================================ variations
# V1: circular version of E1 — the variation challenge.
def _v1_ground():
    ring = [1 + (i * 29) % 999999 for i in range(1, 200001)]
    n = len(ring)
    # circular non-adjacent max: linear twice — exclude first, or exclude last
    def linear(a):
        take = skip = 0
        for x in a:
            take, skip = skip + x, max(take, skip)
        return max(take, skip)
    return max(linear(ring[1:]), linear(ring[:-1]))

V1_BIG = _v1_ground()

V1_CH = challenge(
    "hsgx-p11-v1-circular",
    "Variation 1: The Round Table",
    """**Bài toán.** Same market rules, but the stalls are arranged in a **circle**:
stall n is adjacent to stall 1. Choose a non-adjacent subset with maximum
total revenue.

**Constraints:** 2 ≤ n ≤ 200000; 0 ≤ a[i] ≤ 10^6.

**Input:** line 1: n; line 2: n values.
**Output:** one integer.
""",
    [
        contest_test("sample", T("4", "9 1 1 9"), T("10"),
            "Stalls 1 and 3 → 9+1 = 10; the two ends are ring-adjacent, so 9+9 = 18 is illegal — the linear wrong reports 18."),
        contest_test("all equal", T("4", "3 3 3 3"), T("6"), "Opposite pair."),
        contest_test("two stalls", T("2", "7 9"), T("9"),
            "In a 2-ring the stalls are adjacent (twice over) → only one can run."),
        contest_test("full scale", T("200000", " ".join(str(1 + (i * 29) % 999999) for i in range(1, 200001))), T(str(V1_BIG)),
            "Case split: the answer never uses both endpoints — two linear passes."),
    ],
    level="combination",
    difficulty="advanced",
)

V1_VI = vi_challenge(
    "Biến thể 1: Bàn Tròn",
    """**Bài toán.** Cùng luật chợ, nhưng các sạp xếp thành **vòng tròn**: sạp n kề
sạp 1. Chọn tập không kề có tổng doanh thu lớn nhất.

**Ràng buộc:** 2 ≤ n ≤ 200000; 0 ≤ a[i] ≤ 10^6.

**Input:** dòng 1: n; dòng 2: n giá trị.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "Sạp 1 và 3 → 9+1 = 10; hai đầu kề nhau trong vòng nên 9+9 = 18 bất hợp pháp — lời giải tuyến tính sai báo 18."),
        ("toàn bằng", "Cặp đối diện."),
        ("hai sạp", "Vòng 2 sạp coi như kề nhau (kép) → chỉ một sạp chạy được."),
        ("quy mô đầy đủ", "Chia trường hợp: đáp án không bao giờ dùng cả hai đầu — hai lượt tuyến tính."),
    ],
)

V1_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    auto linear = [](vector<long long>& v) {
        long long take = 0, skip = 0;
        for (long long x : v) {
            long long nt = skip + x, ns = max(take, skip);
            take = nt; skip = ns;
        }
        return max(take, skip);
    };
    // The answer cannot use a[0] and a[n-1] together: try excluding each.
    vector<long long> skipFirst(a.begin() + 1, a.end());
    vector<long long> skipLast(a.begin(), a.end() - 1);
    out << max(linear(skipFirst), linear(skipLast)) << "{{NL}}";
""") + END

V1_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: ignores the ring — plain linear non-adjacent max treats the
    // two ends as non-adjacent, overcounting configurations like [5,1,5,1].
    long long take = 0, skip = 0;
    for (long long x : a) {
        long long nt = skip + x, ns = max(take, skip);
        take = nt; skip = ns;
    }
    out << max(take, skip) << "{{NL}}";
""") + END


# V2: variation of E2 — count subarrays with XOR exactly K (not zero).
def _v2_ground():
    from collections import defaultdict
    n = 200000
    a = [(i * 31 + 5) % (1 << 20) for i in range(1, n + 1)]
    K = 12345
    cnt = defaultdict(int)
    cnt[0] = 1
    s = 0
    ans = 0
    for x in a:
        s ^= x
        ans += cnt[s ^ K]
        cnt[s] += 1
    return ans

V2_BIG = _v2_ground()

V2_CH = challenge(
    "hsgx-p11-v2-xork",
    "Variation 2: The Filtered Gates",
    """**Bài toán.** Same circuit row, but a segment is *useful* when the XOR of
its states equals exactly K. Count useful segments.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ a[i] < 2^20; 0 ≤ K < 2^20.

**Input:** line 1: n, K; line 2: n values.
**Output:** one integer — the count (fits in 64 bits).
""",
    [
        contest_test("sample", T("4 3", "1 2 3 4"), T("2"),
            "Prefix XOR 1,3,0,4 → segments with XOR 3: [1,2], [3] → 2."),
        contest_test("k zero", T("3 0", "5 0 5"), T("2"), "[0] and [5,0,5]... verify: prefixes 5,5,0 → pairs (5@1,5@2)=1 seg, (0@0,0@3)=1 seg → 2."),
        contest_test("full scale", T("200000 12345", " ".join(str((i * 31 + 5) % (1 << 20)) for i in range(1, 200001))), T(str(V2_BIG)),
            "The zero case generalized: count earlier prefixes equal to s⊕K."),
    ],
    level="combination",
    difficulty="advanced",
)

V2_VI = vi_challenge(
    "Biến thể 2: Cổng Lọc",
    """**Bài toán.** Cùng hàng mạch, nhưng một đoạn *hữu ích* khi XOR trạng thái của
nó đúng bằng K. Đếm đoạn hữu ích.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ a[i] < 2^20; 0 ≤ K < 2^20.

**Input:** dòng 1: n, K; dòng 2: n giá trị.
**Output:** một số nguyên — số lượng (vừa 64-bit).
""",
    [
        ("ví dụ", "Prefix XOR 1,3,0,4 → các đoạn XOR 3: [1,2] và [3] → 2."),
        ("k bằng 0", "Prefix 5,5,0 → cặp (5@1,5@2)=1 đoạn, (0@0,0@3)=1 đoạn → 2."),
        ("quy mô đầy đủ", "Trường hợp zero tổng quát: đếm prefix trước đó bằng s⊕K."),
    ],
)

# verify the two small truths in Python
def _v2_check():
    a = [1, 2, 3, 4]
    K = 3
    cnt = 0
    for i in range(len(a)):
        x = 0
        for j in range(i, len(a)):
            x ^= a[j]
            if x == K:
                cnt += 1
    return cnt

V2_S = _v2_check()
assert V2_S == 2, f"V2 sample truth {V2_S}"

V2_R = CPP_STD + cpp("""    long long n, K; in >> n >> K;
    map<long long, long long> cnt;
    cnt[0] = 1;
    long long s = 0, ans = 0;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        s ^= x;
        auto it = cnt.find(s ^ K);
        if (it != cnt.end()) ans += it->second;
        ++cnt[s];
    }
    out << ans << "{{NL}}";
""") + END

V2_W = CPP_STD + cpp("""    long long n, K; in >> n >> K;
    map<long long, long long> cnt;
    cnt[0] = 1;
    long long s = 0, ans = 0;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        s ^= x;
        auto it = cnt.find(s - K);   // WRONG: subtraction instead of XOR —
                                     // only coincides when K's bits never overlap s.
        if (it != cnt.end()) ans += it->second;
        ++cnt[s];
    }
    out << ans << "{{NL}}";
""") + END


# ------------------------------------------------------------------ checkpoint
# The checkpoint problem's lesson page IS the editorial — students must first
# attempt the practice problems above; the page follows the full structure.
CP_MDX = """
**Điểm kiểm tra — Lời giải mẫu.** Before reading further: both practice
problems above should already be attempted (stalled or solved). This page
holds the full editorial for **Problem 1 (The Stalls)** in the canonical
structure — use it to calibrate how you write and read editorials.

## Editorial: The Stalls (non-adjacent max revenue)

**Observation.** For each stall the decision "operate or not" depends only
on the neighbor decision — a single pass of two states suffices.

**Brute force.** All 2^n subsets with an adjacency filter: correct, 2^20
minimum, dead on arrival at n = 200000.

**Why it fails.** Overlapping subproblems: every suffix decision repeats
across exponentially many prefixes.

**Key insight.** Keep two numbers: best revenue *operating* the current
stall (`take`) and *not operating* it (`skip`). Recurrence:
`take = skip + a[i]`, `skip = max(take_prev, skip_prev)`.

**Optimization.** None needed beyond O(n) time, O(1) memory.

**Complexity.** O(n) time, O(1) extra space.

**Common wrong approaches.**
- *Greedy by value* (take the biggest, ban neighbors): fails [2,3,2] →
  greedy 3, optimal 4. The practice test catches it.
- *Parity assumptions*: "take every other stall" fails whenever values vary.

## The variation

The Round Table (circular) removes a single assumption — that the row has
two ends. The fix is a case split, not a new algorithm: the optimal ring
answer never uses both endpoints, so run the linear solver twice, excluding
each endpoint in turn. If your first ring attempt patched the recurrence
itself, note what that felt like — patching a working tool is usually the
wrong move; questioning the tool's *assumption* is the right one.
"""

CP_VI_MDX = """
**Điểm kiểm tra — Lời giải mẫu.** Trước khi đọc tiếp: hai bài luyện phía trên
phải đã được thử (bí hoặc giải xong). Trang này chứa lời giải đầy đủ cho
**Bài 1 (Các Sạp Hàng)** theo cấu trúc chuẩn — dùng nó để hiệu chỉnh cách
bạn viết và đọc lời giải.

## Lời giải: Các Sạp Hàng (doanh thu không kề lớn nhất)

**Nhận xét.** Với mỗi sạp, quyết định "mở hay không" chỉ phụ thuộc quyết định
của sạp kề — một lượt duy nhất với hai trạng thái là đủ.

**Brute force.** Toàn bộ 2^n tập con kèm bộ lọc kề: đúng, nhưng tối thiểu
2^20 — chết ngay khi n = 200000.

**Vì sao gãy.** Bài toán con chồng lấn: quyết định của mỗi đoạn đuôi lặp lại
qua vô số đoạn đầu theo cấp số nhân.

**Ý chính.** Giữ hai số: doanh thu tốt nhất khi *mở* sạp hiện tại (`take`) và
*khi không mở* (`skip`). Công thức: `take = skip + a[i]`,
`skip = max(take_prev, skip_prev)`.

**Tối ưu.** Không cần gì ngoài O(n) thời gian, O(1) bộ nhớ.

**Độ phức tạp.** O(n) thời gian, O(1) bộ nhớ phụ.

**Các hướng sai thường gặp.**
- *Tham theo giá trị* (lấy to nhất, cấm hàng xóm): gãy ở [2,3,2] → tham 3,
  tối ưu 4. Bài luyện bắt được nó.
- *Giả định tính chẵn lẻ*: "lấy sạp cách nhau một" gãy ngay khi giá trị dao động.

## Bài biến thể

Bàn Tròn (vòng tròn) chỉ bỏ một giả định — rằng dãy có hai đầu. Cách sửa là
chia trường hợp, không phải thuật toán mới: đáp án vòng tròn tối ưu không
bao giờ dùng cả hai đầu, nên chạy bộ giải tuyến tính hai lần, mỗi lần loại
một đầu. Nếu lần đầu bạn vá chính công thức truy hồi, hãy nhớ cảm giác đó —
vá một công cụ đang chạy thường là nước sai; hỏi lại *giả định* của công cụ
mới là nước đúng.
"""

write_checkpoint(
    M, "hsgx-cp-m11-editorial",
    "Checkpoint — Editorial Calibrated",
    "The full editorial for The Stalls, the variation transfer lesson, and the round-table variation as the checkpoint challenge.",
    45,
    CP_MDX,
    "Điểm kiểm tra — Lời Giải Chuẩn Hóa",
    "Lời giải đầy đủ cho Các Sạp Hàng, bài học chuyển giao biến thể, và bài biến thể bàn tròn làm thử thách điểm kiểm tra.",
    CP_VI_MDX,
    V1_CH, V1_VI,
    V1_R, V1_W,
)

print("module m11 complete")
