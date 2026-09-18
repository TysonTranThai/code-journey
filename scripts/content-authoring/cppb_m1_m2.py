#!/usr/bin/env python3
"""C++ Beginner — module 1 (first-programs) and module 2 (variables-and-types)."""
from cppb import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 1: first-programs ============================
M1 = "first-programs"

L1A = "what-is-cpp"
L1B = "hello-cpp"
L1C = "output-and-input"
L1D = "reading-compiler-errors"
L1E = "checkpoint-fundamentals"

write_module(
    M1,
    "Your First C++ Programs",
    "What C++ is, how compilation works, and your first programs — from hello world to reading real compiler errors like a professional.",
    "Những chương trình C++ đầu tiên",
    "C++ là gì, compilation hoạt động ra sao, và những chương trình đầu tiên của bạn — từ hello world đến việc đọc lỗi compiler như một lập trình viên chuyên nghiệp.",
    [L1A, L1B, L1C, L1D, L1E],
    ["m1-hello-practice", "m1-errors-practice"],
)

write_lesson(
    M1, L1A,
    "What Is C++ and Why Compile?",
    "C++ is a compiled, statically typed language for software where performance and control matter. Understand what the compiler does before you write your first line.",
    9,
    '''
C++ is a **compiled** language: before your program runs, a program called the **compiler** translates your human-readable source code (`.cpp` files) into machine code your CPU executes directly. That translation step is what makes C++ fast — and it is also why C++ catches certain mistakes *before* the program ever runs.

## The workflow you will repeat thousands of times

```
edit code  →  compile  →  run  →  (read output or errors)  →  repeat
```

Compare that with Python, where the interpreter reads your source directly. In C++, two different tools answer two different questions:

- The **compiler** (`g++`) turns source into an **executable** and refuses to build code it cannot understand. A *compiler error* means "this is not valid C++".
- The **runtime** is your program actually executing. A *runtime error* (a crash) means valid C++ did something dangerous, like dividing by zero or reading past the end of a collection.

## Why learn C++ in 2026?

- It runs everywhere performance matters: games, browsers, databases, operating systems, embedded devices, trading systems.
- It teaches you what the machine is really doing: memory, lifetime, and cost. That knowledge makes you better at *every* language.
- Modern C++ (C++20 is this course's baseline) is a much safer, more expressive language than the C++ of the 1990s. This course teaches the modern language — not "C with classes".

## What "statically typed" buys you

Every variable's type is known at compile time:

```cpp
int score = 100;        // the compiler knows this is a whole number
double price = 9.99;    // ...and this is a decimal
```

If you later write `score = "high";` the compiler stops you with an error — in Python the same mistake would explode at runtime, possibly in production, possibly on a Tuesday night. Types are a feature, and you will learn to lean on them.

## A note on the platform

In this course you write C++ in the browser editor and the platform compiles and runs it in an isolated sandbox using GCC. The graded programs follow one convention you will meet in the next lesson: your code is compiled as a single file, and interactive keyboard input is not part of grading — challenges check what your functions return and what your program prints.

**Coming up:** your first program, and the strange little word `main`.
''',
    "C++ là gì và vì sao phải biên dịch?",
    "C++ là ngôn ngữ biên dịch, kiểu tĩnh, dành cho các phần mềm cần hiệu năng và khả năng kiểm soát. Hãy hiểu compiler làm gì trước khi viết dòng đầu tiên.",
    '''
C++ là ngôn ngữ **biên dịch (compiled)**: trước khi chương trình chạy, một chương trình gọi là **compiler** dịch mã nguồn bạn viết (các file `.cpp`) thành mã máy để CPU thực thi trực tiếp. Chính bước dịch này làm C++ nhanh — và cũng là lý do C++ bắt được một số lỗi *trước khi* chương trình chạy.

## Vòng lặp công việc bạn sẽ lặp lại hàng nghìn lần

```
sửa code  →  biên dịch  →  chạy  →  (đọc output hoặc lỗi)  →  lặp lại
```

Hãy so với Python, nơi interpreter đọc thẳng mã nguồn. Trong C++, hai công cụ trả lời hai câu hỏi khác nhau:

- **Compiler** (`g++`) dịch mã nguồn thành **file thực thi** và từ chối build code mà nó không hiểu được. *Compiler error* nghĩa là "đây không phải C++ hợp lệ".
- **Runtime** là lúc chương trình của bạn thực sự chạy. *Runtime error* (crash) nghĩa là C++ hợp lệ đã làm điều nguy hiểm, ví dụ chia cho 0 hoặc đọc quá giới hạn của một collection.

## Vì sao học C++ năm 2026?

- Nó chạy ở mọi nơi cần hiệu năng: game, trình duyệt, database, hệ điều hành, thiết bị nhúng, hệ thống giao dịch.
- Nó dạy bạn máy móc thực sự làm gì: bộ nhớ, vòng đời, và cái giá của từng thao tác. Kiến thức đó làm bạn giỏi hơn ở *mọi* ngôn ngữ.
- C++ hiện đại (khóa này dùng chuẩn C++20) an toàn và biểu cảm hơn nhiều so với C++ thập niên 90. Khóa này dạy ngôn ngữ hiện đại — không phải "C với class".

## Kiểu tĩnh mang lại gì

Kiểu của mọi biến được biết ngay lúc biên dịch:

```cpp
int score = 100;        // compiler biết đây là số nguyên
double price = 9.99;    // ...và đây là số thập phân
```

Nếu sau này bạn viết `score = "high";`, compiler sẽ chặn lại bằng một lỗi — trong Python, lỗi tương tự chỉ nổ lúc chạy, có thể là lúc đang production. Kiểu dữ liệu là một tính năng, và bạn sẽ học cách tận dụng nó.

## Về nền tảng này

Trong khóa này, bạn viết C++ ngay trên trình soạn thảo của trình duyệt và nền tảng sẽ biên dịch, chạy code trong sandbox cô lập bằng GCC. Chương trình được chấm điểm theo một quy ước bạn sẽ gặp ở bài sau: code được biên dịch thành một file duy nhất, và phần nhập từ bàn phím không nằm trong phần chấm — các challenge kiểm tra hàm của bạn trả về gì và chương trình in ra gì.

**Sắp tới:** chương trình đầu tiên của bạn, và từ khóa nhỏ kỳ lạ `main`.
''',
)

