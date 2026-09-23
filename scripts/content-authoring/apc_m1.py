#!/usr/bin/env python3
"""AP CSA M1 — Java + Programming Foundations (Unit 1 on-ramp)."""
from apc import *

M = "apc-hello"

L1 = r"""
Every Java program starts the same way: a **class**, and inside it a `main`
method — the entry point the JVM calls first.

```java
public class Solution {
    public static void main(String[] args) {
        System.out.println("Hello, AP CSA!");
    }
}
```

Read it piece by piece:

- `public class Solution` — Java code lives in classes; the file name must
  match the class name (`Solution.java`).
- `public static void main(String[] args)` — the exact signature Java looks
  for. Change any word and the program will not start.
- `System.out.println(...)` — prints a line, then moves to the next line.
  `System.out.print(...)` prints **without** moving to a new line.
- Every statement ends with a semicolon `;`.

Compile and run:

```
javac Solution.java    # compile to bytecode
java Solution          # run it
```

**Errors happen in two places.** A *compile-time error* (missing `;`, unknown
word) stops `javac` before anything runs. A *runtime error* (like dividing by
zero) appears while the program runs. Fixing compiler errors is a skill you
will practice from day one.
"""

L2 = r"""
`main` runs top to bottom. **Trace it like the exam asks you to:**

```java
public class Solution {
    public static void main(String[] args) {
        System.out.print("AB");
        System.out.println("CD");
        System.out.println("EF");
    }
}
```

Output:

```
ABCDEF
EF
```

Why two lines, not three? `print("AB")` writes `AB` and stays on the same
line; `println("CD")` finishes that line. Trace rules:

1. One statement at a time, in order.
2. `print` stays on the line; `println` ends it.
3. `println()` with no argument prints just a blank line.

You can also print computed values:

```java
System.out.println(3 + 4);        // 7
System.out.println("3 + 4");      // 3 + 4
```

Quotes make text; no quotes means Java *evaluates* the expression first.
"""

L3 = r"""
Two commandments of Java style (the AP exam follows them too):

1. **Class names** start with an uppercase letter, one word per part:
   `Gradebook`, `StudentList`.
2. **Variables and methods** start lowercase, then capitalize:
   `totalScore`, `findMax()`.

Identifiers may contain letters, digits, `_`, `$`, but may not start with a
digit, and `int`, `class`, `public` are reserved keywords.

Comments are for humans and are ignored by the compiler:

```java
// one-line comment

/* a comment
   spanning lines */
```

**Reading compiler errors.** `javac` reports the file, the line, and a
(terse) reason:

```
Solution.java:4: error: ';' expected
        System.out.println("hi")
                                ^
```

The caret points where the compiler got confused — often *after* the real
mistake. A missing `;` on line 4 is reported on line 4; a missing `}` may be
reported at the very end of the file.
"""

write_module(
    M,
    "Java Program Anatomy",
    "Classes, the main method, print and println, compiling and running, and the two kinds of errors you will meet.",
    "Giải phẫu chương trình Java",
    "Lớp, phương thức main, print và println, biên dịch – chạy chương trình, và hai loại lỗi bạn sẽ gặp.",
    lessons=["apc-m1-anatomy", "apc-m1-trace", "apc-m1-style", "apc-cp-m1"],
    practices=["apc-p1-first"],
)

write_lesson(
    M, "apc-m1-anatomy", "Your first Java program",
    "The class, the main method, println vs print, and what compiling means.",
    12, L1,
    "Chương trình Java đầu tiên",
    "Lớp, phương thức main, println với print, và việc biên dịch nghĩa là gì.",
    r"""
Mọi chương trình Java đều bắt đầu như nhau: một **lớp (class)** và bên trong
nó là phương thức `main` — điểm bắt đầu mà JVM gọi đầu tiên.

```java
public class Solution {
    public static void main(String[] args) {
        System.out.println("Hello, AP CSA!");
    }
}
```

Đọc từng phần:

- `public class Solution` — mã Java nằm trong lớp; tên tệp phải trùng tên lớp
  (`Solution.java`).
- `public static void main(String[] args)` — chữ ký chính xác mà Java tìm
  thấy. Đổi bất kỳ từ nào, chương trình sẽ không chạy.
- `System.out.println(...)` — in một dòng rồi xuống dòng mới.
  `System.out.print(...)` in **mà không** xuống dòng.
- Mọi câu lệnh kết thúc bằng dấu chấm phẩy `;`.

Biên dịch và chạy:

```
javac Solution.java    # biên dịch ra bytecode
java Solution          # chạy
```

**Lỗi xuất hiện ở hai nơi.** Lỗi *biên dịch* (thiếu `;`, từ lạ) chặn `javac`
trước khi chương trình chạy. Lỗi *runtime* (như chia cho 0) xuất hiện khi
chương trình đang chạy. Sửa lỗi trình biên dịch là kỹ năng bạn luyện từ ngày
đầu tiên.
""",
)

