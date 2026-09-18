#!/usr/bin/env python3
"""Final repair for cb_m18_19.py: rebuild the six broken solution-source lines
(registry R/W, format R/W, pipeline solution/wrong) with correct single
backslash escapes and the right content. Then normalize the mangled
join at the end of the checkpoint block."""
import ast

BS = chr(92)
NL = BS + "n"  # file bytes for \n inside a Python string literal


def cc(*parts):
    return NL.join(parts)


P = "cb_m18_19.py"
lines = open(P, encoding="utf-8").read().split("\n")

R_REG = [
    "#include <stdio.h>",
    "#include <string.h>",
    "#define RCAP 16",
    "static char names[RCAP][32];",
    "static int ncount = 0;",
    "void reg_clear(void) { ncount = 0; }",
    "int reg_has(const char *name) {",
    "    if (name == NULL) return 0;",
    "    for (int i = 0; i < ncount; i++)",
    "        if (strcmp(names[i], name) == 0) return 1;",
    "    return 0;",
    "}",
    "int reg_add(const char *name) {",
    "    if (name == NULL || ncount == RCAP) return 0;",
    "    if (reg_has(name)) return 0;",
    "    strcpy(names[ncount], name);",
    "    ncount++;",
    "    return 1;",
    "}",
    "int reg_count(void) { return ncount; }",
    "int main(void) { return 0; }",
]

W_REG = [
    "#include <stdio.h>",
    "#include <string.h>",
    "#define RCAP 16",
    "static char names[RCAP][32];",
    "static int ncount = 0;",
    "void reg_clear(void) { ncount = 0; }",
    "int reg_has(const char *name) {",
    "    if (name == NULL) return 0;",
    "    for (int i = 0; i < ncount; i++)",
    "        if (strcmp(names[i], name) == 0) return 1;",
    "    return 0;",
    "}",
    "int reg_add(const char *name) {",
    "    if (name == NULL || ncount == RCAP) return 0;",
    "    strcpy(names[ncount], name);",
    "    ncount++;",
    "    return 1;",
    "}",
    "int reg_count(void) { return ncount; }",
    "int main(void) { return 0; }",
]

R_FMT = [
    "#include <stdio.h>",
    "void format_price(double p, char *out) {",
    '    snprintf(out, 32, "price=%g", p);',
    "}",
    "int main(void) { return 0; }",
]

W_FMT = [
    "#include <stdio.h>",
    "void format_price(double p, char *out) {",
    '    snprintf(out, 32, "price=%d", p);',
    "}",
    "int main(void) { return 0; }",
]

R_PIPE = [
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
]

W_PIPE = [
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
]

fixed = 0

# 1) the solutions tuple entries: '"cb18-registry-module",' / '"cb19-fix-format",'
#    followed by two single-quoted lines
for i, ln in enumerate(lines):
    if ln in ('            "cb18-registry-module",', '            "cb19-fix-format",') and lines[i + 1].lstrip().startswith("'"):
        cid = ln.strip().strip('",')
        r, w = (R_REG, W_REG) if "registry" in cid else (R_FMT, W_FMT)
        lines[i + 1] = "            '" + cc(*r) + "',"
        lines[i + 2] = "            '" + cc(*w) + "',"
        fixed += 1

# 2) the checkpoint kwargs: a line starting "    ),    solution='..." (mangled join)
for i, ln in enumerate(lines):
    if "    solution='" in ln and "),    solution=" in ln:
        head, rest = ln.split("    solution=", 1)
        lines[i] = head.rstrip() + "\n    solution='" + cc(*R_PIPE) + "',"
        # next line is wrong='...'
        if lines[i + 1].startswith("    wrong='"):
            lines[i + 1] = "    wrong='" + cc(*W_PIPE) + "',"
        fixed += 1

src = "\n".join(lines)

# 3) normalize any leftover mangled joins like '),    C_PRELUDE,' variants
src = src.replace("    ),    solution=", "    ),\n    solution=")

open(P, "w", encoding="utf-8").write(src)
ast.parse(src)
print(f"rebuilt {fixed} line groups; syntax ok")
