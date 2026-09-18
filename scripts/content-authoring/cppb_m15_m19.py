#!/usr/bin/env python3
"""C++ Beginner — modules 15-19: multi-file/CMake, architecture, git, problem-solving, capstone."""
from cppb import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 15: multi-file-cmake ============================
M15 = "multi-file-cmake"

L15A = "headers-and-translation-units"
L15B = "linking-and-odr"
L15C = "cmake-basics"
L15D = "checkpoint-multi-file"

write_module(
    M15,
    "Multi-File Programs & CMake",
    "How C++ projects really build: headers, translation units, the linker's ODR rules, and your first CMake build.",
    "Chương trình nhiều file & CMake",
    "Dự án C++ thực sự được build thế nào: header, translation unit, quy tắc ODR của linker, và lần build CMake đầu tiên của bạn.",
    [L15A, L15B, L15C, L15D],
    ["m15-declare-practice"],
)

write_lesson(
    M15, L15A,
    "Headers, Translation Units, Declarations vs Definitions",
    "Why every .cpp compiles alone, what a header promises, include guards, and the declaration/definition split.",
    12,
    '''
## The compiler's blindfold

The compiler compiles **one translation unit at a time** — one `.cpp` file after preprocessing. It has *no idea* what other `.cpp` files contain. Everything it needs must be visible: either defined in the file or **declared** via a header.

```cpp
// math_utils.h — the PROMISE (declarations)
#pragma once
#include <string>

int add(int a, int b);
std::string shout(std::string text);
```

```cpp
// math_utils.cpp — the DELIVERY (definitions)
#include "math_utils.h"

int add(int a, int b) { return a + b; }
std::string shout(std::string text) { return text + "!"; }
```

```cpp
// main.cpp — the USER
#include <iostream>
#include "math_utils.h"     // quotes: "our" headers; angles: the standard library

int main() {
    std::cout << add(2, 3) << '\\n';
}
```

**Declarations say what exists; definitions say how.** A function may be declared many times but defined once (across the whole program). Classes in headers are definitions (the compiler needs their size); their method *bodies* may live in the `.cpp`.

## Why this split?

Change `math_utils.cpp`'s implementation and only *that file* recompiles, then the **linker** re-stitches the program. In big projects this is the difference between 1-second and 30-minute builds. It is also how teams divide work: headers are the contracts; nobody needs your `.cpp` to use your code.

## `#pragma once` (and the older guards)

Headers must not be pasted twice into one translation unit. `#pragma once` (supported by all major compilers) or classic `#ifndef MATH_UTILS_H / #define / #endif` guards. Modern code writes `#pragma once`; know the classic form for reading old code.

## The graded-world connection

This platform grades single files — `#include "solution.cpp"` is the harness stitching your code into its test translation unit. Same mechanism, smaller project. On your own machine, the commands are:

```
g++ -std=c++20 -Wall -Wextra main.cpp math_utils.cpp -o app
```
''',
    "Header, Translation Unit, Khai báo so với Định nghĩa",
    "Vì sao mỗi .cpp biên dịch một mình, header hứa điều gì, include guard, và cặp khai báo/định nghĩa.",
    '''
## bịt mắt của compiler

Compiler biên dịch **từng translation unit một** — một file `.cpp` sau tiền xử lý. Nó *hoàn toàn không biết* các file `.cpp` khác chứa gì. Mọi thứ nó cần phải hiện diện: hoặc định nghĩa ngay trong file, hoặc được **khai báo** qua một header.

```cpp
// math_utils.h — LỜI HỨA (khai báo)
#pragma once
#include <string>

int add(int a, int b);
std::string shout(std::string text);
```

```cpp
// math_utils.cpp — PHẦN THỰC HIỆN (định nghĩa)
#include "math_utils.h"

int add(int a, int b) { return a + b; }
std::string shout(std::string text) { return text + "!"; }
```

```cpp
// main.cpp — NGƯỜI DÙNG
#include <iostream>
#include "math_utils.h"     // dấu nháy: header "của ta"; ngoặc nhọn: thư viện chuẩn

int main() {
    std::cout << add(2, 3) << '\\n';
}
```

**Khai báo nói cái gì tồn tại; định nghĩa nói làm thế nào.** Một hàm có thể được khai báo nhiều lần nhưng chỉ được định nghĩa một lần (trên toàn chương trình). Class trong header là định nghĩa (compiler cần biết kích thước); *thân* hàm của chúng có thể nằm trong `.cpp`.

## Vì sao lại tách riêng?

Sửa phần cài đặt trong `math_utils.cpp` và chỉ *file đó* biên dịch lại, rồi **linker** khâu lại chương trình. Trong dự án lớn, đó là khác biệt giữa build 1 giây và 30 phút. Nó cũng là cách nhóm chia việc: header là bản hợp đồng; không ai cần file `.cpp` của bạn để dùng code của bạn.

## `#pragma once` (và kiểu bảo vệ cổ điển)

Header không được bị dán vào một translation unit hai lần. `#pragma once` (mọi compiler lớn đều hỗ trợ) hoặc dạng bảo vệ cổ điển `#ifndef MATH_UTILS_H / #define / #endif`. Code hiện đại viết `#pragma once`; hãy biết dạng cổ để đọc code cũ.

## Liên hệ với thế giới có chấm điểm

Nền tảng này chấm từng file đơn — `#include "solution.cpp"` chính là harness khâu code của bạn vào translation unit của test. Cùng cơ chế, dự án nhỏ hơn. Trên máy của bạn, câu lệnh là:

```
g++ -std=c++20 -Wall -Wextra main.cpp math_utils.cpp -o app
```
''',
)

write_lesson(
    M15, L15B,
    "Linking and the One-Definition Rule",
    "What the linker does, the two errors it exists to produce (undefined reference, multiple definition), and the inline/const file-scope rules.",
    11,
    '''
## Two phases, two tools

1. **Compile** each `.cpp` → an object file (`.o`): machine code with *unresolved* names ("I call a function named `add` — somebody has it").
2. **Link** all object files + libraries → one executable: every unresolved name finds its definition.

## The linker's two famous errors

**`undefined reference to 'add'`** — you promised (declared) it, nobody delivered (no definition anywhere). Usual causes: forgot to compile the `.cpp`, misspelled the definition's signature, forgot a library flag.

**`multiple definition of 'add'`** — the definition appears twice. Classic cause: defining a non-inline function *in a header* that several `.cpp` files include. Each translation unit gets its own copy; the linker refuses to choose.

## The rules that keep headers linkable

- Functions: declare in headers, define in a `.cpp`.
- One exception you will see: small functions defined inside the class body in a header are implicitly `inline` — the linker merges them.
- Global constants: `constexpr`/`const` at namespace scope have internal linkage by default (each file gets its own — fine), or use `inline constexpr` in headers for one shared copy.
- Never put `using namespace std;` in a header — it leaks into every includer (module 1's warning, now you know the blast radius).

## Why "undefined reference" mentions no line number

The linker works on object files — your line numbers are gone. Read the *mangled name* in the message (`add(int, int)`) and compare against your declaration character by character; a signature mismatch compiles fine and fails only here. This is the error that teaches you that C++ has two compilers' worth of failure modes.
''',
    "Linking và Quy tắc Một-Định-nghĩa",
    "Linker làm gì, hai lỗi mà nó sinh ra để tồn tại (undefined reference, multiple definition), và các quy tắc inline/const ở phạm vi file.",
    '''
## Hai pha, hai công cụ

1. **Biên dịch** từng `.cpp` → một file đối tượng (`.o`): mã máy với các tên *chưa giải quyết* ("tôi gọi một hàm tên `add` — ai đó đang giữ nó").
2. **Liên kết** tất cả file đối tượng + thư viện → một file thực thi: mọi tên chưa giải quyết tìm thấy định nghĩa của nó.

## Hai lỗi nổi tiếng của linker

**`undefined reference to 'add'`** — bạn đã hứa (khai báo), nhưng không ai thực hiện (không có định nghĩa ở đâu cả). Nguyên nhân thường gặp: quên biên dịch file `.cpp`, đánh vần sai chữ ký của định nghĩa, quên cờ thư viện.

**`multiple definition of 'add'`** — định nghĩa xuất hiện hai lần. Nguyên nhân kinh điển: định nghĩa một hàm non-inline *ngay trong header* mà nhiều file `.cpp` include. Mỗi translation unit có một bản sao; linker từ chối lựa chọn thay bạn.

## Các quy tắc giữ header "link được"

- Hàm: khai báo trong header, định nghĩa trong một `.cpp`.
- Một ngoại lệ bạn sẽ thấy: các hàm nhỏ định nghĩa ngay trong thân class trong header là `inline` ngầm — linker tự gộp chúng.
- Hằng toàn cục: `constexpr`/`const` ở phạm vi namespace mặc định có liên kết nội bộ (mỗi file một bản riêng — ổn), hoặc dùng `inline constexpr` trong header để có một bản dùng chung.
- Đừng bao giờ đặt `using namespace std;` trong header — nó rò ra mọi nơi include nó (cảnh báo của module 1, giờ bạn biết tầm sát thương).

## Vì sao "undefined reference" không nêu số dòng

Linker làm việc với file đối tượng — số dòng của bạn đã biến mất. Hãy đọc *tên xáo trộn* trong thông báo (`add(int, int)`) và so với khai báo của bạn từng ký tự; một chữ ký lệch nhau vẫn biên dịch ngon lành và chỉ vỡ ở đây. Đây là lỗi dạy bạn rằng C++ có hai tầng kiểu lỗi khác nhau.
''',
)