write_lesson(
    M1, L1B,
    "Hello, C++ — Anatomy of a Program",
    "Your first program, line by line: includes, main, statements, braces, semicolons, and the stream insertion operator.",
    10,
    '''
Here is a complete C++ program:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
    return 0;
}
```

Seven lines. Let's read every one of them, because each is a habit for life.

## `#include <iostream>`

`#include` asks the compiler to paste in the declarations for a part of the **standard library** — here, `iostream`, which provides input and output. Angle brackets `<...>` mean "look in the standard library". Includes always appear at the top of the file.

## `int main()`

Every C++ program starts at a function named `main`. The `int` before it means main *returns* a whole number to the operating system: `0` conventionally means "finished successfully". The `()` after the name means it takes no parameters. Exactly one `main` exists per program.

## The body: braces and statements

The `{ }` braces mark the function's body. Inside, each **statement** ends with a semicolon — C++ uses `;` the way humans use periods. Forget one and the compiler will complain, usually on the *next* line, which is why reading errors calmly matters (next lesson).

## `std::cout << "Hello, C++!" << std::endl;`

This single line has three parts:

- `std::cout` — the **console output stream** ("character output"). The `std::` prefix says this name lives in the **standard namespace**; for now, write it as-is every time.
- `<<` — the **stream insertion operator**. You can chain it: `std::cout << a << b;` sends `a` then `b`.
- `std::endl` — a newline plus a flush. For a plain newline, `'\\n'` inside the string is enough: `"Hello!\\n"`.

So the line means: send the text, then a newline, to the console.

## Comments

```cpp
// a one-line comment
/* a comment
   spanning lines */
```

Comments are for humans; the compiler deletes them. Write *why*, not *what*.

## Coming up

Printing is half the conversation. Next: reading input — and why graded challenges on this platform avoid it.
''',
    "Hello, C++ — giải phẫu một chương trình",
    "Chương trình đầu tiên của bạn, từng dòng một: include, main, statement, ngoặc nhọn, dấu chấm phẩy, và toán tử stream insertion.",
    '''
Đây là một chương trình C++ hoàn chỉnh:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
    return 0;
}
```

Bảy dòng. Hãy đọc từng dòng, vì mỗi dòng là một thói quen cho cả sự nghiệp.

## `#include <iostream>`

`#include` yêu cầu compiler chèn khai báo của một phần trong **thư viện chuẩn** — ở đây là `iostream`, cung cấp nhập/xuất. Dấu ngoặc nhọn `<...>` nghĩa là "tìm trong thư viện chuẩn". Include luôn nằm ở đầu file.

## `int main()`

Mọi chương trình C++ bắt đầu tại một hàm tên `main`. `int` phía trước nghĩa là main *trả về* một số nguyên cho hệ điều hành: `0` theo quy ước nghĩa là "chạy thành công". Cặp `()` sau tên nghĩa là hàm không nhận tham số. Mỗi chương trình chỉ có đúng một `main`.

## Thân hàm: ngoặc nhọn và statement

Cặp `{ }` đánh dấu thân hàm. Bên trong, mỗi **statement** kết thúc bằng dấu chấm phẩy — C++ dùng `;` giống như người dùng dấu chấm câu. Quên một dấu và compiler sẽ khó chịu, thường là ở *dòng phía sau*, đó là lý do cần đọc lỗi một cách bình tĩnh (bài tiếp theo).

## `std::cout << "Hello, C++!" << std::endl;`

Một dòng duy nhất gồm ba phần:

- `std::cout` — **console output stream** ("character output"). Tiền tố `std::` cho biết tên này nằm trong **standard namespace**; hiện tại, cứ viết nguyên mẫu như vậy mỗi lần.
- `<<` — **toán tử stream insertion**. Bạn có thể nối chuỗi: `std::cout << a << b;` sẽ gửi `a` rồi `b`.
- `std::endl` — xuống dòng kèm flush. Nếu chỉ cần xuống dòng, `'\\n'` trong chuỗi là đủ: `"Hello!\\n"`.

Vậy dòng này nghĩa là: gửi đoạn text, rồi xuống dòng, ra console.

## Comment

```cpp
// comment một dòng
/* comment
   nhiều dòng */
```

Comment dành cho con người; compiler sẽ xóa chúng. Hãy viết *tại sao*, không phải *cái gì*.

## Sắp tới

In ra màn hình mới là một nửa cuộc trò chuyện. Bài sau: đọc input — và vì sao các challenge có chấm điểm trên nền tảng này tránh dùng nó.
''',
)

