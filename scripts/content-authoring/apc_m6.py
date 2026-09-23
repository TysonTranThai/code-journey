#!/usr/bin/env python3
"""AP CSA M6 — Methods (parameters, returns, scope, decomposition)."""
from apc import *

M = "apc-methods"

L1 = r"""
A **method** is a named, reusable block of behavior. The header tells you
everything:

```java
public static double average(int a, int b)
//        ↑static  ↑return type ↑name     ↑parameters
```

- **Parameters** are the inputs — typed placeholders filled by the call.
- **Return type**: what comes out. `void` means "returns nothing".

```java
public static double average(int a, int b) {
    return (a + b) / 2.0;
}
```

`return` does two jobs: hand back the value **and exit immediately**. Code
after a taken `return` never runs — which is why early-return validation
works:

```java
public static String sign(int n) {
    if (n < 0) {
        return "neg";
    }
    return "non-neg";
}
```

A `void` method can still `return;` early — bare, with no value. Arguments
are matched **by position and type**: `average(3, 4)` fills `a = 3, b = 4`.
Too few, too many, or mismatched types = compile error.
"""

L2 = r"""
**Local variables** live inside the method that declares them — parameters
included. Nothing outside can see them; nothing inside escapes:

```java
public static int twice(int x) {
    int doubled = x * 2;    // local: dies when the method returns
    return doubled;
}
```

**Scope** is where a name is visible. A method can read its own parameters
and locals; it cannot read another method's. Two methods may each have a
local named `x` — different boxes.

**static context**: our `Solution` methods are `static`, which means they
belong to the class, not to an object. A `static` method can call other
`static` methods of the same class directly by name — that is how helpers
compose:

```java
public static int hypotenuseRounded(int a, int b) {
    double c = Math.sqrt(a * a + b * b);
    return (int) (c + 0.5);
}
```

`Math.sqrt` is itself just a static method of the `Math` class — call it as
`Math.sqrt(x)`, never `new Math()` (it has no public constructor).

**Pass-by-value**: Java copies arguments. Reassigning a parameter inside the
method changes only the copy:

```java
public static void bump(int x) {
    x++;              // the caller's variable is untouched
}
```
"""

L3 = r"""
**Decomposition** — the design skill the exam's FRQs reward:

1. Read the spec; identify the *inputs*, the *output*, and the steps.
2. If the steps are complex, name each one as a helper method.
3. Write the top-level method as a sequence of helper calls.

Small worked example — "how many years until doubling a population?":

```java
public static int yearsToDouble(double start) {
    double pop = start;
    int years = 0;
    while (pop < start * 2) {
        pop *= 1.05;      // 5% growth
        years++;
    }
    return years;
}
```

**Preconditions and postconditions** are the contract style the exam uses:

- *Precondition*: what must be true when the method is called
  (`n >= 0`).
- *Postcondition*: what the method guarantees when it returns
  (returns the sum of digits of n).

A method may *assume* its precondition; it must *deliver* its
postcondition. Reading the precondition first tells you which edge cases you
may skip and which you must handle.
"""

write_module(
    M,
    "Methods",
    "Parameters, return values, void, local scope, static helpers, pass-by-value, decomposition, and spec contracts.",
    "Phương thức",
    "Tham số, giá trị trả về, void, phạm vi cục bộ, phương thức tĩnh, truyền theo giá trị, phân rã bài toán, và hợp đồng đặc tả.",
    lessons=["apc-m6-basics", "apc-m6-scope", "apc-m6-decompose", "apc-cp-m6"],
    practices=["apc-p6-methods"],
)

write_lesson(
    M, "apc-m6-basics", "Method anatomy",
    "Headers, parameters, returns, void, early return, argument matching.",
    14, L1,
    "Giải phẫu phương thức",
    "Phần đầu, tham số, return, void, return sớm, khớp đối số.",
    r"""
**Phương thức** là khối hành vi có tên, dùng lại được. Phần đầu cho bạn mọi
thứ:

```java
public static double average(int a, int b)
//        ↑static  ↑kiểu trả về ↑tên      ↑tham số
```

- **Tham số** là đầu vào — chỗ giữ có kiểu, được lấp bởi lời gọi.
- **Kiểu trả về**: thứ được trả ra. `void` nghĩa là "không trả gì cả".

```java
public static double average(int a, int b) {
    return (a + b) / 2.0;
}
```

`return` làm hai việc: đưa giá trị ra **và thoát ngay lập tức**. Code sau một
`return` đã chạy thì không bao giờ chạy — vì sao kiểu return-sớm để kiểm tra
dữ liệu lại hiệu quả:

```java
public static String sign(int n) {
    if (n < 0) {
        return "neg";
    }
    return "non-neg";
}
```

Phương thức `void` vẫn có thể `return;` sớm — trống, không giá trị. Đối số
được khớp **theo vị trí và kiểu**: `average(3, 4)` lấp `a = 3, b = 4`. Thiếu,
thừa, hoặc sai kiểu = lỗi biên dịch.
""",
)

