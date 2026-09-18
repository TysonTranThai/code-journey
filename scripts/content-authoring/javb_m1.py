#!/usr/bin/env python3
"""Java — Beginner — Module 1: java-first-programs.

Authoring discipline: every Java code string (tests, solutions, boilerplate)
is a raw triple-quoted string, so real newlines stay real and Java "\n"
literals stay literal. Snippets are self-contained (each test = own JVM).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-first-programs"

# ── lesson 1.1 — what Java is / JVM model ───────────────────────────────────
L_JVM_EN = r"""
Java is two things at once: a **language** and a **platform**. You write
source code in `.java` files; the **compiler** (`javac`) turns each file into
**bytecode** in a `.class` file; and the **Java Virtual Machine (JVM)** runs
that bytecode on any operating system. That is the famous
"write once, run anywhere" — and it is also why Java feels a bit more formal
than Python: the compiler reads your code *before* anything runs.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, Code Journey!");
    }
}
```

Every word in that program has a job:

- `public class Hello` — Java code always lives inside a **class** (a named
  container for code and data). The file must be named `Hello.java`: the
  *public* class name and the file name must match exactly, including case.
- `main` — the entry point. When you run `java Hello`, the JVM looks for
  exactly this line: `public static void main(String[] args)`. For now, read
  `public static void` as fixed plumbing; each word gets explained in later
  modules.
- `System.out.println(...)` — prints a line of text to the console. The dot
  chain reads "from the System, go to out (the console), call println".
- Every statement ends with a **semicolon** `;`, and blocks of code live
  inside braces `{ }`.

Two errors you will meet immediately, and both are *good* news:

- **Compile-time errors** — `javac` refuses to produce bytecode and tells you
  the file, line, and reason (missing semicolon, misspelled name, wrong
  types). Nothing runs until the compiler is satisfied.
- **Runtime errors** — the code compiled, but something went wrong while
  running (dividing by zero, using a variable that is `null`). The JVM prints
  a **stack trace** describing exactly where it died.

The compiler is your first, fastest code reviewer. Beginners who read its
messages carefully improve dramatically faster than those who just retype
code until it works.

**Vocabulary you will see everywhere**

| Term | Meaning |
|---|---|
| JDK | Java Development Kit — compiler + tools + JVM (what you install) |
| JVM | the machine that runs bytecode |
| bytecode | the portable `.class` instructions `javac` produces |
| JRE | JVM + core libraries (runtime only, no compiler) |

You will practice in this course's editor, which compiles and runs Java the
same way `javac` + `java` do on your own machine.

**Next:** making the program yours — variables and types.
"""

L_JVM_VI = r"""
Java là hai thứ cùng lúc: một **ngôn ngữ** và một **nền tảng**. Bạn viết mã
nguồn trong file `.java`; trình **biên dịch** (`javac`) biến mỗi file thành
**bytecode** trong file `.class`; và **máy ảo Java (JVM)** chạy bytecode đó
trên bất kỳ hệ điều hành nào. Đó là câu "viết một lần, chạy mọi nơi" nổi
tiếng — và cũng là lý do Java trang trọng hơn Python: compiler đọc code của
bạn *trước khi* bất cứ gì chạy.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, Code Journey!");
    }
}
```

Mỗi từ trong chương trình đều có nhiệm vụ:

- `public class Hello` — code Java luôn nằm trong một **class** (thùng chứa
  code và dữ liệu có tên). File phải tên là `Hello.java`: tên class *public*
  và tên file phải khớp tuyệt đối, kể cả chữ hoa/thường.
- `main` — điểm bắt đầu. Khi chạy `java Hello`, JVM tìm đúng dòng này:
  `public static void main(String[] args)`. Tạm thời hãy đọc
  `public static void` như phần cố định; từng từ sẽ được giải thích ở module sau.
- `System.out.println(...)` — in một dòng chữ ra console. Chuỗi dấu chấm đọc
  là "từ System, tới out (màn hình), gọi println".
- Mỗi câu lệnh kết thúc bằng **dấu chấm phẩy** `;`, và khối code nằm trong
  cặp ngoặc nhọn `{ }`.

Hai loại lỗi bạn gặp ngay, và cả hai đều là *tin tốt*:

