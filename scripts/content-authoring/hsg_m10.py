#!/usr/bin/env python3
"""HSG — Module 10: hsg-strings.

std::string mechanics, char classification, palindrome drills, run-length
encoding, anagram sorting signatures, and counting distinct substrings with
brute force plus a set (honestly labeled O(n^3) memory/time — beginner
constraints only). Conventions: T() for test I/O, cpp() for bodies.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
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
#include <string>
#include <vector>
#include <set>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsg-strings"
write_module(
    M,
    "Strings",
    "std::string mechanics: indexing, traversal, palindromes, run-length encoding, anagram signatures, and a first honest look at counting distinct substrings.",
    "Chuỗi",
    "Cơ chế std::string: chỉ số, duyệt, đối xứng, mã hóa chạy dài, chữ ký hoán vị, và lần đầu nhìn thẳng vào việc đếm xâu con phân biệt.",
    ["hsg-m10-basics", "hsg-m10-transform", "hsg-cp-m10"],
    ["hsg-p10-strings"],
)

write_lesson(
    M,
    "hsg-m10-basics",
    "String Mechanics",
    "Indexing, traversal, building strings efficiently, and the contest-style char categories.",
    14,
    """## A string is an array of chars with extras

```cpp
string s = "loi choi";     // s[0] == 'l', s.size() == 8
for (char c : s) ...       // read-only traversal
for (char& c : s) c = toupper(c);   // in-place edit
```

`char` is a small integer: 'a' is 97, '0' is 48. So `c - '0'` converts a
digit character to its value, and `c - 'a'` maps lowercase letters to
0..25 — the bridge into marking arrays for letters.

### Building strings

```cpp
string t;
t += c;          // amortized O(1) per char
t += "abc";      // append a literal
t.push_back('x'); // same as += for a single char
```

Repeated `t = t + c` in a loop is the classic slow version — each
iteration copies the whole string, making the loop O(n^2). With n at
10^5 that is a TLE. Use `+=`.

### Reading input

`cin >> s` reads one whitespace-delimited token. `getline(cin, s)` reads
a whole line including spaces (and strips the newline). Mixing them is
the classic beginner trap: after `cin >> n`, the newline stays in the
buffer, so the next `getline` returns an empty string. Either use
`cin.ignore()` after `>>` or read everything with getline.

### Character categories

`isdigit`, `isalpha`, `islower`, `isupper`, `tolower`, `toupper` from
`<cctype>`: they take an int (pass the char, cast if your warnings are
pedantic) and return the classified/converted result. In contests these
replace a hand-rolled if-chain, nothing more.
""",
    "Cơ chế xâu ký tự",
    "Chỉ số, duyệt, dựng xâu hiệu quả, và các nhóm ký tự kiểu thi đấu.",
    """## Xâu là mảng char kèm tiện ích

```cpp
string s = "loi choi";     // s[0] == 'l', s.size() == 8
for (char c : s) ...       // duyệt chỉ đọc
for (char& c : s) c = toupper(c);   // sửa tại chỗ
```

`char` là số nguyên nhỏ: 'a' là 97, '0' là 48. Nên `c - '0'` đổi ký tự
số thành giá trị, và `c - 'a'` ánh xạ chữ thường về 0..25 — cây cầu vào
mảng đánh dấu cho chữ cái.

### Dựng xâu

```cpp
string t;
t += c;          // khấu hao O(1) mỗi ký tự
t += "abc";      // nối một literal
t.push_back('x'); // với một ký tự thì giống +=
```

Kiểu `t = t + c` trong vòng lặp là phiên bản chậm kinh điển — mỗi vòng
chép toàn bộ xâu, cả vòng là O(n^2). Với n bằng 10^5 là TLE. Dùng `+=`.

### Đọc input

`cin >> s` đọc một token cách nhau bởi khoảng trắng. `getline(cin, s)`
đọc cả dòng kể cả dấu cách (và bỏ dấu xuống dòng). Trộn hai kiểu là bẫy
kinh điển: sau `cin >> n`, dấu xuống dòng còn nằm trong buffer, nên
`getline` kế tiếp trả về xâu rỗng. Hoặc `cin.ignore()` sau `>>`, hoặc
đọc toàn bộ bằng getline.

### Nhóm ký tự

