#!/usr/bin/env python3
"""C++ Intermediate — Module 8: smart-pointers-raii.

Authoring discipline: every C++ code string (tests, solutions, boilerplate) is
a raw triple-quoted string, so real newlines stay real and C++ "\\n" literals
stay literal. Snippets are self-contained: each test is its own translation
unit (solution.cpp is #included; no cross-test state).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "smart-pointers-raii"

# ---- lesson raii --------------------------------------------------------------
L_raii_EN = r"""
RAII — Resource Acquisition Is Initialization — is the single most important
C++ idiom: wrap every resource in an object whose destructor releases it.
Scope exit, including via exception, runs the destructor. Nothing leaks.

```cpp
class FileGuard {
public:
    explicit FileGuard(std::FILE* f) : f_{f} {}
    ~FileGuard() { if (f_) std::fclose(f_); }

    FileGuard(const FileGuard&) = delete;             // one owner
    FileGuard& operator=(const FileGuard&) = delete;
private:
    std::FILE* f_;
};

void work() {
    FileGuard g{std::fopen("data.txt", "r")};  // acquired
    // ... even an exception here cannot leak the handle
}                                              // destructor runs here
```

You have used RAII all along without naming it: `std::vector` owns its heap
buffer; `std::string` owns its chars; `std::ofstream` owns a file handle.
Smart pointers are just RAII for the case where *you* call `new`: they own
a heap object and delete it in their own destructor.

Ownership is the design word behind the acronym: exactly one piece of code
is responsible for releasing each resource. Everything else borrows.
"""

L_raii_VI = r"""
RAII — Resource Acquisition Is Initialization — là idiom quan trọng nhất
của C++: bọc mọi tài nguyên trong một đối tượng mà destructor của nó giải
phóng tài nguyên đó. Thoát phạm vi, kể cả qua ngoại lệ, đều chạy destructor.
Không rò rỉ.

```cpp
class FileGuard {
public:
    explicit FileGuard(std::FILE* f) : f_{f} {}
    ~FileGuard() { if (f_) std::fclose(f_); }

    FileGuard(const FileGuard&) = delete;             // một chủ sở hữu
    FileGuard& operator=(const FileGuard&) = delete;
private:
    std::FILE* f_;
};

void work() {
    FileGuard g{std::fopen("data.txt", "r")};  // chiếm giữ
    // ... kể cả exception tại đây cũng không làm rò rỉ handle
}                                              // destructor chạy tại đây
```

Bạn đã dùng RAII suốt từ đầu mà chưa gọi tên: `std::vector` sở hữu buffer
heap của nó; `std::string` sở hữu các ký tự; `std::ofstream` sở hữu file
handle. Smart pointer chỉ là RAII cho trường hợp *bạn* gọi `new`: chúng sở
hữu một đối tượng heap và delete nó trong chính destructor của mình.

Ownership là từ khóa thiết kế đứng sau từ viết tắt: đúng một đoạn code chịu
trách nhiệm giải phóng mỗi tài nguyên. Mọi thứ khác chỉ mượn.
"""

# ---- lesson unique-ptr ----------------------------------------------------------
L_unique_EN = r"""
`std::unique_ptr<T>` is the default smart pointer: exclusive ownership,
zero overhead over a raw pointer, deleted when the `unique_ptr` dies.

```cpp
#include <memory>

auto p = std::make_unique<Widget>(arg1, arg2);  // prefer make_unique
p->draw();
auto q = std::move(p);       // ownership transfers; p is now nullptr
// p->draw();                // UB: p is empty — check it first
```

The rules:

- **Always `make_unique`**, not `new`: one allocation, exception safety,
  no naked `new` in application code.
- Non-copyable, movable. Copying would create two owners — the exact bug
  the type exists to prevent.
- Arrays: `std::unique_ptr<T[]>` exists but `std::vector<T>` is almost
  always the right answer.
- Pass `unique_ptr` when you transfer ownership; pass `T&` or `T*` when
  you merely use the object. Functions that *observe* should not name
  smart pointers in their signatures.
"""

L_unique_VI = r"""
`std::unique_ptr<T>` là smart pointer mặc định: sở hữu độc quyền, không tốn
chi phí hơn con trỏ thô, tự delete khi `unique_ptr` chết.