- **Lỗi lúc biên dịch** — `javac` từ chối tạo bytecode và nói cho bạn file,
  dòng, và lý do (thiếu chấm phẩy, sai chính tả, sai kiểu). Không gì chạy
  cho tới khi compiler hài lòng.
- **Lỗi lúc chạy** — code đã biên dịch được, nhưng có gì đó sai khi chạy
  (chia cho 0, dùng biến đang `null`). JVM in ra **stack trace** chỉ chính
  xác nơi nó chết.

Compiler là người review code đầu tiên và nhanh nhất của bạn. Người mới đọc
kỹ thông báo của compiler tiến bộ nhanh hơn hẳn những ai chỉ gõ lại code
đến khi nó chạy.

**Thuật ngữ bạn sẽ gặp khắp nơi**

| Thuật ngữ | Nghĩa |
|---|---|
| JDK | Java Development Kit — compiler + công cụ + JVM (cái bạn cài) |
| JVM | máy chạy bytecode |
| bytecode | các lệnh `.class` khả chuyển mà `javac` tạo ra |
| JRE | JVM + thư viện lõi (chỉ để chạy, không có compiler) |

Bạn sẽ thực hành trong trình soạn thảo của khóa học, nơi biên dịch và chạy
Java y như `javac` + `java` trên máy bạn.

**Tiếp theo:** làm cho chương trình thành của bạn — biến và kiểu dữ liệu.
"""

L_PRINT_EN = r'''
`System.out.println` prints and moves to a new line; `System.out.print`
prints without one. You can print values of any type, and join text with
values using the `+` operator:

```java
String name = "Ada";
int age = 36;
System.out.println("Name: " + name);
System.out.println("Age next year: " + (age + 1));
System.out.print("no newline here");
System.out.println(" ...this continues the same line");
```

Output:

```text
Name: Ada
Age next year: 37
no newline here ...this continues the same line
```

Two details worth noticing:

- `"Age next year: " + (age + 1)` — the parentheses matter. Without them,
  `+` is read left-to-right and `1` would be glued onto the text as the
  *character* 1 (`...: 361`).
- Java has a modern formatting option, `String.formatted(...)` (Java 15+),
  and the older `System.out.printf`:

```java
System.out.printf("Total: $%.2f%n", 19.991);   // Total: $19.99
System.out.println("Hi %s, you are %d".formatted("Ada", 36));
```

`%.2f` means "a decimal number with 2 places", `%s` a string, `%d` a whole
number, `%n` a newline. Format strings are the tool of choice when output
needs to line up in columns.

For a multi-line piece of text, a **text block** (Java 15+) keeps the shape
of the text in your source:

```java
String menu = """
    1) Coffee
    2) Tea
    3) Exit
    """;
System.out.println(menu);
```

**Next:** a tour of Java's data types.
'''
L_PRINT_VI = r'''
`System.out.println` in xong rồi xuống dòng; `System.out.print` in không
xuống dòng. Bạn có thể in giá trị của mọi kiểu dữ liệu, và nối chữ với giá
trị bằng toán tử `+`:

```java
String name = "Ada";
int age = 36;
System.out.println("Name: " + name);
System.out.println("Age next year: " + (age + 1));
System.out.print("không xuống dòng ở đây");
System.out.println(" ...câu này nằm trên cùng một dòng");
```

Kết quả:

```text
Name: Ada
Age next year: 37
không xuống dòng ở đây ...câu này nằm trên cùng một dòng
```

Hai chi tiết đáng chú ý:

- `"Age next year: " + (age + 1)` — dấu ngoặc rất quan trọng. Không có nó,
  `+` được đọc từ trái sang phải và `1` bị nối vào chữ như *ký tự* 1
  (`...: 361`).
- Java có các cách định dạng hiện đại: `String.formatted(...)` (Java 15+)
  và `System.out.printf` cổ điển hơn:

```java
System.out.printf("Total: $%.2f%n", 19.991);   // Total: $19.99
System.out.println("Hi %s, you are %d".formatted("Ada", 36));
```

`%.2f` nghĩa là "số thập phân có 2 chữ số lẻ", `%s` là chuỗi, `%d` là số
nguyên, `%n` là xuống dòng. Format string là công cụ được ưa dùng khi cần
output thẳng hàng theo cột.

Với khối văn bản nhiều dòng, **text block** (Java 15+) giữ nguyên hình dạng
của chữ ngay trong mã nguồn:

```java
String menu = """
    1) Coffee
    2) Tea
    3) Exit
    """;
System.out.println(menu);
```

**Tiếp theo:** tham quan các kiểu dữ liệu của Java.
'''
L_COMMENTS_EN = r"""
Comments are notes for humans; the compiler ignores them completely.

