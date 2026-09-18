#!/usr/bin/env python3
"""Structural repair for cb_m18_19.py (round 2).

1. Restore the registry challenge's title/prompt lines (mangled by round 1).
2. Swap reg_add/reg_has definition order inside the remaining single-quoted
   solution strings (C23 forbids implicit declarations).
3. Rewrite cb19-fix-format and cb19-checkpoint-pipeline to test printed output
   through caller buffers (snprintf), since the runtime has no lambda-capture
   helper usable from injected test code.
"""
import re

BS = chr(92)
NL2 = BS + BS + "n"   # the two chars \n as they must appear inside .py string literals


def cc(*parts):
    """Join C source lines into the two-char-escape form used in .py literals."""
    return NL2.join(parts)


P = "cb_m18_19.py"
lines = open(P, encoding="utf-8").read().split("\n")

# ---- 1. restore registry title/prompt -------------------------------------
for i, ln in enumerate(lines):
    if ln == '            "cb18-registry-module",' and lines[i + 1].lstrip().startswith("'"):
        lines[i + 1] = '            "Name Registry",'
        lines[i + 2] = (
            '            "Build a registry of up to 16 names: private storage, public '
            '`int reg_add(const char *name)` (1 = added, 0 = full or NULL), '
            '`int reg_has(const char *name)` (1 if present), `int reg_count(void)`.",'
        )
        print("registry title/prompt restored")
        break

src = "\n".join(lines)

# ---- 2. swap reg_add before reg_has -> reg_has before reg_add --------------
pat = re.compile(
    r"\\nint reg_add\(const char \*name\) \{(.*?)\\n\}\\n"
    r"int reg_has\(const char \*name\) \{(.*?)\\n\}\\n"
)


def swap(m):
    add_body, has_body = m.group(1), m.group(2)
    return (
        NL2 + "int reg_has(const char *name) {" + has_body + NL2 + "}" + NL2
        + "int reg_add(const char *name) {" + add_body + NL2 + "}" + NL2
    )


src, nswap = pat.subn(swap, src)
print(f"definition-order swaps: {nswap}")

# ---- 3. rewrite cb19-fix-format challenge block ----------------------------
new_format_block = """        challenge(
            "cb19-fix-format",
            "Fix: Wrong Format Specifier",
            "Implement `void format_price(double p, char *out)` writing `price=<value>` into out with snprintf, where <value> uses printf's %g formatting for the double. The classic bug is %d with a double — yours must be correct.",
            "#include <stdio.h>\\n",
            [
                ("basic", "char buf[32] = {0};\\nformat_price(12.5, buf);\\nCHECK_STR_EQ(buf, \\"price=12.5\\");", "snprintf(out, 32, \\"price=%g\\", p)."),
                ("integer valued", "char buf[32] = {0};\\nformat_price(7.0, buf);\\nCHECK_STR_EQ(buf, \\"price=7\\");", "%g drops the trailing .0."),
                ("longer", "char buf[32] = {0};\\nformat_price(1234.5, buf);\\nCHECK_STR_EQ(buf, \\"price=1234.5\\");", "Bigger values too."),
            ],
            level="guided",
        ),"""

m = re.search(r'        challenge\(\n            "cb19-fix-format",.*?level="guided",\n        \),', src, re.S)
assert m, "format challenge block not found"
src = src[: m.start()] + new_format_block + src[m.end():]
print("cb19-fix-format block rewritten")

# its VI entry
new_format_vi = """        "cb19-fix-format": vi_challenge(
            "Sửa: Định dạng sai kiểu",
            "Cài `void format_price(double p, char *out)` ghi `price=<giá trị>` vào out bằng snprintf, với <giá trị> dùng định dạng %g của printf cho double. Lỗi kinh điển là %d với double — bản của bạn phải đúng.",
            [("cơ bản", "snprintf(out, 32, \\"price=%g\\", p)."), ("giá trị nguyên", "%g bỏ phần .0 cuối."), ("dài hơn", "Giá trị lớn hơn cũng vậy.")],
        ),"""
m = re.search(r'        "cb19-fix-format": vi_challenge\(.*?\),', src, re.S)
assert m, "format VI not found"
src = src[: m.start()] + new_format_vi + src[m.end():]
print("cb19-fix-format VI rewritten")

# its solutions tuple: find '"cb19-fix-format",' followed by two single-quoted lines
fl = src.split("\n")
for i, ln in enumerate(fl):
    if ln == '            "cb19-fix-format",' and fl[i + 1].lstrip().startswith("'"):
        r = cc(
            "#include <stdio.h>",
            "void format_price(double p, char *out) {",
            '    snprintf(out, 32, "price=%g", p);',
            "}",
            "int main(void) { return 0; }",
        )
        w = cc(
            "#include <stdio.h>",
            "void format_price(double p, char *out) {",
            '    snprintf(out, 32, "price=%d", p);',
            "}",
            "int main(void) { return 0; }",
        )
        fl[i + 1] = "            '" + r + "',"
        fl[i + 2] = "            '" + w + "',"
        print("cb19-fix-format solution pair rebuilt")
        break
src = "\n".join(fl)