write_lesson(
    M, "apc-m1-trace", "Tracing execution",
    "main runs top to bottom; print vs println; printing expressions vs text.",
    10, L2,
    "Truy vết chương trình",
    "main chạy từ trên xuống; print với println; in biểu thức và in văn bản.",
    r"""
`main` chạy từ trên xuống. **Truy vết đúng như đề thi yêu cầu:**

```java
public class Solution {
    public static void main(String[] args) {
        System.out.print("AB");
        System.out.println("CD");
        System.out.println("EF");
    }
}
```

Kết quả:

```
ABCDEF
EF
```

Vì sao chỉ hai dòng chứ không phải ba? `print("AB")` ghi `AB` nhưng ở nguyên
dòng; `println("CD")` kết thúc dòng đó. Quy tắc truy vết:

1. Từng câu lệnh một, theo thứ tự.
2. `print` ở lại dòng; `println` kết thúc dòng.
3. `println()` không đối số in một dòng trống.

Bạn cũng có thể in giá trị được tính:

```java
System.out.println(3 + 4);        // 7
System.out.println("3 + 4");      // 3 + 4
```

Có ngoặc kép là văn bản; không ngoặc kép nghĩa là Java *tính* biểu thức trước
khi in.
""",
)

write_lesson(
    M, "apc-m1-style", "Names, comments, and compiler errors",
    "Naming conventions, comments, and how to read javac error messages.",
    10, L3,
    "Tên, chú thích và lỗi trình biên dịch",
    "Quy ước đặt tên, chú thích, và cách đọc thông báo lỗi của javac.",
    r"""
Hai luật phong cách Java (đề thi AP cũng theo cách này):

1. **Tên lớp** viết hoa chữ cái đầu, mỗi từ một phần: `Gradebook`,
   `StudentList`.
2. **Biến và phương thức** viết thường chữ đầu, rồi viết hoa các từ sau:
   `totalScore`, `findMax()`.

Tên (identifier) có thể chứa chữ, số, `_`, `$`, nhưng không bắt đầu bằng số;
`int`, `class`, `public` là từ khóa dành riêng.

Chú thích dành cho người đọc, trình biên dịch bỏ qua:

```java
// chú thích một dòng

/* chú thích
   nhiều dòng */
```

**Đọc lỗi trình biên dịch.** `javac` báo tệp, dòng, và lý do (ngắn gọn):

```
Solution.java:4: error: ';' expected
        System.out.println("hi")
                                ^
```

Dấu mũ chỉ chỗ trình biên dịch bối rối — thường *sau* chỗ sai thật. Thiếu
`;` ở dòng 4 bị báo ở dòng 4; thiếu `}` có thể bị báo ở cuối tệp.
""",
)

BOILER_HELLO = r"""public class Solution {
    public static void main(String[] args) {
        // your code here
    }
}
"""

BOILER_GREET = r"""public class Solution {
    public static void main(String[] args) {
        System.out.print("AP");
        // add the rest
    }
}
"""

BOILER_BROKEN = r"""public class Solution {
    public static void main(String[] args) {
        System.out.println("Ready")
        system.out.println("set");
    }
}
"""

P_HELLO = challenge(
    "apc-m1-hello",
    "Three-line greeting",
    "Print exactly three lines:\n\n```\nHello, AP!\nI am learning Java\nOne line at a time\n```\n\nUse one `System.out.println` per line inside `main`.",
    BOILER_HELLO,
    [(
        "three lines",
        r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("Hello, AP!", "I am learning Java", "One line at a time"), "exact three lines");
""",
        "Capture what main prints; check the three lines in order.",
    )],
    level="imitation",
)

P_GREET = challenge(
    "apc-m1-print-vs-println",
    "Predict the output",
    "Finish the program so it prints exactly:\n\n```\nAPCSA\nrocks\n```\n\nThe first `print` already writes `AP`. Add statements so `CSA` lands on the **same** line and `rocks` on the next.",
    BOILER_GREET,
    [(
        "exact output",
        r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("APCSA", "rocks"), "two lines");
""",
        "print stays on the line; println ends it.",
    )],
    level="guided",
)

P_EXPR = challenge(
    "apc-m1-print-expr",
    "Print the sum, not the text",
    "Print the **value** of 17 + 25 on one line (just `42`), then the text `17 + 25` on the next line. One println each — think about which one needs quotes.",
    BOILER_HELLO,
    [(
        "value then text",
        r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("42", "17 + 25"), "value first, then text");
""",
        "Without quotes Java evaluates; with quotes it prints literally.",
    )],
    level="combination",
)

P_FIX = challenge(
    "apc-m1-fix-compile",
    "Repair the broken program",
    "The program has TWO compile-time errors: a missing semicolon and a misspelled `System` (Java is case-sensitive). Fix it so it prints:\n\n```\nReady\nset\n```",
    BOILER_BROKEN,
    [(
        "prints after repair",
        r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("Ready", "set"), "exact two lines");
""",
        "Every statement needs ; and System is capitalized.",
    )],
    level="debugging",
)