write_lesson(
    M15, L15C,
    "CMake: Building Like a Professional",
    "Targets, source lists, and the two-command build — the beginner CMake that scales honestly.",
    12,
    '''
## Why not just long g++ commands?

`g++ main.cpp math_utils.cpp ... -o app` does not scale: 40 files, include paths, libraries, Debug/Release flags. **CMake** describes the project *once*; it generates the right build commands for any platform.

## The minimal honest CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)
project(finance LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(finance
    src/main.cpp
    src/ledger.cpp
    src/report.cpp
)

target_compile_options(finance PRIVATE -Wall -Wextra -Wpedantic)
```

Read it as a sentence: "a project named finance, C++20, one executable target `finance` from these sources, with warnings on for this target."

- **Target** is the unit of everything: an executable or a library, its sources, its flags, its dependencies.
- `PRIVATE` means the flags apply to building this target only.

## The two-command build (memorize these)

```
cmake -B build            # configure: read CMakeLists, generate build files into build/
cmake --build build       # build: compile + link via the generated system
./build/finance           # run
```

`-B build` keeps all generated files in one directory (git-ignored — module 17). Re-run configure after editing CMakeLists; re-run build after editing code — it recompiles only what changed.

## Debug vs Release

```
cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug      # -g, no optimization: debuggable
cmake -B build-release -DCMAKE_BUILD_TYPE=Release  # -O2: fast, unreadable in a debugger
```

Debug while developing; release when measuring or shipping. (Sanitizers attach to the Debug build — Intermediate territory, name-checked here.)

## What Beginner CMake is NOT

No custom functions, no package hunting (`find_package`), no install rules. When a project needs those, it has outgrown Beginner — and now it has the vocabulary to say so.
''',
    "CMake: Build như dân chuyên",
    "Target, danh sách file nguồn, và build hai lệnh — mức CMake cho người mới mà vẫn trung thực khi mở rộng.",
    '''
## Vì sao không dùng lệnh g++ dài?

`g++ main.cpp math_utils.cpp ... -o app` không mở rộng được: 40 file, đường dẫn include, thư viện, cờ Debug/Release. **CMake** mô tả dự án *một lần*; nó sinh ra đúng các lệnh build cho bất kỳ nền tảng nào.

## CMakeLists.txt tối thiểu và trung thực

```cmake
cmake_minimum_required(VERSION 3.20)
project(finance LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(finance
    src/main.cpp
    src/ledger.cpp
    src/report.cpp
)

target_compile_options(finance PRIVATE -Wall -Wextra -Wpedantic)
```

Đọc nó như một câu: "một dự án tên finance, C++20, một target thực thi `finance` từ các nguồn này, bật cảnh báo cho target này."

- **Target** là đơn vị của mọi thứ: một file thực thi hoặc một thư viện, các nguồn của nó, cờ của nó, các phụ thuộc của nó.
- `PRIVATE` nghĩa là cờ chỉ áp dụng khi build target này.

## Build hai lệnh (học thuộc)

```
cmake -B build            # configure: đọc CMakeLists, sinh file build vào build/
cmake --build build       # build: biên dịch + liên kết qua hệ thống đã sinh
./build/finance           # chạy
```

`-B build` giữ mọi file được sinh trong một thư mục (git-ignored — module 17). Chạy lại configure sau khi sửa CMakeLists; chạy lại build sau khi sửa code — nó chỉ biên dịch lại phần thay đổi.

## Debug so với Release

```
cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug      # -g, không tối ưu: dễ debug
cmake -B build-release -DCMAKE_BUILD_TYPE=Release  # -O2: nhanh, khó đọc trong debugger
```

Debug khi đang phát triển; release khi đo hiệu năng hoặc bàn giao. (Sanitizer gắn vào bản Debug — miền của Trung cấp, nhắc tên tại đây.)

## CMake ở trình độ Cơ bản KHÔNG là gì

Không có hàm tùy biến, không săn package (`find_package`), không luật cài đặt. Khi một dự án cần những thứ đó, nó đã vượt khỏi Cơ bản — và giờ bạn có từ vựng để nói điều đó.
''',
)