```java
// A single-line comment: everything after // is ignored.

/*
 * A block comment: everything between the markers is ignored,
 * even across many lines.
 */

/**
 * A documentation comment (javadoc): this one is *tool-visible* — the
 * javadoc tool turns these into HTML docs. Convention: start with a verb,
 * describe the contract.
 */
public class Notes {
    public static void main(String[] args) {
        System.out.println("Comments teach; they never run."); // trailing too
    }
}
```

Three habits that separate readable Java from noise:

1. **Explain *why*, not *what*** — `// loop until the buffer drains` teaches;
   `// i plus one` insults.
2. **Prefer renaming over commenting.** If a variable needs a comment to be
   understood, rename it: `d` → `delayMillis`.
3. **Delete dead code instead of commenting it out.** Version control
   remembers it; commented-out code rots and confuses every reader after you.

Java's official style is to use `//` freely for local notes, block comments
for file headers or long explanations, and javadoc (`/** ... */`) for every
public class and method — you will write javadoc when we build libraries in
Module 5.

**Next:** errors — the compiler's and the JVM's — and how to read both.
"""

L_COMMENTS_VI = r"""
Comment là ghi chú cho người; compiler bỏ qua hoàn toàn.

```java
// Comment một dòng: mọi thứ sau // bị bỏ qua.

/*
 * Comment khối: mọi thứ giữa hai dấu bị bỏ qua,
 * kể cả trên nhiều dòng.
 */

/**
 * Comment tài liệu (javadoc): loại này *công cụ đọc được* — công cụ javadoc
 * biến chúng thành tài liệu HTML. Quy ước: bắt đầu bằng động từ, mô tả hợp đồng.
 */
public class Notes {
    public static void main(String[] args) {
        System.out.println("Comment dạy học; chúng không chạy."); // cuối dòng cũng được
    }
}
```

Ba thói quen phân biệt Java dễ đọc với Java ồn ào:

1. **Giải thích *tại sao*, không phải *cái gì*** — `// lặp tới khi buffer cạn`
   dạy được điều; `// i cộng một` là xúc phạm.
2. **Đổi tên thay vì viết comment.** Nếu một biến cần comment mới hiểu được,
   hãy đổi tên: `d` → `delayMillis`.
3. **Xóa code chết thay vì comment nó lại.** Git nhớ nó giúp bạn; code bị
   comment sẽ mục rữa và đánh lừa mọi người đọc sau bạn.

Phong cách chính thức của Java: dùng `//` thoải mái cho ghi chú cục bộ,
comment khối cho header file hoặc giải thích dài, và javadoc (`/** ... */`)
cho mọi class và phương thức public — bạn sẽ viết javadoc khi xây thư viện
ở Module 5.

**Tiếp theo:** lỗi — của compiler và của JVM — và cách đọc cả hai.
"""

L_ERRORS_EN = r"""
Java errors come in two families, and telling them apart is a superpower.

**Family 1: compile-time errors** (javac refuses). The compiler names the
file, the line, and usually the fix:

```java
public class Broken {
    public static void main(String[] args) {
        System.out.println("oops")        // ← missing semicolon
    }
}
```

```text
Broken.java:3: error: ';' expected
        System.out.println("oops")
                                  ^
1 error
```

Read it bottom-up: `';' expected` at line 3, with a caret `^` pointing at
the exact spot. Common members of this family: missing semicolon or brace,
misspelled identifiers (`System.out.println` vs `system.out.println` — Java
is case-sensitive), type mismatches (`int x = "5";`), using a variable
before declaring it.

**Family 2: runtime errors** (the JVM stops and prints a stack trace).

```java
int[] a = new int[3];
System.out.println(a[5]);
```

```text
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException:
Index 5 out of bounds for length 3
    at Broken.main(Broken.java:4)
```

A stack trace reads **top-down as cause, bottom-up as location**: the first
line names the exception and the message; the `at ...` lines list every
method call in flight, innermost first, with file and line. `Broken.java:4`
is where it happened. Stack traces are not scolding — they are a map. You
will learn to *read* them in Module 12 and even to *throw* your own.

