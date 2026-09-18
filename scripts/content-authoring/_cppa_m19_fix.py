#!/usr/bin/env python3
"""Module 19 fixes: per-challenge ledger tuples, mid-flight bus batteries, real W defects."""
import ast
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
p = "cppa_m19_21.py"
src = open(p).read()
Q3 = "'" * 3

# ---------------------------------------------------------------- impls
R_TB = """TokenBucket::TokenBucket(const Clock* clock, std::int64_t capacity, std::int64_t refillPerSec)
    : clock_(clock), capacity_(capacity), refillPerSec_(refillPerSec), tokens_(double(capacity)), lastMs_(clock->nowMs()) {}
bool TokenBucket::tryConsume() {
    const std::int64_t now = clock_->nowMs();
    tokens_ = std::min(double(capacity_), tokens_ + (now - lastMs_) / 1000.0 * refillPerSec_);
    lastMs_ = now;
    if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }
    return false;
}
std::int64_t TokenBucket::tokens() const { return std::int64_t(tokens_); }"""

W_TB = R_TB.replace(
    "    lastMs_ = now;\n",
    "    // WRONG: lastMs_ never advances — refill computed from a stale epoch\n",
)
assert W_TB != R_TB, "W_tb variant"

R_EB = """int EventBus::subscribe(Handler h) { int id = nextId_++; handlers_.emplace_back(id, std::move(h)); return id; }
bool EventBus::unsubscribe(int id) {
    for (auto it = handlers_.begin(); it != handlers_.end(); ++it)
        if (it->first == id) { handlers_.erase(it); return true; }
    return false;
}
void EventBus::emit(const std::string& event) const {
    auto snapshot = handlers_;
    for (auto& [id, h] : snapshot) {
        auto it = std::find_if(handlers_.begin(), handlers_.end(),
                               [id](const auto& p) { return p.first == id; });
        if (it != handlers_.end()) h(event);
    }
}"""

W_EB = R_EB.replace(
    """    auto snapshot = handlers_;
    for (auto& [id, h] : snapshot) {
        auto it = std::find_if(handlers_.begin(), handlers_.end(),
                               [id](const auto& p) { return p.first == id; });
        if (it != handlers_.end()) h(event);
    }""",
    """    // WRONG: snapshot without re-check — a handler cut mid-flight still fires
    auto snapshot = handlers_;
    for (auto& [id, h] : snapshot) h(event);""",
)
assert W_EB != R_EB, "W_eb variant"

R_CL = """void ConfigLadder::set(Layer l, const std::string& key, const std::string& value) {
    auto it = entries_.find(key);
    if (it == entries_.end() || int(l) >= int(it->second.first))
        entries_[key] = {l, value};
}
std::optional<std::string> ConfigLadder::get(const std::string& key) const {
    auto it = entries_.find(key);
    if (it == entries_.end()) return std::nullopt;
    return it->second.second;
}
std::optional<Layer> ConfigLadder::source(const std::string& key) const {
    auto it = entries_.find(key);
    if (it == entries_.end()) return std::nullopt;
    return it->second.first;
}"""

W_CL = R_CL.replace(
    "    if (it == entries_.end() || int(l) >= int(it->second.first))\n        entries_[key] = {l, value};",
    "    entries_[key] = {l, value};                       // WRONG: last-writer-wins, layers ignored",
)
assert W_CL != R_CL, "W_cl variant"


def blob(tb, eb, cl):
    return "\n".join([tb, eb, cl])


R_FULL = blob(R_TB, R_EB, R_CL)
W_FULL_TB = blob(W_TB, R_EB, R_CL)
W_FULL_EB = blob(R_TB, W_EB, R_CL)
W_FULL_CL = blob(R_TB, R_EB, W_CL)

# 1) practice event-bus battery: add a mid-flight unsubscribe block
old_tail = '    CHECK_EQ(log[0], "a:again");\n}' + Q3 + ","
new_tail = (
    '    CHECK_EQ(log[0], "a:again");\n'
    "}\n"
    "{\n"
    "    EventBus bus;\n"
    "    std::vector<std::string> log;\n"
    "    int cId = 0;\n"
    '    bus.subscribe([&](const std::string& e) { log.push_back("a:" + e); if (e == "cut") bus.unsubscribe(cId); });\n'
    '    bus.subscribe([&](const std::string& e) { log.push_back("b:" + e); });\n'
    '    cId = bus.subscribe([&](const std::string& e) { log.push_back("c:" + e); });\n'
    '    bus.emit("cut");\n'
    "    CHECK_EQ(log.size(), 2);                       // c was cut mid-flight\n"
    '    CHECK_EQ(log[0], "a:cut"); CHECK_EQ(log[1], "b:cut");\n'
    "}"
    + Q3
    + ","
)
assert src.count(old_tail) == 1, "practice eb battery anchor"
src = src.replace(old_tail, new_tail)