write_lesson(
    M, "apc-m6-scope", "Scope and static helpers",
    "Local variables, pass-by-value, static-to-static calls, Math methods.",
    12, L2,
    "Phạm vi và phương thức tĩnh",
    "Biến cục bộ, truyền theo giá trị, gọi tĩnh sang tĩnh, các phương thức Math.",
    r"""
**Biến cục bộ** sống bên trong phương thức khai báo nó — tham số cũng vậy.
Không gì bên ngoài nhìn thấy chúng; không gì bên trong thoát ra được:

```java
public static int twice(int x) {
    int doubled = x * 2;    // cục bộ: chết khi phương thức trả về
    return doubled;
}
```

**Phạm vi** là nơi một tên được nhìn thấy. Phương thức đọc được tham số và
biến cục bộ của chính nó; không đọc được của phương thức khác. Hai phương
thức có thể cùng có biến cục bộ tên `x` — hai hộp khác nhau.

**Ngữ cảnh static**: các phương thức `Solution` của ta là `static`, nghĩa là
chúng thuộc về lớp, không thuộc về đối tượng. Phương thức `static` gọi trực
tiếp các phương thức `static` khác cùng lớp bằng tên — đó là cách các helper
kết hợp:

```java
public static int hypotenuseRounded(int a, int b) {
    double c = Math.sqrt(a * a + b * b);
    return (int) (c + 0.5);
}
```

`Math.sqrt` bản thân nó chỉ là phương thức static của lớp `Math` — gọi bằng
`Math.sqrt(x)`, không bao giờ `new Math()` (nó không có constructor public).

**Truyền theo giá trị**: Java sao chép đối số. Gán lại tham số bên trong chỉ
đổi bản sao:

```java
public static void bump(int x) {
    x++;              // biến của người gọi không bị ảnh hưởng
}
```
""",
)

write_lesson(
    M, "apc-m6-decompose", "Decomposition and contracts",
    "Breaking specs into helpers, preconditions and postconditions.",
    12, L3,
    "Phân rã và hợp đồng",
    "Tách đặc tả thành helper, điều kiện tiên quyết và điều kiện sau.",
    r"""
**Phân rã** — kỹ năng thiết kế mà các bài FRQ của đề thi thưởng cho:

1. Đọc đặc tả; xác định *đầu vào*, *đầu ra*, và các bước.
2. Nếu các bước phức tạp, đặt tên từng bước thành một phương thức helper.
3. Viết phương thức chính như một chuỗi lời gọi helper.

Ví dụ nhỏ — "bao nhiêu năm để dân số gấp đôi?":

```java
public static int yearsToDouble(double start) {
    double pop = start;
    int years = 0;
    while (pop < start * 2) {
        pop *= 1.05;      // tăng trưởng 5%
        years++;
    }
    return years;
}
```

**Điều kiện tiên quyết và điều kiện sau** là phong cách hợp đồng đề thi dùng:

- *Điều kiện tiên quyết* (precondition): điều gì phải đúng khi phương thức
  được gọi (`n >= 0`).
- *Điều kiện sau* (postcondition): điều gì phương thức bảo đảm khi trả về
  (trả về tổng các chữ số của n).

Phương thức được phép *giả định* điều kiện tiên quyết; nó phải *hoàn thành*
điều kiện sau. Đọc điều kiện tiên quyết trước cho bạn biết trường hợp biên
nào được phép bỏ và trường hợp nào bắt buộc xử lý.
""",
)

BOILER_F2C = r"""public class Solution {
    public static double toCelsius(double f) {
        return 0; // replace: C = 5/9 of (F - 32)
    }
}
"""

BOILER_ISPRIME = r"""public class Solution {
    public static boolean isPrime(int n) {
        return false; // replace: n >= 2 with no divisors except 1 and n
    }
}
"""