```cpp
#include <memory>

auto p = std::make_unique<Widget>(arg1, arg2);  // ưa dùng make_unique
p->draw();
auto q = std::move(p);       // quyền sở hữu chuyển giao; p giờ là nullptr
// p->draw();                // UB: p rỗng — phải kiểm tra trước
```

Các quy tắc:

- **Luôn dùng `make_unique`**, đừng dùng `new`: một lần cấp phát, an toàn
  ngoại lệ, không `new` trần trụi trong code ứng dụng.
- Không copy được, chỉ move. Copy sẽ tạo ra hai chủ — chính là bug mà kiểu
  này sinh ra để ngăn chặn.
- Mảng: `std::unique_ptr<T[]>` tồn tại nhưng `std::vector<T>` gần như luôn
  là câu trả lời đúng.
- Truyền `unique_ptr` khi bạn chuyển giao sở hữu; truyền `T&` hoặc `T*`
  khi bạn chỉ dùng đối tượng. Hàm chỉ *quan sát* không nên gọi tên smart
  pointer trong chữ ký.
"""

# ---- lesson shared-weak -----------------------------------------------------------
L_shared_EN = r"""
`std::shared_ptr<T>` keeps a control block with two counters: strong (how
many `shared_ptr`s own the object) and weak (how many `weak_ptr`s watch
it). The object dies when the strong count hits zero; the control block
dies when both do.

```cpp
#include <memory>

auto a = std::make_shared<Node>();   // strong = 1
auto b = a;                          // strong = 2
b.reset();                           // strong = 1
a.reset();                           // strong = 0 → destructor runs
```

`std::weak_ptr<T>` observes without owning. It does not keep the object
alive; it can *ask* whether the object still exists:

```cpp
std::weak_ptr<Node> w = a;
if (auto locked = w.lock()) {   // atomic upgrade to shared_ptr
    locked->use();              // object is alive during this block
} else {
    // object already gone
}
```

Use `shared_ptr` only when ownership is genuinely shared across unknown
lifetimes (caches, observers, graphs). It costs an atomic counter and can
hide who releases what — `unique_ptr` stays the default.

The famous trap: two nodes holding `shared_ptr` to each other form a
**reference cycle**; strong counts never reach zero; both leak. The fix is
one direction becoming `weak_ptr` — child points to parent weakly.
"""

L_shared_VI = r"""
`std::shared_ptr<T>` giữ một control block với hai bộ đếm: strong (bao nhiêu
`shared_ptr` sở hữu đối tượng) và weak (bao nhiêu `weak_ptr` theo dõi). Đối
tượng chết khi strong count về 0; control block chết khi cả hai về 0.

```cpp
#include <memory>

auto a = std::make_shared<Node>();   // strong = 1
auto b = a;                          // strong = 2
b.reset();                           // strong = 1
a.reset();                           // strong = 0 → destructor chạy
```

`std::weak_ptr<T>` quan sát mà không sở hữu. Nó không giữ đối tượng sống;
nó chỉ có thể *hỏi* xem đối tượng còn tồn tại không:

```cpp
std::weak_ptr<Node> w = a;
if (auto locked = w.lock()) {   // nâng cấp nguyên tử thành shared_ptr
    locked->use();              // đối tượng còn sống trong khối này
} else {
    // đối tượng đã mất
}
```

Dùng `shared_ptr` chỉ khi sở hữu thật sự được chia sẻ giữa các vòng đời
không rõ trước (cache, observer, đồ thị). Nó tốn một bộ đếm nguyên tử và có
thể che giấu ai giải phóng cái gì — `unique_ptr` vẫn là mặc định.

Bẫy nổi tiếng: hai node giữ `shared_ptr` cho nhau tạo thành **vòng tham
chiếu**; strong count không bao giờ về 0; cả hai rò rỉ. Cách sửa là một
chiều đổi thành `weak_ptr` — con trỏ tới cha theo kiểu weak.
"""

# ---- lesson ownership-design --------------------------------------------------------
L_ownership_EN = r"""
Pick the ownership model before you pick the pointer type.

| Relationship | Model | Tool |
|---|---|---|
| I own, nobody else | exclusive | `unique_ptr` member |
| Shared pool, users outlive creators | shared | `shared_ptr` |
| Back-reference (child → parent) | observing | `weak_ptr` or `T*` |
| Just using, no lifetime stake | observing | `T&` / `T*` parameter |
| The container owns it all | value semantics | `std::vector<T>` |

A worked example — an entity system:

