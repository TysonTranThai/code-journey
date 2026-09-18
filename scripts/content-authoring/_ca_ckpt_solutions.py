#!/usr/bin/env python3
"""Append R/W ledger lines for the five authored checkpoint challenges.

Generated via Python so every backslash and quote is exact. R passes every
test; W fails at least one test per challenge (two-sided contract).
"""
import os

NL = chr(10)
BSL = chr(92)
Q = '"'

P = "scripts/content-authoring/ca-solutions.mjs"


def esc(s):
    out = []
    for ch in s:
        if ch == BSL:
            out.append(BSL + BSL)
        elif ch == Q:
            out.append(BSL + Q)
        elif ch == NL:
            out.append(BSL + "n")
        else:
            out.append(ch)
    return Q + "".join(out) + Q


def cline(*lines):
    return NL.join(lines)


def emit(key, r_src, w_src):
    return (
        "R[" + esc(key) + "] = " + esc(r_src) + ";" + NL
        + "W[" + esc(key) + "] = " + esc(w_src) + ";" + NL
    )


lines_out = []

# ---- m7: penalty model + chooser --------------------------------------------
r7 = cline(
    "#include <stdio.h>",
    "#include <string.h>",
    "#include <stdlib.h>",
    "static int ceil_log2_(int n) { int s = 0; while ((1 << s) < n) s++; return s; }",
    "int structure_penalty(int n_ops, int lookups, int inserts) { return lookups * n_ops + inserts; }",
    "int sorted_penalty(int n_ops, int lookups, int inserts) { return lookups * ceil_log2_(n_ops) + inserts * n_ops; }",
    "const char *choose(int lookups, int inserts) { return lookups >= inserts ? " + Q + "hash" + Q + " : " + Q + "sorted" + Q + "; }",
    "int main(void) { return 0; }",
)
w7 = r7.replace(
    "static int ceil_log2_(int n) { int s = 0;",
    "static int ceil_log2_(int n) { int s = 1;",
)
lines_out.append(emit("ca7-checkpoint-select", r7, w7))

# ---- m9: function-vs-macro evaluation discipline -----------------------------
common9 = cline(
    "#include <stdio.h>",
    "#include <stdbool.h>",
    "#include <string.h>",
    "#include <stdlib.h>",
    "#define IS_POWER2(n) ((n) > 0 && ((n) & ((n) - 1)) == 0)",
    "#define CAT2(a, b) a##b",
    "#define CAT(a, b) CAT2(a, b)",
    "static int g_calls = 0;",
    "static int side(void) { g_calls++; return 100; }",
)
r9 = common9 + NL + cline(
    "static int ca9hello(void) { return 42; }",
    "int max_of(int a, int b) { return a > b ? a : b; }",
    "int safe_max_probe(void) { int r = max_of(side(), 4); return (r == 100 && g_calls == 1) ? 1 : 0; }",
    "int eval_count(void) { return g_calls; }",
    "int main(void) { return 0; }",
)
# W: max_of as the classic macro -> side() evaluates twice when it wins.
w9 = common9 + NL + cline(
    "static int ca9hello(void) { return 42; }",
    "#define max_of(a, b) ((a) > (b) ? (a) : (b))",
    "int safe_max_probe(void) { int r = max_of(side(), 4); return (r == 100 && g_calls == 1) ? 1 : 0; }",
    "int eval_count(void) { return g_calls; }",
    "int main(void) { return 0; }",
)
lines_out.append(emit("ca9-checkpoint-guarded", r9, w9))