# 2) config-ladder battery: lower-layer-over-existing + equal-layer re-set
old_cl = '    CHECK_EQ(c.get("other").value_or("?"), "x");\n}' + Q3 + ","
new_cl = (
    '    CHECK_EQ(c.get("other").value_or("?"), "x");\n'
    '    c.set(Layer::Env, "port", "5555");              // lower layer speaks last for an existing key\n'
    '    CHECK_EQ(c.get("port").value_or("?"), "6060");   // Flag still wins\n'
    '    CHECK(c.source("port").value_or(Layer::Default) == Layer::Flag);\n'
    '    c.set(Layer::Flag, "port", "6161");             // equal layer re-set overwrites\n'
    '    CHECK_EQ(c.get("port").value_or("?"), "6161");\n'
    "}"
    + Q3
    + ","
)
n_cl = src.count(old_cl)
assert n_cl in (1, 2), "config battery anchor"
src = src.replace(old_cl, new_cl)
print(f"config battery patched in {n_cl} place(s)")

# 3) checkpoint battery: real mid-flight unsubscribe
cp_start = src.index('("interleaved battery",')
cp_hint = 'ids are never reused."),'
cp_end = src.index(cp_hint, cp_start) + len(cp_hint)
new_cp = (
    '("interleaved + mid-flight battery",\n'
    "             r" + Q3 + "{\n"
    "    EventBus bus;\n"
    "    std::vector<std::string> log;\n"
    "    int aId = 0;\n"
    "    int cId = 0;\n"
    '    aId = bus.subscribe([&](const std::string& e) {\n'
    '        log.push_back("a:" + e);\n'
    '        if (e == "boom") { bus.unsubscribe(cId); bus.unsubscribe(aId); }\n'
    "    });\n"
    '    bus.subscribe([&](const std::string& e) { log.push_back("b:" + e); });\n'
    '    cId = bus.subscribe([&](const std::string& e) { log.push_back("c:" + e); });\n'
    '    bus.emit("ok");\n'
    "    CHECK_EQ(log.size(), 3);\n"
    '    CHECK_EQ(log[0], "a:ok"); CHECK_EQ(log[1], "b:ok"); CHECK_EQ(log[2], "c:ok");\n'
    "    log.clear();\n"
    '    bus.emit("boom");\n'
    "    CHECK_EQ(log.size(), 2);                       // c was cut mid-flight\n"
    '    CHECK_EQ(log[0], "a:boom"); CHECK_EQ(log[1], "b:boom");\n'
    "    log.clear();\n"
    '    bus.emit("again");\n'
    "    CHECK_EQ(log.size(), 1);                       // a cut itself; only b remains\n"
    '    CHECK_EQ(log[0], "b:again");\n'
    "}" + Q3 + ",\n"
    '             "Snapshot then membership-check: emit iterates a copy but re-checks each id against the live list right before firing; ids are never reused."),'
)
src = src[:cp_start] + new_cp + src[cp_end:]

# 4) M19_PRAC1_SOL: two per-challenge tuples
p1_start = src.index("M19_PRAC1_SOL = [")
p1_end = src.index("M19_PRAC2_CH = [", p1_start)
new_p1 = (
    "M19_PRAC1_SOL = [\n"
    '    ("cppa19-token-bucket",\n'
    "     CP19_BOILER + " + repr(R_FULL) + ",\n"
    "     CP19_BOILER + " + repr(W_FULL_TB) + "),\n"
    '    ("cppa19-event-bus",\n'
    "     CP19_BOILER + " + repr(R_FULL) + ",\n"
    "     CP19_BOILER + " + repr(W_FULL_EB) + "),\n"
    "]\n\n"
)
src = src[:p1_start] + new_p1 + src[p1_end:]

# 5) M19_PRAC2_SOL: per-challenge tuple with a real W
p2_start = src.index("M19_PRAC2_SOL = [")
p2_end = src.index("# ConfigLadder private members", p2_start)
new_p2 = (
    "M19_PRAC2_SOL = [\n"
    '    ("cppa19-config-ladder",\n'
    "     CP19_BOILER + " + repr(R_FULL) + ",\n"
    "     CP19_BOILER + " + repr(W_FULL_CL) + "),\n"
    "]\n\n"
)
src = src[:p2_start] + new_p2 + src[p2_end:]

# 6) checkpoint wrong= -> snapshot-without-recheck variant
w_start = src.rindex("wrong=CP19_BOILER")
w_end = src.rindex(")\n\nprint(")
src = src[:w_start] + "wrong=CP19_BOILER + " + repr(W_FULL_EB) + ",\n" + src[w_end:]

ast.parse(src)
open(p, "w").write(src)
print("module-19 patch applied")