write_lesson(
    M1, L1C,
    "Output, Input, and the Grading Convention",
    "Chain output, read input with std::cin for local programs, and learn how the platform grades: functions and printed output, not typed input.",
    10,
    '''
## Chaining output

`<<` chains naturally, which is how you format small messages:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Linh";
    int age = 20;
    std::cout << "Name: " << name << ", age: " << age << '\\n';
    return 0;
}
```

Output:

```
Name: Linh, age: 20
```

Note that `name` and `age` are *values* — `cout` knows how to print strings, ints, doubles, and more without any format codes.

## Reading input with `std::cin`

`std::cin` is the mirror image: it reads from the keyboard into a variable:

```cpp
std::string name;
int age;
std::cin >> name >> age;   // >> reads, << writes
```

`>>` skips leading whitespace and stops at the next space or newline. Input makes programs interactive — try it locally on your machine. Reading input is also where beginners meet their first *state* bug: reading into the wrong variable type silently fails (age stays at 0). `cin >> x` followed by checking `if (std::cin.fail())` is the honest first lesson in validation, which we develop properly in later modules.

## Why graded challenges do not use `std::cin`

On this platform, graded runs execute your code automatically in a sandbox — nobody is typing at a keyboard. So the grading convention is:

1. **Write functions** with parameters and return values — tests call them directly, e.g. `add(2, 3)` must return `5`.
2. **Or write a `void program()`** that prints something — the test captures what it printed and checks the text.

Lessons and ungraded exploration can still use `cin`; the sandbox simply replaces it with a clear error during graded runs, exactly like the platform already does for Python. This keeps every challenge automatic, objective, and identical for every learner — in both English and Vietnamese.

## The boilerplate you will see

Many challenges pre-fill this shape in the editor:

```cpp
#include <iostream>

void program() {
    // your code here
}

int main() {
    program();
    return 0;
}
```

You fill in `program()`; the harness handles the rest. When a challenge grades a function instead, the boilerplate contains that function's empty shell.
''',
    "Output, Input, và Quy ước chấm điểm",
    "Nối chuỗi output, đọc input bằng std::cin cho chương trình chạy cục bộ, và tìm hiểu cách nền tảng chấm điểm: hàm và kết quả in ra, không phải dữ liệu gõ vào.",
    '''
## Nối chuỗi output

`<<` có thể nối tự nhiên, và đó là cách bạn format các thông báo ngắn:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Linh";
    int age = 20;
    std::cout << "Name: " << name << ", age: " << age << '\\n';
    return 0;
}
```

Kết quả:

```
Name: Linh, age: 20
```

Lưu ý `name` và `age` là *giá trị* — `cout` tự biết cách in string, int, double và nhiều kiểu khác mà không cần mã định dạng.

## Đọc input bằng `std::cin`

`std::cin` là hình ảnh đối xứng: nó đọc từ bàn phím vào biến:

```cpp
std::string name;
int age;
std::cin >> name >> age;   // >> để đọc, << để ghi
```

`>>` bỏ qua khoảng trắng đầu dòng và dừng ở dấu cách hoặc xuống dòng tiếp theo. Input làm chương trình tương tác — hãy thử chạy cục bộ trên máy của bạn. Đọc input cũng là nơi người mới gặp lỗi *trạng thái* đầu tiên: đọc vào sai kiểu biến thì việc đọc âm thầm thất bại (age vẫn giữ 0). `cin >> x` rồi kiểm tra `if (std::cin.fail())` là bài học đầu tiên và trung thực nhất về validation, chúng ta sẽ phát triển đúng trong các module sau.

## Vì sao challenge có chấm điểm không dùng `std::cin`

Trên nền tảng này, các lần chạy có chấm điểm thực thi code của bạn tự động trong sandbox — không ai đang gõ bàn phím cả. Vì vậy quy ước chấm là:

1. **Viết hàm** với tham số và giá trị trả về — test sẽ gọi trực tiếp, ví dụ `add(2, 3)` phải trả về `5`.
2. **Hoặc viết một `void program()`** in ra nội dung nào đó — test sẽ bắt lại những gì được in và kiểm tra text.

Bài học và phần khám phá tự do vẫn có thể dùng `cin`; sandbox sẽ thay nó bằng một thông báo rõ ràng trong lúc chấm, giống hệt cách nền tảng làm với Python. Điều này giữ mọi challenge tự động, khách quan, và giống nhau cho mọi học viên — cả tiếng Anh lẫn tiếng Việt.

## Khung code bạn sẽ gặp

Nhiều challenge điền sẵn dạng này trong trình soạn thảo:

```cpp
#include <iostream>

void program() {
    // code của bạn ở đây
}

int main() {
    program();
    return 0;
}
```

Bạn viết phần thân `program()`; phần còn lại do harness lo. Khi challenge chấm một hàm cụ thể, boilerplate sẽ chứa khung rỗng của hàm đó.
''',
)