CP1 = challenge(
    "apc-cp-m1-output",
    "Checkpoint: trace the program",
    "Complete `main` so it prints exactly:\n\n```\nA B\nA B\nC\n```\n\nUse any mix of `print` and `println` — the exact output is what counts.",
    BOILER_HELLO,
    [(
        "checkpoint output",
        r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("A B", "A B", "C"), "three lines, A B twice");
""",
        "Plan which statements end lines and which stay on them.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p1-first", "First programs", "Write, predict, and fix complete Java programs.",
    "Chương trình đầu tiên", "Viết, dự đoán và sửa các chương trình Java hoàn chỉnh.",
    after_lesson="apc-m1-trace", minutes=35, difficulty="beginner",
    challenges=[P_HELLO, P_GREET, P_EXPR, P_FIX],
    vi_challenges={
        "apc-m1-hello": vi_challenge("Lời chào ba dòng", 'In đúng ba dòng:\n\n```\nHello, AP!\nI am learning Java\nOne line at a time\n```\n\nDùng một `System.out.println` cho mỗi dòng bên trong `main`.',
            [("three lines", "Bắt những gì main in ra; kiểm tra ba dòng đúng thứ tự.")]),
        "apc-m1-print-vs-println": vi_challenge("Dự đoán kết quả", "Hoàn thiện chương trình để in đúng:\n\n```\nAPCSA\nrocks\n```\n\n`print` đầu tiên đã ghi `AP`. Thêm câu lệnh để `CSA` nằm **cùng** dòng và `rocks` ở dòng sau.",
            [("exact output", "print ở lại dòng; println kết thúc dòng.")]),
        "apc-m1-print-expr": vi_challenge("In giá trị, không in văn bản", "In **giá trị** của 17 + 25 ở một dòng (chỉ `42`), rồi in văn bản `17 + 25` ở dòng kế. Mỗi cái một println — hãy nghĩ xem cái nào cần ngoặc kép.",
            [("value then text", "Không ngoặc kép Java tính; có ngoặc kép in nguyên văn.")]),
        "apc-m1-fix-compile": vi_challenge("Sửa chương trình lỗi", "Chương trình có HAI lỗi biên dịch: thiếu dấu chấm phẩy và viết sai `System` (Java phân biệt hoa thường). Sửa để in:\n\n```\nReady\nset\n```",
            [("prints after repair", "Mọi câu lệnh cần ; và System viết hoa.")]),
    },
    solutions=[
        ("apc-m1-hello", BOILER_HELLO.replace("        // your code here",
            '        System.out.println("Hello, AP!");\n        System.out.println("I am learning Java");\n        System.out.println("One line at a time");'),
         BOILER_HELLO.replace("        // your code here",
            '        System.out.println("Hello, AP!");\n        System.out.println("I am learning Java");')),
        ("apc-m1-print-vs-println", BOILER_GREET.replace("        // add the rest",
            '        System.out.println("CSA");\n        System.out.println("rocks");'),
         BOILER_GREET.replace("        // add the rest",
            '        System.out.println("CSA rocks");')),
        ("apc-m1-print-expr", BOILER_HELLO.replace("        // your code here",
            '        System.out.println(17 + 25);\n        System.out.println("17 + 25");'),
         BOILER_HELLO.replace("        // your code here",
            '        System.out.println("17 + 25");\n        System.out.println(17 + 25);')),
        ("apc-m1-fix-compile", r"""public class Solution {
    public static void main(String[] args) {
        System.out.println("Ready");
        System.out.println("set");
    }
}
""",
         r"""public class Solution {
    public static void main(String[] args) {
        // BUG: still the original misspelling (compile error)
        system.out.println("Ready");
        System.out.println("set");
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m1", "Checkpoint: program anatomy",
    "Trace and produce exact output with print/println.",
    15,
    r"""
You can now read a Java program's shape: class → `main` → statements, and
predict exactly what `print`/`println` will draw. Fix the checkpoint task by
*tracing first*, then writing.
""",
    "Điểm kiểm tra: giải phẫu chương trình",
    "Truy vết và tạo kết quả chính xác với print/println.",
    r"""
Bạn đã đọc được hình dạng chương trình Java: lớp → `main` → các câu lệnh, và
dự đoán chính xác `print`/`println` sẽ in gì. Hãy *truy vết trước* rồi mới
viết cho bài kiểm tra.
""",
    CP1,
    vi_challenge("Điểm kiểm tra: giải phẫu chương trình", "Hoàn thiện `main` để in đúng:\n\n```\nA B\nA B\nC\n```\n\nDùng print/println kết hợp bất kỳ — kết quả chính xác mới là quan trọng.",
        [("checkpoint output", "Lên kế hoạch câu nào kết thúc dòng, câu nào ở lại.")]),
    solution=r"""public class Solution {
    public static void main(String[] args) {
        System.out.println("A B");
        System.out.println("A B");
        System.out.println("C");
    }
}
""",
    wrong=r"""public class Solution {
    public static void main(String[] args) {
        System.out.print("A B");
        System.out.print("A B");
        System.out.println("C");
    }
}
""",
)
