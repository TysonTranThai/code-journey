#!/usr/bin/env python3
"""C++ Advanced — module 15 (build-systems) and module 16 (abi-linking).

Grading note: the sandbox compiles a single translation unit with fixed flags
(-std=c++20 -Wall -Wextra -Wpedantic). CMake runs and real multi-object
linking are NOT gradeable there, so this module grades the *portable kernel*
of build/ABI knowledge: feature-test macros, compile-time configuration
arithmetic, alignment/layout math, ABI-stable interfaces (pimpl, extern "C"
factories, function-pointer vtables), and ODR-safe constants. The lessons
teach the full CMake/ABI story; the challenges grade what a single TU can
prove deterministically. Documented, not faked.
"""
from cppa import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 15: build-systems ============================
M15 = "build-systems"

L15A = "cmake-targets-and-props"
L15B = "flags-modes-and-presets"
L15C = "cppa-checkpoint-build"

write_module(
    M15,
    "Advanced Build Systems",
    "CMake targets and properties, Debug/Release flag engineering, presets, and the configuration values your code can see at compile time.",
    "Hệ Thống Build Nâng Cao",
    "CMake targets và properties, kỹ nghệ cờ Debug/Release, presets, và các giá trị cấu hình mà code của bạn nhìn thấy lúc biên dịch.",
    [L15A, L15B, L15C],
    ["m15-config-practice"],
)

write_lesson(
    M15, L15A,
    "CMake Targets & Properties",
    "Modern CMake is targets all the way down: every include path, define, and flag is a property of a target, never a global leak.",
    12,
    r'''
## Targets, not directories

Legacy CMake set global variables (`include_directories`, `add_definitions`) that leaked everywhere. Modern CMake attaches everything to **targets**:

```cpp
add_library(fmtlib STATIC src/fmt.cpp)
target_include_directories(fmtlib PUBLIC include)
target_compile_features(fmtlib PUBLIC cxx_std_20)
target_compile_definitions(fmtlib PRIVATE FMTLIB_BUILDING)
```

The keyword is the contract: `PUBLIC` = needed by consumers too (propagates), `PRIVATE` = only while building me, `INTERFACE` = consumers only (header-only). A consumer that does `target_link_libraries(app PRIVATE fmtlib)` inherits exactly what it needs — usage requirements flow through the build graph.

## Why this matters for correctness

Target scoping is not tidiness; it is correctness. A definition that leaks into a header you ship (because it was `PUBLIC` by accident) becomes an **ODR hazard** for every consumer that compiles with different flags (module 17). The build system is where binary compatibility begins.

## Presets: reproducible configuration

`CMakePresets.json` pins generator, toolchain, and cache variables per configuration so `cmake --preset release` is the same on every machine — the entry point CI uses, and the reason "works on my machine" stops being a build bug.
''',
    "CMake Targets & Properties",
    "CMake hiện đại là targets từ trên xuống dưới: mọi include path, define, và cờ là property của một target, không bao giờ rò rỉ toàn cục.",
    r'''
## Targets, không phải directories

CMake cổ điển đặt biến toàn cục (`include_directories`, `add_definitions`) rò rỉ khắp nơi. CMake hiện đại gắn mọi thứ vào **targets**:

```cpp
add_library(fmtlib STATIC src/fmt.cpp)
target_include_directories(fmtlib PUBLIC include)
target_compile_features(fmtlib PUBLIC cxx_std_20)
target_compile_definitions(fmtlib PRIVATE FMTLIB_BUILDING)
```

Từ khóa chính là hợp đồng: `PUBLIC` = consumer cũng cần (lan truyền), `PRIVATE` = chỉ khi build tôi, `INTERFACE` = chỉ cho consumer (header-only). Consumer gọi `target_link_libraries(app PRIVATE fmtlib)` kế thừa đúng những gì cần — yêu cầu sử dụng chảy qua đồ thị build.

## Vì sao điều này liên quan đến tính đúng đắn

Scoping theo target không phải là sự gọn gàng; đó là tính đúng đắn. Một define rò rỉ vào header bạn giao đi (vì lỡ để `PUBLIC`) trở thành **nguy cơ ODR** cho mọi consumer biên dịch với cờ khác (module 17). Build system là nơi khả năng tương thích nhị phân bắt đầu.

## Presets: cấu hình tái lập được

`CMakePresets.json` ghim generator, toolchain, và biến cache theo từng cấu hình để `cmake --preset release` giống nhau trên mọi máy — điểm vào mà CI dùng, và lý do "chạy trên máy tôi" ngừng là một bug build.
''',
)