BOILER_COUNTVOWEL = r"""public class Solution {
    public static int countVowels(String s) {
        return 0; // replace: a e i o u, any case
    }
}
"""

BOILER_GCD = r"""public class Solution {
    public static int gcd(int a, int b) {
        return 0; // replace: greatest common divisor, Euclid's algorithm
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static boolean isVowel(char c) {
        if (c == 'a') {
            return true;
        }
        if (c == 'e') {
            return true;
        }
        if (c == 'i') {
            return true;
        }
        if (c == 'o') {
            return true;
        }
        if (c == 'u') {
            return true;
        }
        return c == 'A' || c == 'E' || c == 'I';
    }
}
"""

CP_POWER = r"""public class Solution {
    public static int pow(int base, int exp) {
        return 0; // replace: base^exp, exp >= 0, loop only (no Math.pow)
    }
}
"""

P_F2C = challenge(
    "apc-m6-f2c",
    "Convert with a helper",
    "Implement `double toCelsius(double f)`: C = 5/9 × (F − 32). One expression; remember integer division if you write 5/9!",
    BOILER_F2C,
    [(
        "conversion exact",
        r"""
CjTestBase.checkNear(Solution.toCelsius(212.0), 100.0, 1e-9, "boiling");
CjTestBase.checkNear(Solution.toCelsius(32.0), 0.0, 1e-9, "freezing");
CjTestBase.checkNear(Solution.toCelsius(98.6), 37.0, 1e-6, "body temp");
""",
        "5.0 / 9 or 5 / 9.0 — never 5 / 9.",
    )],
    level="imitation",
)

P_PRIME = challenge(
    "apc-m6-isprime",
    "Primality test",
    "Implement `boolean isPrime(int n)`: true when n >= 2 and no divisor between 2 and sqrt(n) divides it. Loop with `i * i <= n` to avoid floating point.",
    BOILER_ISPRIME,
    [(
        "prime boundary",
        r"""
CjTestBase.checkTrue(!Solution.isPrime(0), "0 not prime");
CjTestBase.checkTrue(!Solution.isPrime(1), "1 not prime");
CjTestBase.checkTrue(Solution.isPrime(2), "smallest prime");
CjTestBase.checkTrue(!Solution.isPrime(9), "3*3 composite");
CjTestBase.checkTrue(Solution.isPrime(97), "large prime");
""",
        "Handle n < 2 first; then test divisors while i * i <= n.",
    )],
    level="guided",
)

P_VOWEL = challenge(
    "apc-m6-countvowels",
    "Count with String.charAt",
    "Implement `int countVowels(String s)`: how many of a/e/i/o/u appear (either case). Traverse with `s.length()` and `s.charAt(i)` inside a loop.",
    BOILER_COUNTVOWEL,
    [(
        "vowel count",
        r"""
CjTestBase.checkEq(Solution.countVowels("Hello World"), 3, "e, o, o");
CjTestBase.checkEq(Solution.countVowels("xyz"), 0, "none");
CjTestBase.checkEq(Solution.countVowels("AEIOUaeiou"), 10, "all, both cases");
CjTestBase.checkEq(Solution.countVowels(""), 0, "empty");
""",
        "Lowercase the char (or test both cases) before comparing.",
    )],
    level="guided",
)

P_GCD = challenge(
    "apc-m6-gcd",
    "Euclid's algorithm",
    "Implement `int gcd(int a, int b)`: the greatest common divisor. While `b != 0`, replace `(a, b)` with `(b, a % b)`; the answer is the final `a`. This is the classic loop-with-variables trace.",
    BOILER_GCD,
    [(
        "gcd values",
        r"""
CjTestBase.checkEq(Solution.gcd(12, 18), 6, "12,18");
CjTestBase.checkEq(Solution.gcd(7, 13), 1, "coprime");
CjTestBase.checkEq(Solution.gcd(100, 100), 100, "equal");
CjTestBase.checkEq(Solution.gcd(48, 36), 12, "48,36");
""",
        "gcd(a, 0) is a — the loop exits immediately when b starts as 0.",
    )],
    level="combination",
)

