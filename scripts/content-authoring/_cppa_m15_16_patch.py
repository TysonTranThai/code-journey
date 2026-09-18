#!/usr/bin/env python3
"""Fix m15_16 tests: no nested main(), real config-guards battery, no sign-compare."""
import glob
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MAIN = "\nint main() { return 0; }"

# 1) Script source of truth -------------------------------------------------
p = "cppa_m15_16.py"
src = open(p).read()
n0 = src.count(MAIN)
src = src.replace(MAIN, "")

# config-guards pseudo-test -> real single-TU proof battery
old_test = '''        [
            ("capability markers, not compiler sniffing",
             r\'\'\'// has_format must key on __cpp_lib_format, not on _MSC_VER/__GNUC__.
#if !defined(__cpp_lib_format)
STATIC_ASSERT_FALSE_FMT
#endif
STATIC_ASSERT_HAS_FORMAT_GUARD\'\'\','''
new_test = '''        [
            ("capability markers, not compiler sniffing",
             r\'\'\'static_assert(buildcfg::has_format() == (bool)__cpp_lib_format,
              "has_format must mirror __cpp_lib_format exactly");
static_assert(buildcfg::exceptions_enabled() ==
              (bool)(__cpp_exceptions || __EXCEPTIONS),
              "exceptions_enabled must match this TU");
static_assert(!buildcfg::asserts_disabled(), "NDEBUG is not defined in this TU");
static_assert(!buildcfg::asan_active(), "no sanitizer in this TU");
static_assert(buildcfg::log_level() == 0, "default log level is 0");
CHECK(buildcfg::has_format() || !__cpp_lib_format);\'\'\','''
assert src.count(old_test) == 1, f"old_test count {src.count(old_test)}"
src = src.replace(old_test, new_test)

# sign-compare in pimpl battery: w4.size() vs int literal 2
old_cmp = "CHECK_EQ(w4.size(), 2);"
new_cmp = "CHECK_EQ(w4.size(), std::size_t{2});"
assert src.count(old_cmp) == 1, f"cmp count {src.count(old_cmp)}"
src = src.replace(old_cmp, new_cmp)

open(p, "w").write(src)
print(f"script fixed ({n0} main() removed)")

# 2) On-disk challenge JSONs ------------------------------------------------
ROOT = os.path.join("..", "..")
BASE = os.path.join(ROOT, "src/content/tracks/cpp/courses/cpp-advanced/modules")


def patch_json(path, fixes):
    d = json.load(open(path))
    changed = False
    for t in d["tests"]:
        code = t.get("code", "")
        new = code
        new = new.replace(MAIN, "")
        for old, nu in fixes:
            new = new.replace(old, nu)
        if new != code:
            t["code"] = new
            changed = True
    if changed:
        json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
        print("patched", os.path.relpath(path, ROOT))


fixes = {
    "cppa15-config-guards": [
        ('''// has_format must key on __cpp_lib_format, not on _MSC_VER/__GNUC__.
#if !defined(__cpp_lib_format)
STATIC_ASSERT_FALSE_FMT
#endif
STATIC_ASSERT_HAS_FORMAT_GUARD''',
         '''static_assert(buildcfg::has_format() == (bool)__cpp_lib_format,
              "has_format must mirror __cpp_lib_format exactly");
static_assert(buildcfg::exceptions_enabled() ==
              (bool)(__cpp_exceptions || __EXCEPTIONS),
              "exceptions_enabled must match this TU");
static_assert(!buildcfg::asserts_disabled(), "NDEBUG is not defined in this TU");
static_assert(!buildcfg::asan_active(), "no sanitizer in this TU");
static_assert(buildcfg::log_level() == 0, "default log level is 0");
CHECK(buildcfg::has_format() || !__cpp_lib_format);'''),
    ],
    "cppa15-build-checkpoint": [],
    "cppa16-pimpl-discipline": [("CHECK_EQ(w4.size(), 2);", "CHECK_EQ(w4.size(), std::size_t{2});")],
}

for path in glob.glob(os.path.join(BASE, "build-systems", "**", "*.json"), recursive=True) + \
            glob.glob(os.path.join(BASE, "abi-linking", "**", "*.json"), recursive=True):
    d = json.load(open(path))
    cid = d.get("id")
    if cid in fixes:
        patch_json(path, fixes[cid])

print("done")