write_lesson(
    M1, L1D,
    "Reading Compiler Errors Without Fear",
    "Compiler errors are the compiler doing its job. Learn the read-first-error habit, the classic beginner errors, and the fix loop.",
    11,
    '''
The single most valuable beginner skill in C++ is not syntax — it is **reading compiler errors calmly**. The compiler is not scolding you; it is the only tool that reads your code *before* it runs, and it quotes your mistakes with a line number.

## The habit: read the FIRST error, fix it, recompile

GCC reports many errors per build, but they cascade: error #2 is often a *consequence* of error #1. Always fix the top one first.

## The classic five (and what they actually mean)

**1. Missing semicolon** — `error: expected ';' before '}' token`

```cpp
int x = 5      // oops
```
The fix is obvious, but notice the error points at the `}` *after* the mistake. The line number is where the compiler gave up, not where you sinned.

**2. Undeclared identifier** — `error: 'cont' was not declared in this scope`

Usually a typo (`cont` for `count`) or a missing `#include`. The compiler echoes the exact spelling it could not find — compare it letter by letter with your code.

**3. Undeclared in `std`** — `error: 'cout' was not declared in this scope; did you mean 'std::cout'?`

Modern GCC even suggests the fix. `std::` is required unless you `using namespace std;` — which this course deliberately avoids in headers and larger files (it pollutes every file that includes them; in small exercises it is tolerable, but we practice the professional habit).

**4. Type mismatch** — `error: invalid conversion from 'const char*' to 'int'`

```cpp
int age = "twenty";
```
Static typing working *for* you: the compiler caught at build time what Python would crash on at runtime. Read what it says it found and what it expected.

**5. Uninitialized variable (a warning, not an error!)** — `'x' is used uninitialized`

```cpp
int x;
std::cout << x;   // garbage value
```
This *compiles*. The value printed is whatever bytes happened to sit in memory — a real bug that often "works" on your machine and crashes elsewhere. Turn warnings into your routine: in this course the sandbox already compiles with `-Wall -Wextra -Wpedantic`, and graded code that triggers them still runs, but the warnings are shown — read them.

## The fix loop

```
compile → read first error → fix that one thing → recompile
```

Small, frequent fixes beat giant rewrites. By module 3 you will skim an error and know its *class* before reading the details — that is when C++ stops feeling hostile.
''',
    "Đọc lỗi compiler không sợ hãi",
    "Lỗi compiler là compiler đang làm việc của nó. Học thói quen đọc lỗi đầu tiên, năm lỗi kinh điển của người mới, và vòng lặp sửa lỗi.",
    '''
Kỹ năng đắt giá nhất của người mới học C++ không phải cú pháp — mà là **đọc lỗi compiler một cách bình tĩnh**. Compiler không trách mắng bạn; nó là công cụ duy nhất đọc code của bạn *trước khi* chạy, và nó trích dẫn lỗi kèm số dòng.

## Thói quen: đọc lỗi ĐẦU TIÊN, sửa nó, biên dịch lại

GCC báo nhiều lỗi mỗi lần build, nhưng chúng dây chuyền: lỗi số 2 thường là *hậu quả* của lỗi số 1. Luôn sửa lỗi trên cùng trước.

## Năm lỗi kinh điển (và ý nghĩa thật của chúng)

**1. Thiếu dấu chấm phẩy** — `error: expected ';' before '}' token`

```cpp
int x = 5      // oops
```
Cách sửa hiển nhiên, nhưng lưu ý lỗi chỉ vào `}` *sau* chỗ sai. Số dòng là nơi compiler bỏ cuộc, không phải nơi bạn phạm lỗi.

**2. Undeclared identifier** — `error: 'cont' was not declared in this scope`

Thường là lỗi chính tả (`cont` thay vì `count`) hoặc thiếu `#include`. Compiler in lại đúng chính tả mà nó không tìm thấy — so từng chữ với code của bạn.

**3. Không khai báo trong `std`** — `error: 'cout' was not declared in this scope; did you mean 'std::cout'?`

GCC hiện đại thậm chí gợi ý cách sửa. `std::` là bắt buộc trừ khi bạn `using namespace std;` — điều khóa này chủ động tránh trong header và file lớn (nó làm ô nhiễm mọi file include nó; trong bài tập nhỏ thì chấp nhận được, nhưng chúng ta luyện thói quen chuyên nghiệp).

**4. Sai kiểu** — `error: invalid conversion from 'const char*' to 'int'`

```cpp
int age = "twenty";
```
Kiểu tĩnh đang làm việc *cho* bạn: compiler bắt được lúc build điều mà Python phải crash lúc chạy. Đọc xem nó tìm thấy gì và nó kỳ vọng gì.

**5. Biến chưa khởi tạo (chỉ là cảnh báo, không phải lỗi!)** — `'x' is used uninitialized`

```cpp
int x;
std::cout << x;   // giá trị rác
```
Đoạn này *biên dịch được*. Giá trị in ra là những byte ngẫu nhiên đang nằm trong bộ nhớ — một bug thật, thường "chạy được" trên máy bạn rồi hỏng chỗ khác. Hãy biến cảnh báo thành thói quen: trong khóa này sandbox đã biên dịch với `-Wall -Wextra -Wpedantic`, code có chấm vẫn chạy dù có warning, nhưng warning sẽ được hiển thị — hãy đọc chúng.

## Vòng lặp sửa lỗi

```
biên dịch → đọc lỗi đầu tiên → sửa đúng một chỗ → biên dịch lại
```

Những lần sửa nhỏ, thường xuyên thắng những đợt viết lại lớn. Đến module 3, bạn sẽ liếc một lỗi và biết ngay nó thuộc *loại* nào trước khi đọc chi tiết — lúc đó C++ không còn đáng sợ nữa.
''',
)

# ---- Module 1 checkpoint ----
write_checkpoint(
    M1, L1E,
    "Checkpoint: C++ Fundamentals",
    "Prove the fundamentals: fix a broken program's structure and produce exact output. One graded challenge.",
    15,
    '''
**Checkpoint — C++ fundamentals.** Graded challenge below; pass it to complete the module.

You will repair a program that refuses to compile (missing pieces of the skeleton you now know by heart) and then make its output exact. Everything needed is in lessons 1A–1D. If the compiler complains, read the first error, fix, recompile — the loop is the lesson.
''',
    "Checkpoint: Nền tảng C++",
    "Chứng minh nền tảng của bạn: sửa một chương trình lỗi cấu trúc và tạo output chính xác. Một challenge có chấm điểm.",
    '''
**Checkpoint — nền tảng C++.** Challenge có chấm điểm bên dưới; vượt qua để hoàn thành module.

Bạn sẽ sửa một chương trình không biên dịch được (thiếu những mảnh khung mà bạn giờ thuộc lòng) và sau đó tạo output chính xác. Mọi thứ cần thiết nằm trong các bài 1A–1D. Nếu compiler phàn nàn, hãy đọc lỗi đầu tiên, sửa, biên dịch lại — chính vòng lặp đó là bài học.
''',
    challenge(
        "cpp1-check-hello-fix",
        "Fix and Print",
        "Fix the broken program, then make `program()` print exactly three lines:\\n`CIEN`\\n`compiles clean`\\n`ships on time`\\n(The program must also compile: it is missing its include, its return statement, and a semicolon.)",
        "#include <iostream>\\n\\nvoid program() {\\n    // TODO: print three lines exactly\\n    std::cout << \"CIEN\";\\n    std::cout << \"compiles clean\"\\n    std::cout << \"ships on time\";\\n}\\n\\nint main() {\\n\\n}",
        [
            ("three exact lines", 'auto out = capture([]{ program(); });\\nCHECK_LINES(out, {"CIEN", "compiles clean", "ships on time"});', "Print the three lines in order, separated by newlines (use `std::endl` or `\\\\n`)."),
            ("compiles cleanly", 'CHECK(true);', "The whole program must compile — the missing include, semicolon, and return statement must be repaired."),
        ],
        level="debugging",
    ),
    vi_challenge(
        "Sửa lỗi và in ra",
        "Sửa chương trình bị lỗi, sau đó khiến `program()` in đúng ba dòng:\\n`CIEN`\\n`compiles clean`\\n`ships on time`\\n(Chương trình cũng phải biên dịch được: nó đang thiếu include, lệnh return, và một dấu chấm phẩy.)",
        [("ba dòng chính xác", "In ba dòng theo đúng thứ tự, ngăn cách bằng dấu xuống dòng (dùng `std::endl` hoặc `\\\\n`)."), ("biên dịch sạch", "Toàn bộ chương trình phải biên dịch được — include, dấu chấm phẩy, và lệnh return còn thiếu phải được sửa.")],
    ),
    solution='#include <iostream>\\n\\nvoid program() {\\n    std::cout << "CIEN\\ncompiles clean\\nships on time\\n";\\n}\\n\\nint main() {\\n    program();\\n    return 0;\\n}',
    wrong='#include <iostream>\\n\\nvoid program() {\\n    std::cout << "CIEN\\ncompiles clean\\nships on time";\\n}\\n\\nint main() {\\n    program();\\n}',
)