write_lesson(
    M15, L15B,
    "Flags, Modes & Compile-Time Configuration",
    "Debug vs Release changes observable behavior you can detect: __OPTIMIZE__, NDEBUG, and your own feature-test macros form the code-side contract of the build.",
    11,
    r'''
## The build mode is visible from inside the code

Compilers define markers you can test:

- `__OPTIMIZE__` — GCC/Clang define it when optimizing (-O1+); MSVC does not.
- `NDEBUG` — defined by CMake's *Release/RelWithDebInfo* configurations; it **disables `assert`**. Debug/RelWithDebInfo/Release is not just speed: it changes which assertions exist in the binary.
- Your own macros: `-DCJ_LOG_LEVEL=2` becomes `#if CJ_LOG_LEVEL >= 2` in code.

## Feature-test discipline

Never test compiler identity (`#ifdef _MSC_VER`) when you mean capability. `<version>` / `__has_include` / feature-test macros ask what the toolchain *provides*:

```cpp
#include <version>
#ifdef __cpp_lib_format        // capability question
#  include <format>
#endif
#ifdef __cpp_exceptions        // is exception handling on?
#endif
```

`__has_feature` (Clang) and `__SANITIZE_ADDRESS__` (GCC) report sanitizer state — the code can know whether ASan is watching.

## What the fixed sandbox grades

This course's sandbox compiles with `-std=c++20 -Wall -Wextra -Wpedantic` and no mode toggles — so the graded exercises here test the *code side*: correct `__cpp_*` guards, correct `NDEBUG`-independent logic, and configuration arithmetic that a single translation unit can prove. The full Debug/Release/CI story is in the lesson text, exercised in the projects, not the sandbox.
''',
    "Cờ, Chế Độ & Cấu Hình Lúc Biên Dịch",
    "Debug vs Release thay đổi hành vi quan sát được từ trong code: __OPTIMIZE__, NDEBUG, và feature-test macro của chính bạn tạo thành hợp đồng phía code của build.",
    r'''
## Chế độ build nhìn thấy được từ trong code

Compiler định nghĩa các marker bạn có thể test:

- `__OPTIMIZE__` — GCC/Clang định nghĩa khi tối ưu (-O1+); MSVC thì không.
- `NDEBUG` — được định nghĩa bởi cấu hình *Release/RelWithDebInfo* của CMake; nó **tắt `assert`**. Debug/RelWithDebInfo/Release không chỉ là tốc độ: nó thay đổi assertion nào tồn tại trong binary.
- Macro của bạn: `-DCJ_LOG_LEVEL=2` thành `#if CJ_LOG_LEVEL >= 2` trong code.

## Kỷ luật feature-test

Không bao giờ test danh tính compiler (`#ifdef _MSC_VER`) khi ý bạn là capability. `<version>` / `__has_include` / feature-test macro hỏi toolchain *cung cấp gì*:

```cpp
#include <version>
#ifdef __cpp_lib_format        // câu hỏi capability
#  include <format>
#endif
#ifdef __cpp_exceptions        // exception handling có bật?
#endif
```

`__has_feature` (Clang) và `__SANITIZE_ADDRESS__` (GCC) báo trạng thái sanitizer — code có thể biết ASan có đang theo dõi không.

## Sandbox cố định chấm gì

Sandbox của khóa này biên dịch với `-std=c++20 -Wall -Wextra -Wpedantic`, không chuyển chế độ — nên bài graded ở đây test *phía code*: guard `__cpp_*` đúng, logic độc lập với `NDEBUG` đúng, và phép tính cấu hình mà một translation unit chứng minh được. Toàn bộ câu chuyện Debug/Release/CI nằm trong bài học và các project, không nằm trong sandbox.
''',
)

# ---------------- practice: config guards + configuration arithmetic ----------------
CP15_BOILER = r'''#include <version>
#include <cstdint>

// Compile-time build configuration contract.
// Every query answers with a constexpr value the test can prove.
namespace buildcfg {
// 1) true iff the standard library exposes std::format (feature-test, not compiler sniffing).
constexpr bool has_format();
// 2) true iff exception handling is enabled in this TU.
constexpr bool exceptions_enabled();
// 3) the numeric log level: CJ_LOG_LEVEL if defined, else 0.
constexpr int log_level();
// 4) true iff assertions are compiled out (NDEBUG defined).
constexpr bool asserts_disabled();
// 5) true iff an address sanitizer is active in this TU (either vendor's marker).
constexpr bool asan_active();
} // namespace buildcfg
'''

M15_PRAC1_CH = [
    challenge(
        "cppa15-config-guards",
        "Build Configuration Contract",
        "Implement the five `buildcfg` queries using only capability markers (feature-test macros, __has_include, __has_feature) — no compiler-identity sniffing.",
        CP15_BOILER,
        [
            ("capability markers, not compiler sniffing",
             r'''static_assert(buildcfg::has_format() == (bool)__cpp_lib_format,
              "has_format must mirror __cpp_lib_format exactly");
static_assert(buildcfg::exceptions_enabled() ==
              (bool)(__cpp_exceptions || __EXCEPTIONS),
              "exceptions_enabled must match this TU");
static_assert(!buildcfg::asserts_disabled(), "NDEBUG is not defined in this TU");
static_assert(!buildcfg::asan_active(), "no sanitizer in this TU");
static_assert(buildcfg::log_level() == 0, "default log level is 0");
CHECK(buildcfg::has_format() || !__cpp_lib_format);''',
             "Guard with #ifdef __cpp_lib_format (from <version>). ASan: __SANITIZE_ADDRESS__ (GCC) or __has_feature(address_sanitizer) (Clang)."),
        ],
        difficulty="advanced",
    ),
]

M15_PRAC1_VI = {
    "cppa15-config-guards": vi_challenge(
        "Hợp Đồng Cấu Hình Build",
        "Cài năm truy vấn `buildcfg` chỉ bằng capability marker (feature-test macro, __has_include, __has_feature) — không dò danh tính compiler.",
        [("capability markers, không phải dò compiler",
          "Guard bằng #ifdef __cpp_lib_format (từ <version>). ASan: __SANITIZE_ADDRESS__ (GCC) hoặc __has_feature(address_sanitizer) (Clang).")],
    ),
}

# The sandbox flags are fixed, so the graded assertions must be compiled by the
# solution itself via the boilerplate contract: the test checks that the
# solution-defined constexpr values agree with the preprocessor truth *in this
# exact TU* (which has no NDEBUG, no sanitizers, and __cpp_lib_format per g++).
M15_PRAC1_TEST = r'''// The single-TU proof: every constexpr answer must agree with the
// preprocessor's answer in this translation unit.
static_assert(!buildcfg::asserts_disabled(), "NDEBUG is not defined here");
static_assert(buildcfg::exceptions_enabled(), "exceptions are on");
static_assert(!buildcfg::asan_active(), "no sanitizer in this TU");
static_assert(buildcfg::has_format() == (bool)__cpp_lib_format,
              "has_format must mirror __cpp_lib_format exactly");
static_assert(buildcfg::log_level() == 0, "default log level is 0");
'''

