#!/usr/bin/env python3
"""One-shot fixer for pypa_m7.py: argrepr-based LOAD_GLOBAL detection + cycle-gc redesign."""
import io

p = "scripts/content-authoring/pypa_m7.py"
s = io.open(p, encoding="utf-8").read()

# ── 1. REF: argrepr-based loop_loads_global ──────────────────────────────────
old_ref = '''    "def loop_loads_global(func, name):\\n"
    "    '''True when func's bytecode references the global `name` from inside
    a loop (opname LOAD_GLOBAL appearing at least twice — once for the
    loop iterable setup is fine, we count references beyond setup).'''\\n"
    "    ops = instruction_names(func)\\n"
    "    return ops.count('LOAD_GLOBAL') >= 2"'''
new_ref = '''    "def loop_loads_global(func, name):\\n"
    "    hits = 0\\n"
    "    for ins in dis.get_instructions(func):\\n"
    "        if ins.opname == 'LOAD_GLOBAL' and ins.argrepr == name:\\n"
    "            hits += 1\\n"
    "    return hits >= 2"'''
assert old_ref in s, "REF block not found"
s = s.replace(old_ref, new_ref)

# ── 2. WRONG: argrepr-blind counter ──────────────────────────────────────────
old_wrong_tail = '''    "def loop_loads_global(func, name):\\n"
    "    return True"'''
new_wrong_tail = '''    "def loop_loads_global(func, name):\\n"
    "    # WRONG: counts ALL LOAD_GLOBALs (len/range included) — the hoisted\\n"
    "    # variant also has 3, so it reports True for everything\\n"
    "    return sum(1 for ins in dis.get_instructions(func) if ins.opname == 'LOAD_GLOBAL') >= 2"'''
assert old_wrong_tail in s, "WRONG tail not found"
s = s.replace(old_wrong_tail, new_wrong_tail)

# ── 3. test: two G refs per loop iteration ──────────────────────────────────
old_test = '''                ("loop-load detection",
                 "G = list(range(10))\\n\\ndef loads_in_loop():\\n    out = []\\n    for i in range(3):\\n        out.append(len(G))\\n    return out\\n\\ndef hoisted():\\n    g = G\\n    out = []\\n    for i in range(3):\\n        out.append(len(g))\\n    return out\\n\\nassert loop_loads_global(loads_in_loop, 'G')\\nassert not loop_loads_global(hoisted, 'G')\\nprint('ok')",
                 "Count LOAD_GLOBAL occurrences: the hoisted version references G once."),'''
new_test = '''                ("loop-load detection via argrepr",
                 "G = list(range(10))\\n\\ndef loads_in_loop():\\n    out = []\\n    for i in range(3):\\n        out.append(len(G))\\n        out.append(G[i])\\n    return out\\n\\ndef hoisted():\\n    g = G\\n    out = []\\n    for i in range(3):\\n        out.append(len(g))\\n        out.append(g[i])\\n    return out\\n\\nassert loop_loads_global(loads_in_loop, 'G'), 'loop version must load G inside the loop'\\nassert not loop_loads_global(hoisted, 'G'), 'hoisted version loads G only once in setup'\\nprint('ok')",
                 "Two G references inside the loop vs one in setup — argrepr distinguishes G from len/range."),'''
assert old_test in s, "loop-load test not found"
s = s.replace(old_test, new_test)

# ── 4. cycle-gc: INV_REF / INV_WRONG / prompt / test / VI ────────────────────
old_inv_ref = '''INV_REF = (
    "import gc\\n\\n\\n"
    "class Node:\\n"
    "    def __init__(self):\\n"
    "        self.partner = None\\n\\n\\n"
    "def cycle_count_after_delete():\\n"
    "    '''Create a detached two-node cycle, drop the references, run gc.collect()
    and return (collected_objects, remaining_unreachable_before_collect).'''\\n"
    "    a, b = Node(), Node()\\n"
    "    a.partner, b.partner = b, a\\n"
    "    del a, b\\n"
    "    n_unreachable = len(gc.garbage)\\n"
    "    collected = gc.collect()\\n"
    "    return collected, n_unreachable"
)'''
new_inv_ref = '''INV_REF = (
    "import gc\\n\\n\\n"
    "class Node:\\n"
    "    def __init__(self):\\n"
    "        self.partner = None\\n\\n\\n"
    "def cycle_probe():\\n"
    "    a, b = Node(), Node()\\n"
    "    a.partner, b.partner = b, a\\n"
    "    partners_wired = a.partner is b and b.partner is a\\n"
    "    del a, b\\n"
    "    collected = gc.collect()\\n"
    "    return collected, partners_wired"
)'''
assert old_inv_ref in s, "INV_REF not found"
s = s.replace(old_inv_ref, new_inv_ref)

old_inv_wrong = '''INV_WRONG = (
    "import gc\\n\\n\\n"
    "class Node:\\n"
    "    def __init__(self):\\n"
    "        self.partner = None\\n\\n\\n"
    "def cycle_count_after_delete():\\n"
    "    '''WRONG: never creates the cycle (no partner wiring) — refcounting
    reclaims the nodes instantly and gc.collect() has nothing to do.'''\\n"
    "    a, b = Node(), Node()\\n"
    "    del a, b\\n"
    "    n_unreachable = len(gc.garbage)\\n"
    "    collected = gc.collect()\\n"
    "    return collected, n_unreachable"
)'''
new_inv_wrong = '''INV_WRONG = (
    "import gc\\n\\n\\n"
    "class Node:\\n"
    "    def __init__(self):\\n"
    "        self.partner = None\\n\\n\\n"
    "def cycle_probe():\\n"
    "    # WRONG: never wires the cycle — refcounting frees both nodes and\\n"
    "    # collect() has nothing cycle-related to reclaim\\n"
    "    a, b = Node(), Node()\\n"
    "    partners_wired = a.partner is b and b.partner is a\\n"
    "    del a, b\\n"
    "    collected = gc.collect()\\n"
    "    return collected, partners_wired"
)'''
assert old_inv_wrong in s, "INV_WRONG not found"
s = s.replace(old_inv_wrong, new_inv_wrong)

