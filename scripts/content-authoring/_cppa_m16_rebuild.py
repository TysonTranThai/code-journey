#!/usr/bin/env python3
"""Rebuild the cppa16-opaque-factory solution tuple cleanly (R: idempotent slot destroy + fillApi; W: missing *slot check)."""
import ast
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

p = "cppa_m15_16.py"
src = open(p).read()

start = src.find('("cppa16-opaque-factory",')
assert start > 0, "tuple start"
wp = src.find("write_practice(", start)
assert wp > start
end = src.find("\n]", start)
assert start < end < wp, "tuple end"

WIDGET = (
    "\\nstruct Widget::Impl { std::string keys[64]; std::int64_t vals[64]; std::size_t n = 0; };"
    "\\nWidget::Widget() : impl_(new Impl()) {}"
    "\\nWidget::~Widget() { delete impl_; }"
    "\\nWidget::Widget(Widget&& other) noexcept : impl_(other.impl_) { other.impl_ = nullptr; }"
    "\\nWidget& Widget::operator=(Widget&& other) noexcept {"
    "\\n    if (this != &other) { delete impl_; impl_ = other.impl_; other.impl_ = nullptr; }"
    "\\n    return *this;"
    "\\n}"
    "\\nvoid Widget::set(const std::string& key, std::int64_t value) {"
    "\\n    if (!impl_) impl_ = new Impl();"
    "\\n    for (std::size_t i = 0; i < impl_->n; ++i)"
    "\\n        if (impl_->keys[i] == key) { impl_->vals[i] = value; return; }"
    "\\n    if (impl_->n < 64) { impl_->keys[impl_->n] = key; impl_->vals[impl_->n] = value; ++impl_->n; }"
    "\\n}"
    "\\nstd::int64_t Widget::get(const std::string& key) const {"
    "\\n    if (!impl_) return 0;"
    "\\n    for (std::size_t i = 0; i < impl_->n; ++i)"
    "\\n        if (impl_->keys[i] == key) return impl_->vals[i];"
    "\\n    return 0;"
    "\\n}"
    "\\nstd::size_t Widget::size() const { return impl_ ? impl_->n : 0; }"
)

FILL = (
    "\\nextern \"C\" void wapiFillApi(WidgetApi* api) {"
    "\\n    if (!api) return;"
    "\\n    api->version = 1;"
    "\\n    api->get = apiGet;"
    "\\n    api->set = apiSet;"
    "\\n}"
)

R_BODY = (
    WIDGET
    + "\\nstruct WHandle { Widget* w; };"
    + "\\nstruct WSlot { WHandle* h; };"
    + "\\nextern \"C\" void* wapiCreate() { return new WSlot{new WHandle{new Widget()}}; }"
    + "\\nextern \"C\" void wapiDestroy(void** slot) {"
    + "\\n    if (!slot || !*slot) return;                      // idempotent"
    + "\\n    WSlot* s = static_cast<WSlot*>(*slot);"
    + "\\n    delete s->h->w;"
    + "\\n    delete s->h;"
    + "\\n    delete s;"
    + "\\n    *slot = nullptr;                                  // null the caller slot"
    + "\\n}"
    + "\\nstatic std::int64_t apiGet(void* self, const char* key) {"
    + "\\n    WSlot* s = static_cast<WSlot*>(self);"
    + "\\n    return (s && s->h) ? s->h->w->get(key) : 0;"
    + "\\n}"
    + "\\nstatic void apiSet(void* self, const char* key, std::int64_t v) {"
    + "\\n    WSlot* s = static_cast<WSlot*>(self);"
    + "\\n    if (s && s->h) s->h->w->set(key, v);"
    + "\\n}"
    + FILL
    + "\\n"
)

W_BODY = (
    WIDGET
    + "\\nstruct WHandle { Widget* w; };"
    + "\\nstruct WSlotW { WHandle* h; };"
    + "\\nextern \"C\" void* wapiCreate() { return new WSlotW{new WHandle{new Widget()}}; }"
    + "\\nextern \"C\" void wapiDestroy(void** slot) {"
    + "\\n    if (!slot) return;"
    + "\\n    WSlotW* s = static_cast<WSlotW*>(*slot);          // WRONG: no *slot check — second destroy double-frees"
    + "\\n    delete s->h->w;"
    + "\\n    delete s->h;"
    + "\\n    delete s;"
    + "\\n}"
    + "\\nstatic std::int64_t apiGet(void* self, const char* key) {"
    + "\\n    WSlotW* s = static_cast<WSlotW*>(self);"
    + "\\n    return (s && s->h) ? s->h->w->get(key) : 0;"
    + "\\n}"
    + "\\nstatic void apiSet(void* self, const char* key, std::int64_t v) {"
    + "\\n    WSlotW* s = static_cast<WSlotW*>(self);"
    + "\\n    if (s && s->h) s->h->w->set(key, v);"
    + "\\n}"
    + FILL
    + "\\n"
)

NEW = ('("cppa16-opaque-factory",\n     CP16_BOILER + \'' + R_BODY + "',\n     CP16_BOILER + '" + W_BODY + "'),\n]")

src = src[:start] + NEW + src[end + 2:]
open(p, "w").write(src)
ast.parse(src)
print("tuple rebuilt cleanly, syntax OK")
