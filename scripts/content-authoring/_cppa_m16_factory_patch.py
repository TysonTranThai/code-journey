#!/usr/bin/env python3
"""Fix cppa16-opaque-factory: add factory decls to CP16_BOILER, void** destroy, patch solutions/tests/hints."""
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

p = "cppa_m15_16.py"
src = open(p).read()

# 1) Declarations into CP16_BOILER (r''' block, real newlines)
old_decl = '''struct WidgetApi {
    std::uint32_t version;          // 1
    std::int64_t (*get)(void* self, const char* key);
    void (*set)(void* self, const char* key, std::int64_t value);
};
\'\'\''''
new_decl = '''struct WidgetApi {
    std::uint32_t version;          // 1
    std::int64_t (*get)(void* self, const char* key);
    void (*set)(void* self, const char* key, std::int64_t value);
};

// Opaque-handle factory contract used by the tests.
extern "C" void* wapiCreate();
extern "C" void  wapiDestroy(void** handle);   // takes the slot: can null it (idempotent)
\'\'\''''
c = src.count(old_decl)
assert c == 1, f"decl anchor {c}"
src = src.replace(old_decl, new_decl)

# 2) test code -> pass the slot
old_test = '''wapiDestroy(h);
wapiDestroy(h);                       // must be a no-op\'\'\''''
new_test = '''wapiDestroy(&h);
wapiDestroy(&h);                      // must be a no-op (and null the slot)\'\'\''''
c = src.count(old_test)
assert c == 1, f"test {c}"
src = src.replace(old_test, new_test)

# 3) R solution (escaped form) -> slot-based idempotent destroy
old_r = ('\\nstruct WHandle { Widget* w; };'
         '\\nextern "C" void* wapiCreate() { return new WHandle{new Widget()}; }'
         '\\nextern "C" void wapiDestroy(void* h) {'
         '\\n    if (!h) return;                                   // idempotent: null slot is a no-op'
         '\\n    WHandle* wh = static_cast<WHandle*>(h);'
         '\\n    delete wh->w;'
         '\\n    delete wh;'
         '\\n}')
new_r = ('\\nstruct WHandle { Widget* w; };'
         '\\nstruct WSlot { WHandle* h; };'
         '\\nextern "C" void* wapiCreate() { return new WSlot{new WHandle{new Widget()}}; }'
         '\\nextern "C" void wapiDestroy(void** slot) {'
         '\\n    if (!slot || !*slot) return;                      // idempotent'
         '\\n    WSlot* s = static_cast<WSlot*>(*slot);'
         '\\n    delete s->h->w;'
         '\\n    delete s->h;'
         '\\n    delete s;'
         '\\n    *slot = nullptr;                                  // null the caller\\\'s slot'
         '\\n}')
c = src.count(old_r)
assert c == 1, f"R {c}"
src = src.replace(old_r, new_r)

# 4) W solution (escaped form) -> destroy without the *slot check
old_w = ('\\nstruct WHandle { Widget* w; };'
         '\\nextern "C" void* wapiCreate() { return new WHandle{new Widget()}; }'
         '\\nextern "C" void wapiDestroy(void* h) {'
         '\\n    WHandle* wh = static_cast<WHandle*>(h);           // WRONG: no null guard — second destroy is a double free'
         '\\n    delete wh->w;'
         '\\n    delete wh;'
         '\\n}')
new_w = ('\\nstruct WHandle { Widget* w; };'
         '\\nstruct WSlotW { WHandle* h; };'
         '\\nextern "C" void* wapiCreate() { return new WSlotW{new WHandle{new Widget()}}; }'
         '\\nextern "C" void wapiDestroy(void** slot) {'
         '\\n    if (!slot) return;'
         '\\n    WSlotW* s = static_cast<WSlotW*>(*slot);          // WRONG: no *slot check — second destroy double-frees'
         '\\n    delete s->h->w;'
         '\\n    delete s->h;'
         '\\n    delete s;'
         '\\n}')
c = src.count(old_w)
assert c == 1, f"W {c}"
src = src.replace(old_w, new_w)

# 5) hints (EN + VI)
old_hint_en = "wapiDestroy: delete then set the caller's handle slot to nullptr — pass void** or make the handle a small struct. A destroy that only deletes cannot be idempotent."
new_hint_en = "wapiDestroy(void** slot): if (!slot || !*slot) return; delete contents; *slot = nullptr. Taking the slot is what makes idempotence possible."
c = src.count(old_hint_en)
assert c == 1, f"hint en {c}"
src = src.replace(old_hint_en, new_hint_en)

old_hint_vi = "wapiDestroy: delete rồi đặt ô handle của caller về nullptr — truyền void** hoặc biến handle thành struct nhỏ. Destroy chỉ delete thì không thể idempotent."
new_hint_vi = "wapiDestroy(void** slot): if (!slot || !*slot) return; delete nội dung; *slot = nullptr. Nhận ô nhớ (slot) mới làm được idempotence."
c = src.count(old_hint_vi)
assert c == 1, f"hint vi {c}"
src = src.replace(old_hint_vi, new_hint_vi)

open(p, "w").write(src)
print("script patched: decl, test, R, W, hints")

# 6) on-disk EN challenge JSON: boilerplate + test code
jp = "../../src/content/tracks/cpp/courses/cpp-advanced/modules/abi-linking/practices/m16-abi-practice/challenges/cppa16-opaque-factory.json"
d = json.load(open(jp))
d["boilerplate"] = d["boilerplate"].rstrip() + '''

// Opaque-handle factory contract used by the tests.
extern "C" void* wapiCreate();
extern "C" void  wapiDestroy(void** handle);   // takes the slot: can null it (idempotent)
'''
for t in d["tests"]:
    t["code"] = t["code"].replace("wapiDestroy(h);", "wapiDestroy(&h);")
json.dump(d, open(jp, "w"), ensure_ascii=False, indent=2)
print("disk json patched")