**The beginner loop that works**: write a little → compile → read any error
carefully → fix → repeat. Small batches keep the error list short and the
cause fresh.

**Next:** practice.
"""

L_ERRORS_VI = r"""
Lỗi trong Java có hai dòng họ, và phân biệt được chúng là một siêu năng lực.

**Dòng họ 1: lỗi lúc biên dịch** (javac từ chối). Compiler nêu tên file,
dòng, và thường là cả cách sửa:

```java
public class Broken {
    public static void main(String[] args) {
        System.out.println("oops")        // ← thiếu chấm phẩy
    }
}
```

```text
Broken.java:3: error: ';' expected
        System.out.println("oops")
                                  ^
1 error
```

Đọc từ dưới lên: `';' expected` ở dòng 3, với dấu mũ `^` chỉ đúng vị trí.
Thành viên quen thuộc của dòng họ này: thiếu chấm phẩy hoặc ngoặc, gõ sai
tên (`System.out.println` với `system.out.println` — Java phân biệt hoa
thường), lệch kiểu (`int x = "5";`), dùng biến trước khi khai báo.

**Dòng họ 2: lỗi lúc chạy** (JVM dừng và in stack trace).

```java
int[] a = new int[3];
System.out.println(a[5]);
```

```text
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException:
Index 5 out of bounds for length 3
    at Broken.main(Broken.java:4)
```

Stack trace đọc **từ trên xuống là nguyên nhân, từ dưới lên là vị trí**:
dòng đầu nêu tên exception và thông điệp; các dòng `at ...` liệt kê mọi
phương thức đang chạy, trong cùng nhất đứng trước, kèm file và dòng.
`Broken.java:4` là nơi sự việc xảy ra. Stack trace không phải lời quở trách
— nó là tấm bản đồ. Bạn sẽ học *đọc* nó ở Module 12, và cả *ném* exception
của riêng mình.

**Vòng lặp của người mới hiệu quả**: viết một chút → biên dịch → đọc kỹ
lỗi → sửa → lặp lại. Mẻ code nhỏ giữ danh sách lỗi ngắn và nguyên nhân còn
tươi.

**Tiếp theo:** thực hành.
"""

# ── practice set 1 ──────────────────────────────────────────────────────────
BOILER_HELLO = r"""public class Solution {
    public static void main(String[] args) {
        // Your printing code goes here.
    }
}
"""

P1_INTRO = challenge(
    "javb-m1-intro-print",
    "Say hello to the course",
    'Print exactly three lines:\n\n```\nHello, Code Journey!\nMy name is Java\nI am learning fast\n```\n\n'
    "Use one `System.out.println` per line inside `main`. Every statement ends with a semicolon.",
    BOILER_HELLO,
    [
        (
            "three lines",
            r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("Hello, Code Journey!", "My name is Java", "I am learning fast"), "exact three lines");
""",
            "Capture what main prints and check each line appears in order.",
        ),
    ],
    level="imitation",
)

P1_INTRO_VI = vi_challenge(
    "Chào khóa học",
    'In đúng ba dòng:\n\n```\nHello, Code Journey!\nMy name is Java\nI am learning fast\n```\n\n'
    "Dùng một `System.out.println` cho mỗi dòng bên trong `main`. Mỗi câu lệnh kết thúc bằng chấm phẩy.",
    [("three lines", "Bắt những gì main in ra và kiểm tra từng dòng xuất hiện đúng thứ tự.")],
)