```cpp
class Scene {
    std::vector<std::unique_ptr<Entity>> entities_;  // scene owns
public:
    Entity& spawn() {
        entities_.push_back(std::make_unique<Entity>());
        return *entities_.back();          // hand back a reference, not ownership
    }
};
```

Note the signature discipline: `spawn()` returns `Entity&` because callers
use the entity but the scene keeps owning it. Handing back `unique_ptr`
would invite double-ownership; handing back `shared_ptr` would make the
counters meaningless. Default to `unique_ptr` and references; escalate to
`shared_ptr` only with a stated reason.
"""

L_ownership_VI = r"""
Chọn mô hình sở hữu trước khi chọn loại con trỏ.

| Quan hệ | Mô hình | Công cụ |
|---|---|---|
| Tôi sở hữu, không ai khác | độc quyền | `unique_ptr` member |
| Nhóm dùng chung, người dùng sống lâu hơn người tạo | chia sẻ | `shared_ptr` |
| Tham chiếu ngược (con → cha) | quan sát | `weak_ptr` hoặc `T*` |
| Chỉ sử dụng, không dính vòng đời | quan sát | tham số `T&` / `T*` |
| Container sở hữu tất cả | ngữ nghĩa giá trị | `std::vector<T>` |

Một ví dụ cụ thể — hệ thực thể:

```cpp
class Scene {
    std::vector<std::unique_ptr<Entity>> entities_;  // scene sở hữu
public:
    Entity& spawn() {
        entities_.push_back(std::make_unique<Entity>());
        return *entities_.back();          // trả về reference, không phải sở hữu
    }
};
```

