#!/usr/bin/env python3
"""Module 12 practices: env, release, incident. Raw strings + json.dumps throughout."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "production"

# ── env-practice ────────────────────────────────────────────────────────────
write_practice(
    MOD, "env-practice",
    "Environment Configuration — Practice",
    "Make the twelve-factor contract executable: read config from env, fail fast on missing pieces, and build a config loader you would trust in production.",
    "Cấu hình môi trường — Luyện tập",
    "Biến hợp đồng twelve-factor thành code chạy được: đọc config từ env, fail fast khi thiếu, và viết một config loader đủ tin cậy cho production.",
    "dev-vs-prod", 16, "intermediate",
    [
        {
            "id": "i2-read-env",
            "title": "Env Reader with Fail-Fast",
            "prompt": 'Write `readEnv(env, required)` — env is a plain object standing in for process.env; required is an array of key names. Return the full env object, but throw an Error naming EVERY missing key (comma-separated) instead of failing later at runtime. Missing means absent, empty string, or undefined.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function readEnv(env, required) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "collects all missing keys into one error",
                    "code": fn_wrap("readEnv", "readEnv") + r'''
try {
  readEnv({ PORT: "3000" }, ["PORT", "DATABASE_URL", "SESSION_SECRET"]);
  throw new Error("should have thrown");
} catch (e) {
  if (!e.message.includes("DATABASE_URL") || !e.message.includes("SESSION_SECRET")) {
    throw new Error("Error must name every missing key.");
  }
  if (e.message.includes("PORT")) throw new Error("Present keys must not be flagged.");
}
''',
                    "hint": "Filter first, then throw once with the joined list — fail fast, but fail completely.",
                },
                {
                    "name": "treats empty string as missing",
                    "code": fn_wrap("readEnv", "readEnv") + r'''
try {
  readEnv({ TOKEN: "" }, ["TOKEN"]);
  throw new Error("should have thrown");
} catch (e) {
  if (!e.message.includes("TOKEN")) throw new Error("Empty string counts as missing.");
}
if (readEnv({ TOKEN: "x" }, ["TOKEN"]) !== undefined) {
  // returns env-ish value; just ensure no throw
}
''',
                    "hint": "An empty variable is set to nothing — it cannot configure anything.",
                },
                {
                    "name": "passes through when complete",
                    "code": fn_wrap("readEnv", "readEnv") + r'''
const env = { A: "1", B: "2" };
const out = readEnv(env, ["A", "B"]);
if (out.A !== "1" || out.B !== "2") throw new Error("Complete config passes through untouched.");
''',
                    "hint": "No missing keys — return the config so the caller can keep working.",
                },
            ],
        },
        {
            "id": "i2-config-loader",
            "title": "Typed Config Loader",
            "prompt": 'Write `loadConfig(env)` that converts raw env strings into a typed config object: port (number, default 3000 when absent), databaseUrl (string), debug (boolean — true only for exactly the string "true"), and features (array from a comma-separated FEATURES value; absent => []). Throw on a non-numeric PORT rather than silently defaulting.',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "function loadConfig(env) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "coerces types with the documented rules",
                    "code": fn_wrap("loadConfig", "loadConfig") + r'''
const c = loadConfig({ PORT: "8080", DATABASE_URL: "postgres://x", DEBUG: "true", FEATURES: "dark-mode,export" });
if (c.port !== 8080 || typeof c.port !== "number") throw new Error("PORT becomes a number.");
if (c.debug !== true) throw new Error('DEBUG is true only for the exact string "true".');
if (c.features.length !== 2 || c.features[1] !== "export") throw new Error("FEATURES splits on commas.");
''',
                    "hint": "Number(), === \"true\", split(\",\") — each field states its own rule.",
                },
                {
                    "name": "defaults without lying",
                    "code": fn_wrap("loadConfig", "loadConfig") + r'''
const c = loadConfig({});
if (c.port !== 3000) throw new Error("Absent PORT defaults to 3000.");
if (c.debug !== false) throw new Error("Absent DEBUG is false.");
if (!Array.isArray(c.features) || c.features.length !== 0) throw new Error("Absent FEATURES => empty array.");
''',
                    "hint": "Defaults are part of the contract — they must be explicit and consistent.",
                },
                {
                    "name": "rejects garbage instead of guessing",
                    "code": fn_wrap("loadConfig", "loadConfig") + r'''
try {
  loadConfig({ PORT: "eight-thousand" });
  throw new Error("should have thrown");
} catch (e) {
  if (!/port/i.test(e.message)) throw new Error("Error must mention PORT.");
}
''',
                    "hint": "Number(\"eight-thousand\") is NaN — catch it and say which field broke.",
                },
            ],
        },
    ],
    {
        "i2-read-env": {"title": "Trình đọc env fail-fast", "prompt": 'Viết `readEnv(env, required)` — env là object thay cho process.env; required là mảng tên khoá. Trả về nguyên object env, nhưng ném Error liệt kê TẤT CẢ khoá bị thiếu (cách nhau bằng dấu phẩy) thay vì để lỗi nổ ra lúc chạy. Thiếu nghĩa là: không tồn tại, chuỗi rỗng, hoặc undefined.'},
        "i2-config-loader": {"title": "Config loader có kiểu", "prompt": 'Viết `loadConfig(env)` biến chuỗi env thô thành config có kiểu: port (number, mặc định 3000 khi vắng), databaseUrl (string), debug (boolean — true chỉ khi đúng chuỗi "true"), features (mảng từ FEATURES phân tách bằng dấu phẩy; vắng => []). Ném lỗi khi PORT không phải số thay vì âm thầm dùng mặc định.'},
    },
    solutions=[
        (
            "i2-read-env",
            "function readEnv(env, required) {\n  const missing = required.filter((k) => env[k] === undefined || env[k] === \"\");\n  if (missing.length > 0) {\n    throw new Error(\"Missing required env vars: \" + missing.join(\", \"));\n  }\n  return env;\n}",
            "function readEnv(env, required) {\n  for (const k of required) {\n    if (!(k in env)) throw new Error(\"Missing \" + k);\n  }\n  return env;\n}",
        ),
        (
            "i2-config-loader",
            "function loadConfig(env) {\n  let port = 3000;\n  if (env.PORT !== undefined) {\n    port = Number(env.PORT);\n    if (Number.isNaN(port)) throw new Error(\"PORT must be a number, got: \" + env.PORT);\n  }\n  return {\n    port,\n    databaseUrl: env.DATABASE_URL || \"\",\n    debug: env.DEBUG === \"true\",\n    features: env.FEATURES ? env.FEATURES.split(\",\") : [],\n  };\n}",
            "function loadConfig(env) {\n  return {\n    port: Number(env.PORT),\n    databaseUrl: env.DATABASE_URL,\n    debug: Boolean(env.DEBUG),\n    features: env.FEATURES.split(\",\"),\n  };\n}",
        ),
    ],
)

# ── release-practice ────────────────────────────────────────────────────────
write_practice(
    MOD, "release-practice",
    "Release Engineering — Practice",
    "Decide how changes reach users: release readiness, rollback versus fix-forward, and canary cohort selection.",
    "Kỹ thuật phát hành — Luyện tập",
    "Quyết định thay đổi đến tay người dùng thế nào: độ sẵn sàng phát hành, rollback hay fix-forward, và chọn nhóm canary.",
    "cicd-loop", 16, "intermediate",
    [
        {
            "id": "i2-release-gate",
            "title": "Release Gate",
            "prompt": 'Write `canRelease(checks)` — checks is an object like { ci: bool, migrations: bool, smoke: bool, reviewers: number }. Return "yes" only when ci, migrations and smoke are all true AND reviewers >= 1. Otherwise return the FIRST failing gate name: "ci", "migrations", "smoke", or "review".',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function canRelease(checks) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "all green releases",
                    "code": fn_wrap("canRelease", "canRelease") + r'''
if (canRelease({ ci: true, migrations: true, smoke: true, reviewers: 2 }) !== "yes") {
  throw new Error("All gates pass => release.");
}
''',
                    "hint": "One condition, four clauses.",
                },
                {
                    "name": "reports the first failing gate in order",
                    "code": fn_wrap("canRelease", "canRelease") + r'''
if (canRelease({ ci: false, migrations: false, smoke: false, reviewers: 0 }) !== "ci") {
  throw new Error("Order matters: ci first.");
}
if (canRelease({ ci: true, migrations: false, smoke: false, reviewers: 0 }) !== "migrations") {
  throw new Error("Then migrations.");
}
if (canRelease({ ci: true, migrations: true, smoke: false, reviewers: 0 }) !== "smoke") {
  throw new Error("Then smoke.");
}
if (canRelease({ ci: true, migrations: true, smoke: true, reviewers: 0 }) !== "review") {
  throw new Error("Then review.");
}
''',
                    "hint": "Check gates in a fixed order and return the first failure — deterministic triage.",
                },
            ],
        },
        {
            "id": "i2-rollback-or-fix",
            "title": "Rollback or Fix-Forward",
            "prompt": 'Write `respond(incident)` — incident is { dataLoss: bool, fixReady: bool, mitigationWorks: bool }. Rules: if dataLoss => "rollback" always (protect data first). Otherwise if mitigationWorks && fixReady => "fix-forward". Otherwise if mitigationWorks && !fixReady => "feature-off" (ship the mitigation now, fix later). Otherwise => "rollback".',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function respond(incident) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "data loss always rolls back",
                    "code": fn_wrap("respond", "respond") + r'''
if (respond({ dataLoss: true, fixReady: true, mitigationWorks: true }) !== "rollback") {
  throw new Error("Data loss => rollback, no exceptions.");
}
if (respond({ dataLoss: true, fixReady: false, mitigationWorks: false }) !== "rollback") {
  throw new Error("Even with nothing ready — protect the data.");
}
''',
                    "hint": "The first rule has no exceptions.",
                },
                {
                    "name": "healthy incidents resolve forward",
                    "code": fn_wrap("respond", "respond") + r'''
if (respond({ dataLoss: false, fixReady: true, mitigationWorks: true }) !== "fix-forward") {
  throw new Error("Mitigation works and fix ready => fix forward.");
}
if (respond({ dataLoss: false, fixReady: false, mitigationWorks: true }) !== "feature-off") {
  throw new Error("Mitigation only => disable the feature now, fix later.");
}
if (respond({ dataLoss: false, fixReady: true, mitigationWorks: false }) !== "rollback") {
  throw new Error("Nothing mitigates => roll back.");
}
''',
                    "hint": "Mitigation is the pivot: works => forward-ish, does not => rollback.",
                },
            ],
        },
        {
            "id": "i2-canary-cohort",
            "title": "Canary Cohort Picker",
            "prompt": 'Write `canaryFor(user, rollout)` — user is { id: string, internal: bool, betaOptIn: bool }, rollout is { percent, excludeInternals: bool }. A user is in the canary if: internals are in whenever excludeInternals is false; betaOptIn users are always in; otherwise hash(id) % 100 < percent (hash is provided in the boilerplate). Return true/false.',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "function hash(s) {\n  let h = 0;\n  for (let i = 0; i < s.length; i++) {\n    h = (h * 31 + s.charCodeAt(i)) >>> 0;\n  }\n  return h;\n}\n\nfunction canaryFor(user, rollout) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "opt-in always wins",
                    "code": fn_wrap("canaryFor", "canaryFor") + r'''
if (canaryFor({ id: "u1", internal: true, betaOptIn: true }, { percent: 0, excludeInternals: true }) !== true) {
  throw new Error("Beta opt-in is in even at 0%.");
}
''',
                    "hint": "Check opt-in before anything else.",
                },
                {
                    "name": "internals respect exclusion",
                    "code": fn_wrap("canaryFor", "canaryFor") + r'''
if (canaryFor({ id: "u2", internal: true, betaOptIn: false }, { percent: 100, excludeInternals: true }) !== false) {
  throw new Error("Excluded internals are never canary.");
}
if (canaryFor({ id: "u3", internal: true, betaOptIn: false }, { percent: 100, excludeInternals: false }) !== true) {
  throw new Error("At 100% with no exclusion, internals are in.");
}
''',
                    "hint": "Exclusion only applies to non-opted-in internals.",
                },
                {
                    "name": "percentage gate is deterministic",
                    "code": fn_wrap("canaryFor", "canaryFor") + r'''
const u = { id: "abc", internal: false, betaOptIn: false };
const expected = hash("abc") % 100 < 50;
if (canaryFor(u, { percent: 50, excludeInternals: false }) !== expected) {
  throw new Error("Must match hash(id) % 100 < percent exactly.");
}
if (canaryFor({ id: "zz", internal: false, betaOptIn: false }, { percent: 0, excludeInternals: false }) !== false) {
  throw new Error("0% lets nobody in.");
}
''',
                    "hint": "Use the provided hash — determinism is the point (same user, same bucket).",
                },
            ],
        },
    ],
    {
        "i2-release-gate": {"title": "Cổng phát hành", "prompt": 'Viết `canRelease(checks)` — checks là object dạng { ci: bool, migrations: bool, smoke: bool, reviewers: number }. Trả về "yes" chỉ khi ci, migrations, smoke đều true VÀ reviewers >= 1. Ngược lại trả về tên cổng chặn ĐẦU TIÊN: "ci", "migrations", "smoke", hoặc "review".'},
        "i2-rollback-or-fix": {"title": "Rollback hay fix-forward", "prompt": 'Viết `respond(incident)` — incident là { dataLoss: bool, fixReady: bool, mitigationWorks: bool }. Quy tắc: nếu dataLoss => "rollback" luôn luôn (bảo vệ dữ liệu trước). Nếu không: mitigationWorks && fixReady => "fix-forward"; mitigationWorks && !fixReady => "feature-off" (đưa mitigation lên trước, sửa sau). Còn lại => "rollback".'},
        "i2-canary-cohort": {"title": "Chọn nhóm canary", "prompt": 'Viết `canaryFor(user, rollout)` — user là { id: string, internal: bool, betaOptIn: bool }, rollout là { percent, excludeInternals: bool }. User nằm trong canary khi: internal được vào khi excludeInternals là false; user betaOptIn luôn luôn vào; còn lại hash(id) % 100 < percent (hàm hash có sẵn trong boilerplate). Trả về true/false.'},
    },
    solutions=[
        (
            "i2-release-gate",
            "function canRelease(checks) {\n  if (!checks.ci) return \"ci\";\n  if (!checks.migrations) return \"migrations\";\n  if (!checks.smoke) return \"smoke\";\n  if (checks.reviewers < 1) return \"review\";\n  return \"yes\";\n}",
            "function canRelease(checks) {\n  if (checks.ci && checks.migrations && checks.smoke && checks.reviewers >= 1) return \"yes\";\n  return \"blocked\";\n}",
        ),
        (
            "i2-rollback-or-fix",
            "function respond(incident) {\n  if (incident.dataLoss) return \"rollback\";\n  if (incident.mitigationWorks && incident.fixReady) return \"fix-forward\";\n  if (incident.mitigationWorks) return \"feature-off\";\n  return \"rollback\";\n}",
            "function respond(incident) {\n  if (incident.fixReady) return \"fix-forward\";\n  if (incident.mitigationWorks) return \"feature-off\";\n  return \"rollback\";\n}",
        ),
        (
            "i2-canary-cohort",
            "function canaryFor(user, rollout) {\n  if (user.betaOptIn) return true;\n  if (user.internal && rollout.excludeInternals) return false;\n  return hash(user.id) % 100 < rollout.percent;\n}",
            "function canaryFor(user, rollout) {\n  return hash(user.id) % 100 < rollout.percent;\n}",
        ),
    ],
)

# ── incident-practice ───────────────────────────────────────────────────────
write_practice(
    MOD, "incident-practice",
    "Observability & Incidents — Practice",
    "Build the reflexes: log structure that survives grep, health checks that mean something, and alert triage that respects sleep.",
    "Quan sát & sự cố — Luyện tập",
    "Xây dựng phản xạ: log có cấu trúc sống sót qua grep, health check có ý nghĩa thật, và phân loại alert tôn trọng giấc ngủ.",
    "observability", 15, "intermediate",
    [
        {
            "id": "i2-structured-log",
            "title": "Structured Log Line",
            "prompt": 'Write `logLine(level, event, fields)` returning a single JSON string: {"ts": <fixedTimestamp>, "level": level, "event": event, ...fields}. fixedTimestamp (provided in boilerplate) keeps tests deterministic. Fields spread AFTER level/event so they cannot overwrite them. Invalid level (not "debug"/"info"/"warn"/"error") => throw.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "const fixedTimestamp = 1700000000000;\n\nfunction logLine(level, event, fields) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "JSON with fixed ts and spread fields",
                    "code": fn_wrap("logLine", "logLine") + r'''
const line = logLine("info", "request.completed", { path: "/api/tasks", ms: 42 });
const parsed = JSON.parse(line);
if (parsed.ts !== 1700000000000) throw new Error("ts comes from the fixed timestamp.");
if (parsed.level !== "info" || parsed.event !== "request.completed") throw new Error("level and event present.");
if (parsed.path !== "/api/tasks" || parsed.ms !== 42) throw new Error("Extra fields spread in.");
''',
                    "hint": "JSON.stringify({ ts: fixedTimestamp, level, event, ...fields }).",
                },
                {
                    "name": "fields cannot shadow the envelope",
                    "code": fn_wrap("logLine", "logLine") + r'''
const parsed = JSON.parse(logLine("error", "db.timeout", { level: "debug", event: "hijack" }));
if (parsed.level !== "error") throw new Error("Malicious/sloppy fields must not overwrite level.");
if (parsed.event !== "db.timeout") throw new Error("Event must survive the spread.");
''',
                    "hint": "Spread order decides ownership: envelope first, fields after — or is it the other way? Make the envelope win.",
                },
                {
                    "name": "invalid level throws",
                    "code": fn_wrap("logLine", "logLine") + r'''
try {
  logLine("LOUD", "x", {});
  throw new Error("should have thrown");
} catch (e) {
  if (!/level/i.test(e.message)) throw new Error("Error must mention level.");
}
''',
                    "hint": "Validate against the four allowed levels.",
                },
            ],
        },
        {
            "id": "i2-health-checks",
            "title": "Liveness vs Readiness",
            "prompt": 'Write `healthZ(state)` and `readyZ(state)` — state is { crashed: bool, dbUp: bool, cacheUp: bool }. healthZ: 503 only when crashed (liveness = process alive; dependencies do not matter). readyZ: 200 only when dbUp AND cacheUp (readiness = can serve correctly). Return numbers.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function healthZ(state) {\n  // your code\n}\n\nfunction readyZ(state) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "liveness ignores dependencies",
                    "code": fn_wrap("healthZ", "healthZ") + r'''
if (healthZ({ crashed: false, dbUp: false, cacheUp: false }) !== 200) {
  throw new Error("Alive process is 200 even with every dependency down.");
}
if (healthZ({ crashed: true, dbUp: true, cacheUp: true }) !== 503) {
  throw new Error("Crashed process is 503.");
}
''',
                    "hint": "Only `crashed` matters for liveness.",
                },
                {
                    "name": "readiness requires dependencies",
                    "code": fn_wrap("readyZ", "readyZ") + r'''
if (readyZ({ crashed: false, dbUp: true, cacheUp: true }) !== 200) throw new Error("All up => ready.");
if (readyZ({ crashed: false, dbUp: false, cacheUp: true }) !== 503) throw new Error("DB down => not ready.");
if (readyZ({ crashed: false, dbUp: true, cacheUp: false }) !== 503) throw new Error("Cache down => not ready.");
''',
                    "hint": "Both dependencies must be up.",
                },
            ],
        },
        {
            "id": "i2-alert-triage",
            "title": "Alert Triage",
            "prompt": 'Write `triage(alert)` — alert is { kind, actionable: bool, urgent: bool }. Rules: actionable && urgent => "page" (wake a human); actionable && !urgent => "ticket" (fix in hours); otherwise "dashboard" (noise — chart it, do not alert).',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function triage(alert) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "three outcomes from two booleans",
                    "code": fn_wrap("triage", "triage") + r'''
if (triage({ kind: "5xx-spike", actionable: true, urgent: true }) !== "page") throw new Error("Real incident => page.");
if (triage({ kind: "slow-query", actionable: true, urgent: false }) !== "ticket") throw new Error("Fixable, not urgent => ticket.");
if (triage({ kind: "noise", actionable: false, urgent: false }) !== "dashboard") throw new Error("Noise => dashboard.");
if (triage({ kind: "flap", actionable: false, urgent: true }) !== "dashboard") throw new Error("Urgent noise is still noise.");
''',
                    "hint": "actionable is the gate; urgency only matters when actionable.",
                },
            ],
        },
    ],
    {
        "i2-structured-log": {"title": "Dòng log có cấu trúc", "prompt": 'Viết `logLine(level, event, fields)` trả về MỘT chuỗi JSON: {"ts": <fixedTimestamp>, "level": level, "event": event, ...fields}. fixedTimestamp có sẵn trong boilerplate để test ổn định. Fields được spread SAU level/event nhưng envelope phải thắng khi trùng khoá. Level không hợp lệ (không phải "debug"/"info"/"warn"/"error") => ném lỗi.'},
        "i2-health-checks": {"title": "Liveness vs readiness", "prompt": 'Viết `healthZ(state)` và `readyZ(state)` — state là { crashed: bool, dbUp: bool, cacheUp: bool }. healthZ: 503 chỉ khi crashed (liveness = tiến trình còn sống; phụ thuộc không quan trọng). readyZ: 200 chỉ khi dbUp VÀ cacheUp (readiness = phục vụ đúng được). Trả về số.'},
        "i2-alert-triage": {"title": "Phân loại alert", "prompt": 'Viết `triage(alert)` — alert là { kind, actionable: bool, urgent: bool }. Quy tắc: actionable && urgent => "page" (đánh thức con người); actionable && !urgent => "ticket" (sửa trong vài giờ); còn lại "dashboard" (noise — vẽ biểu đồ, không alert).'},
    },
    solutions=[
        (
            "i2-structured-log",
            "function logLine(level, event, fields) {\n  if (![\"debug\", \"info\", \"warn\", \"error\"].includes(level)) {\n    throw new Error(\"Invalid level: \" + level);\n  }\n  return JSON.stringify({ ts: fixedTimestamp, level, event, ...fields, level, event });\n}",
            "function logLine(level, event, fields) {\n  return JSON.stringify({ ...fields, ts: fixedTimestamp, level, event });\n}",
        ),
        (
            "i2-health-checks",
            "function healthZ(state) {\n  return state.crashed ? 503 : 200;\n}\n\nfunction readyZ(state) {\n  return state.dbUp && state.cacheUp ? 200 : 503;\n}",
            "function healthZ(state) {\n  return state.dbUp && state.cacheUp ? 200 : 503;\n}\n\nfunction readyZ(state) {\n  return state.crashed ? 503 : 200;\n}",
        ),
        (
            "i2-alert-triage",
            "function triage(alert) {\n  if (!alert.actionable) return \"dashboard\";\n  return alert.urgent ? \"page\" : \"ticket\";\n}",
            "function triage(alert) {\n  if (alert.urgent) return \"page\";\n  if (alert.actionable) return \"dashboard\";\n  return \"ticket\";\n}",
        ),
    ],
)

print("Module 12 practice sets written.")