P1_FIX = challenge(
    "javb-m1-fix-compile",
    "Repair the broken greeting",
    "The program below has THREE compile-time errors: a missing semicolon, a misspelled class "
    "reference (`system` must be `System`), and an unclosed string literal. Fix them so it prints:\n\n"
    "```\nFixed it myself\n```\n\n"
    "```java\npublic class Solution {\n    public static void main(String[] args) {\n"
    "        system.out.println(\"Fixed it myself\")\n    }\n}\n```",
    r"""public class Solution {
    public static void main(String[] args) {
        system.out.println("Fixed it myself")
    }
}
""",
    [
        (
            "prints after repair",
            r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
CjTestBase.checkContains(out, "Fixed it myself");
""",
            "Run main and look for the exact phrase.",
        ),
    ],
    level="debugging",
)

P1_FIX_VI = vi_challenge(
    "Sửa lời chào bị hỏng",
    "Chương trình dưới đây có BA lỗi biên dịch: thiếu chấm phẩy, gõ sai tên class (`system` "
    "phải là `System`), và chuỗi chưa đóng. Sửa để nó in:\n\n```\nFixed it myself\n```",
    [("prints after repair", "Chạy main và tìm đúng cụm từ.")],
)

P1_FORMAT = challenge(
    "javb-m1-format-banner",
    "Format a price banner",
    "A shop banner must be printed with formatted numbers. Inside `main`, print exactly:\n\n"
    "```\n=== WEEKLY DEAL ===\nPrice: 19.99 USD\n=== END ===\n```\n\n"
    "Use `String.formatted` (or printf) so the price comes from a `double price = 19.991;` "
    "variable and is rounded to 2 decimal places.",
    r"""public class Solution {
    public static void main(String[] args) {
        double price = 19.991;
        // Print the three banner lines here, using price.
    }
}
""",
    [
        (
            "banner shape",
            r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
CjTestBase.checkLines(out, "=== WEEKLY DEAL ===", "Price: 19.99 USD", "=== END ===");
""",
            "The price line must show 19.99 (two decimals), not 19.991.",
        ),
    ],
    level="guided",
)

P1_FORMAT_VI = vi_challenge(
    "Định dạng banner giá",
    "Banner cửa hàng phải in số đã định dạng. Bên trong `main`, in đúng:\n\n"
    "```\n=== WEEKLY DEAL ===\nPrice: 19.99 USD\n=== END ===\n```\n\n"
    "Dùng `String.formatted` (hoặc printf) để giá lấy từ biến `double price = 19.991;` "
    "và được làm tròn tới 2 chữ số thập phân.",
    [("banner shape", "Dòng giá phải hiện 19.99 (hai số lẻ), không phải 19.991.")],
)