# ---- 4. rewrite cb19-checkpoint-pipeline -----------------------------------
new_pipe_prompt = (
    '        "Fix all three defects in the pipeline below: (1) `avg` must not use integer division, '
    '(2) `max_of` must handle n == 1 correctly (start from a[0]), (3) `report(const int *a, int n, char *out)` '
    'must write `n=<n> avg=<g> max=<g>` into out with snprintf (%g for the doubles). '
    'Reference: report({2, 4}, 2, buf) makes buf `n=2 avg=3 max=4`.\\n\\n'
    "```c\\ndouble avg(const int *a, int n) {\\n    int s = 0;\\n    for (int i = 0; i < n; i++) s += a[i];\\n"
    "    return s / n;          /* BUG: integer division */\\n}\\n"
    "int max_of(const int *a, int n) {\\n    int m;\\n    for (int i = 1; i < n; i++)\\n"
    "        if (a[i] > m) m = a[i];   /* BUG: m uninitialized */\\n    return m;\\n}\\n"
    'void report(const int *a, int n, char *out) {\\n    printf("n=%d avg=%g max=%g\\\\n", n, avg(a, n), (double)max_of(a, n));  /* BUG: prints, ignores out */\\n}\\n```",'
)
m = re.search(r'        "Fix all three defects in the pipeline below:.*?",\n', src, re.S)
assert m, "pipeline prompt not found"
src = src[: m.start()] + new_pipe_prompt + src[m.end():]
print("pipeline prompt rewritten")

# the report-format test inside the checkpoint
old_test = '("report format", "int a[] = {2, 4};\\nCHECK_CONTAINS(capture_printf(() -> report(a, 2)), \\"n=2 avg=3 max=4\\");", "avg prints 3 (as %g), max prints 4."),'
new_test = '("report format", "int a[] = {2, 4};\\nchar buf[64] = {0};\\nreport(a, 2, buf);\\nCHECK_STR_EQ(buf, \\"n=2 avg=3 max=4\\");", "snprintf(out, 64, \\"n=%d avg=%g max=%g\\", n, avg(a, n), (double)max_of(a, n))."),'
assert old_test in src, "report test not found"
src = src.replace(old_test, new_test)
print("report-format test rewritten")

# pipeline VI
new_pipe_vi = """    vi_challenge(
        "Vá đường ống báo cáo",
        "Sửa cả ba lỗi trong đường ống dưới đây: (1) `avg` không được dùng chia số nguyên, (2) `max_of` phải xử lý đúng n == 1 (bắt đầu từ a[0]), (3) `report(const int *a, int n, char *out)` phải ghi `n=<n> avg=<g> max=<g>` vào out bằng snprintf (%g cho các double). Tham chiếu: report({2, 4}, 2, buf) làm buf thành `n=2 avg=3 max=4`.",
        [("avg kiểu double", "(double)s / n."), ("max một phần tử", "Bắt đầu m từ a[0]."), ("định dạng report", "snprintf với n=%d avg=%g max=%g.")],
    ),"""
m = re.search(r'    vi_challenge\(\n        "Vá đường ống báo cáo",.*?\),\n', src, re.S)
assert m, "pipeline VI not found"
src = src[: m.start()] + new_pipe_vi + src[m.end():]
print("pipeline VI rewritten")

# pipeline solution/wrong kwargs
r_pipe = cc(
    "#include <stdio.h>",
    "double avg(const int *a, int n) {",
    "    int s = 0;",
    "    for (int i = 0; i < n; i++) s += a[i];",
    "    return (double)s / n;",
    "}",
    "int max_of(const int *a, int n) {",
    "    int m = a[0];",
    "    for (int i = 1; i < n; i++)",
    "        if (a[i] > m) m = a[i];",
    "    return m;",
    "}",
    "void report(const int *a, int n, char *out) {",
    '    snprintf(out, 64, "n=%d avg=%g max=%g", n, avg(a, n), (double)max_of(a, n));',
    "}",
    "int main(void) { return 0; }",
)
w_pipe = cc(
    "#include <stdio.h>",
    "double avg(const int *a, int n) {",
    "    int s = 0;",
    "    for (int i = 0; i < n; i++) s += a[i];",
    "    return s / n;",
    "}",
    "int max_of(const int *a, int n) {",
    "    int m = a[0];",
    "    for (int i = 1; i < n; i++)",
    "        if (a[i] > m) m = a[i];",
    "    return m;",
    "}",
    "void report(const int *a, int n, char *out) {",
    '    snprintf(out, 64, "n=%d avg=%g max=%g", n, avg(a, n), (double)max_of(a, n));',
    "}",
    "int main(void) { return 0; }",
)
pl = src.split("\n")
for i, ln in enumerate(pl):
    if ln.startswith("    solution='#include <stdio.h>") and "avg(const int *a" in ln:
        pl[i] = "    solution='" + r_pipe + "',"
        # wrong= is the next line
        pl[i + 1] = "    wrong='" + w_pipe + "',"
        print("pipeline solution/wrong rebuilt")
        break
src = "\n".join(pl)

open(P, "w", encoding="utf-8").write(src)
import ast
ast.parse(src)
print("patch complete, syntax ok")