`isdigit`, `isalpha`, `islower`, `isupper`, `tolower`, `toupper` từ
`<cctype>`: nhận int (truyền char, ép kiểu nếu warning gắt) và trả kết
quả phân loại/chuyển đổi. Trong thi đấu chúng thay chuỗi if thủ công,
không hơn.
""",
)

write_lesson(
    M,
    "hsg-m10-transform",
    "String Transformations",
    "Palindrome checks, run-length encoding, anagram signatures — three patterns that solve dozens of beginner problems.",
    13,
    """## Palindrome: two pointers on a string

```cpp
bool pal(const string& s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j)
        if (s[i++] != s[j--]) return false;
    return true;
}
```

O(n), O(1) extra space. Variant drills: ignore case (normalize first),
ignore non-letters (filter first), longest palindromic **substring** by
expanding around each center — O(n^2), fine for n at a few thousand.

## Run-length encoding

```cpp
string rle(const string& s) {
    string out;
    for (int i = 0; i < (int)s.size(); ) {
        int j = i;
        while (j < (int)s.size() && s[j] == s[i]) ++j;
        out += s[i];
        out += to_string(j - i);
        i = j;
    }
    return out;
}
```

"aaabbc" becomes "a3b2c1". The outer loop jumps whole runs via `i = j` —
a template worth memorizing for all "group consecutive elements" problems.

## Anagram signature

Two strings are anagrams iff sorting them is equal: `sort(a); sort(b);
a == b`. O(n log n) and short. The alternative — 26-slot frequency
arrays — is O(n) and generalizes to "how many anagrams of x are in s"
(sliding window over 26 counts). Choose by problem shape, not by habit.

## Counting distinct substrings — an honest ceiling

For a string of length n there are n(n+1)/2 substrings. Inserting every
one into a `set<string>` costs O(n^2) strings of average length O(n):
O(n^3) time and memory in the worst case. For n = 100 that is fine
(~5000 substrings, short). For n = 1000 it is already dangerous; for
n = 10^5 impossible. Beginner problems that ask this will give tiny n —
read the constraint, then pick the tool. (Suffix automaton arrives much,
much later.)
""",
    "Biến đổi xâu",
    "Kiểm tra đối xứng, mã hóa chạy dài, chữ ký hoán vị — ba mẫu giải hàng chục bài tập người mới.",
    """## Đối xứng: hai con trỏ trên xâu

```cpp
bool pal(const string& s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j)
        if (s[i++] != s[j--]) return false;
    return true;
}
```

O(n), bộ nhớ phụ O(1). Các biến thể: bỏ qua hoa/thường (chuẩn hóa trước),
bỏ qua ký tự không phải chữ (lọc trước), xâu con đối xứng **dài nhất**
bằng cách nở quanh mỗi tâm — O(n^2), ổn với n tới vài nghìn.

## Mã hóa chạy dài

```cpp
string rle(const string& s) {
    string out;
    for (int i = 0; i < (int)s.size(); ) {
        int j = i;
        while (j < (int)s.size() && s[j] == s[i]) ++j;
        out += s[i];
        out += to_string(j - i);
        i = j;
    }
    return out;
}
```

"aaabbc" thành "a3b2c1". Vòng ngoài nhảy cả đoạn qua `i = j` — một mẫu
đáng nhớ cho mọi bài "gộp phần tử liên tiếp".

## Chữ ký hoán vị

Hai xâu là hoán vị của nhau khi và chỉ khi sắp xếp chúng bằng nhau:
`sort(a); sort(b); a == b`. O(n log n) và gọn. Phương án khác — 26 ô
tần suất — là O(n) và tổng quát lên "có bao nhiêu hoán vị của x trong s"
(cửa sổ trượt trên 26 bộ đếm). Chọn theo dạng bài, không theo thói quen.

## Đếm xâu con phân biệt — trần honestly