P1_PREDICT = challenge(
    "javb-m1-predict-order",
    "Predict the output, then prove it",
    "Before running anything, write on paper what this prints:\n\n"
    '```java\nSystem.out.println("A");\nSystem.out.print("B");\nSystem.out.print("C");\n'
    'System.out.println("D");\nSystem.out.println("E");\n```\n\n'
    "Then implement `main` so the program produces EXACTLY that output — no extra blank lines, "
    "no trailing spaces.",
    BOILER_HELLO,
    [
        (
            "exact output",
            r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
CjTestBase.checkEq(out, "A\nBCD\nE\n", "mixed print/println output");
""",
            "print glues text onto one line; println ends the line. Expected: A on line 1, BCD on line 2, E on line 3.",
        ),
    ],
    level="combination",
)

P1_PREDICT_VI = vi_challenge(
    "Đoán output, rồi chứng minh",
    "Trước khi chạy bất cứ gì, viết ra giấy chương trình này in gì:\n\n"
    '```java\nSystem.out.println("A");\nSystem.out.print("B");\nSystem.out.print("C");\n'
    'System.out.println("D");\nSystem.out.println("E");\n```\n\n'
    "Sau đó viết `main` để chương trình tạo ra ĐÚNG output đó — không dòng trống thừa, "
    "không khoảng trắng thừa cuối dòng.",
    [("exact output", "print nối chữ vào cùng một dòng; println kết thúc dòng. Kỳ vọng: A dòng 1, BCD dòng 2, E dòng 3.")],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M1_MD = r"""
This checkpoint proves you can take a program from nothing to running.

**The task — Personal Introduction Program.** Print a short, well-formatted
introduction of yourself:

1. A header line: `=== ABOUT ME ===`
2. At least three fact lines in the form `key: value` — for example
   `name: Thao`, `goal: build Android apps`, `favorite number: 7`. The
   `favorite number` must come from an `int` variable; the key names are up
   to you but every line must contain a colon followed by a space.
3. A footer line: `=================`

Format the number with `%d` (or simple concatenation). The grader checks the
header, the footer, that at least three lines contain `": "`, and that one
of them ends with your favorite number. Everything else is your personality.
"""

CK_M1_MD_VI = r"""
Checkpoint này chứng minh bạn đưa một chương trình từ không thành chạy được.

**Nhiệm vụ — Chương trình giới thiệu bản thân.** In phần giới thiệu ngắn,
trình bày đẹp về chính bạn:

1. Dòng tiêu đề: `=== ABOUT ME ===`
2. Ít nhất ba dòng thông tin dạng `key: value` — ví dụ
   `name: Thao`, `goal: build Android apps`, `favorite number: 7`. Số yêu
   thích phải lấy từ biến `int`; tên key tùy bạn nhưng mỗi dòng phải chứa
   dấu hai chấm kèm khoảng trắng.
3. Dòng kết thúc: `=================`

Định dạng số bằng `%d` (hoặc nối chuỗi đơn giản). Grader kiểm tra tiêu đề,
dòng kết thúc, rằng có ít nhất ba dòng chứa `": "`, và một trong số đó kết
thúc bằng số yêu thích của bạn. Còn lại là cá tính của bạn.
"""

CK_M1_CH = challenge(
    "javb-checkpoint-intro",
    "Checkpoint: Personal Introduction Program",
    CK_M1_MD,
    BOILER_HELLO,
    [
        (
            "header and footer",
            r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
CjTestBase.checkContains(out, "=== ABOUT ME ===");
CjTestBase.checkContains(out, "=================");
""",
            "The header and footer lines must appear exactly as given.",
        ),
        (
            "three fact lines",
            r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
long facts = out.lines().filter(l -> l.contains(": ")).count();
CjTestBase.checkTrue(facts >= 3, "at least 3 lines contain \": \"");
""",
            "Count lines containing \": \" — you need at least three.",
        ),
        (
            "favorite number from a variable",
            r"""
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
CjTestBase.checkTrue(
    out.lines().anyMatch(l -> l.startsWith("favorite number: ")),
    "a line 'favorite number: <n>' exists");
String line = out.lines().filter(l -> l.startsWith("favorite number: ")).findFirst().orElse("");
String n = line.substring("favorite number: ".length()).trim();
try {
    Integer.parseInt(n);
} catch (NumberFormatException e) {
    CjTestBase.fail("favorite number is not a whole number: " + n);
}
""",
            "The line must start 'favorite number: ' and end with a whole number that was stored in an int.",
        ),
    ],
    difficulty="beginner",
)

CK_M1_VI = vi_challenge(
    "Checkpoint: Chương trình giới thiệu bản thân",
    CK_M1_MD_VI,
    [
        ("header and footer", "Dòng tiêu đề và dòng kết thúc phải xuất hiện đúng như đã cho."),
        ("three fact lines", "Đếm các dòng chứa \": \" — bạn cần ít nhất ba."),
        ("favorite number from a variable", "Dòng phải bắt đầu 'favorite number: ' và kết thúc bằng số nguyên được lưu trong biến int."),
    ],
)

CK_M1_R = r"""public class Solution {
    public static void main(String[] args) {
        int favorite = 7;
        System.out.println("=== ABOUT ME ===");
        System.out.println("name: Thao");
        System.out.println("goal: build Android apps");
        System.out.printf("favorite number: %d%n", favorite);
        System.out.println("=================");
    }
}
"""

CK_M1_W = r"""public class Solution {
    public static void main(String[] args) {
        // BUG: never prints the header, and favorite number is hard-typed text
        System.out.println("name: Thao");
        System.out.println("goal: build Android apps");
        System.out.println("favorite number: seven");
        System.out.println("=================");
    }
}
"""

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Java & Your First Programs",
    "The JVM model, your first compiled program, printing, comments, and the two error families — the working loop of a Java beginner.",
    "Java & Chương trình đầu tiên",
    "Mô hình JVM, chương trình đầu tiên, in output, comment, và hai dòng họ lỗi — vòng làm việc của người mới học Java.",
    ["what-is-java", "printing-output", "comments-style", "compile-vs-runtime-errors", "java-checkpoint-first-programs"],
    ["javb-p1-first"],
)

write_lesson(
    MOD, "what-is-java",
    "What Java Is & How It Runs",
    "Source → bytecode → JVM: the compile-run cycle that shapes everything else in the language.", 15,
    L_JVM_EN,
    "Java là gì & nó chạy thế nào",
    "Mã nguồn → bytecode → JVM: chu trình biên dịch–chạy định hình mọi thứ khác trong ngôn ngữ.",
    L_JVM_VI,
)

write_lesson(
    MOD, "printing-output",
    "Printing & Formatted Output",
    "println, print, printf/formatted, and text blocks — saying exactly what you mean on the console.", 15,
    L_PRINT_EN,
    "In output & định dạng",
    "println, print, printf/formatted, và text block — nói đúng điều bạn muốn trên console.",
    L_PRINT_VI,
)

write_lesson(
    MOD, "comments-style",
    "Comments & Readable Code",
    "The three comment forms, what javadoc is for, and the habits that keep code self-explanatory.", 10,
    L_COMMENTS_EN,
    "Comment & code dễ đọc",
    "Ba dạng comment, javadoc dùng để làm gì, và những thói quen giữ code tự giải thích.",
    L_COMMENTS_VI,
)

write_lesson(
    MOD, "compile-vs-runtime-errors",
    "Compile Errors vs Runtime Errors",
    "Reading compiler messages like a professional and treating stack traces as maps, not scolding.", 15,
    L_ERRORS_EN,
    "Lỗi biên dịch vs lỗi lúc chạy",
    "Đọc thông báo compiler như dân chuyên nghiệp và coi stack trace là bản đồ, không phải lời quở trách.",
    L_ERRORS_VI,
)

write_practice(
    MOD, "javb-p1-first",
    "Practice: First Programs",
    "Print, format, predict, and repair — the four moves of module one, on real code.",
    "Thực hành: Chương trình đầu tiên",
    "In, định dạng, đoán, và sửa — bốn động tác của module một, trên code thật.",
    "printing-output", 45, "beginner",
    [P1_INTRO, P1_FIX, P1_FORMAT, P1_PREDICT],
    {P1_INTRO["id"]: P1_INTRO_VI, P1_FIX["id"]: P1_FIX_VI, P1_FORMAT["id"]: P1_FORMAT_VI, P1_PREDICT["id"]: P1_PREDICT_VI},
    solutions=[
        (
            P1_INTRO["id"],
            r"""public class Solution {
    public static void main(String[] args) {
        System.out.println("Hello, Code Journey!");
        System.out.println("My name is Java");
        System.out.println("I am learning fast");
    }
}
""",
            r"""public class Solution {
    public static void main(String[] args) {
        // BUG: prints the wrong second line
        System.out.println("Hello, Code Journey!");
        System.out.println("My name is JavaScript");
        System.out.println("I am learning fast");
    }
}
""",
        ),
        (
            P1_FIX["id"],
            r"""public class Solution {
    public static void main(String[] args) {
        System.out.println("Fixed it myself");
    }
}
""",
            r"""public class Solution {
    public static void main(String[] args) {
        // BUG: still the original misspelling
        system.out.println("Fixed it myself");
    }
}
""",
        ),
        (
            P1_FORMAT["id"],
            r"""public class Solution {
    public static void main(String[] args) {
        double price = 19.991;
        System.out.println("=== WEEKLY DEAL ===");
        System.out.printf("Price: %.2f USD%n", price);
        System.out.println("=== END ===");
    }
}
""",
            r"""public class Solution {
    public static void main(String[] args) {
        double price = 19.991;
        System.out.println("=== WEEKLY DEAL ===");
        // BUG: prints raw double, not formatted to 2 places
        System.out.println("Price: " + price + " USD");
        System.out.println("=== END ===");
    }
}
""",
        ),
        (
            P1_PREDICT["id"],
            r"""public class Solution {
    public static void main(String[] args) {
        System.out.println("A");
        System.out.print("B");
        System.out.print("C");
        System.out.println("D");
        System.out.println("E");
    }
}
""",
            r"""public class Solution {
    public static void main(String[] args) {
        // BUG: every line ends with println — output has extra newlines
        System.out.println("A");
        System.out.println("B");
        System.out.println("C");
        System.out.println("D");
        System.out.println("E");
    }
}
""",
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-first-programs",
    "Checkpoint: Your First Program",
    "From empty file to formatted, running program — the compile-run loop as a finished artifact.", 40, CK_M1_MD,
    "Checkpoint: Chương trình đầu tiên",
    "Từ file trống tới chương trình chạy, định dạng đẹp — vòng biên dịch–chạy thành sản phẩm hoàn chỉnh.",
    CK_M1_MD_VI,
    CK_M1_CH, CK_M1_VI,
    solution=CK_M1_R, wrong=CK_M1_W,
)

print("module 1 complete")
