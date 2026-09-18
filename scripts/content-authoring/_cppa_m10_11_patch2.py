#!/usr/bin/env python3
"""Fix module 10-11: prefix module-11 solutions with boilerplate, fix pmr-arena tests, strengthen W."""
P = []


def add(old, new):
    P.append((old, new))


# --- A) pmr-arena: p2 must be 16-aligned too; drop used()==20 (padding-dependent) ---
add(
    "CHECK(static_cast<std::uint8_t*>(p2) >= static_cast<std::uint8_t*>(p1) + 10);\nCHECK_EQ(reinterpret_cast<std::uintptr_t>(p1) % 16, 0u);\nCHECK_EQ(a.used(), 20u);''',",
    "CHECK(static_cast<std::uint8_t*>(p2) >= static_cast<std::uint8_t*>(p1) + 10);\nCHECK_EQ(reinterpret_cast<std::uintptr_t>(p1) % 16, 0u);\nCHECK_EQ(reinterpret_cast<std::uintptr_t>(p2) % 16, 0u);\nCHECK_GE(a.used(), 20u);''',",
)
add(
    '"Round offset up to the next multiple of 16, return buf_ + offset, then advance offset by n."),',
    '"Round the offset up to the next multiple of 16 (padding counts toward used()), return buf_ + offset, advance offset by n."),',
)

# --- B) pmr-arena W: only fails the fit test when padding is in play; make it deterministically wrong ---
add(
    "void* Arena::carve(std::size_t n) {\n    if (offset_ + n > bytes_) return nullptr;   // WRONG: no 16-byte alignment\n    void* p = buf_ + offset_;\n    offset_ += n;\n    return p;\n}",
    "void* Arena::carve(std::size_t n) {\n    void* p = buf_ + offset_;\n    offset_ += n + 16;   // WRONG: no alignment AND overcounts every carve\n    return p;\n}",
)

# --- C) module-11 solutions/wrongs: prefix with the challenge boilerplate so Tracked/allocCount are declared ---
add(
    'M11_PRAC1_SOL = [\n    ("cppa11-reserve-then-build",\n     r\'\'\'#include <vector>\n\nvoid squares',
    'M11_PRAC1_SOL = [\n    ("cppa11-reserve-then-build",\n     M11_PRAC1_CH[0]["boilerplate"] + r\'\'\'void squares',
)
add(
    "     r'''#include <vector>\n\nvoid squares(std::vector<long long>& out, int n) {\n    for (int i = 1; i <= n; ++i) out.push_back(1LL * i * i);  // WRONG: no reserve\n}\n'''),",
    "     M11_PRAC1_CH[0][\"boilerplate\"] + r'''void squares(std::vector<long long>& out, int n) {\n    for (int i = 1; i <= n; ++i) out.push_back(1LL * i * i);  // WRONG: no reserve\n}\n'''),",
)
add(
    'M11_PRAC2_SOL = [\n    ("cppa11-alg-win",\n     r\'\'\'#include <cstdint>\n#include <unordered_set>\n#include <vector>\n\nlong long sumUnique',
    'M11_PRAC2_SOL = [\n    ("cppa11-alg-win",\n     M11_PRAC2_CH[0]["boilerplate"] + r\'\'\'long long sumUnique',
)
add(
    "     r'''#include <cstdint>\n#include <algorithm>\n#include <vector>\n\nlong long sumUnique(const std::vector<Tracked>& data) {\n    std::vector<Tracked> v = data;              // WRONG: sorts -> comparisons blow the bound\n    std::sort(v.begin(), v.end());",
    "     M11_PRAC2_CH[0][\"boilerplate\"] + r'''long long sumUnique(const std::vector<Tracked>& data) {\n    std::vector<Tracked> v = data;              // WRONG: sorts -> comparisons blow the bound\n    std::sort(v.begin(), v.end());",
)
add(
    "    solution=r'''#include <cstdint>\n#include <unordered_set>\n#include <vector>\n\nvoid buildRange",
    '    solution=CP11_CH.boilerplate + r\'\'\'void buildRange',
)
add(
    "    wrong=r'''#include <cstdint>\n#include <algorithm>\n#include <vector>\n\nvoid buildRange",
    '    wrong=CP11_CH.boilerplate + r\'\'\'void buildRange',
)

# --- D) name the CP11 challenge so solutions can reference its boilerplate ---
add(
    '    challenge(\n        "cppa11-perf-checkpoint",',
    '    CP11_CH = challenge(\n        "cppa11-perf-checkpoint",',
)

# --- E) hint texts for the new pmr-arena W ---
add(
    "reset() sets offset_ back to 0 \u2014 carve succeeds again after reset.",
    "reset() sets offset_ back to 0 \u2014 carve succeeds again after reset. The alignment rule: round the offset up to a multiple of 16 BEFORE handing out the pointer.",
)

for i, (old, new) in enumerate(P, 1):
    src = open("cppa_m10_11.py").read()
    c = src.count(old)
    assert c == 1, f"patch {i}: count={c}"
    src = src.replace(old, new)
    open("cppa_m10_11.py", "w").write(src)
print(f"all {len(P)} patches applied")