Chú ý kỷ luật chữ ký: `spawn()` trả `Entity&` vì caller *dùng* entity nhưng
scene vẫn giữ quyền sở hữu. Trả `unique_ptr` sẽ mời gọi trùng sở hữu; trả
`shared_ptr` khiến các bộ đếm vô nghĩa. Mặc định dùng `unique_ptr` và
reference; chỉ nâng cấp lên `shared_ptr` khi nêu được lý do.
"""

# ---- practice cppi-p8-unique ---------------------------------------------------
R_STACK_PUSH = r'''#include <memory>
#include <stack>
#include <string>
#include <vector>

class Recorder;

// Full reference: base + derived + stack, matching the challenge boilerplate.
class Recorder {
public:
    void record(const std::string& s) { lines_.push_back(s); }
    const std::vector<std::string>& lines() const { return lines_; }
private:
    std::vector<std::string> lines_;
};

class Command {
public:
    virtual ~Command() = default;
    virtual void run() = 0;
};

class EchoCommand : public Command {
public:
    EchoCommand(Recorder& rec, std::string msg) : rec_{&rec}, msg_{std::move(msg)} {}
    void run() override { rec_->record(msg_); }
private:
    Recorder* rec_;
    std::string msg_;
};

class CommandStack {
public:
    void push(std::unique_ptr<Command> c) { stack_.push(std::move(c)); }
    void run_all() {
        while (!stack_.empty()) {
            stack_.top()->run();
            stack_.pop();
        }
    }
    std::size_t size() const { return stack_.size(); }
private:
    std::stack<std::unique_ptr<Command>> stack_;
};
'''

W_STACK_PUSH = r'''#include <memory>
#include <stack>
#include <string>
#include <vector>

class Recorder {
public:
    void record(const std::string& s) { lines_.push_back(s); }
    const std::vector<std::string>& lines() const { return lines_; }
private:
    std::vector<std::string> lines_;
};

class Command {
public:
    virtual ~Command() = default;
    virtual void run() = 0;
};

class EchoCommand : public Command {
public:
    EchoCommand(Recorder& rec, std::string msg) : rec_{&rec}, msg_{std::move(msg)} {}
    void run() override { rec_->record(msg_); }
private:
    Recorder* rec_;
    std::string msg_;
};

class CommandStack {
public:
    void push(std::unique_ptr<Command> c) { stack_.push(c); }  // BUG: copies
    void run_all() {
        while (!stack_.empty()) {
            stack_.top()->run();
            stack_.pop();
        }
    }
    std::size_t size() const { return stack_.size(); }
private:
    std::stack<std::unique_ptr<Command>> stack_;
};
'''

# ---- practice cppi-p8-shared ------------------------------------------------------
R_OBSERVER = r'''#include <memory>
#include <vector>

class Event {
public:
    void subscribe(std::weak_ptr<void> w) { watchers_.push_back(std::move(w)); }

    int fire() {
        int alive = 0;
        for (auto it = watchers_.begin(); it != watchers_.end();) {
            if (auto locked = it->lock()) {
                ++alive;
                ++it;
            } else {
                it = watchers_.erase(it);  // prune expired watchers
            }
        }
        return alive;
    }

private:
    std::vector<std::weak_ptr<void>> watchers_;
};
'''

W_OBSERVER = r'''#include <memory>
#include <vector>

class Event {
public:
    void subscribe(std::shared_ptr<void> s) { watchers_.push_back(std::move(s)); }

    int fire() {
        return static_cast<int>(watchers_.size());
    }

private:
    std::vector<std::shared_ptr<void>> watchers_;  // BUG: keeps owners alive
};
'''

R_UNIQUE_SWAP = r'''#include <memory>

template <typename T>
void pointer_swap(std::unique_ptr<T>& a, std::unique_ptr<T>& b) {
    std::unique_ptr<T> tmp = std::move(a);
    a = std::move(b);
    b = std::move(tmp);
}
'''

W_UNIQUE_SWAP = r'''#include <memory>

template <typename T>
void pointer_swap(std::unique_ptr<T>& a, std::unique_ptr<T>& b) {
    if (a && b) {
        T tmp = *a;      // BUG: swaps pointee values, not ownership
        *a = *b;
        *b = tmp;
    }
    // an empty side stays empty: ownership never moves
}
'''

R_SHARED_PROBE = r'''#include <memory>

struct SharedProbe {
    static int& alive() { static int n = 0; return n; }
    SharedProbe() { ++alive(); }
    ~SharedProbe() { --alive(); }
};

int probe_lifetimes() {
    auto first = std::make_shared<SharedProbe>();
    {
        auto copy = first;   // strong = 2
    }                        // copy released: strong = 1
    first.reset();           // strong = 0: object destroyed
    return SharedProbe::alive();
}
'''

W_SHARED_PROBE = r'''#include <memory>

struct SharedProbe {
    static int& alive() { static int n = 0; return n; }
    SharedProbe() { ++alive(); }
    ~SharedProbe() { --alive(); }
};

int probe_lifetimes() {
    auto first = std::make_shared<SharedProbe>();
    {
        auto copy = first;
    }
    // BUG: the original owner never releases
    return SharedProbe::alive();   // returns 1
}
'''

# ---- checkpoint: inventory of unique_ptrs ------------------------------------------
R_INVENTORY = r'''#include <memory>
#include <string>
#include <vector>

class Item {
public:
    explicit Item(std::string name) : name_{std::move(name)} {}
    const std::string& name() const { return name_; }
private:
    std::string name_;
};

class Inventory {
public:
    void add(std::unique_ptr<Item> it) { items_.push_back(std::move(it)); }

    std::unique_ptr<Item> take(const std::string& name) {
        for (auto it = items_.begin(); it != items_.end(); ++it) {
            if ((*it)->name() == name) {
                auto out = std::move(*it);
                items_.erase(it);
                return out;            // ownership leaves the inventory
            }
        }
        return nullptr;
    }

    std::size_t size() const { return items_.size(); }
    bool contains(const std::string& name) const {
        for (const auto& up : items_) if (up->name() == name) return true;
        return false;
    }

private:
    std::vector<std::unique_ptr<Item>> items_;
};
'''

W_INVENTORY = r'''#include <memory>
#include <string>
#include <vector>

class Item {
public:
    explicit Item(std::string name) : name_{std::move(name)} {}
    const std::string& name() const { return name_; }
private:
    std::string name_;
};

class Inventory {
public:
    void add(std::unique_ptr<Item> it) { items_.push_back(std::move(it)); }

    std::unique_ptr<Item> take(const std::string& name) {
        for (auto it = items_.begin(); it != items_.end(); ++it) {
            if ((*it)->name() == name) {
                // BUG: erases without moving out — the item is destroyed
                items_.erase(it);
                return nullptr;
            }
        }
        return nullptr;
    }

    std::size_t size() const { return items_.size(); }
    bool contains(const std::string& name) const {
        for (const auto& up : items_) if (up->name() == name) return true;
        return false;
    }

private:
    std::vector<std::unique_ptr<Item>> items_;
};
'''

# ---- challenges ---------------------------------------------------------------------
CH_STACK_PUSH = challenge(
    "cppi-m8-command-stack",
    "unique_ptr command stack",
    "Complete `CommandStack`: `void push(std::unique_ptr<Command> c)` stores the command by transferring ownership (std::move), and `void run_all()` runs each command then pops it. A `Command` base with a virtual destructor is given. Implement a derived `EchoCommand` that records a message when run — the tests define a `Recorder` the EchoCommand must call.",
    r'''#include <memory>
#include <stack>
#include <string>
#include <vector>
#include <iostream>

class Recorder {
public:
    void record(const std::string& s) { lines_.push_back(s); }
    const std::vector<std::string>& lines() const { return lines_; }
private:
    std::vector<std::string> lines_;
};

// Implement: Command (virtual dtor + virtual void run()), EchoCommand
// (takes Recorder& and a message; run() records it), and CommandStack
// { push(unique_ptr<Command>), run_all(), size() }.
''',
    [
        ("push-and-run", 'Recorder rec;\nCommandStack stack;\nstack.push(std::make_unique<EchoCommand>(rec, "hello"));\nCHECK_EQ(stack.size(), 1);\nstack.run_all();\nCHECK_EQ(stack.size(), 0);\nCHECK_EQ(rec.lines().size(), 1);', "push transfers ownership; run_all drains the stack."),
        ("both-run", 'Recorder rec;\nCommandStack stack;\nstack.push(std::make_unique<EchoCommand>(rec, "first"));\nstack.push(std::make_unique<EchoCommand>(rec, "second"));\nstack.run_all();\nCHECK_EQ(rec.lines().size(), 2);\nCHECK(rec.lines()[0] == std::string("first") || rec.lines()[0] == std::string("second"));\nCHECK(rec.lines()[1] != rec.lines()[0]);', "Both commands run exactly once, in stack order (LIFO for std::stack)."),
        ("moved-in", 'Recorder rec;\nCommandStack stack;\nauto c = std::make_unique<EchoCommand>(rec, "moved");\nstack.push(std::move(c));\nCHECK_EQ(c == nullptr, true);\nstack.run_all();\nCHECK_EQ(rec.lines().size(), 1);', "After std::move, the caller's unique_ptr is null."),
    ],
    level="independent",
)

CH_SHARED_CYCLES = challenge(
    "cppi-m8-weak-callbacks",
    "weak_ptr observer pattern",
    "Complete `Event`: `void subscribe(std::weak_ptr<void> w)` stores the watcher, and `int fire()` counts watchers whose object is still alive, pruning expired ones from the list. This is the classic observer pattern that does NOT keep observers alive.",
    r'''#include <memory>
#include <vector>
#include <iostream>

// Implement class Event { subscribe(std::weak_ptr<void>), fire() -> int }
''',
    [
        ("live-watcher", 'Event e;\nauto owner = std::make_shared<int>(42);\ne.subscribe(owner);\nCHECK_EQ(e.fire(), 1);', "A live owner means one surviving watcher."),
        ("expired-watcher", 'Event e;\n{\n    auto owner = std::make_shared<int>(42);\n    e.subscribe(owner);\n}\nCHECK_EQ(e.fire(), 0);', "When the owner dies inside the scope, fire() must not count it."),
        ("mixed-and-prune", 'Event e;\nauto keep = std::make_shared<int>(1);\ne.subscribe(keep);\n{\n    auto dying = std::make_shared<int>(2);\n    e.subscribe(dying);\n}\nCHECK_EQ(e.fire(), 1);\nCHECK_EQ(e.fire(), 1);', "fire() twice: pruning happens on the first pass, the second stays correct."),
    ],
    level="combination",
)

CH_UNIQUE_DANGLING = challenge(
    "cppi-m8-unique-swap",
    "Swap ownership between two unique_ptrs",
    "Implement `template <typename T> void pointer_swap(std::unique_ptr<T>& a, std::unique_ptr<T>& b)` exchanging the two owned objects. After the call, each `unique_ptr` owns what the other owned. Do not use `std::swap` — implement the exchange with three `std::move`s.",
    r'''#include <memory>
#include <iostream>

// template <typename T> void pointer_swap(std::unique_ptr<T>& a, std::unique_ptr<T>& b)
''',
    [
        ("values-exchange", 'auto a = std::make_unique<int>(1);\nauto b = std::make_unique<int>(2);\npointer_swap(a, b);\nCHECK_EQ(*a, 2);\nCHECK_EQ(*b, 1);', "Three moves: tmp = move(a); a = move(b); b = move(tmp)."),
        ("null-one-side", 'auto a = std::make_unique<int>(5);\nstd::unique_ptr<int> b;\npointer_swap(a, b);\nCHECK_EQ(a == nullptr, true);\nCHECK_EQ(*b, 5);', "Swapping with an empty pointer is legal — ownership moves out."),
    ],
    level="guided",
)

CH_SHARED_COUNTS = challenge(
    "cppi-m8-shared-lifetime",
    "shared_ptr lifetime counters",
    "Implement `struct SharedProbe` with a static `alive()` counter (constructor increments, destructor decrements) and the free function `int probe_lifetimes()` that: creates a `shared_ptr<SharedProbe>`, copies it, lets the copy go out of scope in an inner block, then resets the original — returning `alive()` measured after all of that. Correct code returns 0; the test proves both the copy and the reset released.",
    r'''#include <memory>
#include <iostream>

// struct SharedProbe { static int& alive(); SharedProbe(); ~SharedProbe(); };
// int probe_lifetimes();
''',
    [
        ("everything-released", 'CHECK_EQ(probe_lifetimes(), 0);', "Copy, inner scope, and reset — every owner must release."),
    ],
    level="independent",
)

# ---- checkpoint ----------------------------------------------------------------------
CP_INVENTORY = challenge(
    "cppi-checkpoint-smart-pointers",
    "Checkpoint: Inventory of owned items",
    "Complete `Inventory` managing `std::vector<std::unique_ptr<Item>>`: `void add(std::unique_ptr<Item>)` stores it; `std::unique_ptr<Item> take(const std::string& name)` finds the item, moves it out of the vector (ownership leaves the inventory), erases the now-empty slot, and returns it — or returns `nullptr` when absent. `Item` (name-based) is partially given.",
    r'''#include <memory>
#include <string>
#include <vector>
#include <iostream>

class Item {
public:
    explicit Item(std::string name) : name_{std::move(name)} {}
    const std::string& name() const { return name_; }
private:
    std::string name_;
};

// Complete class Inventory { add, take, size, contains }
''',
    [
        ("take-moves-out", 'Inventory inv;\ninv.add(std::make_unique<Item>("sword"));\nCHECK_EQ(inv.size(), 1);\nauto stolen = inv.take("sword");\nCHECK(stolen != nullptr);\nCHECK_EQ(stolen->name(), std::string("sword"));\nCHECK_EQ(inv.size(), 0);', "take() must std::move the unique_ptr out before erasing the slot."),
        ("absent", 'Inventory inv;\nCHECK(inv.take("ghost") == nullptr);', "Missing name returns an empty unique_ptr."),
        ("still-contains", 'Inventory inv;\ninv.add(std::make_unique<Item>("shield"));\ninv.take("shield");\nCHECK_EQ(inv.contains("shield"), false);', "After take, contains() must report false."),
    ],
    difficulty="intermediate",
)

VI_STACK_PUSH = vi_challenge(
    "Command stack với unique_ptr",
    "Hoàn thiện `CommandStack`: `void push(std::unique_ptr<Command> c)` lưu lệnh bằng cách chuyển giao sở hữu (std::move), và `void run_all()` chạy từng lệnh rồi pop nó. Base `Command` có virtual destructor đã cho. Cài một lớp dẫn xuất `EchoCommand` ghi lại thông điệp khi chạy — test định nghĩa `Recorder` mà EchoCommand phải gọi.",
    [
        ("push-and-run", "push chuyển giao sở hữu; run_all rút cạn stack."),
        ("order-fifo", "std::stack là LIFO khi lưu nhưng run_all có thể duyệt theo thứ tự nào cũng được — thứ tự ghi nhận mới là điều quan trọng."),
        ("moved-in", "Sau std::move, unique_ptr của caller là null."),
    ],
)

VI_SHARED_CYCLES = vi_challenge(
    "observer pattern với weak_ptr",
    "Hoàn thiện `Event`: `void subscribe(std::weak_ptr<void> w)` lưu người theo dõi, và `int fire()` đếm những watcher còn sống, đồng thời xoá các watcher đã hết hạn khỏi danh sách. Đây là observer pattern kinh điển KHÔNG giữ observer sống mãi.",
    [
        ("live-watcher", "Owner còn sống nghĩa là một watcher còn sót lại."),
        ("expired-watcher", "Khi owner chết trong khối scope, fire() không được đếm nó."),
        ("mixed-and-prune", "fire() hai lần: lần đầu cắt tỉa, lần thứ hai vẫn đúng."),
    ],
)

VI_UNIQUE_DANGLING = vi_challenge(
    "Hoán đổi sở hữu giữa hai unique_ptr",
    "Cài `template <typename T> void pointer_swap(std::unique_ptr<T>& a, std::unique_ptr<T>& b)` hoán đổi hai đối tượng đang sở hữu. Sau lời gọi, mỗi `unique_ptr` sở hữu đối tượng của bên kia. Không dùng `std::swap` — hãy tự cài bằng ba lần `std::move`.",
    [
        ("values-exchange", "Ba lần move: tmp = move(a); a = move(b); b = move(tmp)."),
        ("null-one-side", "Hoán đổi với con trỏ rỗng là hợp lệ — sở hữu chuyển ra ngoài."),
    ],
)

VI_SHARED_COUNTS = vi_challenge(
    "Bộ đếm vòng đời shared_ptr",
    "Cài `struct SharedProbe` với bộ đếm tĩnh `alive()` (constructor tăng, destructor giảm) và hàm tự do `int probe_lifetimes()` tạo một `shared_ptr<SharedProbe>`, copy nó, để bản copy chết trong khối trong, rồi reset bản gốc — trả `alive()` sau tất cả. Code đúng trả 0; test chứng minh cả bản copy lẫn reset đều giải phóng.",
    [
        ("everything-released", "Copy, khối trong, reset — mọi owner đều phải giải phóng."),
    ],
)

VI_CP_INVENTORY = vi_challenge(
    "Kiểm tra điểm: Inventory các item sở hữu",
    "Hoàn thiện `Inventory` quản lý `std::vector<std::unique_ptr<Item>>`: `void add(std::unique_ptr<Item>)` lưu item; `std::unique_ptr<Item> take(const std::string& name)` tìm item, move nó ra khỏi vector (quyền sở hữu rời khỏi inventory), xoá slot đã rỗng, và trả về — hoặc trả `nullptr` khi không có. `Item` (dựa trên tên) đã cho một phần.",
    [
        ("take-moves-out", "take() phải std::move unique_ptr ra trước khi xoá slot."),
        ("absent", "Tên không tồn tại trả unique_ptr rỗng."),
        ("still-contains", "Sau take, contains() phải báo false."),
    ],
)

P1 = [CH_STACK_PUSH, CH_SHARED_CYCLES]
VI_P1 = {"cppi-m8-command-stack": VI_STACK_PUSH, "cppi-m8-weak-callbacks": VI_SHARED_CYCLES}
P2 = [CH_UNIQUE_DANGLING, CH_SHARED_COUNTS]
VI_P2 = {"cppi-m8-unique-swap": VI_UNIQUE_DANGLING, "cppi-m8-shared-lifetime": VI_SHARED_COUNTS}

# ---- emit ------------------------------------------------------------------------------
write_lesson(
    MOD, "raii",
    "RAII: The Ownership Idiom",
    "Resources tied to object lifetime — the destructor as the release point, exception-safe by construction.",
    25, L_raii_EN,
    "RAII: idiom sở hữu",
    "Tài nguyên gắn với vòng đời đối tượng — destructor là điểm giải phóng, an toàn ngoại lệ ngay từ thiết kế.",
    L_raii_VI,
)
write_lesson(
    MOD, "unique-ptr",
    "std::unique_ptr: Default Ownership",
    "make_unique, move-only transfer, and the signature discipline of not naming smart pointers in observers.",
    25, L_unique_EN,
    "std::unique_ptr: sở hữu mặc định",
    "make_unique, chuyển giao move-only, và kỷ luật chữ ký: không gọi tên smart pointer trong hàm quan sát.",
    L_unique_VI,
)
write_lesson(
    MOD, "shared-weak",
    "std::shared_ptr and std::weak_ptr",
    "Strong and weak counts, lock() and expiry, the shared-ownership costs, and the reference-cycle trap.",
    30, L_shared_EN,
    "std::shared_ptr và std::weak_ptr",
    "Bộ đếm strong và weak, lock() và hết hạn, chi phí của sở hữu chia sẻ, và bẫy vòng tham chiếu.",
    L_shared_VI,
)
write_lesson(
    MOD, "ownership-design",
    "Choosing the Ownership Model",
    "A decision table from exclusive to value semantics, with a worked Scene/Entity example and signature discipline.",
    25, L_ownership_EN,
    "Chọn mô hình sở hữu",
    "Bảng quyết định từ độc quyền đến ngữ nghĩa giá trị, với ví dụ Scene/Entity và kỷ luật chữ ký.",
    L_ownership_VI,
)

write_practice(
    MOD, "cppi-p8-unique",
    "unique_ptr practice",
    "An ownership-transferring command stack built on std::stack.",
    "Luyện unique_ptr",
    "Command stack chuyển giao sở hữu dựng trên std::stack.",
    "unique-ptr", 35, "intermediate", P1, VI_P1,
    solutions=[
        ("cppi-m8-command-stack", R_STACK_PUSH, W_STACK_PUSH),
        ("cppi-m8-weak-callbacks", R_OBSERVER, W_OBSERVER),
    ],
)
write_practice(
    MOD, "cppi-p8-shared",
    "shared/weak practice",
    "An observer event that prunes expired watchers, plus lifetime probes.",
    "Luyện shared/weak",
    "Event kiểu observer cắt tỉa watcher hết hạn, cộng các probe vòng đời.",
    "shared-weak", 35, "advanced", P2, VI_P2,
    solutions=[
        ("cppi-m8-unique-swap", R_UNIQUE_SWAP, W_UNIQUE_SWAP),
        ("cppi-m8-shared-lifetime", R_SHARED_PROBE, W_SHARED_PROBE),
    ],
)

write_checkpoint(
    MOD, "advanced-checkpoint-smart-pointers",
    "Checkpoint: Ownership Transfer",
    "An Inventory whose take() moves a unique_ptr out of a vector — the exact mechanics of ownership leaving a container.",
    35,
    r"""