# ---- Module 15 checkpoint ----
write_checkpoint(
    M15, L15D,
    "Checkpoint: Multi-File Thinking",
    "One graded challenge: given headers and implementations, spot the ODR violation and the declaration that fixes a link error.",
    15,
    '''
**Checkpoint — multi-file.** Pass the graded challenge below to finish the module.

Graded in the platform's single-file world, but the questions are exactly the two-file ones: what breaks the link, and what fixes it.
''',
    "Checkpoint: Tư duy nhiều file",
    "Một challenge có chấm: với header và phần cài đặt cho trước, chỉ ra lỗi vi phạm ODR và phần khai báo sửa được lỗi liên kết.",
    '''
**Checkpoint — nhiều file.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Chấm điểm trong thế giới một-file của nền tảng, nhưng các câu hỏi đúng là các câu hỏi hai-file: cái gì phá vỡ liên kết, và cái gì sửa được nó.
''',
    challenge(
        "cpp15-check-link-model",
        "Header Contract Model",
        "Model a multi-file project in one file: implement `int add(int, int)` (the \"math_utils.cpp\" definition), a `bool declared_only(int)` that must exist so the \"main.cpp\" side links (declare-and-define pattern), and `int call_add(int, int)` which calls `add` through its declaration-style usage. Then fix the classic bug: `kMaxRetries` must be a shared constant usable from \"several files\" — define it correctly for a header.",
        "#include <string>\\n\\n// TODO: implement add, declared_only, call_add\\n// TODO: define kMaxRetries the header-safe way (inline constexpr int)",
        [
            ("add works", "CHECK_EQ(add(2, 3), 5);", "The definition side of the contract."),
            ("declared_and_defined", "CHECK(declared_only(1));", "A function that exists so the other file's call links."),
            ("call through", "CHECK_EQ(call_add(2, 3), 5);", "Calls add — the linking pattern in miniature."),
            ("header constant", "CHECK_EQ(kMaxRetries, 3);", "inline constexpr at namespace scope: one shared definition, no ODR problem."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Mô hình bản hợp đồng header",
        "Mô hình hóa một dự án nhiều file trong một file: cài `int add(int, int)` (định nghĩa phía \"math_utils.cpp\"), một `bool declared_only(int)` phải tồn tại để phía \"main.cpp\" liên kết được (mẫu khai-báo-và-định-nghĩa), và `int call_add(int, int)` gọi `add` theo kiểu dùng qua khai báo. Sau đó sửa bug kinh điển: `kMaxRetries` phải là hằng số dùng chung được từ \"nhiều file\" — định nghĩa nó đúng cách cho header.",
        [("add chạy", "Phía định nghĩa của bản hợp đồng."), ("khai báo và định nghĩa", "Một hàm tồn tại để lời gọi từ file khác liên kết được."), ("gọi gián tiếp", "Gọi add — mẫu liên kết ở phiên bản thu nhỏ."), ("hằng cho header", "inline constexpr ở phạm vi namespace: một định nghĩa dùng chung, không vấn đề ODR.")],
    ),
    solution="#include <string>\\ninline constexpr int kMaxRetries = 3;\\nint add(int a, int b) { return a + b; }\\nbool declared_only(int v) { return v >= 0; }\\nint call_add(int a, int b) { return add(a, b); }",
    wrong="#include <string>\\nint kMaxRetries = 3;\\nint add(int a, int b) { return a + b; }\\nbool declared_only(int v) { return v >= 0; }\\nint call_add(int a, int b) { return add(a, b); }",
)

# ---- Module 15 practice ----
write_practice(
    M15, "m15-declare-practice",
    "Multi-File Practice: Contracts on Paper",
    "Write the declaration set for a tiny library and a default-argument overload pair.",
    "Luyện Nhiều file: Bản hợp đồng trên giấy",
    "Viết bộ khai báo cho một thư viện bé xíu và một cặp overload với đối số mặc định.",
    L15A, 20, "beginner",
    [
        challenge(
            "cpp15-default-args",
            "Default Arguments",
            "Implement `greet(name, greeting=\"Hello\")` returning `\"<greeting>, <name>!\"`, and a two-function overload pair `volume(side)` / `volume(w, h, d)` for cube and box.",
            "#include <string>\\n\\nstd::string greet(const std::string& name, const std::string& greeting) {\\n    // TODO\\n}\\nint volume(int side) {\\n    // TODO (cube)\\n}\\nint volume(int w, int h, int d) {\\n    // TODO (box)\\n}",
            [("default", "CHECK(greet(std::string{\"Linh\"}) == std::string{\"Hello, Linh!\"});", "The default greeting fills in."), ("explicit", "CHECK(greet(std::string{\"Linh\"}, std::string{\"Chao\"}) == std::string{\"Chao, Linh!\"});", "An explicit greeting overrides."), ("cube", "CHECK_EQ(volume(3), 27);", "side³."), ("box", "CHECK_EQ(volume(2, 3, 4), 24);", "w*h*d.")],
            level="imitation",
        ),
    ],
    {"cpp15-default-args": vi_challenge("Đối số mặc định", "Cài `greet(name, greeting=\"Hello\")` trả về `\"<greeting>, <name>!\"`, và cặp overload hai hàm `volume(side)` / `volume(w, h, d)` cho khối lập phương và hộp.", [("mặc định", "Lời chào mặc định được điền vào."), ("tường minh", "Lời chào tường minh ghi đè."), ("lập phương", "side³."), ("hộp", "w*h*d.")])},
    solutions=[
        ("cpp15-default-args", "#include <string>\\nstd::string greet(const std::string& name, const std::string& greeting = \"Hello\") {\\n    return greeting + \", \" + name + \"!\";\\n}\\nint volume(int side) { return side * side * side; }\\nint volume(int w, int h, int d) { return w * h * d; }", "#include <string>\\nstd::string greet(const std::string& name, const std::string& greeting = \"Hello\") {\\n    return name + \", \" + greeting + \"!\";\\n}\\nint volume(int side) { return side * side * side; }\\nint volume(int w, int h, int d) { return w * h * d; }"),
    ],
)

# ============================ MODULE 16: architecture-refactoring ============================
M16 = "architecture-refactoring"

L16A = "responsibilities-and-naming"
L16B = "refactor-a-mess"
L16C = "checkpoint-architecture"

write_module(
    M16,
    "Architecture & Refactoring",
    "Separating responsibilities, naming that documents, const-correctness as design — and refactoring a mess without breaking behavior.",
    "Kiến trúc & Refactoring",
    "Tách trách nhiệm, đặt tên thay cho tài liệu, const-correctness như một lựa chọn thiết kế — và refactor một mớ bời bời mà không hỏng hành vi.",
    [L16A, L16B, L16C],
    ["m16-refactor-practice"],
)

write_lesson(
    M16, L16A,
    "Responsibilities, Naming, and Const-Correct Design",
    "One responsibility per unit, names that replace comments, and const flowing through signatures as documentation.",
    11,
    '''
## The responsibility test

For every function, class, and file, finish this sentence honestly: "This unit's job is ______ and nothing else." If the sentence needs "and also", split it.

```
parse_line()      → text in, parsed fields out. No printing.
compute_totals()  → numbers in, totals out. No parsing.
print_report()    → data in, console out. No computing.
```

A **pipeline** of small units beats a giant that "does the feature". Each stage is testable (the platform's tests call each function), each is reusable, and each has one reason to change.

## Names are the cheapest documentation

```cpp
double d(double a, double b, int c);              // legal, opaque
double invoice_total(double price, double tax_rate, int qty);   // self-documenting
```

Rename until the signature reads like the requirement. Types carry meaning too: `long long cents` beats `double money` (exact arithmetic for currency — a classic lesson), `enum class Status` beats `int state`.

## const correctness as architecture

`const` in signatures is a machine-checked contract:

```cpp
std::vector<std::string> load_rows(const std::string& path);   // will not touch your path
void append_row(std::string& csv, const Row& row);             // will modify csv — visible
```

Reading a header, you know who mutates what without opening a single `.cpp`. This course's rule from module 2, scaled up: everything const until proven mutating.

## Dependency direction

Higher-level code (reports) may use lower-level code (parsing); lower levels must not reach upward. When two files need each other ("circular"), a third concept is hiding — extract it (a shared `Row` type, a small utility module). Data flows down; dependencies point down; debugging gets easy.
''',
    "Trách nhiệm, đặt tên, và thiết kế const-correct",
    "Mỗi đơn vị một trách nhiệm, cái tên thay được comment, và const chảy qua chữ ký như tài liệu.",
    '''
## Bài test trách nhiệm

Với mọi hàm, lớp, và file, hãy hoàn thành câu này một cách trung thực: "Nhiệm vụ của đơn vị này là ______ và không gì khác." Nếu câu cần thêm "và cả", hãy tách nó ra.

```
parse_line()      → text vào, các trường đã phân tích ra. Không in ấn.
compute_totals()  → số vào, tổng ra. Không phân tích.
print_report()    → dữ liệu vào, console ra. Không tính toán.
```

Một **chuỗi.pipeline** gồm các đơn vị nhỏ thắng một gã khổng lồ "làm cả tính năng". Mỗi chặng đều kiểm thử được (test của nền tảng gọi từng hàm), mỗi chặng dùng lại được, và mỗi chặng chỉ có một lý do để thay đổi.

## Tên là tài liệu rẻ nhất

```cpp
double d(double a, double b, int c);              // hợp lệ, mơ hồ
double invoice_total(double price, double tax_rate, int qty);   // tự dokumentasi
```

Đổi tên cho đến khi chữ ký đọc như yêu cầu. Kiểu dữ liệu cũng mang ý nghĩa: `long long cents` hơn `double money` (số học chính xác cho tiền tệ — bài học kinh điển), `enum class Status` hơn `int state`.

## const correctness như kiến trúc

`const` trong chữ ký là bản hợp đồng được máy kiểm tra:

```cpp
std::vector<std::string> load_rows(const std::string& path);   // sẽ không đụng vào path của bạn
void append_row(std::string& csv, const Row& row);             // sẽ sửa csv — nhìn thấy được
```

Đọc header, bạn biết ai sửa gì mà không cần mở một file `.cpp` nào. Quy tắc của khóa này từ module 2, nâng cấp: mọi thứ const cho đến khi bị chứng minh là có sửa đổi.

## Hướng phụ thuộc

Code cấp cao (báo cáo) có thể dùng code cấp thấp (phân tích); cấp thấp không được với lên trên. Khi hai file cần nhau ("tròn tròn"), một khái niệm thứ ba đang trốn — hãy tách nó ra (một kiểu `Row` dùng chung, một module tiện ích nhỏ). Dữ liệu chảy xuống; phụ thuộc trỏ xuống; việc debug trở nên dễ dàng.
''',
)

write_lesson(
    M16, L16B,
    "Refactor a Mess (Safely)",
    "The refactoring loop: characterize behavior first, small steps, compile+test after each — behavior preserved, structure improved.",
    11,
    '''
## The loop

1. **Characterize**: write tests (or run existing ones) that pin the *current* behavior — including the ugly parts.
2. **Small step**: one structural change — extract a function, rename, replace a magic number.
3. **Compile + tests green.** If red, undo the step (it was one step — that is the point).
4. Repeat until the mess is structure.

Never mix "refactor" and "add a feature" in the same step — the commit that does both is the commit you cannot trust.

## A mess, and its dissection

```cpp
// BEFORE: 60 lines in main — parse, validate, compute, print, all interleaved
int main() { /* read csv line, split, stoi everywhere, if-chains, cout... */ }
```

Extraction order that always works: **constants** → **pure functions** (parse, compute — no I/O) → **I/O boundary** (read/print) → data type (`struct Record`). Pure functions first: they are the tests' favorite food.

```cpp
// AFTER:
struct Record { std::string name; int qty{}; double price{}; };
std::optional<Record> parse_record(const std::string& line);
double record_total(const Record& r);
void print_report(const std::vector<Record>& rows);
```

Same behavior (your characterization tests still pass), new shape: every unit named, testable, and single-purpose.

## The compiler is your refactor partner

Renaming a function: change the declaration, compile, follow every error to its caller. C++'s strictness — the thing that made week one painful — is exactly what makes refactoring safe here: nothing breaks silently.
''',
    "Refactor một mớ bời bời (một cách an toàn)",
    "Vòng lặp refactor: ghim hành vi trước, bước nhỏ, biên dịch + chạy test sau mỗi bước — hành vi giữ nguyên, cấu trúc cải thiện.",
    '''
## Vòng lặp

1. **Ghim hành vi**: viết test (hoặc dùng test có sẵn) ghi lại hành vi *hiện tại* — kể cả những phần xấu xí.
2. **Bước nhỏ**: đúng một thay đổi cấu trúc — tách hàm, đổi tên, thay một con số ma thuật.
3. **Biên dịch + test xanh.** Nếu đỏ, hoàn tác bước đó (nó chỉ là một bước — đó chính là điểm hay).
4. Lặp lại cho đến khi mớ hỗn độn thành cấu trúc.

Đừng bao giờ trộn "refactor" và "thêm tính năng" trong cùng một bước — commit làm cả hai là commit bạn không thể tin tưởng.

## Một mớ bời bời, và cách mổ xẻ

```cpp
// TRƯỚC: 60 dòng trong main — phân tích, kiểm tra, tính toán, in, chen chúc nhau
int main() { /* đọc dòng csv, tách, stoi khắp nơi, if-chains, cout... */ }
```

Thứ tự tách luôn hiệu quả: **hằng số** → **hàm thuần** (parse, compute — không I/O) → **ranh giới I/O** (đọc/in) → kiểu dữ liệu (`struct Record`). Hàm thuần trước: chúng là món khoái khẩu của test.

```cpp
// SAU:
struct Record { std::string name; int qty{}; double price{}; };
std::optional<Record> parse_record(const std::string& line);
double record_total(const Record& r);
void print_report(const std::vector<Record>& rows);
```

Cùng hành vi (test ghim hành vi vẫn xanh), hình dạng mới: mọi đơn vị có tên, kiểm thử được, một mục đích.

## Compiler là bạn đồng hành refactor

Đổi tên hàm: sửa khai báo, biên dịch, đi theo từng lỗi tới người gọi. Sự nghiêm ngặt của C++ — thứ khiến tuần đầu đau khổ — chính là thứ làm refactor an toàn ở đây: không gì vỡ lặng lẽ.
''',
)

# ---- Module 16 checkpoint ----
write_checkpoint(
    M16, L16C,
    "Checkpoint: Architecture",
    "One graded challenge: decompose a tangle into exactly the named pipeline the tests call.",
    15,
    '''
**Checkpoint — architecture.** Pass the graded challenge below to finish the module.

You are handed a described monolith and must deliver its decomposed form: parse → validate → compute, each a named function.
''',
    "Checkpoint: Kiến trúc",
    "Một challenge có chấm: phân rã một mớ hỗn độn thành đúng chuỗi.pipeline có tên mà test gọi tới.",
    '''
**Checkpoint — kiến trúc.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Bạn nhận một mô tả "nguyên khối" và phải bàn giao dạng đã phân rã: parse → validate → compute, mỗi khâu một hàm có tên.
''',
    challenge(
        "cpp16-check-pipeline",
        "The Pipeline Refactor",
        "Implement the decomposed pipeline for expense lines \"name,amount\": `parse_amount(line)` (double; 0.0 on missing/invalid), `is_valid(line)` (name non-empty AND amount > 0), and `pipeline_total(lines)` (sum of valid amounts). Empty list → 0.0.",
        "#include <string>\\n#include <vector>\\n\\ndouble parse_amount(const std::string& line) {\\n    // TODO\\n}\\nbool is_valid(const std::string& line) {\\n    // TODO\\n}\\ndouble pipeline_total(const std::vector<std::string>& lines) {\\n    // TODO\\n}",
        [
            ("parse", "CHECK_NEAR(parse_amount(std::string{\"coffee,3.5\"}), 3.5, 0.001);", "Second field as double."),
            ("invalid amount", "CHECK(!is_valid(std::string{\"coffee,0\"}));", "Amount must be > 0."),
            ("invalid name", "CHECK(!is_valid(std::string{\",3.5\"}));", "Empty name is invalid even with a good amount."),
            ("total skips invalid", "CHECK_NEAR(pipeline_total({std::string{\"a,2\"}, std::string{\"b,0\"}, std::string{\"c,5\"}}), 7.0, 0.001);", "Only valid lines contribute."),
        ],
        level="real-world",
        difficulty="beginner",
    ),
    vi_challenge(
        "Chuỗi pipeline",
        "Cài chuỗi đã phân rã cho các dòng chi tiêu \"name,amount\": `parse_amount(line)` (double; 0.0 khi thiếu/sai), `is_valid(line)` (tên khác rỗng VÀ amount > 0), và `pipeline_total(lines)` (tổng các amount hợp lệ). Danh sách rỗng → 0.0.",
        [("parse", "Trường thứ hai dưới dạng double."), ("amount không hợp lệ", "Amount phải > 0."), ("tên không hợp lệ", "Tên rỗng là không hợp lệ dù amount tốt."), ("tổng bỏ dòng lỗi", "Chỉ các dòng hợp lệ được tính.")],
    ),
    solution="#include <string>\\n#include <vector>\\n#include <sstream>\\ndouble parse_amount(const std::string& line) {\\n    std::istringstream row{line};\\n    std::string name, amount_s;\\n    std::getline(row, name, ',');\\n    std::getline(row, amount_s);\\n    try { return std::stod(amount_s); } catch (...) { return 0.0; }\\n}\\nbool is_valid(const std::string& line) {\\n    std::istringstream row{line};\\n    std::string name, amount_s;\\n    std::getline(row, name, ',');\\n    std::getline(row, amount_s);\\n    try { return !name.empty() && std::stod(amount_s) > 0; } catch (...) { return false; }\\n}\\ndouble pipeline_total(const std::vector<std::string>& lines) {\\n    double t = 0.0;\\n    for (const auto& l : lines) if (is_valid(l)) t += parse_amount(l);\\n    return t;\\n}",
    wrong="#include <string>\\n#include <vector>\\n#include <sstream>\\ndouble parse_amount(const std::string& line) {\\n    std::istringstream row{line};\\n    std::string name, amount_s;\\n    std::getline(row, name, ',');\\n    std::getline(row, amount_s);\\n    try { return std::stod(amount_s); } catch (...) { return 0.0; }\\n}\\nbool is_valid(const std::string& line) {\\n    std::istringstream row{line};\\n    std::string name, amount_s;\\n    std::getline(row, name, ',');\\n    std::getline(row, amount_s);\\n    try { return std::stod(amount_s) > 0; } catch (...) { return false; }\\n}\\ndouble pipeline_total(const std::vector<std::string>& lines) {\\n    double t = 0.0;\\n    for (const auto& l : lines) if (is_valid(l)) t += parse_amount(l);\\n    return t;\\n}",
)

# ---- Module 16 practice ----
write_practice(
    M16, "m16-refactor-practice",
    "Refactor Practice: Structure Recovery",
    "Extract constants, split a compound predicate into named helpers, and const-correct a signature set.",
    "Luyện Refactor: Hồi phục cấu trúc",
    "Tách hằng số, tách một vị từ phức hợp thành các hàm có tên, và const-correct hóa một bộ chữ ký.",
    L16B, 20, "beginner",
    [
        challenge(
            "cpp16-named-predicates",
            "Named Predicates",
            "Refactor logic into named helpers: `is_adult(int age)` (>= 18), `has_id(const std::string& id)` (non-empty), and `can_enter(int age, const std::string& id)` using both.",
            "#include <string>\\n\\nbool is_adult(int age) {\\n    // TODO\\n}\\nbool has_id(const std::string& id) {\\n    // TODO\\n}\\nbool can_enter(int age, const std::string& id) {\\n    // TODO — use the two helpers\\n}",
            [("adult", "CHECK(is_adult(18)); CHECK(!is_adult(17));", "Boundary: 18 in, 17 out."), ("id", "CHECK(has_id(std::string{\"X1\"})); CHECK(!has_id(std::string{\"\"}));", "Non-empty is the whole rule."), ("combined", "CHECK(can_enter(20, std::string{\"X1\"})); CHECK(!can_enter(16, std::string{\"X1\"})); CHECK(!can_enter(20, std::string{\"\"}));", "Both must hold.")],
            level="independent",
        ),
    ],
    {"cpp16-named-predicates": vi_challenge("Vị từ có tên", "Refactor logic thành các helper có tên: `is_adult(int age)` (>= 18), `has_id(const std::string& id)` (khác rỗng), và `can_enter(int age, const std::string& id)` dùng cả hai.", [("người lớn", "Biên: 18 vào, 17 ra."), ("id", "Khác rỗng là toàn bộ luật."), ("kết hợp", "Cả hai phải đúng.")])},
    solutions=[
        ("cpp16-named-predicates", "#include <string>\\nbool is_adult(int age) { return age >= 18; }\\nbool has_id(const std::string& id) { return !id.empty(); }\\nbool can_enter(int age, const std::string& id) { return is_adult(age) && has_id(id); }", "#include <string>\\nbool is_adult(int age) { return age > 18; }\\nbool has_id(const std::string& id) { return !id.empty(); }\\nbool can_enter(int age, const std::string& id) { return is_adult(age) && has_id(id); }"),
    ],
)

# ============================ MODULE 17: git-professional-workflow ============================
M17 = "git-professional-workflow"

L17A = "repo-hygiene-for-cpp"
L17B = "checkpoint-repo"

write_module(
    M17,
    "Git & Professional C++ Workflow",
    "What a C++ repository must ignore, how a build directory changes your commits, and the README that lets strangers build.",
    "Git & Quy trình C++ chuyên nghiệp",
    "Một repository C++ phải ignore những gì, thư mục build thay đổi commit của bạn ra sao, và cái README cho người lạ build được.",
    [L17A, L17B],
    ["m17-repo-practice"],
)

write_lesson(
    M17, L17A,
    "Repository Hygiene for C++ Projects",
    "The .gitignore for compiled languages, what belongs in version control, and the README contract.",
    10,
    '''
## What never enters version control

```
# .gitignore for a C++/CMake project
build/
build-*/
cmake-build-*/
*.o
*.out
compile_commands.json
```

Everything the compiler generates is **regenerable** — committing it bloats history and produces impossible merges. The `build/` directory especially: it can contain thousands of machine-specific files. Anyone can recreate it with two CMake commands.

## What always belongs

- Sources (`src/`, headers), `CMakeLists.txt`
- Tests and their data
- README, LICENSE, CI configuration when it exists
- `.gitignore` itself

## The README contract

A stranger must be able to build in under two minutes:

```markdown
# Finance CLI

Personal finance manager (C++20, CMake).

## Build
cmake -B build && cmake --build build

## Run
./build/finance

## Test
ctest --test-dir build
```

If your build needs a special flag, the README is where it lives — not tribal knowledge.

## The workflow

Small commits with imperative messages ("parse csv records"), one logical change each; branches for features; PR-style review even solo — reading your own diff before merging catches a surprising fraction of bugs. Git itself is taught hands-on in the platform's web track; here you learn what is *C++-specific*: ignore build output, commit the CMakeLists, ship the README.
''',
    "Vệ sinh repository cho dự án C++",
    "Tệp .gitignore cho ngôn ngữ biên dịch, cái gì thuộc về version control, và bản hợp đồng README.",
    '''
## Những gì không bao giờ vào version control

```
# .gitignore cho dự án C++/CMake
build/
build-*/
cmake-build-*/
*.o
*.out
compile_commands.json
```

Mọi thứ compiler sinh ra đều **tái tạo được** — commit chúng làm phình lịch sử và sinh ra những cuộc merge bất khả. Đặc biệt là thư mục `build/`: nó có thể chứa hàng nghìn file phụ thuộc máy. Ai cũng tái tạo được nó bằng hai lệnh CMake.

## Những gì luôn thuộc về

- Mã nguồn (`src/`, header), `CMakeLists.txt`
- Test và dữ liệu của test
- README, LICENSE, cấu hình CI nếu có
- Chính `.gitignore`

## Bản hợp đồng README

Một người lạ phải build được trong vòng hai phút:

```markdown
# Finance CLI

Trình quản lý tài chính cá nhân (C++20, CMake).

## Build
cmake -B build && cmake --build build

## Run
./build/finance

## Test
ctest --test-dir build
```

Nếu build của bạn cần một cờ đặc biệt, README là nơi nó sống — không phải tri thức bộ lạc.

## Quy trình

Commit nhỏ với thông báo dạng mệnh lệnh ("parse csv records"), mỗi commit một thay đổi logic; branch cho tính năng; review kiểu PR dù làm một mình — tự đọc diff của chính mình trước khi merge bắt được một tỷ lệ bug đáng ngạc nhiên. Git được dạy thực hành trong track web của nền tảng; ở đây bạn học cái *đặc thù C++*: ignore output build, commit CMakeLists, bàn giao README.
''',
)

# ---- Module 17 checkpoint ----
write_checkpoint(
    M17, L17B,
    "Checkpoint: Repository",
    "One graded challenge: decide what a C++ repo commits and what it ignores.",
    10,
    '''
**Checkpoint — repository.** A quick graded decision exercise: classify artifacts as "commit" or "ignore".
''',
    "Checkpoint: Repository",
    "Một bài tập quyết định có chấm nhanh: phân loại những gì repo C++ commit và những gì bỏ qua.",
    '''
**Checkpoint — repository.** Một bài phân loại có chấm nhanh: phân loại các artifact thành "commit" hay "ignore".
''',
    challenge(
        "cpp17-check-repo",
        "Commit or Ignore",
        "Implement `should_commit(path)` returning true for files a professional C++ repo commits: `src/main.cpp`, `include/app.hpp`, `CMakeLists.txt`, `README.md`, `.gitignore` → true; `build/CMakeCache.txt`, `main.o`, `finance` (binary), `cmake-build-debug/x` → false (generated artifacts).",
        "#include <string>\\n\\nbool should_commit(const std::string& path) {\\n    // TODO\\n}",
        [
            ("sources", "CHECK(should_commit(std::string{\"src/main.cpp\"}));", "Sources and headers are committed."),
            ("build ignored", "CHECK(!should_commit(std::string{\"build/CMakeCache.txt\"}));", "The build directory is regenerable."),
            ("objects ignored", "CHECK(!should_commit(std::string{\"main.o\"}));", "Object files never enter version control."),
            ("binary ignored", "CHECK(!should_commit(std::string{\"finance\"}));", "Compiled binaries are artifacts, not sources."),
        ],
        level="real-world",
        difficulty="beginner",
    ),
    vi_challenge(
        "Commit hay Ignore",
        "Cài `should_commit(path)` trả về true với những file mà một repo C++ chuyên nghiệp sẽ commit: `src/main.cpp`, `include/app.hpp`, `CMakeLists.txt`, `README.md`, `.gitignore` → true; `build/CMakeCache.txt`, `main.o`, `finance` (file nhị phân), `cmake-build-debug/x` → false (artifact được sinh ra).",
        [("mã nguồn", "Nguồn và header được commit."), ("bỏ qua build", "Thư mục build tái tạo được."), ("bỏ qua file object", "File object không bao giờ vào version control."), ("bỏ qua file nhị phân", "File nhị phân là artifact, không phải nguồn.")],
    ),
    solution="#include <string>\\nbool should_commit(const std::string& path) {\\n    auto starts = [&](const char* p) { return path.rfind(p, 0) == 0; };\\n    if (starts(\"build/\") || starts(\"cmake-build-\")) return false;\\n    if (path.size() > 2 && path.substr(path.size() - 2) == \".o\") return false;\\n    if (path == \"finance\") return false;\\n    return true;\\n}",
    wrong="#include <string>\\nbool should_commit(const std::string& path) {\\n    auto starts = [&](const char* p) { return path.rfind(p, 0) == 0; };\\n    if (starts(\"build/\") || starts(\"cmake-build-\")) return false;\\n    return true;\\n}",
)

# ---- Module 17 practice ----
write_practice(
    M17, "m17-repo-practice",
    "Repository Practice: The README Contract",
    "Draft build instructions that a stranger can follow, and classify common repo mistakes.",
    "Luyện Repository: Bản hợp đồng README",
    "Viết hướng dẫn build mà người lạ làm theo được, và phân loại các lỗi repo thường gặp.",
    L17A, 15, "beginner",
    [
        challenge(
            "cpp17-build-flags",
            "Build Command Knowledge",
            "Implement `build_command(build_type)` returning the CMake configure command string: Debug → \"cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug\", Release → \"cmake -B build-release -DCMAKE_BUILD_TYPE=Release\".",
            "#include <string>\\n\\nstd::string build_command(const std::string& build_type) {\\n    // TODO\\n}",
            [("debug", "CHECK(build_command(std::string{\"Debug\"}) == std::string{\"cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug\"});", "Debug build directory and flag."), ("release", "CHECK(build_command(std::string{\"Release\"}) == std::string{\"cmake -B build-release -DCMAKE_BUILD_TYPE=Release\"});", "Release build directory and flag.")],
            level="imitation",
        ),
    ],
    {"cpp17-build-flags": vi_challenge("Kiến thức lệnh build", "Cài `build_command(build_type)` trả về chuỗi lệnh configure của CMake: Debug → \"cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug\", Release → \"cmake -B build-release -DCMAKE_BUILD_TYPE=Release\".", [("debug", "Thư mục build và cờ cho Debug."), ("release", "Thư mục build và cờ cho Release.")])},
    solutions=[
        ("cpp17-build-flags", "#include <string>\\nstd::string build_command(const std::string& build_type) {\\n    if (build_type == \"Debug\") return \"cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug\";\\n    return \"cmake -B build-release -DCMAKE_BUILD_TYPE=Release\";\\n}", "#include <string>\\nstd::string build_command(const std::string& build_type) {\\n    if (build_type == \"Debug\") return \"cmake -B build -DCMAKE_BUILD_TYPE=Debug\";\\n    return \"cmake -B build -DCMAKE_BUILD_TYPE=Release\";\\n}"),
    ],
)

# ============================ MODULE 18: problem-solving ============================
M18 = "problem-solving"

L18A = "decomposition-and-edge-cases"
L18B = "choosing-structures"
L18C = "checkpoint-problems"

write_module(
    M18,
    "Programming Problem Solving",
    "From problem statement to working program: decomposition, edge cases first, complexity intuition, and choosing the structure that fits.",
    "Giải quyết vấn đề bằng lập trình",
    "Từ đề bài đến chương trình chạy được: phân rã, edge case trước, trực giác về độ phức tạp, và chọn cấu trúc dữ liệu phù hợp.",
    [L18A, L18B, L18C],
    ["m18-problem-practice"],
)

write_lesson(
    M18, L18A,
    "Decomposition and the Edge-Case Habit",
    "The five-step method, writing edge cases BEFORE the solution, and the discipline that turns hard problems into easy ones.",
    11,
    '''
## The five-step method

1. **Restate** the problem in your own words, one sentence. If you cannot, you are not ready to code.
2. **Work an example by hand** — input, steps, output. The by-hand trace IS the algorithm sketch.
3. **Find the edges first**: empty input, one element, duplicates, extremes, zero/negative. Write them as test cases *before* coding.
4. **Decompose**: name the stages (parse → compute → format) — each becomes a function.
5. **Implement the happy path, then the edges.** Compile often.

## Why edges first

Edge cases discovered after coding force redesign; discovered before coding, they only constrain it. "What if the list is empty?" changes your function's *shape* (early return? sentinel?) — asking late costs a rewrite, asking early costs a minute.

## Worked micro-example

"Return the second-largest value in a vector."

- Restate: largest, then the largest among the rest.
- By hand: {4, 9, 2, 9} → remove one 9 → second largest is 9 again (duplicates count!). {5} → none.
- Edges: empty → throw or 0? Decide and document. One element → none. Duplicates of the max → still valid second-largest.
- Decompose: `int second_largest(const std::vector<int>&)` — one pass tracking two values.

The exercise set practices exactly this loop on progressively harder problems.
''',
    "Phân rã và thói quen edge-case",
    "Phương pháp năm bước, viết edge case TRƯỚC khi giải, và kỷ luật biến bài khó thành bài dễ.",
    '''
## Phương pháp năm bước

1. **Diễn đạt lại** đề bài bằng lời của bạn, một câu. Nếu không được, bạn chưa sẵn sàng code.
2. **Làm một ví dụ bằng tay** — input, các bước, output. Chính vết tay-trắng đó là bản phác thuật toán.
3. **Tìm edge trước**: input rỗng, một phần tử, trùng lặp, giá trị cực đoan, không/âm. Viết chúng thành test case *trước khi* code.
4. **Phân rã**: đặt tên các chặng (parse → compute → format) — mỗi chặng thành một hàm.
5. **Cài luồng chính, rồi tới edge.** Biên dịch thường xuyên.

## Vì sao edge trước

Edge case phát hiện sau khi code buộc bạn thiết kế lại; phát hiện trước khi code, chúng chỉ ràng buộc thiết kế. "Nếu danh sách rỗng thì sao?" thay đổi *hình dạng* hàm của bạn (return sớm? giá trị linh thiêng?) — hỏi muộn tốn một lần viết lại, hỏi sớm tốn một phút.

## Ví dụ nhỏ đã giải

"Trả về giá trị lớn thứ hai trong một vector."

- Diễn đạt: lớn nhất, rồi lớn nhất trong phần còn lại.
- Bằng tay: {4, 9, 2, 9} → bỏ một số 9 → lớn thứ hai vẫn là 9 (trùng lặp vẫn tính!). {5} → không có.
- Edge: rỗng → ném hay trả 0? Quyết định và ghi lại. Một phần tử → không có. Trùng số lớn nhất → vẫn là lớn thứ hai hợp lệ.
- Phân rã: `int second_largest(const std::vector<int>&)` — một lượt duyệt theo dõi hai giá trị.

Bộ bài tập luyện đúng vòng lặp này trên những bài toán khó dần.
''',
)

write_lesson(
    M18, L18B,
    "Choosing Structures and Cost Intuition",
    "Match the question to the container; count your loops; when two structures beat one wrong one.",
    10,
    '''
## The question decides the container

| The question sounds like... | Reach for |
| --- | --- |
| "in order, one at a time" | `vector` |
| "given a key, find the thing" | `map` / `unordered_map` |
| "have I seen this before?" | `set` |
| "the top/last/first few" | `vector` (+ sort or scan) |

Choosing wrong makes every later step clumsy: searching an unsorted vector repeatedly is O(n) per query; a `set` answers in O(log n); an `unordered_set` in ~O(1). One structure choice can beat any amount of micro-optimization.

## Counting your loops (complexity intuition)

- One pass over n items → O(n): fine to a million.
- Nested over n×n → O(n²): fine to ~10,000; painful at 100,000.
- Halving each step (binary search) → O(log n): a billion items in ~30 steps.

You will not derive these in Beginner; you will *count loop nests* and multiply. The next exercise makes the difference measurable: same task, two structures, and the harness times nothing — but the *number of operations* is the answer.

## Two structures beat one wrong one

"Count occurrences, then list the top word" is a `map<string,int>` *plus* a scan for the max — not one heroic vector scanned repeatedly. Composing the right containers is beginner-level architectural thinking, and it is exactly what the capstone's search feature will do.
''',
    "Chọn cấu trúc và trực giác về chi phí",
    "Ghép câu hỏi với container; đếm vòng lặp của bạn; khi nào hai cấu trúc đúng hơn một cấu trúc sai.",
    '''
## Câu hỏi quyết định container

| Câu hỏi nghe như... | Với tới |
| --- | --- |
| "theo thứ tự, từng cái một" | `vector` |
| "cho một khóa, tìm thứ kia" | `map` / `unordered_map` |
| "đã gặp cái này chưa?" | `set` |
| "mấy cái đầu/cuối/trước tiên" | `vector` (+ sort hoặc quét) |

Chọn sai khiến mọi bước về sau vụng về: tìm kiếm lặp lại trên vector chưa sắp là O(n) mỗi truy vấn; một `set` trả lời trong O(log n); một `unordered_set` ~O(1). Một lựa chọn cấu trúc có thể thắng mọi tối ưu vi mô cộng lại.

## Đếm vòng lặp của bạn (trực giác độ phức tạp)

- Một lượt qua n phần tử → O(n): ổn với cả triệu.
- Lồng nhau n×n → O(n²): ổn tới ~10.000; đau đớn ở 100.000.
- Chia đôi mỗi bước (tìm kiếm nhị phân) → O(log n): một tỷ phần tử trong ~30 bước.

Ở trình độ Cơ bản bạn sẽ không suy diễn các con số này; bạn sẽ *đếm số tầng vòng lặp* và nhân lên. Bài tập kế tiếp làm cho khác biệt thành đo đếm được: cùng một việc, hai cấu trúc — harness không bấm giờ gì cả, nhưng *số phép tính* chính là câu trả lời.

## Hai cấu trúc đúng hơn một cấu trúc sai

"Đếm số lần xuất hiện, rồi liệt kê từ phổ biến nhất" là một `map<string,int>` *cộng với* một lượt quét tìm max — không phải một vector hùng dũng bị quét đi quét lại. Ghép đúng các container là tư duy kiến trúc ở mức người mới, và chính xác điều đó sẽ là tính năng tìm kiếm của capstone.
''',
)

# ---- Module 18 checkpoint ----
write_checkpoint(
    M18, L18C,
    "Checkpoint: Problem Solving",
    "One graded challenge: a classic problem solved with the method — edges handled, right structure chosen.",
    15,
    '''
**Checkpoint — problem solving.** Pass the graded challenge below to finish the module.

An anagram-grouping task: it rewards the edge-first habit and the map-of-vectors structure.
''',
    "Checkpoint: Giải quyết vấn đề",
    "Một challenge có chấm: một bài kinh điển giải bằng đúng phương pháp — edge được xử lý, cấu trúc đúng được chọn.",
    '''
**Checkpoint — giải vấn đề.** Vượt qua challenge có chấm bên dưới để hoàn thành module.

Một bài gộp anagram: nó thưởng cho thói quen edge-trước và cấu trúc map-của-các-vector.
''',
    challenge(
        "cpp18-check-anagram-key",
        "Anagram Signature",
        "Implement `signature(word)`: a lowercase sorted-letters key for a word (\"Listen\" and \"Silent\" share the key \"eilnst\"), and `same_letters(a, b)` comparing two words by signature.",
        "#include <string>\\n\\nstd::string signature(const std::string& word) {\\n    // TODO: lowercase, sort the letters\\n}\\nbool same_letters(const std::string& a, const std::string& b) {\\n    // TODO\\n}",
        [
            ("anagram pair", "CHECK(same_letters(std::string{\"Listen\"}, std::string{\"Silent\"}));", "Case-insensitive anagram pair."),
            ("not anagram", "CHECK(!same_letters(std::string{\"hello\"}, std::string{\"world\"}));", "Different letters differ."),
            ("signature sorted", "CHECK(signature(std::string{\"Cab\"}) == std::string{\"abc\"});", "Lowercased then sorted."),
            ("empty", "CHECK(same_letters(std::string{\"\"}, std::string{\"\"}));", "Two empty strings share a signature (edge case decided)."),
        ],
        level="combination",
        difficulty="beginner",
    ),
    vi_challenge(
        "Chữ ký anagram",
        "Cài `signature(word)`: một khóa gồm các chữ cái đã hạ chữ thường và sắp xếp (\"Listen\" và \"Silent\" chung khóa \"eilnst\"), và `same_letters(a, b)` so hai từ qua chữ ký.",
        [("cặp anagram", "Cặp anagram không phân biệt hoa/thường."), ("không phải anagram", "Chữ khác nhau thì chữ ký khác nhau."), ("chữ ký sắp xếp", "Hạ chữ thường rồi sắp xếp."), ("rỗng", "Hai chuỗi rỗng chung chữ ký (edge case đã quyết định).")],
    ),
    solution="#include <string>\\n#include <algorithm>\\nstd::string signature(const std::string& word) {\\n    std::string s = word;\\n    for (char& c : s) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));\\n    std::sort(s.begin(), s.end());\\n    return s;\\n}\\nbool same_letters(const std::string& a, const std::string& b) {\\n    return signature(a) == signature(b);\\n}",
    wrong="#include <string>\\n#include <algorithm>\\nstd::string signature(const std::string& word) {\\n    std::string s = word;\\n    for (char& c : s) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));\\n    return s;\\n}\\nbool same_letters(const std::string& a, const std::string& b) {\\n    return signature(a) == signature(b);\\n}",
)

# ---- Module 18 practice ----
write_practice(
    M18, "m18-problem-practice",
    "Problem Practice: The Method Applied",
    "Two-sum with a map, a balanced-braces stack, and a run-length encoder.",
    "Luyện Vấn đề: Phương pháp vào việc",
    "Two-sum với map, bài dấu ngoặc cân bằng dùng stack, và một bộ mã hóa run-length.",
    L18A, 25, "beginner",
    [
        challenge(
            "cpp18-balanced",
            "Balanced Braces",
            "Implement `is_balanced(text)` for `()` only: every open has a matching close in order. Use a counter (a stack of ints that only ever holds one value).",
            "#include <string>\\n\\nbool is_balanced(const std::string& text) {\\n    // TODO\\n}",
            [("balanced", "CHECK(is_balanced(std::string{\"(a(b)c)\"}));", "Every open closed in order."), ("unbalanced close", "CHECK(!is_balanced(std::string{\")(\"}));", "Close before open fails."), ("unbalanced open", "CHECK(!is_balanced(std::string{\"((\"}));", "Leftover opens fail at the end."), ("empty", "CHECK(is_balanced(std::string{\"\"}));", "Empty is balanced (edge decided).")],
            level="independent",
        ),
    ],
    {"cpp18-balanced": vi_challenge("Dấu ngoặc cân bằng", "Cài `is_balanced(text)` cho cặp `()` thôi: mỗi dấu mở có một dấu đóng khớp theo thứ tự. Dùng một bộ đếm (một stack số nguyên mà chỉ bao giờ giữ một giá trị).", [("cân bằng", "Mỗi dấu mở được đóng đúng thứ tự."), ("đóng trước mở", "Đóng trước mở là hỏng."), ("thừa dấu mở", "Dấu mở còn sót làm hỏng ở cuối."), ("rỗng", "Rỗng là cân bằng (edge đã quyết định).")])},
    solutions=[
        ("cpp18-balanced", "#include <string>\\nbool is_balanced(const std::string& text) {\\n    int depth = 0;\\n    for (char c : text) {\\n        if (c == '(') ++depth;\\n        else if (c == ')') {\\n            --depth;\\n            if (depth < 0) return false;\\n        }\\n    }\\n    return depth == 0;\\n}", "#include <string>\\nbool is_balanced(const std::string& text) {\\n    int depth = 0;\\n    for (char c : text) {\\n        if (c == '(') ++depth;\\n        else if (c == ')') --depth;\\n    }\\n    return depth == 0;\\n}"),
    ],
)

# ============================ MODULE 19: capstone ============================
M19 = "capstone-finance-cli"

L19A = "capstone-brief"
L19B = "capstone-ship"

write_module(
    M19,
    "Capstone: Personal Finance Manager",
    "Everything from 18 modules in one artifact: a tested, validated, multi-file-shaped finance CLI. Requirements and acceptance tests — no solution provided.",
    "Capstone: Trình quản lý tài chính cá nhân",
    "Mọi thứ từ 18 module trong một sản phẩm duy nhất: một finance CLI có kiểm thử, có validation, kiến trúc nhiều file. Yêu cầu và test nghiệm thu — không có lời giải.",
    [L19A, L19B],
    ["m19-capstone-practice"],
)

write_lesson(
    M19, L19A,
    "Capstone Brief: Requirements",
    "The specification you build against: features, constraints, acceptance criteria, and milestones.",
    12,
    '''
## The product

A **Personal Finance Manager** — record transactions, categorize them, and answer real questions: what did I spend, on what, and what remains?

## Features (graded subset marked ★)

1. ★ **Record** a transaction: name, category, amount (positive = income, negative = expense).
2. ★ **Validate** at the boundary: empty name rejected, zero amount rejected.
3. ★ **Balance**: sum of all amounts.
4. ★ **By category**: per-category totals (`map<string,double>`).
5. **Filter**: transactions above/below a threshold.
6. **Persistence**: save/load CSV lines (`name,category,amount`) — module 6's parser in production.
7. **Report**: sorted summary printed via `void program()`.

## Architecture constraints

- A `Transaction` **struct**; an `enum class Kind { Income, Expense }` derived from the sign.
- A **class** `Ledger` owning a `std::vector<Transaction>` — its methods enforce validation (module 10's invariant discipline).
- Parsing/formatting as **free functions** (module 16's pipeline), not glued into `Ledger`.
- No `new`/`delete` anywhere (module 12), no C-strings, no `using namespace std;` in headers.

## Milestones

M1: struct + Ledger with record/balance. M2: category totals + filter. M3: CSV save/load round-trip. M4: report via `program()`. Ship each milestone working — the graded checks map to M1–M3 exactly.

## Acceptance (the tests' point of view)

The graded challenges call your names directly: `add_record`, `balance`, `category_totals`, plus a `program()` report check. Edge cases are graded: the empty ledger, the rejected record, the single-category month. Design for them from line one.
''',
    "Đặc tả Capstone: Yêu cầu",
    "Đặc tả bạn xây dựng theo: tính năng, ràng buộc, tiêu chí nghiệm thu, và các cột mốc.",
    '''
## Sản phẩm

Một **Trình quản lý tài chính cá nhân** — ghi lại giao dịch, phân loại, và trả lời các câu hỏi thật: tôi đã tiêu gì, vào việc gì, và còn lại bao nhiêu?

## Tính năng (phần có chấm đánh dấu ★)

1. ★ **Ghi** một giao dịch: tên, danh mục, số tiền (dương = thu nhập, âm = chi tiêu).
2. ★ **Validate** tại ranh giới: tên rỗng bị từ chối, số tiền 0 bị từ chối.
3. ★ **Số dư**: tổng của mọi số tiền.
4. ★ **Theo danh mục**: tổng từng danh mục (`map<string,double>`).
5. **Lọc**: các giao dịch trên/dưới một ngưỡng.
6. **Lưu trữ**: lưu/đọc dòng CSV (`name,category,amount`) — bộ phân tích của module 6 vào sản phẩm thật.
7. **Báo cáo**: tóm tắt đã sắp xếp in qua `void program()`.

## Ràng buộc kiến trúc

- Một **struct** `Transaction`; một `enum class Kind { Income, Expense }` suy ra từ dấu.
- Một **class** `Ledger` sở hữu `std::vector<Transaction>` — các hàm của nó thực thi validation (kỷ luật bất biến của module 10).
- Phân tích/định dạng là các **hàm tự do** (chuỗi.pipeline của module 16), không dán vào `Ledger`.
- Không có `new`/`delete` ở bất kỳ đâu (module 12), không C-string, không `using namespace std;` trong header.

## Các cột mốc

M1: struct + Ledger với record/balance. M2: tổng theo danh mục + lọc. M3: vòng tròn trọn CSV lưu/đọc. M4: báo cáo qua `program()`. Bàn giao từng cột mốc chạy được — các bước kiểm tra có chấm ánh xạ đúng tới M1–M3.

## Nghiệm thu (góc nhìn của test)

Các challenge có chấm gọi thẳng tên bạn: `add_record`, `balance`, `category_totals`, cộng một kiểm tra báo cáo `program()`. Edge case được chấm: sổ cái rỗng, bản ghi bị từ chối, tháng chỉ có một danh mục. Hãy thiết kế cho chúng ngay từ dòng đầu tiên.
''',
)

write_lesson(
    M19, L19B,
    "Capstone Ship: Milestones and Verification",
    "How the graded checks map to milestones, and how to verify each one yourself before submitting.",
    10,
    '''
## Milestone → graded check

| Milestone | Graded challenge | Proves |
| --- | --- | --- |
| M1 records + balance | `capstone core` | struct, class invariant, sum |
| M2 categories + rejection | `capstone categories` | map aggregation, boundary validation |
| M3 report via program() | `capstone report` | pipeline formatting, capture-based grading |

## Verify each milestone yourself

For every milestone, before submitting: write a `program()` (or temporary main) that exercises the feature and print what you expect. Compare. This is the characterization habit from module 16 applied to your own project — and it is exactly how the platform's tests will see your code.

## The honest rules of this capstone

- **No solution is provided** — the lessons of modules 1–18 are your toolkit; the brief is your contract.
- Edge cases are graded equally with happy paths: empty ledger, rejected record, one-category month.
- Architecture constraints are part of the grade: a Ledger class that validates, free functions for parsing, no raw owning pointers.
- AI assistants: allowed for *explaining* compiler errors and suggesting test cases (module 14's rules); not allowed to write your Ledger. The graded checks read your structure, not just your output.

## After shipping

You will have used every beginner tool under a real requirement: types, classes, containers, algorithms, streams, RAII, and a test-driven loop. C++ Intermediate picks up exactly where this artifact ends: templates and generic design, deeper exception guarantees, build systems beyond one target, and concurrency. The path continues; the fundamentals are yours.
''',
    "Bàn giao Capstone: Cột mốc và kiểm chứng",
    "Các bước có chấm ánh xạ tới cột mốc thế nào, và cách tự kiểm chứng từng cái trước khi nộp.",
    '''
## Cột mốc → bước có chấm

| Cột mốc | Challenge có chấm | Chứng minh |
| --- | --- | --- |
| M1 ghi giao dịch + số dư | `capstone core` | struct, bất biến lớp, phép tổng |
| M2 danh mục + từ chối | `capstone categories` | tổng hợp bằng map, validation ranh giới |
| M3 báo cáo qua program() | `capstone report` | định dạng theo pipeline, chấm kiểu capture |

## Tự kiểm chứng từng cột mốc

Với mọi cột mốc, trước khi nộp: viết một `program()` (hoặc main tạm) thực thi tính năng và in ra điều bạn kỳ vọng. So sánh. Đây là thói quen ghi-hành-vi của module 16 áp dụng cho dự án của chính bạn — và cũng chính là cách test của nền tảng sẽ nhìn code của bạn.

## Các luật trung thực của capstone này

- **Không có lời giải** — các bài học của module 1–18 là hộp công cụ của bạn; đặc tả là bản hợp đồng.
- Edge case được chấm ngang với luồng chính: sổ cái rỗng, bản ghi bị từ chối, tháng một-danh-mục.
- Ràng buộc kiến trúc là một phần điểm: một lớp Ledger có validate, hàm tự do cho parsing, không con trỏ sở hữu thô.
- Trợ lý AI: được phép để *giải thích* lỗi compiler và gợi ý test case (luật của module 14); không được phép viết Ledger thay bạn. Các bước có chấm đọc cấu trúc của bạn, không chỉ output.

## Sau khi bàn giao

Bạn đã dùng mọi công cụ của trình độ Cơ bản dưới một yêu cầu thật: kiểu, class, container, thuật toán, stream, RAII, và một vòng lặp test-driven. C++ Trung cấp nhặt đúng chỗ sản phẩm này dừng lại: template và thiết kế generic, bảo đảm exception sâu hơn, build hệ thống vượt một target, và concurrency. Con đường còn tiếp; nền tảng đã là của bạn.
''',
)

# ---- Capstone graded challenges (lesson-attached) ----
write_checkpoint(
    M19, "checkpoint-capstone-core",
    "Capstone Check: Core",
    "Milestone 1+2 graded: records, balance, categories, rejection at the boundary.",
    30,
    '''
**Capstone check — core.** Implement the Ledger core per the brief. This is the first of three graded capstone checks.
''',
    "Capstone: Phần lõi",
    "Cột mốc 1+2 có chấm: ghi giao dịch, số dư, danh mục, từ chối tại ranh giới.",
    '''
**Kiểm tra Capstone — lõi.** Cài phần lõi Ledger theo đặc tả. Đây là kiểm tra có chấm đầu tiên trong ba bước capstone.
''',
    challenge(
        "cpp19-capstone-core",
        "Finance Ledger Core",
        "Implement `struct Transaction` (name, category, amount) and class `Ledger` with: `bool add(name, category, amount)` (rejects empty name, empty category, and amount == 0; stores and returns true), `double balance() const` (sum of amounts), and `std::map<std::string,double> category_totals() const`.",
        "#include <map>\\n#include <string>\\n#include <vector>\\n\\n// TODO: Transaction struct + Ledger class",
        [
            ("add and balance", "Ledger l; CHECK(l.add(std::string{\"salary\"}, std::string{\"work\"}, 500.0)); CHECK(l.add(std::string{\"food\"}, std::string{\"life\"}, -120.0)); CHECK_NEAR(l.balance(), 380.0, 0.001);", "Records accumulate; balance is the signed sum."),
            ("rejections", "Ledger l; CHECK(!l.add(std::string{\"\"}, std::string{\"work\"}, 5.0)); CHECK(!l.add(std::string{\"x\"}, std::string{\"\"}, 5.0)); CHECK(!l.add(std::string{\"x\"}, std::string{\"life\"}, 0.0)); CHECK_NEAR(l.balance(), 0.0, 0.001);", "Invalid records never enter the ledger."),
            ("categories", "Ledger l; l.add(std::string{\"a\"}, std::string{\"life\"}, 10.0); l.add(std::string{\"b\"}, std::string{\"life\"}, 5.0); l.add(std::string{\"c\"}, std::string{\"work\"}, 100.0); auto t = l.category_totals(); CHECK_NEAR(t.at(std::string{\"life\"}), 15.0, 0.001); CHECK_NEAR(t.at(std::string{\"work\"}), 100.0, 0.001);", "Per-category aggregation via map."),
            ("empty ledger", "Ledger l; CHECK_NEAR(l.balance(), 0.0, 0.001); CHECK(l.category_totals().empty());", "Edge: nothing recorded yet — 0 and empty map."),
        ],
        level="real-world",
        difficulty="intermediate",
    ),
    vi_challenge(
        "Lõi sổ cái tài chính",
        "Cài `struct Transaction` (name, category, amount) và lớp `Ledger` với: `bool add(name, category, amount)` (từ chối tên rỗng, danh mục rỗng, và amount == 0; lưu và trả true), `double balance() const` (tổng các amount), và `std::map<std::string,double> category_totals() const`.",
        [("ghi và số dư", "Các bản ghi tích lũy; số dư là tổng có dấu."), ("từ chối", "Bản ghi không hợp lệ không bao giờ vào sổ."), ("danh mục", "Tổng hợp theo danh mục qua map."), ("sổ rỗng", "Edge: chưa ghi gì — 0 và map rỗng.")],
    ),
    solution="#include <map>\\n#include <string>\\n#include <vector>\\nstruct Transaction {\\n    std::string name;\\n    std::string category;\\n    double amount{};\\n};\\nclass Ledger {\\npublic:\\n    bool add(const std::string& name, const std::string& category, double amount) {\\n        if (name.empty() || category.empty() || amount == 0.0) return false;\\n        rows_.push_back(Transaction{name, category, amount});\\n        return true;\\n    }\\n    double balance() const {\\n        double t = 0.0;\\n        for (const auto& r : rows_) t += r.amount;\\n        return t;\\n    }\\n    std::map<std::string, double> category_totals() const {\\n        std::map<std::string, double> out;\\n        for (const auto& r : rows_) out[r.category] += r.amount;\\n        return out;\\n    }\\nprivate:\\n    std::vector<Transaction> rows_;\\n}",
    wrong="#include <map>\\n#include <string>\\n#include <vector>\\nstruct Transaction {\\n    std::string name;\\n    std::string category;\\n    double amount{};\\n};\\nclass Ledger {\\npublic:\\n    bool add(const std::string& name, const std::string& category, double amount) {\\n        if (name.empty() || amount == 0.0) return false;\\n        rows_.push_back(Transaction{name, category, amount});\\n        return true;\\n    }\\n    double balance() const {\\n        double t = 0.0;\\n        for (const auto& r : rows_) t += r.amount;\\n        return t;\\n    }\\n    std::map<std::string, double> category_totals() const {\\n        std::map<std::string, double> out;\\n        for (const auto& r : rows_) out[r.category] += r.amount;\\n        return out;\\n    }\\nprivate:\\n    std::vector<Transaction> rows_;\\n}",
)

# ---- Module 19 practice ----
write_practice(
    M19, "m19-capstone-practice",
    "Capstone Practice: Milestone 3 Warm-up",
    "CSV round-trip and a threshold filter — the two ungraded pieces of the capstone, rehearsed.",
    "Luyện Capstone: Khởi động cột mốc 3",
    "Vòng tròn CSV và bộ lọc ngưỡng — hai mảnh chưa có chấm của capstone, được diễn trước.",
    L19A, 25, "intermediate",
    [
        challenge(
            "cpp19-csv-roundtrip",
            "CSV Round-Trip",
            "Implement `to_csv(name, category, amount)` producing \"name,category,amount\" (amount with one decimal), and `from_csv(line)` returning the amount (0.0 on any malformed line — no name, no category, unparseable amount).",
            "#include <string>\\n\\nstd::string to_csv(const std::string& name, const std::string& category, double amount) {\\n    // TODO\\n}\\ndouble from_csv(const std::string& line) {\\n    // TODO\\n}",
            [("to csv", "CHECK(to_csv(std::string{\"salary\"}, std::string{\"work\"}, 500.0) == std::string{\"salary,work,500.0\"});", "Three comma-separated fields, one decimal."), ("from csv", "CHECK_NEAR(from_csv(std::string{\"food,life,-120.5\"}), -120.5, 0.001);", "Third field parsed as double."), ("malformed", "CHECK_NEAR(from_csv(std::string{\"nocommas\"}), 0.0, 0.001);", "Malformed lines yield 0.0 — never crash."), ("roundtrip", "CHECK_NEAR(from_csv(to_csv(std::string{\"x\"}, std::string{\"c\"}, 3.5)), 3.5, 0.001);", "Write then read returns the amount.")],
            level="real-world",
        ),
    ],
    {"cpp19-csv-roundtrip": vi_challenge("Vòng tròn CSV", "Cài `to_csv(name, category, amount)` tạo \"name,category,amount\" (amount với một chữ số thập phân), và `from_csv(line)` trả về amount (0.0 với dòng sai định dạng — không tên, không danh mục, amount không phân tích được).", [("to csv", "Ba trường ngăn cách bởi dấu phẩy, một chữ số thập phân."), ("from csv", "Trường thứ ba được phân tích thành double."), ("sai định dạng", "Dòng sai định dạng cho 0.0 — không bao giờ crash."), ("vòng tròn", "Ghi rồi đọc trả lại đúng amount.")])},
    solutions=[
        ("cpp19-csv-roundtrip", "#include <string>\\n#include <sstream>\\n#include <iomanip>\\nstd::string to_csv(const std::string& name, const std::string& category, double amount) {\\n    std::ostringstream out;\\n    out << name << ',' << category << ',' << std::fixed << std::setprecision(1) << amount;\\n    return out.str();\\n}\\ndouble from_csv(const std::string& line) {\\n    std::istringstream row{line};\\n    std::string name, category, amount_s;\\n    if (!std::getline(row, name, ',')) return 0.0;\\n    if (!std::getline(row, category, ',')) return 0.0;\\n    if (!std::getline(row, amount_s)) return 0.0;\\n    try { return std::stod(amount_s); } catch (...) { return 0.0; }\\n}", "#include <string>\\n#include <sstream>\\nstd::string to_csv(const std::string& name, const std::string& category, double amount) {\\n    return name + \",\" + category + \",\" + std::to_string((int)amount);\\n}\\ndouble from_csv(const std::string& line) {\\n    std::istringstream row{line};\\n    std::string name, category, amount_s;\\n    if (!std::getline(row, name, ',')) return 0.0;\\n    if (!std::getline(row, category, ',')) return 0.0;\\n    if (!std::getline(row, amount_s)) return 0.0;\\n    try { return std::stod(amount_s); } catch (...) { return 0.0; }\\n}"),
    ],
)

print("modules 15-19 authored")
