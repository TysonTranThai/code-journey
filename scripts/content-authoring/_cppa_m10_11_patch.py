#!/usr/bin/env python3
"""Instrumentation patches for cppa_m10_11.py: real alloc/comparison counters + freeList_ member."""
P = []


def add(old, new):
    P.append((old, new))


# 1) CP10_BOILER: <vector> include + freeList_ member (solutions reference it)
add(
    "CP10_BOILER = r'''#include <cstddef>\n#include <cstdint>\n",
    "CP10_BOILER = r'''#include <cstddef>\n#include <cstdint>\n#include <vector>\n",
)
add(
    "private:\n    std::size_t blocks_, blockSize_;\n    std::uint8_t* storage_ = nullptr;   // your bookkeeping here\n};\n'''",
    "private:\n    std::size_t blocks_, blockSize_;\n    std::uint8_t* storage_ = nullptr;   // your bookkeeping here\n    std::vector<std::uint8_t*> freeList_;\n};\n'''",
)

# 2) cppa11-reserve-then-build: real allocation counter via operator new replacement
add(
    "        r'''#include <vector>\n\n// Fill out with 1\u00b2, 2\u00b2, \u2026, n\u00b2 using at most ONE allocation.\nvoid squares(std::vector<long long>& out, int n);\n''',\n        [\n            (\"values and single allocation\",\n             r'''extern int allocCount();\nstd::vector<long long> v;\nint before = allocCount();",
    "        r'''#include <cstdlib>\n#include <vector>\n\n// Global allocation counter (each graded test is its own program).\ninline int& gAllocs() { static int n = 0; return n; }\nvoid* operator new(std::size_t sz) { ++gAllocs(); return std::malloc(sz); }\nvoid* operator new[](std::size_t sz) { ++gAllocs(); return std::malloc(sz); }\nvoid operator delete(void* p) noexcept { std::free(p); }\nvoid operator delete[](void* p) noexcept { std::free(p); }\nvoid operator delete(void* p, std::size_t) noexcept { std::free(p); }\nvoid operator delete[](void* p, std::size_t) noexcept { std::free(p); }\ninline int allocCount() { return gAllocs(); }\n\n// Fill out with 1\u00b2, 2\u00b2, \u2026, n\u00b2 using at most ONE allocation.\nvoid squares(std::vector<long long>& out, int n);\n''',\n        [\n            (\"values and single allocation\",\n             r'''std::vector<long long> v;\nint before = allocCount();",
)
add(
    "            (\"large n stays at one allocation\",\n             r'''extern int allocCount();\nstd::vector<long long> v;\nint before = allocCount();",
    "            (\"large n stays at one allocation\",\n             r'''std::vector<long long> v;\nint before = allocCount();",
)

# 3) cppa11-alg-win: Tracked element with a real comparison counter; property becomes <= n
add(
    "        r'''#include <cstdint>\n#include <vector>\n\n// Sum of the distinct values in data.\n// Must not sort and must not compare tracked elements more than n times total\n// (hash-based membership, no element-vs-element comparisons).\nlong long sumUnique(const std::vector<long long>& data);\n''',\n        [\n            (\"correct sums\",\n             r'''CHECK_EQ(sumUnique({1, 2, 3, 2, 1}), 6LL);\nCHECK_EQ(sumUnique({}), 0LL);\nCHECK_EQ(sumUnique({5, 5, 5}), 5LL);\nCHECK_EQ(sumUnique({-1, -1, 2, 3}), 4LL);''',\n             \"Insert everything into std::unordered_set<long long>, then sum the set.\"),\n            (\"no sorting-based comparisons\",\n             r'''extern int trackedComparisons();\nint before = trackedComparisons();\nsumUnique({9, 8, 7, 6, 5, 4, 3, 2, 1, 9, 8});\nCHECK_EQ(trackedComparisons() - before, 0);''',\n             \"unordered_set uses hashing \u2014 element comparisons stay at zero; a sort-based approach compares O(n log n) times and fails.\"),\n        ],",
    "        r'''#include <cstdint>\n#include <vector>\n\n// Elements carry a comparison counter. A hash-based solution compares\n// elements only on duplicate insertion (<= n total); a sort-based one\n// needs O(n log n) comparisons and fails the bound.\nstruct Tracked {\n    long long value;\n    inline static int& comparisons() { static int n = 0; return n; }\n    friend bool operator<(const Tracked& a, const Tracked& b) { ++comparisons(); return a.value < b.value; }\n    friend bool operator==(const Tracked& a, const Tracked& b) { ++comparisons(); return a.value == b.value; }\n};\ntemplate <>\nstruct std::hash<Tracked> {\n    std::size_t operator()(const Tracked& t) const noexcept { return std::hash<long long>{}(t.value); }\n};\ninline int trackedComparisons() { return Tracked::comparisons(); }\n\n// Sum of the distinct values in data.\nlong long sumUnique(const std::vector<Tracked>& data);\n''',\n        [\n            (\"correct sums\",\n             r'''CHECK_EQ(sumUnique({{1}, {2}, {3}, {2}, {1}}), 6LL);\nCHECK_EQ(sumUnique({}), 0LL);\nCHECK_EQ(sumUnique({{5}, {5}, {5}}), 5LL);\nCHECK_EQ(sumUnique({{-1}, {-1}, {2}, {3}}), 4LL);''',\n             \"Insert everything into std::unordered_set<Tracked>, adding t.value when the insert is new.\"),\n            (\"no sorting-based comparisons\",\n             r'''int before = trackedComparisons();\nsumUnique({{9}, {8}, {7}, {6}, {5}, {4}, {3}, {2}, {1}, {9}, {8}});\nCHECK(trackedComparisons() - before <= 11);''',\n             \"unordered_set compares only when a duplicate lands in an occupied bucket \u2014 at most n comparisons; a sort-based approach needs O(n log n) and fails the bound.\"),\n        ],",
)