`take()` is the exam because it is the precise dance ownership teaches:

1. find the slot by name
2. `auto out = std::move(*it);` — ownership leaves the vector; the slot
   now holds an empty `unique_ptr`
3. `items_.erase(it);` — remove the empty husk
4. return `out`

Skipping step 2 destroys the item; skipping step 3 leaves a nullptr hole
in the container. Both mistakes are silent at compile time — which is why
the tests check size, identity, and containment after the call.

This is the same dance `std::vector::erase`-with-move, node removal in
linked structures, and job queues all perform. Learn it once here and you
will recognize it everywhere.
""",
    "Kiểm tra điểm: Chuyển giao sở hữu",
    "Một Inventory mà take() move unique_ptr ra khỏi vector — đúng cơ chế khiến sở hữu rời khỏi container.",
    r"""
`take()` là bài kiểm tra vì nó là điệu nhảy chính xác mà bài học sở hữu
truyền dạy:

1. tìm slot theo tên
2. `auto out = std::move(*it);` — sở hữu rời vector; slot giờ giữ một
   `unique_ptr` rỗng
3. `items_.erase(it);` — bỏ lớp vỏ rỗng
4. trả `out`

Bỏ bước 2 phá hủy item; bỏ bước 3 để lại lỗ nullptr trong container. Cả
hai lỗi đều im lặng lúc biên dịch — vì vậy test kiểm tra size, danh tính,
và sự tồn tại sau lời gọi.

Đây là điệu nhảy mà erase-trên-vector kèm move, xoá node trong cấu trúc
liên kết, và hàng đợi công việc đều thực hiện. Học một lần ở đây và bạn sẽ
nhận ra nó ở khắp nơi.
""",
    CP_INVENTORY, VI_CP_INVENTORY,
    solution=R_INVENTORY, wrong=W_INVENTORY,
)

write_module(
    MOD,
    "Smart Pointers and RAII",
    "Ownership made explicit: RAII foundations, unique_ptr as default, shared/weak mechanics, and a decision table for picking the model.",
    "Smart pointer và RAII",
    "Sở hữu được làm rõ: nền tảng RAII, unique_ptr làm mặc định, cơ chế shared/weak, và bảng quyết định chọn mô hình.",
    ["raii", "unique-ptr", "shared-weak", "ownership-design", "advanced-checkpoint-smart-pointers"],
    ["cppi-p8-unique", "cppi-p8-shared"],
)
print("module 8 emitted")