# ---- m11: symbol classification + link-order rule ----------------------------
r11 = cline(
    "#include <stdio.h>",
    "#include <string.h>",
    "#include <ctype.h>",
    "char sym_class(const char *line) {",
    "    const char *p = line;",
    "    while (isspace((unsigned char)*p)) p++;",
    "    int digits = 0;",
    "    while (isdigit((unsigned char)p[digits])) digits++;",
    "    if (digits >= 2) { const char *q = p + digits; while (*q == 32) q++; return *q; }",
    "    return *p;",
    "}",
    "int linker_resolves(const char *order) {",
    "    int seen_plain = 0;",
    "    for (const char *p = order; *p; p++) {",
    "        if (*p == 80) seen_plain = 1;",
    "        else if (*p == 65 && seen_plain) return 1;",
    "    }",
    "    return 0;",
    "}",
    "int main(void) { return 0; }",
)
w11 = r11.replace(
    "    int seen_plain = 0;",
    "    int seen_plain = 0; int saw_archive = 0;",
).replace(
    "        if (*p == 80) seen_plain = 1;",
    "        if (*p == 80) { if (saw_archive) return 1; }",
).replace(
    "        else if (*p == 65 && seen_plain) return 1;",
    "        else if (*p == 65) saw_archive = 1;",
)
lines_out.append(emit("ca11-checkpoint-symbols", r11, w11))

# ---- m13: emitted-form predicates --------------------------------------------
r13 = cline(
    "#include <stdio.h>",
    "#include <string.h>",
    "#include <stdlib.h>",
    "int emitted_ops_sum(int n) { long long s = (long long)n * (n + 1) / 2; return (int)s; }",
    "int strength_steps(int n) { if (n <= 1) return 0; int steps = 0; int left = n; while (left > 1) { left /= 2; steps++; } return steps + 1; }",
    "int would_elide(int pure, int calls, int observed) { return observed ? calls * pure : 0; }",
    "int main(void) { return 0; }",
)
w13 = cline(
    "#include <stdio.h>",
    "#include <string.h>",
    "#include <stdlib.h>",
    "int emitted_ops_sum(int n) { long long s = (long long)n * (n + 1) / 2; return (int)s; }",
    "int strength_steps(int n) { if (n <= 1) return 0; int steps = 0; int left = n; while (left > 1) { left /= 2; steps++; } return steps; }",
    "int would_elide(int pure, int calls, int observed) { return calls * pure; }",
    "int main(void) { return 0; }",
)
lines_out.append(emit("ca13-checkpoint-emitted", r13, w13))

# ---- m16: ownership ledger (W: live() overcounts) ----------------------------
r16 = cline(
    "#include <stdio.h>",
    "#include <stdbool.h>",
    "#include <string.h>",
    "#include <stdlib.h>",
    "#define LEDGER_CAP 8",
    "typedef struct { int ids[LEDGER_CAP]; int count; } ledger_t;",
    "void ledger_init(ledger_t *lg) { memset(lg, 0, sizeof *lg); }",
    "int ledger_acquire(ledger_t *lg, int id) { for (int i = 0; i < lg->count; i++) if (lg->ids[i] == id) return 0; if (lg->count >= LEDGER_CAP) return -1; lg->ids[lg->count++] = id; return 1; }",
    "int ledger_release(ledger_t *lg, int id) { for (int i = 0; i < lg->count; i++) if (lg->ids[i] == id) { lg->ids[i] = lg->ids[--lg->count]; return 1; } return 0; }",
    "int ledger_live(const ledger_t *lg) { return lg->count; }",
    "int ledger_audit(const ledger_t *lg) { if (lg->count < 0 || lg->count > LEDGER_CAP) return 0; for (int i = 0; i < lg->count; i++) for (int j = i + 1; j < lg->count; j++) if (lg->ids[i] == lg->ids[j]) return 0; return 1; }",
    "int main(void) { return 0; }",
)
w16 = r16.replace(
    "int ledger_live(const ledger_t *lg) { return lg->count; }",
    "int ledger_live(const ledger_t *lg) { return lg->count + 1; }",
)
lines_out.append(emit("ca16-checkpoint-ledger", r16, w16))

with open(P, "a", encoding="utf-8") as f:
    f.write(NL.join([""] + lines_out))

print("appended", len(lines_out), "R/W pairs")