# solution + wrong for alg-win
add(
    "M11_PRAC2_SOL = [\n    (\"cppa11-alg-win\",\n     r'''#include <cstdint>\n#include <unordered_set>\n#include <vector>\n\nlong long sumUnique(const std::vector<long long>& data) {\n    std::unordered_set<long long> s(data.begin(), data.end());\n    long long sum = 0;\n    for (long long v : s) sum += v;\n    return sum;\n}\n''',\n     r'''#include <cstdint>\n#include <algorithm>\n#include <vector>\n\nlong long sumUnique(const std::vector<long long>& data) {\n    std::vector<long long> v = data;              // WRONG: sorts -> comparisons counted\n    std::sort(v.begin(), v.end());\n    v.erase(std::unique(v.begin(), v.end()), v.end());\n    long long sum = 0;\n    for (long long x : v) sum += x;\n    return sum;\n}\n'''),\n]",
    "M11_PRAC2_SOL = [\n    (\"cppa11-alg-win\",\n     r'''#include <cstdint>\n#include <unordered_set>\n#include <vector>\n\nlong long sumUnique(const std::vector<Tracked>& data) {\n    std::unordered_set<Tracked> s;\n    long long sum = 0;\n    for (const Tracked& t : data) {\n        if (s.insert(t).second) sum += t.value;\n    }\n    return sum;\n}\n''',\n     r'''#include <cstdint>\n#include <algorithm>\n#include <vector>\n\nlong long sumUnique(const std::vector<Tracked>& data) {\n    std::vector<Tracked> v = data;              // WRONG: sorts -> comparisons blow the bound\n    std::sort(v.begin(), v.end());\n    v.erase(std::unique(v.begin(), v.end()), v.end());\n    long long sum = 0;\n    for (const Tracked& t : v) sum += t.value;\n    return sum;\n}\n'''),\n]",
)