# prompt + test + vi for the gc challenge
old_prompt = '''            "pa-int-cycle-gc",
            "Prove the cycle collector works",
            "Implement `cycle_count_after_delete()`:\\n\\n1. Create two `Node` instances whose `partner` attributes reference each other (a cycle).\\n2. Drop your local references (`del` or rebinding).\\n3. Record `len(gc.garbage)` BEFORE collecting.\\n4. Run `gc.collect()` and capture its return value (number of unreachable objects collected).\\n5. Return `(collected, unreachable_before)`.\\n\\nGrading asserts the collector actually reclaimed the cycle (collected > 0 on a fresh interpreter state) — a variant without the cycle wiring collects nothing relevant and fails the assertion `collected >= 2`.",
            "import gc\\n\\nclass Node:\\n    def __init__(self):\\n        self.partner = None\\n\\n# TODO: cycle_count_after_delete()",
            [
                ("cycle is reclaimed by collect()",
                 "collected, before = cycle_count_after_delete()\\nassert collected >= 2, f'collected: {collected} — cycle must be collected'\\nassert isinstance(before, int)\\nprint('ok')",
                 "Wire a.partner = b and b.partner = a BEFORE dropping references; then gc.collect()."),
            ],'''
new_prompt = '''            "pa-int-cycle-gc",
            "Prove the cycle collector works",
            "Implement `cycle_probe()`:\\n\\n1. Create two `Node` instances (class defined below has `partner = None`).\\n2. Wire the cycle: `a.partner = b` and `b.partner = a`.\\n3. Record `partners_wired = a.partner is b and b.partner is a`.\\n4. Drop your local references to BOTH nodes.\\n5. Run `gc.collect()` and capture its return value.\\n6. Return `(collected, partners_wired)`.\\n\\nGrading asserts `partners_wired is True` AND `collected >= 2` — the two mutually-referencing nodes are only reclaimable by the cycle collector.",
            "import gc\\n\\nclass Node:\\n    def __init__(self):\\n        self.partner = None\\n\\n# TODO: cycle_probe()",
            [
                ("cycle is wired and reclaimed by collect()",
                 "collected, wired = cycle_probe()\\nassert wired is True, f'wired: {wired}'\\nassert collected >= 2, f'collected: {collected} — cycle must be collected'\\nprint('ok')",
                 "Wire a.partner = b and b.partner = a BEFORE dropping references; then gc.collect()."),
            ],'''
assert old_prompt in s, "gc prompt not found"
s = s.replace(old_prompt, new_prompt)

old_vi = '''        "pa-int-cycle-gc": vi_challenge(
            "Chứng minh bộ gom chu kỳ hoạt động",
            "Cài `cycle_count_after_delete()`:\\n\\n1. Tạo hai instance `Node` mà `partner` của chúng trỏ vào nhau (một chu kỳ).\\n2. Bỏ tham chiếu cục bộ (`del` hoặc gán lại).\\n3. Ghi lại `len(gc.garbage)` TRƯỚC khi gom.\\n4. Chạy `gc.collect()` và giữ giá trị trả về (số đối tượng không thể chạm tới đã được gom).\\n5. Trả về `(collected, unreachable_before)`.\\n\\nPhần chấm khẳng định bộ gom thực sự thu hồi chu kỳ (collected > 0 trên trạng thái interpreter sạch) — biến thể không nối chu kỳ sẽ không gom gì liên quan và trượt khẳng định `collected >= 2`.",
            [("Chu kỳ được thu hồi bởi collect()", "Wire a.partner = b và b.partner = a TRƯỚC khi bỏ tham chiếu; rồi gc.collect().")],
        ),'''
new_vi = '''        "pa-int-cycle-gc": vi_challenge(
            "Chứng minh bộ gom chu kỳ hoạt động",
            "Cài `cycle_probe()`:\\n\\n1. Tạo hai instance `Node` (class bên dưới có `partner = None`).\\n2. Nối chu kỳ: `a.partner = b` và `b.partner = a`.\\n3. Ghi `partners_wired = a.partner is b and b.partner is a`.\\n4. Bỏ tham chiếu cục bộ tới CẢ HAI node.\\n5. Chạy `gc.collect()` và giữ giá trị trả về.\\n6. Trả về `(collected, partners_wired)`.\\n\\nPhần chấm khẳng định `partners_wired là True` VÀ `collected >= 2` — hai node trỏ chéo nhau chỉ bộ gom chu kỳ thu hồi được.",
            [("Chu kỳ được nối và được thu hồi bởi collect()", "Nối a.partner = b và b.partner = a TRƯỚC khi bỏ tham chiếu; rồi gc.collect().")],
        ),'''
assert old_vi in s, "gc VI not found"
s = s.replace(old_vi, new_vi)

io.open(p, "w", encoding="utf-8").write(s)
print("m7 fixes applied")