M15_PRAC1_SOL = [
    ("cppa15-config-guards",
     '#include <version>\n#include <cstdint>\n\nnamespace buildcfg {\n#if defined(__cpp_exceptions) || defined(__EXCEPTIONS)\nconstexpr bool exceptions_enabled() { return true; }\n#else\nconstexpr bool exceptions_enabled() { return false; }\n#endif\n#ifdef NDEBUG\nconstexpr bool asserts_disabled() { return true; }\n#else\nconstexpr bool asserts_disabled() { return false; }\n#endif\n#if defined(__SANITIZE_ADDRESS__) || (defined(__has_feature) && __has_feature(address_sanitizer))\nconstexpr bool asan_active() { return true; }\n#else\nconstexpr bool asan_active() { return false; }\n#endif\n#ifndef CJ_LOG_LEVEL\n#define CJ_LOG_LEVEL 0\n#endif\nconstexpr int kLogLevel = CJ_LOG_LEVEL;\nconstexpr int log_level() { return kLogLevel; }\n#ifdef __cpp_lib_format\nconstexpr bool has_format() { return true; }\n#else\nconstexpr bool has_format() { return false; }\n#endif\n} // namespace buildcfg\n',
     '#include <version>\n#include <cstdint>\n\nnamespace buildcfg {\nconstexpr bool exceptions_enabled() { return true; }      // WRONG: hardcoded, ignores __cpp_exceptions\nconstexpr bool asserts_disabled() { return false; }        // WRONG: hardcoded\nconstexpr bool asan_active() { return true; }              // WRONG: claims sanitizer always on\nconstexpr int log_level() { return 3; }                    // WRONG: ignores CJ_LOG_LEVEL\nconstexpr bool has_format() { return true; }               // WRONG: unguarded claim\n} // namespace buildcfg\n'),
]

write_practice(
    M15, "m15-config-practice",
    "Practice: Compile-Time Build Config",
    "Make the binary answer build questions itself — capability markers only, provable by static_assert in the same TU.",
    "Luyện tập: Cấu Hình Build Lúc Biên Dịch",
    "Biến binary tự trả lời câu hỏi build — chỉ dùng capability marker, chứng minh được bằng static_assert trong cùng TU.",
    L15B, 14, "advanced",
    challenges=M15_PRAC1_CH, vi_challenges=M15_PRAC1_VI, solutions=M15_PRAC1_SOL)