# 4) CP11 checkpoint: same instruments
add(
    "        r'''#include <cstdint>\n#include <vector>\n\n// (1) out gets 0..n-1 with at most one allocation.\nvoid buildRange(std::vector<int>& out, int n);\n\n// (2) number of distinct values; no element-vs-element comparisons allowed.\nint countDistinct(const std::vector<int>& data);\n''',\n        [\n            (\"buildRange: one allocation, right values\",\n             r'''extern int allocCount();\nstd::vector<int> v;\nint before = allocCount();",
    "        r'''#include <cstdint>\n#include <cstdlib>\n#include <vector>\n\n// Allocation counter (each graded test is its own program).\ninline int& gAllocs() { static int n = 0; return n; }\nvoid* operator new(std::size_t sz) { ++gAllocs(); return std::malloc(sz); }\nvoid* operator new[](std::size_t sz) { ++gAllocs(); return std::malloc(sz); }\nvoid operator delete(void* p) noexcept { std::free(p); }\nvoid operator delete[](void* p) noexcept { std::free(p); }\nvoid operator delete(void* p, std::size_t) noexcept { std::free(p); }\nvoid operator delete[](void* p, std::size_t) noexcept { std::free(p); }\ninline int allocCount() { return gAllocs(); }\n\n// Comparison-counted element (see module 11 practice).\nstruct Tracked {\n    long long value;\n    inline static int& comparisons() { static int n = 0; return n; }\n    friend bool operator<(const Tracked& a, const Tracked& b) { ++comparisons(); return a.value < b.value; }\n    friend bool operator==(const Tracked& a, const Tracked& b) { ++comparisons(); return a.value == b.value; }\n};\ntemplate <>\nstruct std::hash<Tracked> {\n    std::size_t operator()(const Tracked& t) const noexcept { return std::hash<long long>{}(t.value); }\n};\ninline int trackedComparisons() { return Tracked::comparisons(); }\n\n// (1) out gets 0..n-1 with at most one allocation.\nvoid buildRange(std::vector<int>& out, int n);\n\n// (2) number of distinct values; hash-based membership keeps comparisons <= n.\nint countDistinct(const std::vector<Tracked>& data);\n''',\n        [\n            (\"buildRange: one allocation, right values\",\n             r'''std::vector<int> v;\nint before = allocCount();",
)
add(
    "            (\"countDistinct: hash, don't compare\",\n             r'''extern int trackedComparisons();\nint before = trackedComparisons();\nCHECK_EQ(countDistinct({1, 2, 2, 3, 3, 3}), 3);\nCHECK_EQ(trackedComparisons() - before, 0);\nCHECK_EQ(countDistinct({}), 0);''',\n             \"std::unordered_set<int> s(data.begin(), data.end()); return (int)s.size();\"),",
    "            (\"countDistinct: hash, don't compare\",\n             r'''int before = trackedComparisons();\nCHECK_EQ(countDistinct({{1}, {2}, {2}, {3}, {3}, {3}}), 3);\nCHECK(trackedComparisons() - before <= 6);\nCHECK_EQ(countDistinct({}), 0);''',\n             \"std::unordered_set<Tracked> s; insert each element; return (int)s.size();\"),",
)

add(
    "    solution=r'''#include <cstdint>\n#include <unordered_set>\n#include <vector>\n\nvoid buildRange(std::vector<int>& out, int n) {\n    out.reserve(n);\n    for (int i = 0; i < n; ++i) out.push_back(i);\n}\nint countDistinct(const std::vector<int>& data) {\n    std::unordered_set<int> s(data.begin(), data.end());\n    return static_cast<int>(s.size());\n}\n''',",
    "    solution=r'''#include <cstdint>\n#include <unordered_set>\n#include <vector>\n\nvoid buildRange(std::vector<int>& out, int n) {\n    out.reserve(n);\n    for (int i = 0; i < n; ++i) out.push_back(i);\n}\nint countDistinct(const std::vector<Tracked>& data) {\n    std::unordered_set<Tracked> s;\n    for (const Tracked& t : data) s.insert(t);\n    return static_cast<int>(s.size());\n}\n''',",
)
add(
    "    wrong=r'''#include <cstdint>\n#include <algorithm>\n#include <vector>\n\nvoid buildRange(std::vector<int>& out, int n) {\n    for (int i = 0; i < n; ++i) out.push_back(i);   // WRONG: no reserve\n}\nint countDistinct(const std::vector<int>& data) {\n    std::vector<int> v = data;                       // WRONG: sort-based -> comparisons counted\n    std::sort(v.begin(), v.end());\n    v.erase(std::unique(v.begin(), v.end()), v.end());\n    return static_cast<int>(v.size());\n}\n''',",
    "    wrong=r'''#include <cstdint>\n#include <algorithm>\n#include <vector>\n\nvoid buildRange(std::vector<int>& out, int n) {\n    for (int i = 0; i < n; ++i) out.push_back(i);   // WRONG: no reserve\n}\nint countDistinct(const std::vector<Tracked>& data) {\n    std::vector<Tracked> v = data;                  // WRONG: sort-based -> comparisons blow the bound\n    std::sort(v.begin(), v.end());\n    v.erase(std::unique(v.begin(), v.end()), v.end());\n    return static_cast<int>(v.size());\n}\n''',",
)

for i, (old, new) in enumerate(P, 1):
    c = src.count(old) if (src := open("cppa_m10_11.py").read()) else None
    # read fresh each patch is wasteful; instead read once below
    break

src = open("cppa_m10_11.py").read()
for i, (old, new) in enumerate(P, 1):
    c = src.count(old)
    assert c == 1, f"patch {i}: count={c}"
    src = src.replace(old, new)
open("cppa_m10_11.py", "w").write(src)
print(f"all {len(P)} instrumentation patches applied")