# ---- Module 1 practice sets ----
write_practice(
    M1, "m1-hello-practice",
    "Hello Practice: Output Basics",
    "Six output challenges: exact lines, chained values, and prediction. Every solution is two or three lines of std::cout.",
    "Luyện Hello: Nền tảng Output",
    "Sáu challenge về output: dòng chính xác, giá trị nối chuỗi, và dự đoán. Mỗi lời giải chỉ là hai đến ba dòng std::cout.",
    L1B, 20, "beginner",
    [
        challenge(
            "cpp1-hello-world",
            "Hello, Code Journey",
            "Make `program()` print exactly:\\n`Hello, Code Journey!`",
            '#include <iostream>\\n\\nvoid program() {\\n    // your code\\n}\\n\\nint main() {\\n    program();\\n    return 0;\\n}',
            [("exact greeting", 'auto out = capture([]{ program()\\n});\\nCHECK_CONTAINS(out, "Hello, Code Journey!");', "Print the exact string with std::cout and <<.")],
            level="imitation",
        ),
    ],
    {"cpp1-hello-world": vi_challenge("Hello, Code Journey", "Khiến `program()` in đúng:\\n`Hello, Code Journey!`", [("lời chào chính xác", "In đúng chuỗi bằng std::cout và <<.")])},
    solutions=[
        ("cpp1-hello-world", 'void program() { std::cout << "Hello, Code Journey!\\n"; }', 'void program() { std::cout << "Hello Code Journey!\\n"; }'),
    ],
)

write_practice(
    M1, "m1-errors-practice",
    "Fix the Build: First Errors",
    "Meet the four classic build breakers on purpose — missing semicolons, typos, missing std, and a missing return — and repair them.",
    "Sửa bản build: Lỗi đầu tiên",
    "Chủ động gặp bốn loại lỗi build kinh điển — thiếu chấm phẩy, lỗi chính tả, thiếu std, thiếu return — và sửa chúng.",
    L1D, 25, "beginner",
    [
        challenge(
            "cpp1-fix-semicolon",
            "Repair: Missing Semicolon",
            "This program fails with `expected ';' before '}' token`. Fix it so it compiles and prints `fixed!`.",
            '#include <iostream>\\n\\nvoid program() {\\n    std::cout << "fixed!"\\n}\\n\\nint main() {\\n    program();\\n    return 0;\\n}',
            [("prints fixed", 'auto out = capture([]{ program(); });\\nCHECK_CONTAINS(out, "fixed!");', "Add the missing semicolon after the cout statement.")],
            level="debugging",
        ),
    ],
    {"cpp1-fix-semicolon": vi_challenge("Sửa lỗi: Thiếu dấu chấm phẩy", "Chương trình này báo lỗi `expected ';' before '}' token`. Hãy sửa để nó biên dịch và in ra `fixed!`.", [("in ra fixed", "Thêm dấu chấm phẩy còn thiếu sau lệnh cout.")])},
    solutions=[
        ("cpp1-fix-semicolon", 'void program() { std::cout << "fixed!\\n"; }', 'void program() { std::cout << "fixed!" }'),
    ],
)

# ============================ MODULE 2: variables-and-types ============================
M2 = "variables-and-types"

L2A = "variables-and-initialization"
L2B = "operators-and-conversion"
L2C = "const-and-auto"
L2D = "checkpoint-types"

write_module(
    M2,
    "Variables, Types & Expressions",
    "Declare, initialize and transform data: primitive types, operators, integer division traps, const correctness, and when auto helps.",
    "Biến, Kiểu & Biểu thức",
    "Khai báo, khởi tạo và biến đổi dữ liệu: kiểu nguyên thủy, toán tử, bẫy chia số nguyên, const correctness, và khi nào auto hữu ích.",
    [L2A, L2B, L2C, L2D],
    ["m2-vars-practice", "m2-ops-practice"],
)