Xâu dài n có n(n+1)/2 xâu con. Đưa tất cả vào `set<string>` tốn
O(n^2) xâu, mỗi xâu dài trung bình O(n): O(n^3) thời gian và bộ nhớ
trường hợp xấu. n = 100 thì ổn (~5000 xâu con, ngắn). n = 1000 đã nguy
hiểm; n = 10^5 bất khả thi. Bài level beginner hỏi cái này sẽ cho n rất
nhỏ — đọc giới hạn rồi mới chọn công cụ. (Suffix automaton tới rất,
rất sau.)
""",
)

A1 = challenge(
    "hsg-p10-pal-strip",
    "Palindrome Check",
    T(
        "**Description:** Given a string s (letters and digits), determine whether it reads the",
        "same forwards and backwards. Case matters: 'a' and 'A' are different characters.",
        "",
        "**Input:** One line: s (1 <= |s| <= 10^6).",
        "**Output:** `YES` if s is a palindrome, otherwise `NO`.",
        "",
        "**Example:** `racecar` -> `YES`; `abab` -> `NO`.",
    ),
    [
        contest_test("sample yes", T("racecar"), T("YES"),
                     "Reads the same both ways."),
        contest_test("sample no", T("abab"), T("NO"),
                     "a != b at the first comparison."),
        contest_test("single char", T("x"), T("YES"),
                     "One character is always a palindrome."),
        contest_test("case sensitive", T("AbBa"), T("NO"),
                     "Reversed it is aBbA: 'A' vs 'a' at both ends — case matters."),
    ],
    level="imitation",
    difficulty="beginner",
)

A2 = challenge(
    "hsg-p10-rle",
    "Run-Length Encode",
    T(
        "**Description:** Compress a string by replacing each maximal run of equal characters with",
        "the character followed by the run length.",
        "",
        "**Input:** One line: s (1 <= |s| <= 10^6, lowercase letters).",
        "**Output:** The RLE string.",
        "",
        "**Example:** `aaabbc` -> `a3b2c1`.",
    ),
    [
        contest_test("sample", T("aaabbc"), T("a3b2c1"),
                     "Runs: a x3, b x2, c x1."),
        contest_test("single run", T("zzzz"), T("z4"),
                     "One run covers everything."),
        contest_test("no repeats", T("abc"), T("a1b1c1"),
                     "Every run has length 1."),
        contest_test("long run", T("b" * 40), T("b40"),
                     "Counts can exceed 9 — to_string handles it."),
    ],
    level="guided",
    difficulty="beginner",
)

A3 = challenge(
    "hsg-p10-anagram",
    "Anagram Verdict",
    T(
        "**Description:** Two lines. Print `YES` if the second is an anagram of the first",
        "(same characters with the same multiplicities), otherwise `NO`.",
        "",
        "**Input:** Two lines: s and t (1 <= |s|, |t| <= 10^6, lowercase letters).",
        "**Output:** `YES` or `NO`.",
        "",
        "**Example:** `listen` / `silent` -> `YES`; `listen` / `tense` -> `NO`.",
    ),
    [
        contest_test("sample yes", T("listen", "silent"), T("YES"),
                     "Same letters, same counts."),
        contest_test("sample no", T("listen", "tense"), T("NO"),
                     "Different letters entirely."),
        contest_test("length mismatch", T("ab", "abb"), T("NO"),
                     "Same letters available, but counts differ."),
        contest_test("identical", T("abc", "abc"), T("YES"),
                     "A string is an anagram of itself."),
    ],
    level="guided",
    difficulty="beginner",
)

A4 = challenge(
    "hsg-p10-cases",
    "Case Statistics",
    T(
        "**Description:** Given a line of text, count uppercase letters, lowercase letters,",
        "and digits. Print them on one line in that order, space-separated.",
        "",
        "**Input:** One line (1 <= length <= 10^6, letters, digits, and spaces).",
        "**Output:** Three integers separated by single spaces.",
        "",
        "**Example:** `Hoc Sinh Gioi 2026` -> `3 10 4`.",
    ),
    [
        contest_test("sample", T("Hoc Sinh Gioi 2026"), T("3 8 4"),
                     "H S G upper; o,c,i,n,h,i,o,i lower (8); four digits."),
        contest_test("empty of letters", T("123 456"), T("0 0 6"),
                     "Only digits and a space."),
        contest_test("all upper", T("ABC"), T("3 0 0"),
                     "Three uppercase, nothing else."),
        contest_test("spaces only", T("   "), T("0 0 0"),
                     "Spaces are neither letters nor digits — reading the line matters here."),
    ],
    level="guided",
    difficulty="beginner",
)

A5 = challenge(
    "hsg-p10-distinct",
    "Distinct Substrings",
    T(
        "**Description:** Count the distinct non-empty substrings of s. Constraints are small",
        "on purpose: 1 <= |s| <= 120.",
        "",
        "**Input:** One line: s (1 <= |s| <= 120, lowercase letters).",
        "**Output:** One integer — the number of distinct non-empty substrings.",
        "",
        "**Example:** `aba` -> `5` (a, b, ab, ba, aba).",
    ),
    [
        contest_test("sample", T("aba"), T("5"),
                     "a, b, ab, ba, aba — the full string counts too."),
        contest_test("single", T("a"), T("1"),
                     "Just the one substring."),
        contest_test("all same", T("aaa"), T("3"),
                     "a, aa, aaa."),
        contest_test("ab", T("ab"), T("3"),
                     "a, b, ab."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p10-pal-strip": vi_challenge(
        "Kiểm tra xâu đối xứng",
        T(
            "**Đề bài:** Cho xâu s (chữ và số), xác định xem nó có đọc xuôi bằng đọc ngược không.",
            "Hoa/thường có ý nghĩa: 'a' và 'A' là hai ký tự khác nhau.",
            "",
            "**Dữ liệu vào:** Một dòng: s (1 <= |s| <= 10^6).",
            "**Dữ liệu ra:** `YES` nếu s đối xứng, ngược lại `NO`.",
            "",
            "**Ví dụ:** `racecar` -> `YES`; `abab` -> `NO`.",
        ),
        [
            ("sample yes", "Đọc hai chiều giống hệt."),
            ("sample no", "a != b ngay lần so sánh đầu."),
            ("single char", "Một ký tự luôn đối xứng."),
            ("case sensitive", "'A' != 'a' — hoa/thường có ý nghĩa, nên AbA thất bại."),
        ],
    ),
    "hsg-p10-rle": vi_challenge(
        "Mã hóa chạy dài",
        T(
            "**Đề bài:** Nén xâu bằng cách thay mỗi đoạn dài nhất gồm các ký tự giống nhau bằng",
            "ký tự đó kèm độ dài đoạn.",
            "",
            "**Dữ liệu vào:** Một dòng: s (1 <= |s| <= 10^6, chữ thường).",
            "**Dữ liệu ra:** Xâu sau khi nén RLE.",
            "",
            "**Ví dụ:** `aaabbc` -> `a3b2c1`.",
        ),
        [
            ("sample", "Các đoạn: a x3, b x2, c x1."),
            ("single run", "Một đoạn phủ toàn bộ."),
            ("no repeats", "Mọi đoạn đều dài 1."),
            ("long run", "Số đếm có thể vượt 9 — to_string xử lý được."),
        ],
    ),
    "hsg-p10-anagram": vi_challenge(
        "Phán quyết hoán vị",
        T(
            "**Đề bài:** Hai dòng. In `YES` nếu dòng thứ hai là hoán vị của dòng thứ nhất",
            "(cùng ký tự, cùng số lượng), ngược lại `NO`.",
            "",
            "**Dữ liệu vào:** Hai dòng: s và t (1 <= |s|, |t| <= 10^6, chữ thường).",
            "**Dữ liệu ra:** `YES` hoặc `NO`.",
            "",
            "**Ví dụ:** `listen` / `silent` -> `YES`; `listen` / `tense` -> `NO`.",
        ),
        [
            ("sample yes", "Cùng ký tự, cùng số lượng."),
            ("sample no", "Khác hẳn bộ ký tự."),
            ("length mismatch", "Đủ loại ký tự nhưng số lượng khác nhau."),
            ("identical", "Một xâu là hoán vị của chính nó."),
        ],
    ),
    "hsg-p10-cases": vi_challenge(
        "Thống kê hoa thường",
        T(
            "**Đề bài:** Cho một dòng văn bản, đếm chữ hoa, chữ thường, và chữ số.",
            "In ba số trên một dòng, cách nhau bởi dấu cách, theo thứ tự đó.",
            "",
            "**Dữ liệu vào:** Một dòng (1 <= độ dài <= 10^6, chữ, số, và dấu cách).",
            "**Dữ liệu ra:** Ba số nguyên cách nhau một dấu cách.",
            "",
            "**Ví dụ:** `Hoc Sinh Gioi 2026` -> `3 10 4`.",
        ),
        [
            ("sample", "H S G hoa; các chữ còn lại thường; bốn chữ số."),
            ("empty of letters", "Chỉ có số và dấu cách."),
            ("all upper", "Ba chữ hoa, không gì khác."),
            ("spaces only", "Dấu cách không phải chữ cũng không phải số — đọc cả dòng mới bắt được chỗ này."),
        ],
    ),
    "hsg-p10-distinct": vi_challenge(
        "Xâu con phân biệt",
        T(
            "**Đề bài:** Đếm số xâu con khác rỗng phân biệt của s. Giới hạn cố tình nhỏ: 1 <= |s| <= 120.",
            "",
            "**Dữ liệu vào:** Một dòng: s (1 <= |s| <= 120, chữ thường).",
            "**Dữ liệu ra:** Một số nguyên — số xâu con khác rỗng phân biệt.",
            "",
            "**Ví dụ:** `aba` -> `5` (a, b, ab, ba, aba).",
        ),
        [
            ("sample", "a, b, ab, ba, aba — cả xâu đầy đủ cũng được tính."),
            ("single", "Chỉ đúng một xâu con."),
            ("all same", "a, aa, aaa."),
            ("ab", "a, b, ab."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p10-strings",
    "String Problem Set",
    "Palindromes, RLE, anagrams, char statistics, and honest brute-force substring counting.",
    "Bài tập chuỗi",
    "Đối xứng, RLE, hoán vị, thống kê ký tự, và đếm xâu con kiểu vét cạn trung thực.",
    "hsg-m10-transform",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p10-pal-strip",
            CPP_STD + cpp("""    string s; in >> s;
    int i = 0, j = (int)s.size() - 1;
    bool ok = true;
    while (i < j) {
        if (s[i] != s[j]) { ok = false; break; }
        ++i; --j;
    }
    out << (ok ? "YES" : "NO") << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    int i = 0, j = (int)s.size() - 1;
    bool ok = true;
    while (i < j) {
        if (s[i] != s[j]) { ok = false; break; }
        // near-miss: advances i but forgets to move j back
        ++i;
    }
    out << (ok ? "YES" : "NO") << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p10-rle",
            CPP_STD + cpp("""    string s; in >> s;
    string out_s;
    for (int i = 0; i < (int)s.size(); ) {
        int j = i;
        while (j < (int)s.size() && s[j] == s[i]) ++j;
        out_s += s[i];
        out_s += to_string(j - i);
        i = j;
    }
    out << out_s << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    string out_s;
    for (int i = 0; i < (int)s.size(); ) {
        int j = i;
        while (j < (int)s.size() && s[j] == s[i]) ++j;
        out_s += s[i];
        out_s += to_string(j - i);
        // near-miss: i = j is replaced by ++i, rescanning run
        // interiors and emitting duplicate partial runs
        ++i;
    }
    out << out_s << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p10-anagram",
            CPP_STD + cpp("""    string s, t; in >> s >> t;
    sort(s.begin(), s.end());
    sort(t.begin(), t.end());
    out << (s == t ? "YES" : "NO") << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s, t; in >> s >> t;
    // near-miss: checks that every char of t exists in s, ignoring
    // multiplicities — "aabb" passes against "ab"
    bool ok = true;
    for (char c : t)
        if (s.find(c) == string::npos) { ok = false; break; }
    out << (ok ? "YES" : "NO") << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p10-cases",
            CPP_STD + cpp("""    string line;
    getline(in, line);
    long long up = 0, lo = 0, di = 0;
    for (char c : line) {
        if (isupper((unsigned char)c)) ++up;
        else if (islower((unsigned char)c)) ++lo;
        else if (isdigit((unsigned char)c)) ++di;
    }
    out << up << " " << lo << " " << di << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string line;
    getline(in, line);
    long long up = 0, lo = 0, di = 0;
    for (char c : line) {
        if (isupper((unsigned char)c)) ++up;
        else if (islower((unsigned char)c)) ++lo;
        // near-miss: no digit branch — digits fall through uncounted
        else if (false) ++di;
    }
    out << up << " " << lo << " " << di << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p10-distinct",
            CPP_STD + cpp("""    string s; in >> s;
    set<string> seen;
    int n = (int)s.size();
    for (int i = 0; i < n; ++i)
        for (int len = 1; i + len <= n; ++len)
            seen.insert(s.substr(i, len));
    out << seen.size() << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string s; in >> s;
    set<string> seen;
    int n = (int)s.size();
    for (int i = 0; i < n; ++i)
        // near-miss: len starts at 2 — all length-1 substrings missed
        for (int len = 2; i + len <= n; ++len)
            seen.insert(s.substr(i, len));
    out << seen.size() << "{{NL}}";
""") + END,
        ),
    ],
)

CH10 = challenge(
    "hsg-cp-m10-pal-count",
    "Palindromic Substrings",
    T(
        "**Description:** Count the substrings of s that are palindromes. Occurrences at",
        "different positions count separately: `aaa` has 6 (three `a`, two `aa`, one `aaa`).",
        "",
        "**Input:** One line: s (1 <= |s| <= 1000, lowercase letters).",
        "**Output:** One integer — the number of palindromic substrings.",
        "",
        "**Example:** `abba` -> `6` (a, b, b, a, bb, abba).",
    ),
    [
        contest_test("even palindrome", T("abba"), T("6"),
                     "Singles a,b,b,a plus bb plus abba — an even-length center must be checked."),
        contest_test("all same", T("aaa"), T("6"),
                     "n*(n+1)/2 when every substring is a palindrome."),
        contest_test("none even", T("abc"), T("3"),
                     "Only the three single characters."),
        contest_test("middle mirror", T("aba"), T("4"),
                     "a, b, a, and the full aba."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP10 = vi_challenge(
    "Xâu con đối xứng",
    T(
        "**Đề bài:** Đếm số xâu con của s là xâu đối xứng. Các lần xuất hiện ở vị trí khác nhau",
        "được tính riêng: `aaa` có 6 (ba `a`, hai `aa`, một `aaa`).",
        "",
        "**Dữ liệu vào:** Một dòng: s (1 <= |s| <= 1000, chữ thường).",
        "**Dữ liệu ra:** Một số nguyên — số xâu con đối xứng.",
        "",
        "**Ví dụ:** `abba` -> `6` (a, b, b, a, bb, abba).",
    ),
    [
        ("even palindrome", "Các ký tự đơn a,b,b,a cộng bb cộng abba — tâm chẵn phải được kiểm tra."),
        ("all same", "n*(n+1)/2 khi mọi xâu con đều đối xứng."),
        ("none even", "Chỉ ba ký tự đơn."),
        ("middle mirror", "a, b, a, và toàn bộ aba."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m10",
    "Checkpoint — Strings",
    "Pass the graded problem to finish the strings module.",
    15,
    """**Checkpoint — chuỗi.** Pass the graded challenge below. The classic
implementation is expansion around every center: 2n-1 centers (each
character, and each gap between characters), each expanding while the
mirrored characters match — O(n^2) total, fine for n = 1000. The
near-miss everyone writes at least once is checking only the character
centers and forgetting the gaps — every even-length palindrome
(`bb`, `abba`) then goes uncounted.

**Điểm kiểm tra — chuỗi.** Pass bài chấm bên dưới. Cài đặt kinh điển là
nở quanh mọi tâm: 2n-1 tâm (mỗi ký tự, và mỗi khe giữa hai ký tự), mỗi
tâm nở trong khi các ký tự đối xứng vẫn bằng nhau — tổng O(n^2), ổn với
n = 1000. Near-miss mà ai cũng viết ít nhất một lần là chỉ kiểm tra tâm
ký tự mà quên các khe — mọi xâu đối xứng chẵn (`bb`, `abba`) sẽ bị bỏ
sót.
""",
    "Checkpoint — Strings",
    "Pass the graded problem to finish the strings module.",
    """**Điểm kiểm tra — chuỗi.** Pass bài chấm bên dưới. Cài đặt kinh điển là
nở quanh mọi tâm: 2n-1 tâm (mỗi ký tự, và mỗi khe giữa hai ký tự), mỗi
tâm nở trong khi các ký tự đối xứng vẫn bằng nhau — tổng O(n^2), ổn với
n = 1000. Near-miss mà ai cũng viết ít nhất một lần là chỉ kiểm tra tâm
ký tự mà quên các khe — mọi xâu đối xứng chẵn (`bb`, `abba`) sẽ bị bỏ
sót.
""",
    CH10,
    VI_CP10,
    solution=CPP_STD + cpp("""    string s; in >> s;
    int n = (int)s.size();
    long long cnt = 0;
    auto expand = [&](int l, int r) {
        while (l >= 0 && r < n && s[l] == s[r]) { ++cnt; --l; ++r; }
    };
    for (int c = 0; c < n; ++c) {
        expand(c, c);      // odd-length centers
        expand(c, c + 1);  // even-length centers (the gaps)
    }
    out << cnt << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    string s; in >> s;
    int n = (int)s.size();
    long long cnt = 0;
    auto expand = [&](int l, int r) {
        while (l >= 0 && r < n && s[l] == s[r]) { ++cnt; --l; ++r; }
    };
    for (int c = 0; c < n; ++c) {
        // near-miss: only odd-length centers — every even-length
        // palindrome (bb, abba, ...) goes uncounted
        expand(c, c);
    }
    out << cnt << "{{NL}}";
""") + END,
)

print("M10 done")