P_FIX = challenge(
    "apc-m6-fix-vowel",
    "Debug the vowel check",
    "`isVowel` is missing uppercase vowels and compiles fine — it just answers wrong for 'O' and 'U' (and claims some consonants are vowels? no — it misses two). Repair it with the smallest change so all ten vowel letters return true and consonants return false. Hint: a tidy fix converts the char to lowercase first.",
    BOILER_FIX,
    [(
        "all vowels",
        r"""
CjTestBase.checkTrue(Solution.isVowel('a') && Solution.isVowel('A'), "a pair");
CjTestBase.checkTrue(Solution.isVowel('e') && Solution.isVowel('E'), "e pair");
CjTestBase.checkTrue(Solution.isVowel('i') && Solution.isVowel('I'), "i pair");
CjTestBase.checkTrue(Solution.isVowel('o') && Solution.isVowel('O'), "o pair");
CjTestBase.checkTrue(Solution.isVowel('u') && Solution.isVowel('U'), "u pair");
CjTestBase.checkTrue(!Solution.isVowel('x') && !Solution.isVowel('Z'), "consonants");
""",
        "Character.toLowerCase(c) then compare against the five lowercase vowels.",
    )],
    level="debugging",
)

CP6 = challenge(
    "apc-cp-m6-power",
    "Checkpoint: integer power",
    "Implement `int pow(int base, int exp)`: base raised to exp using a loop (no Math.pow). exp >= 0. Note the special case: anything to the 0 is 1.",
    CP_POWER,
    [(
        "power cases",
        r"""
CjTestBase.checkEq(Solution.pow(5, 0), 1, "zero exponent");
CjTestBase.checkEq(Solution.pow(5, 1), 5, "first power");
CjTestBase.checkEq(Solution.pow(2, 10), 1024, "2^10");
CjTestBase.checkEq(Solution.pow(7, 3), 343, "7^3");
CjTestBase.checkEq(Solution.pow(-2, 3), -8, "negative base, odd power");
""",
        "Accumulator starts at 1; multiply exp times.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p6-methods", "Method toolkit", "Helpers, loops inside methods, algorithm classics.",
    "Bộ công cụ phương thức", "Helper, vòng lặp trong phương thức, các thuật toán kinh điển.",
    after_lesson="apc-m6-scope", minutes=50, difficulty="beginner",
    challenges=[P_F2C, P_PRIME, P_VOWEL, P_GCD, P_FIX],
    vi_challenges={
        "apc-m6-f2c": vi_challenge("Chuyển đổi bằng helper", "Cài đặt `double toCelsius(double f)`: C = 5/9 × (F − 32). Một biểu thức; nhớ chia số nguyên nếu bạn viết 5/9!",
            [("conversion exact", "5.0 / 9 hoặc 5 / 9.0 — không bao giờ 5 / 9.")]),
        "apc-m6-isprime": vi_challenge("Kiểm tra số nguyên tố", "Cài đặt `boolean isPrime(int n)`: đúng khi n >= 2 và không có ước nào từ 2 đến căn(n) chia hết nó. Vòng lặp với `i * i <= n` để tránh số thực.",
            [("prime boundary", "Xử lý n < 2 trước; rồi thử các ước trong khi i * i <= n.")]),
        "apc-m6-countvowels": vi_challenge("Đếm với String.charAt", "Cài đặt `int countVowels(String s)`: có bao nhiêu a/e/i/o/u (cả hai dạng chữ). Duyệt bằng `s.length()` và `s.charAt(i)` trong vòng lặp.",
            [("vowel count", "Chuyển ký tự sang chữ thường (hoặc thử cả hai dạng) trước khi so sánh.")]),
        "apc-m6-gcd": vi_challenge("Thuật toán Euclid", "Cài đặt `int gcd(int a, int b)`: ước chung lớn nhất. Trong khi `b != 0`, thay `(a, b)` bằng `(b, a % b)`; kết quả là `a` cuối. Đây là bài truy vết kinh điển với biến trong vòng lặp.",
            [("gcd values", "gcd(a, 0) là a — vòng lặp thoát ngay khi b ban đầu là 0.")]),
        "apc-m6-fix-vowel": vi_challenge("Sửa kiểm tra nguyên âm", "`isVowel` thiếu các nguyên âm IN HOA và vẫn biên dịch tốt — chỉ trả lời sai cho 'O' và 'U'. Sửa với thay đổi nhỏ nhất để cả mười ký tự nguyên âm trả về true và phụ âm trả về false. Gợi ý: sửa gọn là chuyển ký tự sang chữ thường trước.",
            [("all vowels", "Character.toLowerCase(c) rồi so với năm nguyên âm chữ thường.")]),
    },
    solutions=[
        ("apc-m6-f2c", r"""public class Solution {
    public static double toCelsius(double f) {
        return 5.0 / 9 * (f - 32);
    }
}
""",
         r"""public class Solution {
    public static double toCelsius(double f) {
        // BUG: 5 / 9 is integer division — always 0
        return 5 / 9 * (f - 32);
    }
}
"""),
        ("apc-m6-isprime", r"""public class Solution {
    public static boolean isPrime(int n) {
        if (n < 2) {
            return false;
        }
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }
}
""",
         r"""public class Solution {
    public static boolean isPrime(int n) {
        // BUG: tests all the way to n — slow but ALSO miscounts? no:
        // BUG: forgets n < 2 — claims 1 and 0 are prime
        if (n == 1) {
            return false;
        }
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }
}
""".replace("// BUG: tests all the way to n — slow but ALSO miscounts? no:\n        // BUG: forgets n < 2 — claims 1 and 0 are prime",
            "// BUG: forgets n < 2 — claims 0 and 1 are prime")),
        ("apc-m6-countvowels", r"""public class Solution {
    public static int countVowels(String s) {
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = Character.toLowerCase(s.charAt(i));
            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                count++;
            }
        }
        return count;
    }
}
""",
         r"""public class Solution {
    public static int countVowels(String s) {
        // BUG: counts uppercase U and O but skips lowercase pairs? no:
        // BUG: tests only lowercase — "AEIOU" counted as zero
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                count++;
            }
        }
        return count;
    }
}
""".replace("// BUG: counts uppercase U and O but skips lowercase pairs? no:\n        ", "")),
        ("apc-m6-gcd", r"""public class Solution {
    public static int gcd(int a, int b) {
        while (b != 0) {
            int t = b;
            b = a % b;
            a = t;
        }
        return a;
    }
}
""",
         r"""public class Solution {
    public static int gcd(int a, int b) {
        // BUG: swaps the update order — a is overwritten before the remainder
        while (b != 0) {
            a = b;
            b = a % b;
        }
        return a;
    }
}
"""),
        ("apc-m6-fix-vowel", r"""public class Solution {
    public static boolean isVowel(char c) {
        char lo = Character.toLowerCase(c);
        return lo == 'a' || lo == 'e' || lo == 'i' || lo == 'o' || lo == 'u';
    }
}
""",
         r"""public class Solution {
    public static boolean isVowel(char c) {
        // BUG: original flaw kept — no uppercase O or U handled
        if (c == 'a') {
            return true;
        }
        if (c == 'e') {
            return true;
        }
        if (c == 'i') {
            return true;
        }
        if (c == 'o') {
            return true;
        }
        if (c == 'u') {
            return true;
        }
        return c == 'A' || c == 'E' || c == 'I';
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m6", "Checkpoint: methods",
    "Integer power by loop — accumulator pattern with a special case.",
    18,
    r"""
One method, one loop, one accumulator, one special case (exponent 0). The
signature-to-implementation pipeline you will use in every FRQ.
""",
    "Điểm kiểm tra: phương thức",
    "Lũy thừa nguyên bằng vòng lặp — mẫu tích lũy với một trường hợp đặc biệt.",
    r"""
Một phương thức, một vòng lặp, một bộ tích lũy, một trường hợp đặc biệt (số
mũ 0). Quy trình chữ ký → cài đặt mà bạn sẽ dùng trong mọi bài FRQ.
""",
    CP6,
    vi_challenge("Điểm kiểm tra: phương thức", "Cài đặt `int pow(int base, int exp)`: base mũ exp bằng vòng lặp (không dùng Math.pow). exp >= 0. Chú ý trường hợp đặc biệt: mọi số mũ 0 cho kết quả 1.",
        [("power cases", "Bộ tích lũy bắt đầu 1; nhân đúng exp lần.")]),
    solution=r"""public class Solution {
    public static int pow(int base, int exp) {
        int result = 1;
        for (int i = 0; i < exp; i++) {
            result *= base;
        }
        return result;
    }
}
""",
    wrong=r"""public class Solution {
    public static int pow(int base, int exp) {
        // BUG: seed is base, not 1 — wrong for exp 0 and off by one factor
        int result = base;
        for (int i = 1; i < exp; i++) {
            result *= base;
        }
        return result;
    }
}
""",
)