write_lesson(
    M2, L2A,
    "Variables and Initialization",
    "Types, declaration, initialization, assignment, and the brace-initialization habit that catches narrowing bugs.",
    11,
    '''
A **variable** is a named piece of memory with a type. In C++, you declare it once and the compiler enforces the type forever:

```cpp
int score = 0;            // whole numbers
double price = 19.99;     // floating point
char grade = 'A';         // a single character (single quotes!)
bool passed = true;       // true or false
std::string name = "Ha";  // text (double quotes) — needs #include <string>
```

## Declaration vs initialization vs assignment

- **Declaration** creates the variable: `int x;`
- **Initialization** gives it its first value — do it on the same line, always.
- **Assignment** replaces the value later: `x = 5;`

An uninitialized variable contains garbage. Not "zero", not "empty" — *garbage*: whatever bits were already in that memory. Reading it is undefined behavior.

## Brace initialization — the modern default

```cpp
int width{10};          // preferred modern form
int y = 3.7;            // compiles: y becomes 3 — silently!
int z{3.7};             // error: narrowing conversion — compiler catches it
```

Braces refuse lossy conversions. That is why this course writes `{}` for new variables: the compiler becomes your safety net.

## `auto` — say the type once

```cpp
auto count = 10;        // int — the compiler deduces it from the initializer
auto ratio = 0.5;       // double
auto title = std::string{"Report"};
```

`auto` is not a "dynamic type" (types are still fixed at compile time); it just avoids repeating them. Rule of thumb in this course: use explicit types for simple values, `auto` when the type is obvious from the right-hand side. (More in lesson 2C.)

## Names matter

`int x2tmp1;` compiles; `int pending_items;` communicates. Modern C++ style: `snake_case` for variables and functions, `PascalCase` for types you will meet in module 10.

**Practice next:** declare, initialize, and compute — the compiler will grade your types.
''',
    "Biến và khởi tạo",
    "Kiểu dữ liệu, khai báo, khởi tạo, gán giá trị, và thói quen khởi tạo bằng ngoặc nhọn giúp bắt lỗi thu hẹp kiểu.",
    '''
Một **biến** là một vùng bộ nhớ có tên và có kiểu. Trong C++, bạn khai báo nó một lần và compiler sẽ thực thi kiểu đó mãi mãi:

```cpp
int score = 0;            // số nguyên
double price = 19.99;     // số thực
char grade = 'A';         // một ký tự (nháy đơn!)
bool passed = true;       // true hoặc false
std::string name = "Ha";  // text (nháy kép) — cần #include <string>
```

## Khai báo, khởi tạo và gán

- **Khai báo** tạo ra biến: `int x;`
- **Khởi tạo** gán giá trị đầu tiên — hãy làm ngay trên cùng một dòng, luôn luôn.
- **Gán** thay giá trị sau đó: `x = 5;`

Biến chưa khởi tạo chứa dữ liệu rác. Không phải "0", không phải "rỗng" — *rác*: những bit đã nằm sẵn trong vùng nhớ đó. Đọc nó là hành vi không xác định (undefined behavior).

## Khởi tạo bằng ngoặc nhọn — chuẩn hiện đại

```cpp
int width{10};          // dạng hiện đại được ưa chuộng
int y = 3.7;            // biên dịch được: y thành 3 — âm thầm!
int z{3.7};             // lỗi: narrowing conversion — compiler bắt được
```

Ngoặc nhọn từ chối các phép chuyển kiểu làm mất dữ liệu. Vì vậy khóa này viết `{}` cho biến mới: compiler trở thành lưới an toàn của bạn.

## `auto` — chỉ nói kiểu một lần

```cpp
auto count = 10;        // int — compiler suy ra từ giá trị khởi tạo
auto ratio = 0.5;       // double
auto title = std::string{"Report"};
```

`auto` không phải "kiểu động" (kiểu vẫn cố định lúc biên dịch); nó chỉ giúp không phải lặp lại. Nguyên tắc trong khóa này: dùng kiểu tường minh cho giá trị đơn giản, dùng `auto` khi kiểu đã hiển nhiên từ vế phải. (Chi tiết ở bài 2C.)

## Tên biến quan trọng

`int x2tmp1;` biên dịch được; `int pending_items;` truyền đạt ý nghĩa. Phong cách C++ hiện đại: `snake_case` cho biến và hàm, `PascalCase` cho kiểu (bạn sẽ gặp ở module 10).

**Luyện tập tiếp theo:** khai báo, khởi tạo và tính toán — compiler sẽ chấm kiểu của bạn.
''',
)

write_lesson(
    M2, L2B,
    "Operators, Division Traps, and Conversion",
    "Arithmetic, comparison and logical operators; why 7/2 is 3; overflow in one sentence; and explicit casts.",
    12,
    '''
## Arithmetic

`+ - * / %` work as expected on integers and doubles — with one famous trap:

```cpp
std::cout << 7 / 2;      // 3   — integer / integer = integer!
std::cout << 7.0 / 2;    // 3.5 — one double makes the whole expression double
std::cout << 7 % 2;      // 1   — remainder (modulo)
```

**Integer division truncates.** If a calculation *should* be fractional, at least one operand must be a double. `%` is for integers only and is everywhere in real code: even/odd checks, ring buffers, pagination.

## Comparison and logic

Comparisons produce `bool`: `== != < <= > >=`. Combine them with `&&` (and), `||` (or), `!` (not). Precedence trips beginners, so when in doubt, parenthesize:

```cpp
if ((age >= 18) && (has_ticket)) { /* ... */ }
```

(Real bug to avoid: `=` assigns, `==` compares. `if (x = 5)` compiles — and is almost never what you meant.)

## Conversion: implicit and explicit

```cpp
int small = 3.9;               // implicit: 3, silently (why braces are better)
double avg = static_cast<double>(total) / count;   // explicit, honest
```

`static_cast<double>(x)` says out loud "I want a real-numbered division here". This course uses `static_cast` — never C-style `(double)x` casts, which are hard to search for and can silently succeed where they should fail.

## Overflow in one sentence

Every type has limits (`int` is typically ±2.1 billion). Computing past them **wraps around silently** — there is no exception. The beginner defense is simply: pick a sensible type (`long long` for big counts) and know that overflow exists. Deep handling is Intermediate material.

## Practice focus

The exercises here are pure computation — unit conversions, bill splits, grade averages — chosen because each one famously bites beginners with the division trap at least once.
''',
    "Toán tử, bẫy chia số nguyên, và chuyển kiểu",
    "Toán tử số học, so sánh và logic; vì sao 7/2 bằng 3; overflow trong một câu; và phép ép kiểu tường minh.",
    '''
## Số học

`+ - * / %` hoạt động như mong đợi trên số nguyên và số thực — với một cái bẫy nổi tiếng:

```cpp
std::cout << 7 / 2;      // 3   — nguyên / nguyên = nguyên!
std::cout << 7.0 / 2;    // 3.5 — chỉ cần một double để cả biểu thức thành double
std::cout << 7 % 2;      // 1   — số dư (modulo)
```

**Chia số nguyên cắt phần thập phân.** Nếu phép tính *phải* có phần lẻ, ít nhất một toán hạng phải là double. `%` chỉ dùng cho số nguyên và xuất hiện khắp nơi trong code thật: kiểm tra chẵn/lẻ, bộ đệm vòng, phân trang.

## So sánh và logic

Phép so sánh cho ra `bool`: `== != < <= > >=`. Kết hợp bằng `&&` (và), `||` (hoặc), `!` (phủ định). Độ ưu tiên hay làm người mới vấp, nên cứ nghi ngờ thì đặt ngoặc:

```cpp
if ((age >= 18) && (has_ticket)) { /* ... */ }
```

(Bug thật cần tránh: `=` là gán, `==` là so sánh. `if (x = 5)` vẫn biên dịch được — và hầu như không bao giờ là điều bạn muốn.)

## Chuyển kiểu: ngầm định và tường minh

```cpp
int small = 3.9;               // ngầm định: 3, âm thầm (vì sao ngoặc nhọn tốt hơn)
double avg = static_cast<double>(total) / count;   // tường minh, rõ ràng
```

`static_cast<double>(x)` nói to "tôi muốn phép chia số thực ở đây". Khóa này dùng `static_cast` — không bao giờ dùng kiểu ép kiểu kiểu C `(double)x`, thứ khó tìm kiếm và có thể âm thầm thành công ở nơi đáng ra phải thất bại.

## Overflow trong một câu

Mọi kiểu đều có giới hạn (`int` thường là ±2,1 tỷ). Tính toán vượt giới hạn sẽ **vòng lại một cách âm thầm** — không có exception nào cả. Phòng thủ của người mới chỉ đơn giản là: chọn kiểu hợp lý (`long long` cho số đếm lớn) và biết rằng overflow tồn tại. Xử lý sâu là môn của Trung cấp.

## Trọng tâm luyện tập

Các bài tập ở đây thuần tính toán — đổi đơn vị, chia hóa đơn, điểm trung bình — được chọn vì mỗi bài đều nổi tiếng làm người mới trúng bẫy chia số nguyên ít nhất một lần.
''',
)