write_checkpoint(
    M15, L15C,
    "Checkpoint — Build Reasoning",
    "One graded challenge: reimplement the config contract so every static_assert in the test passes by construction.",
    8,
    r'''
## What you must be able to do

Answer build questions **from inside the code**, with capability markers, so that a fixed-flags compile of your file *proves* the answers. This is the skill CI config, sanitizer-gated code paths, and versioned ABIs are all built on.
''',
    "Điểm Chốt — Suy Luận Build",
    "Một bài chấm điểm: cài lại hợp đồng cấu hình để mọi static_assert trong test đúng by construction.",
    r'''
## Bạn phải làm được gì

Trả lời các câu hỏi build **từ trong code**, bằng capability marker, để một lần biên dịch cờ cố định của file bạn *chứng minh* các câu trả lời. Đây là kỹ năng mà CI config, code-path có sanitizer-gate, và ABI có phiên bản đều dựa trên.
''',
    challenge(
        "cppa15-build-checkpoint",
        "Config Contract, Proven",
        "Implement the `buildcfg` namespace so that every static_assert in the test file holds in this TU (no NDEBUG, no sanitizers, exceptions on). Same contract as the practice — this one must be exact.",
        CP15_BOILER,
        [
            ("static_assert proof battery",
             r'''static_assert(buildcfg::exceptions_enabled());
static_assert(!buildcfg::asserts_disabled());
static_assert(!buildcfg::asan_active());
static_assert(buildcfg::has_format() == (bool)__cpp_lib_format);
static_assert(buildcfg::log_level() == 0);''',
             "Each answer: the preprocessor truth of THIS TU. __cpp_exceptions for exceptions, NDEBUG for asserts, __SANITIZE_ADDRESS__/__has_feature(address_sanitizer) for ASan, __cpp_lib_format guarded, CJ_LOG_LEVEL defaulting to 0."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Hợp Đồng Cấu Hình, Chứng Minh Được",
        "Cài namespace `buildcfg` để mọi static_assert trong test đúng trong TU này (không NDEBUG, không sanitizer, exceptions bật). Cùng hợp đồng với bài luyện — bài này phải chính xác tuyệt đối.",
        [("static_assert proof battery",
          "Mỗi câu trả lời: sự thật preprocessor của TU NÀY. __cpp_exceptions cho exceptions, NDEBUG cho asserts, __SANITIZE_ADDRESS__/__has_feature(address_sanitizer) cho ASan, guard __cpp_lib_format, CJ_LOG_LEVEL mặc định 0.")],
    ),
    solution='#include <version>\n#include <cstdint>\n\nnamespace buildcfg {\n#if defined(__cpp_exceptions) || defined(__EXCEPTIONS)\nconstexpr bool exceptions_enabled() { return true; }\n#else\nconstexpr bool exceptions_enabled() { return false; }\n#endif\n#ifdef NDEBUG\nconstexpr bool asserts_disabled() { return true; }\n#else\nconstexpr bool asserts_disabled() { return false; }\n#endif\n#if defined(__SANITIZE_ADDRESS__) || (defined(__has_feature) && __has_feature(address_sanitizer))\nconstexpr bool asan_active() { return true; }\n#else\nconstexpr bool asan_active() { return false; }\n#endif\n#ifndef CJ_LOG_LEVEL\n#define CJ_LOG_LEVEL 0\n#endif\nconstexpr int kLogLevelCP = CJ_LOG_LEVEL;\nconstexpr int log_level() { return kLogLevelCP; }\n#ifdef __cpp_lib_format\nconstexpr bool has_format() { return true; }\n#else\nconstexpr bool has_format() { return false; }\n#endif\n} // namespace buildcfg\n',
    wrong='#include <version>\n#include <cstdint>\n\nnamespace buildcfg {\nconstexpr bool exceptions_enabled() { return true; }   // fine here, but:\nconstexpr bool asserts_disabled() { return true; }     // WRONG: NDEBUG is not defined in this TU\nconstexpr bool asan_active() { return true; }          // WRONG: no sanitizer here\nconstexpr int log_level() { return 2; }                // WRONG: default must be 0\nconstexpr bool has_format() { return false; }          // WRONG: __cpp_lib_format is defined here\n} // namespace buildcfg\n',
)

# ============================ MODULE 16: abi-linking ============================
M16 = "abi-linking"

L16A = "api-vs-abi"
L16B = "abi-stable-interfaces"
L16C = "cppa-checkpoint-abi"

write_module(
    M16,
    "ABI, Linking & Compatibility",
    "API vs ABI, name mangling, ODR, visibility — and the pimpl/extern-C/function-table patterns that let a shipped library evolve without breaking its binaries.",
    "ABI, Linking & Khả Năng Tương Thích",
    "API vs ABI, name mangling, ODR, visibility — và các pattern pimpl/extern-C/bảng hàm để thư viện đã giao đi tiến hóa mà không phá binary của nó.",
    [L16A, L16B, L16C],
    ["m16-abi-practice"],
)

write_lesson(
    M16, L16A,
    "API vs ABI",
    "Your API is what callers write; your ABI is what the linker binds. Changing one without the other is how shipped libraries break.",
    12,
    r'''
## Two contracts, two audiences

- **API** (application programming interface): the headers — what compilers accept.
- **ABI** (application binary interface): sizes, layouts, calling conventions, mangled symbol names, which member functions exist *as symbols* — what linkers and already-compiled binaries require.

Adding a parameter changes both. Reordering `private:` members changes only the ABI — and silently corrupts every binary that was compiled against the old layout.

## What the linker actually binds

Each non-inline function and global becomes a **mangled symbol** (`_ZN4demo6Engine4tickEv` encodes namespace/class/name/params). Change a signature and the symbol name changes — old binaries get an unresolved-symbol error at load (visible, at least). Change a class layout with the same signatures and nothing fails to link: calls jump in, offsets land in the wrong places, data corrupts (invisible, worse).

## The One Definition Rule

A function or object with external linkage must have exactly one definition across the whole program; an inline/class-member definition must be **identical** in every TU that includes it. Two TUs including a header compiled with different `-DVERSION` options can quietly violate ODR — the linker picks one, and the other's callers use it. This is why ABI-relevant macros must never differ across a program's TUs.

## Inline is ABI too

Making a previously non-inline member function `inline` changes *which* copies exist; removing `inline` from a header-defined function can break consumers that no longer find the symbol. Header-defined functions are ABI surface — versioned and frozen once shipped.
''',
    "API vs ABI",
    "API của bạn là những gì caller viết; ABI là những gì linker ràng buộc. Đổi cái này mà không đổi cái kia là cách thư viện đã giao đi bị phá.",
    r'''
## Hai hợp đồng, hai khán giả

- **API** (application programming interface): các header — những gì compiler chấp nhận.
- **ABI** (application binary interface): kích thước, layout, calling convention, tên symbol đã mangle, hàm thành viên nào tồn tại *dưới dạng symbol* — những gì linker và binary đã biên dịch từ trước yêu cầu.

Thêm một tham số đổi cả hai. Đổi thứ tự thành viên `private:` chỉ đổi ABI — và âm thầm làm hỏng mọi binary được biên dịch với layout cũ.

## Linker thực sự ràng buộc gì

Mỗi hàm non-inline và biến toàn cục trở thành một **symbol đã mangle** (`_ZN4demo6Engine4tickEv` mã hóa namespace/class/tên/tham số). Đổi chữ ký và tên symbol đổi — binary cũ gặp lỗi unresolved-symbol lúc load (hỏng thấy được, may ra). Đổi layout class với cùng chữ ký thì không gì fail khi link: call nhảy vào, offset rơi sai chỗ, dữ liệu hỏng (hỏng không thấy được, nguy hơn).

## Quy tắc Một Định Nghĩa (ODR)

Một hàm hay đối tượng có external linkage phải có đúng một định nghĩa trong toàn chương trình; định nghĩa inline/thành viên lớp phải **giống hệt** trong mọi TU include nó. Hai TU include cùng header nhưng biên dịch với `-DVERSION` khác nhau có thể lặng lẽ vi phạm ODR — linker chọn một, callers của bên kia dùng bản được chọn. Vì thế macro liên quan ABI không bao giờ được khác nhau giữa các TU của một chương trình.

## Inline cũng là ABI

Biến một hàm thành viên non-inline thành `inline` đổi *bản sao nào* tồn tại; bỏ `inline` khỏi hàm định nghĩa trong header có thể phá consumer không còn tìm thấy symbol. Hàm định nghĩa trong header là bề mặt ABI — được phiên bản hóa và đóng băng một khi đã giao.
''',
)

write_lesson(
    M16, L16B,
    "ABI-Stable Interfaces",
    "pimpl, extern \"C\" factories, and function-pointer tables: three load-bearing patterns that keep binaries working while the implementation moves.",
    12,
    r'''
## Pattern 1 — pimpl (pointer to implementation)

```cpp
// engine.hpp — shipped, frozen
class Engine {
public:
    Engine();
    ~Engine();                       // must be out-of-line! (see below)
    void tick(int units);
private:
    struct Impl;                     // never defined in the header
    Impl* impl_;                     // or std::unique_ptr<Impl> with out-of-line dtor
};
```

All private state hides behind one pointer. Adding members, changing algorithms, even swapping data structures: the header never changes, the layout of `Engine` stays one-pointer-wide, old binaries keep working. The destructor must live in the .cpp — the compiler generates the deleter there, where `Impl` is complete. (With `unique_ptr<Impl>` as a member, an in-header inline dtor would instantiate `default_delete<Impl>` on an incomplete type — a compile error; with a raw pointer plus out-of-line dtor, it is just a delete you owe once.)

## Pattern 2 — extern "C" factory + opaque handle

`extern "C"` disables mangling: one fixed symbol name, callable from any language, immune to C++ signature drift. Combined with an opaque pointer it is the classic plugin boundary:

```cpp
extern "C" Engine* engine_create();
extern "C" void    engine_tick(Engine*, int units);
extern "C" void    engine_destroy(Engine*);
```

Implementation can be rewritten completely; the three symbols are the contract.

## Pattern 3 — versioned function tables

New capability without breaking old callers: append function pointers at the end of a struct and bump a version field. Old callers read v1 fields and stop; new callers check `version >= 2` before touching later entries. This is how OS and driver ABIs stay stable for decades.

## What the fixed sandbox grades

Real .so linking is not gradeable in a single-TU harness, so the exercises grade the patterns' *logic*: pimpl lifecycle with the correct out-of-line destructor discipline, opaque-handle factory/destroy contracts, table versioning arithmetic, and ODR-safe constant scoping. Documented limitation, deliberately chosen.
''',
    "Giao Diện Ổn Định ABI",
    "pimpl, factory extern \"C\", và bảng con trỏ hàm: ba pattern trụ cột giữ binary chạy tốt trong khi phần cài đặt vẫn di chuyển.",
    r'''
## Pattern 1 — pimpl (con trỏ tới phần cài đặt)

```cpp
// engine.hpp — đã giao, đóng băng
class Engine {
public:
    Engine();
    ~Engine();                       // phải định nghĩa ngoài lớp! (xem dưới)
    void tick(int units);
private:
    struct Impl;                     // không bao giờ định nghĩa trong header
    Impl* impl_;                     // hoặc std::unique_ptr<Impl> với dtor out-of-line
};
```

Mọi trạng thái private nấp sau một con trỏ. Thêm thành viên, đổi thuật toán, thậm chí thay cấu trúc dữ liệu: header không đổi, layout của `Engine` vẫn rộng một con trỏ, binary cũ vẫn chạy. Destructor phải nằm trong .cpp — compiler sinh deleter ở đó, nơi `Impl` đã complete. (Với `unique_ptr<Impl>` làm thành viên, dtor inline trong header sẽ instantiate `default_delete<Impl>` trên kiểu chưa complete — lỗi biên dịch; với con trỏ thô cộng dtor out-of-line, đó chỉ là một delete bạn nợ đúng một lần.)

## Pattern 2 — factory extern "C" + handle mờ

`extern "C"` tắt mangle: một tên symbol cố định, gọi được từ bất kỳ ngôn ngữ nào, miễn nhiễm với trôi chữ ký C++. Kết hợp với con trỏ mờ, đó là biên giới plugin cổ điển:

```cpp
extern "C" Engine* engine_create();
extern "C" void    engine_tick(Engine*, int units);
extern "C" void    engine_destroy(Engine*);
```

Phần cài đặt có thể viết lại hoàn toàn; ba symbol đó là hợp đồng.

## Pattern 3 — bảng hàm có phiên bản

Thêm năng lực mới mà không phá caller cũ: nối con trỏ hàm vào cuối struct và tăng trường phiên bản. Caller cũ đọc các trường v1 rồi dừng; caller mới kiểm tra `version >= 2` trước khi đụng các mục sau. Đây là cách ABI của OS và driver giữ ổn định hàng thập kỷ.

## Sandbox cố định chấm gì

Link .so thật không chấm được trong harness một TU, nên bài tập chấm *logic* của pattern: vòng đời pimpl với kỷ luật dtor out-of-line đúng, hợp đồng factory/destroy handle mờ, phép tính phiên bản bảng, và scoping hằng an toàn ODR. Hạn chế được ghi nhận, được chọn có chủ đích.
''',
)

# ---------------- practice: pimpl lifecycle + opaque factory ----------------
CP16_BOILER = r'''#include <cstddef>
#include <cstdint>
#include <string>

// --- ABI-stable widget: pimpl with disciplined lifecycle ---
class Widget {
public:
    Widget();                       // allocates Impl
    ~Widget();                      // YOU implement out-of-line discipline
    Widget(const Widget&) = delete;
    Widget& operator=(const Widget&) = delete;
    Widget(Widget&& other) noexcept;
    Widget& operator=(Widget&& other) noexcept;
    void set(const std::string& key, std::int64_t value);
    std::int64_t get(const std::string& key) const;   // 0 if absent
    std::size_t size() const;
private:
    struct Impl;
    Impl* impl_;
};

// --- versioned function table (pattern 3) ---
struct WidgetApi {
    std::uint32_t version;          // 1
    std::int64_t (*get)(void* self, const char* key);
    void (*set)(void* self, const char* key, std::int64_t value);
};

// Opaque-handle factory contract used by the tests.
extern "C" void* wapiCreate();
extern "C" void  wapiDestroy(void** handle);   // takes the slot: can null it (idempotent)
extern "C" void  wapiFillApi(WidgetApi* api);  // the library publishes its v1 table
'''

M16_PRAC1_CH = [
    challenge(
        "cppa16-pimpl-discipline",
        "Pimpl Lifecycle Discipline",
        "Implement `Widget`'s pimpl correctly: constructor allocates, destructor destroys exactly once, move steals and nulls the source (double-move-safe: moving twice must not crash), and every operation is safe on an empty (moved-from) instance.",
        CP16_BOILER,
        [
            ("lifecycle battery",
             r'''{
    Widget w;
    w.set("hits", 42);
    CHECK_EQ(w.get("hits"), 42);
    CHECK_EQ(w.size(), 1);
    Widget w2(std::move(w));
    CHECK_EQ(w2.get("hits"), 42);      // stolen
    CHECK_EQ(w.size(), 0);             // source emptied
    w.set("after", 1);                 // moved-from must be safe to reuse
    CHECK_EQ(w.get("after"), 1);
    Widget w3(std::move(w));           // double move: no crash, no leak
    CHECK_EQ(w3.get("after"), 1);
    Widget w4(std::move(w3));
    CHECK_EQ(w4.size(), std::size_t{1});
}''',
             "Move: steal impl_ then set source impl_ = nullptr. All ops must branch on impl_ == nullptr (treat as empty). Destructor: delete impl_ only if non-null (delete on nullptr is fine — but the moved-from dtor runs too, so a second delete of the SAME pointer is the crash to avoid)."),
        ],
        difficulty="advanced",
    ),
    challenge(
        "cppa16-opaque-factory",
        "Opaque-Handle Factory Contract",
        "Implement the extern \"C\"-style factory contract (linkage-free in this harness): `wapiCreate/WapiDestroy` manage an opaque handle, and the versioned `WidgetApi` table exposes only v1 calls. Destroy must be idempotent (destroying twice is a no-op, not a double free).",
        CP16_BOILER,
        [
            ("opaque handle + idempotent destroy",
             r'''void* h = wapiCreate();
WidgetApi api{};
wapiFillApi(&api);                    // library wires its thunks into the table
api.set(h, "k", 7);
CHECK_EQ(api.get(h, "k"), 7);
wapiDestroy(&h);
wapiDestroy(&h);                      // must be a no-op (and null the slot)''',
             "wapiDestroy(void** slot): if (!slot || !*slot) return; delete contents; *slot = nullptr. Taking the slot is what makes idempotence possible."),
        ],
        difficulty="advanced",
    ),
]

M16_PRAC1_VI = {
    "cppa16-pimpl-discipline": vi_challenge(
        "Kỷ Luật Vòng Đời Pimpl",
        "Cài pimpl của `Widget` đúng: constructor cấp phát, destructor hủy đúng một lần, move đánh cắp và làm rỗng nguồn (an toàn double-move: move hai lần không crash), mọi thao tác an toàn trên instance rỗng (đã move).",
        [("lifecycle battery",
          "Move: đánh cắp impl_ rồi đặt nguồn impl_ = nullptr. Mọi thao tác phải kiểm tra impl_ == nullptr (coi như rỗng). Destructor: chỉ delete impl_ khi khác null.")],
    ),
    "cppa16-opaque-factory": vi_challenge(
        "Hợp Đồng Factory Handle Mờ",
        "Cài hợp đồng factory kiểu extern \"C\" (không cần linkage trong harness này): `wapiCreate/WapiDestroy` quản lý handle mờ, bảng `WidgetApi` có phiên bản chỉ mở các call v1. Destroy phải idempotent (destroy hai lần là no-op, không double free).",
        [("opaque handle + destroy idempotent",
          "wapiDestroy(void** slot): if (!slot || !*slot) return; delete nội dung; *slot = nullptr. Nhận ô nhớ (slot) mới làm được idempotence.")],
    ),
}

M16_PRAC1_SOL = [
    ("cppa16-pimpl-discipline",
     CP16_BOILER + '\nstruct Widget::Impl { std::string keys[64]; std::int64_t vals[64]; std::size_t n = 0; };\nWidget::Widget() : impl_(new Impl()) {}\nWidget::~Widget() { delete impl_; }\nWidget::Widget(Widget&& other) noexcept : impl_(other.impl_) { other.impl_ = nullptr; }\nWidget& Widget::operator=(Widget&& other) noexcept {\n    if (this != &other) { delete impl_; impl_ = other.impl_; other.impl_ = nullptr; }\n    return *this;\n}\nvoid Widget::set(const std::string& key, std::int64_t value) {\n    if (!impl_) impl_ = new Impl();   // moved-from widgets are empty but reusable\n    for (std::size_t i = 0; i < impl_->n; ++i)\n        if (impl_->keys[i] == key) { impl_->vals[i] = value; return; }\n    if (impl_->n < 64) { impl_->keys[impl_->n] = key; impl_->vals[impl_->n] = value; ++impl_->n; }\n}\nstd::int64_t Widget::get(const std::string& key) const {\n    if (!impl_) return 0;\n    for (std::size_t i = 0; i < impl_->n; ++i)\n        if (impl_->keys[i] == key) return impl_->vals[i];\n    return 0;\n}\nstd::size_t Widget::size() const { return impl_ ? impl_->n : 0; }\n',
     CP16_BOILER + '\nstruct Widget::Impl { std::string keys[64]; std::int64_t vals[64]; std::size_t n = 0; };\nWidget::Widget() : impl_(new Impl()) {}\nWidget::~Widget() { delete impl_; }\nWidget::Widget(Widget&& other) noexcept : impl_(other.impl_) { other.impl_ = nullptr; }\nWidget& Widget::operator=(Widget&& other) noexcept {\n    // WRONG: no self-check and no source nulling — self-assignment deletes then copies garbage\n    delete impl_; impl_ = other.impl_;\n    return *this;\n}\nvoid Widget::set(const std::string& key, std::int64_t value) {\n    for (std::size_t i = 0; i < impl_->n; ++i)          // WRONG: no nullptr guard — moved-from set() crashes\n        if (impl_->keys[i] == key) { impl_->vals[i] = value; return; }\n    if (impl_->n < 64) { impl_->keys[impl_->n] = key; impl_->vals[impl_->n] = value; ++impl_->n; }\n}\nstd::int64_t Widget::get(const std::string& key) const {\n    if (!impl_) return 0;\n    for (std::size_t i = 0; i < impl_->n; ++i)\n        if (impl_->keys[i] == key) return impl_->vals[i];\n    return 0;\n}\nstd::size_t Widget::size() const { return impl_ ? impl_->n : 0; }\n'),
    ("cppa16-opaque-factory",
     CP16_BOILER + '\nstruct Widget::Impl { std::string keys[64]; std::int64_t vals[64]; std::size_t n = 0; };\nWidget::Widget() : impl_(new Impl()) {}\nWidget::~Widget() { delete impl_; }\nWidget::Widget(Widget&& other) noexcept : impl_(other.impl_) { other.impl_ = nullptr; }\nWidget& Widget::operator=(Widget&& other) noexcept {\n    if (this != &other) { delete impl_; impl_ = other.impl_; other.impl_ = nullptr; }\n    return *this;\n}\nvoid Widget::set(const std::string& key, std::int64_t value) {\n    if (!impl_) impl_ = new Impl();\n    for (std::size_t i = 0; i < impl_->n; ++i)\n        if (impl_->keys[i] == key) { impl_->vals[i] = value; return; }\n    if (impl_->n < 64) { impl_->keys[impl_->n] = key; impl_->vals[impl_->n] = value; ++impl_->n; }\n}\nstd::int64_t Widget::get(const std::string& key) const {\n    if (!impl_) return 0;\n    for (std::size_t i = 0; i < impl_->n; ++i)\n        if (impl_->keys[i] == key) return impl_->vals[i];\n    return 0;\n}\nstd::size_t Widget::size() const { return impl_ ? impl_->n : 0; }\nstruct WHandle { Widget* w; };\nstruct WSlot { WHandle* h; };\nextern "C" void* wapiCreate() { return new WSlot{new WHandle{new Widget()}}; }\nextern "C" void wapiDestroy(void** slot) {\n    if (!slot || !*slot) return;                      // idempotent\n    WSlot* s = static_cast<WSlot*>(*slot);\n    delete s->h->w;\n    delete s->h;\n    delete s;\n    *slot = nullptr;                                  // null the caller slot\n}\nstatic std::int64_t apiGet(void* self, const char* key) {\n    WSlot* s = static_cast<WSlot*>(self);\n    return (s && s->h) ? s->h->w->get(key) : 0;\n}\nstatic void apiSet(void* self, const char* key, std::int64_t v) {\n    WSlot* s = static_cast<WSlot*>(self);\n    if (s && s->h) s->h->w->set(key, v);\n}\nextern "C" void wapiFillApi(WidgetApi* api) {\n    if (!api) return;\n    api->version = 1;\n    api->get = apiGet;\n    api->set = apiSet;\n}\n',
     CP16_BOILER + '\nstruct Widget::Impl { std::string keys[64]; std::int64_t vals[64]; std::size_t n = 0; };\nWidget::Widget() : impl_(new Impl()) {}\nWidget::~Widget() { delete impl_; }\nWidget::Widget(Widget&& other) noexcept : impl_(other.impl_) { other.impl_ = nullptr; }\nWidget& Widget::operator=(Widget&& other) noexcept {\n    if (this != &other) { delete impl_; impl_ = other.impl_; other.impl_ = nullptr; }\n    return *this;\n}\nvoid Widget::set(const std::string& key, std::int64_t value) {\n    if (!impl_) impl_ = new Impl();\n    for (std::size_t i = 0; i < impl_->n; ++i)\n        if (impl_->keys[i] == key) { impl_->vals[i] = value; return; }\n    if (impl_->n < 64) { impl_->keys[impl_->n] = key; impl_->vals[impl_->n] = value; ++impl_->n; }\n}\nstd::int64_t Widget::get(const std::string& key) const {\n    if (!impl_) return 0;\n    for (std::size_t i = 0; i < impl_->n; ++i)\n        if (impl_->keys[i] == key) return impl_->vals[i];\n    return 0;\n}\nstd::size_t Widget::size() const { return impl_ ? impl_->n : 0; }\nstruct WHandle { Widget* w; };\nstruct WSlotW { WHandle* h; };\nextern "C" void* wapiCreate() { return new WSlotW{new WHandle{new Widget()}}; }\nextern "C" void wapiDestroy(void** slot) {\n    if (!slot) return;\n    WSlotW* s = static_cast<WSlotW*>(*slot);          // WRONG: no *slot check — second destroy double-frees\n    delete s->h->w;\n    delete s->h;\n    delete s;\n}\nstatic std::int64_t apiGet(void* self, const char* key) {\n    WSlotW* s = static_cast<WSlotW*>(self);\n    return (s && s->h) ? s->h->w->get(key) : 0;\n}\nstatic void apiSet(void* self, const char* key, std::int64_t v) {\n    WSlotW* s = static_cast<WSlotW*>(self);\n    if (s && s->h) s->h->w->set(key, v);\n}\nextern "C" void wapiFillApi(WidgetApi* api) {\n    if (!api) return;\n    api->version = 1;\n    api->get = apiGet;\n    api->set = apiSet;\n}\n'),
]

write_practice(
    M16, "m16-abi-practice",
    "Practice: ABI-Stable Patterns",
    "Pimpl lifecycle under a double-move battery, and an opaque factory whose destroy survives being called twice.",
    "Luyện tập: Pattern Ổn Định ABI",
    "Vòng đời pimpl dưới loạt double-move, và factory mờ whose destroy sống sót khi bị gọi hai lần.",
    L16B, 16, "advanced",
    challenges=M16_PRAC1_CH, vi_challenges=M16_PRAC1_VI, solutions=M16_PRAC1_SOL)

write_checkpoint(
    M16, L16C,
    "Checkpoint — ABI Reasoning",
    "Grade the ABI contract itself: implement a layout-probe that proves which changes are binary-breaking versus source-compatible.",
    8,
    r'''
## What you must be able to do

Decide, from code alone, whether a change breaks the ABI. The graded challenge freezes a struct, then asks your code to prove the layout facts a maintainer must know before touching it.
''',
    "Điểm Chốt — Suy Luận ABI",
    "Chấm chính hợp đồng ABI: cài một layout-probe chứng minh thay đổi nào là phá binary, thay đổi nào tương thích nguồn.",
    r'''
## Bạn phải làm được gì

Quyết định, chỉ từ code, một thay đổi có phá ABI hay không. Bài chấm điểm đóng băng một struct, rồi yêu cầu code của bạn chứng minh những sự thật layout mà người bảo trì phải biết trước khi đụng vào nó.
''',
    challenge(
        "cppa16-abi-checkpoint",
        "Layout Probe",
        "Implement the four `probe` functions against the frozen `Record` struct: size, alignment, member offsets of `id` and `score`. The test checks them against the ABI facts this compiler produces — wrong probe logic (hardcoded guesses) fails on some platform by construction.",
        '#include <cstddef>\n#include <cstdint>\n\nstruct Record {                 // frozen: reordering these members breaks the ABI\n    std::uint32_t id;\n    double score;\n    std::uint32_t flags;\n};\n\nnamespace probe {\nconstexpr std::size_t size();             // sizeof(Record)\nconstexpr std::size_t align();            // alignof(Record)\nconstexpr std::size_t offset_id();        // offsetof(Record, id)\nconstexpr std::size_t offset_score();     // offsetof(Record, score)\n} // namespace probe\n',
        [
            ("probe equals the compiler's own ABI facts",
             r'''static_assert(probe::size() == sizeof(Record), "size must be sizeof(Record)");
static_assert(probe::align() == alignof(Record), "align must be alignof(Record)");
static_assert(probe::offset_id() == offsetof(Record, id), "id offset");
static_assert(probe::offset_score() == offsetof(Record, score), "score offset");
static_assert(probe::offset_score() % alignof(double) == 0, "double is aligned");
CHECK_EQ(probe::offset_id(), 0);
CHECK(probe::offset_score() >= probe::offset_id() + sizeof(std::uint32_t));''',
             "Forward to the compiler: sizeof(Record), alignof(Record), offsetof(Record, member). Hardcoded numbers are exactly the ABI lie this module warns about."),
        ],
        difficulty="advanced",
    ),
    vi_challenge(
        "Layout Probe",
        "Cài bốn hàm `probe` đối với struct `Record` đã đóng băng: size, alignment, offset của thành viên `id` và `score`. Test đối chiếu với các sự thật ABI mà compiler này sinh ra — logic probe sai (đoán cứng) sẽ fail trên platform khác by construction.",
        [("probe bằng đúng các sự thật ABI của compiler",
          "Chuyển tiếp cho compiler: sizeof(Record), alignof(Record), offsetof(Record, member). Số cứng chính là lời nói dối ABI mà module này cảnh báo.")],
    ),
    solution='#include <cstddef>\n#include <cstdint>\n\nstruct Record {\n    std::uint32_t id;\n    double score;\n    std::uint32_t flags;\n};\n\nnamespace probe {\nconstexpr std::size_t size() { return sizeof(Record); }\nconstexpr std::size_t align() { return alignof(Record); }\nconstexpr std::size_t offset_id() { return offsetof(Record, id); }\nconstexpr std::size_t offset_score() { return offsetof(Record, score); }\n} // namespace probe\n',
    wrong='#include <cstddef>\n#include <cstdint>\n\nstruct Record {\n    std::uint32_t id;\n    double score;\n    std::uint32_t flags;\n};\n\nnamespace probe {\nconstexpr std::size_t size() { return 24; }            // WRONG: hardcoded — breaks when padding differs\nconstexpr std::size_t align() { return 8; }            // WRONG: hardcoded\nconstexpr std::size_t offset_id() { return 0; }        // WRONG: hardcoded (right here by luck)\nconstexpr std::size_t offset_score() { return 4; }     // WRONG: 4 is not 8-aligned; real offset differs\n} // namespace probe\n',
)

print("m15_16 authored")