write_lesson(
    M2, L2C,
    "const and auto",
    "Make immutability the default with const, use auto where types are obvious, and learn what constexpr hints at.",
    9,
    '''
## `const`: promise the compiler (and your teammates) it won't change

```cpp
const double vat_rate = 0.1;
vat_rate = 0.2;          // error — and that is the point
```

A `const` variable cannot be assigned after initialization. Read it as "read-only". This is not bureaucracy: immutability shrinks the amount of state you must hold in your head, and it lets the compiler catch an entire bug class. This course's default is: **make every variable `const` unless it genuinely changes.**

`const` also documents intent better than any comment: a reader sees `const` and stops wondering whether that value mutates later.

## `auto` with const

`auto` drops top-level `const`/references by default — a subtle rule you will meet again in module 11. For now:

```cpp
const double rate{0.1};
auto r = rate;           // r is double (copy) — fine here
```

When in doubt in these early modules, write the explicit type; reach for `auto` when the initializer makes it obvious.

## A glimpse of `constexpr`

```cpp
constexpr int kDays_in_week = 7;   // known at compile time
```

`constexpr` means "this value is computed at compile time". You will mostly write `const`; `constexpr` appears in real codebases for true constants. Knowing it exists is enough for Beginner.

## Style note

You will see two camps for constants: `kDaysInWeek` (Google-style) and `DAYS_IN_WEEK`. Pick one per project, stay consistent — and prefer `constexpr`/`const` over `#define` macros, which do not respect scope or types.
''',
    "const và auto",
    "Đặt tính bất biến làm mặc định với const, dùng auto khi kiểu hiển nhiên, và tìm hiểu constexpr gợi ý điều gì.",
    '''
## `const`: hứa với compiler (và đồng đội) rằng nó sẽ không đổi

```cpp
const double vat_rate = 0.1;
vat_rate = 0.2;          // lỗi — và đó chính là điều ta muốn
```

Biến `const` không thể bị gán sau khi khởi tạo. Hãy đọc là "chỉ đọc". Đây không là quan liêu: tính bất biến làm giảm lượng trạng thái bạn phải nhớ trong đầu, và cho compiler bắt được cả một lớp bug. Mặc định của khóa này là: **hãy thêm `const` cho mọi biến trừ khi nó thật sự thay đổi.**

`const` còn truyền đạt ý định tốt hơn mọi comment: người đọc thấy `const` và thôi tự hỏi liệu giá trị đó có bị thay đổi sau này không.

## `auto` với const

`auto` bỏ `const`/reference mức trên theo mặc định — một quy tắc tinh tế bạn sẽ gặp lại ở module 11. Hiện tại:

```cpp
const double rate{0.1};
auto r = rate;           // r là double (bản sao) — ổn ở đây
```

Khi còn phân vân ở những module đầu, hãy viết kiểu tường minh; chỉ dùng `auto` khi vế khởi tạo khiến kiểu hiển nhiên.

## Liếc qua `constexpr`

```cpp
constexpr int kDays_in_week = 7;   // biết ngay lúc biên dịch
```

`constexpr` nghĩa là "giá trị này được tính lúc biên dịch". Bạn sẽ chủ yếu viết `const`; `constexpr` xuất hiện trong code thật cho các hằng số đúng nghĩa. Biết nó tồn tại là đủ cho trình độ Cơ bản.

## Ghi chú phong cách

Bạn sẽ thấy hai trường phái đặt tên hằng: `kDaysInWeek` (kiểu Google) và `DAYS_IN_WEEK`. Chọn một trong hai cho mỗi dự án và giữ nhất quán — và hãy ưu tiên `constexpr`/`const` thay vì macro `#define`, thứ không tôn trọng phạm vi lẫn kiểu.
''',
)

# ---- Module 2 checkpoint ----
write_checkpoint(
    M2, L2D,
    "Checkpoint: Types and Expressions",
    "One graded challenge: compute a receipt exactly right — prices, tax, and a bill split without the integer-division bug.",
    15,
    '''
**Checkpoint — types and expressions.** Pass the graded challenge below to finish the module.

It is a small receipt calculator: totals, a tax line, and an even bill split. The tests check exact numeric output — every famous trap from this module is waiting in it, once each.
''',
    "Checkpoint: Kiểu và biểu thức",
    "Một challenge có chấm: tính hóa đơn chính xác — giá tiền, thuế, và chia đều hóa đơn không dính bẫy chia số nguyên.",
    '''
**Checkpoint — kiểu và biểu thức.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Đây là một bài tính hóa đơn nhỏ: tổng cộng, dòng thuế, và chia đều tiền cho cả nhóm. Test kiểm tra đầu ra số chính xác — mỗi cái bẫy nổi tiếng của module này đang chờ trong đó, mỗi bẫy đúng một lần.
''',
    challenge(
        "cpp2-check-receipt",
        "Receipt Calculator",
        "Implement `receipt(price, people)` so `program()` prints exactly:\\n`total: 26.4` (price times 1.1 tax, as a double)\\n`per person: 13.2` (total split between 2 people — real division!)\\nBoth numbers must be doubles, printed with a single space after the label.",
        "#include <iostream>\\n\\nvoid program() {\\n    // TODO: compute and print\\n}\\n\\nint main() {\\n    program();\\n    return 0;\\n}",
        [
            ("taxed total", 'CHECK_NEAR(receipt_total(24.0), 26.4, 0.001);', "total = price * 1.1 — make sure the math is done in doubles."),
            ("fair split", 'CHECK_NEAR(receipt_per_person(24.0, 2), 13.2, 0.001);', "per person = total / people. If you divide integers you will get 13 instead of 13.2."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Máy tính hóa đơn",
        "Cài đặt `receipt` để `program()` in đúng:\\n`total: 26.4` (giá nhân 1.1 thuế, là số thực)\\n`per person: 13.2` (tổng chia cho 2 người — phép chia số thực!)\\nCả hai số phải là double, in với một dấu cách sau nhãn.",
        [("tổng sau thuế", "total = price * 1.1 — đảm bảo phép tính thực hiện trên double."), ("chia công bằng", "mỗi người = total / people. Nếu bạn chia số nguyên sẽ nhận được 13 thay vì 13.2.")],
    ),
    solution='double receipt_total(double price) { return price * 1.1; }\\ndouble receipt_per_person(double price, int people) { return price * 1.1 / people; }\\nvoid program() {\\n    std::cout << "total: " << receipt_total(24.0) << "\\n";\\n    std::cout << "per person: " << receipt_per_person(24.0, 2) << "\\n";\\n}',
    wrong='double receipt_total(double price) { return price * 1.1; }\\ndouble receipt_per_person(double price, int people) { return (int)(price * 1.1) / people; }\\nvoid program() {\\n    std::cout << "total: " << receipt_total(24.0) << "\\n";\\n    std::cout << "per person: " << receipt_per_person(24.0, 2) << "\\n";\\n}',
)

# ---- Module 2 practice sets ----
write_practice(
    M2, "m2-vars-practice",
    "Variables Practice",
    "Declare, initialize, convert — including the brace-initialization narrowing check and swap-without-temp.",
    "Luyện Biến",
    "Khai báo, khởi tạo, chuyển kiểu — gồm cả kiểm tra thu hẹp kiểu bằng ngoặc nhọn và hoán đổi không cần biến tạm.",
    L2A, 20, "beginner",
    [
        challenge(
            "cpp2-swap-values",
            "Swap Two Variables",
            "Implement `swapThem(a, b)` so that after it runs, `a` holds the old `b` and vice versa. (Yes, `std::swap` exists — write it by hand once so you feel the assignment semantics.)",
            "void swapThem(int& a, int& b) {\\n    // TODO\\n}",
            [("swapped", "int a = 1, b = 2;\\nswapThem(a, b);\\nCHECK_EQ(a, 2);\\nCHECK_EQ(b, 1);", "Use a temporary: int tmp = a; a = b; b = tmp;")],
            level="imitation",
        ),
    ],
    {"cpp2-swap-values": vi_challenge("Hoán đổi hai biến", "Cài đặt `swapThem(a, b)` để sau khi chạy, `a` giữ giá trị cũ của `b` và ngược lại. (Ừ thì `std::swap` có sẵn — nhưng hãy tự viết một lần để cảm nhận ngữ nghĩa gán.)", [("đã hoán đổi", "Dùng biến tạm: int tmp = a; a = b; b = tmp;")])},
    solutions=[
        ("cpp2-swap-values", "void swapThem(int& a, int& b) { int tmp = a; a = b; b = tmp; }", "void swapThem(int& a, int& b) { int tmp = a; a = a; b = tmp; }"),
    ],
)

write_practice(
    M2, "m2-ops-practice",
    "Operators Practice: The Division Trap",
    "Unit conversion, averages, and even/odd — each hiding the integer-division or modulo lesson.",
    "Luyện Toán tử: Bẫy chia số nguyên",
    "Đổi đơn vị, trung bình, chẵn/lẻ — mỗi bài ẩn một bài học về chia số nguyên hoặc modulo.",
    L2B, 25, "beginner",
    [
        challenge(
            "cpp2-celsius",
            "Celsius to Fahrenheit",
            "Implement `to_fahrenheit(celsius)` using the formula F = C * 9/5 + 32. Beware: `9/5` in integers is 1!",
            "double to_fahrenheit(double celsius) {\\n    // TODO\\n}",
            [("freezing point", "CHECK_NEAR(to_fahrenheit(0.0), 32.0, 0.001);", "0°C is 32°F"), ("boiling point", "CHECK_NEAR(to_fahrenheit(100.0), 212.0, 0.001);", "100°C is 212°F"), ("body temp", "CHECK_NEAR(to_fahrenheit(37.0), 98.6, 0.001);", "37°C is 98.6°F")],
            level="guided",
        ),
    ],
    {"cpp2-celsius": vi_challenge("Độ C sang độ F", "Cài đặt `to_fahrenheit(celsius)` với công thức F = C * 9/5 + 32. Cẩn thận: `9/5` trong số nguyên là 1!", [("điểm đóng băng", "0°C là 32°F"), ("điểm sôi", "100°C là 212°F"), ("nhiệt độ cơ thể", "37°C là 98.6°F")])},
    solutions=[
        ("cpp2-celsius", "double to_fahrenheit(double celsius) { return celsius * 9.0 / 5.0 + 32.0; }", "double to_fahrenheit(double celsius) { return celsius * (9 / 5) + 32; }"),
    ],
)

print("modules 1-2 authored")
